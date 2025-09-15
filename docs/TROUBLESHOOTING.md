# Troubleshooting

## Orchestrator did not run
- Ensure the issue has the `task:agent` label.
- Check that GitHub Actions are enabled for the repository.

## send_messages workflow fails
- Verify provided draft paths exist under `outreach/drafts/`.
- Missing front matter results in a warning but the workflow continues.
- If dependencies are needed, add a `requirements.txt` in the repository root or `scripts/`.

## Label sync errors
- The workflow uses `${{ github.repository }}`; confirm the repository name is `ai-comapny`.

## Secret scan warnings
- The secret scan workflow logs warnings but does not fail the run.
