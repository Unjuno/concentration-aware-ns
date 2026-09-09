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

## SU2 time-indexing control reproduced and intervention verified

A spatially uniform control removes spatial discretization from the question:
u=(1+t^2,0,0), p=0 and f=(2t,0,0), initialized at t=0. On a periodic 4^3 mesh,
five/ten/twenty first-order dual-time updates (dt=0.1/0.05/0.025, final physical
update time 0.5) match u_x=1+dt^2*k*(k-1), i.e. source at the previous time.
All four residual criteria are met at every update. A diagnostic image changing
only single-zone SetPhysicalTime to (TimeIter+1)*dt instead matches
u_x=1+dt^2*k*(k+1), the backward-Euler source-at-next-time recurrence. Full
per-step errors and raw archives are saved for both variants. This establishes
the source-time behavior in this configuration; neither recurrence equals the
continuous exact solution at finite dt, so ordinary truncation error is separate.

The current master bc15466602a687d6fb796d5df7a12ce3fde0949a still contains the
same MMS time assignment and source consumer (source inspection, not a fresh
master executable). Searches for MMS, MMS time and physical time found no direct
duplicate; issue 690 concerns adding time-varying boundary conditions. The bug
report template was reviewed. A general correction needs review across time
schemes and restart/multizone paths; the intervention alone does not establish it.

## Analytic interpretation narrowed after self-audit

The uniform control confirms old-time MMS forcing, but both old- and next-time
recurrences are first-order consistent. The evidence does not establish a
fundamentally inconsistent time integrator. An intentional explicit-source
contract remains an alternative explanation. Before upstream submission, the
report must distinguish the observed recurrence from the desired MMS time
contract and avoid extending this result to unrelated production simulations.
The full derivation and limitations are in docs/analytic-self-audit.md. The user
requested analytic priority and skepticism toward simulation-derived conclusions;
GOAL.md revision 4 records that constraint without reducing project scope.

## PhysicsNeMo native residual evaluation executed

Pinned v2.2.1 source was checksum-verified and imported unmodified in an isolated
CPU audit environment. The exact transient 3D localized reference was evaluated
by PhysicsInformer at 96 seeded points. Continuity residual max=4.44e-16 and
momentum residual max=1.91e-15 (float64). Time derivatives were supplied explicitly:
the source auto-differentiates x/y/z and warns that t derivatives are caller
inputs. This is a documented interface constraint, not a discovered defect.

An independent PyTorch differentiation of the scalar potential also matches the
NumPy reference velocity, gradient and forcing below 1e-15. Raw diagnostics,
installation logs and a frozen minimal CPU dependency list are retained. This
proves a working residual-evaluation path only; neural training, spatial/time
sampling studies, local acceptance and the PhysicsNeMo audit conclusion remain
incomplete. The full package's optional features were not installed or tested.

## SU2 localized study-v1 launched

The frozen protocol runs n=16/32/64 at dt=0.001 and n=64 at dt=0.0005/0.00025,
all to updated solution time 0.05. The upstream source-time convention is retained
and disclosed. Each step must meet all four residual thresholds to count as
converged; completion alone does not grant quality acceptance. The reader checks
unique periodic vertex coordinates, reports duplicate-value disagreement and
preserves both output/source time and updated solution time. SU2's vertex phase
differs from OpenFOAM's cell-center phase; peak comparisons must retain that fact.

The reader was exercised on the completed pilot (512 unique points, zero periodic
duplicate mismatch, five converged steps, velocity error 0.0267038). Three targeted
reader tests check arbitrary mesh row ordering, missing points and changed time
conventions. The full unit suite now passes 19 tests. The larger sweep is running;
no full-study outcome has been assigned.

## Acceptance triage strengthened

The original flag/point-error prototype could not represent an uncertainty
interval crossing a tolerance. Version 2 requires reviewed artifact hashes and
error bounds, retains UNCERTAIN when an upper bound is unavailable, and supports
proved failure from a one-sided lower bound. CLI success now requires both
standard and local acceptance. Hashes establish byte identity only, not truth of
a review. No solver report was reclassified as accepted. The 25-test suite covers
threshold overlap, one-sided bounds, modified evidence and root escape as well as
existing geometry/metric checks. SU2 study-v1 remains live in its original process.

## SU2 upstream discussion submitted

Submitted https://github.com/su2code/SU2/discussions/2890 in Q&A after checking
issues and discussions, including related temporal study discussion 1441.
The report contains the uniform analytic recurrence, raw pinned reproducer,
intervention and explicit limitations. It asks whether old-time MMS forcing is
intentional and proposes documentation plus a regression case. It does not claim
a general time-integrator defect. Read-back confirms the posted body matches the
saved report exactly. Source inspection of newer master is distinguished from
executed v8.5.0. No second repository or unsolicited duplicate issue was created.
Maintainer interpretation is pending; the localized SU2 sweep is still running.

## PhysicsNeMo learned-solution pilot completed

A native FullyConnected network (3 layers, width 32, tanh) was trained for 500
Adam updates using native PhysicsInformer residuals. Inputs enforce spatial
periodicity; the ansatz u=u0+t*network enforces the exact initial velocity. No
exact transient velocity labels are used. The training lattice is 16^3 with five
time nodes, and a separate 32^3 lattice evaluates the final velocity at t=0.05.
The final relative velocity L2 error is 0.0551001. This is an integration pilot,
not evidence of convergence or sufficient accuracy; batch loss is not monotonic
and the field is not exactly solenoidal. Checkpoint, evaluation arrays, parameters,
training and console logs, plus hashes are archived in evidence/physicsnemo-pinn-pilot-v1.

The native model imports additional core dependencies beyond the earlier residual
only audit. These were installed without modifying upstream source, and the CPU
dependency freeze was refreshed. A three-resolution/multiple-time-node sampling
study and independent validation residuals remain to be implemented and run.

## PhysicsNeMo sampling matrix launched

Study-v1 freezes five paired-seed runs: spatial lattice n=16/32/64 with five time
nodes, plus n=64 with nine and seventeen time nodes. Each receives 5000 Adam
updates with the same model, initial seed and batch budget. Evaluation uses a
64^3 lattice shifted by phase 0.37, distinct from all training lattices, and native
residual evaluation at independent random coordinates and three off-lattice times.
Time-node spacing is a collocation choice, not a numerical integrator time step.
This fixed-budget study cannot by itself establish optimizer convergence or
seed-independent accuracy. Each completed case archives weights, predictions,
training logs and independent validation results. The shared PDE extraction was
rechecked and leaves the exact-reference residual results unchanged.

## First PINN matrix case and derivative attribution

The n16/nt5, 5000-update case completed with velocity relative L2 0.0199231 on the
independent shifted 64^3 grid. Reloading the checkpoint exactly reproduces every
saved velocity sample. Direct network autograd at those same points gives peak
gradient=20.1206 and vorticity=28.4544, whereas FD2 gives 19.7145 and 27.8801.
The autograd peak errors relative to analytic peaks at those samples are about
0.91%. This separates a postprocessing contribution from network error; it is
not a bound on continuous extrema or a complete quality PASS. Raw case and
checkpoint-linked derivative diagnostics are published. Remaining matrix cases
continue in the original process; the SU2 sweep is also still active.

## Spatial PINN matrix complete; temporal comparisons continue

All three spatial lattices with five time nodes completed. Relative velocity
errors are 0.0199231 (n16), 0.0200489 (n32), and 0.0195663 (n64). This small,
nonmonotonic change at fixed training budget does not establish convergence.
Held-out momentum residual maxima are approximately 0.433–0.460 in this
nondimensional setup, so the velocity error alone does not establish a solved PDE.
Direct checkpoint differentiation supplements FD2 for each completed spatial case.
The comparison tool reads completed archives, not live training logs. Audit.md
was reconciled with current pins, licenses, evidence and SU2's submitted Q&A;
PhysicsNeMo's explicit time-derivative contract is not classified as a defect.

## PhysicsNeMo five-case matrix completed

All five runs completed and native autograd derivative evidence was matched to
archived checkpoint/evaluation hashes. At n64, increasing time nodes from 5 to 9
to 17 yields velocity errors 0.0195663, 0.0185950 and 0.0179996 for this paired
seed and fixed 5000-update budget. This is not a universal convergence claim.
The report includes held-out residuals and finite-sample derivative errors;
continuous peak certification, optimizer and seed uncertainty remain open.

SU2 still runs its unchanged study. A separate preregistered n16, five-step
CFL=100 control is testing iteration cost under the same -10 residual criterion;
no study parameters were silently changed.

## Continuum energy reference derived and checked

Derived the exact mean kinetic energy using separated periodic integrals and
scaled modified Bessel functions. Independent one-dimensional quadrature at
sigma=0.25/0.5/1 agrees within 2.8e-17. This eliminates reference-grid quadrature
from the energy comparison, but does not certify floating-point Bessel errors.
The archived numerical sample means still combine solution and quadrature error.
At OpenFOAM n32, energy error versus the continuum formula is 0.00201044, compared
with the previously established >=13.12% gradient-peak underestimation bound.
This supports separating aggregate and local diagnostics without attributing the
latter entirely to the solver. PINN energy errors are approximately 1.01–1.06%.

## Analytic spectrum reference added

Derived continuum Fourier coefficients using the separable Bessel expansion of
ψ, then û_k=i(k×a)ψ̂_k. Archived FFT shell energies are now compared against this
independent reference rather than only checking their own Parseval identity.
Three selected low-mode coefficients agree with a phase-corrected sampled FFT
within 1.8e-17. This is a numerical check of those modes, not a proof eliminating
aliasing at arbitrary resolution. The truncated-cube energy remainder is stored
as signed floating-point evidence; no certified tail or quality PASS is inferred.

## SU2 CFL control completed

The CFL=100 five-step control completed under the same four -10 residual
thresholds. Total first-five iterations decreased from 9320 at CFL=10 to 5216
at CFL=100 (about 44%). At the first completed update, coordinates match exactly
and maximum velocity difference is 8.25e-10. Later baseline fields were not
written, so later field equality is unverified; fewer iterations is not a measured
wall-time speedup. Raw control and baseline first-update evidence are archived.
The unchanged full study remains active. This is setup optimization evidence,
not an upstream solver defect.

The selected Fourier-coefficient check is now a standalone reproducible command:
`python3 -m tools.check_reference_fourier`. Its output exactly matches the
previous recorded check in the verification environment.

## Real-evidence OpenFOAM gate report

The completed OpenFOAM study now has a readable report and a reproducible v2 gate
input tied to the actual artifacts. The n32 diagnostic disparity is retained,
but space/time and full standard-acceptance flags remain false because the
asymptotic temporal regime and complete uncertainty review are unresolved. The
result is UNCERTAIN in all gate fields; no flags were promoted merely to obtain
REPRODUCED. Aggregate measurements are read from recorded summaries, not inferred
from prior commentary. The report also records why no upstream bug is filed.

## First localized SU2 study case archived

n16 completed all 50 updates with all residual criteria met and zero periodic
duplicate mismatch. Velocity error=0.101648, continuum-reference energy error=
0.120279, sampled FD2 gradient/vorticity peak errors≈0.374/0.376. The exact sampled
reference itself has FD2 gradient-peak error≈0.281. This is a coarse-case accuracy
failure, not a reproduced miss of the full conventional criteria: velocity alone
already fails 2%. The n32 case is active. Interim report and hash-checked raw
archive are published; no causal attribution to the time-contract question is made.
