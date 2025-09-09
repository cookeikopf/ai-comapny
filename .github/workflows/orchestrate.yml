# scripts/orchestrate.py
import os, json, datetime, pathlib, traceback

def yaml_escape(s: str) -> str:
    # minimal safe escape for YAML double-quoted scalars
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("[orchestrate] ERROR: GITHUB_EVENT_PATH missing or file not found")
        return 0  # don't fail the job; just skip

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    issue = event.get("issue") or {}
    num   = issue.get("number")
    title = (issue.get("title") or "").strip()
    body  = (issue.get("body") or "").strip()

    if not isinstance(num, int):
        print("[orchestrate] ERROR: issue.number not found in event")
        return 0

    pathlib.Path("reports/board").mkdir(parents=True, exist_ok=True)

    # try to reuse latest plan for this issue
    existing = sorted(pathlib.Path("reports/board").glob(f"plan-{num}-*.md"))
    if existing:
        plan_path = str(existing[-1])
        should_write = False
    else:
        ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        plan_path = f"reports/board/plan-{num}-{ts}.md"
        should_write = True

    if should_write:
        fm = [
            "---",
            f"issue: {num}",
            f'title: "{yaml_escape(title)}"',
            "deterministic_first: true",
            "owner: orchestrator",
            "agents: [engineer, growth]",
            f"created_utc: {datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            "---",
            "",
        ]
        md = f"""# Plan für Issue #{num}: {title}

## Kontext
{body or '(kein Issue-Body)'}

## Deterministischer Ansatz
1. I/O spezifizieren, Tests zuerst
2. Agent-PRs mit `Closes #{num}`
3. HITL: du prüfst & mergest

## Deliverables
- [ ] Engineer (Code/Tests)
- [ ] Growth (Outreach-Drafts)
"""
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write("\n".join(fm) + md)

    # Expose output for the workflow step
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"plan_path={plan_path}\n")

    print(f"[orchestrate] plan_path={plan_path}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        # Never fail the job hard; print the stack for debugging.
        print("[orchestrate] FATAL ERROR:\n" + traceback.format_exc())
        # still set a dummy output so downstream steps don't explode
        gh_out = os.environ.get("GITHUB_OUTPUT")
        if gh_out:
            with open(gh_out, "a", encoding="utf-8") as f:
                f.write("plan_path=reports/board/plan-error.txt\n")
        # exit 0 to avoid failing the workflow on first setup
        raise SystemExit(0)
