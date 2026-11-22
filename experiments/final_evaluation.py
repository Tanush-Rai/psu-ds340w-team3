"""Full synthetic evaluation and dataset export for Team 3.

This is 20 generated tasks x 8 variants. No LLM or original DSBench agent
is evaluated here. The five development tasks and 15 test tasks are
reported separately, along with all 20 tasks.
"""
import csv
import json
from pathlib import Path
from run_pilot import VARIANTS, evaluate, tasks

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"


def summary_by_split(predictions, split):
    current = [r for r in predictions if split == "all" or r["split"] == split]
    summary = []
    for variant in VARIANTS:
        cases = [r for r in current if r["variant"] == variant[0]]
        n = len(cases)
        correct = sum(r["accepted_correct"] for r in cases)
        errors = sum(r["unflagged_error"] for r in cases)
        flagged = sum(r["flagged"] for r in cases)
        summary.append({
            "split": split, "variant": variant[0], "n_tasks": n,
            "accepted_correct": correct,
            "accepted_accuracy_pct": round(100 * correct / n, 2),
            "unflagged_errors": errors,
            "unflagged_error_pct": round(100 * errors / n, 2),
            "flagged": flagged,
            "flagged_pct": round(100 * flagged / n, 2),
            "mean_cell_edits": round(sum(r["edits"] for r in cases) / n, 2),
        })
    return summary


def write_csv(filename, rows):
    with (OUT / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    dataset = tasks()
    assert len(dataset) == 20
    flat_rows = []
    for task in dataset:
        for j, row in enumerate(task["rows"], 1):
            flat_rows.append({
                "task_id": task["id"], "split": task["split"],
                "kind": task["kind"], "target_region": task["region"],
                "row_number": j, "region": row["region"],
                "sales": row["sales"], "expected_answer": str(task["expected"]),
            })
    assert len(flat_rows) == 240
    write_csv("synthetic_rows_240.csv", flat_rows)

    predictions = [evaluate(t, v) for t in dataset for v in VARIANTS]
    assert len(predictions) == 160
    write_csv("full_task_predictions.csv", predictions)

    by_split = {s: summary_by_split(predictions, s) for s in ("dev", "test", "all")}
    summary = by_split["dev"] + by_split["test"] + by_split["all"]
    write_csv("full_evaluation.csv", summary)

    print("Full controlled evaluation: 20 synthetic tasks x 8 variants = 160 runs")
    print("Condition                      Dev   Test   All   Unflagged(all)")
    for i, variant in enumerate(VARIANTS):
        dev, test, all_ = (by_split[s][i] for s in ("dev", "test", "all"))
        print(f"{variant[0]:28} {dev['accepted_correct']:>2}/5  "
              f"{test['accepted_correct']:>2}/15  "
              f"{all_['accepted_correct']:>2}/20   "
              f"{all_['unflagged_errors']:>2}/20")
    print("Dataset and evaluation exports written to results/")


if __name__ == "__main__":
    main()
