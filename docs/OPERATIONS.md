# Operations

## Creating an Issue
1. Open an issue using the `agent-task` template.
2. Ensure the label `task:agent` is present. The orchestrator workflow will plan and dispatch agents.

## Reviewing Plans and PRs
- The orchestrator comments a plan in the issue.
- Agent workflows open pull requests referencing the issue.
- Merging an agent PR closes the issue via `Closes #<number>` in commit messages.

## Sending Outreach
1. Place drafts in `outreach/drafts/` with YAML front matter:
   ```markdown
   ---
   to: person@example.com
   subject: Hello
   ---
   Body text
   ```
2. Trigger the `send_messages` workflow with inputs:
   - `draft_ids`: comma separated list of draft paths (e.g. `outreach/drafts/001.md`).
   - `dry_run`: `true` to preview, `false` to send.
3. The workflow runs in the `production` environment which requires manual approval for real sends.

## Evaluations
Run the `eval.yml` workflow or `pytest` locally to ensure changes pass basic checks.

See `docs/TROUBLESHOOTING.md` for common problems.
