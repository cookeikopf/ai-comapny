import os, json, datetime, pathlib, traceback, re
from llm import chat

def yaml_escape(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("[orchestrate] ERROR: GITHUB_EVENT_PATH missing or file not found"); return 0

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    issue = event.get("issue") or {}
    if not issue:
        issue = {
            "number": os.environ.get("MANUAL_ISSUE_NUMBER"),
            "title": os.environ.get("MANUAL_ISSUE_TITLE"),
            "body": os.environ.get("MANUAL_ISSUE_BODY"),
        }
    num_raw = issue.get("number")
    try:
        num = int(num_raw)
    except (TypeError, ValueError):
        print("[orchestrate] ERROR: issue.number not found"); return 0
    title = (issue.get("title") or "").strip()
    body  = (issue.get("body") or "").strip()

    pathlib.Path("reports/board").mkdir(parents=True, exist_ok=True)

    existing = sorted(pathlib.Path("reports/board").glob(f"plan-{num}-*.md"))
    if existing:
        plan_path = str(existing[-1])
        should_write = False
    else:
        ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        plan_path = f"reports/board/plan-{num}-{ts}.md"
        should_write = True

    ai_plan = chat("founder", f"Issue #{num}: {title}\n{body}")
    if should_write:
        fm = ["---",
              f"issue: {num}",
              f'title: "{yaml_escape(title)}"',
              "deterministic_first: true",
              "owner: orchestrator",
              "agents: [engineer, growth]",
              f"created_utc: {datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
              "---",
              ""]
        md = f"""# Plan für Issue #{num}: {title}

## Kontext
{body or '(kein Issue-Body)'}

## AI Plan
{ai_plan or '(kein Model-Output – deterministische Platzhalter)'}

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

    # einfache Heuristik (nur Log, tatsächliches Dispatching macht der Workflow)
    title_lc = (title or "").lower()
    wants_engineer = bool(re.search(r"(parse|script|normalize|gate|test|engineer|pipeline)", title_lc))
    wants_growth   = bool(re.search(r"(outreach|draft|growth|message|email|template)", title_lc))
    fire_engineer  = wants_engineer or (not wants_engineer and not wants_growth)
    fire_growth    = wants_growth

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"plan_path={plan_path}\n")

    print(f"DISPATCH: engineer={fire_engineer} growth={fire_growth} plan={plan_path}")
    print(f"[orchestrate] plan_path={plan_path}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        print("[orchestrate] FATAL:\n" + traceback.format_exc())
        gh_out = os.environ.get("GITHUB_OUTPUT")
        if gh_out:
            with open(gh_out, "a", encoding="utf-8") as f:
                f.write("plan_path=reports/board/plan-error.txt\n")
        raise SystemExit(0)

