# Repository Summary

This repository hosts automation for the "ai-comapny" project. Key areas:

## Workflows
- `.github/workflows/orchestrate.yml` – coordinates agents from issues.
- `.github/workflows/agent-engineer.yml` – engineer agent workflow.
- `.github/workflows/agent-growth.yml` – growth agent workflow.
- `.github/workflows/send_messages.yml` – sends outreach drafts via `scripts/send_messages.py`.
- `.github/workflows/labels.yml` – syncs repository labels.
- `.github/workflows/secret-scan.yml` – soft secret scanning.
- `.github/workflows/eval.yml` – run lightweight evaluations.
- `.github/workflows/ceo-observer.yml` – erstellt CEO-Vorschlags-Issues; mit `approve-proposal.yml` freigeben.

## Scripts
- `scripts/send_messages.py` – parse drafts under `outreach/drafts/` and send or dry‑run messages.

## Data paths
- `outreach/drafts/` – markdown drafts with optional YAML front matter specifying `to` and `subject`.
- `config/feature_flags.yaml` – feature toggles such as outbound email permissions.

## Running
Workflows are triggered via GitHub Actions. For manual invocation use `workflow_dispatch` on relevant workflows.

See `docs/OPERATIONS.md` for day‑to‑day instructions.
