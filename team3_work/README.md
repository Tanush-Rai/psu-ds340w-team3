# Team 3: verification and follow-up experiments

Parent paper: [DSBench (Jing et al., ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50e9ad960ae78b741a6b4fea533f2eaf-Abstract-Conference.html)

Official code: https://github.com/LiqiangJing/DSBench

## What we can verify

Our repository already includes the authors' original `data_modeling/show_result.py` and their saved result files. From the repository root run:

```powershell
python -m pip install -r requirements.txt
python team3_work/verify_official_demo.py
```

This re-runs the original scoring summary on the saved data-modeling experiment and checks four values against our repository's README. It also writes `team3_work/verification_output.json`. GitHub Actions repeats the same check under **Actions -> Verify DSBench saved results**.

The original data-modeling experiment yielded these saved-summary figures:

| Metric | Value |
| --- | ---: |
| Task completion rate | 0.16216216216216217 |
| Total cost recorded | 2.7426375 |
| Total time recorded (seconds) | 8325.69773888588 |
| Normalized performance | 0.06518438585408579 |

**Do not confuse this with running a new GPT agent or reproducing the entire DSBench analysis benchmark.** The repository contains saved outputs from the authors, and the check only recomputes the summary.

## Next research steps

Our topic is reliability of **data analysis** through cleaning and result checking. We will use the paper's data-analysis notebooks and the data-analysis benchmark for any eventual model comparison. Before adding new methods, our evaluation should keep the same tasks/model/scorer and record how many tasks were completed. Proposed separate modules: load/clean data, run model, verify results, and score answers. The small synthetic demonstration prepared for this course is separate from this original-paper demonstration.

## Recording outline

1. Show the team repository and this page.
2. Explain that `show_result.py` is the author's original data-modeling evaluation summary and the saved outputs came with the authors' repository.
3. Run `python team3_work/verify_official_demo.py`; point out the four metrics and the PASS line.
4. If the GitHub Actions check has completed successfully, show it too.
5. Be clear: this verifies the provided result-summary code, **not** a fresh agent run. Discuss how a future cleaning/checking extension would need real data-analysis benchmark tasks.

The recording must show a real terminal run. Do not present output that the group did not obtain or claim that specific teammates wrote code they did not write.
