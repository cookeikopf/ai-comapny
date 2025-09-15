import os
import pathlib
from llm import chat


def main() -> int:
    title = os.getenv("ISSUE_TITLE", "(no title)")
    num = os.getenv("ISSUE_NUMBER", "0")
    prompt = f"Issue #{num}: {title}\nGenerate an outreach draft."
    resp = chat("growth", prompt)
    out_dir = pathlib.Path("reports/agent_runs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"growth-draft-{num}.md"
    content = resp or "# Outreach Draft\nDeterministische Platzhalter ohne Model-Ausgabe."
    out_file.write_text(content, encoding="utf-8")
    print(f"[growth] draft -> {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
