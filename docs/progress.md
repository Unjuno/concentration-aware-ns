# Progress

## 2026-09-09 — repository bootstrap

- User authorized repository creation after the initial read-only review.
- Host observed: Darwin arm64; git 2.54.0; GitHub account Unjuno.
- Docker daemon responds: linux aarch64. No solver/container has been executed.
- Initial PATH inspection did not find foamRun, simpleFoam or SU2_CFD.
- Primary source audit and draft protocol recorded.
- First deliverable: repository and conservative report checker.

## Remaining completion evidence

- Freeze full source pins, licenses, runtime images and protocol thresholds.
- Implement and independently verify reference/forcing and derivatives.
- Build OpenFOAM adapter; run full space/time studies and AMR controls.
- Implement SU2 and current PhysicsNeMo adapters and independent studies.
- Preserve real logs and reference/metric data in reproducible run manifests.
- Search duplicate upstream issues; submit only supported improvements.
- Publish complete audit with report URLs or reasons not to submit.

Neither a repository commit nor checker tests complete the benchmark goal.

## Analytic reference implementation

- Public repository created: https://github.com/Unjuno/concentration-aware-ns
- Implemented smooth periodic u, grad(u), curl(u) and analytic forcing in NumPy.
- Nine unit tests passed with `python3 -m unittest discover -s tests -v`.
  The finite-difference reconstruction uses three stencil widths and verifies
  approximately second-order error reduction. This is a formula consistency
  test, not the required three-grid CFD experiment.
- Broader independent reference verification, production parameter freezing,
  solver integration, run logs and upstream findings remain outstanding.

## OpenFOAM runtime and pilot setup

- Built the ARM64 runtime from Ubuntu 24.04 and the official Foundation
  `openfoam13_20260624_arm64.deb`, verifying the package SHA256.
- Built image ID:
  `sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`.
- Build log and observed official package index are in `evidence/environment/`.
- Added `tools/openfoam_case.py`: periodic 3D mesh, analytic initial velocity,
  laminar incompressible configuration and coded analytic forcing.
- Launched an 8^3-cell integration pilot at dt=0.001 through t=0.005 under a
  non-root container user. Completion is **not verified**. The initial blockMesh
  log remains empty and a separate Docker status request is also pending.
  Do not interpret this as a solver failure or restart a possibly live run.
- Runtime documentation/recipe are reproducible setup artifacts. Solver execution,
  C++ forcing correctness and the space/time studies remain unverified.

## Source identification and post-processing

- Located `openai/NavierStokesAndEuler` at the user's direction; recorded pinned
  statement audit in `docs/openai-source.md`. This replaces the missing-source
  issue, not the independent-proof-check requirement.
- Added uniform periodic-grid gradient/vorticity and shell-spectrum diagnostics.
  Verified known Fourier-mode energy, Parseval normalization and second-order
  derivative convergence; 13 unit tests pass. Raw output: `evidence/tests/`.
- Docker status query returned EOF; a bounded socket ping timed out after 10 s.
  Pilot exec session remains open, with no solver output. Runtime completion is
  unresolved; no shared Docker restart or duplicate pilot launch was attempted.

## OpenFOAM pilot completed; study-v1 prepared

The existing pilot process returned exit 0. blockMesh and foamRun logs end with
End. At t=0.005, a solver-written C field agrees with the generated cell ordering
within 1e-12. The 8^3 diagnostic velocity relative L2 error is approximately 0.146;
FD2 peak errors against analytic values at cell centers are approximately 0.448
(gradient) and 0.423 (vorticity). These include underresolution and derivative
errors, so no software-defect or acceptance-miss conclusion follows.

Added an ASCII field analyzer which requires verified coordinates and a completed
physical time. Study-v1 parameters/thresholds are frozen in protocols before its
execution; the generator now uses ordinary outerCorrectorResidualControl and
writes only at final time to limit disk usage. Full reference independence,
continuous extrema and uncertainty assessment remain required.

## Study-v1 partial results

16^3 and 32^3 completed with 50/50 outer-loop convergence messages each. Velocity
relative L2 errors are 0.0654 and 0.0187. Gradient peak errors at cell sample sites
are 0.224 and 0.0678. Applying FD2 to the analytic samples alone produces errors
0.235 and 0.0762, respectively: the apparent peak discrepancy is substantially
explained by derivative/sampling resolution, not evidence of a solver defect.
64^3 and the temporal sweep are still running. Completed-case raw inputs, fields,
logs and diagnostics are archived in evidence/of13-study-v1; summary is partial.
Full quality and hypothesis verdicts remain UNCERTAIN.

## Three spatial grids and independent formula checks

64^3 at dt=0.001 completed, giving velocity relative L2 error 0.00491374.
The temporal runs at dt=0.0005 and 0.00025 remain in progress.
Symbolic differentiation at 64 seeded points matches the NumPy reference with
maximum absolute errors below 6e-14. The generated C++ forcing, compiled against
OpenFOAM vector types and evaluated at 48 seeded points with non-unit volumes,
matches within 8e-15. This mock assembly test does not prove the solver's force
sign convention. Raw JSON results and runnable check scripts are preserved.
Added one-sided analytic center bounds for continuous peaks, avoiding a claim
that cell-sampled analytic maxima are the true continuous maxima.

## AMR comparison completed; attribution still open

AMR study-v1 completed all three budgets at t=0.05:

| maxCells | final cells | volume-weighted velocity relative L2 |
|---|---:|---:|
| 4096 | 4096 | 0.0654077 |
| 5000 | 7624 | 0.275639 |
| 100000 | 30416 | 0.280839 |

The budget-only limit is not an exact cell-count ceiling. A source-tree example
labels maxCells approximate; the observed overshoot is not classified as a defect.
The no-refinement control matches the uniform 16^3 result. Increased refinement
in this transient initialization does not reduce the velocity error. Coarse-to-fine
initial-field interpolation and mesh/flux correction remain confounders. Next
control: reuse the refined mesh with the analytic field initialized directly on
that mesh, then solve without remeshing. No upstream defect claim is warranted.

AMR setup corrections were to our adapter: Foundation uses time().name(), mesh
changes need pcorr solver settings, and writeCellVolumes writes Vc. A no-refinement
run need not emit cellLevel; the reader records its initial-grid/no-refinement
inference explicitly rather than pretending a level file existed. The completed
4096 case was reanalyzed, not rerun. Raw artifacts are in evidence/of13-amr-v1.
16 unit tests pass, including nonuniform/constant volume field parsing.

Uniform dt=0.0005 also completed with velocity relative L2 0.00491960; the final
dt=0.00025 run remains active. The nearly unchanged error indicates spatial error
may dominate; final temporal comparison is needed before concluding separation.

## Refined-mesh initialization controls completed

On the same final meshes, initializing the exact field directly and disabling
remeshing gives errors 0.0187805 (7624 cells) and 0.00500089 (30416 cells), compared
with 0.275639 and 0.280839 in the adaptive histories. Cell-center correspondence
was verified. Final mesh geometry alone therefore does not explain the large AMR
errors. Initial coarse-field representation, interpolation and dynamic flux
correction remain the relevant combined confounder; this control does not isolate
those individually. Raw artifacts: evidence/of13-remap-control-v1.

## Uniform space/time sweep completed

All five study-v1 cases reached t=0.05, with outer convergence recorded at every
physical step (50, 50, 50, 100, 200 steps). The final dt=0.00025 velocity error is
0.00492265. On the 64^3 mesh, adjacent temporal field differences normalized by
the finest solution are 2.08819e-5 and 1.48385e-5. Their observed difference order
is only 0.493; the results do not establish asymptotic first-order temporal
convergence or justify Richardson extrapolation. They show small sensitivity
for these three time steps while the total error remains about 0.49%.

At 32^3 the velocity L2 error is below the preregistered 2% threshold, while the
FD2 gradient peak underestimates the continuous maximum by at least 13.12%, using
a one-sided analytic lower bound. This is a concrete mismatch between aggregate
velocity accuracy and the reported local diagnostic. It is not an upstream
solver defect: exact-reference sampling and finite differences are substantial
contributors, and full standard acceptance and uncertainty gates remain open.
Raw fifth-case archive and complete peak bounds are preserved. Reproduce the
temporal comparison with `python3 -m tools.compare_openfoam_time`.

## SU2 adapter build in progress

The first build failed because our recipe disabled downloading MEL without
providing its headers. The corrected recipe explicitly fetches and verifies the
upstream-pinned MEL archive, alongside SU2 and Eigen. This is an experiment setup
error, not an upstream bug. The rebuilt image is not yet certified or executed.
The C++ velocity/forcing helper extracted literally from mms.patch independently
matches the NumPy reference at 64 seeded points (maximum absolute differences
8.33e-17 and 1.11e-16). This check excludes full SU2 assembly and scaling.

## SU2 compiled and periodic pilot executed

Pinned SU2/MMS image built successfully; image identity and build log are saved
under evidence/su2. Two 8^3 periodic pilots ran five updates and exited with code
zero. The 200-inner-iteration pilot stopped each update before reaching the
requested residual threshold; it is retained as setup evidence. Raising the cap
to 1000 yielded convergence in 545, 466, 462, 458 and 453 iterations, with all four
reported log10 residuals below -10. Logged density=1 and viscosity=0.01 match the
reference coefficients, and all three periodic pairs were matched.

A time-indexing question must be resolved before assigning an error: history
reports 0 through 0.004 for five dt=0.001 updates. At the pinned source,
CSinglezoneDriver.cpp:120 passes TimeIter*dt to MMS, while the static first-order
dual-time residual in CFVMFlowSolverBase.inl advances U^n to U^(n+1), from an exact
t=0 initialization. This suggests a source/reference phase mismatch, but the
localized pilot does not isolate it from spatial errors. Next verification:
a spatially uniform, explicitly time-dependent manufactured control, preserving
the main concentration benchmark. This is a candidate, not a reported defect.
