# PhysicsNeMo held-out validation v2

## Result

All 25 frozen checkpoints (five seeds over five spatial/time-node cases) were
re-evaluated on a new, fixed 64^3 periodic grid with fractional-cell phase
`0.618034`, different from the original evaluation phase `0.37`. The run used
the pinned PhysicsNeMo v2.2.1 source at
`1b961314e42a0625502ba1592d25f706f1e02a24`, Python 3.14.5, Torch 2.11.0,
CPU float64, and two threads. Protocol and harness were frozen at commit
`d2e71d71`; the per-model archive and checkpoint hashes, source-tree audit,
thresholds, and all outcomes are in
`evidence/physicsnemo-heldout-validation-v2/results.json`.

The prospectively declared cross-target tolerances were 2% for endpoint
velocity L2 and kinetic energy, and 5% for sampled gradient peak, vorticity
peak, shell-spectrum L1, and divergence normalized by the exact sampled
gradient peak. Nineteen models passed all six sampled metrics; six failed only
the 2% velocity L2 tolerance. The failures were seed 709 at n32/nt5 and seed
8191 in all five cases. Every model passed all sampled local metrics. No model
reproduced the predeclared conjunction “global sampled metrics pass while a
sampled local metric fails.”

| Case | Overall sampled quality | Global metrics | Local metrics | Velocity L2 mean [range] |
|---|---:|---:|---:|---:|
| n16 / nt5 | 4/5 pass | 4/5 pass | 5/5 pass | 1.866% [1.479%, 2.482%] |
| n32 / nt5 | 3/5 pass | 3/5 pass | 5/5 pass | 1.885% [1.470%, 2.500%] |
| n64 / nt5 | 4/5 pass | 4/5 pass | 5/5 pass | 1.894% [1.479%, 2.570%] |
| n64 / nt9 | 4/5 pass | 4/5 pass | 5/5 pass | 1.821% [1.449%, 2.366%] |
| n64 / nt17 | 4/5 pass | 4/5 pass | 5/5 pass | 1.772% [1.421%, 2.248%] |

`nt` is the PINN's training-time collocation-node count, not a time-step
refinement. This prospective evaluation reuses frozen trained weights but uses
previously unused spatial sample coordinates; it does not retrain or tune
models. The endpoint time is still a training collocation time. The old v1
verdicts remain unchanged.

## Scope and interpretation

This changes the PhysicsNeMo sampled acceptance evidence from “no numerical
threshold was preregistered” to a frozen, common sampled-quality policy and its
held-out outcomes. It does not certify an optimizer-converged model: each
training run completed 5,000 steps, which is only a run-integrity gate. The
64^3 values are finite samples; continuous gradient/vorticity extrema and
continuous local-quality verdicts remain `UNCERTAIN`. Seed 8191's repeated
velocity failures show this fixed training procedure is seed-sensitive under
the 2% policy; five seeds do not establish a population guarantee. No model
defect, incompressibility theorem, physical instability, molecular alignment,
or constitutive-viscosity change follows.

AMR is not applicable to this fixed-architecture PINN study. The odd-width
PhysicsNeMo spectrum issue remains separately tracked by [issue #2007](https://github.com/NVIDIA/physicsnemo/issues/2007)
and [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008); these even
64-point spectra do not exercise that bug. No duplicate upstream report was
filed.

Reproduce in the pinned environment:

```sh
PYTHONPATH=work/physicsnemo-source \
  work/physicsnemo-env/bin/python -m tools.physicsnemo_validation_v2 \
  --protocol protocols/physicsnemo-heldout-validation-v2.json \
  --output evidence/physicsnemo-heldout-validation-v2/results.json
```
