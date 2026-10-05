# PhysicsNeMo matched high-gradient MMS study

## Why this study was added

The existing PhysicsNeMo PINN study uses the Gaussian-streamfunction MMS in
`tools/reference.py`, while the OpenFOAM and SU2 local-concentration studies use
the periodic Fourier-envelope MMS in `tools/high_gradient_reference.py`. The
old PhysicsNeMo results therefore do not constitute a matched three-target
experiment. This additive study implements the latter MMS in Torch and retains
the Gaussian study and its artifacts unchanged.

## Independent formulation check

`tools/physicsnemo_shared_mms.py` expresses the exact velocity using Torch
operations so autograd can differentiate it. Before running PINN training, its
values and first spatial derivatives were compared with the independent NumPy
reference at three points. A second check computed the full transient momentum
residual by Torch autograd and supplied forcing from the independent NumPy
implementation. Both tests passed; the residual maximum was below `2e-11`.
These checks establish consistency of this implementation at sampled points,
not a continuum proof or a solver validation result.

## Frozen experiment

The prospective protocol is
`protocols/physicsnemo-shared-high-gradient-v1.json`. It fixes the source at
PhysicsNeMo v2.2.1 commit `1b961314e42a0625502ba1592d25f706f1e02a24`, CPU
float64, a 3x32 tanh network, 5,000 Adam updates, five seeds, three spatial
cases, three time-node cases (with the shared `n=64, nt=5` case counted once),
and independent 64^3 phase-shifted evaluation. Thresholds match the existing
cross-target acceptance policy. They are sampled engineering tolerances, not
mathematical bounds.

## Completed execution and interpretation

All 25 prescribed models completed with exit code 0 and exactly 5,000 logged
optimizer updates. The independent archive audit verified all 25 archive
hashes, case/seed metadata, final finite losses and finite validation metrics.
The machine-readable record is
`evidence/physicsnemo-shared-high-gradient-v1/verification.json`; its summary
reports `COMPLETE` for run integrity. Every model returned sampled quality
`FAIL` under the preregistered thresholds. Continuous local quality remains
`UNCERTAIN`.

The table gives the mean and sample standard deviation across five seeds; all
values are percentages. The columns follow protocol order: velocity relative
L2, energy relative error, sampled gradient-peak relative error, sampled
vorticity-peak relative error, shell-spectrum relative L1, and normalized
divergence peak.

| Case | Velocity | Energy | Gradient peak | Vorticity peak | Spectrum | Divergence |
|---|---:|---:|---:|---:|---:|---:|
| n16, nt5 | 6.634 ± 0.565 | 10.689 ± 0.077 | 5.154 ± 0.003 | 5.146 ± 0.009 | 10.689 ± 0.077 | 0.407 ± 0.076 |
| n32, nt5 | 6.582 ± 0.618 | 10.682 ± 0.085 | 5.155 ± 0.007 | 5.153 ± 0.007 | 10.682 ± 0.085 | 0.404 ± 0.085 |
| n64, nt5 | 6.561 ± 0.596 | 10.680 ± 0.081 | 5.158 ± 0.005 | 5.154 ± 0.010 | 10.680 ± 0.081 | 0.405 ± 0.083 |
| n64, nt9 | 6.657 ± 0.678 | 10.693 ± 0.093 | 5.157 ± 0.006 | 5.154 ± 0.008 | 10.693 ± 0.093 | 0.418 ± 0.086 |
| n64, nt17 | 6.725 ± 0.667 | 10.701 ± 0.093 | 5.158 ± 0.007 | 5.155 ± 0.009 | 10.701 ± 0.093 | 0.428 ± 0.089 |

The 2% velocity and energy limits and 5% spectrum limit are exceeded in every
case; the mean sampled gradient-peak error also exceeds its 5% limit in every
case. The normalized divergence stays below its 5% limit. Increasing the
spatial collocation count from 16 to 64 at five time nodes does not materially
change the measured errors for this network and optimizer budget. Increasing
time nodes from 5 to 17 at n=64 likewise does not improve these metrics. These
are descriptive results for this frozen PINN configuration, not asymptotic
convergence statements.

The preregistered sampled blind spot is **not reproduced**: its decision rule
requires at least one global metric to pass while a local metric fails. Here,
global metrics fail along with the sampled gradient and vorticity metrics.
This study identifies a PINN approximation-quality limitation for this task;
it does not identify an OpenFOAM, SU2, or PhysicsNeMo solver defect, a
continuum error floor, or a physical concentration phenomenon. The 64^3 grid
does not certify continuous extrema, and the fixed training budget does not
certify optimizer convergence.

The one-update preflight smoke run is archived separately at
`evidence/physicsnemo-shared-high-gradient-smoke/seed709-n16-nt5-smoke.tar.gz`
(SHA-256 `8c60460f174ce11e7982452bfb361926609cb3c5d2d7cc03666fb4df46090542`).
It is explicitly marked `SMOKE_ONLY` and is not counted among the 25 models.

## Scope limits

The historical Gaussian-streamfunction study is not changed. The high-gradient
MMS is smooth and periodic; this experiment tests whether a PINN meets the
sampled field and derivative tolerances on that known solution. It does not
test molecular alignment, phase transition, a Navier–Stokes singularity, or
physical material behavior. A finite 64^3 evaluation grid cannot certify
continuous extrema, and a fixed optimizer budget is not a convergence proof.
