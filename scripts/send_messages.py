#!/usr/bin/env python3
"""
Send outreach messages based on prepared drafts.

This script is designed to be triggered by the GitHub Actions workflow
``send_messages.yml``. It reads a comma‑separated list of draft IDs from
the ``--draft-ids`` argument, loads the corresponding Markdown files from
``outreach/drafts/``, and either simulates or actually sends them via the
configured MCP stubs (e.g. gmail_mcp_stub for email).

Sending messages is always gated behind human approval in GitHub. The
``config/feature_flags.yaml`` file controls whether actual sending is
enabled. When ``allow_outbound_email`` or ``allow_slack_post`` are false,
this script will run in dry‑run mode regardless of the ``--dry-run`` flag.

Usage:
  python scripts/send_messages.py --draft-ids 001,002 --dry-run true
"""

import argparse
import os
import sys
import yaml
from pathlib import Path

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
    parser.add_argument("--draft-ids", required=True, help="Comma‑separated list of draft IDs (e.g. 001,002)")
    parser.add_argument("--dry-run", default="true", help="If true, simulate sending only")
    args = parser.parse_args()

    draft_ids = [d.strip() for d in args.draft_ids.split(",") if d.strip()]
    dry_run_flag = args.dry_run.lower() == "true"

    feature_flags = load_feature_flags()
    allow_email = feature_flags.get("allow_outbound_email", False)

    # Force dry run if outbound email is not allowed
    if not allow_email:
        dry_run_flag = True

    gmail = GmailMCP()

    drafts_dir = Path("outreach/drafts")
    if not drafts_dir.exists():
        print(f"Drafts directory {drafts_dir} not found", file=sys.stderr)
        sys.exit(1)

    for draft_id in draft_ids:
        draft_path = drafts_dir / f"{draft_id}.md"
        if not draft_path.exists():
            print(f"Draft file {draft_path} not found", file=sys.stderr)
            continue
        with draft_path.open(encoding="utf-8") as f:
            body = f.read()
        # Simple heuristic: first line as subject, rest as body
        lines = body.strip().split("\n", 1)
        subject = lines[0][:78] if lines else "AI Company Outreach"
        content = lines[1].strip() if len(lines) > 1 else ""

        # Determine recipient: default to environment variable or placeholder
        to = os.environ.get("DEFAULT_TO", "example@example.com")

        if dry_run_flag:
            print(
                f"Dry run – would send email to {to} with subject '{subject}'.\n"\
                f"Draft ID: {draft_id}\n"
            )
        else:
            print(f"Sending email draft {draft_id} to {to} …")
            gmail.send_email(to=to, subject=subject, body=content)

    if dry_run_flag:
        print("Dry run complete; no emails were sent.")


if __name__ == "__main__":
    main()