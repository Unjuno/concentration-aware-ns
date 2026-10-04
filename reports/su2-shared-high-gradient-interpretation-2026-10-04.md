# Interpretation rules for the SU2 shared high-gradient matrix

These rules were recorded before any solver result from run `37190363204` was
available. They supplement, but do not modify, the frozen case protocol
`protocols/su2-shared-high-gradient-v1.json` (SHA-256
`dacd7638a306a810c986ce8d5922f16e55a76698b67d97f7ff892b7f6c9b60aa`).

## Separate verdicts

- **Standard acceptance, per case:** process exit 0, SU2 success marker,
  exactly the planned time updates, and all four logged residuals at or below
  `-10` for every update.
- **Sampled solution quality, per case:** apply the five frozen thresholds for
  velocity, energy, sampled gradient peak, sampled vorticity peak, and sampled
  spectrum. This remains a finite-grid sampled verdict.
- **Replay integrity:** the archive verifier must reproduce saved diagnostics
  within its fixed `1e-12` replay-only comparison tolerance and validate the
  protocol, patch, archive and field-file hashes.

No conjunction of these verdicts is a mathematical singularity test or proof
of a SU2 implementation defect.

## Resolution boundary

The exact-field FD2 floor on SU2's unique vertex phase is `FAIL` at n=16 and
n=32 for the 5% peak-gradient and peak-vorticity limits, and `PASS` at n=64.
Therefore n=16/n=32 local metric failures are resolution-limited observations.
An n=64 local failure, if standard acceptance passes and archive replay
succeeds, is an **observed fine-grid quality gap under this test**. It remains
`UNCERTAIN` as a reproducible acceptance blind spot because this matrix has
only one spatial resolution whose exact-field operator floor meets both peak
limits. The n=64 temporal rows reuse the same spatial grid and do not count as
independent spatial replications.

Classify the frozen SU2 experiment as:

- **NOT_OBSERVED_AT_TESTED_RESOLUTION** only if n=64 passes both standard and
  sampled-quality gates with successful archive replay. This says nothing
  about other meshes, equations, or physical regimes.
- **OBSERVED_FINE_GRID_QUALITY_GAP** if n=64 passes standard acceptance and
  replay but fails one or more sampled-quality thresholds. Do not file an
  upstream defect from this alone.
- **UNCERTAIN / INCOMPLETE** if n=64 misses standard acceptance, its replay or
  input checks fail, or its exact-field operator floor is not reproduced.

To call an acceptance blind spot **REPRODUCED** and consider a SU2 issue, a
successor run must add a second spatially finer, floor-adequate mesh (n=128),
freeze it before execution, and reproduce standard-PASS/local-quality-FAIL on
both n=64 and n=128 after archive replay. Existing SU2 issues and contribution
guidance must then be refreshed and checked for overlap. Until those conditions
hold, no upstream report is warranted.

All interpretations are limited to the smooth incompressible manufactured
solution. They do not imply molecular alignment, deterministic particle
positions, phase transition, a physical viscosity change, blow-up, or hazard.
