# Methods in brief

## Data

| Dataset | What it is | Used for |
|---|---|---|
| MIT Supercloud, labelled jobs | 3,430 deep-learning jobs in 10 model families run by the MIT team; V100 GPUs; `nvidia-smi` every 100 ms | Development of the estimators (731 jobs), benchmark confirmation, GPU count (C4), period check (C6) |
| MIT Supercloud, real users | Unlabelled GPU jobs of academic users with Slurm accounting | C1–C4: each user's first 4 GPU jobs (development, 1,125 jobs, 310 users) and next 4 (held-out, 956 jobs, 251 users) |
| Elsayed et al. 2026 | 8-GPU H100 and B200 nodes, 15-minute sessions, 20 ms sampling | Idle power (C6) |
| Own fault-injection jobs | 13 jobs on a GTX 1660 SUPER | Diagnosis pilot (C5) |

## Pipeline (frozen as v0.3 before the held-out test)

1. **Read the telemetry** per GPU: utilisation, power, memory; Slurm request and final state.
2. **Steady-state onset** by change-point detection, so the start-up phase is skipped.
3. **Cycle (period)** by autocorrelation of utilisation and of power, with an octave guard against harmonics; a
   rhythm counts as strong only if the two periods agree within 10% (v0.3).
4. **Features at minute t** (t = 0, 1, 2, 5, 10, 15, 20): power, memory, idle GPUs, period and its strength.
5. **Prediction with calibrated bounds:** leave-one-group-out models with cross-conformal 90% bounds (α = 0.1).
6. **Replay** of time-limit policies with kill-and-retry energy accounting (C4).

The frozen pipeline is identified by a fingerprint (`d6f22f9ac3d1007c…`) checked before each scoring stage.

## Evaluation discipline

1. Freeze the code and record its fingerprint.
2. Write the pass criteria before the test data are selected or read, and commit them to git.
3. Score once on untouched jobs. A failed criterion is reported as failed; thresholds are not changed afterwards.
4. Anything learned after looking is labelled post hoc or exploratory and changes no verdict.

Proportions carry Wilson 95% intervals; AUROC carries a bootstrap 95% interval (2,000 resamples).
