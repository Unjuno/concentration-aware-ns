# OpenFOAM Foundation 13 high-gradient AMR matrix — 2026-10-02

## Frozen comparison

The AMR settings were recorded before execution in
[`protocols/high-gradient-of13-amr-v1.json`](../protocols/high-gradient-of13-amr-v1.json)
(SHA256 recorded in the matrix manifest). All runs use the pinned Foundation 13
image and compare against the uniform `n=64`, `dt=0.001`, `T=0.05` control. The
three AMR cases begin from an `n=16` mesh and use the corrected analytic sensor
`(partial_x u_y)^2`, refine interval 2, and maximum level 2. Their archived
inputs, logs, endpoint fields, and hashes are listed in
[`evidence/of13-high-gradient-v2/matrix-manifest.json`](../evidence/of13-high-gradient-v2/matrix-manifest.json).

## Results

| Requested cell cap | Actual endpoint cells | Level counts | Cells above cap | Volume-weighted velocity L2 error |
|---:|---:|---|---:|---:|
| 4,096 | 4,096 | level 0: 4,096 | 0 | 8.876% |
| 5,000 | 5,440 | level 0: 3,904; level 1: 1,536 | 440 | 32.070% |
| 100,000 | 21,120 | level 0: 3,584; level 1: 2,176; level 2: 15,360 | 0 | 38.572% |

The `cap4096` case did not refine; the endpoint has no `cellLevel` field, and
both the initial cell count and the absence of refinement events support level
zero. `cap5000` exceeded its requested cap by 440 cells after refinement. The
runtime did not report blocked candidate counts. The 100,000-cell case reached
level 2 but used only 21,120 cells, so it does not show budget saturation.
Nonuniform shell spectra remain unavailable because no reconstruction method
has been validated.

A second weighted-error calculation independently reproduces the global errors
from the archived cell centers, velocities and volumes. It also shows where the
squared error accumulates: at cap 5,000, level-1 cells occupy 4.69% of the
volume but contribute 92.10% of the total weighted squared error; at cap
100,000, level-2 cells occupy 5.86% of the volume and contribute 77.89% of the
error. The endpoint volume sum is `248.0502134424`, matching `(2*pi)^3`.
The raw calculation and field hashes are in
[`evidence/tests/of13-high-gradient-amr-error-strata.json`](../evidence/tests/of13-high-gradient-amr-error-strata.json).

For context, the uniform `n=16` control has 8.876% velocity error and the
uniform `n=64` control has 0.478%. Refinement therefore did not improve this
particular `n=16` initialized AMR sequence, and the measured error increased as
the tested cell cap/attained level rose. These are this-matrix observations,
not a universal statement about AMR.

## Interpretation and next discriminators

All cases exit with code 0, reach `T=0.05`, and end with `End`. The source-backed
standard-acceptance checker reports PASS for each run: Foundation 13's configured
outer-corrector convergence decision is observed on every physical step, with
the case's frozen iteration and endpoint requirements satisfied. The separate
v2 local-quality gate reports FAIL because volume-weighted velocity L2 exceeds
the preregistered 2% threshold in all three AMR cases; the fine uniform control
is below it. The combined gate therefore classifies an acceptance/local-error
discrepancy as REPRODUCED for these tested cases. Machine-readable reports are
`of13-high-gradient-amr-cap*-gate.json` and `*-verdict.json` in `reports/`.

This is a scoped discrepancy observation, not evidence of an OpenFOAM defect or
a general acceptance blind spot: all AMR cases start from the coarse `n=16`
base mesh, and base-mesh error, refinement interpolation, sensor/schedule and
runtime interactions are confounded. The standard PASS records the configured
outer-corrector decision; raw debug residual histories were not enabled, and
source-to-binary identity is not established. The velocity-error interval is
the protocol-defined discrete, volume-weighted cell-center quantity with a
`1e-12` numerical roundoff budget. Other metrics have unavailable upper bounds,
so this is a proved threshold failure, not a comprehensive quality assessment.

The discrepancy could be caused by the coarse `n=16` base field, interpolation
and conservation during refinement, the sensor/adaptation schedule, or another
runtime interaction. The error stratification locates much of the difference in
refined cells but does not identify which mechanism caused it. No OpenFOAM
upstream defect is established. A discriminating follow-up should separately
compare a non-refined `n=16` run with the cap-4096 control, inspect field
conservation across the first refinement event, and repeat the same AMR schedule
from a better-resolved base mesh before making a software claim.

The velocity metric is a proved local-quality FAIL for these runs; unbounded
peak-gradient, peak-vorticity and spectrum metrics remain unresolved. The
frozen AMR protocol itself remains unchanged; this post-run classification is
recorded separately by the v2 gate. This smooth MMS does not model the OpenAI
construction and provides no evidence of blow-up, molecular alignment,
particle-position certainty, phase transition, or constitutive-viscosity change.
