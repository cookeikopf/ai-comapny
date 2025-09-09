#!/usr/bin/env python
"""
Smoke evaluation script. Verifies existence of key files and checks basic project integrity.
Returns non-zero exit on failure, causing the GitHub Actions job to fail.
"""
import os
import sys

def main():
    required_files = [
        "agents/founder/system.md",
        "docs/index.html",
        "config/cost_limits.yaml",
        "config/policies.yaml",
        "config/feature_flags.yaml"
    ]
    missing = [p for p in required_files if not os.path.exists(p)]
    if missing:
        print("Missing files:\n" + "\n".join(missing))
        sys.exit(1)
    print("Smoke OK")

if __name__ == "__main__":
    main()