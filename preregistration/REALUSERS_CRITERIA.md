# Criteria for the real-user study

Written 2026-10-21 14:41, against `analysis/realusers.py` at sha256 `c8dcc940…7fed65` (frozen firstrun0 v0.2
functions underneath, fingerprint `bcfa94b8…`). The thresholds below are not changed after results are seen; a
criterion that fails is reported as failed.

## What was known when this was written

Be exact about this, because the study was already running:

- **Not yet computed:** the `failures` stage (it was at 650 of 1,125 jobs) and the report. Criteria R1–R6 are
  therefore set before their results exist.
- **Computed but not opened:** `lofo_summary.csv` and `replay_summary.csv` were written at 14:04. Neither file, nor
  the part of `realusers_log.txt` that prints them, was read in the session that wrote these criteria. Criteria
  R7–R10 are set before reading, not before computing. Whether anyone else has looked at them is not known here.
- **Seen:** the job counts by Slurm state from the `table` stage: 1,125 jobs, 411 COMPLETED, 295 CANCELLED,
  253 FAILED, 160 TIMEOUT, 6 OUT_OF_MEMORY. Counts, not energy.
- Context from development (benchmark jobs, MIT team): only COMPLETED jobs were used, users' limits were almost
  all unlimited, 1 of 715 jobs had an idle GPU, and tightening time limits never beat the users' requests on
  energy.

## The two questions

1. **Energy:** do real users waste enough GPU energy, visibly enough by minute 10, for a watcher to matter?
   This is the first test of the energy half of the research question under real conditions.
2. **Prediction:** do the calibrated forecasts carry over to users the model has never seen?

"Failed" means FAILED, TIMEOUT, OUT_OF_MEMORY or NODE_FAIL, as in `realusers.py`. CANCELLED is kept apart.
All energies are GPU energy from `nvidia-smi`; host power is not in the data.

## Energy (from `failures.json`, not yet computed)

| # | Claim | Passes if |
|---|---|---|
| R1 | Failed runs are a material share of energy | failed-run energy ≥ 10% of all GPU energy |
| R2 | Most of that waste happens late enough to act on | `failed_energy_after10_share_pct` ≥ 50% |
| R3 | Minute 10 can tell which runs will fail, for unseen users | `warning_auroc` ≥ 0.70 |
| R4 | The addressable saving is worth building for | at 10% false alarms, `failed_energy_after10_flagged_kwh` ≥ 3% of all GPU energy |
| R5 | Idle reserved GPUs are a second, visible target | `idle_energy_after10_kwh` ≥ 1% of all GPU energy, and `idle_seen_by_10min_pct` ≥ 80% |
| R6 | Extend-instead-of-kill has something to save | TIMEOUT jobs ≥ 5% of all GPU energy (`by_state`) |

Reading: the energy half is **supported for waste avoidance** if R1–R4 all pass. If R4 fails, avoiding wasted runs is
not a material energy lever for these users, and energy savings would have to come from power caps (Zeus replay)
or from Boole looking different from MIT. R4 and R5 are upper bounds: they assume every flagged run is fixed or
stopped.

## Prediction for new users (from `lofo_summary.csv`, computed, not read)

Same bars as the benchmark confirmation (C2–C4, C6), so the two can be compared directly. Leave-users-out, 10 user
groups, completed jobs only, alpha = 0.1.

| # | Claim | Passes if |
|---|---|---|
| R7 | Strong rhythm + step count (oracle) predicts runtime | strong-tier runtime median error ≤ 1% at 10 and 20 min |
| R8 | Bounds stay honest for new users | pooled coverage ≥ 85% for runtime and energy at 10 and 20 min, both scenarios |
| R9 | Without the step count, watching still does not help runtime | median error at 20 min not below 0.8 × the 0-min error (undeclared) |

## Time limits against real requests (from `replay_summary.csv`, computed, not read)

The replay uses completed jobs only, so the users' own requests can never have killed them. On energy, the
`requested` policy is unbeatable here by construction. That is not tested; the useful question is reserved time.

| # | Claim | Passes if |
|---|---|---|
| R10 | Forecast limits free reserved time at small energy cost | at alpha = 0.1, the best non-oracle policy cuts median slack by ≥ 50% vs `requested`, with energy overhead ≤ 10% |

## Known limits of this study

- MIT Supercloud academic users on V100s, 2021–2022; not CloudCIX customers or B200s.
- Each user's earliest 4 GPU jobs stand in for new customers. Early jobs probably fail more than later ones, so
  R1–R4 may overstate waste for established customers.
- No declared step counts exist for these jobs; R7 uses the same oracle as development.
- Labels are inferred from telemetry and Slurm, so jobs that "completed" but produced nothing useful count as
  completed.
