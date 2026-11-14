# Glossary

Terms used in the claims and figures, in plain words.

## Jobs and clusters

| Term | Meaning |
|---|---|
| **Slurm** | The job scheduler used on most supercomputers, including MIT Supercloud and CloudCIX's Boole. Users submit a job with a request (GPUs, memory, time limit); Slurm queues it and runs it when resources are free. |
| **Batch job** | A script that runs unattended from start to finish. Most results here are on batch jobs. |
| **Interactive session** | A job that opens a shell or notebook for a person to work in. Often left open and idle. |
| **TIMEOUT** | Slurm's state for a job killed because it reached its time limit. It can be waste (a stuck job) or a long job that saves checkpoints and is resubmitted to continue. |
| **Idle GPU** | A GPU allocated to a job whose mean utilisation over the whole run stayed under 5%. |
| **Users' first 4 jobs / next 4 jobs** | Each MIT Supercloud user's GPU jobs in submission order: jobs 1–4 were used to develop the method; jobs 5–8 were set aside, untouched, for the final test. |
| **The 5 largest jobs** | The five jobs with the most GPU energy in the test set; together they hold 44% of it. Every pre-registered result is also reported without them, so a few giant jobs cannot drive a conclusion. |

## Evidence

| Term | Meaning |
|---|---|
| **Pre-registered** | The pass criteria were written and committed to git before the test data were selected or read. A criterion that fails is reported as failed. |
| **Held-out** | Measured on data that no analysis had touched while the method was being built. |
| **Development data** | The data the method was built and tuned on. Results there show what was learned, not what was confirmed. |
| **Exploratory / post hoc** | An analysis chosen after looking at the data. A lead to test, not a result. |
| **Unseen users** | For trained models (the failure warning, C3): each user is scored by a model built only on other users' jobs. |
| **Returning users** | The model has also seen the same user's earlier jobs, as it would for an established customer. |

## Measures

| Term | Meaning |
|---|---|
| **Recall** | Of the GPUs that really stayed idle, the share the minute-10 check flagged. |
| **False alarms** | Of the GPUs the check flagged, the share that were used later in the run. |
| **AUROC** | How well a warning ranks failing runs above completing ones: the chance that a randomly chosen failing run gets a higher warning score than a randomly chosen completing run. 0.5 is a coin flip, 1.0 is perfect. |
| **95% interval** | The range the true value is likely to lie in, given how many jobs were measured (Wilson intervals for shares, bootstrap intervals for AUROC). |
| **Regret** | Extra energy a choice uses compared with the best possible choice for that job. |

## The method

| Term | Meaning |
|---|---|
| **Cycle (period)** | The repeating pattern of a training job, usually one training step, read from the rise and fall of GPU activity and power. |
| **Strong rhythm** | A cycle found clearly, with GPU activity and power agreeing on its length within 10%. |
| **Steady-state onset** | When start-up (loading data, compiling) ends and the repeating cycle begins. |
| **Conformal bounds** | A way of putting a range around a forecast that is calibrated on past jobs, so that a 90% bound should contain the true value about 90% of the time. |
| **Coverage** | How often the bounds actually contained the true value. |
| **Declared step count (oracle)** | The total number of training steps, if the job states it. Here it is read from the finished run to show the best case; FirstRun would use it only when a customer declares it. |
| **Telemetry gate** | In the diagnosis pilot (C5): the language model may only choose a cause consistent with the job state the telemetry rules see. Devised after the run. |
