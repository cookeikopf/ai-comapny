#!/usr/bin/env python
"""
Simple cost guard to enforce budget limits. Reads current run cost from environment and
exits with non-zero status if the cost exceeds hard_abort_over_eur.
"""
import os
import json
import sys

# Default limits; these can be overridden by config or environment variables
LIMIT_PER_RUN = float(os.getenv('COST_LIMIT_PER_RUN', '0.50'))
HARD_ABORT = float(os.getenv('COST_LIMIT_HARD_ABORT', '0.60'))

def main():
    usage_json = os.getenv('RUN_COST_JSON') or '{"eur": 0}'
    try:
        usage = json.loads(usage_json)
    except json.JSONDecodeError:
        print("Invalid RUN_COST_JSON")
        sys.exit(2)
    cost = usage.get('eur', 0)
    if cost > HARD_ABORT:
        print("COST_GUARD: Hard abort – run cost exceeds maximum limit.")
        sys.exit(2)
    if cost > LIMIT_PER_RUN:
        print("COST_GUARD: Warning – cost over per-run limit, consider splitting tasks.")
    else:
        print("COST_GUARD: OK")

if __name__ == '__main__':
    main()