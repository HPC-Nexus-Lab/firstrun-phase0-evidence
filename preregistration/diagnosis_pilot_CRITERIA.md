# Fault-injection pilot: pre-registered criteria

Written before any case was recorded or diagnosed (2026-10-22). Exploratory pilot for the FirstRun proposal's O4.

## Cases

13 jobs on one GTX 1660 SUPER: 10 with one injected fault each, 3 healthy controls. Neutral ids c01-c13
(shuffled, seed 20261022); the answer key (`key/labels.json`) is never shown to the model.

| Telemetry class | Causes in the pilot |
|---|---|
| GPU unused, CPU busy | cpu_only_build, not_moved_to_gpu, gpu_hidden_by_env, cpu_workload_on_gpu_node |
| Nothing running | hung_waiting_for_peer, idle_interactive_session |
| Low GPU use | input_pipeline_bottleneck, batch_too_small, (healthy GNN at moderate use) |
| GPU memory growing | gpu_memory_leak |
| Some GPUs idle | single_gpu_code_multi_gpu_request |
| GPUs used | healthy CNN, healthy LLM fine-tune |

Five cases run their script for real on this machine's CPU-only PyTorch (made to look like a CUDA cluster
where needed); seven reproduce the script's GPU and CPU behaviour with real CUDA kernels and allocations and
print generated log lines; one is an idle interactive session. Extra requested GPUs (2 in one case, 4 in
another) have simulated idle traces. Telemetry is the first 3 minutes of each job.

## What the agent sees

The batch submission, the script with line numbers (none for the interactive session), the job log, and a
telemetry summary of numbered facts. It must pick one cause from the closed list above (plus `healthy`), cite
evidence ids, and write a short message to the user. Model: qwen3:8b via Ollama on this machine, temperature 0.

The verifier accepts a diagnosis only if every cited id exists and, for a fault, it cites at least one
telemetry fact and at least one script, log or submission line (telemetry only for the interactive session).
A rejected diagnosis counts as wrong.

## Criteria

- **D1** Verified cause correct for at least 8 of the 10 faulty jobs.
- **D2** Every cited evidence id exists in all 13 diagnoses.
- **D3** No healthy control is given a fault.
- **D4** At least 3 of the 4 "GPU unused, CPU busy" jobs get the right cause. A telemetry-only rule can get at
  most 1 of these 4, because their telemetry is the same.

Reported, not judged: the telemetry-only rule baseline on all 13; a second local model (qwen3-coder:30b);
time per diagnosis; the messages themselves.
