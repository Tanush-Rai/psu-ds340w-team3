"""Check the DSBench evaluation output using the authors' saved result files.

This runs the original show_result.py from the repository root.
It does not run a new LLM experiment.
"""
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "Task completion rate": 0.16216216216216217,
    "All the cost": 2.7426375,
    "The total time consuming": 8325.69773888588,
    "The performance": 0.06518438585408579,
}


def main():
    run = subprocess.run(
        [sys.executable, "show_result.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    if run.stderr.strip():
        print(run.stderr.strip(), file=sys.stderr)
    results = {}
    for label in EXPECTED:
        match = re.search(r"^" + re.escape(label) + r" is ([-+\d.eE]+)$", run.stdout, re.M)
        if match is None:
            raise RuntimeError(f"Missing result: {label}\n{run.stdout}")
        results[label] = float(match.group(1))
        if not math.isclose(results[label], EXPECTED[label], rel_tol=1e-9, abs_tol=1e-9):
            raise AssertionError(f"{label}: got {results[label]}, expected {EXPECTED[label]}")
    print(run.stdout.strip())
    print("PASS: all four saved-result metrics match the values documented in README.md")
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "DSBench data_modeling/show_result.py and published saved output files",
        "experiment_type": "recomputed summary of authors' saved modeling results (no fresh model run)",
        "metrics": results,
        "passed": True,
    }
    target = ROOT / "team3_work" / "verification_output.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Saved report: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
