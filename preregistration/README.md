# Pre-registration files and their provenance

The files in this folder are copied **verbatim** from the private Phase 0 repository (`firstrun_phase0`). Paths
inside them refer to that repository. Commit dates and file dates below are recorded by the author's own tools;
they are not third-party timestamps. Future pre-registrations for the Fellowship will be deposited with a
timestamping service (OSF or Zenodo).

| File | Used for | Provenance | sha256 |
|---|---|---|---|
| [REALUSER_CONFIRMATION_CRITERIA.md](REALUSER_CONFIRMATION_CRITERIA.md) | C2, C3 (held-out test) | Committed in git `89bda07` on 2026-10-21 15:42 (+01:00), with the v0.3 freeze. Test jobs were selected at 15:43 (`selection.json`) and scored on 2026-10-22. Unchanged since the commit. | `6d469d5d…cdef0` |
| [REALUSERS_CRITERIA.md](REALUSERS_CRITERIA.md) | C4 time limits (R10), C1 context | Written 2026-10-21 14:41, committed in `89bda07` at 15:42. The file itself states that R7–R10 were set after their results were **computed but before they were read**, and R1–R6 before their results existed. Unchanged since the commit. | `2bd670d0…0b8a1` |
| [diagnosis_pilot_CRITERIA.md](diagnosis_pilot_CRITERIA.md) | C5 | **Not committed to git.** File dated 2026-10-22 13:13; recording began 13:56. Names qwen3:8b as the judged model and qwen3-coder:30b as reported, not judged. The telemetry gate is not in it: that result is post hoc. | `e9601dc5…88697` |

Frozen pipeline fingerprint (v0.3): `d6f22f9ac3d1007ce6f1b31766c64e70ea52e0650a47b51851179ceae7fc5285`.
