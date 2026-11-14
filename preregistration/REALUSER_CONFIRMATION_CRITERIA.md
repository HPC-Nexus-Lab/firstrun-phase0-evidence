# Criteria for the held-out real-user confirmation

Written 2026-10-21, after freezing firstrun0 v0.3 (fingerprint `d6f22f9ac3d1007c…`, `../FROZEN.json`) and
**before any confirmation job was selected, downloaded or read**. Committed to git in `firstrun_phase0` before the
`select` stage ran; the commit time is the proof. Scoring code: `analysis/realusers_confirm.py` at sha256
`f91be647e38902a3a219508209cd7544c7c26e6c67166ab5837b684bead4d83b`, with the thresholds below copied into it. A criterion that fails is reported as failed; thresholds
and definitions are not changed after results are seen.

## What was known when this was written

- The development real-user study (each user's earliest 4 GPU jobs, 1,125 jobs from 310 users) and its reports
  (`firstrun_realusers/results/REALUSERS.md`, `ROBUSTNESS.md`). The claims below come from it.
- The v0.2 benchmark confirmation (`firstrun_phase0_confirm/results/CONFIRMATION.md`), which motivated v0.3.
- v0.3 was developed on the benchmark development set and the development real users only.
- **Nothing about the confirmation jobs**: not their number, size, Slurm states or telemetry.

## Data

Each real user's **next 4 GPU jobs**: ranks 5-8 by submit time (ties broken by job id), using the same ordering
that gave the development selection ranks 1-4. Excluded: every job id in the development `jobs_all.parquet` or
`gpu_manifest.csv`, and every labelled benchmark job. All Slurm states, no size cap. Users with fewer than 5 GPU
jobs contribute nothing. A job whose traces cannot be read is reported as missing, not replaced.

## Protocol

- **Pipeline:** frozen v0.3, verified against `FROZEN.json` before each stage that computes results. The
  development users' jobs 1-4 are re-read with the same v0.3 code, so training and test rows come from identical
  code; every v0.2 column must come out unchanged.
- **Primary, "unseen users":** users keep their 10 groups from the development study. Jobs 5-8 of users in group
  g are predicted by models trained and calibrated only on jobs 1-4 of users in the other 9 groups. Every test job
  is untouched and comes from a user the model never saw. (Training on all development users would let a user's
  own early jobs inform the forecast of their later ones; that is reported as the secondary "returning users"
  protocol and is not judged.)
- **Batch** = Slurm `job_type` not containing `INTERACTIVE`. **Failed** = FAILED, TIMEOUT, OUT_OF_MEMORY or
  NODE_FAIL; CANCELLED is neither failed nor completed. **Idle** GPU = mean utilisation under 5%.

## Criteria

| # | Claim | Measured on | Passes if |
|---|---|---|---|
| C1 | A minute-10 check finds the GPUs that stay idle | every GPU of a new batch job that ran longer than 10 min. Flagged = mean utilisation over its first 10 min < 5%; idle = whole-run mean utilisation < 5% | recall (flagged and idle / idle) **≥ 90%** and false alarms (flagged but not idle / flagged) **≤ 15%** |
| C2 | Minute 10 warns of runs that will fail, for unseen users | new batch jobs that ran longer than 10 min and ended COMPLETED or failed. Features and classifier as `realusers.py failures` (10-min telemetry + request), trained on development jobs of every type | AUROC **≥ 0.70** |
| C3 | Strong-rhythm runtime bounds are honest | new COMPLETED jobs longer than 20 min whose rhythm is strong under v0.3, with the oracle step count; 90% bounds (alpha = 0.1) | coverage **≥ 85%** at 10 **and** 20 min |
| C4 | Peak memory is known by minute 10 | new COMPLETED jobs longer than 20 min, no step count (undeclared scenario) | median absolute error **≤ 1%** at 10 min |

## Reading rules, fixed now

- **Giant jobs.** The primary verdict uses all new jobs. Each criterion is also computed with the 5 new jobs of
  largest GPU energy removed from the test set (models are not retrained). Both verdicts are reported; a claim
  "holds without the giant jobs" only if both pass.
- **Minimum sample.** C1 needs at least 20 idle GPUs; C2 at least 20 failing and 20 completing jobs; C3 at least
  10 strong-tier jobs at each cut; C4 at least 20 jobs. Below that the verdict is INCONCLUSIVE, which is not a
  pass.
- **Uninformative bounds.** A C3 pass whose median bound half-width exceeds 100% (bounds wider than x2 and /2) is
  reported as "PASS (uninformative bounds)": the bounds are honest but too wide to support a tight-forecast claim.
- **Uncertainty.** Wilson 95% intervals for proportions and a bootstrap 95% interval (2,000 resamples, seed 7) for
  AUROC are reported next to each value. The verdict uses the point estimate.
- **Code fixes.** If the scoring code must be fixed after this commit, the fix and its reason go in the git history
  and in the report; thresholds and definitions stay as written here.

## Development values, for comparison (not criteria)

From the development study, under slightly different definitions: idle recall 98% (all job types, including jobs
shorter than 10 min) and 9% false alarms (batch, any length); warning AUROC 0.78 on batch jobs (out-of-fold by user
group, v0.2 features); peak-memory median error 0.0% at 10 min; strong-tier coverage 100% with a median half-width
of about 1,300% (16 jobs at 10 min). The scoring stage recomputes all four on jobs 1-4 under exactly the
definitions and code above.

## Known limits

- The confirmation users are the development users. "Unseen" holds only through the group protocol, and a user's
  later jobs may repeat their early ones (the same script resubmitted).
- Users with at least 5 GPU jobs are the more active users; their later jobs probably fail less than first jobs.
- The real-user strong tier is small (16 jobs at 10 min in development) and its bounds borrow the pooled quantile,
  so C3 is a weak test of the v0.3 calibration change. That change was motivated by benchmark data, for which no
  untouched labelled jobs remain.
- MIT Supercloud V100s, 2021-2022, academic users; GPU energy only (no host power). CC BY-NC-ND 4.0: derived data
  stays local.
