# scripts/orchestrate.py
import os, json, datetime, pathlib

# Event laden
with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
    event = json.load(f)

issue = event["issue"]
num   = issue["number"]
title = issue["title"].strip()
body  = (issue.get("body") or "").strip()

# Ordner sicherstellen
pathlib.Path("reports/board").mkdir(parents=True, exist_ok=True)

# Existierende Pläne suchen
existing = sorted(pathlib.Path("reports/board").glob(f"plan-{num}-*.md"))
if existing:
    plan_path = str(existing[-1])
    should_write = False
else:
    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    plan_path = f"reports/board/plan-{num}-{ts}.md"
    should_write = True

# Falls neu → schreiben
if should_write:
    fm = [
        "---",
        f"issue: {num}",
        f'title: "{title.replace("\"","\\\"")}"',
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

# Output an GitHub Actions weitergeben
gh_out = os.environ.get("GITHUB_OUTPUT")
if gh_out:
    with open(gh_out, "a", encoding="utf-8") as f:
        f.write(f"plan_path={plan_path}\n")

print(f"[orchestrate] plan_path={plan_path}")
