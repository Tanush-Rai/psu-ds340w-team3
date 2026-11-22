# DS 340W Team 3 - Data cleaning and result checking

**Team:** Miftaj Chowdhury, Jackson Shinsky, Tanush Rai

Our current experiment studies how simple cleaning and independent result checking affect tabular calculations. The parent paper is [DSBench](https://arxiv.org/abs/2409.07703), but the new experiments use **synthetic data and a rule-based analyst**, not the original DSBench agent tasks. The original DSBench saved-result verification from our earlier assignment is still available below.

## Final evaluation (Week 13)

The project now includes all 20 deterministic tasks, each evaluated with eight variants (160 experiment runs), along with complete source data and task-level predictions. There are five development tasks and 15 test tasks.

| Condition | Development correct | Test correct | All correct |
| --- | ---: | ---: | ---: |
| Baseline | 0/5 | 1/15 | 1/20 |
| Trim category spaces | 2/5 | 7/15 | 9/20 |
| Clean number formatting | 0/5 | 3/15 | 3/20 |
| Both cleaning methods | 5/5 | 15/15 | 20/20 |
| Checking only | 0/5 | 1/15 | 1/20 |
| Cleaning + checking | 5/5 | 15/15 | 20/20 |
| Checking + repair | 5/5 | 15/15 | 20/20 |
| Cleaning + checking + repair | 5/5 | 15/15 | 20/20 |

Checking without repair flagged 19/20 answers; it prevented incorrect unflagged output in this toy setting but did not increase accepted correct answers. The improvement from cleaning is limited to formatting problems deliberately introduced in the synthetic dataset. None of these numbers should be presented as a gain over the published DSBench agent accuracy.

## Running the code

From the repository's main folder:

```powershell
python experiments/run_pilot.py
python experiments/final_evaluation.py
cd experiments
python -m unittest discover -v
```

The scripts use only Python's standard library. GitHub Actions runs the scripts and tests on every relevant update.

## Dataset, scripts, and results

- [Complete dataset: 240 raw rows across 20 tasks](results/synthetic_rows_240.csv)
- [All 160 per-task predictions and flags](results/full_task_predictions.csv)
- [Full 20-task and development/test comparison table](results/full_evaluation.csv)
- [Complete evaluation script](experiments/final_evaluation.py)
- [Pilot methods and tests](experiments/README.md)
- [Original DSBench saved-result verification](team3_work/README.md)

**Dataset details:** Each row contains task ID, split, operation (total/mean/count), target region, source row number, raw region, raw sales string and expected task answer. The generator is deterministic and stored in `experiments/run_pilot.py`. The original DSBench dataset was not used for this new-technique evaluation.

---

## Earlier assignment: original DSBench saved-result verification

# DSBench Kaltura Demo

This folder is a small, repeatable demo of the official DSBench evaluation code. It uses the authors' unchanged `data_modeling/show_result.py` file and the saved experiment results included in the official repository. It does not require an API key or a large dataset download.

Official source: https://github.com/LiqiangJing/DSBench

Paper: https://proceedings.iclr.cc/paper_files/paper/2025/hash/50e9ad960ae78b741a6b4fea533f2eaf-Abstract-Conference.html

## Files

- `show_result.py`: unchanged DSBench evaluation-summary code
- `data.json`: DSBench modeling-task metadata
- `save_performance/`: extracted from the authors' `save_performance.zip`
- `output_model/`: extracted from the authors' `output_model.zip`
- `requirements.txt`: the one dependency needed for this demo
- `LICENSE`: original DSBench MIT license

## One-time setup on Windows

Open this folder in VS Code. Then open a PowerShell terminal in VS Code and run:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

In VS Code, press `Ctrl+Shift+P`, choose `Python: Select Interpreter`, and select the Python interpreter inside `.venv`.

Do this setup before starting the Kaltura recording.

## Run during the Kaltura recording

1. Start recording your full screen.
2. Briefly show this README and the official source link.
3. Open `show_result.py` so the code is visible.
4. Click the triangle-shaped `Run Python File` button in the top-right corner of VS Code.
5. Keep the terminal visible until all four result lines appear with no traceback or error.

Expected output:

```text
Task completion rate is 0.16216216216216217
All the cost is 2.7426375
The total time consuming is 8325.69773888588
The performance is 0.06518438585408579
```

If the VS Code Run button uses the wrong Python installation, run this command in the terminal instead:

```powershell
.venv\Scripts\python.exe show_result.py
```

## Short script to say in the recording

"This is the public GitHub repository for DSBench, the parent paper our group selected. I downloaded the authors' code and the saved experiment results provided in the repository. This file is their evaluation-summary script, `show_result.py`. It reads the DSBench task information, ground-truth and baseline scores, and the saved GPT-3.5 results. I am running the code now. The terminal shows the task completion rate, total cost, total run time, and normalized performance, and the program finishes without errors. Our project will focus on improving reliability for the data-analysis side of DSBench, but this run confirms that the parent repository's evaluation code and provided results work on our system."

## GitHub upload

Upload this folder to the team's repository:

https://github.com/Tanush-Rai/psu-ds340w-team3

Do not upload the `.venv` folder. It is only a local Python environment.

## Important note

This demo summarizes the authors' saved data-modeling results because that is the part of the public repository that includes both runnable evaluation code and all required result files. The authors' full data-analysis notebooks require a separate dataset download and an API key. Your group's later project can still focus on the DSBench data-analysis tasks, as stated in the assignment document.
