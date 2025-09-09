#!/usr/bin/env python3
"""
Generate a simple summary of current tasks and post to Slack.

This script is intended to be run as a scheduled job (e.g. via GitHub Actions)
to post a summary of open issues or recently completed tasks to an internal
Slack channel. It uses the Slack MCP stub to simulate posting; when the
real integration is enabled, it will send messages for real.

Currently this script lists all files in ``outreach/drafts`` and prints a
summary. In a real implementation, you might query the GitHub API for
Issues/PRs or use internal state to build more meaningful summaries.
"""

import os
from pathlib import Path

try:
    from tools.slack_mcp_stub import SlackMCP
except ImportError:
    class SlackMCP:
        def __init__(self):
            pass
        def post_message(self, channel: str, message: str):
            print(f"(Stub) Would post to #{channel}: {message}\n")


def main() -> None:
    drafts_dir = Path("outreach/drafts")
    draft_files = sorted(drafts_dir.glob("*.md"))
    summary_lines = []
    for path in draft_files:
        summary_lines.append(f"Draft {path.stem}: {path.name}")
    if not summary_lines:
        summary = "Keine aktuellen Drafts."
    else:
        summary = "Offene Drafts:\n" + "\n".join(summary_lines)

    slack = SlackMCP()
    channel = os.environ.get("SLACK_SUMMARY_CHANNEL", "drafts")
    slack.post_message(channel=channel, message=summary)

    print("Summary posted to Slack (or simulated)")


if __name__ == "__main__":
    main()