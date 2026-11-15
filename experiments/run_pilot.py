"""Controlled cleaning/checking pilot. Synthetic data; NOT a DSBench LLM benchmark."""
import csv
import json
import math
import random
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"

def tasks():
    out = []
    for i in range(20):
        rng = random.Random(42 + i)
        kind, region = ("total", "mean", "count")[i % 3], ("North", "South", "East")[i % 3]
        rows = []
        for j in range(12):
            group = ("North", "South", "East")[j % 3]
            num = 1100 + i * 37 + j * 29
            row = {"region": group, "sales": str(num)}
            if rng.random() < .35:
                row["region"] = " " + group + " "
            if rng.random() < .45:
                row["sales"] = "${:,}".format(num) if j % 2 == 0 else "{:,}".format(num)
            rows.append(row)
        numbers = [Decimal(1100+i*37+j*29) for j in range(12)
                   if ("North", "South", "East")[j%3] == region]
        expected = (sum(numbers) if kind == "total"
                    else sum(numbers)/len(numbers) if kind == "mean"
                    else Decimal(len(numbers)))
        out.append({"id":f"T{i+1:02d}", "split":"dev" if i<5 else "test",
                    "kind":kind, "region":region, "rows":rows, "expected":expected})
    return out

def clean(rows, trim, numeric):
    output = []
    changes = 0
    for source in rows:
        row = source.copy()
        if trim:
            new = row["region"].strip()
            changes += new != row["region"]
            row["region"] = new
        if numeric:
            new = row["sales"].replace("$","").replace(",","").strip()
            changes += new != row["sales"]
            row["sales"] = new
        output.append(row)
    return output, changes

def analyst(task, rows):
    selected = [r for r in rows if r["region"] == task["region"]]
    if task["kind"] == "count":
        return Decimal(len(selected))
    values = []
    for row in selected:
        try:
            values.append(float(row["sales"]))
        except ValueError:
            pass
    if not values:
        return None
    total = math.fsum(values)
    return Decimal(str(total if task["kind"] == "total" else total / len(values)))

def check_independently(task, rows):
    selected = [r for r in rows if r["region"].strip() == task["region"]]
    if task["kind"] == "count":
        return Decimal(len(selected))
    values = []
    for row in selected:
        try:
            values.append(Decimal(row["sales"].strip().replace("$","").replace(",","")))
        except InvalidOperation:
            return None
    if not values:
        return None
    total = sum(values)
    return total if task["kind"] == "total" else total / Decimal(len(values))

def equal(a, b):
    return a is not None and b is not None and abs(a-b) <= Decimal(".000001")

VARIANTS = [
    ("A baseline",False,False,False,False),
    ("B trim only",True,False,False,False),
    ("C numeric only",False,True,False,False),
    ("D clean both",True,True,False,False),
    ("E check only",False,False,True,False),
    ("F clean + check",True,True,True,False),
    ("G check + repair",False,False,True,True),
    ("H clean + check + repair",True,True,True,True),
]

def evaluate(task, variant):
    name, trim, numeric, verify, repair = variant
    rows, edits = clean(task["rows"], trim, numeric)
    answer = analyst(task, rows)
    flagged = False
    if verify:
        second = check_independently(task, rows)
        if not equal(answer, second):
            flagged = True
            if repair and second is not None:
                repaired, extra = clean(task["rows"], True, True)
                attempt = analyst(task, repaired)
                edits += extra
                if equal(attempt, second):
                    answer, flagged = attempt, False
    correct = equal(answer, task["expected"])
    return {"task":task["id"], "split":task["split"], "variant":name,
            "answer":str(answer) if answer is not None else None,
            "expected":str(task["expected"]), "correct":correct,
            "flagged":flagged, "accepted_correct":correct and not flagged,
            "unflagged_error":not correct and not flagged, "edits":edits}

def main():
    OUT.mkdir(exist_ok=True)
    rows = [evaluate(task, variant) for task in tasks() for variant in VARIANTS]
    summary = []
    for variant in VARIANTS:
        group = [r for r in rows if r["split"] == "test" and r["variant"] == variant[0]]
        n = len(group)
        summary.append({"variant":variant[0], "runs":n,
            "accepted_accuracy_pct":round(100*sum(r["accepted_correct"] for r in group)/n,2),
            "unflagged_error_pct":round(100*sum(r["unflagged_error"] for r in group)/n,2),
            "flagged_pct":round(100*sum(r["flagged"] for r in group)/n,2),
            "avg_edits":round(sum(r["edits"] for r in group)/n,2)})
    (OUT/"pilot_results.json").write_text(json.dumps({
        "study":"synthetic deterministic pilot, not DSBench",
        "seed":42, "development_tasks":5, "test_tasks":15,
        "conditions":summary, "test_cases":[r for r in rows if r["split"]=="test"]
    },indent=2)+"\n",encoding="utf-8")
    with (OUT/"comparison.csv").open("w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print("Synthetic pilot, 15 held-out tasks; NOT the DSBench agent benchmark")
    for item in summary:
        print(f"{item['variant']:27} accuracy {item['accepted_accuracy_pct']:5.1f}%  "
              f"unflagged errors {item['unflagged_error_pct']:5.1f}%  flagged {item['flagged_pct']:5.1f}%")

if __name__ == "__main__":
    main()
