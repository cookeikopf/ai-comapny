import os
import subprocess
import sys


def run_cost_guard(eur: float) -> int:
    """Helper to run the cost_guard script with a fake cost."""
    env = os.environ.copy()
    env["RUN_COST_JSON"] = f"{{\"eur\": {eur}}}"
    result = subprocess.run(
        [sys.executable, "scripts/cost_guard.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode


def test_cost_guard_allows_small_cost():
    # Below the hard_abort threshold (0.60 in config), should exit 0
    rc = run_cost_guard(0.1)
    assert rc == 0


def test_cost_guard_aborts_high_cost():
    # Above the hard_abort threshold, should exit with non-zero
    rc = run_cost_guard(0.7)
    assert rc != 0