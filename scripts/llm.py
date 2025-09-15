import glob
import os
from typing import Optional

try:
    import openai
except Exception:  # pragma: no cover - openai optional
    openai = None


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def load_system(agent: str) -> str:
    return _read(os.path.join("agents", agent, "system.md"))


def load_memory(limit: int = 4000) -> str:
    parts = []
    for pattern in ("reports/board/*.md", "reports/agent_runs/*.md"):
        for p in sorted(glob.glob(pattern))[-3:]:
            parts.append(f"# {p}\n" + _read(p))
    blob = "\n\n".join(parts)
    return blob[:limit]


def chat(agent: str, prompt: str) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or openai is None:
        return None
    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": load_system(agent)},
                {"role": "user", "content": f"{prompt}\n\nMEMORY:\n{load_memory()}"},
            ],
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
