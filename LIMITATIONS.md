# What did not hold up, and the limits of Phase 0

Listed beside the claims on purpose: the negative results shaped the proposal as much as the positive ones.

## Results that failed or were uninformative

| Finding | Evidence | Consequence for the proposal |
|---|---|---|
| Recommended time limits never beat users' own finite requests (R10 **FAIL**) | Pre-registered, development real users | Sizing before the run was dropped as a core aim; probing is a stretch goal tested as a comparator |
| Runtime cannot be forecast without a declared step count: 60–90% error, and watching longer does not reduce it | Pre-registered (R9 pass, as predicted) | Runtime is forecast only for repeating jobs of declared length |
| Strong-rhythm runtime bounds on held-out real users: formally pass, but ±800–1,400% wide; median error 2–5%, not the ~1% seen on benchmarks | Pre-registered (C3, "uninformative bounds") | No tight-forecast claim is made for real users |
| v0.2 benchmark confirmation: strong-tier coverage 74% against an 85% target (3 of 6 criteria failed) | Pre-registered, benchmark | Led to the period-agreement rule (v0.3), which is development evidence only |
| Choosing GPU type (H100 vs B200): the 5-minute measurement transfers, but the energy gap is 9% | Exploratory | Not a deliverable; Boole is a single GPU type |
| Power caps: worthwhile mainly for jobs longer than about 10 hours, on older GPUs (Zeus traces) | Exploratory | A stretch goal only |
| The pre-registered diagnosis model (qwen3:8b) failed all four pilot criteria | Exploratory pilot | The 13/13 gate result needs its own pre-registered test |

## Limits of the data

- **Not Boole.** MIT Supercloud academic users on V100 GPUs, 2021–2022. CloudCIX customers, B200 hardware and job
  mix may differ; WP1 measures Boole's own baseline before targets are fixed.
- **"Unseen users" through a group protocol.** The held-out jobs are later jobs of the same users; users are unseen
  only in the sense that each is scored by models built on other users' jobs.
- **GPU energy only.** Host CPU, memory and network power are not in the public data.
- **Giant jobs.** Five jobs hold 44% of held-out GPU energy; every pre-registered criterion is also reported without
  them, and energy shares are quoted as ranges.
- **Labels from telemetry and Slurm.** A job that "completed" but produced nothing useful counts as completed.
- **Offline replay.** No advice was delivered to anyone; savings from customers acting on advice are modelled in
  the proposal at 25%, 50% and 75% action rates, not measured.
