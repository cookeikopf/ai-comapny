import sys
from pathlib import Path


def load_module():
    """Dynamically load the normalize_leads module from scripts."""
    # Determine the scripts directory relative to this test file
    root = Path(__file__).resolve().parents[1]
    scripts_dir = root / "scripts"
    sys.path.insert(0, str(scripts_dir))
    import normalize_leads  # type: ignore  # noqa: F401
    return normalize_leads


def test_normalize_row():
    mod = load_module()
    row = {
        "Company": "  OpenAI  ",
        "Name": "  Alice ",
        "Role": "Engineer ",
        "EmailOrURL": "  ALICE@Example.COM  ",
    }
    norm = mod.normalize_row(row)
    assert norm["Company"] == "OpenAI"
    assert norm["Name"] == "Alice"
    assert norm["Role"] == "Engineer"
    # Email lowercased and trimmed
    assert norm["EmailOrURL"] == "alice@example.com"


def test_is_valid_email():
    mod = load_module()
    assert mod.is_valid_email("user@example.com")
    assert not mod.is_valid_email("bad-email@")