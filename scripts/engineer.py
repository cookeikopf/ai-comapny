import os
import pathlib
from llm import chat


def main() -> int:
    title = os.getenv("ISSUE_TITLE", "(no title)")
    num = os.getenv("ISSUE_NUMBER", "0")
    prompt = f"Issue #{num}: {title}\nProvide a short engineering plan."
    resp = chat("engineer_codex", prompt)
    out_dir = pathlib.Path("reports/agent_runs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"engineer-plan-{num}.md"
    content = resp or "# Engineer Plan\nDeterministische Platzhalter ohne Model-Ausgabe."
    out_file.write_text(content, encoding="utf-8")
    print(f"[engineer] plan -> {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
