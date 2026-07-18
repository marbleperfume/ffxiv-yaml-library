"""CLI validator run — structured findings to the terminal.

    python WebApp/backend/run_validators.py          (from repo root, or anywhere)

Exit code 1 if any `error`-severity finding exists (CI-compatible, same
contract as the original Project_Validator.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.validators import run_all  # noqa: E402


def main():
    findings = run_all()
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        loc = f["file"] + (f":{f['line']}" if f.get("line") else "")
        print(f"[{f['severity'].upper():7}] {f['rule']:26} {loc}\n"
              f"          {f['message']}")
    summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "no findings"
    print(f"\n=== {summary} ===")
    return 1 if counts.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
