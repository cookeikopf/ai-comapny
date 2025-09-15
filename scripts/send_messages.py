#!/usr/bin/env python3
"""
Send outreach messages based on prepared drafts.

This script is designed to be triggered by the GitHub Actions workflow
``send_messages.yml``. It reads a comma-separated list of draft paths from
the ``--draft-ids`` argument or ``DRAFT_IDS`` environment variable,
loads the corresponding Markdown files and either simulates or actually
sends them via the configured MCP stubs (e.g. gmail_mcp_stub for email).

Sending messages is always gated behind human approval in GitHub. The
``config/feature_flags.yaml`` file controls whether actual sending is
enabled. When ``allow_outbound_email`` or ``allow_slack_post`` are false,
this script will run in dry-run mode regardless of the ``--dry-run`` flag.

Usage:
  python scripts/send_messages.py --draft-ids outreach/drafts/001.md --dry-run true
"""

import argparse
import os
import sys
from pathlib import Path

import yaml

try:
    from tools.gmail_mcp_stub import GmailMCP
except ImportError:
    # If the stubs cannot be imported, define minimal dummy classes
    class GmailMCP:
        def __init__(self):
            pass
        def send_email(self, to: str, subject: str, body: str):
            print(f"(Stub) Would send email to {to}\nSubject: {subject}\nBody:\n{body}\n")

def load_feature_flags() -> dict:
    ff_path = Path("config/feature_flags.yaml")
    if not ff_path.exists():
        return {}
    with ff_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-ids", help="Comma-separated list of draft paths")
    parser.add_argument("--dry-run", default=os.environ.get("DRY_RUN", "true"), help="If true, simulate sending only")
    args = parser.parse_args()

    raw_ids = args.draft_ids or os.environ.get("DRAFT_IDS", "")
    draft_paths = [d.strip() for d in raw_ids.split(",") if d.strip()]
    dry_run_flag = str(args.dry_run).lower() == "true"

    feature_flags = load_feature_flags()
    allow_email = feature_flags.get("allow_outbound_email", False)
    if not allow_email:
        dry_run_flag = True

    gmail = GmailMCP()

    if not draft_paths:
        print("No draft paths provided", file=sys.stderr)
        return

    for draft in draft_paths:
        draft_path = Path(draft)
        if not draft_path.exists():
            print(f"Draft file {draft_path} not found", file=sys.stderr)
            continue
        raw = draft_path.read_text(encoding="utf-8")

        to = os.environ.get("DEFAULT_TO", "example@example.com")
        subject = "AI Company Outreach"
        content = raw

        if raw.startswith("---"):
            try:
                _, fm, body = raw.split("---", 2)
                meta = yaml.safe_load(fm) or {}
                to = meta.get("to", to)
                subject = meta.get("subject", subject)
                content = body.lstrip()
            except Exception as exc:  # noqa: BLE001
                print(f"Failed to parse front matter in {draft_path}: {exc}", file=sys.stderr)

        preview = content.strip().splitlines()[0][:80] if content.strip() else ""
        if dry_run_flag:
            print(f"DRY RUN - To: {to}\nSubject: {subject}\nPreview: {preview}\n")
        else:
            print(f"Sending email {draft_path} to {to} …")
            gmail.send_email(to=to, subject=subject, body=content)

    if dry_run_flag:
        print("Dry run complete; no emails were sent.")

if __name__ == "__main__":
    main()
