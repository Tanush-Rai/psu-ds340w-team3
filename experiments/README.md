# Team 3: New technique pilot

This folder extends our DSBench-inspired reliability project with a **separate controlled experiment**. It is **not** a reproduction of the paper's LLM benchmarks; it uses 20 synthetic tabular tasks (5 development, 15 held-out test), a deterministic rule-based analyst, and seed 42.

## Run
From repository root:

```powershell
python experiments/run_pilot.py
cd experiments
python -m unittest discover -v
```

This uses Python's standard library only. Outputs are written to `results/comparison.csv` and `results/pilot_results.json`. The earlier original-paper saved-result demonstration (`show_result.py`) remains unchanged.

## Techniques
We tested eight conditions: baseline; trimming category whitespace; parsing currency and thousands separators; both cleaning steps; independent checking; combined cleaning and checking; checking with a single repair; and all three.

The initial analyst selects region labels exactly and attempts to parse sales as floats. A separate checker strips region whitespace and uses Decimal arithmetic. If checking disagrees, the answer is **flagged**, not silently accepted. With repair enabled, the program performs one full cleaning pass, reruns the analyst, and accepts the repaired output only if it agrees with the independent computation. The checker does **not** see the reference answer.

## Test results (15 controlled synthetic tasks)

| Condition | Accepted accuracy | Unflagged incorrect answers | Flagged |
| --- | ---: | ---: | ---: |
| Baseline | 6.7% | 93.3% | 0% |
| Trim only | 46.7% | 53.3% | 0% |
| Numeric only | 20.0% | 80.0% | 0% |
| Both cleaning rules | 100% | 0% | 0% |
| Check only | 6.7% | 0% | 93.3% |
| Clean + check | 100% | 0% | 0% |
| Check + repair | 100% | 0% | 0% |
| Clean + check + repair | 100% | 0% | 0% |

These percentages describe controlled, deliberately introduced formatting problems; they should **not** be compared numerically to the DSBench paper's published agent accuracy. The independent checker knows how to correct exactly the formatting noise introduced here; generalization to real analysis tasks is untested. Successful repair is not evidence of an LLM's new reasoning ability.

## Next steps for the actual parent-paper benchmark

Retrieve 20 actual DSBench **data-analysis** tasks with input data and reference answers; keep five development and 15 held-out test tasks, grouped by source table. Fix a single LLM, prompt, settings and execution budget. Run each condition over the same task set, preserving predictions, code, references, errors, runtime and model calls. Replace this toy analyst with an agent adapter. Do not call the current synthetic pilot a DSBench result.

The original paper draft and revised methodology discuss this planned extension. The main contribution proposed is a modular, auditable cleaning–checking–repair workflow, not a new foundation model.
