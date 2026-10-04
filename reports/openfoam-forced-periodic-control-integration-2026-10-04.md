# OpenFOAM forced-periodic exact-control integration

Date: 2026-10-04  
Scope: connect the exact smooth periodic solution from arXiv:2609.38210v1 to
the existing OpenFOAM Foundation 13 case generator.

## Implementation

`tools/openfoam_case.py` now accepts `profile="forced-periodic"`. It writes
the exact velocity and pressure at cell centers at time zero, plus a coded
momentum source for

`u_t + (u · ∇)u = -∇p + νΔu + f`.

For this reference, `u=exp(-2νt)u0`, `p=exp(-4νt)p0`, and
`Δu0=-2u0`; the time derivative and viscous term cancel, leaving
`f=exp(-4νt)((u0 · ∇)u0+∇p0)`. The generated source uses the Foundation 13
sign convention already audited in
`reports/openfoam-source-sign-audit-2026-09-28.md`. The case manifest records
the reference and forcing identity.

## Checks

Test-first case generation check: the new test initially failed because the
profile was rejected, then passed after implementation. It compares the
written initial velocity and pressure against the independent NumPy reference
at all cell centers and checks the transient forcing form. The existing
Gaussian/high-gradient case-generation test also passes.

A second test compiles and evaluates the actual emitted C++ source body at four
points with non-unit cell volumes and compares the recovered forcing with the
independent Python reference. It is configured to run on hosted Ubuntu CI. On
the current macOS host it was skipped because Apple's compiler refuses to run
until the Xcode license is accepted; no attempt was made to change system
license state. Thus the emitted C++ expression has not yet passed compilation
in this local run.

The generic OpenFOAM analyzer was also extended to select this exact reference
and measure pressure error after removing only the spatially constant gauge
offset. A synthetic archive containing exact fields initially failed because
the analyzer was selecting the Gaussian reference. After the profile-aware
fix, the synthetic velocity and gauge-invariant pressure errors are each below
`1e-15`; the OpenFOAM case/analyzer test group passes locally, with the C++
compiler test skipped for the host limitation above.

## Limits

This is case-generator and source-expression integration only. The Foundation
13 six-case workflow is now frozen in
`protocols/of13-forced-periodic-control-v1.json` and
`.github/workflows/forced-periodic-openfoam.yml`. It uses spatial n=16/32/64
at dt=0.001 and temporal dt=0.002/0.001/0.0005 at n=32, to t=0.05. The runner
refuses to overwrite prior outputs and saves failed as well as successful case
archives. The hosted run has not yet completed, so pressure-correction
behavior, space/time convergence, archived mesh errors, and full-horizon
completion are still unverified. The field is a smooth solver/source calibration control with
fixed Fourier support, not the paper's localized concentration simulation and
not evidence for molecular alignment, particle-position certainty, or a
viscosity transition. Any solver result remains contingent on independent
input, convergence, and execution-record checks.
