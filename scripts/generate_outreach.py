#!/usr/bin/env python3
"""
Generate outreach draft messages from leads.

This script reads the normalized leads file (``sales/leads.normalized.csv``) or
falls back to ``sales/leads.csv`` if not normalized. For each lead, it
generates a Markdown draft file under ``outreach/drafts/`` using a
deterministic template. The template is read from ``kb/playbooks/outreach_style.md``
and supports simple placeholder replacement:

  {Company} – the lead's company name
  {Name} – the contact's name (if present)
  {Role} – the contact's role/title (if present)

If the template contains a placeholder that is not available in the lead row,
it will be replaced with an empty string. Once drafts are generated, you can
review them and decide which ones to send via the ``send_messages`` workflow.

This script is deterministic by default. If the heuristics or template are
insufficient, you may choose to implement an escalation to an LLM. In that
case, ensure that you record the reason for escalation as per the
``policies.yaml`` escalation criteria and mark the drafts with a flag
``HITL_REQUIRED``.
"""

import csv
import os
import re
from pathlib import Path


def load_template(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def render(template: str, lead: dict) -> str:
    """Replace placeholders in the template with values from lead."""
    def replace(match: re.Match) -> str:
        key = match.group(1)
        return lead.get(key, "").strip()
    return re.sub(r"\{([^}]+)\}", replace, template)


def main() -> None:
    # Determine the input file: prefer normalized leads if present
    normalized_path = Path("sales/leads.normalized.csv")
    raw_path = Path("sales/leads.csv")
    input_path = normalized_path if normalized_path.exists() else raw_path
    if not input_path.exists():
        raise FileNotFoundError(
            "No input leads found. Please place leads.csv in the sales folder."
        )

    # Load leads
    with input_path.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        leads = list(reader)

    if not leads:
        print(f"No leads to process in {input_path}")
        return

    # Load template
    template_path = Path("kb/playbooks/outreach_style.md")
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    template = load_template(str(template_path))

    drafts_dir = Path("outreach/drafts")
    drafts_dir.mkdir(parents=True, exist_ok=True)

    for idx, lead in enumerate(leads, start=1):
        body = render(template, lead)
        # Determine file name: zero‑padded index
        filename = drafts_dir / f"{idx:03d}.md"
        with filename.open("w", encoding="utf-8") as f:
            f.write(body)
        print(f"Wrote draft for lead {idx} → {filename}")

    print(f"Generated {len(leads)} outreach drafts in {drafts_dir}")


if __name__ == "__main__":
    main()