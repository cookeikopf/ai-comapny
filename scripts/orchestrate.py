#!/usr/bin/env python
"""
Simple orchestrator stub: reads a GitHub issue event, writes a plan stub and creates tasks.
In a real implementation this script would call GPT‑5 via OpenAI's API, generate plans
and tasks, and open issues/PRs accordingly.
"""
import json
import os
import sys
import datetime as dt
import pathlib

def main():
    # Determine event path from environment or argument
    event_path = os.environ.get("GITHUB_EVENT_PATH") or (sys.argv[1] if len(sys.argv) > 1 else None)
    if not event_path or not os.path.exists(event_path):
        print("No event file found. This script must be run by GitHub Actions.")
        return
    event = json.load(open(event_path))
    issue = event.get("issue", {})
    title = issue.get("title", "Untitled task")
    # Create reports directory
    pathlib.Path("reports/board").mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M")
    plan_path = f"reports/board/plan-{timestamp}.md"
    with open(plan_path, "w") as f:
        f.write(f"# Plan Stub\n\n- Task: {title}\n- Owner: founder\n- KPIs: TBD\n")
    print(f"Wrote plan stub to {plan_path}")

if __name__ == "__main__":
    main()