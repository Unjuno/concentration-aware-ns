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
The same generated-source comparison was included in the Ubuntu Python suite
at commit `0c37949d545e9f08629bd1324ada2eb9bf0f152b`; that full run reports
407 passed, one skipped, and 89 subtests. The macOS skip therefore reflects
only the local Xcode license constraint. The subsequently added archive-replay
tool and this report revision also pass the complete local Python suite: 407
passed, two skipped, and 89 subtests.

The Foundation 13 hosted solver subsequently built and ran all six cases at
source commit `1cacf3c282a2c6ea5a81354865bba1ab0e932427` in image
`sha256:383b0f958aa9867af6e2db9ec7681141393c9d213cd821c1f68a33f4353f0baf`
(`linux/arm64`). Each case's `codedFvModel` therefore compiled and executed in
the solver itself. The Actions run is
[37174784940](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37174784940).
Downloaded case archives, image/package build evidence, and protocol are
preserved under
`evidence/of13-forced-periodic-control-hosted-1cacf3c/`; independent archive,
hash, exit-code, time-grid, and diagnostic replay passes in `verification.json`.

The generic OpenFOAM analyzer was also extended to select this exact reference
and measure pressure error after removing only the spatially constant gauge
offset. A synthetic archive containing exact fields initially failed because
the analyzer was selecting the Gaussian reference. After the profile-aware
fix, the synthetic velocity and gauge-invariant pressure errors are each below
`1e-15`; the OpenFOAM case/analyzer test group passes locally, with the C++
compiler test skipped for the host limitation above.

## Solver results

All six cases reached t=0.05 with exactly the prescribed number of steps and
an `End` record: 50/50/50 for spatial n=16/32/64, and 25/50/100 for temporal
n=32 at dt=0.002/0.001/0.0005. Applying the repository's existing Foundation
13 standard stopping gate after the run (absolute outer-corrector tolerance
1e-8, 12 correctors, exact fixed-step sequence) gives PASS for all six. Every
step has a PIMPLE convergence record; the observed maximum is five iterations,
except n32/dt=0.0005 where it is four.

| Cases | Velocity relative L2 | Gauge-free pressure relative L2 | Sampled gradient peak relative error | Sampled vorticity peak relative error |
|---|---:|---:|---:|---:|
| n16, dt=0.001 | 2.706e-3 | 1.168e-1 | 2.496e-2 | 2.037e-2 |
| n32, dt=0.001 | 6.980e-4 | 3.232e-2 | 6.243e-3 | 4.916e-3 |
| n64, dt=0.001 | 1.733e-4 | 7.060e-3 | 1.564e-3 | 1.217e-3 |
| n32, dt=0.002 | 6.984e-4 | 3.267e-2 | 6.242e-3 | 4.916e-3 |
| n32, dt=0.0005 | 6.972e-4 | 3.167e-2 | 6.246e-3 | 4.915e-3 |

Spatial velocity errors show observed orders 1.955 and 2.010 across the two
doublings; gauge-free pressure errors show 1.853 and 2.195. Sampled derivative
errors also fall by about four at each spatial doubling. This is evidence of
convergence for this smooth manufactured control, not the concentration case.

The three time-step cases complete and their errors are recorded, but their
total-error changes at fixed n=32 are small and do not isolate temporal error
from the spatial error floor. The temporal-order assessment remains
`UNCERTAIN`; a more sensitive temporal control is still needed. There was no
predeclared local-quality threshold for this calibration field, so its
`quality` label remains `UNCERTAIN` even though the retrospective standard
stopping gate passes.

## Limits

The six-case workflow is frozen in
`protocols/of13-forced-periodic-control-v1.json` and
`.github/workflows/forced-periodic-openfoam.yml`. The runner refuses to
overwrite prior outputs and saves failed as well as successful case archives.
Pressure correction and spatial refinement are now exercised for this smooth
field; resolved temporal order remains open, and no localized high-gradient
or AMR behavior is tested here. The field has fixed Fourier support, is not the
paper's localized concentration simulation, and provides no evidence for
molecular alignment, particle-position certainty, or a material-viscosity
transition. Any solver result remains contingent on independent input,
convergence, and execution-record checks.
