#!/usr/bin/env python3
"""
Normalize leads from the raw sales CSV.

This script reads the file at ``sales/leads.csv``, validates and normalizes
its contents, then writes two output files:

* ``sales/leads.normalized.csv`` containing only valid rows with trimmed
  whitespace and lowercase email addresses/URLs.
* ``sales/leads.rejected.csv`` containing rows that were rejected, along with
  a ``reason`` column explaining why.

The script is deterministic and does not use any LLMs. It should be run
whenever new leads are added. If you run into cases where the deterministic
approach fails to classify certain rows correctly, consider adding more
validation rules or escalating via the orchestrator according to the
``policies.yaml`` escalation criteria.
"""

import csv
import os
import re


def is_valid_email(email: str) -> bool:
    """Simple regex-based email validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email or "") is not None


def normalize_row(row: dict) -> dict:
    """
    Trim whitespace and normalize fields. Emails and URLs are lowercased. Other
    fields are stripped of surrounding whitespace but remain unchanged.
    """
    normalized = {}
    for key, value in row.items():
        value = (value or "").strip()
        if key.lower() in {"email", "emailorurl", "url", "email_or_url"}:
            normalized[key] = value.lower()
        else:
            normalized[key] = value
    return normalized


def main() -> None:
    input_path = os.path.join("sales", "leads.csv")
    normalized_path = os.path.join("sales", "leads.normalized.csv")
    rejected_path = os.path.join("sales", "leads.rejected.csv")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        required_fields = {"Company", "Name", "Role", "EmailOrURL"}
        missing_columns = required_fields - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                f"Missing required columns in input CSV: {', '.join(sorted(missing_columns))}"
            )

        normalized_rows = []
        rejected_rows = []
        for row in reader:
            norm = normalize_row(row)
            reason = None
            # Check that at least Company and one of Name or Role is present
            if not norm.get("Company"):
                reason = "Missing Company"
            elif not (norm.get("Name") or norm.get("Role")):
                reason = "Missing Name or Role"
            # Validate Email or URL
            email_or_url = norm.get("EmailOrURL")
            if not email_or_url:
                reason = reason or "Missing EmailOrURL"
            elif "@" in email_or_url and not is_valid_email(email_or_url):
                reason = reason or "Invalid email format"

            if reason:
                norm["reason"] = reason
                rejected_rows.append(norm)
            else:
                normalized_rows.append(norm)

    # Write normalized rows
    with open(normalized_path, "w", newline="", encoding="utf-8") as nf:
        writer = csv.DictWriter(nf, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in normalized_rows:
            writer.writerow({key: row.get(key, "") for key in reader.fieldnames})

    # Write rejected rows with reason column
    with open(rejected_path, "w", newline="", encoding="utf-8") as rf:
        fieldnames = list(reader.fieldnames) + ["reason"]
        writer = csv.DictWriter(rf, fieldnames=fieldnames)
        writer.writeheader()
        for row in rejected_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    print(
        f"Normalized {len(normalized_rows)} rows → {normalized_path}; "
        f"rejected {len(rejected_rows)} rows → {rejected_path}"
    )


if __name__ == "__main__":
    main()