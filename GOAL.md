# Goal — revision 2, 2026-09-09

## Revision 342 — certify exact continuum peaks for the shared N=4 MMS

Closed the reference-side continuous-extremum gap for the active
Fourier-envelope MMS. A trigonometric reduction followed by exact rational
Bernstein certificates on `[0,1]^2` proves `max |grad u|_F =
sqrt(65)/8*exp(-t)` and `max |curl u| = 9/8*exp(-t)`, both attained at
`(x,y,z)=(pi/(2N),0,0)` for `N=4`. The checker stores all four 9x9 coefficient
tables and source/runtime provenance. Its focused TDD regression passes; a
200,000-point field-evaluator sample is recorded only as a sanity check. This
certifies the analytic reference, not solver extrema. Existing same-grid
acceptance denominators and historical verdicts are unchanged. See
`reports/high-gradient-global-peaks-analytic-certificate-2026-10-04.md` and
`evidence/tests/high-gradient-global-peaks.json`. The live SU2 jobs remain
separate execution gates.

## Revision 341 — reconcile the follow-up note with earlier source audits

A repository-wide cross-check found that the September 15 reduced-profile
preprint and the Constantin–Ignatova–Vicol v2 theorem were already covered in
the physical-bridge audit, October 3 literature review, October 4 shared-
hypothesis review, and source metadata. The October 4 follow-up note therefore
consolidates existing findings; it does not record two newly discovered
results. Updated its status and cross-links so readers can distinguish a
consolidated recap from new evidence. No theorem, simulation, benchmark verdict,
or upstream disposition changed.

## Revision 340 — correct the analytic-forcing source to its current version

Rechecked arXiv's version history: Constantin–Ignatova–Vicol
arXiv:2609.20803 is v2, revised September 29, not v1. The v2 theorem requires
spatial analyticity locally uniformly on cylinders strictly before the
candidate singular time; its analyticity radius may shrink toward that time.
It separately assumes a uniform spatial C2 force bound up to the endpoint.
This keeps the result conditional and distinct from OpenAI's smooth,
non-analytic force. Corrected the dated literature note to link and describe
v2 precisely. No proof verification, solver verdict, or physical inference is
upgraded.

## Revision 339 — add the conditional analytic-forcing regularity follow-up

The literature refresh found Constantin, Ignatova and Vicol's September 17
preprint, arXiv:2609.20803. It proves conditional regularity under anisotropic
Type II angular-mean bounds and axisymmetry on a shrinking core when the force
is spatially analytic. The authors identify the OpenAI construction as
satisfying the profile hypotheses for their argument, but its smooth,
compactly supported force is non-analytic, so the theorem does not contradict
that construction. They explicitly do not claim to have verified OpenAI's
proof; our review has not independently checked or formalized theirs. This
sharpens the mathematical boundary around the constructed forcing, but gives
no molecular or solver-defect result. Recorded in
`reports/recent-openai-ns-followup-2026-10-04.md`; OpenFOAM verdicts and the
two live SU2 runs are unchanged.

## Revision 338 — commit the replay receipt for the six-case OpenFOAM matrix

Re-ran `tools.verify_openfoam_high_gradient_matrix` against the current six
archived Foundation 13 cases. All six archive/input/log checks and standard
gates reproduced; n=16/n=32 fail only the sampled local-quality gate while
n=64/n=128 and both n=64 temporal refinements pass. The predefined fine-grid
blind spot remains `NOT_OBSERVED`. Committed the previously untracked
machine-readable receipt referenced by the already tracked report. The
separate n=128 AMR snapshot remains an exploratory, no-quality-gate result;
its 15 release parts are present with SHA-256 digests. See
`reports/openfoam-high-gradient-matrix-recheck-2026-10-04.md` and
`evidence/tests/openfoam-high-gradient-matrix-2026-10-04-b996015.json`.
Goal remains active.

## Revision 337 — separate established complex-fluid alignment from theorem implications

Added a targeted literature check showing that shear-induced molecular
orientation and shear thinning are real for particular liquid-crystalline and
polymer systems, in experiments and molecular-dynamics studies. Updated the
claim boundary: this keeps the user's material hypothesis open as a separate
constitutive/microscopic research path, while the constant-viscosity
continuum blow-up theorem does not entail that behavior. See the physical
bridge audit and the revised row in `reports/attachment-hypothesis-audit-2026-10-04.md`.

## Revision 336 — audit post-announcement blow-up and physical bridge work

Added a dated source audit of OpenAI's September 2026 forced 3D
Navier–Stokes blow-up construction and a September 15 arXiv preprint that
recasts its leading-order swirl profiles and estimates when liquid/gas
continuum assumptions fail. The proof's diverging continuum velocity does not
derive molecular alignment, particle-position determinism, phase transition,
or viscosity collapse. The physical estimates are exploratory and the
preprint explicitly leaves the finite-viscosity forced evolution and stress
realizability open. No simulation-based claim or upstream report follows.
Details and a bounded next-review list are in
`reports/openai-ns-blowup-physical-bridge-audit-2026-10-04.md`.

## Revision 335 — freeze interpretation rules before SU2 output is visible

Recorded the distinction between solver stopping acceptance, finite-sample
quality, and replay integrity before the active SU2 matrix produced a result.
The exact-field FD2 floor supports treating n=16/n=32 peak-metric failures as
resolution-limited. A possible n=64 standard-PASS/local-FAIL will be an
observed fine-grid quality gap, but the SU2 defect-reproduction rule requires a
second adequate spatial grid at n=128; n=64 time refinements do not substitute.
The live run's inputs and thresholds are unchanged. Rules and reporting limits
are in `reports/su2-shared-high-gradient-interpretation-2026-10-04.md`. The
five-case run remains active and no output has been judged yet.

## Revision 334 — prepare a post-run SU2 archive replay gate

Added a verifier that checks the run protocol, adapter patch, archive hashes,
case metadata, process exit, SU2 success markers, input/output digests, and
then reruns the saved postprocessor on every successful archived case. A fixed
`1e-12` comparison is used only to compare replayed diagnostic values with
their saved copies; it does not alter any solver-quality threshold. A synthetic
archive test passes and the full locked suite passes (430 passed, 4 skipped,
89 subtests). The active GitHub matrix is still running, so this reviewer has
not yet been applied to the real archives. Its stated scope excludes an
independent SU2 solver implementation and continuum-extrema certification.

## Revision 333 — separate SU2 stencil underresolution from solution error

Added a reproducible reference-only audit on the same unique periodic vertex
phase used by SU2. For the exact N=4 field at t=0.05, centered-FD2 peak errors
for gradient/vorticity are 35.9%/33.8% at n=16, 9.86%/9.25% at n=32, and
2.52%/2.36% at n=64. Thus coarse-grid failures of the 5% derivative gates can
come from the diagnostic operator even when sampled velocity is exact; n=64 is
the first tested resolution whose exact-field operator floor is below both
limits. This is a resolution floor, not evidence about SU2's simulated field.
The receipt and test are `evidence/tests/su2-shared-high-gradient-resolution-floor.json`
and `tests/test_su2_shared_high_gradient_resolution.py`. The shared SU2 matrix
is still executing; its build and solver results must be interpreted against
this floor before calling any disagreement reproducible.

## Revision 332 — freeze the SU2 shared-reference matrix

Added the separate five-case SU2 Fourier-envelope protocol, LGPL-preserving
adapter image recipe, periodic-vertex case generation, and analysis that
reports residual completion separately from velocity, energy, sampled
gradient/vorticity peaks, and sampled spectrum gates. The pinned driver source
sets MMS physical time to `TimeIter*dt`; the analyzer now reports the final
source time, printed history time, and completed solution time as separate
values. Four focused tests pass, including an exact-field analysis fixture
whose coarse sampled derivative gate correctly fails. The full local suite
passes (428 passed, 4 skipped, 89 subtests). This is a frozen prospective
matrix; the SU2 image build and five solver cases have not yet run. The marked
push will launch them on the pinned Linux/arm64 workflow, with all build and
case evidence retained as an artifact. The full goal remains active.

## Revision 331 — verify the SU2 shared-MMS formulas on Linux

The new adapter helper compiled with GCC in hosted Python-verification run
37189462449 and matched the independent NumPy high-gradient reference at 257
seeded points (maximum absolute error `2.43e-17` in velocity and `2.78e-17`
in forcing). The run also passed the complete locked Python suite (425 passed,
3 skipped, 89 subtests). This checks the helper's algebra, not the patched SU2
build, solver integration, time-level semantics, or accuracy. The PR's
`exact-control` check and the separate full-horizon SU2 CFL run are still
running. The matched-reference SU2 case matrix is therefore not yet executed.
The full goal remains active.

## Revision 330 — close the SU2 reference-family gap before comparing solvers

An audit of the frozen SU2 source adapter and `protocols/su2-study-v1.json`
confirms that the existing SU2 matrix uses a Gaussian-streamfunction MMS,
whereas the OpenFOAM and added PhysicsNeMo high-gradient matrices use the
Fourier-envelope MMS. The existing runs therefore do not form a three-solver
matched-reference comparison. A separate local candidate patch for pinned
SU2 v8.5.0 and a randomized helper-parity checker are drafted without changing
the historical Gaussian study or the active CFL job. The patch applies in a
dry run against the checksum-verified pinned SU2 source archive. C++ parity
execution is still unverified: the local Apple compiler refuses to run before
the Xcode license is accepted, and Docker's content store currently returns an
I/O error. No license action, daemon restart, solver run, or upstream report
was made. Next gate: compile and compare the adapter helper in an authorized
Linux build environment, then freeze the matched SU2 cases only after the
existing source-time semantics and mesh sampling contract are independently
resolved. The full goal remains active.

## Revision 329 — refresh the three-project upstream disposition

Refreshed OpenFOAM Foundation 13, SU2, PhysicsNeMo and the OpenAI reference
repository through GitHub's live API at 2026-10-04 06:46 UTC. OpenFOAM and SU2
default-branch commits remain at their pinned audit revisions; PhysicsNeMo's
latest source commit matches the previously inspected October 2 head. SU2
issues #2353/#2932 and discussion #2890, PhysicsNeMo issues #2001/#2007 and
PRs #1853/#2008, and OpenFOAM's inspected open issue list add no new overlap.
PhysicsNeMo #2042 is a newly open nonuniform-bin Wasserstein integration
report and is unrelated to the periodic derivative/spectrum paths exercised
here. License files and contribution guidance were checked; OpenAI's reference
repository still disables issues and discussions. No upstream post is
warranted. The scoped API response and still-live SU2 baseline handle are
recorded in `evidence/upstream-refresh/live-status-2026-10-04T0646Z.json`.
PR #4 remains open with `CLEAN` merge state and successful Python and exact
OpenFOAM-control checks. The fresh SU2 baseline remains in progress, so the
full goal remains active.

## Revision 328 — independently replay the fresh six-case Foundation 13 run

Hosted run 37181406146 completed all six smooth forced-periodic cases on one
Linux/arm64 image. An independent archive replay verified all inputs, endpoint
fields, diagnostics, update counts, exits, and the standard stopping gate.
Velocity/pressure spatial observed orders range from about 1.85 to 2.19; the three-step
fixed-grid comparison remains unable to resolve temporal order. A cross-run
comparison found bit-identical saved fields and metrics against the earlier
complete run, but different immutable image IDs and upper rootfs layers despite
an identical 393-package inventory. The image rebuild is therefore not
byte-identical; within each case matrix all six rows shared one image. Detailed
receipts and limits are recorded in
`reports/openfoam-forced-periodic-rerun-2026-10-04.md` and
`evidence/of13-forced-periodic-control-hosted-37181406146/`. The local
kinetic-gradient analysis is also recorded but not yet pushed. The long SU2
matched pair is still in progress; the full goal remains active.

## Revision 327 — define a kinetic gradient-to-collision crossover test

Replayed the published BGK/Chapman–Enskog stress relation to distinguish the
dimensionless strain-over-collision rate from the paper's numerical
wave–particle horizon ratio. The order estimate `||sigma||/p ~
tau_coll*||S||` gives a concrete trigger for testing where a continuum
constitutive closure loses accuracy; it does not imply molecular alignment,
deterministic positions, or viscosity collapse. A preregisterable kinetic
comparison and the observable-separation requirements are in
`reports/kinetic-gradient-crossover-analysis-2026-10-04.md`. This is an
analytical proposal, not a completed kinetic simulation, and leaves the current
CFD benchmark unchanged. The full goal remains active.

## Revision 326 — add a kinetic-scale bridge to the hypothesis audit

An official arXiv query for 2026-09-27 through 2026-10-04 returned 32
Navier–Stokes-keyword records. Four primary-source preprints were relevant to
the particle/continuum and concentration questions: Liu–Xu's exact
wave–particle kinetic decomposition (including its full Boltzmann extension),
Dimarco et al.'s low-Mach kinetic relaxation/AP scheme, and Chiarini's DNS of
an explicitly modified equation separating vorticity amplification from
vortex tilting. Together they suggest a future, separately specified kinetic
comparison and strengthen the need to report gradient extremes, energy
dissipation and geometric organization independently. They do not establish
molecular alignment, deterministic positions, spontaneous blow-up, or a
viscosity-coefficient transition in OpenAI's construction. Evidence, query
response hash, and scope limits are in
`reports/research-refresh-2026-10-04-kinetic-bridge-and-vorticity.md` and
`evidence/upstream-refresh/arxiv-ns-window-2026-10-04.json`. No upstream issue
was warranted. The hosted same-image SU2 pair remains the next numerical
discriminator; its current execution is still in progress. The full goal
remains active.

## Revision 325 — derive an exact singular affine counterexample to conflated physical claims

Derived and symbolically checked an exact unforced affine Navier–Stokes field
whose velocity-gradient scale diverges at a finite time and whose generic
infinitesimal material directions align. The determinant of its deformation
map remains one, an advected isotropic Gaussian keeps its peak density, and
the fixed viscosity coefficient drops out because this particular field has
zero Laplacian. This sharply separates continuum line-direction alignment,
position-density concentration, and constitutive change. The example has
infinite energy and linear spatial growth, so it is explicitly outside the
Clay decaying-data class and is not claimed to reproduce OpenAI's flow. The
derivation and SymPy receipt are in
`reports/singular-affine-alignment-constant-viscosity-2026-10-04.md` and
`evidence/analytic-checks/singular-affine-alignment-2026-10-04.json`.
No upstream report is justified; OpenAI's GitHub repo has issues disabled and
this result identifies no defect. The full benchmark and proof audit remain
open.

Live literature refresh found the public Lei–Ren explanatory record still at
Part I; its abstract defers oscillatory-pulse residual cancellation to a
planned Part II. A bounded exact-title search did not locate a separate Part
II record, which is evidence of non-location only and does not establish that
no draft exists or challenge OpenAI's proof. The independent public-paper
audit still lacks a replay of that final stage. See
`reports/research-refresh-openai-part-II-status-2026-10-04.md`.

## Revision 324 — preserve the canceled SU2 full-horizon successor honestly

The hosted same-image SU2 pair run 37160281461 built and probed its ARM64
successor image and started both cases, but the job reached its 300-minute
limit before the CFL=100 control completed. The CFL=10 baseline reached all
50 updates with process exit zero; 48 met the inner residual criterion, and
sampled velocity/gradient/vorticity errors exceeded their frozen local
thresholds. The partial control cannot be analyzed as a completed run, so the
matched-pair question stays open. Artifacts and the exact evidence boundary
are in `evidence/su2-full-horizon-run-37160281461/` and
`reports/su2-full-horizon-cfl-readiness-2026-10-04.md`. Continue with a
bounded/split execution design; do not infer that cancellation is a solver
failure or call the control successful. The overall research goal remains
active.

## Revision 323 — execute and independently replay the Foundation 13 exact control

The new ARM64 Foundation 13 workflow completed all six v1 cases to t=0.05 in
image `sha256:383b0f958aa9867af6e2db9ec7681141393c9d213cd821c1f68a33f4353f0baf`;
the OpenFOAM `codedFvModel` compiled and ran. Afterward, the repository's
existing 1e-8/12-corrector standard gate passes all six. We downloaded all case
archives and independently rechecked their hashes, exits, exact step sequences,
and numerical diagnostics with `tools.verify_forced_periodic_openfoam_run.py`;
all 6 replay successfully. Spatial velocity and pressure errors show roughly
second-order refinement. At fixed n=32, the time-step changes are too small
relative to spatial error to resolve temporal order, so that part stays
UNCERTAIN. Machine replay evidence and solver archives are under
`evidence/of13-forced-periodic-control-hosted-1cacf3c/`; the run is
[37174784940](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37174784940).
This control still does not test concentration, singularity, molecular
alignment, or a viscosity transition. Continue with a more time-sensitive
control only if it can be isolated without conflating spatial error; full goal
remains open.

## Revision 322 — scope the photon-fluid connection against primary sources

Audited established photon-fluid and radiation-hydrodynamics literature to
test the light-as-fluid hypothesis. Nonlinear optics does support a useful
2D paraxial wave-fluid model, including measured excitation spectra, steepening
and a superfluid-like optical-drag reduction. But its density/velocity come
from optical intensity/phase; effective time is propagation distance;
interactions are mediated by a nonlinear material; diffraction/quantum
pressure and material response limit the ideal hydrodynamic singularity.
Radiation hydrodynamics is a separate photon-distribution/matter-coupling
transport theory whose viscous limit assumes optically thick scattering and
scales above the mean free path. These results suggest an established optical
analogue for threshold-dependent drag, not deterministic molecule alignment or
a material's viscosity changing due to the audited 3D NS solution. This is a
literature-scope correction, not a new finding or upstream defect; evidence and
primary sources are in
`reports/photon-fluid-and-radiation-hydrodynamics-audit-2026-10-04.md`.

## Revision 321 — freeze a real Foundation 13 exact-control run

Added `protocols/of13-forced-periodic-control-v1.json`, a non-overwriting
runner that records per-case commands, raw logs, time-step counts, diagnostics,
and archived case hashes, plus a Linux/arm64 GitHub Actions workflow using the
repository's pinned Foundation package recipe. The six frozen rows are spatial
n=16/32/64 at dt=0.001 and temporal dt=0.002/0.001/0.0005 at n=32, all to t=.05.
The schedule builder checks exact integral step counts (50/50/50 and 25/50/100)
and tests pass. This is a smooth, fixed-spectrum source/solver calibration only;
it makes no prediction about local concentration or particles. The hosted
OpenFOAM experiment has not yet run; its output must be inspected for
completion and convergence before judging the control. Goal remains open.

## Revision 320 — add profile-aware OpenFOAM output analysis

Extended `tools/analyze_openfoam.py` to compare the forced-periodic control
against its own exact velocity and pressure, with pressure error invariant to
a constant gauge offset. A synthetic exact archive initially failed because
the analyzer compared velocity to the Gaussian field; after the fix, velocity
and gauge-adjusted pressure errors are below `1e-15`, and existing OpenFOAM
case/analyzer tests pass. This exercises stored-field parsing and metric
selection only, not a solver run. The solver control still needs fresh
multi-resolution and time-step results before any CFD quality inference; no
concentration or molecular claim follows. The updated report is
`reports/openfoam-forced-periodic-control-integration-2026-10-04.md`.

## Revision 319 — connect the exact control to OpenFOAM case generation

Extended `tools/openfoam_case.py` with a `forced-periodic` profile for the
smooth pressure-bearing exact solution from arXiv:2609.38210v1. Generated
cases contain exact cell-center velocity and pressure initial fields and
analytic time-dependent forcing using the Foundation 13 source sign already
audited for the existing cases. Test-first generation checks compare both
initial fields with the independent NumPy reference; a generated-C++ source
comparison is set to run on hosted Ubuntu. The local macOS compiler test was
skipped because Apple's Xcode license blocks compiler invocation. No Foundation
solver run has used this profile yet, so this changes no CFD verdict; the
control remains unrelated to concentration and physical-particle claims. See
`reports/openfoam-forced-periodic-control-integration-2026-10-04.md`. Goal
remains open.

## Revision 318 — add a separate pressure-bearing periodic reference control

Implemented the exact smooth 3D periodic solution from arXiv:2609.38210v1 as
`tools/forced_periodic_reference.py`, returning velocity, analytic gradient,
vorticity, pressure, pressure gradient and exact forcing. It remains a
separate calibration field: its fixed Fourier profile decays exponentially
and does not test concentration. Test-first fixed values caught a wrong
coordinate derivative before correction; focused tests pass (2), the existing
symbolic residual/work replay matches its stored output, and the full locked
suite passes (402 passed, 1 skipped, 89 subtests). Logs, environment and hashes
are recorded under `evidence/analytic-checks/forced-periodic-reference-implementation-2026-10-04.json`.
No solver has run the new reference yet, so no CFD conclusion changes.
The active SU2 pair and hosted PR CI remain open.

## Revision 317 — distinguish stale closure from PhysicsNeMo resolution

Live API refresh found that feature request #1852 was closed by the stale bot
on October 4, with no technical maintainer response. The overlapping consumer
issue #2001 remains open, while implementation PR #1853 remains an old draft
and is marked unmergeable. The separate odd-width spectrum issue #2007 and
focused fix PR #2008 remain open; #2008 passes focused checks but is two ahead
and fourteen behind main, and no full upstream suite was run. Because existing
issues/PRs already cover these findings, no duplicate issue or status-only
comment was posted. Current status and source fields are saved in the dated
evidence JSON and `reports/physicsnemo-status-refresh-2026-10-04.md`. The
benchmark's even-grid spectral result is unchanged; the full objective remains
open.

## Revision 316 — replay the directional-versus-positional countercheck

Re-ran the alignment-uncertainty, accumulated-strain, and rotational-diffusion
tests under `requirements-verification-locked.txt`: 7 passed. Recomputed the
particle-position probability artifact with SymPy 1.14.0; all 14 symbolic
identity/control checks pass and the output matches the committed evidence
JSON byte-for-byte. This supports only the stated affine Gaussian and
infinitesimal-direction models: direction alignment can rise while a bounded
3D position event becomes less likely, and pointwise-diverging strain need not
have divergent accumulated strain. No molecular law or finite-particle
transfer follows. The separate SU2 full-horizon pair and new PR CI are still
running, so the overall objective remains open.

## Revision 315 — trace the post-announcement force constraint to formal fields

Read the full Constantin–Ignatova–Vicol paper (2609.20803 v2), including its
scope caveat and force-only corollary. Its authors explicitly do not claim to
verify OpenAI's construction; they infer the needed velocity hypotheses from
that manuscript. Conditionally, if the asserted singularity and those bounds
hold, their Corollary 2.3 rules out the force vanishing identically in any
space-time cylinder reaching the singular point, but does not require a
nonzero value exactly at the endpoint. Hash-pinned source inspection of
OpenAI's compact candidate found smoothness, compact spatial support, future
time support and the residual equation; its `force_nonzero_of_no_global_solution`
lemma only gives a nonzero value somewhere at positive time. The stronger
external consequence is a separate regularity-theorem result, not a formal
source defect. Exact hypotheses, source hashes and scope are recorded in
`reports/post-announcement-navier-stokes-literature-2026-10-04.md`. This does
not imply molecular alignment or constitutive change. The benchmark, PR checks,
and long SU2 run remain active.

## Revision 314 — record post-announcement regularity and force-density results

Checked recent primary arXiv work beyond the OpenAI announcement. Constantin,
Ignatova, and Vicol (2609.20803 v2) prove regularity under analytic forcing for
solutions satisfying the construction's anisotropic Type II bounds and exact
axisymmetry in a collapsing core; in the corresponding C2-bounded class, the
force cannot vanish near the singular point or be locally uniformly spatially
analytic. This is compatible with a smooth nonanalytic force and is not a
refutation. Cao, Chi, and Nie (2609.10262 v4) state density of smooth
blowup-producing forces in relative L1_t H^s_x exactly for s<1/2, while
preserving initial velocity. This is a weak-topology density result, not
engineering robustness or physical realizability. Neither result supports
molecular position certainty, particle alignment, or a viscosity transition;
no upstream implementation defect was identified, so no issue was filed. The
source-scoped interpretation and follow-up forcing check are in
`reports/post-announcement-navier-stokes-literature-2026-10-04.md`, with version
metadata in its evidence JSON. The benchmark and active SU2 gates remain open.

## Revision 313 — stream native SU2 progress without weakening log evidence

The full-horizon runner wrote solver output only to an artifact file, leaving
the long GitHub Actions step silent until completion. It now tees combined
stdout/stderr to the same byte-preserving log while flushing decoded progress
to Actions and returns a `CompletedProcess` with the original exit code. A new
test first failed because the streaming helper was absent, then verified that
progress is visible before its child exits, both streams are preserved exactly,
and a nonzero exit remains observable. The locked full suite passes: 400
passed, 1 skipped, 89 subtests. The already-running native pair uses its frozen
older checkout, so this change affects future executions only and supplies no
result for that active pair. Goal remains active.

## Revision 312 — search the Foundation issue tracker for AMR/gradient overlap

Followed the OpenFOAM Foundation README to its separate `bugs.openfoam.org`
tracker and searched targeted terms for `maxCells`, `maxRefinement`, dynamic
refinement, field mapping/history, and gradient evaluation. Search-indexed
historical matches include the region-specific `maxRefinement` design question
(#4107), a refinement-history write issue (#3928), and an old least-squares
gradient report (#141). Their described scopes do not match this benchmark's
approximate whole-level `maxCells` cap, first-map exact-cell-average audit, or
Gauss derivative diagnostic. Direct unauthenticated page fetches returned the
tracker login screen, so current ticket details and exhaustive absence of a
duplicate remain unverified. No new solver defect was found, so no Foundation
issue was filed; the record and retrieval limitation are documented in
`reports/openfoam-foundation-tracker-refresh-2026-10-04.md` and its evidence
JSON. The complete benchmark goal remains active.

## Revision 311 — capture a withdrawn opposite-claim preprint and external kernel replay

The arXiv record for Thomas Ruf, 2609.18808, now marks the September 16–17
unforced Navier–Stokes global-regularity preprint withdrawn; its author says an
error in equation (27) makes the crucial inequality below equation (29) wrong.
The claimed theorem is therefore not usable evidence, and it concerns the
homogeneous unforced equations, so it neither refutes nor validates OpenAI's
smooth-forced construction. Replaying equation (27)'s Hölder step confirms that
the displayed second factor should have exponent 1, not 1/alpha^2; propagating
that gives an exponent about 2.268 in place of the paper's subquadratic 1.89,
so its stated energy absorption does not follow. This matches the author's
withdrawal note; no broader proof audit was attempted. Separately, the Lean Kernel Arena currently records
acceptance of 129,842 declarations exported from OpenAI/NavierStokesAndEuler at
the same latest source commit, f9e8bc5. This is additional proof-term/kernel
checking evidence, not a mathematical review of the derivation or physical
validation. GitHub confirms the OpenAI repository has not moved since Sep 10
and has no issues, discussions, or pull requests enabled. Sources, captured
metadata, exact scope and limitations are in
`reports/research-refresh-withdrawn-global-regularity-and-kernel-replay-2026-10-04.md`
and `evidence/upstream-refresh/withdrawn-ruf-paper-and-lean-arena-2026-10-04.json`.
The hosted SU2 matched-pair workflow remains in progress; the full goal remains
active.

## Revision 310 — connect the new exact-solution audit to routine verification

Added the independently derived periodic forced-NS checker to the Python PR
workflow and its uploaded evidence bundle, and linked the source audit plus
replay command from README. Re-ran it under the locked verification requirements
(SymPy 1.14.0); all divergence, Laplacian, projected-force, PDE-residual and
periodic-work identities are exactly zero. The workflow YAML parses locally.
These are source-algebra and automation checks only, not a solver rerun or a
reproduction of the paper’s concentration simulations. Changes are local while
the previous commit’s hosted checks finish; full goal remains active.

## Revision 309 — cross-check the new preprint’s reproduction artifact

Statically inspected the arXiv v1 ancillary source package and pinned its archive
and file hashes. The paper says concentration.py reproduces Table 2, but its CLI
defaults to Tend=2 although multiple tabulated peak times exceed 2, and it has
no neutral/work-doing selector: step_local is always called with its default
neutral=True. If manually switched to neutral=False, the separate applied_work
helper still subtracts the neutralizing term and returns zero by construction.
This is a narrow artifact reproducibility/interface gap; the shipped neutral
path remains internally consistent. It does not challenge the PDE analysis or
target solvers. The arXiv artifact has no issue tracker and its code license is
unspecified, so no upstream post was made. Static evidence is added to the
source audit report and JSON; no numerical run was used. Full goal remains
active.

## Revision 308 — audit a new exact forced-flow and concentration preprint

Found Thambynayagam, arXiv:2609.38210v1 (submitted Sep 24). Independently
replayed the paper’s smooth 3D periodic exact base solution with SymPy 1.14.0:
divergence, Laplacian eigenfield relation, projected-force divergence, strong
forced-NS residual, and periodic zero-work identities all simplify to zero.
That base field decays with fixed Fourier support, so it is a useful exact
solver/source check but is not itself a concentration experiment. The separate
localized simulations report under-resolution-sensitive peak vorticity and
explicitly do not establish systematic enhancement or singularity; they were
not independently rerun here. This is close prior art: differentiate our
contribution as a predeclared cross-solver/AMR-cap acceptance audit, not the
first local-gradient resolution warning. No upstream defect is demonstrated.
Report, checker, output, source digest, and limits are recorded under
`reports/forced-periodic-ns-new-source-audit-2026-10-04.md`,
`tools/check_forced_periodic_ns_candidate.py`, and evidence files. Full goal
remains active.

## Revision 307 — replay the displayed Part I scale thresholds

Expanded the explicit sufficient lower bounds for `C_*` in Theorem 12.4
against both radius inequalities in (12.6). With `P_* > 0`, `C_* >= 1`, and
finite `A,K` fixed independently of the final `C_*` increase, the tenth-power
and eighth-to-tenth-power implications check algebraically. This supports the
displayed simultaneous-choice step only; it does not prove the cited lemmas,
moment closure, lower-order induction, or Part II cancellation. No solver or
physical-particle claim follows. Derivation and scope are recorded in
`reports/lei-ren-part1-scale-inequality-replay-2026-10-04.md` and its JSON.
Full goal remains active.

## Revision 306 — check whether Part I leaves profile compatibility conditional

Checked Lei–Ren arXiv:2609.35406v2 directly after a secondary search result
characterized its construction as conditional on unresolved simultaneous
compatibility. Part I does list Assumption 12.1, but Section 12.1 says it is
discharged for its concrete pieces; Theorem 12.4 gives an ordered simultaneous
choice (`P_*`, `delta`, `j`, then `Lambda`, then sufficiently large dependent
`C_*`) and its proof verifies all four clauses. Thus “do not grow one parameter
while freezing dependencies” is not equivalent to leaving compatibility open.
This is a source-level correction only: constants and all supporting lemmas,
lower-order induction, and Part II residual cancellation remain unaudited.
No solver defect follows. Details and PDF digest are recorded in
`reports/lei-ren-part1-compatibility-crosscheck-2026-10-04.md` and its evidence.
Full goal remains active.

## Revision 305 — refresh primary project trackers and correct the SU2 thread shape

Targeted GitHub REST/GraphQL responses confirm the audited OpenFOAM Foundation
13 and SU2 heads are unchanged and PhysicsNeMo remains at `b45a5c8`, with the
audited spectrum blob unchanged. OpenFOAM Issue #2 is adjacent but unrelated;
SU2 #2353/#2932 remain open and #2857 closed/unmerged; PhysicsNeMo #2007/#2008
remain open. The SU2 #2890 thread has one maintainer comment and one nested
author reply (created Sep 26, updated Sep 30), no later reply, and no accepted
answer. The existing BDF2 evidence is a reply in that thread, not maintainer
acceptance. GitHub repository metadata says `NOASSERTION` for OpenFOAM and SU2;
their pinned source/package license evidence remains separately recorded.
Full targeted responses and hashes are in
`evidence/upstream-refresh/three-project-live-status-2026-10-04T0129Z.json`.
No duplicate upstream post is warranted; full goal remains active.

## Revision 304 — check for the announced oscillatory-correction companion

Queried the arXiv Atom API at 2026-10-04 01:24:44 UTC for the exact announced
Lei–Ren Part II title and its distinctive subtitle. The exact-title query
returned zero records; the subtitle query found only Part I, arXiv:2609.35406v2.
This bounded metadata check leaves the companion unlocated; it does not prove
absence from other indexes or unpublished sources. The captured scope and
result are in `evidence/upstream-refresh/lei-ren-companion-arxiv-check-2026-10-04.json`.
No conclusion about the OpenAI construction changes; full goal remains active.

## Revision 303 — replay the shared strain–diffusion algebra in the pinned environment

Reran `tools/check_burgers_vortex.py` with the repository's
`requirements-verification.txt` under SymPy 1.14.0. Continuity, radial and
axial momentum, azimuthal momentum, and vorticity residuals are zero for the
stated ansatz under `q'=4 nu-aq`; the smooth-axis swirl limit also matches.
This independently reproduces the continuum algebra but not its imposed
feedback closure, finite-energy suitability, molecular interpretation, or the
OpenAI construction. The full benchmark goal remains active; details are in
the 2026-10-04 research report.

## Revision 302 — replay the analytic-forcing obstruction's source hypotheses

Compared the local pure-swirl and positive axial-on-axis hypotheses used in
Remark 2.6 of arXiv:2609.20803v2 against OpenAI's Theorem 3.1, coordinate
bound (10.3), axis datum (B.1), and localization discussion (10.1). The
fixed off-axis set follows by choosing a small time/axial slab so that
`X=r^2/(2q)>X_ext`; on-axis `u_z=j0*tau^(-A)>0`, while annular corrections
vanish there. This verifies those source statements and their compatibility;
it does not audit the complete correction-series proof or Lean artifact. The
result is a conditional exclusion of spatially analytic forcing, not an
upstream defect. The detailed crosswalk is in the 2026-10-04 research report;
full benchmark goal remains active.

## Revision 301 — verify the new forcing regularity boundary and preserve the live wait

Read the full relevant proof and corollaries of Constantin–Ignatova–Vicol
arXiv:2609.20803v2. Under their profile hypotheses, analytic forcing implies
regularity; their separate pure-swirl/open-set argument also rules out
space-analytic forcing on pre-singular time slabs for the stated OpenAI flow
properties. The authors explicitly do not verify OpenAI's construction, so
this remains a conditional mathematical boundary, not a proof defect. Recast
the shared Burgers-strain calculation with its explicit azimuthal residual in
the report; it remains an infinite-energy ansatz and says nothing about
molecular coordinates. The public GitHub run page independently shows the
frozen SU2 run 37160281461 as `In progress` at 2026-10-04 01:11 UTC; logs are
not exposed there, and it was not restarted. Full goal remains active.

## Revision 300 — audit the shared molecular hypothesis against new results

Re-derived the shared conversation's strain–diffusion vortex equations and
bounded-strain width estimate. Its feedback blow-up branch is an exact
idealized unforced solution family, but imposes a closure and has infinite
whole-space energy because of its linear background; it does not imply
molecular alignment or determine particle positions. Read two new primary
preprints: Constantin–Ignatova–Vicol (arXiv:2609.20803v2) give conditional
regularity under analytic forcing and profile hypotheses while explicitly
leaving the OpenAI construction unverified; Petrillo–Glimm (arXiv:2609.23868)
prove a limit on finite Galerkin computations as evidence for unforced blow-up.
Clay's “apparently been settled” notice is procedural, not technical validation.
Neither preprint yields a verified upstream defect. Details and bounded claim language
are in `reports/research-refresh-2026-10-04-shared-hypothesis-and-new-regularity-results.md`.
The active hosted SU2 pair and PR checks remain separate gates; full goal
remains active.

## Revision 299 — verify the tracked project from a fresh locked export

The fixed local HEAD `e039e4b4098fedda2f53f76a71d3a447e384b5c1` passed
`tools.check_clean_export --locked` in a new macOS arm64 / Python 3.14.5
environment. All 47 report-replay steps, 399 tests (one skip; 89 subtests),
and seven supplemental analytic/review commands passed; 328 tracked
report/test-evidence files were byte-identical before and after. The
path-normalized logs and checksums are in
`evidence/clean-export-2026-10-04-e039e4b/`. This is postprocessing
reproducibility only. At the same check, PR #4's `c0b2b1f` test job passed,
some path filters were still pending, and the hosted native SU2 pair remained
in progress without readable logs. Full goal remains active.

## Revision 298 — complete and preserve the full local verification suite

On macOS arm64 with Python 3.14.5 / uv 0.11.17, ran the entire repository
suite in an ephemeral environment using the locked verification requirements:
399 passed, 1 skipped, 89 subtests passed. The exact command, dependency-file
hash, raw log hash and scope limitation are in
`evidence/tests/full-suite-2026-10-04-c0b2b1f/`. This validates the benchmark
repository at `c0b2b1f`; it is not the SU2 native pair or any upstream
project's own complete test suite. Full goal remains active.

## Revision 297 — record a post-announcement similarity-flow study

Checked OpenAI's announcement and `openai/NavierStokesAndEuler`: these describe
an analytical forced-continuum result with Lean formalization, not a molecular
simulation or ordinary CFD solver. Added a scoped review of Duraiswami's
2026-09-15 arXiv preprint on a reduced similarity-profile problem. Its own
abstract leaves part of the stability calculation unconverged, does not run
the finite-viscosity full evolution, and reports no evidence of practical
reachability. The numerical work was not independently reproduced; no solver
verdict or upstream issue changes. Record: `reports/recent-openai-ns-followup-2026-10-04.md`.
Full goal remains active.

## Revision 296 — check whether PhysicsNeMo head movement touches audited operators

PhysicsNeMo `main` advanced from `83d6a337…` to `b45a5c81…` by two commits.
The compare API lists 22 changed files; none is the odd-width spectrum path,
the periodic grid-gradient implementations, `Gradients`, or `PhysicsInformer`.
The exact tree entries at both revisions are recorded in
`evidence/upstream-refresh/physicsnemo-audited-source-delta-2026-10-04T0001Z.json`
and linked from `reports/physicsnemo-live-status-2026-10-03.md`. This does not
reproduce the framework or expand the historical benchmark pin; the existing
issue/PR disposition remains unchanged. Full goal active.

## Revision 295 — preserve the hosted verification artifact

The independent `tests` job in hosted run 37160281461 completed successfully on
the immutable dispatch source `c9f0c4367aa5c06b4c875f9acd74739de2cef7c7`.
Its artifact rechecked the finite n32/n64/n32-half OpenFOAM position samples
and analytic enclosures; the three analytic JSONs remain byte-identical. The
n64 native floating secant diagnostics differ slightly from the earlier
record, and that difference is preserved rather than rounded away. Artifact
ID/digest, extracted-file SHA256 manifest and scope are under
`evidence/tests/dispatch-tests-37160281461/`. This is not solver output from
the still-running paired SU2 job. The full goal remains active.

## Revision 294 — refresh target and duplicate-reporting status

Captured a read-only live metadata snapshot for all three solver repositories
and the directly overlapping issues/discussions/PRs. OpenFOAM Foundation 13
and SU2 default heads are unchanged; PhysicsNeMo main advanced to
`b45a5c810c741e6b41f8515be24c51121f8fc21f`, while the relevant issue/PR records
remain open and tracked. No duplicate post is justified. The scope and exact
normalized responses are in
`evidence/upstream-refresh/live-status-2026-10-03T2355Z.json`, linked from the
proposal audit. Hosted SU2 successor job 37160281461 remains active without
case output yet; the full goal remains active.

## Revision 293 — test the attached proposal against archived benchmark evidence

The proposal's standard-pass/local-fail hypothesis is observed narrowly on
OpenFOAM n16/n32; the preregistered fine-grid persistence criterion is
`NOT_OBSERVED`. SU2 has no case passing the complete aggregate-accuracy and
all-step-residual conjunction while failing sampled local quality.
PhysicsNeMo stays UNCERTAIN because continuous peaks and a model-specific
threshold are missing. Foundation 13's reproduced maxCells overshoot follows
the inspected approximate whole-level budget behavior and is not a defect
finding. Molecular ordering, phase transition, viscosity collapse, and
deployed-control implications remain unsupported. The proposal-to-evidence
crosswalk and no-post rationale are in
`reports/attachment-hypothesis-audit-2026-10-04.md`. Existing long-horizon
SU2 successor run 37160281461 is still live at its paired-solver step; no
result is inferred from the running job. The full goal remains active.

## Revision 292 — validate and replay the tightened force bound

Envelope-aware upper endpoints are about forty times smaller than the coarse
bound. Input source/archive/parameter checks and five corruption controls pass;
previous coarse expressions are recomputed. A guarded source export with the
output excluded reproduces v2 exactly on the same host. Prepared hosted CI
now recomputes both force bounds and preserves outputs. Its execution remains
pending; full objective and global/physical/proof requirements remain active.
See `reports/su2-force-envelope-upper-2026-10-04.md`.

## Revision 291 — bound corrected MMS force displacement across the domain

Derived conservative Euclidean bounds for the executed SU2 reference's linear
and quadratic force terms, yielding an absolute O(dt) continuous-domain bound.
Three digest-verified archived parameter cases have Arb128 upper endpoints;
corrected point diagnostics fall below the bounds. The estimate is loose and
does not determine solver error, acceptance or physical behavior. Full goal
active; see `reports/su2-force-time-uniform-upper-2026-10-04.md`.

## Revision 290 — correct an independently identified reference-family mistake

The SU2 source-lag auxiliary audit used an unrelated MMS. Corrected source
matches archived sigma/nu and the executed reference; additive v2 results
supersede that quantitative v1 interpretation. Two family/resolution regression
tests pass. Old evidence is retained with explicit report correction. Publish
this scientific correction despite queued old CI, preserving its prior state.
Full goal active; see `reports/su2-source-lag-reference-correction-2026-10-04.md`.

## Revision 289 — verify the body-force restriction analytically

Arb128 proves a synthetic smooth-branch local derivative above one with
opposing body force, while the matched zero-force control is below one.
Independent symbolic differentiation and repeated same-host JSON pass.
This prevents extending the earlier body-force-free contraction to arbitrary
forcing; no native trajectory or physical instability is established.
Current publication CI remains queued, so new commits remain local.
Full goal active; see `reports/particle-body-force-sensitivity-2026-10-04.md`.

## Revision 288 — prepare hosted branch and scalar-transcription checks

Added conditional drag recomputation and g++ -O0/-O2 scalar controls to Python
CI, with failure-preserving artifacts. Local numerical controls and three
checker corruption controls pass. C++/hosted execution remains pending.
Exact-head run 37157306920 at a611973 is queued; publication is held to avoid
cancelling it. These are scalar transcriptions, not native OpenFOAM cloud
verification. Full goal active; see
`reports/solid-particle-drag-ci-integration-2026-10-04.md`.

## Revision 287 — distinguish smooth drag sensitivity, threshold and viscosity input

Pinned solidParticle algebra gives body-force-free branch sensitivities below
one, but an idealized Re=.01 branch jump remains. Arb128, Python negative
controls and twenty exact parameter controls verify the declared synthetic
example; no native cloud execution is claimed. High-Re drag viscosity elasticity
lies between approximately .313 and one while nu remains an input. Independent
symbolic differentiation and metadata-qualified guarded replay pass. Optional
C++ compilation failed on Xcode license state and is preserved. Preceding CI
37156524829 passes 375 tests/rechecks; current new audit is separate. Full goal
active; see `reports/solid-particle-drag-branch-scope-2026-10-04.md`.

## Revision 286 — identify a concrete carrier-interpolation consumer

Three pinned Foundation 13 source files show solidParticleCloud constructing
cellPoint carrier U/nu/rho interpolators and solidParticle using explicit
barycentric interpolation in drag. Tracking uses particle U_, so carrier-field
divergence is not the particle-volume Jacobian rate. The frozen-Dc sensitivity
formula and twenty exact controls pass; own-tools export replay matches JSON.
No cloud execution, general particle error, viscosity inference or violated
contract is claimed. Current publication-head CI 37156115323 is tracked without
restart. Full goal active; see
`reports/cell-point-solid-particle-consumer-2026-10-04.md`.

## Revision 285 — distinguish affine incompressibility from discrete mass balance

All four recorded affine pieces have enclosed nonzero divergence. Trace alone
forces gradient-error lower bounds 52.4054%, 48.2669%, 27.5135% and 47.7117%
relative to reference peaks. Same-host guarded replay matches all certificates.
This is a point-reconstruction constraint, not discrete mass-conservation failure;
no automatic SU2/PhysicsNeMo, particle, proof or physical transfer is made.
Their missing bridges and upstream no-post reasons are recorded. Hosted run
37155563101 separately passes 371 tests, v2 equality and the rational scalar
checker. Full goal remains active. See
`reports/cell-point-affine-divergence-impact-2026-10-04.md`.

## Revision 284 — verify hosted v2 equality and independent scalar normalization

Hosted CI 37155045329 passes 366 tests and all three v2 analytic byte-equality
checks on Linux x86_64. Executed merge and publication-head source/data/dependency
closures match. Environment and cross-host floating native diagnostics are saved.
A standard-library rational checker independently validates conservative dyadic
floors/normalization and rejects four corrupted variants; 371 local tests pass.
Its next hosted check remains separate. The v1 failure is retained; no universal
portability, global continuity/extrema or physical/proof completion is claimed.
Full goal active; see `reports/published-cell-point-dyadic-hosted-2026-10-04.md`.

## Revision 283 — preserve host mismatch and use conservative dyadic v2 receipts

Publication-head CI passes 362 tests but fails v1 analytic byte equality on n32;
computed interval lower bounds differ around 1e-13 while inputs/reference boxes
match. Failure evidence is retained. Additive v2 rounds absolute and normalized
lower bounds down on an exact 32-bit dyadic grid; reported four-decimal percent
claims remain unchanged. Local v2 recheck passes. Locked dependencies and runtime
version receipts improve diagnosis; fresh-host v2 success remains unproved.
No weakened byte-equality gate or original solver-gate change. Full goal active.
See `reports/published-cell-point-dyadic-bounds-2026-10-04.md`.

## Revision 282 — make published matrix evidence independently executable

A single verifier checks published finite native samples/receipts against the
independent source pin and recomputes all three analytic ball error JSONs. The
local command passes; new source-substitution/duplicate controls pass. Hosted CI
now executes and preserves the same recheck after tests. A fresh-host result is
not claimed until exact run/artifact verification. Prior neighborhood geometry
certificates are hash-bound inputs, not reconstructed by this small recheck.
Full goal active; see `reports/published-cell-point-matrix-recheck-2026-10-04.md`.

## Revision 281 — verify larger native queries and uniform local error

All three larger-target read-only jobs succeed on source 560a786f. Independent
checks verify 57 samples, complete twelve-candidate sets, exact rational ball
membership, source/binary/field identities and explicit-overload agreement.
Cross-host floating diagnostic differences are preserved. New Arb128 enclosures
give uniform idealized-ball gradient error lower bounds 86.3198%, 48.8078% and
85.2408%, with direct curl bounds; all three analytic JSONs replay byte-identically.
No global maximum, universal floating search, original gate or physical claim is
upgraded. Full goal active. See `reports/cell-point-matrix-native-uniform-error-2026-10-04.md`.

## Revision 280 — freeze larger-target native position replay

Three SHA-bound protocols replay n32/n64/half-step captured fields read-only,
with nineteen fixed queries each inside the previously enclosed local balls.
Target/hash/schedule and exact rational membership controls reject substitutions.
Fresh hosted jobs must verify native candidate search, node/stock source identity,
explicit-overload agreement and unchanged U/p. Runtime execution/results remain
unproved at launch; no continuum or original quality gate is upgraded. See
`reports/cell-point-matrix-native-query-launch-2026-10-04.md`. Full goal active.

## Revision 279 — enclose local neighborhoods of three larger matrix witnesses

At the n32/n64/half-step selected targets, Arb128 proves a fixed radius-1/4096
ball inside exactly one of twelve captured candidates. Full streams and node
hashes bind the candidates to the earlier derivative witnesses. This extends
idealized local uniqueness beyond n16, without native floating search or global
continuity claims. Same-host guarded selected-export replay and corruption
controls support reproducibility. Native larger-target position replay and the
full objective remain open. See `reports/cell-point-matrix-neighborhood-2026-10-04.md`.

## Revision 278 — complete native spatial/temporal captures and independent local checks

All three frozen hosted capture jobs succeed, completing n16/n32/n64 plus n32
half-step native coverage. Original recipe/input/final field and archive identities
pass. All four selected affine derivative witnesses replay byte for byte; gradient
lower bounds are 95.1187%, 86.3341%, 48.8169% and 85.2550%, respectively.
Disk-backed topology diagnostics pass for all cases; the full suite has 344 tests
passing, one skip and 89 subtests. Complete capture releases and digest receipts
preserve reproducibility. This closes the execution gap recorded in revision 277,
without upgrading local bounds to global maxima, convergence rates, physical laws
or an upstream defect. The full goal remains active. See
`reports/cell-point-capture-derivative-matrix-2026-10-04.md`.

## Revision 277 — verify/publicize n32 capture and screen derivatives in bounded batches

The n32-dt0.001 hosted job succeeds on frozen source 4e60b230. Independent
checks verify original twenty recipe hashes, inputs/final U/p byte identity,
read-only probe invariance, complete raw/mesh members and shared triangles.
All native degeneration/base counts are zero. Complete n32 data are public
with a GitHub digest matching local SHA256; n64/temporal jobs remain pending.

New numerical source 24af332b retains node arrays but screens tetrahedral rows
in batches of 10000. n16 reproduces the prior interval witness exactly; the
n32 selected idealized affine piece has gradient/curl error lower bounds of
86.3341%/9.9634% of analytic global peaks at its centroid. The full 339-test
suite passes (1 skip, 89 subtests); both JSONs replay byte for byte in a guarded
same-host selected export. No whole-program RSS limit is claimed.

This is partial two-case local evidence, not global maxima, convergence rates,
native n32 branch/continuity certification, original-gate upgrades or a defect/
physical result. n64 and half-step execution and independent analysis remain
required. See `reports/cell-point-n32-capture-derivative-2026-10-04.md` and the
n32 capture/bounded-batch evidence. The full objective stays unchanged and active.

## Revision 276 — launch unchanged fine and temporal native captures

Frozen source 4e60b23065811d488fe6890ad59af698a81c35b8 launches hosted run
37147687736 for n32-dt0.001, n64-dt0.001 and n32-dt0.0005, serially on fresh
ARM64 VMs. Together with archived n16, these target three spatial resolutions
and a temporal interpolation comparison. All twenty original recipe hashes
match; the complete locked suite passes 334 tests (1 skip, 85 subtests).
The added collector requires original initial inputs and final U/p to
match before the unchanged read-only probe executes. Four rejection controls
pass. The original numerical recipe, gates and predecessor evidence are preserved.

At the launch observation n32 is active and the other cases are queued;
results remain INCOMPLETE/UNCERTAIN, not capture or quality PASS. Poll the same
live handles before restarting. Later independent capture checks and bounded-
memory local derivative/resolution analysis are still required. No physical,
solver-defect, global-continuity or full-goal conclusion changes. See
`reports/cell-point-fine-capture-launch-2026-10-04.md` and
`evidence/of13-cell-point-capture-matrix-v1/launch.json`.

## Revision 275 — execute native position queries and enclose a unique local region

An isolated ARM64 read-only replay restores the existing public n16 mesh/U/p
without evolution. Nineteen native position queries select the target face
vertices and exactly match the explicit tet overload; no nearest-tet fallback
is logged. Twelve native candidates per query are recorded; nine source files
and two stock libraries match the pin/original binary receipts, and U/p are
unchanged. Native nodal data exactly match the earlier derivative witness.

Separately, Arb128 proves the radius-1/128 ball around the exact centroid is
strictly inside the target candidate and outside all eleven others of cell
5332. All nineteen decoded native points and candidate identities match this
region/list. The 330-test suite passes (1 skip, 85 subtests); guarded selected
export reproduces the analytic JSON byte for byte. Cross-host NumPy secant
reference diagnostics differ by about 1e-16, so both outputs and the byte-
identity failure are retained. The frozen native verifier passes on both hosts.

This closes local idealized overlap and finite native-query evidence gaps;
it does not certify arbitrary floating inputs, global geometry/continuity,
automatic cell location, larger resolutions or whole-domain extrema. Earlier
95.1187%/9.1092% error bounds remain centroid results, not bounds throughout
the ball. Original gates, physical/proof claims and the full goal remain open.
See `reports/cell-point-position-neighborhood-2026-10-04.md` and the native
query/local-neighborhood evidence directories. No new upstream defect is claimed.

## Revision 274 — enclose one actual local affine derivative witness

The n16 runtime capture now yields an Arb96 local witness on tet CSV row 71793
(cell 5332, face 22295). For the idealized real-arithmetic piece of cellPoint's
explicit barycentric overload, its interior-centroid gradient/curl errors are
at least 95.1187% / 9.1092% of the respective analytic reference global peaks.
The local determinant excludes zero; gradient and curl are computed directly
from the captured nodal affine map and the independent analytic derivative.
This requires no exact cell-average interpretation or global chord-to-curl transfer.

Three controls and the full 318-test suite pass (1 skip, 83 subtests); a guarded
Git-directory-free selected export reproduces the witness JSON byte-for-byte.
Floating search selects a witness, not a global optimum. Global partition and
continuity, actual position-query branch/rounding, larger cases and original
gates remain unverified or unchanged. See
`reports/cell-point-local-derivative-2026-10-04.md` and
`evidence/cell-point-local-derivative-v1/`. No new CFD or physical/defect claim
follows. Other solver, proof/physical and full-goal obligations stay open.

## Revision 273 — execute unchanged n16 recipe and capture actual cellPoint data

A fresh isolated ARM64 hosted run completed the original n16 recipe and a
compiled read-only cellPoint probe. All twenty recipe source identities,
original n16 input/final U/p byte identity, disabled-control identity and
read-only probe field hashes pass. Eight installed source files match the pin.
Final and initial polyMesh instances, 20,209 point values, 207,488 tetrahedra
and 48,816 internal-face evaluations are preserved for 16,640 cells.

Centre interpolation differs by at most 5.58e-17; shared-face samples by
3.82e-15. Every shared triangle matches owner/neighbour vertex identities;
native degenerate/invalid-base counts are zero. Floating cell/tet volume sums
agree within 1.06e-14 relative. The independent analyzer and 315-test suite
pass (1 skip, 83 subtests). A full public release bundle matches GitHub's SHA256
receipt; old raw evidence and thresholds are unchanged.

This executes the capture specification for a prospective n16 successor,
not recovery of old meshes or larger-case execution. Full geometric partition,
rounding/continuity certification and exact point-witness transfer remain
unproved. See `reports/openfoam-cell-point-capture-n16-2026-10-04.md` and
`evidence/of13-cell-point-capture-v1-n16/`. No solver defect, physical claim
or original gate upgrade follows. Remaining resolution studies, source/proof,
other solver and full-goal obligations stay open.

## Revision 272 — identify a named cellPoint interpolation and its runtime gap

Eight pinned Foundation 13 source files identify `cellPoint` as tetrahedral
interpolation of cell-centre and shared vertex values. A finite conforming
nondegenerate idealized decomposition yields a Lipschitz point-interpolating
field, so it is a specific candidate for the prior gradient chord bound. The
source's degenerate quarter-weight fallback prevents unconditional transfer.
Exact shared-face/centre affine identities, 125 integer controls and an
independent discontinuous negative control clarify the required hypotheses.

All four original raw archives/member hashes pass verification but contain no
polyMesh members. Actual decomposition, direct cellPoint evaluation, fallback
behavior and binary identity remain unverified. A prospective capture checklist
records the mesh/tet/point-field and runtime evidence needed; it is not an
executed run. The 312-test suite passes (1 skip, 83 subtests); no new CFD,
C++ interpolation run, clean-export replay or solver gate upgrade is claimed.
See `reports/openfoam-cell-point-contract-2026-10-04.md` and
`evidence/of13-cell-point-contract-v1/`. Reconstruction relevance, original
quality, other solver targets, proof/physical obligations and full goal remain open.

## Revision 271 — constrain gradients under native point interpolation

An independent Arb96 chord witness now bounds peak gradient-field error for
any C1 field interpolating the exact decoded native velocity points. No exact
cell-average interpretation is required. At n64 the relative lower bound is
46.1968%; the other three cases give 78.4778%, 80.6201%, 79.4674%. All are
rounded down from exact rational endpoints. The floating nearest-neighbour
search only selects witnesses; it is not a global maximum certificate.

The condition is C1 point interpolation (or a Lipschitz representative), not
H1 alone or an established upstream continuum contract. No pointwise curl
bound follows, and the original acceptance gate remains unchanged. Three
controls and the full 311-test suite pass (1 skip, 83 subtests); a guarded
Git-directory-free selected export reproduces the four-case analysis JSON
byte-for-byte. See `reports/openfoam-amr-point-gradient-bound-2026-10-04.md`
and `evidence/amr-point-gradient-bound-v1/`. No new CFD or upstream defect
is claimed. Reconstruction relevance, original solver quality, other targets,
proof/physical obligations and the full goal remain open.

## Revision 270 — adversarially validate the focused upstream fix verdict

A weakness in our PhysicsNeMo spectrum reproducer's fixed expectation is now
corrected: disappearance of the old failure pattern alone is insufficient.
All even/odd axis and transpose controls plus positive finite spectra must
pass. The freshly fetched current main reproduces existing Issue #2007; the
existing PR #2008 passes every fix control. A deliberately invalid zero-spectrum
function is rejected with exit 1, though the old negative rule would accept it.
Eleven adversarial tests and the complete 308-test suite pass (1 skip, 83 subtests).

Fresh API reads show PhysicsNeMo main advanced to b45a5c81 without changing the
spectrum function; PR #2008 remains open, 2 ahead/14 behind. OpenFOAM and SU2
heads are unchanged; the existing SU2 discussion has no new reply and PR #2857
remains closed/unmerged. No duplicate upstream report is justified. Historical
evidence and all frozen solver verdicts stay separate. See
`reports/upstream-spectrum-fix-controls-2026-10-04.md` and
`evidence/physicsnemo-spectrum-fix-controls-2026-10-04/`.
This repairs a benchmark verification weakness and refreshes disposition; it
does not complete upstream validation, continuous quality, physical/proof
obligations or the full goal.

## Revision 269 — verify archived point-value inputs before transferring mean bounds

All four original AMR mean-quality cases are initialized at cell centres,
confirmed independently by finite Fourier point evaluation. Relative errors
against exact initial cube means are 7.765609%, 1.878300%, 0.465768% at
n16/n32/n64; the n32 half-time-step input is identical. Forcing is evaluated
at centres and volume weighted. Six pinned OpenFOAM source files and primary
documents do not establish the exact-native-average H1 reconstruction guarantee
needed to transfer the previous conditional certificate to the solver.

The certificate remains valid under its stated conditions. This audit distinguishes
input recipe, engineering mean target and continuous reconstruction; it does not
subtract initial errors from final errors or label centre quadrature a bug.
All four archive/member hashes and frozen input source identities are checked;
two new controls and the complete 297-test suite pass (1 skip, 83 subtests).
No new CFD run or clean-export replay is claimed. See
`reports/openfoam-amr-input-representation-2026-10-04.md` and
`evidence/amr-input-representation-v1/`. No new upstream issue is justified.
Reconstruction interpretation, original acceptance, other targets, physical/proof
obligations and the full goal remain open.

## Revision 268 — outward-enclosed nominal-mean continuum error bounds

Arb at 96 bits now encloses the four final-state native-mean necessary-condition
calculations. A Fourier alias-class bound includes the entire continuum H^-1
mass without truncation; rational polynomial envelope bounds replace the
floating reference peak enclosure. Under the exact decoded binary64 means on
the canonical dyadic partition, n64 gradient L2 error is at least 46.6290% and
relative peak-of-gradient-error at least 7.4621%. For divergence-free H1
reconstructions, relative peak-of-curl-error is at least 6.2651%. Quotations are
rounded down from exact rational endpoints. All four final cases exclude the
disclosed 5% target in this specific scope.

The original gate is unchanged: nominal means/canonical geometry are explicit
conditions, not an upstream exact-average contract or a certificate for
unpublished internal values. Earlier floating results and all twelve-state
records remain separate. Three new independent controls and the full 295-test
suite pass; a frozen selected export reproduces all four certificates
byte-for-byte. A standard-library rational scalar checker validates the
normalization chain and rejects four corrupted bound variants, without claiming
to prove the FFT or source interpretation. The initial zero-centred-ball power
failure was corrected before freeze and is recorded.

See `reports/openfoam-amr-arb-mean-certificate-2026-10-04.md` and
`evidence/amr-arb-mean-certificate-v1/`; source is `4222bd31`. No new solver,
upstream defect or physical claim follows. Original acceptance, other targets,
proof/physical obligations and the full goal remain open.

## Revision 267 — separate mean conservation from filtered gradient quality

All twelve archived states now have an explicitly mean-preserving smooth
Fourier reconstruction and exact-native-mean controls, plus a separate
reconstruction-independent H1 gradient lower-bound formula. The latter uses
native mean errors as a P0 dual test field, measured Fourier coefficients and
complete outside mass to bound its H^-1 norm. It imposes no copied subcell
averages on the unknown H1 field. At n64/postSolve, C=63 gives gradient L2 lower
formula 47.1269% and peak-of-error lower formula 5.4030%, conditional on exact
native-mean interpretation; this is not a rounding-certified gate verdict.

The chosen mean-preserving polynomial has actual gradient/curl errors
107.6343% / 97.3415%, versus its exact-native-mean control 3.8968% / 3.2128%.
A smooth shear proves that copying exact coarse means to extra voxels before
reconstruction can have velocity L2 error tending to zero but derivative
relative error tending to pi^2/4. This is an analysis-operator limit, not a
solver nonconvergence theorem. The old filtered polynomial's small errors stay
valid for its separate non-mean-preserving scope.

Seven new analytical controls, complete 292-test local suite and byte-identical
selected-export replay of both analyses pass. Their source pins and the earlier
289-test R-source result remain separate. No new threshold or upstream defect
is introduced. See `reports/openfoam-amr-mean-constraint-gradient-2026-10-04.md`
and the two linked evidence directories. The new conditional bound narrows the
continuous-field interpretation gap; original acceptance, other targets,
proof/physical obligations and the complete goal remain open.

## Revision 266 — measure a named smooth AMR reconstruction

The twelve archived states now have exact finite-polynomial gradient/curl
Parseval diagnostics and analytical peak enclosure formulas on 32^3/64^3
periodic grids. The representation is explicitly w=P_B v, |k_j|<=7; it removes
outside modes and generally changes original cell averages. Final n64 gradient
and curl L2 errors are 0.5023% / 0.4965%; peak-error formulas give
0.3974–0.8353% / 0.4182–0.7699%. Endpoints are floating evaluations without
interval-certified rounding, so no acceptance verdict is upgraded.

The discarded P0 velocity norm is 6.1608%, and original global P0 error stays
6.1795%. Helmholtz diagnostics quantify a 0.0725% longitudinal band correction
at n64; curl is invariant to its removal. This is a representation diagnostic,
not an executed CFD correction. All four map-stage diagnostic pairs are exactly
identical. Four new analytic controls and the full 285-test suite pass; a
selected frozen export reproduces the complete analysis JSON byte-for-byte
under Python-level process/network/Git-open guards. Its initial dependency-file
omission is preserved and excluded. See
`reports/openfoam-amr-band-reconstruction-2026-10-03.md` and
`evidence/amr-band-reconstruction-v1/`. Numerical source is `21754518`.
Original AMR acceptance, other targets, mathematical/physical obligations and
the full goal remain open; no retrospective threshold or upstream claim follows.

## Revision 265 — validate the declared AMR P0 spectrum and its outside mass

Computed continuum Fourier coefficients of the cube-constant velocity in all
12 archived N=3 states. Finest-voxel repetition preserves the same function;
the voxel FFT needs its center phase and sinc window. Selected coefficients
agree with direct cube integrals within 3.01e-15. The independent binomial
reference matches real-space quadrature and the earlier rational Parseval norm.
Finite-cube coefficient mismatch plus the complete outside mass recovers every
archived spatial P0 error within 2.04e-15 in relative L2.

At n64/postSolve, inside-cube coefficient error is 0.4814%, outside-cube norm
is 6.1608% and global P0 error is 6.1795%, relative to the same continuum
reference norm. Every preMap/mapped band array and voxel norm is bit-identical.
This quantifies unchanged spectral content at the parent-value map and the
error omitted by finite-band-only inspection. The outside mass includes all
unresolved integer modes but is not resolved into individual outside shells.

The method is a validated P0 spectral diagnostic, with 281 local tests, one
skip and 83 subtests passing. It adds no retrospective quality threshold and
does not replace the original AMR peak/spectrum quality gate or a smooth
velocity/gradient reconstruction. P0 jumps can themselves produce divergent
derivative-weighted Fourier sums for bounded step fields; this representation
limit implies no physical blow-up, molecular alignment or viscosity change.
Goal remains active. See `reports/openfoam-amr-p0-spectrum-2026-10-03.md` and
`evidence/amr-p0-spectrum-v1/`.

A fresh code export of `e6e3480` completes all twelve states under Python-level
process/network/Git-file guards; all tools modules originate in that export.
Its analysis JSON and twelve coefficient arrays are strictly byte-identical
to the published result. The initial wrong-CWD/relative-path launch mistakes
are preserved and excluded from the accepted guarded validation. No CFD,
proof or entire historical report replay is performed by this scoped test.
`evidence/amr-p0-spectrum-clean-export-e6e3480/` records exact hashes and limits.

## Revision 264 — execute the four-case AMR matrix and qualify the discrepancy

Frozen `3566f890` hosted run `37124421538` completes all four fresh ARM64
cases and native analyses. Every standard gate passes. The n16 disabled
capture control leaves final U/p byte-identical; all eight original module
sources and 167 stock-library payloads match the pinned official package.
Both fine fixed-dt reference operators pass at all captured stages.

Final n32/n64 velocity mean mismatches are 13.8446% / 3.9248%, exceeding the
prospective 2% target. At n64, gradient/curl means 4.0255% / 3.2919% PASS their
5% targets. The common fine-grid discrepancy concerns velocity mean quality;
the errors improve with resolution, so no nonconvergence or upstream contract
violation is established. The original AMR peak/spectrum obligations stay open.

Same-time map snapshots show exact parent-value injection. Analytic P0
orthogonality explains the changed velocity mean error: its lower representation
floor is exchanged for mean mismatch while total continuum P0 velocity error
stays unchanged, with squared-identity residuals near 1e-16. A mean-error jump
alone therefore does not establish newly introduced continuum velocity error.

Cross-platform initial-U byte identity failure is retained. Separate optional
32-epsilon numerical compatibility does not relabel byte identity as PASS or
change any solver quality threshold. Archives, conditional replay records,
source/environment identities and the raw release remain in this single
repository. Overall goal is active; other solver, continuous-field and
proof/physical obligations remain open. See
`reports/openfoam-amr-mean-quality-v1-2026-10-03.md`.

## Revision 263 — freeze and execute prospective AMR mean-quality controls

The new N=3 successor fixes n16/n32/n64 at dt=.001 and n32 at dt=.0005,
common first-map time .002, end .05 and one refinement level. Full-domain
velocity/curl/gradient mean errors have prospective 2%/5%/5% engineering
limits; integrated P0 representation floors remain separate. These new
mean norms do not replace the original N=4 peak/spectrum obligations.

The analytic uniform reference precheck passes for n32/n64; n16 remains
coarse. Actual native reference-operator adequacy must pass on every fine
captured stage before a persistent discrepancy is reportable. Three cell-only
snapshots retain native gradients and an independent real-space MMS control.
An n16 disabled-capture run must leave final U/p byte-identical. The matrix
aggregator rejects missing controls, cases, source/protocol identities or
inadequate reference reconstruction. No actual N=3 solver outcome is claimed
by this preflight record.

All eight pinned module source files and 167 stock library payloads are
checked against the official hash-pinned package. Fresh hosted ARM64 VMs,
bounded solver resources and preserved raw/partial artifacts isolate each
case from the unresponsive local Docker service. Compilation, solver
execution and archive analysis are still required after the harness commit
is frozen. Quality failure alone is not a solver defect or evidence of
molecular alignment, phase transition or viscosity reduction. Goal stays
active. Protocol: `protocols/of13-amr-mean-quality-v1.json`.
Local locked preflight: 271 tests pass, one skip and 80 subtests pass;
workflow shell/YAML and Python syntax/whitespace checks pass. This is
harness validation, not CFD execution. Evidence:
`evidence/amr-mean-quality-preflight-v1/manifest.json`.

## Revision 262 — separate AMR derivative representation and mean errors

Recomputed the n=16/32/64 archived first-map tensors and curls on the same
physical support. Closed-form Fourier cell moments separate integrated P0
error into exact cell-mean mismatch and an unavoidable representation floor.
All 18 total-error comparisons agree with the independent saved quadrature
within 8.33e-16. At n=64 the gradient floor falls 13.8870% to 7.0390% while
mean mismatch rises 1.6132% to 12.1187%; similar totals near 14% obscure these
opposing changes. Tests independently differentiate the real-space envelope,
check nested-cube moments and attack invalid geometry/values.

This is an archived-input analytic diagnostic, with no new solver execution,
AMR quality threshold or upstream defect claim. It bounds the named P0
representation only; the earlier uniform peak threshold is a different norm.
The n=16 original protocol-hash limitation is preserved. See
`reports/openfoam-amr-derivative-projection-2026-10-03.md` and its machine-readable
evidence. Next AMR work needs a prospective representation-aware quality gate
and transfer versus post-step controls. Other solver, proof/physical and
release obligations remain open. Goal remains active.

Validation at frozen source `5bc0691`: hosted tests pass 264 with one skip and
70 subtests. A fresh locked CPython 3.14.5 export passes 47 replay steps,
six follow-up checks and strict comparison of 237 unchanged files. The earlier
3.12 strict metadata/hash failure is preserved with every differing field;
the new AMR artifact matches exactly in both environments. A supplemental
package archive replay in the fresh export also passes, using immutable
input-source Git blobs from the clone, without rerunning CFD. These records
do not certify later publication commits or broaden scientific conclusions.

## Revision 261 — execute the package control and independently replay evidence

Frozen commit `e6a5b1ad` completed hosted ARM64 run `37118442037`: runtime
build, wmake, all three aligned grids and 15 snapshots. The independent
archive replayer verifies106 regular files, frozen inputs/sources and selected
25 source / 3 linked-library payload identities. Hosted and macOS replay verdicts
match; seven derived floating metrics differ by at most 1.083e-15. Both return
PASS for the specified discrete-operator gate, which is not a continuum-error
or whole-benchmark PASS.

The constant-one control has exactly zero complete residual and physical flux
in saved numbers, but native scalar residual is exactly 0.25 / 0.125 / 0.0625,
matching the extra cyclic-source prediction. This is a diagnostic reproduction
with 2024 prior discussion; mechanism novelty/maintainer contract confirmation
are not claimed. Inspected standard solve/convergence paths use separate
statistics; no universal simulation failure is established. Actual arithmetic
flux errors are 6.38855/3.09540/1.52411percent despite normalized PCG residuals
below 1e-12. Harmonic equilibrium matches traction to 4.67e-15 but takes zero PCG
iterations, so perturbed-start convergence is untested.

The e6 Python CI failed three synthetic fixture tests missing the moved recipe
in app/Dockerfile; production data and replay passed. The corrected local
suite passes 260 tests, one skip and 57 subtests; separate raw-data review
found no material evidence or scope issue. Corrected the fixture,
retained the failure distinction and record final tests/CI separately. Full
observations, prior-art/channel limits and replay commands are in
`reports/openfoam-interface-package-operator-2026-10-03.md` and
`evidence/of13-interface-operator-v1/`. No new upstream issue is posted while
prior official-tracker status and API intent remain unresolved. Original AMR,
other solver-quality, proof/physical and release obligations remain open.
Goal is active.

## Revision 260 — preserve failed acquisition and change the download path

Hosted run `37117700448` at frozen commit `85aad783` stopped before utility
compilation/execution: the official package transfer closed with 13,326,066
bytes remaining and curl exited 18. The exact failed build log and hosted
status are retained in `evidence/of13-interface-hosted-failure-37117700448/`.
There is no operator or solver-quality result from that run. Python CI at the
same commit passed 252 tests, one skip and 57 subtests.

Use an additive interface runtime recipe with the same pinned Ubuntu base,
package URL and final SHA256, but bounded resumable package acquisition.
Controls confirm that a partial transfer resumes to the expected hash and an
incorrect payload is rejected after the retry bound. Numerical inputs and
acceptance thresholds are unchanged. The source-only review identifies exact
2024 prior discussion, current 13/14/dev contribution paths and limited tracker
access; mechanism novelty and a universal simulation defect are not claimed.
An archive-only replayer now verifies frozen sources/inputs and independent
matrix/flux analysis without executing archived binaries. Freeze this revised
harness before another hosted execution. Original benchmark/AMR/physical gates
remain open; the goal is active.

## Revision 259 — freeze an auxiliary package operator probe

Prepared a prospective stationary scalar Couette operator probe on aligned
16/32/64 by 2 by 2 Cartesian grids. Its committed protocol separates process
integrity, complete matrix/physical-flux quality and the native scalar residual
prediction. The specified constant field has complete residual and physical
flux zero; source inspection predicts an extra cyclic load in the native
scalar residual. This is a candidate to test, not yet a package reproduction.
The utility, case generator, independent matrix/flux analyzer, runner and
ARM64 hosted workflow are frozen together before production execution.

The exact official Debian package hash matches the runtime recipe. Its 25
relevant supplied source files match source commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90` byte for byte, and three selected
library payload hashes are recorded for comparison with runtime-linked files.
This does not prove how those binaries were compiled. The local containerd
blob read failed even during a fresh additive build; preserved environment
logs classify this as STOP/INCOMPLETE, with no solver quality verdict. Use a
fresh hosted ARM64 VM for the package run and retain its full logs/identity.
The probe is auxiliary to the original smooth 3D concentration and AMR work;
those open gates and all molecular/constitutive bridges remain open.
Goal remains active.

## SU2 control continuation addendum — 2026-10-04

Replayed the completed baseline from raw archived outputs and verified its
diagnostics against the saved receipt. The result remains quality `UNCERTAIN`:
48/50 physical updates meet the inner residual threshold, velocity relative
error is 2.277%, and sampled gradient/vorticity relative errors are about
11.24%. Added a control-only continuation protocol that rechecks the archived
baseline, rebuilds and measures the ARM64 runtime, and stops before SU2 unless
the immutable image receipt exactly matches the completed baseline. Added
separate-run review support so the previously cancelled seven-row control
cannot be relabeled complete or paired. Local locked suite: 424 passed, 2
skipped, 89 subtests passed. Hosted continuation has not yet run; no new
numerical conclusion or goal completion is claimed. AMR staging artifacts
present in the shared checkout were left untouched.

## Revision 258 — clean export of compatible-interface analysis

Exported fixed commit `b0e590e3c1b9b19044748fac7ad06109785f6fe5` from
tracked Git content into a fresh locked CPython 3.14.5 environment on macOS
27.0.1 arm64. All 46 report/evidence replay steps and six follow-up checks
exited zero; all 234 compared tracked report/test-evidence files remained
byte-identical. The fresh test stage passed 233 tests, with one skip and five
subtests. Saved wrapper/test-log hashes and all 46 raw replay log hashes match.
The sanitized result and logs are preserved in
`evidence/clean-export-2026-10-03-success-b0e590e/`. This confirms Python
postprocessing/evidence reproducibility at the named commit and host only;
no CFD solver or Lean proof was rerun and no physical verdict is upgraded.

The PR description also removes its stale whole-repository OPEN claim:
the October 2 pinned-source audit records compiled OpenAI candidate/whole-space
theorem declarations with standard axioms, and their source hashes match the
pinned checkout. The OPEN note is local to the proposition-definition module.
Our actual-profile pressure premise remains a separate unresolved extension
obligation. Next interface work is a frozen package-level operator probe;
the AMR-quality, other solver-quality and physical bridges remain open.
Hosted Python CI is a separate PR check. Goal remains active.

## Revision 257 — impose incompressible interface compatibility before interpretation

Derived the admissible velocity-gradient jump `[A]=b outer n`, with `b dot n=0`
for shared differentiable velocity traces and incompressibility on both sides.
The source-convention normal contraction of the explicit transpose-gradient
correction is therefore zero at the interface. This excludes the earlier
independent-tensor fixed-jump norm growth for that compatible continuum class.
Built an exact piecewise-viscosity planar Couette control: the explicit term
vanishes, while the orthogonal scalar FV arithmetic interface coefficient gives
solved flux errors of 6.39%, 3.10% and 1.52% at 16/32/64 cells; harmonic
half-cell resistance reproduces the exact flux/cell values. Independently
assembled stiffness matrices match the exact chain. This is a conditional
stencil analysis, not an executed OpenFOAM case or a scheme-wide defect.
Ten controls and five new targeted tests pass. Relative metrics explicitly
require nonzero traction. Full published replay passes all 46 steps, including
233 tests, one skip and five subtests. Details are in
`reports/incompressible-interface-stress-compatibility-2026-10-03.md`.
Separately, fixed commit `a444a5f` passes a fresh locked 45-step clean export,
six follow-up checks and 232 unchanged tracked files; that export predates
the compatibility additions. A tracked-only export of the new additions remains
to be checked. Core AMR, solver-quality and proof/physical gaps remain open.
Goal stays active.

## Revision 256 — link interpolation algebra to the pinned correction operator

Captured the relevant parent/change/current Foundation-13 sources at immutable
revisions; all 13 current files match the local tree, and the change's
`linearViscousStress.C` matches the current pin byte for byte. Traced the
explicit correction through product flux versus separately interpolated
coefficient/tensor, field-name scheme selection, face contraction and
owner/neighbour conservative assembly. The simple covariance is established
for the common uncorrected linear kernel; mixed weights, corrections and
multi-donor mappings require additional terms. Exact controls show that signed
global cancellation can coexist with local residual-density growth in a
synthetic unresolved planar layer. A product-constant, independently
prescribed tensor control also exposes a contrast-dependent interpolation
overshoot. Neither control is a compatible manufactured fluid solution or an
upstream defect reproduction. The checker passes ten exact controls and five
targeted tests. Full published replay passes all 45 steps, including 228 tests,
one skip and five subtests. Fresh tracked-only export and hosted checks are
separate validation stages. Source identities, limits and next evidence are in
`reports/openfoam-stress-operator-source-link-2026-10-03.md`. The original
benchmark, AMR-quality and proof/physical bridges remain open. Goal is active.

## Revision 255 — fixed-commit clean export at the viscosity-jump audit head

Exported commit `0526de204d4cab95a432db254c148bdb1773c0bc` from tracked Git
content into a fresh locked CPython 3.14.5 environment on macOS 27.0.1 arm64.
All 44 report-replay steps and six follow-up checks exited zero. The strict
comparison covered 230 tracked report/test-evidence files and found no changes.
The result and sanitized logs are preserved in
`evidence/clean-export-2026-10-03-success-0526de2/`. This is a Python
postprocessing/evidence reproducibility check only. Hosted Python CI passed on
the resulting branch head `e5d78a4b1c9bcd129b75578bf0e443c843c6866e` (run
`37110793834`). No solver, Lean proof, or physical verdict was rerun or
upgraded. Goal remains active.

## Revision 254 — replay the added stress-interpolation analysis

Added the generic same-weight interpolation-covariance checker to the public
report replay and ran the complete replay with the verification environment on
PATH. All 44 steps passed, including the full pytest suite (223 passed, one
skipped, five subtests passed), and the new symbolic identity step passed.
The working-tree replay also refreshed the repository's prior recorded
diagnostics whose platform provenance had advanced to macOS 27.0.1. The
fixed-commit clean export and hosted CI for the next commit remain to be
verified. This algebraic control neither reproduces the upstream VoF case nor
changes the solver or physical verdict. Goal remains active.

## Revision 253 — distinguish the existing viscosity-jump issue from the hypothesis

Repeated the live version/license/issue check across the pinned OpenAI source,
OpenFOAM Foundation 13, SU2 v8.5.0 and NVIDIA PhysicsNeMo. OpenAI remains at
the pinned source with Issues/Discussions disabled. SU2's source-time
Discussion #2890 and Issue #2353 remain the existing records; broad target-time
PR #2857 is closed unmerged. PhysicsNeMo main advanced to `b45a5c8`, but the
odd-width spectrum source is unchanged and its Issue #2007 / PR #2008 remain
the correct reports. No duplicate post was warranted. The live status and
source identities are in
`reports/live-upstream-recheck-2026-10-03-0824Z.md`.

The OpenFOAM GitHub tracker has a directly adjacent existing Issue #2 about
two-phase stress-flux interpolation at viscosity/gradient jumps. For a generic
same-weight face interpolation, symbolically verified
`I(aG)-I(a)I(G)=w(1-w)(a_P-a_N)(G_P-G_N)`: smooth affine fields give an `O(h^2)`
face defect, while finite unresolved jumps can give a defect without an `h`
factor. The derivation does not replay OpenFOAM's full operator or reproduce
the attached case. The frozen smooth, single-phase MMS uses constant `nu`, so
this is a separate interface-discretization benchmark candidate, not evidence
for molecular alignment or physical viscosity loss. No upstream post was
made because the existing issue already tracks that report. See
`reports/openfoam-stress-interpolation-covariance-2026-10-03.md` and the exact
symbolic record in `evidence/tests/openfoam-stress-interpolation-covariance-2026-10-03.json`.
Goal remains active.

## Revision 252 — clean export passes at the refreshed current head

Ran fixed commit `48579a4e70176c1166f33a75b2ef803b2714e30a` from a
tracked-only archive in a fresh locked CPython 3.14.5 environment on macOS
27.0.1 arm64. All 43 report-replay steps and six follow-up checks exited zero;
all 227 compared report/test-evidence files remained byte-identical. GitHub
Actions also passed for this commit. The sanitized result and logs are in
`evidence/clean-export-2026-10-03-success-48579a4/`. This confirms the
postprocessing/evidence path on the recorded host only; it does not rerun
solvers, Lean, or change any scientific verdict. The main benchmark, upstream
audit, and proof-scope gaps remain open.

## Revision 251 — refresh environment provenance after macOS upgrade

A fresh locked clean export of `1160042e53d2db0a372f6a7a60bec9570784bd06`
completed all 43 report-replay steps and six follow-up checks, but its strict
artifact comparison found seven differences. Field-level audit showed only the
platform string changing from macOS 26.6.2 to 27.0.1 in two test-evidence JSON
files; five SU2 gate hashes changed because their referenced diagnostic replay
also recorded the upgraded host. Numeric values and verdicts were unchanged.
Preserved the failed comparison and sanitized logs in
`evidence/clean-export-2026-10-03-current-head-1160042-os-drift/`. Refreshed
the two test records, SU2 diagnostic replay, and dependent SU2 report hashes
for the current host. A new fixed-commit clean export is required; this
metadata refresh does not change any solver or scientific verdict. Goal
remains active.

## Revision 250 — revalidate the published n=128 AMR review artifact

Recomputed the four-resolution nested-cell-average audit in memory and matched
the saved result exactly. Independently hashed all 15 local n=128 review
chunks, the assembled Zstandard file, and the instrumentation library; they
match the tracked manifests. GitHub's current Release API reports all 15
published chunk names, sizes, and digests matching the same parts manifest.
This checks public artifact integrity and postprocessing replay, not the CFD
solver or field-quality verdict; AMR remains UNCERTAIN. No solver was rerun,
and the large local untracked files were preserved. Details are in
`reports/openfoam-amr-nested-cell-average-error-2026-10-03.md` and
`evidence/tests/openfoam-amr-nested-cell-average-live-recheck-2026-10-03.json`.
Goal remains active.

## Revision 249 — add the analytic-forcing regularity boundary to impact scope

Refreshed primary arXiv records and added the 2026-09-29 Constantin, Ignatova,
and Vicol conditional regularity result. Under its analytic-forcing, bounded-C2,
anisotropic-mean, and shrinking-core axisymmetry assumptions, the candidate
point is regular; applied to the cited OpenAI construction properties, this
rules out spatially analytic forcing in the stated local-uniform sense and says
the force cannot vanish throughout any backward cylinder ending at the point.
This gives no pointwise force lower bound and does not contradict smooth
nonanalytic forcing or the claimed construction itself. Also recorded
Petrillo–Glimm's distinct unforced positive-defect target and their limit on
what finite Galerkin computation can certify. No simulations or upstream
reports were made, and benchmark gates are unchanged. Versioned evidence and
scope are in `reports/research-refresh-2026-10-03-forcing-regularity-and-defect-target.md`
and `evidence/upstream-refresh/analytic-literature-2026-10-03.json`. Goal
remains active.

## Revision 248 — confirm the preserved OpenFOAM rerun is no longer present

A fresh read-only check on 2026-10-03 JST found neither recorded host PID nor
solver process; Docker responded, returned no matching container from `ps -a`,
and `inspect` reported no such object. The preserved attempt remains
36/100 converged steps with unknown exit status and no endpoint archive, so it
is still excluded from solver verdicts. The same frozen row had already
completed separately and passed both gates; no retry was launched. The new
timestamped observation is
`evidence/of13-high-gradient-v2/incomplete-rerun-2026-10-02/status-recheck-2026-10-03.json`.
Goal remains active.

## Revision 247 — correct the full-suite reproduction instructions

The README's prior test instructions installed only the minimal NumPy
requirement and invoked unittest discovery, while maintained CI installs
`requirements-verification.txt` and runs pytest. Replaying the old command in
the host environment failed because SymPy and python-flint were absent; the
failure was environmental/setup-related, not a test regression. The README now
matches the CI install/test commands. At commit `2b647bbcc64106c758497d875a29f7850320b3be`,
the CI-equivalent pytest command in the isolated Python 3.14.5 verification
environment passed 223 tests, one skip, and five subtests. The exact result and
log are in `evidence/tests/python-verification-2026-10-03-head-2b647bb.json`
and `evidence/tests/python-suite-2026-10-03-head-2b647bb.log`; hosted CI remains
separately tracked. Goal remains active.

## Revision 246 — inspect the linked force-density formalization

Read-only audit of `mathzhuonichi/blowup_density` found its README claims 27
mapped article results closed in Lean. Its latest observed main commit
`af963994418ae32ff16e00a942bf532410928b09` has a successful GitHub Actions
contracts/architecture run; GitHub reports no declared license, Issues enabled
but no open issues, and Discussions disabled. This supports reproducibility
within its stated mapped scope, not independent validation of the OpenAI
building block or any particle-scale physics. No code was reused and no report
was filed. The evidence snapshot and limits are recorded in
`reports/research-refresh-2026-10-03-openai-ns-profile-exposition.md` and
`evidence/upstream-refresh/blowup-density-2026-10-03.json`. Goal remains active.

## Revision 245 — refresh related OpenAI Navier–Stokes literature

Recorded two current arXiv developments: Lei–Ren's explanatory reconstruction
of the profile and admissible-stress stage (arXiv:2609.35406), and Cao–Chi–Nie's
force-space density result built from the compact forced solution
(arXiv:2609.10262). The latter's stated sharp `L¹_t Hˢ_x` threshold concerns
perturbing the external force, not fixed-force breakdown or molecular
alignment. Neither paper changes the local solver matrix or closes the
extension-level `actualProfile` pressure gap. Details and scope limits are in
`reports/research-refresh-2026-10-03-openai-ns-profile-exposition.md`. Goal
remains active.

## Revision 244 — verify the added model audit from a fixed commit

The fresh locked clean export of `d4cbe01243633b7a0499a65dc923b12dd117e4cc`
passed all 43 report replay steps and six follow-up checks. Its exact comparison
covered 222 tracked files and found no changes. The result manifest and logs
are preserved in `evidence/clean-export-2026-10-03-success-d4cbe01/`. This
supports reproducibility for the recorded macOS/Python 3.14.5 environment; it
does not upgrade solver or molecular claims. The broad benchmark objective
remains active.

## Revision 243 — recheck the archived matrix and add a new internal-state model

Revalidated the current OpenFOAM Foundation 13 six-case archive index rather
than treating the stopped October 2 repeat as live work. The archive verifier
passed all six hashes and recomputed standard/local gate outcomes; the fine
grid blind-spot criterion remains `NOT_OBSERVED`. The partial 36/100-step
rerun is explicitly superseded by the archived 100/100-step row.

Reviewed the newly submitted 2026-10-01 visco-morphoelastic preprint
arXiv:2610.01487 and derived an exact homogeneous-extension solution for its
internal strain tensor. The tensor follows the imposed strain axes while the
Kelvin–Voigt viscous coefficient stays fixed; only the projected total stress
ratio varies through the separate elastic strain stress. This adds a relevant
continuum internal-state model, but proves nothing about molecules, the OpenAI
flow, or a physical viscosity transition. The derivation, checker, and source
limits are recorded in `reports/visco-morphoelastic-internal-state-2026-10-03.md`.
The full locked suite passed (223 passed, one skipped, five subtests). A fresh
fixed-commit clean export remains required after this addition. Goal remains
active.

## Revision 242 — exact tracked-only clean export passes

Ran the committed `5aeefc37` revision in a fresh locked environment using
Python 3.14.5, matching its recorded evidence environment. All 42 report
replay steps and six follow-up checks passed; all 219 tracked files were
byte-identical after replay (`changed_files: []`). This verifies replay
reproducibility for this host/runtime and fixed revision, not solver correctness
or a broader platform guarantee. PR #4 CI also passed and the PR is open with
a clean merge state. The manifest, logs and scope note are preserved under
`evidence/clean-export-2026-10-03-success-5aeefc3/`. The broader benchmark and
upstream audits remain active.

## Revision 241 — identify clean-export metadata drift

The clean export at `c1c7870` replayed all 42 report steps and six follow-up
checks successfully, but seven generated JSON files differed. A field-by-field
comparison against the exact commit showed no numerical or verdict changes:
two evidence records differed only in Python/platform provenance, and five
SU2 report files consequently carried different hashes for those evidence
records. Regenerated the two environment records with the repository host's
Python 3.14.5, the runtime used by the existing spectral/OpenFOAM evidence.
The next fixed-commit clean export must confirm byte-identical artifacts.
Scientific conclusions remain unchanged and the goal remains active.

## Revision 240 — separate scientific replay from environment metadata drift

After the PATH fix, a tracked-only replay at `a6e2ce5` completed all 42 report
steps and six follow-up checks, but the final byte comparison found two
environment-only JSON differences: an absolute interpreter path and a Python
3.12.10 versus 3.14.5/platform-string mismatch. Preserved this unsuccessful
comparison separately. Made the force-scaling record portable by recording
the interpreter implementation instead of a local executable path; retained
version and platform metadata. The next clean export will use the recorded
Python 3.12.10 runtime so exact environment evidence can match. No solver
result or scientific verdict changed. Goal remains active.

## Revision 239 — correct clean-export interpreter resolution

A tracked-only clean export at the then-current `2d3983d` created its locked
venv and installed dependencies, but report replay failed immediately because
the replay runner launched nested `python` via inherited host PATH and selected
a global interpreter without pytest. Preserved the failure, hashes and
classification as a benchmark-tooling/reproducibility defect; no solver or
scientific verdict changes. Wrote the PATH-priority regression first, observed
its expected import failure, fixed the exporter to prepend the fresh venv's
scripts directory for all nested commands, then saw the regression pass and
the full suite pass (222 passed, one skipped, five subtests). A fresh
tracked-only replay using the corrected committed exporter is still required.
The goal remains active.

## Revision 238 — derive the optical-fluid equation boundary

Added the Madelung form of the effective GPE/NLSE to the impact map:
continuity plus compressible potential-flow momentum with nonlinear pressure
and quantum pressure. The conservative equation has no Newtonian viscous
Laplacian; optical loss or drive must be modeled separately. The paraxial
propagation coordinate and transverse plane also differ from a 3D material
flow. This gives a concrete comparison for the user's light-fluid intuition
while leaving any coupling to the audited Navier–Stokes construction
unproved. No new optical computation or experiment is claimed. The single
repository objective remains active.

## Revision 237 — place the light-fluid idea in its established model family

Checked primary and review literature on the light-fluid suggestion. A real
neighboring field maps paraxial propagation in nonlinear optical media to an
effective 2D Gross–Pitaevskii/nonlinear-Schrödinger fluid, including laboratory
measurements of drag suppression. This is a useful connection for future
cross-model work, but the governing equation, dimensional reduction and
material-mediated photon interactions differ from this benchmark's
incompressible Navier–Stokes and rigid-director SDE. Added the evidence and
scope limits to the impact map. No new optical result or transfer theorem is
claimed; any optical extension needs its own derived model and validation.
The benchmark and broader goal remain active.

## Revision 236 — map demonstrated reach and adversarial falsifiers

Read the original hypothesis note as unverified input and cross-checked its
claims against the current solver, OpenAI-source, and director-model records.
Added an impact-scope map separating the observed OpenFOAM standard-PASS /
sampled-local-FAIL cases from the unresolved SU2 and PhysicsNeMo comparisons,
the conditional mathematical construction, and the unsupported molecular,
rheological, industrial-control, and light-as-fluid extrapolations. Added a
red-team checklist for forcing, derivatives, stopping gates, hidden extrema,
AMR budgets and stale/incomplete artifacts, plus a publication boundary that
requires source-pinned evidence and duplicate checks. This is a synthesis and
work plan, not a new solver result, exhaustive impact survey, upstream defect
claim, or legal conclusion. The hosted workflow for the current PR head is
still queued while local verification passed; resolve or document that state.
The repository remains the single canonical location and the benchmark goal
remains active.

## Revision 235 — remove the subcritical equator exception conditionally

Corrected the scalar SDE audit: its pole drifts are `(-2d(s),+2d(s))`, so
the poles are not absorbing for positive rotational diffusivity. In the
coordinate `theta=asin(p_z)`, the noise is additive and the late-time drift
has strictly positive derivative on a fixed band around the equator. For any
fixed future Brownian path, at most one interior state at a deterministic
positive time can then converge to the equator. Finite-time elliptic smoothing
gives that state a nonatomic law, and future-increment independence yields
zero probability of equator convergence. Combined with the existing
APT/strict-Lyapunov classification, this gives almost-sure convergence to a
pole for the prescribed ideal-director SDE, subject to standard
two-dimensional point nonattainment and elliptic-smoothing facts. The SymPy
checker validates algebra only, not those probability results. Updated the
derivation, checker and focused regressions; the prior equator-gap entries
below are historical and superseded by this revision. No molecular ordering,
particle-position certainty, phase transition, viscosity change, or transfer
to the OpenAI flow is established. The broader benchmark goal remains active.

## Revision 234 — explain the nested AMR cell-average error across resolutions

Combined the n=16/32/64/128 same-run first-refinement analyses using the exact
nested-partition identity
`sum_K |K||a_P-u_K|^2 = |P||a_P-u_P|^2 + sum_K |K||u_K-u_P|^2`. In all four
captured events, mapped cell values equal same-run piecewise-constant parent
injection; the exact subcell-average variation term is 40.573%, 20.800%,
10.465%, and 5.240%, with pairwise observed orders 0.964, 0.991, and 0.998.
The parent DOF error falls from 12.598% to 0.220%, while the mapped child DOF
comparison is dominated by the predictable variation revealed by refinement.
Added a scope-limited analytic report, a replayable cross-run source-artifact
audit, and updated upstream disposition: this narrows AMR remap attribution
but leaves AMR quality UNCERTAIN, because stored
OpenFOAM values are not presumed to be exact cell averages and no quality
threshold or continuum estimate exists. No upstream issue or physical claim
is justified. This does not establish AMR convergence. The overall benchmark
goal remains active.

## Revision 228 — classify subcritical full-sphere stochastic limit sets

For the prescribed Jeffery director with `delta<1`, the transformed
rotational diffusivity has finite time integral. The ambient sphere SDE then
has a convergent finite-quadratic-variation martingale perturbation and is an
asymptotic pseudotrajectory of the deterministic Jeffery flow. Its strict
Lyapunov function `V=p_z^2` restricts the sample-path limit set to either the
equator or one pole. This sharpens the previous open result but does not
establish almost-sure polar alignment: avoidance of the unstable equator under
the exact decaying continuous-time noise remains unproved. Added the
framework citations, exact finite-integral/Lyapunov identities and regression
coverage. This remains a conditional ideal-director model; it establishes no
molecular ordering, phase transition, viscosity change, or transfer from the
OpenAI field. Next work should verify an applicable equator-avoidance theorem
or preserve this explicit exception, then continue the wider acceptance
benchmark. The benchmark goal remains active.

## Revision 229 — preserve the continuous-time equator-avoidance gap

Checked the cited nonconvergence result rather than transferring its
conclusion by analogy. Benaïm (1999), Theorem 9.1, is stated for a discrete
Robbins–Monro algorithm with gain/regularity and unstable-direction noise
conditions; it is not directly a theorem for the present state-dependent
continuous-time sphere SDE. The subcritical limit set remains “equator or one
pole,” with almost-sure polar alignment unresolved. Document this applicability
boundary and keep searching for a continuous-time theorem or a direct proof.
The full 42-step report replay and 220-test suite passed on the preceding
revision; PR #4 CI for that code revision is pending. The wider benchmark goal
remains active.

## Revision 230 — pin the inapplicable nonconvergence theorem precisely

Read Benaïm (1999), §9 and Theorem 9.1 (pp. 49–50), rather than relying on a
search-result summary. It treats a discrete Robbins–Monro process and requires
gain, smoothness, and unstable-direction noise conditions. Therefore it
supports neither zero probability of equator convergence nor almost-sure
alignment for this continuous-time sphere SDE. Recorded this exact scope
boundary in the model note; the analytical question remains open. No new
simulation or upstream finding was inferred. PR #4's latest hosted test job
remains queued; local code tests were already green on the preceding code
revision. Goal remains active.

## Revision 231 — reduce the equator question to an exact scalar SDE

Projected the Itô sphere equation onto `x=p_z` and checked the exact marginal
`dx=[(a-2d(s))*x-a*x^3]ds+sqrt(2d(s)*(1-x^2))*dW_s` symbolically. Its linear
equatorial approximation has an unstable Gaussian integrating-factor
amplitude and therefore zero probability of equator convergence for that
linear model. The cubic drift and state-dependent noise prevent transferring
that result to the original SDE. Added a regression test and made this
non-implication explicit. Next analytical step is to prove the nonlinear
terminal-amplitude law has no atom at zero on paths converging to the
equator, or find a theorem with matching hypotheses. Goal remains active.

## Revision 232 — replay the exact equatorial reduction

The new scalar Itô reduction and its decomposition identities pass in the
SymPy checker (13 identities total), with 4/4 focused tests. The locked full
report replay passes 42/42; all recorded log hashes match; the complete suite
reports 221 passed, one skipped, five subtests. These validate the algebra
and repository replay only. The nonlinear equator-avoidance question remains
open, and the wider benchmark goal remains active.

## Revision 233 — check the new analysis on the workflow Python version

Ran the focused orientation checker/tests with Python 3.12.10, matching the
workflow's Python minor version: 4 tests passed and all 13 symbolic identities
passed. Saved the command, environment, lockfile/checker hashes and test-output
hash in `evidence/tests/spherical-orientation-diffusion-py312-2026-10-03.json`.
This is a focused compatibility check, not a full Python 3.12 suite or hosted
CI result. Goal remains active.

## Revision 227 — replace the supercritical tangent-plane claim with a full-sphere result

The earlier rotational-diffusion calculation found divergent variance for
`D_r ~ (1-t)^(-delta)` when `delta>1`, but that calculation was linearized in
the tangent plane and explicitly left global isotropization unresolved. Added
the full `S^2` Jeffery–Smoluchowski equation under the same prescribed,
spatially uniform extensional strain. At `delta=1`, its zero-current invariant
density is proportional to `exp(chi*p_z^2)` with finite width and an explicit
two-pole-cone probability. For `delta>1`, a mean-zero Poincare energy estimate
gives convergence to the uniform sphere density in `L2`; the local variance
blowup therefore marks approximation breakdown, not unbounded physical
orientation variance. The `delta<1` global stochastic convergence theorem
remains unproved. Added an exact SymPy checker, two regression tests, a
full-sphere derivation and a correction to the tangent-plane/literature notes.
The complete Python 3.14.5 report replay passed all 42 steps and the suite
reported 219 passed, one skipped, five subtests. Evidence is in
`docs/full-sphere-rotational-diffusion.md`,
`evidence/tests/spherical-orientation-diffusion-2026-10-03.json`, and
`evidence/report-replay/summary.json`. This prescribed ideal-particle model
does not establish a microscopic diffusion law, particle-position certainty,
phase transition, viscosity change, or a consequence for CFD acceptance. The
benchmark goal remains active.

## Revision 226 — independently recheck the actual-profile pressure witness path

Fetched the current OpenAI/NavierStokesAndEuler main metadata and confirmed
that it remains at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` under
Apache-2.0, with issue tracking disabled. Re-read the pinned source path from
`PreparedOutgoing.PreparedProfile.amplitude_lower`, through nominal and
modulated assembly, into `FinalSlowBase.ProfileData`. The prepared amplitude
bound survives the former path, but is not a field of the latter; the source
then defines `actualProfile` by classical choice from the ordinary
`profileData_nonempty`. Re-ran the pinned Lean provenance checker: the
existential strong-amplitude theorem, selected-profile positivity theorem,
and normalization nonuniformity theorem all pass with only
`propext`, `Classical.choice`, and `Quot.sound`, and no `sorryAx`. This
reconfirms a witness-transfer gap, not a counterexample or proof failure for
the upstream result. No simulation was run. No upstream report was made
because this is a gap in our extension and the upstream issue tracker is
disabled. Reproducibility data is in
`evidence/lean-verification/actual-profile-pressure-recheck-2026-10-03.json`.
The benchmark goal remains active.

## Revision 223 — revalidate the archived OpenFOAM matrix and clarify supersession

Replayed the current six-case Foundation 13 matrix from frozen archives. All
six archive hashes, endpoint fields, step counts, convergence records and
acceptance outputs match the index: standard acceptance passes all six;
sampled local quality fails n=16/32 and passes n=64/n=128 plus both temporal
rows. The preregistered persistent discrepancy remains `NOT_OBSERVED`. Replayed
the n=64 temporal triplet separately: exact velocity error is nearly constant
and slightly increases as dt decreases, so temporal convergence is not
certified. Clarified that the October 2 incomplete half-step repeat is
superseded by the already complete 100-step archived matrix row; the partial
run is retained but excluded from verdicts. The update is in the partial-run
README/status JSON, and the full replay record is
`evidence/tests/openfoam-six-case-and-temporal-replay-2026-10-03.json`.
The hosted Actions run for current PR changes remains queued; local replay is
not a substitute for hosted CI. No solver defect, continuum singularity, or
physical claim follows. Goal remains active.

## Revision 224 — distinguish unbounded strain from infinite accumulated strain

Extended the conditional Jeffery analysis with the rate family
`gamma(t)=gamma0*(1-t)^(-alpha)`. Every `alpha>0` has an unbounded instantaneous
strain, but for `0<alpha<1` its time integral is finite, so a director retains
a strictly positive endpoint angle in the ideal model. An exact example
`gamma=(1/10)/sqrt(1-t)`, `kappa=3/4` gives integrated strain `1/5`; under an
added isotropic initial-director law, only 3.62% enter a fixed 10-degree cone
as `t→1`. The OpenAI-style `1/(1-t)` rate is the nonintegrable critical case
and conditionally aligns an ideal Jeffery director, provided finite-size
spatially uniform strain actually holds. Added exact symbolic replay, two
regression tests, and the published-report replay step. The full 41-step
replay passed with 217 tests, one skipped, and five subtests; see
`evidence/report-replay/summary.json`. This sharpens rather than removes the
finite-particle/molecular bridge: no such uniformity or microscopic model is
established by the continuum pointwise derivative.
Evidence is in `evidence/tests/alignment-integrability-threshold.json` and
`docs/fiber-vortex-literature-audit.md`. Goal remains active.

## Revision 225 — validate the new analysis on the CI Python version

Ran the complete 217-test benchmark suite at commit
`5a2b5e2a2c9a42b68c5416acecbe42611de285c2` under Python 3.12.10, matching the
workflow's Python minor version. Result: 217 passed, one skipped, five
subtests passed. The new accumulated-strain algebra checker and both tests
also pass independently under Python 3.12.10. Environment, dependency
versions, requirements digest, full log and hash are preserved in
`evidence/tests/full-suite-2026-10-03-py31210-after-alignment.json` and `.log`.
The hosted Ubuntu 24.04 job remains independently queued, so the local result
does not substitute for Actions. Goal remains active.

## Revision 222 — quantify the force-density construction's actuator-scale gap

Re-derived the localized force rescaling in Cao–Chi–Nie arXiv:2609.10262v4.
It agrees with the paper's `L^q_t H^s_x` exponent `2/q-3/2-s`; at the same
time, pointwise force amplitude scales as `ε^-3`, one spatial derivative as
`ε^-4`, and one time derivative as `ε^-5`. This makes precise why density in
the weak Sobolev topologies is not evidence of feasibility under uniform
actuator amplitude or rate limits. Added an exact SymPy replay and regression
test, and recorded the conclusion as conditional scaling only: it proves no
bounded-actuator regularity theorem and does not validate the OpenAI proof.
The follow-up literature report is updated. Goal remains active.

## Revision 221 — replay n=128 mapped gradients within bounded memory

Rebuilt the compact n=128 release archive and replayed its Gauss diagnostic.
The mapped-stage JSON and same-parent face audit match the full-run record
exactly. The compact package omits `preMap_faces.csv`, so preMap falls back to
centered periodic differences and differs slightly from the original captured-
face Gauss value; the method and values are explicit in
`compact-gauss-replay-verification.json` and the AMR report. Replaced whole-CSV
decoding and Python row dictionaries with 8,192-row numeric chunks, added a
multi-batch parser regression test, and reran the full suite: 214 passed, one
skipped, five subtests passed on both Python 3.14.5 and the CI-target Python
3.12.10. Commands, environment, lockfile/requirements digests and logs are in
`evidence/tests/gauss-streaming-full-suite-2026-10-03.*` and
`evidence/tests/gauss-streaming-ci-python-full-suite-2026-10-03.*`. The GitHub
Ubuntu job remains independently queued. No solver or physical conclusion
changes.

## Revision 220 — sharpen the finite-observation theorem boundary

Re-read Cao–Chi–Nie v4 directly at Theorem 4.7. It explicitly gives the
whole-space result for a finite family of complete uniform Cartesian grids:
velocity and force cell averages agree in every cell for all `t<T`, while
the altered solution has `limsup ||u(t)||_infinity = infinity` at its terminal
time. Clarified that this is prior published content, and that the torus,
finite-polyhedral-AMR, and finite point/face probe formulation in our report
is a separate conditional adaptation. Replaced potentially ambiguous
"unbounded as t approaches T" wording with the source's limsup statement;
this does not claim monotone divergence or a limit. No physical or solver
conclusion changes. Source review confirms no upstream defect to report from
this analytic result.

## Revision 219 — replay the local nullspace check and stabilize archive logs

Added the existing SymPy cell-local divergence-free null-sequence audit to the
published report-replay sequence. The full 39-step replay passed on Python
3.14.5: 213 passed, one skipped, five subtests passed; each recorded step log
matches its SHA-256. The replay scope explicitly excludes the generalized
finite-AMR proof adaptation, the cited blowup packet, solver reruns, and any
scientific verdict upgrade. Stabilized split-AMR archive replay by suppressing
zstd's successful temporary-path message while preserving its stderr on
failure; a focused regression test covers that contract. The archived AMR
volume-integrated numerical result is unchanged. Evidence is in
`evidence/report-replay/summary.json`, `tests.log`, and
`openfoam_amr_volume_integrated.log`.

## Revision 218 — exercise the CI Python version locally

Ran the full benchmark suite on local macOS arm64 with Python 3.12.10, matching
the Python minor version specified by GitHub Actions. Result: 212 passed, one
skipped, five subtests passed in 103.82 s. The command, resolved dependency
versions, requirements digest, raw log and SHA-256 are recorded in
`evidence/tests/full-suite-2026-10-03-py31210.json` and `.log`. This increases
confidence in Python-version compatibility but does not substitute for the
queued Ubuntu 24.04 workflow run and does not validate upstream solvers.

## Revision 217 — distinguish a new explanatory preprint from proof verification

Checked Lei–Ren, arXiv:2609.35406v2 (submitted Sep 28, revised Sep 29, 2026).
Its authors describe an expository reconstruction of the OpenAI profile
construction and state that residual correction by oscillatory pulses is for a
companion Part II. Recorded it as explanatory literature only: it is not an
independent verification of the full theorem, and this audit makes no claim
about the planned companion's status. The finite-mesh report also corrects its
v4 theorem numbering and records the torus/AMR extension as our conditional
proof adaptation, not a source theorem. No CFD, microscopic, or constitutive
conclusion changes.

## Revision 216 — formally rule out a uniform amplitude floor from the C-quantifier

Added and Lean-checked `no_uniform_lower_bound_over_normalizations`: for any
fixed phase and finite threshold, `realAmplitude=exp(Λ*phase)/C` has no
positive lower bound uniform over all larger `C`. The theorem has only
`[propext, Classical.choice, Quot.sound]` and no `sorryAx`. This confirms the
all-larger-normalization interface alone cannot supply the root amplitude
floor needed by the limiting route; it does not describe the single finite C
stored by `actualProfile` or imply a pressure-sign failure. Evidence is in
`evidence/lean-verification/actual-profile-amplitude-normalization-2026-10-03.json`.

## Revision 215 — trace the selected normalization threshold

Inspected the final witness path through `preparedWitness_exists` and
`exists_ordered_matching_threshold`. Its `C0` is a max of the analytic
entrance normalization and an `eventually_atTop` threshold for later
prefix/separation controls. The interface supplies lower bounds and an
all-larger-`C` guarantee, but no quantitative upper bound for `C0(Λ)`.
Since amplitude is `exp(Λ*realPhase)/C`, a scale-limit proof cannot presently
compare the root amplitude to coefficient errors. This is a missing rate in
the proof interface, not evidence the chosen C is too large or the pressure
claim false. Recorded in the actualProfile audit.

## Revision 214 — identify the missing root-scale coefficient asymptotics

The pinned source already connects its reference axial derivative exactly to
the pressure moment `Z` and bounds the actual `ns` error by `O(1/Λ)`. At
`chi=0`, the remaining root cone variables reduce to
`q=-8 φ_Y/φ` and `r²=(2/Λ)n²/(a²φ²)`. The current error bounds give only
`φ_Y=O(1/Λ)` and, if `Z=0`, `n=O(1/Λ)`; the normalization gives no rootwise
lower bound on amplitude `a`. Thus `Λr²` may not have a finite limit under
the recorded assumptions. The next analytic task is the coupled first-order
fixed-point expansion and amplitude asymptotic. No root-pressure conclusion
is added; source identities and exact relations are recorded in the audit.

## Revision 213 — make the entrance-cone asymptotic obligation explicit

Rewrote the retained cone margin using `q=p1>0`, `r=p2` as the exact
inequality `q^2+r^2>(9/4)q`. At the zero-`chi` root, coefficient convergence
alone makes `q→0` and the unscaled inequality degenerates. A pressure proof
now has a sharper target: establish joint first-order bounds for `Λq` and
`Λr²` over the allowed normalization and connect those limits to `Z`. This
algebraic reformulation does not assert that such limits exist or imply a
pressure sign. See the amended actualProfile audit; the full benchmark goal
remains active.

## Revision 212 — correct the all-scale pressure-limit diagnosis

Corrected the October 3 retained-entrance audit: the coefficient witnesses do
converge to one fixed reference pair because every error is `O(1/Λ)`, even
though the existence quantifier selects profiles separately at each scale.
The direct cone limit remains singular at the zero-`chi` root (`p1` tends to
zero and `coneSize = p1 + p2^2/p1`), while `p2` also contains a scale-dependent
angular-amplitude denominator. Thus witness selection alone neither blocks
nor proves the pressure moment; a joint-rate estimate or nonsingular reformulation
is needed. This is a proof-route correction, not evidence against `actualProfile`.
Source details and qualifications are recorded in
`reports/actual-profile-pressure-provenance-2026-10-01.md`; no amplitude,
solver-quality, or physical conclusion changes.

## Revision 211 — refresh target-project reporting dispositions

Rechecked live GitHub state for PhysicsNeMo, SU2, and the OpenAI source. The
PhysicsNeMo odd-width spectrum issue remains open with its fix PR unmerged and
the affected main blob unchanged; SU2 v8.5.0 remains pinned and its source-time
discussion is closed without a marked answer; OpenAI's repository remains
Apache-2.0 with issues disabled. No duplicate or unsupported upstream report
was warranted. API responses and bounded disposition are in
`evidence/upstream-refresh/upstream-status-2026-10-03.json` and
`reports/upstream-status-2026-10-03.md`. This does not close the wider solver
audit, quality uncertainty, or actualProfile pressure-proof gap.

## Revision 210 — add current forcing-structure and finite-grid literature

Audited the primary arXiv texts for Constantin–Ignatova–Vicol (2609.20803v2)
and Cao–Chi–Nie (2609.10262v4). The first result is conditional on analytic
forcing, a uniform preterminal spatial C2 bound, anisotropic angular-mean
bounds, and exact axisymmetry on a positive-radius core; it does not cover
arbitrary smooth forcing. The second gives topology-dependent force-density
thresholds and, for a fixed finite set of whole-space grids, a construction
that matches velocity and force cell averages despite terminal blow-up. It
does not assert failure of refinement convergence for one fixed smooth case,
or indistinguishability of local-gradient/vorticity diagnostics. These
preprints have not been independently verified and establish no solver defect
or material-scale implication. Recorded in the dated report and completion
audit; full Python suite passed (212 passed, 1 skipped, 5 subtests), and PR #4
CI passed at head `02eefa4`. The actualProfile pressure-threshold gap and other
completion requirements remain open.

## Revision 209 — make clean test environments actually runnable

An isolated review of PR #6's exact head exposed a reproducibility gap: a
fresh venv installed from its advertised verification lock lacked `pytest`,
so the documented test command failed to start. Added and pinned `pytest` and
its transitive dependencies on PR #6 (commit `7088dcf`); a newly created
Python 3.14.5 environment then passed all 65 tests and five subtests, and all
10 archived cases matched their manifest digests and required members. The
current PR #4 branch already declared pytest but omitted those transitive
pins, so its verification lock was aligned. This is a benchmark-tooling
reproducibility correction, not a solver or physical finding. Goal remains
active.

## Revision 208 — recover the sharp one-third integral bound

An independent re-derivation corrected Revision 207's over-conservative
coefficient change. Although `1/(C-1)` alone can exceed `1/3`, the exact
integral is `I/tau0 = integral_Q^1 s^(-C) ds`; for `C<4` and `Q<=s<=1`, its
integrand is bounded by `s^(-4)`. Equivalently, with `b=C-1` and
`L=-log(Q)`, compare `integral_0^L exp(b*s) ds` to its `b=3` case. This
proves `I <= tau0/3*(Q^(-3)-1)`, so the original Q^43 tube and angle
prefactors with coefficient `1/3` are valid. Updated the derivation, symbolic
checker, regression test, and JSON evidence. Targeted tests pass; full-suite
replay and PR CI remain to be checked. This repairs a coefficient argument;
the result remains conditional on continuum tube/Hessian envelopes and the
classical packet comparison, not molecular alignment. Goal remains active.

## Revision 207 — tighten the finite-packet Q^43 prefactors

Rechecked the selected source interval `C in [7999999/2000000, 4)` and
replaced the direct-integral coefficient `1/3` with the uniformly justified
`1/2` bound, since `C-1>2`; updated the tube and angle prefactors while
preserving the conditional Q^43 exponent. Added symbolic regression controls
and regenerated the machine-readable artifact. Full Python suite: 212 passed,
1 skipped, 5 subtests; targeted symbolic checker and evidence-link audit pass.
Committed as `8b4589d` to PR #4; CI was queued at the last check. The packet
law remains conditional on the stated tube/Hessian envelopes and continuum
ODE comparison; it does not imply molecular ordering or fixed-size particle
alignment. Goal remains active.

## Revision 202 — separate tracer occupancy, trajectories, and orientation

Replayed the shrinking-core enclosure in a fresh pinned-dependency venv and
passed its regression test (1/1); recompiled the abstract Lean measure lemma,
which reports only `propext`, `Classical.choice`, and `Quot.sound`. Clarified
that bounded-density passive-tracer occupancy of the shrinking Eulerian core,
selected individual trajectories, and finite-particle/molecular orientation
are three distinct observables requiring different assumptions. These checks
do not validate the OpenAI construction itself or establish microscopic
ordering. The repository's tracked goal remains active and incomplete.

## Revision 203 — conditional finite-director probability and diffusion cutoff

Reconciled the user hypothesis with the existing Jeffery-director and reduced
rotational-diffusion analyses. Under an added isotropic initial director law,
spatially uniform axisymmetric strain `gamma=C/[2(1-t)]`, and a prolate Jeffery
particle, the ideal orientation probability inside any fixed positive-angle
cone tends to one with exponent `3*kappa*C/2`; this is not a probability law
derived by Navier–Stokes. In the tangent-plane stochastic model, if rotational
diffusion scales as `D_r~(1-t)^(-delta)`, variance vanishes for `delta<1`, has
a nonzero limit at `delta=1`, and leaves the small-angle regime for `delta>1`.
Recorded the initial-law and sphere (`kappa=0`) qualifications in
`docs/fiber-vortex-literature-audit.md`. No molecular conclusion follows;
finite-size field uniformity, material-specific diffusion, interactions,
stress closure, and physical cutoff remain open.

## Revision 204 — replay current tracked head and query Foundation tracker

Exported tracked commit `28aa3c2de78264d243598aaf9064918f7e3a8d1b` to a
fresh directory and locked venv on the recorded macOS/Python 3.14.5 host.
All 38 published-report replay steps and seven postprocessing checks exited
successfully; 196 report/test-evidence files were byte-identical. The result
was initially in ignored `work/`, then promoted as Revision 206 to tracked
evidence. This covers tracked Python
postprocessing, not solver builds/runs, training or Lean execution. A bounded
search of OpenFOAM's separate Foundation bug tracker found only adjacent
snappyHexMesh and maxGlobalCells items, not a match for the exploratory AMR
quality observation; tracker pages partly rejected direct fetches, so this is
not an exhaustive duplicate audit and no issue was posted. Goal remains active.

## Revision 205 — derive the photon-fluid model boundary

Added the Madelung reduction of the common dimensionless paraxial cubic NLSE
to the exploratory audit. It yields variable-density continuity plus
compressible inviscid Euler with a quantum-pressure/dispersive term; the
velocity is phase-irrotational away from defects. Therefore the established
photon-fluid analogy is useful for its own optical-drag and wave-concentration
questions, but does not inherit incompressible Navier–Stokes volume
preservation, viscosity, or the OpenAI theorem. This analytic model check is
anchored to the primary Carusotto–Ciuti review and Michel et al. experiment;
it is a derivation from the stated equation, not a simulation or independent
optical experiment. A separate optical benchmark remains only a candidate
until a precise platform/equation/parameter set is selected.

## Revision 206 — publish the current-head replay bundle

Promoted the successful clean export of commit `28aa3c2` from ignored `work/`
into `evidence/clean-export-2026-10-02-current-head-28aa3c2/`, including
sanitized logs, package/command/result manifest, hash of the generated
tracked-tree archive, and reproduction instructions. Updated the completion
audit to state exactly what this proves: 38 replay steps, seven extra checks,
196 byte-identical report/evidence files on one recorded host. It does not
include the archive itself, full pytest, solver execution, training, Lean, or
scientific quality certification. Goal remains active.

## Revision 201 — refresh targeted upstream states and odd-width reproduction

Re-read the live records for the four audited projects. PhysicsNeMo `main`
advanced to `83d6a337`, while the affected power-spectrum file blob stayed
unchanged and the 33x33 asymmetry reproduced again; issue #2007 remains open
and fix PR #2008 remains behind main. Posted the source hash, reproduction
result, even-grid non-impact, and limitation to the existing issue. SU2
Discussion #2890 is closed/resolved with no chosen answer; adjacent issues
#2353/#2932 remain open, so no duplicate was filed. OpenFOAM's AMR result
still does not establish a defect; the OpenAI Lean repository has no issue
route. The bounded statuses and dispositions are in
`reports/upstream-status-2026-10-02.md` and
`evidence/upstream-refresh/upstream-status-2026-10-02.json`. Goal remains
active.

## Revision 200 — bound tracer occupancy of the shrinking Eulerian core

Combined the pinned OpenAI paper's fixed-similarity-coordinate core definition
with the existing preterminal incompressible-flow measure bound. An explicit
enclosing-cylinder calculation gives `vol(C_tau) <= 4*pi*X_c*eta_c*(1-eta_c^2)^(-(3/2-h))*tau^(3/2-h)`. Since `0<h<0.01`, any passive-tracer law with a fixed bounded initial density has core-occupancy probability `O(tau^(3/2-h)) -> 0`. A SymPy check validates the coordinate algebra and exponent range; the measure-domination lemma is already Lean-checked. This does not track a point-mass trajectory, finite particle, molecule, or orientation law. It sharpens the distinction between shrinking Eulerian-core occupancy and infinitesimal tangent-direction alignment; no physical or software defect claim follows. See `docs/incompressible-position-uncertainty.md` and `evidence/tests/shrinking-core-mass-bound.json`. Goal remains active.

## Revision 199 — assess the archived maximum-refinement endpoint

Analyzed the archived cap100000 endpoint at `t=0.05`, validating its 101,760
cell fields and level counts (2,176/3,328/96,256 for levels 0/1/2). Integrating
the saved cellwise-constant OpenFOAM `grad(U)` tensor against the analytic MMS
on the common interior gives 130.3984% gradient and 208.8220% curl relative
L2 error; order-6/order-8 quadrature agrees to `4.44e-16`. This distinct run
history is not appended to the first-map resolution trend. The metric does not
validate the tensor construction or continuous velocity field, and no
preregistered quality threshold exists; verdict remains `UNCERTAIN`, with no
solver-defect or physical-singularity conclusion. Reproducer and raw archive
hash are recorded in `tools/analyze_amr_cap100000_integrated.py` and
`evidence/tests/amr-cap100000-integrated-endpoint-2026-10-02.json`.

## Revision 198 — replay the AMR cell-integrated derivative audit

## Revision 198 — replay the AMR cell-integrated derivative audit

Re-ran `tools.compare_amr_resolution_volume_integrated` from its recorded
Foundation 13 archives and matched the tracked JSON byte-for-byte, including
all three spatial levels and both mapped derivative operators. The targeted
AMR quadrature/geometry tests passed 5/5. Mapped Gauss gradient/curl errors on
the common physical support are 54.25%/59.72% (n=16), 27.86%/31.26%
(n=32), and 14.01%/15.85% (n=64). These are errors of the named cellwise-
constant reconstructions against the analytic MMS, not of a uniquely defined
continuous solver field. The old runs remain exploratory and cannot be assigned
a preregistered AMR quality verdict; that status stays UNCERTAIN. The rerun
hash/environment/test record is
`evidence/tests/amr-volume-integrated-rerun-2026-10-02.json`. Goal remains
active.

## Revision 197 — remove imported swirl amplitude and parameterize phase

This revision supersedes Revision 196's illustrative coefficient and cutoff
numbers. The external preprint's final 32-parameter reduced-profile match
reports `F_0(0)=0.336`; an earlier retained five-parameter attempt reports
0.262 with matching residual 0.437. Neither is the coefficient of
`FinalSlowBase.actualProfile`. The preprint's “fraction of a revolution per
decade” concerns particle motion and explicitly disclaims material-line
winding; the tangent-frame phase here is a different observable. Removed the
imported coefficient/cutoff table and replaced it with turns per unit
`K=f_* d_*^(1+h) tau_0^(-h)` across the `h=0` limit and values
`h={.005,.0099}` within the target range, plus conditional one-turn
thresholds. SymPy identity, sensitivity test, and JSON
artifact were regenerated. Lean evidence is current-source matched for the
axis deformation ODE/uniqueness, but does not formalize this antiderivative or
extract the selected swirl coefficient. No molecular or finite-particle
conclusion follows; the benchmark goal remains active.

## Revision 196 — integrate the material tangent-frame rotation

Evaluated the transverse rotation already present in the selected axis
trajectory's deformation matrix. For fixed axis similarity coordinate,
`Omega=f_* (tau/d_*)^(-1-h)`, so its accumulated phase is
`f_* d_*^(1+h) tau_0^(-h) (Q^(-h)-1)/h` for `h>0` and diverges as `Q→0` if
`f_*≠0`. This does not prevent directional alignment: the transverse
component rotates while its size relative to the axial component tends to
zero. An illustrative `f_*=0.336`, taken only from a separate computed profile,
gives 0.32 turns by the paper's water-cutoff scale `Q=.003`, 0.65 turns by its
air scale `Q=1e-5`, and 2.21 turns only at `Q=1e-15`. That distinguishes finite
physical-cutoff estimates from formal continuation to the singular limit and
does not imply finite-particle or molecular winding. Added a symbolic check,
regression test, and explanation in `docs/openai-core-material-trajectory.md`;
artifact: `evidence/tests/material-rotation-phase.json`. The selected-profile
coefficient remains non-effective, and the benchmark goal remains active.

## Revision 195 — independently replay the public similarity-flow test suite

Pinned the preprint's public GitLab snapshot at
`10377a74f81ab7f6edff0892a379d4937e17fd9b`, inspected the bounded test entry
point, and ran `python tests.py` in an isolated `work/` directory. All four
checks pass: coordinate-operator identity, leading-order NS substitution,
heat-exterior residual decreasing from 2.98e-2 to 9.77e-4 over four grids, and
manufactured-solution errors reaching about 1e-11. This independently replays
the published checks but does not validate their sufficiency, recreate raw
parameter sweeps, or reproduce the complete OpenAI construction. Evidence and
hashes are in `evidence/external/swirl-collapse-verification-2026-10-02.json`.
No particle alignment or material-line winding conclusion is upgraded. Goal
remains active.

## Revision 194 — assess the post-announcement similarity-flow study

Added a scoped review of Duraiswami's 2026-09-15 arXiv follow-up, which
computes a related porous-annulus profile and an axis Cauchy problem in the
OpenAI construction's similarity variables. It is not a reproduction of the
full force pulses, higher-order corrections, or finite-viscosity evolution.
The reported particle-turn estimate characterizes the collapse as Eulerian
profile collapse rather than material-line winding, so the user's particle
alignment/probability idea remains an open observable and needs trajectory and
finite-particle tests. The preprint also documents numerical hazards: domain
truncation can create spurious bifurcations, mapped grids resolve a layer missed
by plain modes, and some branches/spectra remain unconverged. Those are
author-reported and not independently replayed here. No OpenAI GitHub issue is
justified without a demonstrated source defect. Effective extraction of the
selected OpenAI coefficients remains open. Details and source provenance are
in `reports/openai-flow-interpretation-followup-2026-10-02.md`. Goal remains
active.

## Revision 193 — check AMR derivative sensitivity to the post-processing operator

Added a second, unweighted one-ring least-squares derivative estimate from mapped cell-center velocities and captured face adjacency, then applied the same cell-volume MMS integration. At n=64 it gives 14.0719% gradient and 15.9026% curl error, close to the face-Gauss values 14.0147% and 15.8499%; the maximum mapped difference across n=16/32/64 is under 0.092 percentage points. All cell normal matrices are full-rank with maximum condition number 5.0; exact affine recovery and rank-deficiency rejection tests pass. This is post-processing sensitivity evidence, not OpenFOAM's declared gradient scheme or a continuous-field bound. AMR remains `UNCERTAIN`. Updated `reports/openfoam-amr-volume-integrated-diagnostics-2026-10-02.md` and the machine-readable artifact. Goal remains active.

## Revision 192 — integrate AMR derivative error over each cell

Added a reproducible volume-integrated diagnostic for the archived n=16/n=32/n=64 first-map Gauss-gradient fields. It compares the cellwise-constant finite-volume gradient/curl to the analytic MMS derivatives integrated throughout each retained cubic cell, on the same physical interior. At n=64, gradient relative L2 is 13.9804% preMap and 14.0147% mapped; earlier cell-center values were 1.8830% and 12.1431%. Order-6/order-8 tensor quadrature agrees within 1.20e-13 in absolute relative-L2 ratio. This captures P0 within-cell variation but is not a continuous OpenFOAM field bound; AMR quality remains `UNCERTAIN` because no threshold was preregistered. Added unit tests and the replay to the published report runner. Evidence is in `reports/openfoam-amr-volume-integrated-diagnostics-2026-10-02.md` and `evidence/of13-amr-volume-integrated-comparison-2026-10-02.json`. Goal remains active.

## Revision 191 — reconcile the incomplete OpenFOAM repeat with the completed matrix row

Current manifests show that the October 2 n64/dt=.0005 attempt stopped after 36/100 converged steps, while the identical protocol row had already completed 100/100 steps, passed standard and local gates, and entered the six-case matrix on September 30. Corrected the current completion audit so the partial repeat remains preserved/excluded but is not described as a separate missing matrix condition. The matrix verdict does not change. Evidence is `evidence/of13-high-gradient-v2/incomplete-rerun-2026-10-02/status.json`, `evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005-manifest.json`, and `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`. Goal remains active.

## Revision 190 — trace the retained entrance margin's pressure-cutoff dependency

Re-read the pinned OpenAI source proof of `NaturalEntrance.CoefficientProfile.cone_at_four` and the records selected by `FinalSlowBase.actualProfile`. Its high-`chi` branch gets the cone margin from the retained slope estimate; its low-`chi` branch uses the pressure cutoff `|Z| ≤ delta → 99/100 < chi` to force pressure deviation, then separation and smallness estimates. `prepare_axis_with_cutoff` constructs that cutoff using `core.P ≥ 2` but returns the cutoff separately from `AxisPreparation`; the selected record retains entrance existence, not that proof. The exact root pressure-moment inequality remains disconnected from the selected entrance conditions. This narrows the witness-provenance gap but proves neither that the missing implication is impossible nor that `actualProfile` violates a threshold. No upstream issue or physical inference is justified. Details and pinned-file hashes are in `reports/actual-profile-pressure-provenance-2026-10-01.md` and `evidence/upstream-refresh/entrance-branch-dependency-2026-10-02.json`. Goal remains active.

## Revision 189 — clarify coarse versus persistent OpenFOAM gate disagreement

Reconciled the six-case matrix wording with the frozen v2 protocol and
`matrix_reproduction` implementation. The data do contain a standard-PASS /
sampled-local-FAIL disagreement at n=16 and n=32. The preregistered matrix
hypothesis is narrower: the discrepancy must persist at both adequately
resolved levels n=64 and n=128. Both fine cases pass the local gate, so that
persistent criterion is `NOT_OBSERVED`; this does not erase the coarse-grid
disagreement. Added a regression test that preserves this distinction and
updated the completion audit. The frozen protocol, matrix manifest, and replay
evidence remain unchanged. Goal remains active.

## Revision 188 — PhysicsNeMo periodic-boundary claim narrowed against pinned source

Re-fetched the five PhysicsNeMo derivative/API/test files from current main
`83d6a337` and recorded their SHA-256 values. The low-level finite-difference
and spectral functions explicitly document periodic assumptions, so the
existing issue's broad implication that the implementation never documents
periodicity is too strong. The public `GradientsFiniteDifference` and
`PhysicsInformer` entry points still omit that precondition and expose no
boundary-mode option; tests crop two boundary cells and therefore do not
establish nonperiodic boundary accuracy. An exact evaluation of the source's
periodic central stencil on a nonperiodic linear ramp yields `(2-N)/2` at the
first node. PyTorch is unavailable here, so this was a source/algebra audit, not
an execution. Existing issues #2001/#1852 and draft PR #1853 already cover the
concern; no duplicate report was filed. The benchmark itself uses periodic
autodiff and is unaffected. Evidence is in
`reports/physicsnemo-upstream-derivative-audit-2026-10-02.md` and
`evidence/upstream-refresh/physicsnemo-boundary-source-check-2026-10-02.json`.
Goal remains active.

## Revision 187 — exact-head clean export and full-suite evidence

Exported commit `5cb3d65c2b4c065df1cc21ed4ec68dde3b603d7b` from the tracked
Git tree using a fresh locked Python 3.14.5 environment. All 37 published
report-replay steps, six added checks, and a separate full-suite run passed;
the replay reported 201 passed, 1 skipped, and 5 subtests passed, and all 189
compared report/test-evidence files remained byte-identical. The first attempt
used Python 3.12 and changed only recorded interpreter strings plus dependent
hashes; repeating under the recorded Python 3.14 environment removed all seven
differences. The sanitized commands, package list, archive/runner hashes, and
logs are in `evidence/clean-export-2026-10-02-current-head-5cb3d65/`. This
validates postprocessing and archived evidence, not solver reruns or scientific
verdicts. Hosted CI at this head remains queued. Goal remains active.

## Revision 186 — separate audit of neural-forcing blow-up preprint

Read the primary text of Li, arXiv:2609.23934v1. Its reciprocal-vorticity
Riccati and positive-probability steps are conditional on a strict continuum
certificate over a robust open set of frozen forcings. The paper explicitly
leaves candidate-specific validated error enclosures and a positive corrected
margin uncomputed for its archived finite-resolution trajectories; existence
of a loss minimizer is also distinguished from feasibility of a zero
certificate. No unconditional claim about those examples follows from the
plots, and no molecular, viscosity, or light-fluid inference is supported.
This is a mathematical methods audit, not a defect report for the three CFD/ML
repositories, so no upstream post was warranted. Details and source locations
are in `reports/neural-forcing-preprint-audit-2026-10-02.md` and
`evidence/literature/neural-forcing-preprint-2026-10-02.json`. Goal remains
active.

## Revision 185 — latest-head tracked-only export and full-suite replay

Exported committed head `2fb068172a25d980f9eb52b5a519e8666e35fe79` from Git's
tracked tree into a fresh directory and locked Python 3.14.5 environment. All
37 published-report replay steps and six added checks passed; 188 report/test-
evidence files were unchanged. The full suite from the exported source reported
201 passed, 1 skipped, and 5 subtests passed. Sanitized logs, archive/runner
hashes, package versions, and commands are in
`evidence/clean-export-2026-10-02-current-head-2fb0681/`. This is a current-head
postprocessing/export verification, not a solver rebuild/run or scientific
verdict upgrade. Goal remains active.

## Revision 184 — Lagrangian volume constraint on particle-alignment inference

Derived the pre-singular flow-map invariant for the cited smooth incompressible
field: `F=D_aX` satisfies `d(det F)/dt=(div u)det F=0`, hence `det F=1` and
positive-volume material parcels remain positive-volume for every subcritical
time. The OpenAI construction's shrinking, increasingly slender vortex core is
an Eulerian region with axial through-flow, not proof that a fixed set of
molecules aligns into a line. Its `L∞` velocity divergence also does not imply
all particles have unbounded speed or a change in the fixed constitutive
viscosity. Assumptions, derivation, and limits are in
`reports/lagrangian-volume-preservation-and-core-geometry-2026-10-02.md`. This
kinematic distinction does not alter CFD acceptance results. Goal remains
active.

## Revision 183 — live upstream status and PhysicsNeMo reproduction refresh

Refreshed the public project heads and existing report records. OpenFOAM
Foundation 13 and SU2 remain at their audited source heads; no new matching
OpenFOAM issue or duplicate SU2 report is warranted. PhysicsNeMo main advanced
to `83d6a337`, but its odd-width spectrum implementation has the same source
hash and the 33-wide asymmetry reproduces again. The existing PR #2008's exact
head passes the focused regression controls; it remains open and review-required
on an older base. Current-main and fix-control source hashes/results, plus all
project dispositions, are recorded in `evidence/upstream-refresh/live-status-2026-10-02.json`
and `reports/upstream-disposition.md`. No duplicate upstream post was made.
The latest benchmark PR's hosted CI remains queued; the complete local suite
passed on Python 3.12. Goal remains active.

## Revision 182 — follow-up literature scan

Scanned OpenAI’s public Lean repository and post-announcement papers through
2026-10-02. The strongest relevant new result is conditional regularity under
spatially analytic forcing plus structural hypotheses attributed to the
construction; its stated consequence constrains the blow-up force but does not
contradict a merely smooth, nonanalytic force. New profile and numerical
preprints suggest concrete forcing-regularity and similarity-profile audits,
while a separate neural-forcing proof claim remains unaudited. No molecular
alignment, particle trajectory, viscosity-change, practical reachability, or
solver-defect inference follows. Detailed scope, limitations, and source links
are in `reports/navier-stokes-followup-literature-2026-10-02.md`. Goal remains
active.

## Revision 181 — third AMR map resolution and common-support audit

Pre-registered and ran the Foundation 13 n64 same-run first-map capture from
commit `ffc81a2`. The independent predictor's 91,392 buffered cells and
901,888 predicted post-map cells matched the solver log exactly. The solver
exited zero with `End`; the 996 MB archive hash was recomputed and all 59 tar
members were fully read. Mapped cell values exactly match parent injection
(relative L2 0; parent-volume closure error `1.98e-14`). Recomputed the n16,
n32, and n64 Gauss-gradient/vorticity comparisons on one shared physical
interior, correcting the earlier cross-resolution mask mismatch. Gradient
error's descriptive pairwise slopes are ~1.883/~1.964 before map and
~0.993/~1.001 after map; this is consistent with piecewise-constant transfer and is not a
defect verdict, asymptotic proof, or continuous-field certificate. AMR quality
remains UNCERTAIN because no quality threshold was preregistered. Full scope,
reproduction commands, and limitations are in
`reports/openfoam-amr-common-support-resolution-2026-10-02.md` and
`evidence/of13-amr-resolution-comparison-2026-10-02.json`. The full 996 MB
as-run archive is preserved locally; a compact review archive is published as
verified split Zstandard parts to stay within GitHub file limits. Goal remains
active.

## Revision 180 — rate-capped tail clock-mass upper bound independently checked

Added and compiled a Lean corollary converting the conditional signed
tail-pressure bound into an upper bound on the nonnegative post-flattening
clock-weight mass:
`integral_{flattenEnd}^∞ clockWeight ≤ P²/50`. Independent nanoda checked
64,192 declarations with zero typechecker errors and found all six selected
theorems; the existing single pretty-printer limitation remains. This bound is
for an existential rate-capped full `ProfileData` assembled from the pinned
source, not a concentration lower bound and not a property of
`FinalSlowBase.actualProfile`. It therefore does not establish the root
pressure sign or any particle/physical consequence. Summary and hashes are in
`evidence/lean-verification/selected-schedule-tail-mass-nanoda-2026-10-02.json`.
Here `P` is the positive outgoing core amplitude `d.core.P`, not the signed
pressure function.
Goal remains active.

## Revision 179 — pressure-threshold algebra and benchmark replay refreshed

Re-ran the exact SymPy pressure-moment check in the locked environment
(SymPy 1.14.0). It reproduces the root identity and sufficient amplitude
threshold; low- and high-moment algebraic controls have opposite signs. These
controls are not complete constructed profiles, and no quantitative bound for
the pinned `actualProfile` follows. Replayed the frozen Foundation 13 archive
matrix: six archives pass standard acceptance; local quality fails only at
n16/n32, so the preregistered blind-spot conjunction remains `NOT_OBSERVED`.
This is archive/diagnostic replay, not a new solver run or physical validation.
The latest PR #4 head `7b5eda9` remains open and mergeable; its Python
verification workflow is still queued. Details and the distinction between
pressure-tail bounds and the unresolved actual-profile moment are in
`reports/analytic-pressure-followup-2026-10-02.md`. Overall goal remains active.

## Revision 178 — independent nanoda check of selected schedule pressure tail

Independently exported and checked the selected-schedule tail-pressure Lean
extension with the pinned nanoda checker. It checked 64,191 declarations with
zero typechecker errors; the selected tail-coefficient, pressure-bound, and
existential rate-capped profile declarations are present. The log also reports
one pretty-printer limitation (`Unable to print axioms`); Lean's source-side
axiom audit lists only `propext`, `Classical.choice`, and `Quot.sound` for the
extension's declarations. The approximately 612 MiB export is retained locally
with its SHA-256 rather than committed; the checked source, checker image ID,
logs, hashes, and replay script are tracked in
`evidence/lean-verification/selected-schedule-tail-nanoda-2026-10-02.json` and
`runtime/lean-verification/check_selected_schedule_tail_pressure_nanoda.sh`.

This verifies terms under the recorded checker setup; it does not validate the
upstream mathematical construction's assumptions or physical relevance. The
rate-capped profile remains existential and is not identified with
`FinalSlowBase.actualProfile`; the root-pressure premise for that actual choice
remains unresolved. No full pressure-sign, fluid simulation, particle
alignment, phase-transition, or molecular-scale conclusion follows. Overall
goal remains active.

## Revision 177 — incomplete OpenFOAM rerun container status resolved

Rechecked the preserved Foundation 13 n64/dt=.0005 attempt against its raw
solver log: 36 of 100 steps converged through `t=.018`; the following `.0185`
time label has no convergence record. The run has no `exit.json` or endpoint
archive. Current Docker inspection finds no container object, and no host
`foamRun` process is present. Published the sanitized inputs, input hashes,
invocation, logs and current liveness observation at
`evidence/of13-high-gradient-v2/incomplete-rerun-2026-10-02/`. It remains
excluded from the completed six-case matrix and all scientific verdicts. Goal
remains active.

## Revision 176 — Foundation v14 current-release and tracker audit

Refreshed the OpenFOAM Foundation upstream inventory against the current
release and source. Foundation v14 is the current release, and
`OpenFOAM/OpenFOAM-14` advanced to `162fa7a2e51e9c9a86c3000efdd885907f7d1acc`
on September 30. The repo's only open issue concerns a tutorial crash, while
two open PRs concern ParaView/VTK; none matches this benchmark. Its `COPYING`
declares GPL-3.0-or-later; the GitHub API license field is `NOASSERTION`.
Foundation guidance points effective development to `OpenFOAM-dev` and
requires its Contributor Agreement for significant fixes/new development.

The official Mantis all-issues page redirects to login in this environment;
prior targeted searches therefore remain non-exhaustive. Foundation 14 has
only a single n64/dt=.001 compatibility probe: normalized endpoint fields and
sampled metrics match Foundation 13, but this does not establish a full v14
matrix or AMR behavior. No new defect is reproduced and no upstream issue is
warranted. Evidence is in
`reports/openfoam-foundation-current-upstream-audit-2026-10-02.md` and
`evidence/upstream-refresh/openfoam-foundation-current-2026-10-02.json`.
Overall benchmark goal remains active.

## Revision 175 — completion audit and fixed-head clean export

Reconciled the completion audit with the October 2 OpenFOAM, SU2, and
PhysicsNeMo evidence. The frozen six-case OpenFOAM replay passes standard
acceptance for all cases; sampled local quality fails n16/n32 and passes
n64/n128 plus both n64 temporal cases, so the preregistered blind spot remains
NOT_OBSERVED. A separate live n64 dt=.0005 attempt stopped at 36/100 steps and
is preserved as incomplete, without changing that result. SU2's five archives
also reproduce no standard-PASS/local-FAIL conjunction; related residual
location and time-boundary discussions are already recorded upstream.
PhysicsNeMo's nonperiodic derivative issue does not apply to this benchmark's
periodic autodiff path, and its continuous maximum remains uncertified.

Exported commit `28d417e0ef4e9fccf2876cb0d2cc3c087045c1bf` from tracked Git data
into a fresh locked environment. All 37 replay steps and six additional checks
passed; 182 report/test-evidence files remained byte-identical and tests
reported 200 passed, one skipped, and five subtests passed. The sanitized
record is `evidence/clean-export-2026-10-02-current-head-28d417e/`. This is
postprocessing replay, not a solver rebuild/run, PhysicsNeMo training, Lean
execution, or a scientific verdict upgrade. The original goal remains active:
AMR quality, continuous-field derivatives, the actual-profile pressure
premise, executable extraction, and complete OpenFOAM tracker coverage are
still unresolved. No molecular alignment, phase transition, or
constitutive-viscosity conclusion follows.

## Revision 174 — SU2 residual/local-QoI and upstream triage rechecked

On the current SU2 public state (latest release v8.5.0; master
`bc15466602a687d6fb796d5df7a12ce3fde0949a`), re-ran the frozen five-archive
aggregate/residual review in the locked Python environment. Hashes and metrics
match the tracked review. No case satisfies both the aggregate velocity/energy
thresholds and every-step residual threshold: n16 passes residuals but fails
accuracy, n32 fails both, and all three n64 time cases pass aggregate accuracy
but have 2/3/7 residual-miss steps. Thus the proposed standard-PASS/local-FAIL
blind spot is not reproduced by this SU2 matrix; continuous derivative maxima
remain uncertified. Live issue #2353 covers implicit boundary/motion time
semantics, Discussion #2890 is closed without an accepted answer and already
contains the benchmark's source-time report, and issue #2932 already requests
MAX_RES_LOC output for residual hotspot locations. No duplicate was filed.
Source/issue/license/policy snapshot and exact dispositions are in
`reports/su2-localized-residual-upstream-audit-2026-10-02.md` and
`evidence/upstream-refresh/su2-localized-residual-upstream-audit-2026-10-02.json`.
Overall benchmark goal remains active.

## Revision 173 — PhysicsNeMo boundary-gradient issue triaged against benchmark path

Rechecked the live NVIDIA/physicsnemo repository at main
`83d6a337eecfc70e215ed1978af8dba9a38580fb` (Apache-2.0), the benchmark's
historical v2.2.1 pin `1b961314e42a0625502ba1592d25f706f1e02a24`, current issue
#2001, existing feature issue #1852, draft PR #1853, and the contribution guide.
The reported periodic-wrap limitation concerns grid finite-difference/spectral
derivatives on non-periodic domains. Our frozen periodic benchmark uses
`PhysicsInformer(grad_method='autodiff')` and PyTorch autograd, so that issue
does not apply to the measured path. Existing reports cover the concern and
the guide asks contributors to check for work already underway; no duplicate
was filed. This is not a defect reproduction and does not upgrade the
PhysicsNeMo quality verdict, which remains UNCERTAIN. Evidence is in
`reports/physicsnemo-upstream-derivative-audit-2026-10-02.md` and
`evidence/upstream-refresh/physicsnemo-derivative-boundary-audit-2026-10-02.json`.
Overall benchmark goal remains active.

## Revision 172 — primary PINN gradient-bound claim checked

Inspected the author manuscript and journal record for De Ryck, Jagtap and
Mishra's Navier–Stokes PINN error analysis. Theorem 3.4's L2 stability estimate
contains a Grönwall factor exponential in the exact solution's
`||∇u||_{L∞}`; Remark 3.5 says strong-vorticity/large-gradient classical
solutions can make the bound indicate large generalization error. This is
conditional theory and motivates complementary local derivative checks; it
does not assert failure for every high-gradient case or show that our current
PhysicsNeMo run violates the theorem. Existing PhysicsNeMo metrics remain
finite-sample descriptive, with uncertified continuous peaks and a 5%
comparator not preregistered for that solver. No upstream report is warranted
from this literature audit alone. Detailed scope and structured source record:
`reports/pinn-navier-stokes-gradient-bound-scope-2026-10-02.md` and
`evidence/upstream-refresh/pinn-navier-stokes-gradient-bound-2026-10-02.json`.
Overall benchmark goal remains active.

## Revision 171 — six-case concentration-gate claim replayed from current archives

Re-ran `python -m tools.verify_openfoam_high_gradient_matrix` against the
current six-case index. The verifier passed archive, manifest, protocol and
endpoint checks; all six cases pass the configured standard-acceptance gate.
The frozen local-quality gate fails at n=16 and n=32 and passes at n=64, n=128,
and both finer n=64 time steps. The preregistered persistent-blind-spot verdict
is `NOT_OBSERVED`. This demonstrates a finite-resolution mismatch between the
configured standard gate and the separate local-quality gate in two cases; it
does not establish a general defect in residual-based stopping, an OpenFOAM
bug, or a physical singularity. Archive-level replay JSON is
`evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-02-followup.json`.
The high-gradient AMR quality attribution remains `UNCERTAIN`; its fixed-final-
mesh comparison narrows but does not isolate coarse-history/interpolation/flux
effects. This evidence sharpens the benchmark claim and does not upgrade its
solver-defect verdict. Overall benchmark goal remains active.

## Revision 170 — pre-publication source head passes tracked-only replay

Exported tracked commit `84a3cc6e4bffad458466441201e3b45bcdd77fc6` into a
fresh directory and locked virtual environment. The clean-export check passed
all 37 report-replay steps and six additional checks; 178 tracked
report/test-evidence files remained byte-identical. The complete suite in that
export passed `200 passed, 1 skipped, 5 subtests passed` in 103.23 seconds.
Sanitized commands, package versions, logs and hashes are published in
`evidence/clean-export-2026-10-02-tracer-head/`. Commit `59c8831` publishes
the documentation and sanitized record for that immediately preceding source
head; it changes no code or tests. This is same-host postprocessing/evidence
replay, not solver rebuilds or runs, model retraining, Lean execution, or a
scientific-verdict upgrade. Overall benchmark goal remains active.

## Revision 169 — tracer-position bound applied to the pinned candidate

Connected the Lean-checked transported-mass inequality to the pinned OpenAI
periodic candidate on every fixed preterminal interval `[t0,T]` with
`0<t0<T<1`. Its claimed smoothness, unit periodicity, and divergence-free
property descend to a smooth field on compact `T^3`; standard ODE existence
and Liouville's determinant formula then give a volume-preserving flow on that
interval. For any tracer ensemble with density bounded by `K` at `t0`, the
probability of any measurable moving target at `T` is at most `K` times its
volume. For unit-torus balls of radius `R<1/2`, this is `K*4πR^3/3`.
The measure inequality's Lean replay exits 0 with only the standard
`propext`, `Classical.choice`, and `Quot.sound` axioms; the classical ODE bridge
is documented but not Lean-formalized. This does not describe point-mass,
Brownian, molecular, or orientation dynamics, nor establish a bound uniform at
the singular endpoint. See `docs/incompressible-position-uncertainty.md`.
Overall goal remains active.

## Revision 168 — current OpenFOAM matrix independently rechecked

Re-ran `PYTHONPATH=. python3 tools/verify_openfoam_high_gradient_matrix.py`
and `PYTHONPATH=. python3 tools/compare_high_gradient_temporal.py` against the
current archives. The six-case matrix integrity check passes; all declared
steps, converged-step counts, endpoint fields, and hashes match. The n=64
fixed-grid temporal endpoint-difference order is 0.4985896, while exact
velocity-error orders are -0.00103 and -0.00193; this descriptive trend is
not a temporal error certificate. The frozen concern remains `NOT_OBSERVED`,
AMR quality remains `UNCERTAIN`, and no solver defect or physical singularity
is inferred. The archived 36-step attempt is superseded by the complete
100-step case and remains separately preserved. PR #4 local tests and hosted
CI statuses are recorded in revision 167; hosted CI is checked independently.
Overall goal remains active.

## Revision 167 — full local suite passes at current PR head

Because GitHub Actions run `36926321769` remained queued with no runner, ran
the exact test suite locally on current checkout `fdc9d82290dbd9d76964071540652a338b07aa50`:
`work/reference-check-env/bin/python -m pytest -q tests`. Python 3.14.5 and
pytest 9.1.1 reported `200 passed, 1 skipped, 5 subtests passed` in 105.29 s,
exit 0. The skip is not counted as a pass. Machine-readable execution metadata
and the locked-requirements hash are in
`evidence/tests/full-pytest-2026-10-02.json`. This local run does not change
the hosted check's queued status and does not rerun the CFD or PhysicsNeMo
solvers. Overall goal remains active.

## Revision 166 — official claim and prize statuses separated

Rechecked the live primary pages. OpenAI continues to claim that its forced
construction establishes alternatives C and D and says it will not claim the
prize. Clay's announcement calls the result “apparently” settled and says
evaluation is unhurried; Clay's Navier–Stokes page is still labeled `Active`.
This is an administrative-status snapshot, not evidence that Clay rejected
the proof. Preserve the distinction in future descriptions; the dated capture
is `evidence/upstream-refresh/clay-status-2026-10-02.json` and the explanation
is appended to `reports/recent-developments-and-hypothesis-audit-2026-09-28.md`.
The proof-status audit and the three-solver benchmark remain separate work;
overall goal remains active.

## Revision 165 — capped prepared selector gives a uniformly small tail

Formalized that the explicit coefficient multiplying `P^2` in the selected
schedule tail bound is at most `1/100` whenever
`lam ≤ exp(-(exp(m)+12+3/5))/4`. This is the incoming lambda cap used inside
the pinned source's tail-threshold construction. The source's public profile
selector does not preserve that cap in its result, so the audit reduces its
valid threshold by taking a minimum with the cap, then reruns the existing
scheduled-family and prepared-profile construction while retaining both the
exact wait identity and cap. Lean proves existence of such a prepared profile
with tail pressure at least `-P^2/100`; the declarations use only
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.

This is an alternative source-derived selection and does not establish the
same bound for `FinalSlowBase.actualProfile`, which is still chosen through a
record that drops the prepared witness, amplitude proof, wait identity, and
lambda cap. It also does not establish the remaining root-pressure premise,
solver correctness, or any molecular/viscosity interpretation. Exact source
hashes, replay output, and scope are recorded in
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`;
the provenance limitation is in
`reports/actual-profile-pressure-provenance-2026-10-01.md`. Overall goal
remains active.

Follow-up: the rate-capped prepared profile now also passes through the
pinned `NominalConeAssembly.exists_certificate` and
`ModulatedProfileAssembly.exists_of_certificate` constructors. Lean proves
existence of a full `FinalSlowBase.ProfileData` record whose `outgoing` field
is exactly that capped prepared profile, so the tail estimate survives the
later nominal/modulation stages. This remains existential and does not
identify `FinalSlowBase.actualProfile`, whose classical choice is separate.

## Revision 164 — conditional tail bound normalized by core amplitude squared

Proved the exact `clockWeight(flattenEnd)` formula from the pinned outgoing
schedule's pulse amplitude and decay. Combining it with the source theorem
`pulseAmplitude_small` proves a `P^2`-relative lower bound for the tail
pressure, conditional on the exact wait identity
`wait = 60 * log (1 / lam)`. Its coefficient is
`(5/32) * lam^60 * exp(2*exp(m) - 4/5 - 13/lam - (1+2*lam)*flattenLength)`.
Lean reports only `[propext, Classical.choice, Quot.sound]` for the new
declarations, with no `sorryAx`. The coefficient still depends on `m` and
`lam`, and this lemma alone does not show that it is small for the final
selected profile or prove the needed root-pressure sign. Source log, hashes,
and scope are updated in
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`;
the analytical limitation is in
`reports/actual-profile-pressure-provenance-2026-10-01.md`. Overall goal
remains active.

## Revision 163 — selected-schedule tail mass bounded by endpoint clock weight

Extended the isolated Lean audit from eta-independence to a quantitative
one-sided estimate for the actual constructed schedule:
`-(5/8) exp(6/5) clockWeight(flattenEnd) <= tailPressureContribution <= 0`.
Both inequalities compile against the pinned OpenAI/NavierStokesAndEuler
source and use only `[propext, Classical.choice, Quot.sound]`, with no
`sorryAx`. This identifies an explicit endpoint quantity controlling the
zero-exponent pressure tail. It is not yet normalized by `core.P^2`, so the
actual-profile root-pressure premise remains unproved; the remaining bridge
must use the pulse-amplitude and parameter-threshold constraints. The updated
log/hash/scope record is
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`,
and interpretation is appended to
`reports/actual-profile-pressure-provenance-2026-10-01.md`. The broader
benchmark and research goal remains active.

## Revision 161 — pressure-data-only amplitude converse ruled out

Analytically constructed and symbolically replayed a countermodel for the
weaker implication from generic pressure hypotheses to the ideal-prefix
amplitude threshold. For any
`0<B<2`, the prescribed prefix `B^2 exp(y/5)` plus exponent-zero tail mass `2`
on `[1,2]` yields `P(eta)=-1-(5/2)B^2(1+eta^2)^(-2)`, so pressure remains at
most `-1` and `eta P'(eta)>=0` while the prefix amplitude is below 2. This is
not a counterexample to the selected OpenAI-derived profile: the added tail
need not satisfy its schedule-shape and entrance-profile constraints. The
SymPy 1.14 checker and focused regression test pass, and the check is included
in the published-evidence replay. The full suite on the resulting worktree
passed 200 tests, skipped one, and passed five subtests in 103.18 seconds
under Python 3.14.5. It rules out recovering the amplitude from `PressureData`
and generic admissibility alone, narrowing the remaining proof to those
additional constraints or witness retention. GitHub Actions remains queued
at prior PR #4 head `f51dc335`; the new checker is local pending the final
head's run. The full benchmark goal remains active.

## Revision 162 — selected schedule tail identified as the pressure bridge

Checked the pinned source identities behind the prior countermodel. The actual
`SchedulePressure` exponent reaches zero after `flattenEnd`, so that region's
pressure integral is an eta-independent negative constant. This matches the
generic countermodel's mechanism structurally, but the actual tail weight is
coupled to `TailData` and is not freely selectable. The next analytical target
Lean now checks that the selected schedule's tail pressure contribution on
`Ici flattenEnd` is exactly independent of eta; both declarations use only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. The replay,
input hashes, and scope are recorded in
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`.
The next target is a quantitative upper bound for this tail mass relative to
`core.P^2`, or an exact root-pressure estimate using retained schedule
constraints. This does not establish the pressure premise for `actualProfile`
or a molecular/viscosity consequence. Goal remains active.

## Revision 160 — prospective PhysicsNeMo held-out gate evaluated

To address the old PhysicsNeMo verdict's missing preregistered threshold, froze
`protocols/physicsnemo-heldout-validation-v2.json` at commit `d2e71d71` before
the full evaluation. It applies the shared benchmark tolerances (2% velocity
L2/energy, 5% sampled gradient/vorticity peaks, spectrum L1, and normalized
divergence) to the five fixed cases across five archived seeds. All 25 frozen
models completed on a new 64^3 shifted spatial grid from the pinned v2.2.1
source. Nineteen passed all sampled metrics; six failed only velocity L2,
including all five cases for seed 8191. Every sampled local metric passed, so
the preregistered sampled global-pass/local-fail conjunction was
`NOT_OBSERVED` wherever global metrics passed. This does not certify continuous
extrema, optimizer convergence, or population behavior; continuous local
quality remains `UNCERTAIN`. Full results and limitations are in
`reports/physicsnemo-heldout-validation-v2-2026-10-02.md` and
`evidence/physicsnemo-heldout-validation-v2/results.json`. The new protocol,
evaluator and tests are on PR #4; the full Python test suite and current CI
still need verification. Overall goal remains active.

## Revision 159 — six-case matrix status reconciled against the archives

Rechecked the apparent conflict between the immutable base manifest and the
later matrix index. The base `manifest.json` remains a historical 4/6 run
record; it must not be read as the current matrix status. The dated
`manifest-current-2026-09-30.json` joins the two separately archived temporal
rows, and `tools.verify_openfoam_high_gradient_matrix` independently replays
all six archives and gates from their hashes. The replay reports 6/6 complete,
all standard gates passing, local-quality failures only at n=16 and n=32, and
the preregistered n=64/n=128 persistent-blind-spot result `NOT_OBSERVED`.
This reconciles document state; it adds no solver run and no physical evidence.
The temporal triplet still does not certify asymptotic time convergence, and
AMR attribution remains UNCERTAIN. CI for PR #4 is still QUEUED at head
`bca222f921f338ca62bb245ed9a1df4a0d8f22d7`; overall goal remains active.

## Revision 158 — full suite after AMR post-processing audit

The new OpenFOAM tensor-convention regression tests pass (4). The complete
locked-dependency suite at the current worktree passes 194 tests, skips one,
and passes five subtests in 104.19 seconds. The skip is not counted as a pass.
The post-processing replay itself also completed on four archived cases and
validated exact meshes, source archive hashes, OpenFOAM gradient/vorticity
consistency, and the dynamic archived-gradient byte comparison. These checks
do not change the AMR quality status from UNCERTAIN. Goal remains active.

## Revision 157 — same-mesh AMR derivative controls replayed

Applied Foundation 13 `foamPostProcess` `grad(U)` and `vorticity` to the two
archived dynamic-AMR cases and their analytic-initialized fixed-final-mesh
controls. For each cell budget, points, faces, owner/neighbour, boundary,
centers, and volumes match exactly. Source inspection caught and corrected the
OpenFOAM gradient tensor's derivative-index-first storage before comparing to
the analytic derivative. The separate vorticity field agrees with the curl of
the converted gradient within `2.62e-16` relative L2, and regenerated dynamic
`grad(U)` fields match the archived solver fields byte-for-byte.

On the shared interior mask, dynamic/control gradient relative L2 errors are
48.72%/7.35% at cap5000 and 89.79%/1.98% at cap100000; vorticity errors are
54.65%/8.63% and 110.42%/2.34%, respectively. This shows much higher error
after the dynamic coarse-to-fine history than on the same endpoint mesh when
initialized analytically, but the control does not isolate mapping from
coarse-history error and later evolution. AMR quality remains UNCERTAIN and no
upstream defect is established. The replay tool, exact metrics, logs, and
limits are in `tools/replay_amr_remap_gradient_controls.py`,
`reports/openfoam-amr-remap-derivative-controls-2026-10-02.md`, and
`evidence/of13-amr-remap-gradient-controls-2026-10-02/`. Goal remains active.

## Revision 156 — full local suite at the published PR head

At PR head `88698e033c4d1999aaa4358d3cdcc6a25cf8cce6`, the first direct
locked-environment `pytest` invocation failed during collection because this
repository requires its root on `PYTHONPATH`. Re-running with
`PYTHONPATH=.` and the locked verification requirements passed: 190 tests,
one skipped, and five subtests in 103.96 seconds. The skip remains a skip, not
a pass. This validates the current full local suite; the GitHub Actions check
for the PR was still queued at the time of this run. Goal remains active.

## Revision 155 — bounded-position probability in the affine comparison model

Replayed the exact SymPy checks for the tangent-map/Gaussian calculation,
finite-packet exponent conditions, and Jeffery-director comparison in the
locked verification environment. Clarified a useful geometric distinction:
under the imposed global affine map, a fixed-radius infinite axial tube has
probability tending to one, while the probability of every fixed-radius 3D
ball tends to zero, uniformly over a moving ball center, with upper bound
`sqrt(2/pi) * R * Q^C / sigma`. Thus “alignment” does not mean bounded
position certainty even within this idealized comparison model. This bound
does not transfer to the nonlinear selected flow: its finite-packet estimate
still requires non-effective tube/Hessian constants and a shrinking initial
packet. No molecular or viscosity claim follows. Details are in
`docs/particle-position-probability.md`; goal remains active.

## Revision 154 — Foundation 14 single-case compatibility probe

Ran the unchanged high-gradient protocol at `n=64`, `dt=0.001`, and
`endTime=0.05` using the official OpenFOAM Foundation 14 package `20260724`
in a locally built, pinned-base Linux/arm64 image. All 50 steps converged and
the configured standard and sampled local-quality gates passed. The endpoint
fields `U`, `p`, `phi`, `C`, `Ccx`, `Ccy`, and `Ccz` match the published v13
case byte-for-byte after normalizing only the version banner; the five
recorded sampled diagnostics also match exactly. Corrected the earlier source
focus: this case selects `incompressibleFluid`, not `isothermalFluid`. The v14
MRF and moving-mesh refactors are outside this static, no-MRF case. Therefore
this is one-case compatibility evidence only, not full v14 equivalence,
continuous-extremum certification, a solver-defect finding, or support for
the molecular/physical hypothesis. The v14 matrix remains open. Details and
replay artifacts are in `reports/openfoam-foundation14-compatibility-probe-2026-10-02.md`
and `evidence/of14-high-gradient-v1/`. Goal remains active.

## Revision 153 — scope-gate outputs replay cleanly at a fixed commit

For commit `a3d07c19b66c497a9047df2a3650582157399004`, a tracked-only export
with a fresh Python 3.14.5 environment completed all 36 report/evidence replay
steps and six additional checks. All 172 compared tracked evidence/report
files remained byte-identical (`changed_files=[]`). The locked-environment
full suite separately passed 190 tests, skipped one, and passed five subtests;
the tested Python source and tests match the a3d07c1 tree, whose later commit
changes only reports, documentation, and evidence. GitHub PR #4's check is
still QUEUED for hosted-runner allocation, with no failure conclusion. The
replay record is in `evidence/clean-export-2026-10-02-scope-gate.json`. Goal
remains active; Foundation v14 is a separate follow-up comparison, not covered
by these checks.

## Revision 152 — regenerated verdict snapshots retain declared scope

The tracked-only replay of fixed commit `3b394646e9fd5c3cfac1c8cfeacb89d2df5a611a`
completed all 36 steps, but its clean comparison found seven derived verdict
JSON files that predated the new scope field. Replaying with the recorded
Python 3.14.5 runtime isolated the diffs to additive `scope` values; all
`standard_acceptance`, `local_quality`, and `hypothesis` values stayed
`UNCERTAIN`. Updated those seven snapshots so the published outputs match the
gate's current schema. A separate fixed-export Python 3.12.13 test run passed
190 tests, skipped one, and passed five subtests in 121.21 seconds. The
follow-up clean export confirmed byte-identical replay after the seven snapshot
updates. Goal remains active.

## Revision 151 — current-release and estimator literature refresh

Checked the OpenFOAM Foundation's v14 release notes and identified a new
coverage gap: the existing uniform-grid and AMR evidence is pinned to v13, so
v14 should be evaluated separately with the unchanged manufactured case and
runtime provenance before making any cross-version claim. Also found a 2026
VPINN paper reporting a local adaptive error estimator for stationary
Navier–Stokes energy-norm error. It motivates a method comparison only; its
stationary neural formulation does not validate this unsteady finite-volume
field or establish physical consequences. No existing verdict or upstream
defect disposition changed. Details and source links are in
`reports/recent-navier-stokes-verification-developments-2026-10-01.md` and
`evidence/upstream-refresh/openfoam14-and-vpinn-estimator-2026-10-02.json`.
Goal remains active.

## Revision 150 — gate verdicts now preserve their declared scope

The v2 report triage gate previously emitted `REPRODUCED`/`FAIL` without
carrying the report's top-level scope into CLI output, and it would still
classify a synthetic or real report with no scope. Added a test-first
regression: omission leaves all decisions UNCERTAIN, and a valid decision
echoes its declared scope. The failing tests reproduced both behaviors before
the minimal checker change; focused tests now pass (14). Existing v2 report
files were inventoried and each contains a non-empty scope. Documentation now
states scope is required but is itself not proof, and distinguishes actual
solver-field claims from discrete/named-reconstruction metrics. Full suite and
all report replays remain to be checked. Goal remains active.

## Revision 149 — continuous-extremum target made explicit in protocol

Updated the shared benchmark protocol so every continuous-extremum claim names
its object (analytic reference, declared reconstruction, or underlying solver
field). It now states that finite-volume DOFs, even under exact-cell-average
and uniform-velocity-convergence assumptions, cannot by themselves certify
the underlying field's continuous derivative. Actual-field certification
requires explicit regularity/unresolved-mode premises; otherwise its verdict
stays UNCERTAIN, and a trig-interpolant certificate does not transfer. Added
the same requirement to the acceptance criteria of internal issue #5 and
read it back from GitHub. No solver or frozen v2 verdict changed. Goal remains
active.

## Revision 148 — nullspace limit added to the gate successor issue

Read back the new comment on the existing benchmark issue #5:
https://github.com/Unjuno/concentration-aware-ns/issues/5#issuecomment-5936795793
It records the divergence-free smooth cell-local sequence, the exact-average
and face-trace invariances, the small-uniform-velocity/large-gradient scaling,
and the restriction that this is neither the archived solver field nor a
same-forcing solution. The recommendation is to require regularity/unresolved
mode assumptions for any actual-field continuous bound, or scope certificates
to named reconstructions. This extends internal acceptance planning; it does
not report an OpenFOAM defect or alter frozen verdicts. Goal remains active.

## Revision 147 — derivative observation limit strengthened and replayable

Replaced the arbitrary-amplitude smooth null perturbation with an explicit
high-frequency divergence-free sequence supported inside one finite-volume
cell. With `A_k=(0,0,k^(-3/2) chi sin(k*y))` and `w_k=curl(A_k)`, each perturbation
has zero cell average and zero face trace; `||w_k||_infinity=O(k^(-1/2))` while
`||grad(w_k)||_infinity=Theta(k^(1/2))` under the stated nonzero smooth cutoff
assumption. Thus the derivative is not continuous in even uniform velocity
error over the observation class. This still does not show an OpenFOAM output
contains the perturbation or that it obeys the same forced PDE. Added symbolic
replay `tools/check_fv_derivative_nullspace.py`, JSON output, and a regression
test. SymPy identities and the focused test pass; the full suite reports 188
passed, 1 skipped, 5 subtests. Existing frozen solver verdicts and upstream
disposition are unchanged. Goal remains active.

## Revision 146 — evidence-bundle commit also replays from tracked export

Ran a second tracked-only clean export on the evidence-bundle commit
`0d1d1648cad91d99f79e62abfe5193ebe3af619b`. Its fixed-commit manifest reports
36/36 replay steps, six additional checks successful, 171 compared tracked
report/evidence files, and `changed_files=[]`. The sanitized follow-up result
and per-step logs are saved in
`evidence/clean-export-2026-10-02-upstream-refresh/current-head-0d1d164/`.
Compared with the commit whose exported source ran the full 187-test suite,
this commit changes only goal/completion documentation and the evidence
bundle, not Python source or tests; that exact source/test suite is therefore
unchanged. No solver was rebuilt or rerun. Goal remains active.

## Revision 145 — current focused upstream audit passes tracked-only replay

Ran `tools.check_clean_export --locked` against fixed commit
`039ace23a542e82bfc81632d14673d05abea3cec` in a fresh tracked-only export and
virtual environment. All 36 published report replay steps and six additional
checks exited zero; 171 tracked report/evidence files were byte-identical
after replay. Ran the full test suite from that extracted source as a separate
step: 187 passed, 1 skipped, and 5 subtests passed. The complete redacted
manifest, per-step logs, pytest log, hashes, environment, and reproduction
commands are in
`evidence/clean-export-2026-10-02-upstream-refresh/`. This validates public
Python/evidence replay only, not solver execution or new scientific claims.
The overall goal remains active.

## Revision 144 — three-project focused upstream refresh recorded

Refreshed default-branch heads, releases and existing records through the
official GitHub APIs. OpenFOAM Foundation 13 remains at the benchmark source
commit; its four GitHub issues do not match the AMR finding. The separate
Foundation tracker returned HTTP 403 to direct access; focused searches found
only older/differently scoped AMR items, so absence of a match is not claimed
as exhaustive. SU2 master remains at the audited source pin; Discussion #2890
and Issue #2353 remain the appropriate time-level records. PhysicsNeMo main
advanced one commit, changing only three example README paths; the audited
`power_spectrum.py` blob is identical. Issue #2007 and PR #2008 remain open,
with the PR behind main. No duplicate issue is justified. The exact live
metadata and source-blob comparison are in
`evidence/upstream-refresh/three-project-inventory-2026-10-02.json`. Overall
goal remains active; latest PR Actions test remains queued.

## Revision 143 — PR-scoped concurrency now observed cancelling obsolete runs

Read the authoritative Actions run records after pushing follow-up commits.
The post-change runs for `c94aa4b` and `a5f939e` each ended `cancelled` when a
newer run in the PR-scoped concurrency group arrived, confirming that the
workflow prevents those post-change superseded heads from accumulating. One
pre-change queued run (`c9479c4`) did not join that group and was separately
sent a cancellation request. The latest exact-head check for `8997b75` remains
QUEUED without a runner assignment; concurrency solves stale-check churn, not
the underlying GitHub Actions service/account queue condition. No solver or
mathematical verdict changed. Overall goal remains active.

## Revision 142 — CI concurrency mitigation awaits hosted-runner evidence

After adding the PR-scoped concurrency group, the PR head advanced to
`a5f939e8cf93ce53fa3af0eebc0f7f9667e171d9`. The authoritative check-runs API
shows its `tests` check queued since 2026-10-01 16:54:45 UTC; the preceding
`c94aa4b` and older checks also remained queued at the latest read. Therefore
the workflow change's effect on already-pending work is not demonstrated, and
the root runner-assignment delay remains unresolved. Do not describe the new
setting as verified queue mitigation until a subsequent PR update is observed
starting/cancelling runs as intended. Latest source and local scientific
changes remain covered by the immediately prior full local suite (187 passed,
1 skipped, 5 subtests); only workflow/log documentation changed after it. The
benchmark goal remains active.

## Revision 141 — superseded pull-request verification runs are cancellable

The PR's repeated commits had accumulated queued checks for obsolete heads.
Added a workflow concurrency group keyed by pull-request number (or ref for
non-PR events), with cancellation of superseded runs, following the current
GitHub Actions workflow-concurrency contract. Older unstarted checks were
cancelled where possible. This reduces stale queue buildup but does not fix the
underlying GitHub-hosted runner assignment problem: the latest check on
`c94aa4b` is still QUEUED, while the exact-head local suite on the preceding
science/documentation changes passed. Repository actions are enabled and
workflow permissions are read-only; the billing endpoint was unavailable to
the current token. No current GitHub Status incident explains the delay.
`reports/openfoam-fv-continuous-derivative-identifiability.md` remains a
mathematical scope result, not an upstream defect report. Overall goal remains
active.

## Revision 140 — finite-volume continuous-field ambiguity bounded analytically

Audited the pinned Foundation 13 `volVectorField` typedef and formalized the
interpretation limit for archived finite-volume DOFs. Even under the stronger
assumption that each stored value is an exact cell average, a nonzero smooth
divergence-free curl supported strictly inside one cell has zero cell average
and vanishes near all faces. Arbitrary amplitude therefore preserves every
average and face value while making the continuous gradient arbitrarily
large. This is an information-theoretic non-uniqueness result, not evidence
that OpenFOAM produced such a field, that the perturbed field satisfies the
same forced PDE, or that molecules align. Added
`reports/openfoam-fv-continuous-derivative-identifiability.md` and linked it
from the completion audit; no duplicate OpenFOAM issue was filed. Commit
`98e8dcc` is pushed to PR #4. The exact-head local suite passes (187 passed,
1 skipped, 5 subtests), but the matching GitHub Actions job remains QUEUED
without runner assignment. The overall benchmark and upstream audit remain
active.

## Revision 139 — fixed-head clean export passes from public artifacts

Re-ran `tools.check_clean_export --locked` on fixed commit
`e5f4aab6c6411266c6300abe6c79023a77e4411e` in a fresh tracked-only archive and
venv after removing the temporal replay's ignored-`work/` dependency. All 36
published replay steps and six extra verifier checks exited zero; 170 tracked
report and `evidence/tests` files were byte-identical after replay. The locked
environment ran the full test suite: 187 passed, 1 skipped, 5 subtests passed.
Pre-fix failure evidence from commit `46691344` is retained beside the passing
result. The export is same-host Python/evidence replay, not a solver rebuild,
solver rerun, training run, Lean replay, or scientific-verdict upgrade. The
reproduction package is `evidence/clean-export-2026-10-02-archive-replay/`.
Absolute workstation and temporary roots are replaced with placeholders in
the public log copies, and their published-copy hashes are recomputed.
The overall goal remains active.

## Revision 138 — remove tracked-only temporal replay dependency on ignored data

A tracked-only clean export at `46691344f203f504f18f04829531e9be1dfc7646`
failed report replay at step 8, `openfoam_temporal_triplet`, because the
comparison script read `work/of13-high-gradient-v2/...`, which is ignored and
absent from a public `git archive`, even though all three frozen case tarballs
were tracked. Reworked the comparer to safely extract each hashed public
archive into a fresh temporary directory, verify the archived solver-log hash
and completion/acceptance state, and reproduce the matrix status from the
cross-run and base manifests. Added path-traversal and unexpected-case tests.
The focused archive tests pass (4), the temporal comparison reproduces the
prior values (order `0.4985896`, both input/center checks true, time-error
certificate false), and the full suite passes (187 passed, 1 skipped, 5
subtests). This is a benchmark reproducibility defect, not a solver defect.
The fixed-commit clean-export rerun remains in progress; goal stays active.
Revision 139 records its successful completion.

## Revision 137 — full local verification of current PR head

Inspected the live GitHub PR set and upstream feedback state. PRs #1–#3 have
successful checks; PR #4 is open at the current branch HEAD
`2ccc60e98205b0f954346925d895b2f4c1b87d09`, and its matching GitHub Actions
run remains `QUEUED` since 2026-10-01 16:11 UTC. Independently ran the same
workflow command, `python -m pytest -q tests`, in the existing pinned
`work/reference-check-env` (Python 3.14.5, pytest 9.1.1, SciPy 1.16.2,
python-flint 0.9.0): 183 passed, 1 skipped, 5 subtests passed in 102.81 s.
The system Python lacked pytest and the older PhysicsNeMo environment lacked
SciPy; neither failure was attributed to repository code. Live upstream
recheck confirms PhysicsNeMo issue #2007 and PR #2008 are still open, and SU2
Discussion #2890 remains closed/unanswered. These existing reports make a
duplicate upstream post unwarranted. OpenAI still has Issues and Discussions
disabled. The goal remains active; a matching hosted check is still pending.

## Revision 136 — physical-scaling follow-up rechecked

Reread Duraiswami's arXiv:2609.17642 through the reduced similarity-profile
computation, admissibility-cone analysis, and section 8 physical estimates.
The paper's smooth reduced-profile cone failure is explicitly scoped away from
the full OpenAI piecewise pulse construction, which it does not compute. Its
water cavitation and air compressibility estimates occur before molecular
scales under the stated illustrative conditions; tracer paths turn only a
fraction of a revolution per collapse-time decade in its computed profile.
These are model-dependent order-of-magnitude estimates, not experimental
validation. They sharpen the cutoff and material-motion distinctions while
leaving the selected-field infinitesimal alignment result separate and finite
packets conditional. Evidence and scope are preserved in
`evidence/upstream-refresh/duraiswami-physical-followup-2026-10-02.json` and
the dated literature report. The overall repository goal remains active.

## Revision 135 — correct the OpenAI Lean proof-status audit

The prior report treated the `OPEN` comment in `NavierStokes/ProblemStatement.lean`
as the status of the entire OpenAI repository. That was a false negative: the
file defines the proposition without proving it locally, while
`NavierStokes/ActualCandidateAssembly.lean` proves
`selected_candidate : ProblemStatement.candidateStatement` and
`NavierStokes/R3/Theorem.lean` proves `theorem_1_1` and the breakdown statement.
On a clean clone at upstream commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`,
`lake build NavierStokes.ActualCandidateAssembly NavierStokes.R3.Theorem`
completed successfully (9,350 jobs). `#print axioms` for the candidate theorem,
whole-space theorem, and initial-rest theorem reported only `propext`,
`Classical.choice`, and `Quot.sound`. Evidence, source hashes, and scope limits
are recorded in
`evidence/lean-verification/openai-public-proof-audit-2026-10-02.json`;
historical artifacts are retained. This verifies that the pinned repository
formally checks these declarations, not that this project has independently
validated the construction's mathematics or its implications for molecular
ordering, particle certainty, light, phase transitions, or viscosity. The
three-project benchmark goal remains active.

## Revision 134 — latest upstream records and completion metadata hardened

Replayed the independent six-case matrix verifier after tightening it to check
index timestep/convergence counts and embedded local-quality verdicts against
the archived logs and recomputed metrics. Refreshed current upstream state:
PhysicsNeMo main advanced only through dependency maintenance while its audited
`power_spectrum.py` blob stayed unchanged; issue #2007 and PR #2008 remain the
existing odd-width report/fix; SU2 discussion #2890 is closed but still marked
unanswered and contains no code-fix record; OpenAI's repository still has no
issue/discussion channel. The status capture and technical disposition are in
`evidence/upstream-refresh/live-status-2026-10-01T1424Z.json`,
`reports/upstream-status-2026-10-01.md`, and
`reports/recent-navier-stokes-verification-developments-2026-10-01.md`. No
duplicate upstream issue is warranted. The multi-solver and analytic audit
goal remains active.

## Revision 133 — independent replay of the completed OpenFOAM matrix

Rechecked the authoritative cross-run status after the last update: the
six-case high-gradient uniform matrix is complete, and the historical
`n64, dt=0.0005` partial run is explicitly superseded by a separate validated
100/100-step archive. Added an independent replay tool that verifies the
protocol and base-manifest hashes, all six archive hashes, reconstructs and
checks both the split n=128 Zstandard package and original gzip tar, parses
archived timestep/convergence logs and `fvSolution`, confirms endpoint fields,
recomputes local-quality gates, and re-evaluates the preregistered matrix rule.
It passes: all six rows pass standard acceptance; local quality is FAIL at
n=16/32 and PASS at n=64/128 and both smaller n=64 time steps; the persistent
fine-grid blind spot is `NOT_OBSERVED`. The integration test passes. This
closes a stale-status ambiguity and strengthens artifact reproducibility, but
does not establish source/binary equivalence or a continuous finite-volume
derivative certificate. AMR local-quality and broader solver audits remain
open. See `reports/openfoam-six-case-matrix-independent-replay-2026-10-01.md`.

## Revision 132 — AMR derivative replay and post-announcement analytic refresh

Repacked the preserved v5/v6 n=32 same-run AMR archives as package-a4 and
corrected archive tests to distinguish later OpenFOAM checkpoint files from
the excluded later-stage diagnostic CSV snapshots. Replayed both parent-value
and Gauss-gradient analyses from the public tarballs; the uniform preMap
gradient uses centered periodic differences, while the mapped gradient uses
captured oriented face fluxes. Mapped gradient/vorticity errors increase for
these piecewise-constant parent injections, which identifies a mapping
mechanism in these cases and does not establish an AMR defect. Full suite:
`182 passed, 1 skipped, 5 subtests passed`.

Refreshed post-announcement mathematics and the live SU2 #2890 discussion.
The 29 September Constantin–Ignatova–Vicol v2 regularity theorem, under its
joint axisymmetric-core, Type-II, and analytic-forcing assumptions, constrains
the claimed smooth-forced construction but does not contradict a merely
`C∞` nonanalytic force; Cao–Chi–Nie's density result takes the compact
blow-up construction as an input and is not an independent construction.
The OpenAI continuum-to-particle statement motivates a separate microscopic
modeling question, but no reviewed source establishes molecule ordering,
particle-position determinism, optical-fluid behavior, or viscosity collapse.
SU2 #2890's second-order temporal MMS follow-up strengthens the source-time
reproducer while maintaining its stated limits: no general fix is asserted,
and the maintainer recommends explicit stored-time/target-time semantics.
Details and source links are in
`reports/recent-navier-stokes-verification-developments-2026-10-01.md` and
`reports/openfoam-amr-resolution-replication-2026-10-01.md`. The overall
multi-solver verification goal remains active.

## Revision 131 — same-run finite-volume-average DOF audit

Applied the analytic cell-average formula for the separable high-gradient MMS
to the v4 preMap and mapped cell sets from the same run. The closed-form
Fourier/sinc integration has an existing independent tensor-Gauss cross-check
with maximum absolute discrepancy `1.80e-16`. Stored preMap values differ from
coarse exact cell averages by 13.7834% relative L2; mapped values on refined
child DOFs differ from exact child averages by 42.4839%, while the child-center
point-sample error is 41.7955%. The normalized squared child-average error is
`0.015871` inherited parent DOF error plus `0.164617` exact parent-to-child
average variation, with cross term and identity residual at roundoff scale.
This is a DOF-average diagnostic and does not assert OpenFOAM stores exact
cell averages, continuous reconstruction error, or a quality/defect result.
Evidence and replay are in `evidence/of13-amr-same-run-map-v4-run3/` and
`tools/analyze_amr_same_run_map.py`.

## Revision 130 — same-run AMR mapping mechanism isolated

Added a v4 capture immediately before and after `mesh_.update()` at the same
`t=0.002` in one OpenFOAM Foundation 13 run. The saved run has 4,096 pre-map
cells and 16,640 mapped cells. Independent containing-parent injection from
that same run matches every mapped cell-centered velocity value (relative L2
and max absolute difference both zero); parent/child volume closure is
`6.53e-15`. The velocity volume integral changes by `2.91e-16` absolute, with
net change `8.10e-17` scaled by integrated speed. Exact-MMS point-sample error
on mapped child centers is 41.7955%, which is not a finite-volume cell-average
error. Solver exit is zero, `End` is present, the six stage events are logged,
and the override module load is confirmed. The first runner failed only after
archiving because a protocol metadata key was missing; this is explicitly
recorded and the manifest was recovered from preserved artifacts without a
solver rerun. Protocol, archive, manifest, analyzer, and tests are in
`protocols/high-gradient-of13-amr-same-run-map-v4.json`,
`evidence/of13-amr-same-run-map-v4-run3/`,
`tools/analyze_amr_same_run_map.py`, and
`tests/test_amr_same_run_map.py`. This identifies this event's mapping as
piecewise-constant parent injection, not a general defect, quality result, or
physical claim.

## Revision 129 — archived AMR parent-value audit and source-built cap check

The archived AMR stage snapshot was reanalyzed from frozen tarballs rather
than ignored working fields. Independent piecewise-constant transfer from the
earlier archived parent field agrees with the mapped stage to weighted relative
L2 `1.79e-16`, and both give 41.7955% point-sample error against exact MMS at
child centers. This is cross-run evidence: the v1 parent and v3 stage cases
match 10/11 common inputs, with `system/controlDict` write interval the one
difference. A same-run pre-map capture remains necessary for direct
attribution. The pinned Foundation 13 `refiner` library was also rebuilt and
loaded in the same runtime image; the n=16 `maxCells=5000` case again grew
from 4,096 to 16,640 cells. This is consistent with the already documented
approximate-cap, whole-level selection semantics. It is not a new defect
finding, quality verdict, or physical result; no duplicate upstream issue is
warranted. The reproduction remains supplemental evidence under
`work/of13-maxcells-probe-v1/`, while the authoritative source interpretation
is in `reports/openfoam-amr-source-budget-audit-2026-09-28.md` and
`docs/audit.md`.

## Revision 128 — axis-set concentration separated from position certainty

Extended the exact linearized Gaussian calculation along the candidate axis
trajectory. Under the volume-preserving singular values
(Q^(C/2), Q^(C/2), Q^(-C)), the probability within any fixed-radius tube
around the *infinite* axis tends to one, while probability in a finite cylinder
of fixed radius and axial length is asymptotic to
sqrt(2/pi)*(L/sigma)*Q^C and tends to zero. This refines the earlier
fixed-ball result: transverse set concentration can be real in the linearized
model even while bounded 3D position certainty decreases. Exact formulas and
scope limits are in docs/linearized-axis-tube-concentration.md; SymPy
identities, assumptions, and source hash are in
evidence/tests/alignment-uncertainty.json. It remains a Gaussian pushforward
through the variational map, not a nonlinear finite-packet, molecular,
phase-transition, or viscosity result. No solver verdict or upstream report
changes.

Build a reproducible Concentration-Aware Navier–Stokes Verification Benchmark.
Treat the supplied proposal as hypotheses. Verify primary sources, repository
revisions, licenses and execution environments before interpreting experiments.

1. Establish one dedicated repository, a preregistered protocol and reusable
   evidence collection/reporting tools.
2. Implement a smooth, localized 3D incompressible manufactured solution with
   known forcing. Independently verify reference values, forcing and derivatives.
3. Execute OpenFOAM first, then independent SU2 and PhysicsNeMo evaluations.
   Compare at least three spatial resolutions and multiple applicable time steps.
   Record standard convergence/validation, local gradient and vorticity peaks,
   spectra and applicable AMR constraints. Separate hypothesis reproduction from
   numerical quality acceptance.
4. Classify broad audit candidates by evidence and cause. Record fixed commits,
   environments, inputs, thresholds, raw logs, uncertainty and reproduction steps.
5. Complete one audit pass over all three projects. Search existing issues and
   inspect contribution policies. Report only reproducible, nonduplicate findings
   with concrete improvements through appropriate issues or PRs. Preserve report
   URLs or justified decisions not to submit.
6. Publish reproducible artifacts and per-project conclusions with remaining
   limitations. Completion requires actual evidence for all steps above; a passing
   checker or synthetic demonstration is not evidence of a solver defect.

Do not infer blow-up, singularities or engineering danger from numerical error.
An unverified purported OpenAI construction is not an assumption of this work.

## Execution authorization and revisions

The user subsequently authorized creation of this repository and operational
progress. Repository creation is no longer held for the initial review stage.
Upstream submissions remain conditional on the evidence requirements above.
Document new findings and changes of implementation plan here through commits;
do not quietly reduce the three-project scope or redefine completion.

This file versions the operational goal. The desktop goal text is separately
managed by the app; editing this file does not change the app's saved goal.

## Revision 127 — rotational-diffusion challenge to particle alignment

Added a checked tangent-plane stochastic director model for a prolate Jeffery
particle in an imposed `gamma~(1-t)^(-1)` extension. Constant rotational
diffusion changes the strong-strain angular scale to a Brownian-limited
`(1-t)^(1/2)` while still allowing variance to vanish in the ideal endpoint
limit. If `D_r~(1-t)^(-delta)`, the reduced-model boundary is `delta=1`:
subcritical diffusion growth permits asymptotic alignment, comparable growth
leaves a finite angular variance, and supercritical growth exits the
small-angle regime. The exact ODE branches are SymPy-checked in
`evidence/tests/rotational-diffusion-alignment.json`; assumptions and source
comparisons are in `docs/rotational-diffusion-alignment-cutoff.md`. This
strengthens a narrow kinematic bridge to anisotropic colloid directors but
does not establish molecular ordering, particle-center certainty, a viscosity
law, or transfer to the OpenAI field. Actual rotational diffusion, spatial
finite-size effects, full-sphere orientation statistics, and a physical cutoff
remain unmeasured. The original three-solver benchmark and completion audit
remain active. The three added unit tests pass, and the full verification
suite at this revision passed 159 tests with one skip and five subtests.

## Revision 19 — pressure-qualified alternative profile selection (2026-10-01)

Continue to audit the original `FinalSlowBase.actualProfile` without silently
replacing it. A separate Lean extension now selects a complete profile through
the prepared amplitude-bounded witness and proves the root pressure sign for
that alternate selection. Keep claims about this alternate object distinct
from claims about OpenAI's fixed choice. This is a new analytic workstream, not
a waiver of the manufactured-solution benchmark, three-project audit, justified
upstream reporting, or reproducible-publication requirements in revisions 1–18.

## Revision 20 — selected slow-base viscous/material-acceleration ratio (2026-10-01)

The qualified alternate selection now has a Lean-proved finite limit for the
ratio of viscosity times spatial Laplacian to material acceleration along its
natural material curve; at the pressure-qualified root this signed ratio has a
strictly negative limit while its magnitude tends to a strictly positive
constant. Keep this result scoped to the alternate
`FinalSlowBase.velocity` field. It is not yet transferred to the original fixed
`FinalSlowBase.actualProfile` or the assembled periodic field, and it does not
establish molecular alignment, particle-position certainty, a phase transition,
a viscosity law, singularity, or a solver defect. No upstream report follows
from this lemma alone. Continue the analytic transfer audit and full benchmark
goal without treating the negative signed ratio as reduced viscous effectiveness.

## Expanded scope authorized 2026-09-09

The user explicitly authorized starting work, upstream GitHub issues and related
technical discussion. Create exactly one project repository. Extend the impact
inventory to relevant numerical analysis, Scientific ML and fluid control claims;
record searched scope and unassessed areas instead of claiming universal coverage.
Develop the analytic reference problem and publish reproducible technical methods
as defensive disclosure. Adversarial evaluation means trying to falsify the
benchmark's claims and testing counterexamples, not treating projects as guilty.
The ambiguous phrase concerning analytical work is operationalized as deriving
and checking this manufactured solution, not promising to solve open regularity
problems. A paper/construction beyond the supplied proposal needs an identifiable
primary source before it can support a claim of a new discovery.

## Revision 3 — source located

The user pointed to OpenAI's repository. It is now identified and pinned in
`docs/openai-source.md`. Audit its actual definitions and constructive witness
before transferring the discovery to numerical impact claims. The existing MMS
is a calibration problem, not a substitute for auditing that construction.

## Revision 4 — analytic priority and self-falsification

The user explicitly cautioned against over-trusting simulation or amplifying our
own cached conclusions. Before interpreting numerical output, derive the governing
identity, assumptions, time/space conventions and discriminating predictions.
Distinguish an analytic implication, a source-code observation, an empirical
result and a proposed interpretation. Test alternatives that could invalidate
our interpretation. Re-read authoritative evidence when a conclusion changes;
prior summaries and successful runs are pointers, not proof. Simulations remain
permitted as supporting evidence and do not establish the new theorem, molecular
alignment, universal solver failure or engineering danger. Preserve the full
three-project and identified-construction scope.

## Revision 5 — September 2026 research refresh and hostile tube audit

Historical status at that stage; its withdrawn-transfer conclusion is
superseded by Revision 48 below.

The OpenAI source's actual-base second-derivative rate gives a base-field
Hessian exponent, but hostile review found no quantitative lower envelope for
the neighborhood where the assembled field equals that base. The previously
reported `Q^(Cstretch+39)` transfer to the assembled field is withdrawn. Keep
the generic packet algebra conditional until the equality-tube radius is
controlled. Recent related preprints are recorded with their distinct forcing
and regularity hypotheses. This revision adds evidence; it does not waive any
solver, upstream-audit, publication or completion requirement above.

## Revision 6 — skeptical particle-alignment audit and late-September refresh

The user proposed that a continuum blow-up or accelerating contraction could
make molecular positions more deterministic, align particles, or sharply reduce
viscous effectiveness. Treat this as a hypothesis, not as an interpretation
already implied by the theorem. Distinguish Eulerian profile narrowing from
Lagrangian material-line deformation and both from molecular orientation or
particle-position probability. The Navier–Stokes field alone provides no
particle ensemble or kinetic bridge. Duraiswami's 15 September leading-order
study reports only a fraction of a material-particle revolution per decade and
model-dependent liquid/gas continuum cutoffs before molecular scales; it also
omits the full pulse annulus and higher-order/full forced evolution. Use it as a
countercheck, not as a definitive physical simulation. Other newly checked
preprints concern conditional regularity, force-space density, and an unforced
positive-energy-defect search; each has different hypotheses and none supplies
the molecular implication. The detailed sources, numerical limitations and
falsifiable follow-up are recorded in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`. Preserve the
full project goal and current solver gates.

## Revision 7 — source-supported tube-radius route under audit

Historical status at that stage; the direct assembled cusp-ball result and
endpoint Hessian transfer were later completed in Revisions 47–48.

The refreshed OpenAI source exposes positive, scale-explicit inner support
radii for the actual initial copy waves, particular/signed annular terms, and
mean streams. This may yield a uniform assembled-field equality tube of radius
proportional to `sqrt(1-t)` and repair the withdrawn packet-radius exponent.
Treat this as a proof obligation, not as an achieved result: formalize that all
stage and direct sums inherit the common support hole on a complete tube and
verify the tube stays in every cited band/domain. The derivation and exact
source boundary are recorded in `docs/packet-constant-dependencies.md`. A
generic Lean lemma now proves the pointwise hole for any supported copy-family
sum; the all-stage assembly and tube-domain transfer remain open.

## Revision 8 — photon-fluid comparison and OpenFOAM sign source audit

The user renewed the photon-fluid idea, correcting that photons are discrete.
Record photon fluids as a separate, established analogue-model research track:
in selected nonlinear optical platforms, collective field intensity and phase
map to effective density and velocity. Published experiments report both
threshold-like suppression of optical obstacle drag and dispersive-wave
transitions. These results motivate a concrete full-wave-versus-reduced-fluid
comparison, but do not establish ordinary material-viscosity loss, molecular
ordering, or a realization of the OpenAI 3D Navier–Stokes construction. Keep
the model, observables, geometry and validity regime explicit; do not replace
the original solver-benchmark goal with this analogy.

A pinned-source audit now verifies the generated Foundation 13 MMS forcing
sign through the coded model callback, `fvModels().source(U)`, matrix
subtraction and Euler time assembly. This narrows the previous test limitation
to runtime integration and accuracy: static source algebra supports the sign,
but only an actual solver run can test the compiled case, pressure correction,
and requested convergence metrics. Preserve the audit manifest and never
promote it into a solver-run PASS.

## Revision 9 — first frozen OpenFOAM high-gradient matrix execution

The pinned Foundation 13 image became available and the frozen uniform-grid
runner started at source commit `0e0288f`. The n=16 and n=32 cases completed
with standard acceptance PASS but local-quality FAIL; their reference-only
FD2 floors already exceed the preregistered fine-grid threshold, so they are
underresolution observations. The n=64 case completed with both gates PASS.
The n=128 container began its first time step but produced no new log output
for more than 25 minutes while Docker inspection/top/stats calls also remained
pending. Preserve the live runner and all partial files; do not infer a solver
result or restart OrbStack from this observation. The n=128 and two smaller-dt
n=64 cases are still required before the protocol's matrix verdict. Completed
case archives, hashes and a cautious incomplete-matrix manifest are in
`evidence/of13-high-gradient-v2/`; the current report is
`reports/high-gradient-of13-v2-run-2026-09-28.md`. The new archive utility
accepts only complete cases and marks incomplete matrices UNCERTAIN.

## Revision 10 — analytic high-gradient identities and slow n=128 execution

The high-gradient MMS now records exact selected-point Frobenius-gradient and
vorticity values as lower bounds on the continuous maxima, without claiming
they are sharp global peaks. A reproducible derivation note and independent
SymPy-versus-Fourier formula comparison are checked in. Both formula tests pass;
they do not certify a numerical solver. The original Foundation 13 n=128 runner
remains live and has advanced to 0.024 seconds of the 0.05-second interval,
with a logged cumulative OpenFOAM `ExecutionTime` near 499 seconds at that
point (not a per-step timing). Preserve and reobserve the same run; do not
restart it or treat resource cost as a solver failure. The spatial/time matrix and its reproduction
verdict remain INCOMPLETE/UNCERTAIN.

## Revision 11 — independent finite-mode spectrum reference

The high-gradient MMS now has a separate exact finite-Fourier shell-energy
evaluator. It was cross-checked against resolved cell-centered FFTs for
N=4,8,16. That comparison caught a factor-of-two error in the first coefficient
table, which was corrected before accepting the tests. The corrected independent
shell sums pass against the sampled FFT. The formula and correction history are
documented in `docs/high-gradient-spectrum.md`; this is reference validation,
not a solver result. Meanwhile, the original n=128 OpenFOAM process remains live
at t=0.027s, so the spatial/time matrix is still incomplete. The older Gaussian
AMR sweep does not satisfy high-gradient v2; its dedicated three-budget v2 AMR
runner remains unexecuted, as does validation of any nonuniform-grid spectrum.

## Revision 13 — Python verification CI

A GitHub Actions workflow now runs the full Python suite on Python 3.12 for
pull requests and pushes to `main`. Both duplicate runs on the first PR update
passed; the branch filter now prevents duplicate feature-branch push/PR runs.
The same suite passed locally on Python 3.12 (74 tests and five subtests). Its
scope is analytic checks, gates, adapters and input generators; it does not run
CFD solvers. The successful run reported GitHub's Node 20 removal warning, so
the workflow now uses `actions/checkout@v5` and `actions/setup-python@v6` for
Node 24; the updated-action PR check passed. The hosted runner warned that
`ubuntu-latest` will migrate, so the workflow now pins `ubuntu-24.04`; the
resulting PR check also passed. At the latest observation the existing n=128
Foundation 13 job remains live at t=0.041s. Although its solver log did not
advance for roughly four minutes, a read-only Docker exec observed the
container's `foamRun` process in runnable state at 66% CPU and 12.9% memory;
this distinguishes active computation from a stopped container.

## Revision 12 — high-gradient AMR input-generation checks

Three new unit tests exercise the high-gradient AMR case generator: sensor
creation/update and boundary correction, refinement limits/budget, and the
minimum refine interval needed to initialize the sensor. They pass but do not
test OpenFOAM's runtime adaptation or mesh-level/budget behavior. The original
uniform n=128 process remains live and has reached t=0.027s; uniform/time and
high-gradient AMR solver matrices remain incomplete.


## Revision 14 — late-September literature and upstream refresh

A new dated source audit is recorded in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`. Rechecked
related work includes the conditional regularity result for analytic forcing,
the latest version of force-space density results, and a neural-forcing
proposal. None verifies molecular alignment, material-viscosity collapse, or
an OpenFOAM/SU2/PhysicsNeMo defect. They sharpen the next falsification tasks:
compare the OpenAI force against analyticity/local-vanishing hypotheses; state
topologies when testing robustness; and require fixed-force replay plus exact
time/spectrum contracts for numerical candidates. SU2's active target-time PR
and PhysicsNeMo 26.08 mesh calculus/epistemic uncertainty/CFD surrogate
benchmark additions are audit leads, not confirmed defects or solver evidence.
The current OpenFOAM Foundation 13 run stays pinned to its existing image and
continues separately; any patch-level replication must get its own source and
image manifest. No scope or completion gate is relaxed.


## Revision 15 — n=128 completion and temporal runner stall

The original OpenFOAM Foundation 13 uniform runner completed n=128, dt=0.001
at t=0.05 with exit code zero, 50 recorded steps, 50 five-iteration PIMPLE
convergences, and the `End` marker. Independent acceptance analysis reports
standard acceptance PASS and local quality PASS; its original case tree was
archived and content-verified at
`evidence/of13-high-gradient-v2/README-n128-archive.md` (the 169 MiB tar is published as a checksummed, split Zstandard package because GitHub rejects a single file above 100 MiB). The manifest now has
four of six uniform cases complete, with the full matrix still
INCOMPLETE/UNCERTAIN because both smaller-dt n=64 cases remain incomplete.

The automatically started n=64, dt=0.0005 case reached `Time = 0.018s` on its 36th step; 35 earlier steps have
PIMPLE convergence records, each in five iterations. Its log stopped changing
at 2026-09-28 11:51:31 JST. At a later check no `foamRun` process was observable;
the host runner and Docker CLI had zero CPU, and Docker/OrbStack control commands
were unresponsive. The host runner was terminated to prevent a hung sequence
from retaining the lane; its partial input/logs remain intact with no exit.json
and no solver verdict. A Docker stop request was issued but has not returned, so
container removal and daemon health are unverified. No global OrbStack restart
was attempted. A different queued task was told the lane has no observed solver
process but Docker state could not be confirmed. Resume only after container/daemon
state can be queried reliably; preserve this partial run and restart that frozen
case only from a clean, verified container after recording the prior attempt.

## Revision 16 — related unforced-Euler construction and gradient sensitivity

The OpenAI announcement links a separate unforced 3D Euler construction. Its
primary paper explicitly builds iterated localized oscillatory packets whose
velocity increments carry an inverse-frequency factor while phase
differentiation restores an order-one gradient increment. Record this as a
cross-problem analytic reason to keep local-gradient acceptance separate from
aggregate velocity error. Euler has no viscous stress, and this construction
does not validate molecular alignment, a material-viscosity change, or the
forced Navier–Stokes numerical cases. The primary-source distinction and exact
scope are documented in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`; the frozen
benchmark and three-project audit scope are unchanged.

## Revision 17 — acceptance parser false-pass control

Adversarial self-testing found that the OpenFOAM standard-acceptance parser
could accept a synthetic log with the right record count and final time but
duplicate/skipped intermediate time labels. The checker now validates every
logged timestamp against the frozen fixed-step schedule and has a regression
test that rejects the counterexample. A hash-checked audit of all four complete
high-gradient v2 archives confirms their existing logs follow the schedule;
their solver verdicts do not change. Classify this as our evaluation-harness
bug, not an upstream solver defect. Details and the rerunnable audit artifact
are in `reports/internal-gate-self-audit-2026-09-28.md` and
`evidence/tests/high-gradient-time-sequence.json`.

## Revision 18 — rerunnable PhysicsNeMo odd-width audit

The targeted PhysicsNeMo spectrum defect is already tracked upstream in
Issue #2007 with fix PR #2008, so no duplicate post is warranted. The local
audit previously retained outputs and source hashes but lacked its exact
reproducer. Added a CPU script that loads the unmodified `power_spectrum.py`
directly, checks even/odd axis-mode controls and deterministic transpose
symmetry, and writes source-hashed evidence. The current main/release source
file hash still matches the audited defective implementation; PR #2008 remains
the existing remediation path. The exact PR head was independently run through
the same even/odd and transpose controls and suppressed the counterexample;
that does not substitute for its full upstream CI/test suite or merge review.
Full upstream-suite validation remains open.

## Revision 19 — conditional support-hole cusp tube and source-bound correction

The similarity equation now has an explicit classical geometric estimate for
the full spatial tube of radius `c*sqrt(1-t)` around the selected axis curve.
Writing `eta=z/q^(1/2-h)`, the normalized map
`F(eta)=eta*(1-eta^2)^(-(1/2-h))` has derivative bounded below by `1-2h`;
this controls axial tube displacement, chart margin, and the localization
plateaus once a common positive inner-support coefficient is supplied. Exact
algebraic identities are checked and included in archived report replay. This
does not yet prove that every selected primitive, cutoff sum, spatial curl and
final localized velocity share the required inner hole. A source audit also
corrected an earlier misdescription: `SublevelShrinkingSupport` is an outer
support bound, while inner support comes from separate annular lower bounds.
Do not promote the conditional cusp geometry to a Lean-checked assembled-field
theorem, a numerical packet certificate, or a molecular conclusion.

## Revision 20 — locked replay restored on the current commit

The current NumPy-2.5.3 evidence metadata mismatch was resolved by regenerating
the analytic reference artifact under the repository's locked NumPy 2.5.2
environment, preserving the earlier failed replay as historical evidence. A
fresh tracked-only export at commit `03ce175` reproduced all 113 compared
report/test files exactly; all 26 report steps and 85 tests passed. This proves
the bounded Python postprocessing replay, not solver/training/Lean reproduction
or completion of the support-hole-to-final-field theorem. The saved run and
hashes are under `evidence/clean-export-2026-09-28-cusp-tube/`.

## Revision 21 — late-September source and research check

The current primary-source refresh confirms the OpenAI NavierStokesAndEuler
repository still reports zero `sorry` declarations and formalizes the forced
Navier–Stokes alternatives (C)/(D), plus unforced Euler results; Lean checking
validates the encoded statements against Lean's kernel but does not by itself
establish that the paper's encoding matches every intended analytic/physical
claim. The Clay Institute's 11 September statement says the problem has
"apparently been settled" and that evaluation/credit will be deliberately
unhurried. No newer official evaluation was found in this pass.

New September papers/preprints include a forced-data distribution result
(arXiv:2609.10262), a neural-forcing candidate/certification proposal
(arXiv:2609.23934), and a shell-model cascade study (arXiv:2609.26790).
They extend mathematical discussion of force topology, fixed-force validation,
and scale transfer. The latter is a shell-model result, not a theorem about
molecular trajectories. None establishes particle alignment, deterministic
molecular positions, or a velocity-induced collapse of material viscosity;
those remain separate physical hypotheses requiring a kinetic/constitutive
model and experiment. Numerical simulation may itself be wrong or
under-resolved and is retained only as conditional evidence.

The current OpenFOAM Foundation 13 matrix remains incomplete: four of six
uniform cases have complete archives; n=64, dt=0.0005 has a preserved partial
log with 36 observed steps and no verified container exit, while dt=0.00025
has not run. A zero-CPU orphan Docker client and a long-running `docker info`
call remain visible, with no `foamRun` process observed. Container/daemon state
is unknown. Do not restart OrbStack or disturb unrelated containers without
explicit authorization; resume only after read-only container state queries
work, preserving the partial evidence.

The concrete result relevant to the initial proposal is still bounded: the
completed n=16/n=32 cases pass standard acceptance but fail local-quality
acceptance, whereas n=64/n=128 pass both. This is a resolution-sensitive
benchmark outcome, not a solver defect or blow-up signal. Finish the frozen
time-refinement matrix and dedicated AMR budgets, then complete the SU2 and
PhysicsNeMo audit before considering any additional upstream report. Recheck
existing issue/PR status first to avoid duplicates.

## Revision 22 — stage-uniform primitive support hole

A pinned-source reread narrowed the remaining analytic gap. The copy,
particular, signed and mean correction primitives admit a shared positive
inner-hole coefficient

    c0 = min(leftRadius/(4*sqrt(2)), patch.a/4) > 0,

where `leftRadius` and `patch.a` are the selected positive source constants.
The initial physical copy annulus supplies the first term; every positive
particular/signed stage lies outside the same nominal active annulus; and the
mean stream/direct families use the fixed initialization-patch radius. This
corrects Revision 19's implication that selected-uniform primitive constants
were still missing. The coefficient is existential and non-numerical.

The remaining analytic target is now the passage from these stage-uniform zero
regions to the complete selected weighted series, its spatial curl, direct
field sum, periodic spatial localization and final time activation on a
quantitative cusp tube. Existing source lemmas provide component decompositions
and per-stage zero germs, but no end-to-end theorem has yet been checked for the
final activated velocity. Keep the packet estimate conditional, do not claim a
Lean proof of the tube, and do not infer molecular alignment or constitutive
viscosity change. The exact source map and corrected status are recorded in
`docs/packet-constant-dependencies.md` and
`docs/support-hole-tube-geometry.md`.

## Revision 23 — compiled exterior-transfer theorem and remaining tube geometry

The actual selected construction now has a compiling Lean extension at
`verification/SupportHoleAssembly.lean`. Its theorem composes the exterior
identities for stage zero, all positive potential stages and all direct stages
with cutoff local finiteness, spatial curl, periodic localization and late-time
activation. Under explicit exterior, zeroth-cutoff plateau, spatial-plateau and
late-time hypotheses, the final activated velocity is eventually equal to
the selected smooth-base velocity.

The pinned source archive is retained under `work/` with SHA-256
`9832374e0926a8a9dfb19699e50bf8ddb957fb9e961e7cc85b8fb689eda2b1b7`. Lean
4.34.0-rc2 and pinned mathlib commit
`85e3a25e006c35636f0e53b0e9296caca2685bc0` were obtained from a verified source
archive and populated Lean cache. The five imported upstream modules built
successfully (3,679 jobs), and the extension compiled with `lake env lean` in
the upstream project environment. This verifies the conditional exterior
equality theorem. It does not verify the whole moving cusp-tube inclusion: the
quantitative chart, ball, sublevel and plateau inequalities have not yet been
formalized and connected to its hypotheses. No numerical tube radius or
physical/molecular conclusion is claimed.

The initial copy and mean terms were separately checked against the same
annular inner-hole mechanism; source assembly lemmas show their exterior zero
behavior, so they are not an independent obstruction. The remaining proof
target is specifically to formalize the whole-tube geometry and instantiate
the checked transfer theorem uniformly for every point in that tube.


## Revision 24 — radial-hole bridge and actual exterior scale

The Lean extension now includes
`selected_inner_exterior_velocity_germ_of_radial_hole`. It uses the source
identity `physicalPosition[0]^2/(2*physicalQ)=cartesianChart.2.1` to convert a
strict inner-radius condition into exclusion from the actual active annulus,
then applies the compiled selected-field equality theorem. Its explicit
remaining hypotheses are `q<Q_res`, the zeroth-cutoff plateau, spatial
localization plateau, and late-time activation.

A scale audit found the exterior cutoff must be stated more tightly than the
physical construction's `qbig`: the source defines
`residualBand=firstBand+1` and `qbig=2*ChartScales.Q(residualBand)`, while
`ActualExteriorPrefix.exteriorDomain` requires
`q<ChartScales.Q(residualBand)`. Accordingly, the moving-tube condition was
corrected to `tau<s0*Q_res`. The whole-ball proof deriving this chart bound
and all plateaus for every tube point is still not formalized. This narrows a
concrete precondition; it does not change the conditional status of the
cusp-tube claim.

The same n=64, dt=0.0005 OpenFOAM attempt was rechecked on 2026-09-28: its
`log.foamRun` still has its 11:51:31 timestamp, host PID 91031 is still waiting,
and an 8-second read-only query through OrbStack's own Docker CLI timed out.
No `foamRun` process appeared in the host process listing. Container state is
still unknown; no solver or daemon restart was attempted.


## Revision 25 — Lean-checked similarity-chart upper bound

`verification/SupportHoleAssembly.lean` now formalizes
`physicalQ_time_identity` by pulling the pinned source's implicit similarity
equation back to Cartesian spacetime. It also proves
`physicalQ_le_of_eta_margin`: under `|eta|<=beta<1`, the physical similarity
scale satisfies `q<=(1-t)/(1-beta^2)`. This verifies the chart upper-bound
step used to place a tube inside `q<Q_res`, once a uniform eta margin is
available. The remaining geometric proof is to derive that margin for every
point in each shrinking spatial ball using the derivative lower bound for the
normalized axial map, then combine radial and localization bounds. No solver or
physical conclusion follows from this analytic lemma.

## Revision 26 — axial-coordinate margin formally connected

Pinned-source calculus now gives a compiled fixed-time spatial Lipschitz bound
for the normalized axial similarity coordinate:

    |eta(tau,z)-eta(tau,z')| <= |z-z'| / ((1-a)*tau^((1-a)/2)).

The axis normalization was separately derived from the forward similarity
equation, yielding `coordinateEta_axis_center`. These combine in
`coordinateEta_margin_of_axial_radius`: if an axial point lies within
`delta*(1-2h)*tau^((1-2h)/2)` of the prescribed axis center, then its eta is
bounded by `|eta0|+delta`. This is a rigorous conditional bridge and removes the
need for a hand-waved continuity radius. It does not yet establish that a full
three-dimensional moving ball satisfies that axial hypothesis, or the radial
sublevel and all cutoff/localization plateau inequalities, so no whole-tube
instantiation or packet transfer is claimed.

The follow-up lemma `coordinateEta_margin_of_sqrt_axial_radius` now discharges
the analytic scaling factor for `tau<=1`: an axial displacement bounded by
`c*sqrt(tau)` implies `|eta|<=|eta0|+c/(1-2h)`. It uses
`tau^(1/2)=tau^D*tau^h` with `D=(1-2h)/2`, so `tau^h<=1`. This still assumes
an axial-coordinate displacement bound; converting a full 3D Euclidean ball
to that premise, plus the remaining tube sublevel and cutoff conditions,
remains open.

The pinned upstream `lake build` completed successfully (11,424 jobs) against
the retained OpenAI/NavierStokesAndEuler snapshot. The published Comparator
challenge modules emit explicit `sorry` warnings, while `ComparatorSolution`
reports only `[propext, Classical.choice, Quot.sound]` for the two exposed
Navier--Stokes breakdown theorem declarations. The four new local chart
lemmas also report only these standard Lean axioms; logs are in
`evidence/openai-lean-2026-09-30/`. These outputs are scope-limited and are not
independent peer review. The September 28 OpenFOAM
manifest still shows four of six high-gradient cases complete; the half-step
case remains archived=false at 36 records/35 converged steps and the quarter
step is unstarted. The container/process state is not reasserted here.

## Revision 27 — late-September physical interpretation check

A current-source refresh found a new explanatory preprint by Lei and Ren
(arXiv:2609.35406, posted September 28) on the profile-construction part of
OpenAI's paper. The refreshed research note distinguishes its axial slender-core
scaling from molecular alignment and records the paper's componentwise Reynolds
numbers: angular growth does not remove radial viscous balance. It also tracks
Clay's September 11 position as “apparently settled” with evaluation and credit
assignment deliberately unhurried. See
`docs/recent-developments-2026-09-30.md`. This adds a Lagrangian particle-track
workstream as a separate, testable question; it does not revise any benchmark
PASS/FAIL or imply physical blow-up.

## Revision 28 — current-main PhysicsNeMo defect recheck

A live refresh found PhysicsNeMo main had advanced since the prior inventory.
The exact new main still reproduces tracked odd-width Issue #2007, while current
PR #2008's head passes the same CPU controls; the PR remains open and behind
main. Fresh outputs, source hashes, inventory, and a bounded update to the
existing PR are recorded in `reports/physicsnemo-refresh-2026-09-30.md`. No
duplicate issue was filed. The full three-project scope remains active.

## Revision 29 — one temporal OpenFOAM row completed

The preserved v2 `n=64, dt=0.0005` case now completes all 100 steps with 100
PIMPLE convergence records, endpoint fields and `End`; standard acceptance and
all five preregistered local-quality metrics pass. A first post-run false
rejection exposed a substring-count bug in the new runner (`ExecutionTime` was
mistaken for a time-step row). The solver output was preserved and an
independent line-anchored validator then confirmed and archived it. The
regression fixture now includes `ExecutionTime`/`ClockTime` lines. A current
cross-run manifest records five of six rows complete; `dt=0.00025` remains
unstarted, so the overall matrix remains INCOMPLETE/UNCERTAIN. See
`reports/high-gradient-of13-temporal-addendum-2026-09-30.md`.

## Revision 30 — uniform matrix complete; discrepancy not observed

The second n=64 temporal row (`dt=0.00025`) completed all 200 steps and passed
the frozen standard and local-quality gates. The additive current manifest now
records all six uniform-grid rows complete, while preserving the five-of-six
snapshot and the immutable original base manifest. A hash-checked three-step
n=64 comparison found matching cell centers and non-time inputs. The endpoint
difference trend is descriptive and does not certify a temporal order; the
exact-velocity error does not decrease monotonically across these three steps.
The matrix rule is NOT_OBSERVED because n=64 and n=128 both pass standard and
local-quality gates. This weakens the original specific discrepancy hypothesis
for this frozen case; it is not a general solver guarantee. Dedicated AMR
budgets remain required and unrun, so the broader verification goal stays
active. See the temporal addendum report and comparison artifact.

## Revision 31 — high-gradient AMR and fixed-mesh controls completed

The three frozen high-gradient AMR budgets completed. The 4096 budget did not
refine; 5000 produced 16,640 cells and 100000 produced 101,760. Exact
budget-blocked candidate counts were not retained. Event logs show the
cap100000 case selected 12,416 candidates at 16,640 cells, transiently reached
103,552, then unrefined 256 split points and ended at 101,760. Pinned source
selection adds a complete refinement-level group before checking the allowance;
the computed 11,908-candidate allowance therefore aligns with the 508-candidate
whole-level excess. This observed event matches approximate-cap semantics and
does not support a defect report. Fixed-final-mesh runs
initialized from the analytic field reduced velocity error from 37.0% to 1.88%
and from 40.1% to 0.483% on the 5000/100000 meshes. This supports an
adaptation-history/remapping contribution, while leaving individual sensor,
flux-correction, remapping and projection mechanisms unresolved. AMR verdicts
remain UNCERTAIN; no upstream defect report is warranted yet. Raw case trees
remain locally under `work/`; tracked compact summaries are the two AMR v2
manifest artifacts cited in the temporal addendum. The project goal remains
active pending component-level diagnosis and the remaining cross-solver and
analytic work.

## Revision 32 — AMR continuity residual discriminator

Read-only OpenFOAM post-processing of `div(phi)` on both high-gradient AMR
endpoints and their same-final-mesh fixed controls found volume-weighted RMS
continuity residuals roughly 1e-11 or less after normalization by `Urms/(2*pi)`.
The solver logs' maximum local continuity error is below 3e-15 for all four
cases. The 37–40% AMR-path velocity error therefore is not explained by a large
discrete mass-flux imbalance at the endpoint or in the reported time-step
continuity metrics. Momentum/field remapping and transient local effects remain
unresolved; this diagnostic neither proves the solver correct nor establishes
an upstream defect. The hash-linked post-processing output is
`evidence/of13-high-gradient-amr-flux-balance-2026-09-30.json`.

## Revision 33 — analytic counterexample for alignment-to-viscosity inference

An exact affine incompressible Navier–Stokes solution on R^3 now separates
material-line alignment from constitutive viscosity: separations align toward
the axial direction while the viscosity coefficient remains arbitrary and
constant, and the viscous force is identically zero. This falsifies the
standalone inference from alignment to reduced viscosity, but does not test a
specific constructed profile or finite-energy flow. The derivation and
symbolic negative controls are in
`docs/affine-alignment-viscosity-counterexample.md` and
`evidence/tests/affine-alignment-counterexample.json`. This result does not
reduce any solver, three-project, or upstream-audit requirements.

## Revision 34 — nonzero viscous balance during axis alignment

The analytic hypothesis check now includes the classical Burgers vortex. Its
axis deformation aligns infinitesimal directions exponentially, while away
from the axis its nonzero azimuthal viscous diffusion exactly balances
azimuthal advection; the constitutive viscosity remains constant. The symbolic
cylindrical-equation and deformation checks are recorded in
`docs/burgers-vortex-alignment-viscous-balance.md` and
`evidence/tests/burgers-vortex-balance.json`. This is a stronger counterexample
to inferring reduced relative viscosity from alignment alone, but its
unbounded-domain idealization does not establish behavior of the selected
OpenAI construction or molecular matter.

## Revision 35 — off-axis material deformation in Burgers vortex

The Burgers-vortex calculation now follows an off-axis material trajectory,
not only the axis linearization. Its exact cylindrical flow map has a radial
to-azimuthal shear coefficient with a finite long-time limit; thus infinitesimal
separations with nonzero axial component still align as `O(exp(-3 gamma t))`.
Along that same trajectory the nonzero azimuthal viscous term continues to equal
the azimuthal advection term at every finite time. The extended derivation and
symbolic artifact are in `docs/burgers-vortex-alignment-viscous-balance.md` and
`evidence/tests/burgers-vortex-balance.json`. This closes the earlier gap of
demonstrating deformation only on-axis and term balance only off-axis, within
this exact idealized solution; transfer to the selected OpenAI profile remains
unproved.

## Revision 36 — adversarial regression coverage for the analytic check

The Burgers-vortex verifier now checks radial and axial vector Laplacians,
pressure-gradient compatibility, and all three steady momentum components. Its
off-axis alignment claim is tested by the symbolic limit of the squared
transverse-to-axial displacement ratio, rather than by a copied expected
factor. A unit-test subprocess runs the verifier in a temporary directory and
asserts its equations, nonzero viscous term, closed-form shear limit, alignment
limit, and deliberate sign-error controls. This is regression protection for
the stated analytical scope, not independent formal verification.

## Revision 37 — verify variational equation and axis alignment limit

The final tautological axis-rate check was replaced by a direct symbolic
residual of `F' - (grad u)F` and the limit of the squared transverse-to-axial
ratio for arbitrary initial displacement with nonzero axial component. The
automated test asserts both axis and off-axis limits are derived as zero. This
closes a verification-quality gap in the analytic counterexample artifact; the
result remains confined to the classical idealized Burgers vortex.

## Revision 38 — exact position probabilities for a tracer ensemble

The exact Burgers-vortex material flow map now transports an imposed isotropic
Gaussian tracer ensemble. Its physical Jacobian is one; transverse variance
contracts while axial variance expands, preserving covariance determinant,
peak density and differential entropy. Probability in a fixed-radius infinite
axis tube tends to one, but probability in a fixed finite cylinder decays like
`sqrt(2/pi)*(L/sigma)*exp(-2*gamma*t)`. Symbolic identities and the regression
check are in `docs/burgers-vortex-position-probability.md`,
`tools/check_burgers_vortex_tracer_probability.py`, and
`evidence/tests/burgers-vortex-tracer-probability.json`. This sharpens the
observation-geometry distinction for passive tracers only; it is not a
molecular, stochastic, finite-energy, or OpenAI-profile result.


## Revision 39 — live upstream disposition rechecked

The three upstream targets were rechecked read-only against GitHub at
2026-09-30 10:31:46 UTC. OpenFOAM Foundation 13 and SU2 master still match the
audited commits; SU2 discussion #2890's maintainer response and BDF2 follow-up
are both verified by GraphQL node lookup. PhysicsNeMo issue #2007 remains open;
PR #2008 is open, behind, review-required, and diverged from current main by
9 main-ahead / 2 PR-ahead commits. No duplicate reports were warranted. The
structured status snapshot is
`evidence/upstream-refresh/live-status-2026-09-30.json`; these statuses are
time-bounded and do not replace full framework testing or cover every external
issue tracker.

## Revision 40 — finite-fiber literature boundary added

Added a source audit of the 2026 JFM numerical study of finite flexible fibers
in a prescribed Stokes-flow Burgers-like analogue. Its centered-fiber
alignment result is relevant to finite-object orientation, while its model is
not the exact Burgers/Navier–Stokes field and supplies no molecular,
constitutive-viscosity, phase-transition, experimental, or OpenAI-profile
conclusion. Added the bounded result to the impact-scope matrix and the
2026-09-30 development note; see `docs/fiber-vortex-literature-audit.md`.
This updates the literature boundary only and leaves numerical solver verdicts
unchanged.

## Revision 41 — molecular rheology and temporal archive recheck

Rechecked both frozen n64 temporal-addendum archives: their SHA-256 digests
match their manifests, each archived solver log contains the `End` marker,
and the manifests report 100/100 (`dt=0.0005`) and 200/200 (`dt=0.00025`)
converged steps with both gates passing. Kept these as row-level reproduction
evidence, not an asymptotic temporal-order or general defect claim. Added
Jadhao–Robbins' squalane result to the impact matrix: molecular alignment
saturates after only about a threefold viscosity decrease, while thinning
continues. This supports a material-specific alignment/rheology connection
but does not bridge the OpenAI continuum profile to molecules. See
`docs/recent-developments-2026-09-30.md` and
`reports/impact-scope.md`.

## Revision 42 — exact-reference temporal comparison

Replayed the archived n64 v2 OpenFOAM temporal triplet against the exact MMS
endpoint. All three rows pass both acceptance gates, with velocity errors
0.00478066, 0.00478409, and 0.00479049 as dt is quartered. The exact-error
trend is effectively flat/slightly increasing; endpoint field-difference
order is about 0.499. Recorded hashes, input/grid correspondence, and full
interpretation in `evidence/tests/high-gradient-of13-v2-temporal-comparison-2026-09-30.json`
and `reports/openfoam-v2-temporal-comparison-2026-09-30.md`. No asymptotic
time-convergence or general defect claim follows; the local acceptance
blind-spot remains NOT_OBSERVED.

## Revision 43 — PhysicsNeMo pointwise derivative audit

Added a hash-linked checker that reopens all five fixed-budget PhysicsNeMo
archives and validates each derivative report against its checkpoint and
evaluation array. On 262,144 samples per case, sampled peak-magnitude errors
are 0.91–0.97%, while maximum pointwise derivative-field differences,
normalized by the exact sampled peak, are 1.20–1.26%. This shows why peak
level and pointwise field metrics should be reported together. Added the
reproducible JSON and a report clarifying that these are finite-sample
observations, not continuous bounds; all PhysicsNeMo acceptance verdicts
remain UNCERTAIN. See `reports/physicsnemo-pointwise-gradient-audit-2026-09-30.md`.

## Revision 44 — cross-solver matrix and AMR evidence audit

Replayed OpenFOAM archive chronology, all five SU2 diagnostic archives, SU2's
n64 time triplet and aggregate standard review. The three solver coverage
states are now summarized together in
`reports/solver-matrix-coverage-2026-09-30.md`: OpenFOAM's 4-grid/3-dt uniform
matrix is complete with fine-grid blind-spot `NOT_OBSERVED`; SU2's 3-grid/3-dt
matrix is complete but no run satisfies all aggregate/residual checks; and
PhysicsNeMo's three spatial densities plus 5/9/17 collocation-node experiment
is not a time-step study and remains UNCERTAIN.

The AMR pilot and two fixed-final-mesh controls previously existed only as
ignored work trees and summary manifests. Added five raw archives (~49 MiB),
archive/tree hashes, a verifier and a current cross-run manifest pointer.
Verified every archive entry against its source work tree, all archive hashes,
and case counts. Kept the AMR verdict UNCERTAIN: batch adaptation exceeded the
nominal 5,000-cell setting to 16,640 cells and the 100,000 setting to 101,760;
candidate counts and nonuniform spectra remain unavailable. Fixed-mesh
controls narrow the discrepancy toward adaptive history without isolating
which remap/flux/sensor component is responsible. No new upstream issue is
warranted by this evidence.

## Revision 45 — OpenFOAM runtime provenance and fresh reproduction guide

Replaced the stale OpenFOAM runtime instructions that still described the
uniform matrix as in progress. The guide now separates archive replay from a
fresh solver run and provides commands for the uniform matrix, AMR cases, and
fixed-final-mesh controls. Added the exact image ID, platform, Foundation DEB
hash, Dockerfile/build-log/package-inventory hashes to the current cross-run
manifest. The Ubuntu apt index was not snapshot-pinned, and source-to-binary
equivalence is not established; these remain explicit reproduction limits.
Verified all five published AMR/remap archives and trees, valid JSON, clean
diff formatting, and 91 tests (plus 5 subtests).

## Revision 46 — independent kernel check of the analytic ratio

Re-ran the pinned Lean extension from the current source and confirmed its
output is byte-identical to the recorded Lean log. Then exported the actual
candidate viscous/acceleration ratio, its `Z>0` specialization, and the exact
pressure-moment threshold with lean4export, and independently checked the
dependency closure with nanoda. Two runs checked 85,455 declarations with zero
typechecker errors; the 949,729,487-byte export hashes matched. Added a guarded
reproduction script and compact hash manifest; the generated proof closure
stays under ignored `work/`, not in Git. This strengthens confidence in the
conditional analytic theorem but does not prove its local pressure condition
for the upstream `actualProfile` choice. No molecular or constitutive-viscosity
claim is added.

## Revision 47 — conditional uniform terminal cusp-ball transfer

Formalized center decay at `tau=0`, combined it with the fixed-time spatial
ball/chart estimates, the selected construction's physical exterior, cutoff
plateaus, and the actual field-germ theorem. The pinned Lean run proves that
for every fixed axis coordinate in `(-1,1)`, an admissible positive ball-radius
coefficient and eta margin exist, and then an existential `tau0>0` works for
every time `0<tau<tau0` and every point in the shrinking `c*sqrt(tau)` ball.
Evidence is `evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/`; details and
limits are in `docs/support-hole-tube-geometry.md` and
`reports/openai-support-hole-assembly-audit.md`. This is a conditional
continuum local-germ equality, not a finite-size material packet, molecular
alignment, phase transition, or viscosity theorem. It adds no solver defect
finding; solver acceptance claims remain separately gated by the benchmark.

## Revision 48 — endpoint Hessian rate transferred onto the cusp ball

Extended the pinned Lean proof to show that the entire moving cusp ball
eventually lies in any prescribed endpoint neighborhood, then transferred the
upstream actual-base second-jet rate to the actual selected field throughout
that ball. The result is an existential full-spacetime bound `C*q^(-40)` on a
parameter-dependent terminal interval; all ten audited declarations use only
`propext`, `Classical.choice`, and `Quot.sound`. The repeatable source, log,
image and declaration audit are in
`evidence/openai-lean-2026-09-30-cusp-hessian-v6/manifest.json`.

This supplies a field-equality-ball radius proportional to `sqrt(1-t)`. If its
Hessian bound is restricted to spatial directions and the classical packet
comparison is applied, the conditional shrinking-initial-packet exponent is
`Cstretch+39`, in `[42.9999995,43)`. Neither spatial restriction of the local
jet nor nonlinear packet comparison is jointly formalized in this extension;
the estimate remains non-effective and does not show fixed-size packet
misalignment, particle alignment, molecular determinism, phase transition or
reduced viscosity. No new upstream solver defect is established.

Validation: the pinned Lean checker and axiom audit pass; the symbolic packet
algebra checker passes; repository tests pass (`98 passed, 5 subtests`). A
whole-repository pytest invocation also traverses preserved checkouts under
`work/` and encounters duplicate-module collection errors, so the validated
scope is explicitly `pytest tests`.

## Revision 49 — re-audit of the alignment hypothesis and run chronology

Replayed the symbolic directional-probability, Jeffery-bridge and packet-bound
checks against the new packet analysis. The selected continuum deformation has
singular values `Q^(C/2), Q^(C/2), Q^(-C)` and determinant one. Under an imposed
isotropic distribution of *infinitesimal separation directions*, the
probability of lying within any fixed nonzero angle of the axis tends to one.
The separate Gaussian position comparison keeps peak density and volume
unchanged, while probability in a fixed finite cylinder tends to zero. This
supports only continuum tangent-direction alignment, not molecular positions,
finite-particle alignment or a viscosity transition. The Jeffery calculation
is a separate ideal director model with its own uniform-strain and
zero-inertia assumptions.

Also cross-checked the apparent OpenFOAM temporal-run contradiction: the
previously stalled `n64, dt=0.0005` attempt is retained as an incomplete
historical attempt, while a later validated replay completed 100/100 steps;
the `dt=0.00025` case completed 200/200. The current cross-run manifest has
six complete uniform cases, zero incomplete rows, and blind-spot verdict
`NOT_OBSERVED`; the archived time-sequence audit passes. The earlier stall note
remains valid historical evidence and is superseded for current matrix status.

Refreshed the upstream identity check: OpenAI's target is a Lean 4
formalization repository at `openai/NavierStokesAndEuler`, pinned work uses
Lean 4.34.0-rc2, and its repository license is Apache-2.0. GitHub Issues are
disabled there; moreover this work establishes no implementation defect to
report. Current benchmark PR #2 now carries the endpoint Hessian transfer and
its Python CI passes. PR #3 remains a separate pytest-discovery follow-up.

## Revision 50 — current upstream issue-scope refresh

Re-read the live issue/PR inventories and default-branch heads for OpenFOAM
Foundation 13, SU2, PhysicsNeMo, and the OpenAI Lean repository. The detailed
snapshot and relevance decisions are in
`reports/upstream-status-2026-10-01.md` and
`evidence/upstream-refresh/live-status-2026-10-01.json`. No new report is
warranted: OpenFOAM's open items do not match the exercised paths; SU2's
time-contract observations overlap its existing discussion/issue; and
PhysicsNeMo's relevant odd-width spectrum and non-periodic derivative behavior
already have open tracking items, while the tested workload is even-width,
periodic, and uses autograd. A pinned MLP import smoke did not hit the separate
open PhysicsNeMo Warp custom-op issue; that smoke is not a reproduction of its
deforming-plate entry point. OpenAI's source repo is Apache-2.0 Lean source with
GitHub Issues disabled, not a CFD solver repository. The full three-solver
benchmark goal remains active; no broad completion is inferred from this
inventory refresh.

## Revision 51 — independent check of cusp-Hessian transfer

The exact v6 `SupportHoleAssembly.lean` source was exported and independently
checked by nanoda in the pinned offline checker container. Nanoda checked
85,487 declarations with zero typechecker errors and reported one pretty-printer
error (`Unable to print axioms`); Lean separately printed and matched the
permitted axiom set for all ten selected declarations. Run provenance and
artifact hashes are in
`evidence/lean-verification/support-hole-nanoda-2026-10-01.json`, with the
reproduction script at `runtime/lean-verification/check_support_hole_nanoda.sh`.
The raw 906 MiB export remains local under `work/`, identified by SHA256. This
independent proof-term check strengthens confidence in the formalized
conditional cusp-ball/Hessian result; it does not validate the pinned upstream
construction, formalize the classical packet comparison, or establish a
particle, molecular, phase-transition, or viscosity consequence. The benchmark
completion goal remains active.

## Revision 52 — local spatial-jet restriction lemma

Added `verification/SpatialJetRestriction.lean`, proving that at a locally
`C^m` spacetime point the fixed-time spatial iterated derivative norm is at
most the full spacetime derivative norm. The proof reduces local smoothness to
a neighborhood and uses the norm-one embedding `v -> (0,v)`. The pinned Lean
4.34.0-rc2 elaboration exited 0 in the digest-pinned offline checker; its source
hash and invocation are recorded in
`evidence/lean-verification/spatial-jet-local-restriction-2026-10-01.json`.

This is a standalone generic lemma. No `#print axioms` audit was captured, and
the attempted composition with the selected-field cusp-ball Hessian theorem
did not produce a checked module: the initial attempt had a Lean module/import
setup failure, and the local Docker/OrbStack service then stopped responding
to bounded read-only status queries. No mathematical counterexample was
observed, but the composition is unverified. The `Cstretch+39` estimate
therefore remains conditional on this composition and the classical nonlinear
packet argument. It only concerns a shrinking initial packet and implies no
molecular ordering, phase transition, particle-position certainty, or
viscosity law. The three-solver benchmark and upstream audit objectives remain
active.

## Revision 77 — adaptive refinement cost for one worst cell

Added `tools/audit_physicsnemo_hotcell_refinement.py` and its full terminal
partition JSON. On the worst cell from the 16^3 cover, the maximum terminal
upper drops from 52.134 to 2.0987, 0.93861, and 0.36148 at budgets of 129,
513, and 2,049 evaluations. The exploratory 0.26 comparator is first reached
at 3,923 evaluations / 1,962 leaves (upper 0.259992); leaf volume sum matches
the parent volume exactly in the recorded float calculation. This measures
only one cell and cannot be extrapolated to the remaining 4,095 cells or a
whole-domain result. The comparator remains unregistered; no PhysicsNeMo
quality verdict changes, and the overall goal remains active.

## Revision 53 — selected-field spatial Hessian transfer

Added `verification/SpatialHessianTransfer.lean`. It combines the local
spatial-jet restriction with the already checked cusp-ball germ and
full-spacetime Hessian result: on the same shrinking ball, the selected
candidate's fixed-time spatial Hessian is bounded by `C*q^(-40)` on an
existential terminal interval. Local `ContDiffAt` for the candidate is
derived from its eventual equality with the smooth selected base. Both the
generic helper and composed theorem print only `propext`, `Classical.choice`,
and `Quot.sound` in the Lean 4.34.0-rc2 environment. Run/source details are
recorded in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`.

This closes the formal spatial-restriction step; the classical nonlinear
packet comparison, existential constants and terminal interval, finite-stage
extraction, and full benchmark matrix remain unfinished. The resulting
`Cstretch+39` statement is still a conditional shrinking-initial-packet
allowance. It proves no fixed-size misalignment or molecular, phase-transition,
particle-position, or viscosity consequence. The overall benchmark goal stays
active.

## Revision 54 — conservative packet-radius specialization

Rechecked the piecewise sufficient-radius derivation against the source
stretch enclosure and the newly Lean-checked spatial Hessian transfer. Under
the conditional envelopes `rho=rho0*Q^(1/2)` and `k<=k0*Q^(-40)`, the existing
`Cstretch+39` power is in `[42.9999995,43)`. Using the independently
Lean-checked `Cstretch<4` bound gives `a<=Q^(-4)` and
`I<=(tau0/3)*Q^(-3)`. Both the tube-exit criterion and fixed-angle error
criterion then permit a conservative `delta<=K*Q^43` for sufficiently small
Q, with K depending on non-effective tube/Hessian and angle constants. The
exact exponent specialization and prefactor forms are recorded in
`evidence/tests/packet-radius-scaling.json` and reproduced by
`tools/check_packet_radius_scaling.py`.

This is an algebraic consequence of conditional envelopes, not evidence that
the actual flow loses alignment at finite size. No numerical prefactors were
extracted, and no molecular, phase-transition, particle-position, or viscosity
claim follows. The nonlinear comparison and full benchmark goal remain active.

## Revision 56 — feedback closure compared with singular Burgers vortex

Audited the user-shared model `q'=4 nu-aq`, `W=Gamma/(pi q)`, `a=kappa W`.
The width ODE follows from the Gaussian-vorticity ansatz under prescribed
linear strain; the extra feedback closure is imposed. Its threshold and
self-similar parameterization match the published singular Burgers-vortex
family of Maekawa–Miura–Prange for a corresponding circulation, where the paper
says strain behaves "as if" it depends on vorticity. This is not derivation of
a feedback law from Navier–Stokes. The solution uses spatially growing linear
strain, so it does not demonstrate a finite-energy blow-up or molecular effect.
Compared this relation with the pinned OpenAI core along its selected material
axis: a pointwise fixed proportionality fails because strain scales as
`tau^-1`, whereas nonzero axial vorticity scales as `tau^-(1+h)` for `h>0`.
This does not test closure against global peak vorticity without proving that
this trajectory attains the spatial maximum. Added
the derivation and source pin in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`. The result
sharpens the model test but leaves the concentration-aware benchmark goal
active.

## Revision 57 — reproducible algebra check and stale-run recheck

Added `tools/check_burgers_feedback_mapping.py` and its JSON output under
`evidence/tests/`. It checks the imposed-closure parameterization and
strain/vorticity coefficients for five representative cases using
standard-library floating-point arithmetic; status is explicitly
`PASS_ARITHMETIC_ONLY`, not a PDE or theorem validation. The repository-root
command is `python tools/check_burgers_feedback_mapping.py`. Re-ran the live
process-table check: the earlier host runner, orphan Docker client, solver, and
Docker stop/inspect clients are no longer present. This establishes that those
local processes are gone, but Docker/OrbStack's container inventory was not
recovered from its previously unresponsive daemon, so container removal remains
unverified. The partial attempt remains preserved and is not restarted on this
analytical turn.

## Revision 58 — completion audit includes the feedback hypothesis

Added a separate row to `docs/completion-audit.md` for the user-proposed
Burgers feedback and particle interpretation. It keeps the imposed strain
history, the additional closure, the known singular Burgers-vortex parameter
match, and the OpenAI pointwise-versus-global-peak gap distinct. The row links
the report and its arithmetic-only checker and explicitly records that no
molecular or probability consequence is established. Full benchmark and
three-project completion gates remain active.

## Revision 59 — current three-project release and issue inventory

Captured a read-only official GitHub API refresh in
`evidence/upstream-refresh/three-project-inventory-2026-10-01.json` and
integrated the dispositions into `reports/upstream-disposition.md`. The SU2
latest release matches the benchmark pin and its time-source reports remain in
existing tracking. OpenFOAM's currently open items do not match the benchmark
path. PhysicsNeMo v2.2.2 changes version/install guidance but not the audited
CFD or spectrum source; the odd-width spectrum defect remains identical on
current main and is already tracked by open issue #2007 / PR #2008. No duplicate
upstream issue was filed. This status refresh does not close the separate
PhysicsNeMo acceptance-threshold/continuous-peak gap or the solver reproduction
requirements.

## Revision 60 — live-source recheck of follow-up literature

Rechecked `openai/NavierStokesAndEuler` main on 2026-10-01; it remains at
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. The arXiv API reports v2 of Lei
and Ren's Part I current as of 2026-09-29. An exact-title query for the
announced Part II returned only Part I, so no Part II record was found as of
this check. The already documented conditional analytic-forcing result remains
unapplied to OpenAI's actual force. The recheck and its limits are in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`; solver
reproduction and the broader benchmark goal remain active.

## Revision 61 — fresh cross-solver archive replay

Replayed the six published postprocessing/hash checks from
`work/reference-check-env` on 2026-10-01. The four base OpenFOAM fixed-step
archives again matched their frozen 50-step schedules; all five SU2 diagnostic
replays exactly matched current postprocessing, while inner-residual misses
still prevent a temporal error certificate; all five AMR/remap archives passed
their byte/tree checks; and all five PhysicsNeMo checkpoint/evaluation pairs
matched their archive hashes. PhysicsNeMo sampled peak errors remain
approximately 0.91–0.97%, with maximum sampled derivative-field differences
of 1.20–1.26% on the stated normalization. These are artifact/replay checks,
not solver reruns, continuous-field certificates, or physical validation. The
full scoped results are in `reports/solver-matrix-coverage-2026-09-30.md`.
The project goal remains active.

## Revision 62 — exact-rational global derivative-cover bound (superseded)

To address the PhysicsNeMo continuous-gradient-peak gap, added an exact-rational
second-derivative envelope for all 25 frozen PINN checkpoints. It combines the
stored binary64 weights as exact fractions, a tanh-chain Hessian bound, and an
analytic `580` entry bound for the manufactured reference velocity Hessian.
Under an illustrative 5% comparison only, a best-case uniform Lipschitz cover
would still require 30,821–37,878 nodes per axis (about 2.93e13–5.43e13 total
points), even assuming zero error at every grid node. Eight-point autograd
sanity checks remained below each envelope; the largest observed/envelope
ratio was about 0.0123%. This shows the global bound is too coarse for practical
certification, not that the fields are inaccurate or that local interval
methods cannot work. Five percent remains unregistered for PhysicsNeMo, and
no prior verdict changes. This first calculation used an incorrect assignment
of the sine/cosine input features and its numerical bounds are withdrawn by
Revision 64. The derivation, machine record, checker and tests are
in `reports/physicsnemo-pointwise-gradient-audit-2026-09-30.md`,
`evidence/tests/physicsnemo-global-hessian-coverage.json`, and
`tools/physicsnemo_global_hessian_bound.py`. The full 97-test suite passes.
The next continuous-peak step is local interval subdivision, not treating
sampled maxima as certificates; the benchmark goal remains active.

## Revision 63 — external method update

Reviewed a newly submitted arXiv preprint claiming computer-assisted global
regularity for explicitly bounded families of periodic data. Its finite-path
plus uniform a-posteriori enclosure and independent exact-arithmetic checks
are a useful method lead for our still-open continuous peak audit. The scope
does not transfer directly: this benchmark asks for derivative-error
enclosures, and the preprint's claimed theorem is restricted to its stated
unforced data families. Its reproducibility package/DOI is described as
forthcoming, so the result remains unverified here. The new development and
its limits are recorded in
`reports/recent-navier-stokes-verification-developments-2026-10-01.md`.
Continue by testing adaptive local enclosures and looking for the preprint's
independently auditable artifacts; keep all material/particle interpretations
as open hypotheses unless supported by a kinetic model and data. The overall
goal remains active.

The OpenAI source repository currently has Issues and Discussions disabled;
do not claim an upstream report was filed. Continue building evidence locally
and identify a project-provided feedback route only if one is documented.

## Revision 64 — corrected PhysicsNeMo feature-order bound (floor updated in 65)

Reviewing the frozen training call revealed that the seven inputs are ordered
as three sine coordinates, then three cosine coordinates, then `t/end`. The
first global Hessian-bound implementation grouped sine/cosine features by
axis, so its derivative allocation and all derived grid costs were not
justified. Corrected the axis mapping, added a regression case that catches
the diagonal mixed-derivative underbound, and made the audit reject a changed
training feature expression and verify that the script matches the frozen run
harness commit. Also used the exact endpoint identity
`u_pred-u_ref=t*MLP+(1-exp(-t))*u0` with `1-exp(-t)<t=1/20`, reducing the
reference-Hessian contribution from 580 to 29. The initial corrected
uniform-grid calculation used a lower bound for the exact peak, giving a
conservative count for a stricter threshold rather than an optimistic lower
floor. Revision 65 fixes that direction. The prior Revision 62 feature-mapping
values are withdrawn; no PhysicsNeMo quality verdict changes. The benchmark
goal remains active.

## Revision 65 — optimistic floor uses a peak upper bound

For a 5% illustrative comparator, using the exact gradient peak's lower bound
would reduce the error budget and overstate the minimum required grid size.
The corrected floor instead uses `4*sqrt(28)*exp(-1/20)<424/21<21`, so the
most generous possible 5% budget is `21/20`, and `pi>3` to lower-bound the
variation term; it also assumes zero sampled-grid error. Across 25 frozen
models this gives at least 9,465–13,743 nodes per axis (8.48e11–2.60e12 total
points) for this Hessian envelope. It is a lower bound for this proof route,
not an end-to-end certificate. The sampled
network-Hessian-to-bound ratio remains at most 0.0168% on eight deterministic
points and is only a sanity check. No threshold is preregistered and no quality
verdict changes. This correction was found by reviewing the inequality
direction independently of the feature-order bug. The benchmark goal remains
active.

## Revision 66 — exploratory local interval point check

Implemented a local interval enclosure for the spatial Jacobian of the frozen
PhysicsNeMo prediction error and checked its reference-field Jacobian formula
against the repository's manufactured-solution implementation. Unit tests
cover a small analytic tanh network, multiple reference points, box refinement,
and validation-state restoration. On the frozen `n64-nt17` archive, the audit
selected the largest sampled gradient-error point from 262,144 saved points,
then re-evaluated that exact point independently with PyTorch autograd. The
largest componentwise midpoint difference was `2.17e-15`; the maximum
degenerate point-interval width was `1.97e-59` at 60 decimal digits. This is
only a point-level implementation cross-check: it supplies no neighbourhood
bound, full-domain cover, continuous-extremum certificate, or new quality
verdict. The checkpoint's sampled gradient error and overall PhysicsNeMo
quality remain as previously recorded (`UNCERTAIN`). Reproduce using
`PYTHONPATH=.:work/physicsnemo-source work/physicsnemo-env/bin/python
tools/audit_physicsnemo_interval_probe.py`; details and hashes are in
`reports/physicsnemo-local-interval-probe-2026-10-01.md` and
`evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json`. The full
102-test suite passed.

## Revision 67 — local interval wrapping and subdivision probe

Extended the frozen `n64-nt17` local probe to nonzero-width boxes around the
largest saved sampled gradient-error point. Direct interval evaluation's
Frobenius upper bound grows from `0.255` at half-width `1e-4` to `0.747` at
half-width `0.01`; nine corner/center autograd checks at each tested scale fell
inside the computed enclosures with a `1e-7` floating tolerance. Equal
subdivision of the half-width `0.01` box lowers the maximum cell upper bound
from `0.747` for one cell to `0.492`, `0.367`, and `0.307` for 8, 64, and 512
cells. This shows local subdivision reduces wrapping but remains costly and
loose; the 512-cell bound is still about 22% above the sparse sampled maximum.
The record and limitations are in
`evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json` and
`reports/physicsnemo-local-interval-probe-2026-10-01.md`. This is not a
full-domain cover or proof-kernel validation. No PhysicsNeMo quality verdict
changes; the project goal remains active.

## Revision 68 — Arb centered local Hessian enclosure

The previous mpmath interval dependency was material: mpmath 1.3.0 explicitly
labels its interval support experimental. Added a pinned
`python-flint==0.9.0` verification dependency and an Arb midpoint-radius
implementation of the frozen network's first and second spatial jets. A
centered mean-value enclosure combines the Jacobian ball at the box center
with an Arb Hessian enclosure over the box. An independent finite-difference
test checks the analytic reference Hessian; point evaluations check the
centered enclosure at 27 points in each neighborhood box and at subdivision
cell centers.

On the `n64-nt17` candidate, the half-width `0.01` Frobenius error upper bound
falls from `0.943` under direct interval propagation to `0.357` with the
centered form. Splitting that same parent box into 8, 64, and 512 equal cells
lowers the maximum cell bound to `0.273`, `0.257`, and `0.253`. The method
degrades on larger boxes: at half-width `0.05`, the centered bound grows to
about `4.13e5`, versus `5.90e3` for the direct form. See
`tools/physicsnemo_arb_interval_probe.py`,
`tools/audit_physicsnemo_arb_interval_probe.py`, and
`reports/physicsnemo-arb-centered-interval-probe-2026-10-01.md`, with hashes
and numerical data in
`evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json`.
These selected point checks and one tiny local box do not constitute a
domain-wide proof. The PhysicsNeMo verdict remains `UNCERTAIN`; continue with
complete-domain adaptive coverage and independent proof-kernel assurance. The
overall goal remains active.

## Revision 69 — adaptive Arb cover cost around one candidate

Added a deterministic worst-upper-first axis-bisection helper with serialized
terminal cells, finite-upper validation, explicit target/budget/stagnation
status, and tests for complete parent-box coverage. On the frozen PhysicsNeMo
candidate, the exploratory (not preregistered) `0.26` Frobenius comparator is
met for half-width `0.01` using 77 evaluations / 39 leaves and for `0.025`
using 1,085 / 543. At half-width `0.05`, the 2,049-evaluation budget ends with
1,025 leaves and maximum upper `0.27613`, above the comparator. Terminal-cell
center autograd checks were within the computed intervals at `1e-8` floating
tolerance. The exact boxes and bounds are preserved in
`evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json`; method
and limits are in the matching report. This covers only three local boxes about
one sampled candidate, does not validate Arb with an independent proof kernel,
and does not establish a domain-wide maximum. PhysicsNeMo quality remains
`UNCERTAIN`; the overall benchmark goal remains active.

## Revision 70 — whole-periodic-domain Arb enclosure probe

Tightened each Arb `sin`, `cos`, and `tanh` ball by intersecting with the
analytic range `[-1,1]`, with a regression test; this corrects severe
range-wrapping from broad balls without changing the represented functions.
The frozen-model audit now uniformly tiles an outward-rounded superset of
`[-pi,pi]^3` at 2, 4, and 8 cells per axis. Every cell-center autograd check
(584 total) fell within its component enclosures at `1e-8` floating tolerance.
The maximum centered Frobenius upper bounds were still approximately 242,057,
70,089, and 12,251, versus maximum cell-center samples 0.0148, 0.0553, and
0.146. Thus a complete tiled upper enclosure is computationally constructible,
but this method remains much too loose to certify a useful continuous peak at
these resolutions. The exact rerun is recorded in
`evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json` and
explained in the associated report. Center sampling is diagnostic only; Arb is
not independently proof-kernel checked; no acceptance threshold is
preregistered. The PhysicsNeMo verdict remains `UNCERTAIN` and the overall
goal remains active.

## Revision 71 — derivative-range tightening and rejected norm recurrence

Added analytic range intersections for `tanh'` and `tanh''` in the Arb spatial
jet. With this tightening, the maximum centered Frobenius enclosure on the
512-cell (8-per-axis) periodic-domain cover falls from 12,251 to 275.01; the
maximum cell-center sample is 0.14597. Whole-domain worst-upper-first adaptive
bisection uses 2,049 evaluations / 1,025 leaves but remains at maximum upper
167.31, above the illustrative `0.26` comparator. This is still too loose for
a useful continuous peak certificate. Local adaptive results and all updated
intervals were regenerated from the frozen `n64-nt17` archive and are in the
existing Arb evidence/report files.

Also evaluated an exact-rational vector-Hessian recurrence based on weight
matrix Frobenius norms across all 25 frozen PhysicsNeMo checkpoints. The
illustrative uniform-grid floor worsened to 287,269–328,448 nodes per axis,
about 24–31 times the componentwise route's 9,465–13,743. This candidate is
rejected for efficiency and does not replace the existing bound. The comparison
is preserved in `tools/physicsnemo_global_hessian_bound.py`, its auditor and
`evidence/tests/physicsnemo-global-hessian-coverage.json`. Sampled AD checks do
not prove the global recurrence. No threshold or quality verdict changes; the
overall benchmark goal remains active.

## Revision 72 — monotone Arb tanh endpoint enclosure

Replaced broad-ball Taylor evaluation of tanh activations with endpoint
interval evaluation, justified by monotonicity of tanh, then intersected the
hull with its analytic range `[-1,1]`. A regression check confirms a strict
narrowing on `[-1,1]` and containment of selected point evaluations. On the
frozen `n64-nt17` model, 512 uniform boxes covering an outward-rounded
`[-pi,pi]^3` now have maximum centered Frobenius upper 235.32. A full-domain
adaptive partition with 2,049 evaluations / 1,025 leaves reaches 151.40, still
far above the exploratory `0.26` comparator. At the sampled candidate's local
boxes the same target is met with 63 / 32 leaves for half-width `0.01` and
1,021 / 511 for `0.025`; half-width `0.05` remains budget-limited at 0.27174.
The regenerated values and full terminal partition are in the Arb evidence
JSON; details are in its report. The global enclosure remains too coarse for a
useful continuous peak certificate, and no quality verdict changes. The
project goal remains active.

## Revision 73 — local quadratic Taylor enclosure and global comparison

Added a second-order Taylor enclosure of the gradient-error field, with the
point Hessian at the box center and an Arb interval third-derivative remainder
over the full box. The MLP third jet is checked componentwise against PyTorch
autograd; selected manufactured-field third derivatives are checked against
independent finite differences; a synthetic 27-point direct-Arb check is
contained. On the frozen sampled candidate, half-width `0.01` tightens the
Frobenius upper from 0.3240 to 0.2618, and half-width `0.025` from 0.7580 to
0.3684. However, on full-domain uniform covers Taylor is worse: at 8 divisions
per axis, 4,173 versus 235.3 for centered mean-value, with similarly large
penalties at 2 and 4 divisions. A budget-matched hybrid adaptive cover (513
box evaluations, 257 leaves) has maximum 469.90, identical to standard
centered adaptive bisection at the same cap; the centered run takes about 10.6
seconds while hybrid computes both forms. This route is retained only for
small local boxes, not adopted as the global method. All thresholds here are
exploratory; PhysicsNeMo quality remains `UNCERTAIN` and the full benchmark
goal remains active. Reproduction data and bounds are in the Arb audit JSON
and report.

## Revision 74 — local/global cell-scale crossover

Measured centered and quadratic-Taylor bounds on seven expanding cubes around
the same frozen sampled candidate. Taylor is tighter at half-width 0.05 (ratio
0.612), approximately tied at 0.075 (1.031), and looser from 0.1 onward (1.62
at 0.1). This crossover is local to that candidate and geometry. The prior
2,049-evaluation whole-periodic-domain adaptive cover ends in boxes of width
0.785 per axis (half-width about 0.393), far above the measured local crossover
scale; thus the current global partition cannot benefit from switching to the
Taylor form. Exact values are stored in
`evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json` and
discussed in the associated report. No accuracy threshold or physical
interpretation is inferred. The benchmark goal remains active.

## Revision 75 — 16-per-axis full-domain centered cover

Added `tools/audit_physicsnemo_centered_domain_cover.py` and a hash-linked
record for a uniform 16^3 cover of the entire outward-rounded periodic cube
for the frozen `n64-nt17` checkpoint. At 30 decimal digits, the maximum cell
Frobenius upper is 52.134 across 4,096 cells, down from 235.317 at 8^3; the
recorded run took 67.2 seconds. The maximum error-Jacobian norm at the 4,096
cell centers is 0.22006, and all point samples fell inside their component
intervals within `1e-8` floating tolerance. This is a complete tiled interval
upper under Arb's arithmetic contract, but remains about 237 times the center
sample maximum and is not a useful certified peak relative to any registered
PhysicsNeMo criterion (none exists). Center checks do not prove the interval
method or library. Full result, hashes, environment, and limitations are in
`evidence/tests/physicsnemo-centered-domain-cover-n16.json`; reproduction
command is in the associated report. Quality remains `UNCERTAIN`; the overall
goal remains active.

## Revision 76 — decomposition of the worst 16^3 cover cell

Extended the reproducible 16^3 whole-domain audit to save the maximum-upper
cell and separate its center Jacobian from coordinatewise Hessian-variation
bounds. The worst cell is `[2.3562,2.7489]^3`, centered at `(2.5525,2.5525,
2.5525)`. Its center Jacobian Frobenius upper is 0.0508, while the centered
cell upper is 52.134; Hessian-variation Frobenius bounds by coordinate are
16.69, 18.16, and 17.38. The second-order Taylor upper on the same box is
293.83, so its remainder is much worse at this cell scale. The decomposition
is saved in `evidence/tests/physicsnemo-centered-domain-cover-n16.json` and
explained in the interval report. It indicates interval Hessian dependency
inflation as the current bottleneck; it does not validate the Arb library
independently or change the `UNCERTAIN` quality status. The full goal remains
active.

## Revision 78 — packet-bound logical boundary

Strengthened the exact packet-bound audit to encode a logical guard: a rational
case with comparison upper `4/19` above tube radius `1/10` is classified only
as not certified by this sufficient estimate. The archived JSON explicitly
lists trajectory exit, finite-packet misalignment, molecular alignment, and
viscosity change as conclusions not implied. A separate `4/99` case remains
certified inside. The symbolic identities and applicable solver/gate tests
pass; this does not prove the classical packet comparison or supply constants
for the OpenAI construction. No physical claim or quality verdict changes.

## Revision 79 — live upstream disposition rechecked

A same-day GraphQL refresh confirms SU2 discussion #2890 (one maintainer reply)
and issue #2353 remain the current temporal records; PhysicsNeMo issue #2007
and PR #2008 remain open, with #2008 behind base. Exact node timestamps and
SHAs are preserved in `evidence/upstream-refresh/live-status-2026-10-01T2345Z.json`.
No duplicate report was filed because the observed scope remains tracked. This
refresh does not broaden the tested code paths or close any numerical-quality
gaps; the overall goal remains active.

## Revision 80 — diagonal limit-exchange counterexample

Added a generic smooth counterexample to the inference from decay of each
fixed finite stage prefix to decay of a growing cutoff sum. With diverging
schedule `a(j)=j` and terms `q*chi(j*q)`, every fixed term tends to zero, while
on `q=1/n` the full finite sum stays between 1 and 2. The lower bound is exact;
the executable check records the smooth-cutoff values and verifies the bounds.
This is not a counterexample to the pinned OpenAI construction. It identifies
the missing construction-specific uniform tail estimate needed for finite
stage extraction and does not change any solver or physical verdict.

## Revision 81 — correction: source-specific analytic tail is present

Reinspection of the pinned `SlowBorelBase.lean` found that the generic
counterexample does not identify a missing tail theorem for the selected
observable. `AdmissibleScales.ordinary` supplies stagewise jet bounds;
`ordinary_tail_bound` sums them into a uniform tail bound, and the existing
Lean extension proves `axial_derivative_tail_tends_zero` with only the audited
standard axioms. Revision 80's wording that a construction-specific uniform
tail estimate remains missing was too strong and is superseded. The remaining
gap is effective numerical extraction: the selected schedule, compact
derivative constants, and coefficients are still existential/noncomputable.
The generic smooth counterexample remains valid only as a warning that
fixed-prefix identities alone would be insufficient. No physical or solver
verdict changes.

## Revision 82 — exact finite-window schedule extractor

Added an exact-rational schedule extractor for a finite chart window
`q>=q_min`. It checks source absorption inequalities by integer arithmetic,
enforces schedule doubling, and reports the first stage after which every
later cutoff is zero on that window. Synthetic tests and a clearly labeled
synthetic example validate the implementation. The input jet bounds and
positive exponent lower bound must be certified externally; neither has been
numerically extracted for the selected OpenAI coefficients. This makes no new
solver, blow-up, particle, or viscosity claim and does not change the overall
research goal or its three-project gates.

## Revision 83 — general incompressible tracer-density invariant

Added an analytic scope note deriving volume preservation from the flow-map
variational equation and Liouville's determinant identity. For smooth
incompressible passive-tracer transport, density values, all defined Lp norms,
and differential entropy are preserved, even while covariance and
geometry-selected event probabilities may change. The note distinguishes
infinitesimal orientation, absolute position distributions, finite-particle
models, and constitutive viscosity. It supplies a direct countercheck to
interpreting local directional alignment as generic positional certainty or
viscosity loss. The result is conditional on smooth flow and does not assert a
continuation through a singular time.

## Revision 84 — PhysicsNeMo full-domain interval cover remains too coarse

An adaptive Arb interval cover was evaluated over a full periodic domain for
the frozen PhysicsNeMo n64-nt17 checkpoint. At 8,192 boxes it gives a
pointwise lower bound near 0.25093 and a continuous-domain upper bound near
7.27396; the 10% gap target is not met. The cover is useful as an explicit
continuous upper enclosure but is too loose for a peak-quality verdict. The
quality gate remains UNCERTAIN; the work does not establish a software defect
or a continuous maximum. Hashes, limits, and reproduction instructions are in
the report and machine record.

## Revision 85 — independent dense sample slightly raises PhysicsNeMo peak

An independent 1,048,576-point scrambled-Sobol evaluation with PyTorch
autograd found a sampled gradient-error Frobenius value `0.25234574`, about
0.56% above the earlier 262,144-point lattice maximum. An Arb point enclosure
supports a pointwise lower bound at that candidate. The new point is in the
same local region; this indicates slight underestimation by the old sampling
grid, not a continuous-maximum certificate or solver defect. The global
interval upper remains coarse and the PhysicsNeMo quality gate remains
UNCERTAIN. Inputs, hashes, and reproduction steps are preserved in the new
report and evidence JSON.

## Revision 86 — local PhysicsNeMo peak candidate refined

A bounded multi-start PyTorch L-BFGS search from the top 16 points in the
independent Sobol scan found a candidate with gradient-error Frobenius value
`0.25340829` and final gradient norm `8.42e-8`, about 0.42% above the previous
sampled maximum. Arb point and local-box enclosures support the candidate value;
a quadratic Taylor upper bound is `0.25344430` on the box of half-width `1e-4`.
This is strictly local evidence: it is not a continuous/global maximum proof,
not a defect report, and not evidence for particle alignment or viscosity
change. The full-domain cover remains coarse, so the PhysicsNeMo verdict and
overall goal remain UNCERTAIN and active. See the report and hashed machine
record for limits and reproduction.

## Revision 87 — fixed-cone packet exponent independently derived

An independent componentwise derivation confirms the conditional `Q^43`
packet-radius law for remaining inside a fixed axis cone under the stated tube
and Hessian envelopes. The linear axial/transverse ratio is
`Q^(3C/2)*tan(theta0)`; comparing the nonlinear remainder with the axial
component yields angle allowance `Q^(C+kappa-1)`. This is a different and
weaker requirement than controlling error relative to the contracting
transverse component, which yields `Q^(kappa+5C/2-1)` (`Q^49` at conservative
`C=4`, `kappa=40`). The derivation and distinction are now in the report and
symbolic records, with two focused tests passing. This validates algebra only;
all packet and physical conclusions remain conditional or unsupported.

## Revision 88 — OpenFOAM six-case matrix replay reconciled

A current-state audit corrected reliance on the older historical partial
attempt: the cross-run manifest has all six spatial/time cases complete. Fresh
archive, hash, time-sequence, standard-gate and temporal-comparator replays
confirm the two temporal addendum cases completed at 100/100 and 200/200 steps;
the old 35/36 case remains preserved and superseded. The n=64 temporal
three-point order is about 0.499 and exact-velocity error is nearly flat, so
this is no asymptotic temporal-error certificate. The matrix's persistent
local-quality-blind-spot criterion remains NOT_OBSERVED. Details and replay
scope are recorded in `reports/solver-matrix-coverage-2026-09-30.md`; no new
solver run or upstream report was needed.
## Revision 89 — short AMR first-refinement probe

A frozen n=16 three-step OpenFOAM Foundation 13 diagnostic compared AMR with a
same-grid uniform control around the first refinement interval. Both runs
completed and their raw archives passed checksum and member-read checks. AMR
refined from 4,096 to 16,640 cells before t=0.003. The relative
volume-weighted velocity error rose from 5.875% to 39.948% across that interval;
the control rose from 5.875% to 6.161%, giving the preregistered descriptive
contrast +0.33786. The first post-refinement sample already includes one solved
step, so remapping, flux correction, projection, sensor updates and later
evolution are not separated. This merits a direct pre/post transfer audit but
does not establish a solver defect, singularity, molecular alignment, or
viscosity transition. The full record is in
`reports/solver-matrix-coverage-2026-09-30.md` and
`evidence/of13-amr-first-refinement-v1/`. The three-project research goal
remains active and UNCERTAIN.

## Revision 90 — AMR error rise traced to mesh-dependent norm sampling

An independent retrospective quadrature audit materially revised Revision 89's
interpretation. The frozen probe's cell-centre-weighted relative L2 norm is
5.875% on n=16 before refinement and 39.948% on the AMR mesh afterward, but a
counterfactual that only assigns unchanged parent-cell values to their child
cells already gives 41.816% under the new centre-sampling rule. Integrating
piecewise-constant and cellwise gradient-linear reconstructions within cells
with converged Gauss quadrature reverses the apparent AMR degradation contrast
(-1.638 and -7.060 percentage points, respectively). Thus the positive
centre-sample contrast is confounded by changed quadrature and is not evidence
that AMR worsened the represented field. Public Foundation 13 source inspection
is consistent with parent-cell value mapping followed by flux correction and a
solved step; package-binary equivalence remains unverified. A next analytical
priority is to check whether published cross-resolution local metrics have
similar sampling limitations, while retaining the original fixed-grid gates
and all solver/physical claims as separate questions. See the new audit in the
cross-solver coverage report and its machine-readable JSON.

## Revision 91 — uniform-grid velocity norm depends on reconstruction

The velocity-L2 quadrature audit was extended to the archived OpenFOAM
n=16/32/64/128 spatial series at t=0.05. Cell-centre relative errors are
8.876%, 1.876%, 0.478%, and 0.121%; integrating the cellwise Gauss-gradient
linear reconstruction gives 22.637%, 4.970%, 1.193%, and 0.296%. Thus the
velocity-only 2% threshold for n=32 changes with reconstruction, while n=64
and n=128 remain below it under both measures. The combined local gates and
the discrete fine-grid `NOT_OBSERVED` classification were not recomputed and
remain as frozen; this does not certify continuous-domain extrema. Full
Quadrature convergence checks, source-field hashes, and rerun instructions
are recorded in `reports/solver-matrix-coverage-2026-09-30.md` and
`evidence/of13-high-gradient-v2/uniform-cell-center-quadrature-audit.json`.

## Revision 92 — exact cell-average reference added

Derived a closed-form exact cell average for the localized high-gradient MMS
from its separable Fourier factors, using normalized sinc weights for each
mode. Compared with the archived OpenFOAM cell values at n=16/32/64/128, this
DOF-level relative L2 is 15.558%, 3.581%, 0.894%, and 0.225%. Independent
10-point tensor Gauss integration over five n=16 cells agrees with the closed
form to 1.8e-16. This avoids selecting P0/P1 reconstructions, but assumes the
FV DOFs should be compared with exact volume means; the installed solver's
field semantics were not independently established. It is supplementary and
does not rewrite the frozen gate or establish continuous extrema. Results and
hashes are included in the same machine-readable audit.

## Revision 93 — AMR quadrature finding split by error meaning

Applied the exact analytic cell-average reference to the first-refinement AMR
checkpoints. The AMR DOF-level errors are 13.783% at t=0.002 and 40.559% at
t=0.003; the uniform control is 13.783% and 13.915%, giving a cell-average
difference-in-differences of +26.643 percentage points. Assigning unchanged
coarse parent values to refined children already gives 42.484% against exact
t=0.002 child-cell averages. Thus the positive frozen cell-centre contrast is
sampling-confounded, while the finer cell-average DOF metric independently
shows a large coarse-to-fine prolongation/resolution mismatch. The P0
continuous-field integral is partition-invariant for the mapped field, so
these statements concern different error definitions. The installed U-field
semantics and post-remap solver-step effects remain unresolved; no upstream
defect verdict follows. Keep AMR quality `UNCERTAIN` and make the norm meaning
explicit. The AMR audit JSON and coverage report contain all comparisons.

## Revision 94 — SU2 sampled-field semantics pinned to solver source

Checked the frozen SU2 v8.5.0 cases against their archived configs and the
matching local source checkout (`7478e9d684537fbb123a5e170eb7956d51b54ca6`).
The reported velocity L2 is explicitly a discrete norm on unique periodic
vertices; finite-difference/spectral derivative metrics are grid diagnostics.
The cases use FDS with MUSCL edge reconstruction, no slope limiter, and
Green–Gauss gradients. Source inspection shows separate reconstruction
gradients for convective edge states and primitive gradients supplied to the
viscous residual, so the nodal output does not define a unique canonical
continuous postprocessing field. An FV cell-average interpretation would be
unsupported. Existing measured results and UNCERTAIN gates are unchanged; no
solver defect or continuous-extremum claim follows. Details are recorded in
`reports/su2-study-v1-interim.md`. The multi-solver research goal remains
active and UNCERTAIN.

## Revision 95 — SU2 reference energy quadrature isolated analytically

Derived the exact mean kinetic energy of the manufactured solution on the
frozen periodic SU2 vertex grids from separability and reflection symmetry.
The finite-grid result is
14 beta^2 exp(-2t-6 beta) B_n A_n^2, where A_n and B_n are the discrete
means of exp(2 beta cos d) and exp(2 beta cos d) sin^2(d). It agrees with
direct analytic-field sampling on n=8 and n=16 test grids. At benchmark
parameters, reference quadrature bias is -0.0071755% for n=16 and at
floating-point precision for n=32/64. Replacing the continuum denominator in
the diagnostic-only energy comparison with this exact vertex-grid reference
changes the n=16 observed discrepancy from 12.0279% to 12.0216%; all other
cases are unchanged to displayed precision. Thus reference-grid quadrature is
not a material explanation for the measured energy errors. The original
frozen threshold comparisons and UNCERTAIN gates are unchanged; this does not
certify continuous numerical-field energy. See
reports/su2-study-v1-interim.md and
evidence/tests/su2-standard-review.json.

## Revision 96 — SU2 sampled shell-spectrum contrast separated

Added a reproducible three-way comparison of the archived solver FFT shell
energy, analytic-reference FFT on the same vertices, and continuum Fourier
shell energies. The reference's grid sampling/aliasing/shell-assignment
contrast is 0.00718% at n=16 and below 1e-12% at n=32/64 when normalized by
continuum kinetic energy; solver-sample versus analytic-sample contrasts are
12.0738%, 2.4667%, and about 0.3552% at n=16/32/64. Both FFT shell totals
match their respective sampled kinetic energies within 2.8e-17. The comparison
does not certify a continuous numerical spectrum, and continuum coefficients
retain the mode-cube cutoff-32 non-interval tail limitation. Frozen gates are
unchanged. Reproduction and hashes are in
reports/su2-study-v1-interim.md and
evidence/tests/su2-spectral-aliasing-audit.json.

## Revision 97 — SU2 derivative error localized by reference strength

Reloaded all five SU2 restart archives and independently replayed the periodic
centered-FD2 gradient/curl. Separated solver-sample FD2 versus exact analytic
derivatives, analytic-sample FD2 truncation, and solver-sample FD2 versus
analytic-sample FD2. For n=16/32/64 (dt=.001), gradient RMS terms (total,
reference-stencil, sample-field difference) are (0.3806, 0.2832, 0.1185),
(0.1119, 0.07839, 0.03997), and (0.02589, 0.02014, 0.007503); vorticity
terms are (0.3770, 0.2774, 0.1151), (0.1108, 0.07672, 0.03965), and
(0.02550, 0.01971, 0.007289). Reference-only truncation scales near second
order. The top decile of exact-reference gradient magnitude contains
99.65/99.87/99.68% of squared sample-field gradient error; for vorticity
strength it contains 99.82/99.94/99.96% of squared sample-field vorticity
error. These are discrete descriptive spatial associations with the smooth
manufactured profile, not physical concentration, inter-vertex bounds, a
singularity, or a solver defect. Frozen verdicts remain unchanged; complete
case results and replay checks are in
reports/su2-study-v1-interim.md and
evidence/tests/su2-local-derivative-audit.json.

## Revision 98 — AMR piecewise-constant error orthogonally decomposed

Derived and evaluated the exact L2 identity
||U_h-u||^2 = ||U_h-P_hu||^2 + ||P_hu-u||^2 for the explicit P0 reconstruction,
where P_hu is the exact cell-average MMS projection. Parseval provides the
continuum norm; exact sinc cell averages provide the projection and DOF term.
The split total agrees with independent order-8 Gauss integration within
1.6e-15. At t=.003, AMR total relative error is 46.0763%, from orthogonal
components 39.3816% DOF mismatch and 23.9190% unresolved projection floor;
uniform n=16 is 47.7139%, 12.3494%, and 46.0881%. Refinement raises projected
energy capture from 78.76% to 94.28%, lowering the projection floor, while
the solved AMR values have larger mismatch to exact cell means; the net P0
error improves by only 1.638 points. The cell-average-normalized 40.559%
AMR error therefore measures a different quantity. This is conditional on
P0 reconstruction and does not prove the solver field semantics or diagnose
a defect. Details and reproduction are in
reports/solver-matrix-coverage-2026-09-30.md and
evidence/tests/amr-p0-projection-decomposition.json.

## Revision 99 — AMR level-wise MMS energy and gradient localization

Extended the exact Fourier cell-integral audit to the squared Frobenius norm
of the analytic velocity gradient and grouped velocity energy, gradient
energy, projection floor, and DOF mismatch by archived cellLevel. At t=.003,
level-1 cells occupy 43.75% of the domain but contain 99.999379% of exact
kinetic energy, 99.998070% of exact gradient energy, 99.994697% of the P0
projection floor, and 99.990771% of the cell-DOF mismatch. Level 0 occupies
56.25% and carries the small complements. Exact per-cell energy integrals
reconcile with global Parseval totals; independent 32-point domain and
16-point cell Gauss tests validate the gradient formulas. The AMR sensor was
defined from the known analytic envelope, so this demonstrates alignment of
this mesh with this manufactured field, not blind concentration detection or
a physical transition/solver defect. Hashes and reproduction details are in
reports/solver-matrix-coverage-2026-09-30.md and
evidence/tests/amr-p0-projection-decomposition.json.

## Revision 100 — AMR prescribed-sensor mapping checked against archive

Parsed the archived t=.003 `refineSensor`, centers, volumes, and `cellLevel`
after checking the frozen protocol and archive hashes. The stored sensor
matches `g(y)g(z)`, the explicitly prescribed analytic envelope, with maximum
absolute residual 3.33e-15 over 16,640 cells. Level 1 occupies 43.75% of the
domain volume and contains all cells with sensor >=.01; 72.32% of its volume
is above that threshold, consistent with threshold-edge and buffer effects.
This verifies implementation of the known sensor and its mesh footprint, not
blind detection, particle alignment, or a physical transition. Reproduce with
`work/reference-check-env/bin/python -m tools.audit_amr_sensor_mapping`; the
hash-pinned output is `evidence/of13-amr-first-refinement-v1/sensor-mapping-audit.json`.

## Revision 101 — Directional alignment limit generalized beyond isotropy

For the audited infinitesimal flow derivative, the finite-time spherical-cap
probability uses isotropy, but a fixed Borel law `lambda` on unoriented initial
directions has the more general limit `1 - lambda(E)`, where `E` is the exactly
transverse great circle. Every direction off E enters every fixed positive-
angle axis cone as `Q -> 0`; directions on E stay transverse. Bounded
convergence yields the probability limit. Thus no-mass-on-E suffices for
qualitative directional alignment, while a transverse atom of mass p leaves
limiting aligned mass 1-p. This is only a distributional statement about
infinitesimal continuum separations, conditional on the selected local flow
derivative; it does not concern finite particles, absolute position, molecules,
or viscosity. The cone-boundary algebra check and scope are recorded in
`docs/particle-position-probability.md`,
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`, and
`evidence/tests/particle-position-probability.json`.

## Revision 102 — Default pytest discovery bounded to canonical tests

An unscoped `pytest -q` from the repository root tried to collect historical
checkouts, source snapshots, and dependency repositories under `work/`, causing
duplicate-module collection errors unrelated to the canonical suite. Added
`pytest.ini` with `testpaths = tests`, so the simple root command exercises the
maintained suite only. Explicit verification remains `python -m pytest -q
tests`; rerun both forms after this configuration change.

## Revision 103 — Distributional finite-packet bound under a faster shrinking scale

The existing fixed-direction packet allowance has an angle-dependent
prefactor and is not uniform near the transverse plane. Under the
source-derived, non-effective tube/Hessian envelopes `rho~Q^(1/2)`,
`k<=k0*Q^(-40)`, and `7999999/2000000 <= C < 4`, taking initial continuum
tracer radius `delta0*Q^44` and excluding only directions with
`|cos(theta0)|<Q^(1/2)` makes both transverse/axial and nonlinear-remainder/
axial ratios vanish uniformly. For a fixed direction law with no mass on the
transverse plane, the excluded probability tends to zero. Thus the endpoint
cone probability tends to one conditionally on the classical packet bound;
the constants remain non-effective, the packet shrinks to zero, and this is
not a molecular or fixed-size-particle result. Algebraic exponents and
assumption limits are recorded in `docs/axis-packet-bound.md` and
`evidence/tests/packet-radius-scaling.json`.

## Revision 104 — PhysicsNeMo tracked odd-width fix refreshed at current main

Rechecked NVIDIA PhysicsNeMo at current main
`b08dd3f61ac44c784f7c03b0cc93947226365cad` and reran the focused odd-width
spectral reproducer against both that immutable source and PR #2008 head
`7407608723062dc11ba5332e9ff3774f42bb02d9`. The defect remains on main: the
33x33 height-cosine peak is 10.0833, while its width-axis counterpart splits
across 6.1875/5.0417, and a transpose control differs by 0.10945. PR #2008
suppresses these controls to 3.58e-7, but remains open, review-required, and
behind current main (the compared histories have 11 main-only and 2 PR-only
commits). No duplicate post was made because issue #2007 and the existing PR
already track the finding; the prior comment contains the reproduction. The
current benchmark uses even widths, so its recorded spectra are unaffected.
Reproducer outputs, source hashes, and live API state are in
`evidence/upstream-refresh/physicsnemo-live-recheck-2026-10-01T0337Z.json` and
`evidence/upstream-refresh/physicsnemo-2026-10-01T0335Z/`.

## Revision 105 — OpenFOAM cap4096 AMR candidates recovered from archive

Corrected the event-audit interpretation that described the cap4096 case as
having zero candidates: its log establishes zero refinement events, while the
unrefinement “split points” lines do not measure refinement candidates. A new
reproducible audit checks the raw archive hash, reconstructs the 16^3 periodic
mesh from archived centers, verifies the prescribed sensor to 9.99e-16, and
applies the pinned Foundation 13 strict thresholds and one-layer face-neighbor
buffer. It recovers 1,280 raw sensor-eligible cells and 1,792 buffered
candidates before the maxCells guard. Since the unchanged 4,096-cell mesh is
already at maxCells=4,096, the source guard skips selection. The cap5000 log
independently selects 1,792 cells and its mesh grows by 7*1,792, confirming the
reconstruction. The eligible-check count is still unknown, and this expected
guard behavior does not establish a defect. Updated the source-budget report,
event audit, and v2 manifest without changing the generic log-only
`blocked_candidate_count` field. Reproduce with
`work/reference-check-env/bin/python tools/audit_openfoam_amr_candidate_budget.py`;
the evidence is `evidence/tests/openfoam-amr-candidate-budget-audit.json`.

## Revision 106 — flat-but-active forcing boundary cross-checked against both papers

Refreshed Constantin–Ignatova–Vicol arXiv:2609.20803 to v2 (29 September) and
read its Theorem 1.1, Corollary 2.3, Remark 2.6 and Appendix A against the
official OpenAI Navier–Stokes manuscript. Conditional on the construction's
claimed singularity and the authors' cited source crosswalk, analytic forcing
is excluded and the force cannot vanish on any neighborhood cylinder. A
separate identity-theorem argument uses the paper's pure-swirl open set and
nonzero axial velocity to exclude a common spatial-analyticity bound on the
relevant ball-time slabs without assuming blow-up or the Type-II theorem.
OpenAI Lemma 10.2 also gives zero mixed space-time force jets at the terminal
point, while Lemma 10.3 extends the force smoothly; combined with conditional
nonvanishing, this is a flat-but-active forcing boundary. The force remains
smooth and C2-bounded; the result supplies no amplitude lower bound, actuator
claim, molecular inference, or solver defect. The derivation, source locations,
assumptions, and limits are recorded in
`reports/openai-analytic-forcing-bridge-2026-10-01.md` and
`evidence/openai-analytic-forcing-v2-audit.json`; no simulation or upstream
post was warranted.

## Revision 109 — exact repeat of one OpenFOAM temporal row

Using the frozen Foundation 13 linux/arm64 image and protocol, reran the
`n=64, dt=0.0005` case at source commit `0dc1e99b06ef1632e9199891c8382a21ee2a267b`
in a new work root. The solver completed 100/100 time steps and PIMPLE
convergence records. A new archive comparator verifies all four endpoint
fields (`U`, `p`, `C`, `phi`) byte-identical to the earlier archive, all five
diagnostic errors exactly equal, and every other raw difference confined to
the case mount path and runtime log metadata/hash. The repeated archive,
manifest, environment, comparator and limitations are published under
`evidence/of13-high-gradient-repeat-2026-10-01/`; interpretation is added to
the temporal addendum and completion audit. This is one-case execution
reproducibility, not evidence of solver-wide reliability or a physical result.
The broader three-project goal remains active.

## Revision 108 — clean-export failure repaired and latest artifacts replayed

A fresh fixed-commit export exposed two reproducibility gaps: pytest was
installed separately by CI but omitted from the locked verification set, and
the published report replay used unittest discovery, which did not execute
pytest-style functions. The replay now installs pinned pytest 9.1.1 and uses
the same complete `pytest -q tests` command as CI. Replaying the reports also
found ten stale generated gate JSONs: five PhysicsNeMo reports had an outdated
source hash; five SU2 reports lacked analytic finite-grid energy quadrature
values. Their standard/local gate verdicts did not change. After refreshing
those canonical outputs, 93 evidence links matched and report replay passed.
A fresh archive of commit `33c460715ad6cc3f9f61303d94b85efc5be06f2b` then
passed all 26 replay steps and six additional checks, with zero byte changes
across 152 reports/test-evidence files; full pytest reported 146 passed, one
skipped, and five subtests passed. Logs and exact reproduction instructions are
in `evidence/clean-export-2026-10-01-current/`. This verifies tracked Python
postprocessing only and does not rerun solvers, PhysicsNeMo training, or Lean.
The overall benchmark, remaining analytic obligations and per-target audit
completion remain active.

## Revision 110 — hostile verification of repeat-comparison provenance

Adversarial review found that the one-case OpenFOAM repeat comparator initially
trusted archived manifests for completion and did not constrain unrelated raw
archive differences. It now independently verifies every archived input hash,
raw 100-step time sequence, 100 PIMPLE convergence records, zero exit and
terminal `End`; binds solver logs, parameters, endpoint U/C hashes, diagnostics,
and manifest verdicts; and rejects raw differences outside five declared
runtime/log files. Four hostile tests pass, including a coherently rewritten
time label and an unexpected archive-member difference. The full verification
suite reports 150 passed, one skipped, and five subtests passed. This raises
confidence in the evidence comparison for one repeated case only. It does not
validate the physical interpretation, establish solver-wide reproducibility,
or close the broader OpenFOAM/SU2/PhysicsNeMo and analytic research goal.

## Revision 111 — exact separation of orientation from positional certainty

Extended the selected-axis deformation calculation with an exact Gaussian
pushforward result. For covariance `sigma^2 I`, the variational map has
eigenvalues `sigma^2 Q^C`, `sigma^2 Q^C`, and `sigma^2 Q^(-2C)`, so covariance
volume, differential entropy, and peak density remain constant. Directional
transverse-to-axial ratio shrinks as `Q^(3C/2)`, while for any fixed radius `R`
the probability of lying within that ball around the center is bounded above by
`sqrt(2/pi)*(R/sigma)*Q^C`, tending to zero. A SymPy reproducer with negative
controls is archived at `evidence/tests/alignment-uncertainty.json` and covered
by pytest. This precisely rejects the inference that directional alignment
means greater absolute-position certainty in the linearized Gaussian model. It
does not extend to finite packets of the nonlinear PDE, molecular dynamics, or
a viscosity law; those remain separate obligations.

## Revision 112 — interval proof of one PhysicsNeMo local maximum

The strongest refined candidate on the frozen `n64-nt17` PhysicsNeMo model was
previously only a numerical proposal. A new Arb Krawczyk check on a radius
`1e-4` box proves the objective gradient has exactly one zero there: the
Krawczyk image is strictly interior, its infinity-norm contraction bound is
`0.40051`, and the preconditioner determinant is bounded away from zero.
Interval Hessian bounds give strict negative diagonal dominance throughout the
box, proving the zero is its unique strict local maximum. Its gradient-error
norm lies in `[0.253408291696744, 0.253444297122580]`; independent PyTorch
autograd sanity checks agree with interval point derivatives within `5.6e-15`.
The hashed evidence and reproduction command are in
`evidence/tests/physicsnemo-local-stationary-certificate-2026-10-01.json` and
`reports/physicsnemo-local-peak-refinement-2026-10-01.md`. This does not certify
the global maximum, validate the Arb library with a proof kernel, set a
preregistered PhysicsNeMo threshold, or justify an upstream defect report. The
quality verdict remains UNCERTAIN and the full goal remains active.

## Revision 113 — separate PhysicsNeMo velocity and derivative trends

Replayed the frozen five-seed analysis from its archived run manifest; all 20
added archive SHA-256 checks passed and the machine-readable results were
unchanged. The paired contrasts show that n=16→32 raises sampled gradient- and
vorticity-peak error for four of five seeds, while n=64, nt=9→17 lowers sampled
velocity relative L2 for all five seeds but raises both sampled derivative-peak
errors for three seeds. The latter mean derivative-error increase is about
0.000022. The seed-control report now records this metric disagreement and its
shared-validation and finite-sampling limits. No continuous peak, node-count
causality, or PhysicsNeMo acceptance threshold is established; its verdict
remains UNCERTAIN and the overall goal remains active.

## Revision 114 — OpenFOAM local-quality sensitivity to derivative reconstruction

Reopened all six frozen Foundation 13 high-gradient archives and verified each
archive SHA-256 against the current matrix or temporal manifest. Recomputed
centered-FD2 and real trigonometric-interpolant derivatives from the same cell-
center velocities. A separate band-limited reference test confirms that the
spectral derivative reproduces the analytic reference gradient and vorticity at
all n=16/32/64/128 centers to roundoff (worst peak reconstruction defect below
4e-14). At n=32 the frozen FD2 derivative peak errors are 10.28% and 9.18%,
while the alternative interpolant's node-peak errors are 0.465% and 0.045%;
holding velocity, energy, and spectrum gates fixed changes only this row's
counterfactual local-quality status from FAIL to PASS. The adequately resolved
n=64/n=128 spatial cases remain PASS, so the frozen matrix-level blind-spot
classification does not change. At n=32, the pointwise sampled gradient L2
error is 9.53% under FD2 and 1.92% under the trigonometric reconstruction;
vorticity values are 9.14% and 0.168%. Sampled argmax indices also change,
though tied/near-tied discrete maxima are possible. This demonstrates
the FD2 bias has a matching analytic scale: for the MMS streamwise mode k=4,
the centered-difference derivative gain is sin(kh)/(kh), predicting 9.968%
attenuation at n=32 versus observed full-vector peak discrepancies of 10.28%
and 9.18%. More directly, the exact reference sampled field passed through the
same FD2 stencil has peak floors of 9.862%/9.251%; computed-FD2 versus
reference-FD2 peak differences are only 0.464%/0.078%. Thus most of the coarse
FD2 failure is stencil truncation, with a small nonzero solver-field residual.
This does not exactly predict the vector maxima. This demonstrates
reconstruction sensitivity of the n=32 derivative gate, not which
reconstruction is the canonical continuous OpenFOAM field: no inter-node
supremum or continuous solver field is certified. Evidence and reproduction are in
`reports/openfoam-gradient-reconstruction-sensitivity-2026-10-01.md` and
`evidence/tests/openfoam-gradient-reconstruction-sensitivity-2026-10-01.json`;
the solver was not rerun and no upstream defect is claimed. The multi-target
goal remains active.

## Revision 107 — protocol-status consistency and OpenFOAM field interpretation

The general `docs/protocol.md` still described the independent reference as
TODO, all solver studies as unrun, and tolerances as unfrozen, despite later
frozen protocols and evidence. It now explicitly serves as a methodology/index
and points to the solver-specific protocols, manifests, and coverage report.
The PR #4 branch also records the source-backed distinction that benchmark
initial OpenFOAM `U` is generated from cell-centre samples, while the exact
cell-average interpretation of time-evolved values remains unproved. The
locked reference environment ran 138 tests (one skipped), and GitHub CI passed
for the documentation update. This repairs evidence navigation and terminology;
it does not close the three-project audit, analytic limitations, or publication
deliverables, so the overall goal remains active.


## Revision 15 — selected-profile pressure-premise provenance (2026-10-01)

The user's pressure-sign hypothesis is now checked with a source-bound Lean
extension. A complete prepared-profile data witness with core amplitude at least
2 exists, but the selected `FinalSlowBase.actualProfile` is only proved to have
positive amplitude; the construction bound is not carried through the current
`ProfileData` choice. This is not a counterexample and does not establish that
the selected amplitude falls below the weaker `9/40` local threshold. Keep the
actual-profile pressure-sign premise open until a quantitative bound is derived
or its witness is retained through the final selection. No OpenAI upstream issue
was submitted: the evidence is an extension proof-provenance gap and the upstream
repository has issues/discussions disabled. The completed OpenFOAM matrix remains
unchanged; the old n64 partial attempt is superseded by a verified completed
rerun. See `reports/actual-profile-pressure-provenance-2026-10-01.md`.

## Revision 16 — formal uniform pressure threshold (2026-10-01)

The small-parameter rational inequality behind the local pressure threshold is
now proved in the pinned Lean extension. It proves that any outgoing profile
with core amplitude `b >= 9/40` has `Z > 0` at the prescribed root; combining
this with the prepared `b >= 2` witness and the nominal/modulation assemblies
proves that at least one complete `ProfileData`/root pair has `Z > 0`. This is
existential only. It does not transfer the amplitude premise to the separate
`FinalSlowBase.actualProfile` classical choice, so the selected-profile sign and
force-ratio claims remain conditional. No molecular/viscosity inference follows.
The result, hashes, and proof boundary are in
`reports/pressure-threshold-lean-audit-2026-10-01.md`.

## Revision 17 — newly posted explanatory source (2026-10-01)

The literature refresh found Lei–Ren Part I, arXiv:2609.35406 v2. It explains
the profile-construction stage, while stating that oscillatory-pulse residual
correction is deferred to a companion Part II; the authors describe it as an
exposition not intended for journal submission. We checked only metadata and
abstract. Treat it as a useful explanatory route, not independent verification
of the full OpenAI construction. See the dated literature report and metadata
evidence under `evidence/upstream-refresh/`.

## Revision 18 — linearized-flow volume and covariance (2026-10-01)

The axis deformation's diagonal scale-volume factor and preservation of the
isotropic Gaussian covariance eigenvalue product are now Lean-checked. This
supports the existing conclusion that directional alignment in the linearized
model need not increase certainty near the center. The probability tail bound
remains analytic/SymPy-checked; nonlinear finite-packet and molecular transfer
remain open. See `reports/linearized-flow-volume-audit-2026-10-01.md`.

## Revision 115 — integrated artifact replay (2026-10-01)

The one-command published-evidence replay now directly checks the OpenFOAM
uniform/time-step archives and AMR trees, the SU2 standard acceptance review,
and PhysicsNeMo checkpoint-to-derivative links. Each step records exact local
argv, a portable `python3` replay command and a hash-verified log. The 31-step
replay passed. This improves archived-evidence auditability; it is not a fresh
solver/training run or a continuous-field certificate, and it does not close
the full benchmark goal.

## Revision 116 — source-current and viscous-ratio interpretation audit (2026-10-01)

A live GitHub API recheck confirms OpenAI `main` remains at the pinned
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; metadata still reports Apache-2.0
and disables Issues/Discussions. The selected-profile amplitude premise remains
unproved: `PreparedProfile` carries `P >= 2`, but the `ProfileData` choice does
not carry that proof. This is a provenance gap, not evidence that the chosen
profile has small amplitude. Also, the new negative `nu*Δu/materialAcceleration`
limit concerns an alternate slow-base field, not a full candidate satisfying
the unit-viscosity equation; in the latter, acceleration balances viscosity,
pressure, and force together. Do not infer a constitutive-viscosity effect from
that ratio. Evidence and exact scope are in the dated pressure-provenance and
qualified-profile reports.

## Revision 117 — refreshed three-project upstream inventory (2026-10-01)

Re-read current GitHub metadata, issue/discussion records, and pinned license
files for OpenFOAM Foundation 13, SU2, and NVIDIA PhysicsNeMo. The audited code
heads remain unchanged; existing issue/PR coverage remains sufficient for
PhysicsNeMo and SU2, while OpenFOAM's four listed GitHub issues do not match the
AMR observation and its separate Foundation bug tracker was not exhaustively
searched. No new upstream post is justified. The inventory is archived with
license-file blob IDs and explicitly bounded search scope. The benchmark's
remaining numerical/analytic uncertainty and full completion conditions stay
active.

## Revision 118 — absolute localization versus relative packet expansion

Under the existing conditional tube/Hessian envelopes and classical packet
comparison, the `Q^44` initial-radius family has an all-direction endpoint
upper bound `O(Q^40)`, while for a set of directions whose probability tends
to one, endpoint displacement divided by initial radius is bounded below by
`(1/2)Q^(1/2-C)` and diverges. This reconciles absolute endpoint localization
with relative expansion and shows why the shrinking-initial-packet limit is
not evidence that the flow contracts positional uncertainty or localizes a
fixed-size packet. The exponent controls and assumptions are recorded in
`docs/axis-packet-bound.md` and `evidence/tests/packet-radius-scaling.json`.
The classical comparison theorem and all non-effective constants remain open
limitations; the original three-solver benchmark and audit requirements remain
unchanged.

## Revision 119 — formal finite-measure exceptional-band limit

Added `verification/FinitePacketProbability.lean`, which proves for a finite
measure and a measurable nonnegative observable `c` that the mass of shrinking
strict sublevel sets converges to the mass of `{c=0}`. The pinned Lean
4.34.0-rc2 elaboration and axiom audit pass; the exact source hash, assumptions,
scope, and reproduction command are recorded in
`evidence/lean-verification/finite-packet-probability-2026-10-01.json`. This
formalizes only the measure-continuity step in the conditional shrinking-band
argument. It does not establish measurability for a chosen sphere direction
law, validate the packet comparison or Navier–Stokes hypotheses, or support
molecular alignment, deterministic particle positions, phase transition, or
viscosity-change claims. The nonlinear comparison and non-effective tube and
Hessian constants remain open, as do the full solver benchmark and upstream
issue review conditions.

## Revision 120 — no uniform rate from atomless direction laws

The finite-packet exceptional-band argument gives qualitative convergence for a
fixed direction law with no exactly transverse atom, but no quantitative rate
without further anti-concentration assumptions. An explicit atomless law with
density `1/[c*(log(e/c))^2]` has tail
`lambda{c<Q^(1/2)}=1/[1+(1/2)log(1/Q)]`, which vanishes more slowly than every
positive power of Q. This does not refute the probability-one limit; it bounds
what can be claimed from the present assumption. The derivation and limitations
are recorded in `docs/axis-packet-bound.md` and
`evidence/tests/packet-angle-law-rate.json`.

## Revision 121 — conditional algebraic rate with anti-concentration

Generalized the angular cutoff to `c>=Q^s`. Under the current `Q^44` packet
and `k=O(Q^-40)` envelope, both transverse and nonlinear-to-axial ratios vanish
for `s<min(3C/2,5-C)`. Since the source-derived exponent has `C<4`, `s=1` is
admissible. If the fixed direction law additionally obeys
`lambda{c<epsilon}<=L*epsilon^beta`, the conditional endpoint-cone failure
probability is bounded by `L*Q^beta` for sufficiently small Q; uniform
unoriented spherical measure gives `L=beta=1`. This rate needs the extra
distribution assumption and retains a non-effective small-Q threshold. The
derivation is in `docs/axis-packet-bound.md` and
`evidence/tests/packet-angle-law-rate.json`.

## Revision 122 — exact uniform-sphere tangent orientation law

For the linearized flow map, the transverse and axial singular values give
unit determinant and an exact cone cutoff for uniform spherical initial
orientations: `c_star=Q^(3C/2)/sqrt(tan(theta_star)^2+Q^(3C))`. Thus the
linearized cone-failure probability is exactly `c_star`, asymptotic to
`Q^(3C/2)/tan(theta_star)`. The symbolic cutoff identity has residual zero.
This is the orientation distribution of infinitesimal material separations;
it says nothing by itself about finite particles, centers, or molecules. The
finite-packet `O(Q)` sufficient bound additionally pays for a nonlinear
remainder and may be conservative. Derivation and evidence are in
`docs/axis-packet-bound.md` and
`evidence/tests/packet-radius-scaling.json`.

## Revision 123 — instrumented AMR stage-capture protocol prepared

The earlier AMR first-refinement contrast conflated topology mapping, flux
correction, momentum prediction and pressure correction. Pinned Foundation-13
source ordering shows functionObject execution occurs before `preSolve()` and
its `mesh_.update()`, so functionObjects cannot capture the mapped state. Added
a frozen stage-snapshot protocol plus a source-hash-guarded transformer for the
pinned incompressible solver module. The diagnostic records `U/p` and
`phi/Uf` immediately after mapping, after `correctPhi`, before/after pressure
correction, and after PIMPLE; it does not alter equation assembly. The
instrumented module compiled successfully against the recorded arm64 image.
A solver run and final-state noninterference comparison are still required
before attributing any AMR error change. See the protocol and reproduction
instructions in `protocols/high-gradient-of13-amr-stage-snapshot-v1.json` and
`runtime/openfoam13/README.md`.

## Revision 124 — preserve failed capture attempt and correct stage gates

The first instrumented run completed at `t=0.003` and exited zero, but the
capture gate correctly rejected it: only four named stages appeared, with
repeated PIMPLE callbacks yielding 12 events total. Inspection of the exact
Foundation source showed `mesh_.update()` resets `topoChanged()` before the
mapped callback, and pressure hooks execute once per outer iteration. The raw
v1 case and logs are retained under `work/of13-amr-stage-snapshot-v1/`. Added
v2 with a time-only condition at the call sites (the mapped call itself is
immediately after mesh update) and first/final PIMPLE-iteration guards for
pressure snapshots. This is a protocol correction, not evidence about solver
accuracy. The v2 run and final-state comparison remain pending; see
`protocols/high-gradient-of13-amr-stage-snapshot-v2.json`.

## Revision 125 — separate mapping and post-advance stage times

The v2 attempt completed but omitted `mapped`: source inspection shows
`foamRun` calls `preSolve()` and `mesh_.update()` before incrementing
`runTime`, then enters PIMPLE at `t=0.003`. Thus the mapped state is recorded
at `t=0.002`, while `correctPhi` and later stages are at `t=0.003`. The v2
raw case and logs remain in `work/of13-amr-stage-snapshot-v2/`. Added v3 with
the time gate matched to each call site and separate per-stage output paths.
This is measurement-protocol bookkeeping, not a numerical result. The v3
solver run and final-state noninterference comparison remain pending; see
`protocols/high-gradient-of13-amr-stage-snapshot-v3.json`.

## Revision 126 — first-refinement stage attribution measured

The v3 instrumented n=16 run captured all five stages on one 16,640-cell,
48,816-face topology and completed normally. The final `U`, `p`, `phi`, and
`Uf` files are byte-identical to the frozen uninstrumented control. The
volume-weighted velocity error against exact MMS was 41.7955% after mapping,
41.8156% after `correctPhi`, 41.7898% before pressure correction, and 39.9477%
after pressure/PIMPLE. `correctPhi` changed face flux by 97.35% relative L2
while cell `U` was unchanged; reconstructed volume-weighted RMS `div(phi)`
dropped 89.85%. Pressure correction reduced the velocity error by 1.842
percentage points in this run. Full inputs, raw stage CSVs, hashes, and the
reproducible analyzer are recorded in `evidence/of13-amr-stage-snapshot-v3/`,
`tools/analyze_amr_stage_snapshots.py`, and
`reports/openfoam-amr-stage-snapshot-v3-2026-10-01.md`. This localizes the
observed discrepancy to a state already present immediately after mapping,
but does not distinguish interpolation, gradient reconstruction, timestep,
or model/source effects. It does not establish a solver defect or physical
claim; AMR quality remains UNCERTAIN and no upstream issue is warranted from
this single mechanism probe. The raw provenance JSON's stale checkpoint
description and its correction are transparently recorded in
`evidence/of13-amr-stage-snapshot-v3/provenance-correction.json`.

## Revision 128 — n=32 same-run AMR mapping replication

Added an independent structured-grid predictor for the frozen periodic sensor
and one-layer neighbor buffer. It predicts 12,288 selected cells at n=32;
Foundation 13 logs the same count and refines 32,768 to 118,784 cells. The
same-run mapped velocity equals parent piecewise-constant injection exactly,
with relative parent-volume closure `9.17e-15`. Coarse exact-cell-average DOF
error is 3.4942%, versus 13.7834% at n=16; mapped child DOF error is 21.0789%,
versus 42.4839%, and child-center point-sample error is 20.9906%, versus
41.7955%. The exact-average squared-error decomposition again attributes most
of the child DOF metric to subcell reference-average variation, not a change in
mapped values. This is a two-resolution exploratory mapping replication, not
an AMR quality verdict or physical claim. The compact replay archive preserves
all cell snapshots, inputs and logs; full face data and dynamicCode remain in
the local ignored raw run and are excluded from n=32 conclusions. A packaging
root error was repaired without rerunning, and original malformed tarballs
were preserved under `work/`. See
`reports/openfoam-amr-resolution-replication-2026-10-01.md` and the evidence
directory. Targeted tests: 7 passed. Harness provenance remains limited because
the runner source overlay was dirty at execution and its exact patch hash was
not captured before launch.

## Revision 129 — n=32 fixed-map-time time-step control

Repeated the n=32 first-refinement capture with `dt=0.0005` and
`refineInterval=4`, holding the first map at `t=0.002`; later solver snapshots
are at `t=0.0025`. Foundation 13 again selected the predicted 12,288 cells and
mapped 32,768 to 118,784. Parent injection remains exact and volume closure is
`9.17e-15`. At dt=.0005, coarse and mapped exact-cell-average DOF errors are
3.496856% and 21.079361%, versus 3.494218% and 21.078943% at dt=.001; mapped
point-sample errors are 20.990984% and 20.990564%. These small differences
compare discrete histories with a changed step count/refineInterval and do not
constitute temporal order or accuracy verification. Compact archives retain
all cell snapshots, inputs and logs, with face data excluded and no
flux/divergence claims. See the updated AMR-resolution report and
`evidence/of13-amr-same-run-map-v6-n32-dt0005/`.

## Revision 130 — interior Gauss-gradient and vorticity under AMR mapping

Added a bounded finite-volume gradient/curl replay from cell and face snapshots.
Both stages use a shared physical interior mask aligned two base-cell widths
from periodic boundaries. Relative pointwise-reference gradient error rises
from 26.3494% to 48.3516% at n=16, and 8.7188% to 22.0848% at n=32; vorticity
error rises from 31.0782% to 54.3949% and 9.0557% to 21.5574%, respectively.
At n=32, halving dt changes these mapped metrics only in the last few decimal
places. Of 352,128 mapped internal faces, 147,456 (41.8757%) connect children
of the same parent; their captured Uf equals the injected parent value exactly,
so they add no subcell slope. This is consistent with refining a
piecewise-constant field, not evidence of a solver defect. The gradient is a
specified Gauss reconstruction compared with analytic point derivatives, not
necessarily OpenFOAM's stored grad(U), a cell-integrated norm, or a physical
claim. The n=32 compact archives now retain mapped faces; uniform preMap
gradients replay from periodic centered differences, and later face stages
remain excluded. Analyzer and limits are in
`tools/analyze_amr_gauss_gradient.py` and the updated dated report.

## Revision 127 — reusable analytic cell-average evaluator

Extracted the high-gradient MMS's exact cubical velocity-average formula into
`tools/high_gradient_cell_average.py`, so AMR analysis no longer imports a
grid-audit script that reads fixed n=16 archive data at import time. The
evaluator accepts scalar or per-cell widths, validates geometry and supports
explicit frequency. Added an independent 12-point tensor Gauss test on
nonuniform widths and centers near periodic boundaries, plus invalid-input
checks. The targeted tests pass (6 tests including AMR archive replay), the
existing independent archive probe remains `1.8041e-16` max absolute
difference, and the archived AMR values replay unchanged. This improves the
analytic evidence path; it is not a new solver run, higher-resolution AMR
result, or solver-quality verdict. Commit `696c0b9` is pushed to PR #4;
GitHub Actions run `36867525667` was queued at the latest check.


## Revision 140 — n=128 compact archive revalidated; follow-up literature context

On 2026-10-03, reconstructed the published n=128 AMR compact archive from
its 15 Zstandard parts. The reconstructed gzip archive matches the recorded
SHA-256 `e08e17eaf9789bf5c7cc9d8c368ec48dae2d2104e5d4be457cd39b4d955721bb`;
the independent member verifier again confirms byte identity for the preMap
cells, mapped cells, and mapped-face snapshots against the archived manifest.
The recorded first-map diagnostic has 2,097,152 preMap cells and 6,949,888
mapped cells; its specified interior Gauss point-gradient relative L2 error
changes from 0.6084% to 5.2472%, while same-parent mapped faces carry exactly
the injected parent value. This is a discrete reconstruction/mapping result
for one exploratory event. It neither isolates an OpenFOAM defect nor says
anything about molecular alignment, physical phase change, constitutive
viscosity, or a continuum singularity. A fresh full numerical replay is
resource-intensive and has not completed; the prior stored metric is not
claimed as independently recalculated here.

The 2026-09-17 Constantin–Ignatova–Vicol preprint proves conditional
regularity under anisotropic Type-II and exact-core-axisymmetry assumptions
when the force is analytic; its authors explicitly state that they have not
verified the OpenAI construction. The result is conditional and does not
exclude arbitrary smooth forcing. The 2026-09-08 OpenAI page describes a
continuum Navier–Stokes singularity, not tracked molecules. These sources
reinforce keeping continuum, numerical reconstruction, and microscopic
models separate. No solver-quality threshold or upstream report follows.
The existing PR #4 CI run 37032506247 completed successfully.


## Revision 141 — finite-mesh observation nullspace corollary

Derived a conditional extension of the finite-grid observation argument to
any fixed finite family of finite periodic meshes with closed skeletons that
leave open cell interiors, including ordinary polyhedral AMR meshes. A small
ball can avoid all mesh faces and finitely many prescribed sample points while
lying in one cell of every mesh. Under the torus localized-insertion theorem
in Cao–Chi–Nie arXiv:2609.10262v4, the inserted and reference solutions then
have identical velocity and force cell averages for each mesh, identical
velocity traces/derivatives on mesh faces, and identical velocity/force at the
selected point samples, although the inserted continuum solution is asserted
to become unbounded at the prescribed terminal time. This is an adaptation of
the paper's proof, not a theorem quoted verbatim or independently validated.
It concerns variation of the force and finite-observation identifiability; it
does not contradict fixed-MMS refinement convergence, establish a solver bug,
or imply molecular ordering or viscosity change. Details, proof and limits are
in `reports/finite-mesh-observation-nullspace-2026-10-03.md`. Goal remains
active.


## Revision 142 — acceptance scope now carries the finite-observation limit

Updated `docs/acceptance-gate-v2.md`: local PASS is explicitly restricted to
the frozen MMS, input representation, reconstruction and metrics; finite cell,
face or point observations do not certify a universal continuous peak bound.
A continuum-bound claim now calls for a validated explicit reconstruction or
an independent regularity/unresolved-mode estimate. This is a scope rule, not
a change to any existing numerical verdict. Targeted gate tests pass (14). The
latest PR #4 head is `793bdc46fa798ad1b7e22ee0237755c72cda7142`; its GitHub CI
run `37035369482` is queued. Goal remains active.


## Revision 143 — live PhysicsNeMo records and full benchmark suite

Refreshed NVIDIA/PhysicsNeMo main and existing related issues/PRs. Main is
`83d6a337`; the odd-width spectrum file remains blob `fb3e8cda`, Issue #2007
is open, and fix PR #2008 is open/review-required and diverged from current
main (2 ahead, 12 behind). Periodic derivative behavior and its
consumer-facing documentation gap are already tracked by #1852/#2001 and
draft PR #1853; #1852 is stale but open. No duplicate was posted. Saved exact
metadata and disposition in the dated evidence/report. The full local benchmark
suite on current HEAD completed `212 passed, 1 skipped, 5 subtests passed`;
this does not stand in for the upstream PhysicsNeMo suite. Goal remains active.

## Revision 144 — full local suite preserved as hashed evidence

Re-ran the complete locked Python verification suite on commit
`b6dde6fa5b1014f5149a4ed6ca8e8d119df3b2a3`: 212 passed, one skipped, five
subtests passed. The raw 377-byte log and JSON manifest record the command,
macOS arm64/Python 3.14.5/uv 0.11.17 environment, lockfile hash and output
hash under `evidence/tests/full-suite-2026-10-03-b6dde6f.*`. This is local
benchmark-repository validation, not a full build of the upstream projects.
GitHub Actions for that commit remains queued. Goal remains active.


## Revision 145 — reconcile PhysicsNeMo v2 acceptance scope

Corrected the cross-target hypothesis audit and impact map to include the
prospectively frozen PhysicsNeMo held-out v2 policy: 19/25 checkpoints pass all
six sampled metrics, six fail velocity L2 only, and all 25 pass the sampled
local metrics. No sampled global-pass/local-fail blind spot was observed under
the shared 2%/5% engineering tolerances. Clarified that these are not a
PhysicsNeMo-specific calibration and do not certify continuous extrema,
population-level seed behavior, or optimizer convergence. The v1 comparative
matrix remains historical and now points to v2. No upstream issue or verdict
change follows. Goal remains active.


## Verification addendum — larger cellPoint evidence replay (2026-10-04)

Re-ran `tools.verify_published_cell_point_matrix` at source commit
`4e44429a371ee3e096ce3f74a06b789aa3ea8ef0` in the locked Python 3.14
environment. The n32, n64 and n32 half-step
finite native-query measurements reproduce exactly from the stored JSONs;
all three Arb128 uniform idealized-ball enclosures reproduce byte-for-byte.
The compact receipt is archived at
`evidence/cell-point-matrix-review-2026-10-04/verification.json`. This verifies
postprocessing only, not a new OpenFOAM run or a global/native-floating search
certificate. The separate SU2 matched full-horizon job remains active; the
complete objective remains open.

## SU2 continuation provenance result — 2026-10-04

Hosted continuation v3 replayed the archived baseline and rebuilt the pinned
ARM64 runtime, then stopped before CFL=100 because the new image ID and rootfs
layers differed from the historical image. Binary, patched source, package
versions, compiler, source revision, recipe and container config matched, but
those measurements do not override the frozen image-identity gate. The
rejected artifact and comparison are preserved in
`evidence/su2-full-horizon-control-continuation-37179161618/`. Frozen v4 now
runs both CFL cases on the same saved image shared across two independent
360-minute jobs. That matched pair has not run; overall solver and cross-project
completion remain open.

Hosted run 37180101797 has since passed frozen-input preparation, historical
baseline replay and the shared-image build. Its fresh CFL=10 solver case is
`in_progress`; the CFL=100 job waits on baseline completion. No fresh numerical
result is available yet. A contemporaneous GitHub API snapshot of the three
upstream targets is stored at
`evidence/upstream-refresh/three-project-live-status-2026-10-04T0543Z.json`;
existing tracked issues/PRs remain the right reporting channels, so no duplicate
upstream post was made. Overall goal remains active.

## Revision 146 — matched high-gradient PhysicsNeMo PINN study

The historical PhysicsNeMo PINN matrix uses a different Gaussian MMS from the
OpenFOAM/SU2 high-gradient benchmark. Added a Torch implementation of the shared
periodic Fourier-envelope MMS, checked its values and gradients against the
independent NumPy reference, and verified the full momentum residual with
independent analytic forcing (maximum sampled residual below 2e-11). Froze and
ran the additive 25-model PhysicsNeMo v2.2.1 matrix: five collocation
configurations by five seeds, each with 5,000 updates. All 25 archives, exit
codes, update counts, finite final losses/metrics and SHA-256 digests passed the
run-integrity audit. All 25 failed the preregistered sampled field/derivative
quality gate; their global metrics failed along with local derivative metrics,
so the sampled blind-spot rule was not reproduced. Continuous extrema remain
uncertain, and this is a PINN approximation result rather than evidence of an
upstream solver defect or physical particle alignment. Full results and
limitations are in `reports/physicsnemo-shared-high-gradient-2026-10-04.md` and
`evidence/physicsnemo-shared-high-gradient-v1/`. Focused MMS/reference tests
pass; the attempted full local collection could not start because the available
Python environments lack the repository-wide SciPy and python-flint
dependencies. Goal remains active.

## Revision 147 — full locked-suite replay on the matched-MMS commit

Re-ran the repository-wide suite from PR head `f49a482826f954e4e8f97fa5a1953856f36e54ea`
using `requirements-verification-locked.txt`: 424 passed, four skipped and 89
subtests passed. The two shared-MMS Torch/autodiff tests separately pass in the
recorded PhysicsNeMo v2.2.1 CPU environment with Torch 2.11.0. Commands,
versions, raw logs and hashes are in
`evidence/tests/f49a482-verification.json`. PR #4's Foundation 13 forced-
periodic exact-control check has passed; remaining queued changes checks and
the Python CI job have not completed. Hosted SU2 run 37180101797 is still
reported `in_progress` at the frozen CFL=10 solver step and has exposed no
logs or numerical result. Overall target coverage and the active goal remain
incomplete.

## Revision 148 — independent replay of the complete OpenFOAM matrix index

Ran `tools.verify_openfoam_high_gradient_matrix` against the current six-case
index and its archived inputs. All protocol/index/base-manifest hashes,
archives, logs, endpoint fields, timestep counts, standard acceptance results
and sampled-quality decisions reproduced. All six pass standard acceptance;
n16/n32 at dt=0.001 fail local sampled quality while n64/n128 at dt=0.001 and
both n64 temporal refinements pass. The predefined fine-grid concentration
rule is `NOT_OBSERVED`. The saved 36-record dt=0.0005 attempt is superseded by
the independently archived 100-step completion; no new solver run was needed.
AMR remains a separate pilot with quality `UNCERTAIN`. Receipt and scope are in
`evidence/tests/openfoam-high-gradient-matrix-2026-10-04-b996015.json` and
`reports/openfoam-high-gradient-matrix-recheck-2026-10-04.md`. Goal remains
active.

## Revision 149 — raw-archive replay of the Foundation 13 AMR mean study

Reconstructed the exact experiment harness tree at commit
`3566f89058071910a41bb68010eb258c7bbc3d74`, retrieved all four raw cases from
the existing checksummed GitHub Release, and verified each release digest,
archive-member hash, stage analysis and case manifest. Same-host reanalysis
exactly matches the saved macOS analysis objects; the pinned aggregator exactly
reproduces the matrix JSON: all standard gates pass, the disabled-capture
control is byte-identical, fine-grid derivative-reference controls are
adequate, and n32/n64 fail the specified postSolve mean-quality gate. This
supports `REPRODUCED_SPECIFIED_MEAN_GATE_DISCREPANCY` for that metric only; the
analytic projection decomposition, improving resolution trend and separately
uncertain N=4 peak/spectrum gate do not establish an OpenFOAM implementation
defect or physical mechanism. Full receipt and limits are in
`evidence/tests/openfoam-amr-mean-quality-replay-2026-10-04-b996015.json` and
`reports/openfoam-amr-mean-quality-independent-replay-2026-10-04.md`. No new
upstream post is justified.

## Revision 343 — certified-reference peak sampling diagnostic

Added a supplemental N=4 diagnostic comparing the exact analytic gradient and
vorticity sampled at the frozen uniform cell centers against their newly
certified continuous maxima. At protocol time t=0.05, captured fractions range
from 66.3242%/65.2161% (gradient/vorticity) at n=16 to 99.3972%/99.3871% at
n=128. This measures reference-field undersampling only; it does not bound a
solver field between cells, and it does not modify either gate or its
denominators. The analyzer reports certified continuum values and sampling
fractions separately for N=4; other frequencies receive null for these fields.
Reproduction code, test, JSON receipt, and scope note are in
`tools/measure_high_gradient_peak_sampling.py`,
`tests/test_high_gradient_peak_sampling.py`,
`evidence/tests/high-gradient-cell-center-peak-sampling.json`, and
`reports/openfoam-continuum-peak-sampling-2026-10-04.md`. Full locked local
verification: 432 passed, 4 skipped, 89 subtests passed. The implementation
and receipt are in commit `4d82240c`; the goal-log update and its correction
are in `f0d20541` and `8f6bd69`. All are pushed to PR #4. The latest Python CI
job is still running, so hosted validation is pending. Goal remains active.

## Revision 344 — guard the frequency scope of the continuum diagnostic

Extended the OpenFOAM analyzer regression to verify that the N=4 continuum
certificate is not applied to an N=2 reference: all certificate-specific peaks
and sampling fractions are null for the unsupported frequency. The focused
regression passes, and the subsequent full locked suite passes 434 tests, with
4 skipped and 89 subtests. Hosted CI is pending for the latest PR head. Goal
remains active.

## Revision 345 — decompose archived solver peaks against continuum reference

Replayed all six archived OpenFOAM matrix cases after verifying the frozen
index, protocol, archive hashes, endpoint fields and stored gate decisions.
Compared the certified N=4 continuum maxima with three distinct quantities:
exact analytic derivatives at cell centers, FD2 on exact sampled velocity,
and FD2 on solver cell-centered velocity. At n=64, the solver FD2 peak is
95.027% of the continuum gradient maximum and 95.271% of the continuum
vorticity maximum; the n=128 ratios are 98.738% and 98.802%. Both temporal
refinements at n=64 change these ratios by at most about 0.002 percentage points,
while the finer spatial grid raises them. All six standard/local verdicts
remain exactly as frozen: standard PASS throughout, local FAIL at n16/n32 and
PASS at n64/n128 and temporal refinements; the predefined adequately resolved
blind-spot rule remains `NOT_OBSERVED`. These are sampled FD2/reference ratios,
not continuous solver extrema or a defect claim. Reproduction code and
hash-verified receipt are `tools/compare_openfoam_peaks_to_continuum.py` and
`evidence/tests/openfoam-continuum-peak-decomposition-2026-10-04.json`; scope is
documented in `reports/openfoam-archived-continuum-peak-decomposition-2026-10-04.md`.
The complete local suite passes 434 tests, 4 skipped, 89 subtests. Goal remains
active.

## Revision 346 — hosted replay of the continuum peak decomposition

At commit `1b40ece31627cde6cba6da7e7ba8bb5706dddc2d`, GitHub's full Python
verification job passed: 435 passed, 3 skipped, 89 subtests passed. The local
locked run on macOS passed 434 tests with 4 skipped; the one-test skip-count
difference is environment-dependent and is not a failure. The PR's other
completed Foundation 13 analysis checks pass or are intentionally skipped by
their path filters. A newly started Foundation 13 forced-periodic spatial and
temporal control run has completed its container build and is executing the
frozen cases. The separate SU2 shared matrix and CFL-control jobs remain
in-progress. PR #4 remains open; no solver verdict is inferred until those
archives finish and pass replay. Goal remains active.

## Revision 347 — cross-image replay of the Foundation 13 smooth control

Hosted run `37196452449` from source `1b40ece31627cde6cba6da7e7ba8bb5706dddc2d`
completed the frozen six-case forced-periodic matrix. Independent replay
verified every archive, input/output hash, field diagnostic and exact step
count. All six sets of six scalar metrics match the previously verified run
`37174784940` exactly, despite distinct recorded runtime image IDs and six
different archive hashes; both runs also give identical spatial velocity and
pressure observed orders. The new replay receipt and comparison tool/test are
in `evidence/of13-forced-periodic-control-hosted-1b40ece/`,
`tools/compare_forced_periodic_control_runs.py`, and
`tests/test_compare_forced_periodic_control_runs.py`. The full bundle is
published at release `of13-forced-periodic-control-rerun-1b40ece`; GitHub's
asset digest matches the locally replayed package SHA-256.

The retrospective standard stopping check passes six of six; local quality
and temporal order remain `UNCERTAIN` because this calibration protocol did
not freeze a local threshold and does not isolate temporal error from the
spatial floor. This is not a localized high-gradient or AMR result. The latest
complete local suite passes 436 tests, 4 skipped, and 89 subtests. The
separate SU2 matrix and CFL-control jobs remain in progress. Goal remains
active.

## Revision 348 — third exact replay and hosted control verification

At PR source `739a4bf76cc39b4af3ea8e31b46bdf41cb56120f`, hosted Python
verification passes: 437 passed, 3 skipped, 89 subtests. The local macOS
suite passes 436 tests, 4 skipped, and 89 subtests; the skip-count difference
is environment-specific. Foundation 13 exact-control job `37197955693`
completed all six frozen cases; independent archive/diagnostic replay passes.
Every case's six metrics exactly match both prior verified runs, on three
distinct image IDs, with distinct per-case archive hashes. The third build,
protocol and replay data are durably recorded and its full raw case bundle is
published at `of13-forced-periodic-control-rerun-739a4bf`; GitHub's asset SHA
matches the locally verified bundle. Results remain a smooth periodic
control: quality and temporal order are `UNCERTAIN`, and no high-gradient/AMR
or physical conclusion follows. The matched SU2 matrix and CFL-control jobs
still need completion. PR #4 remains open and the complete goal remains active.

## Revision 349 — separate kinetic crossover from incompressible pressure

Added an analytical scale bridge using the OpenAI paper's reported
characteristic core rate `Gamma_core ~ (T-t)^-1`: for a specified kinetic
relaxation model, `chi = tau_rel Gamma_core` diverges under a fixed positive
relaxation time, while `tau_rel ~ (T-t)^alpha` yields divergence only for
`alpha < 1`. The independent spatial Knudsen ratio has its own exponent and
crossover; neither determines a molecular orientation statistic. Corrected an
important model boundary: the BGK identity `tau_rel = mu/p` uses a
thermodynamic ideal-gas pressure, whereas incompressible NS pressure enforces
`div u = 0` and supplies no temperature/EOS, so it cannot set the theorem's
molecular collision time. The SymPy algebra receipt and focused regression
pass. No kinetic solve, physical crossover time, material transition, or
upstream software defect is established. Goal remains active.

## Revision 350 — refresh upstream scope before any further report

Captured current GitHub REST records for the three solver targets and the
OpenAI formalization repository at 2026-10-04 11:36 UTC. Relevant issues and
PRs still cover the overlapping OpenFOAM viscosity-contrast, SU2 time/residual,
and PhysicsNeMo boundary/spectrum reports; newly opened PhysicsNeMo #2044 is
unrelated. OpenAI still has no GitHub issue/discussion route. No new
reproducible software defect emerged, so no upstream report was posted. Exact
branch SHAs and record metadata are preserved in
`evidence/upstream-refresh/live-status-2026-10-04T1137Z.json`. Goal remains
active.

## Revision 351 — resolve the current state of the partial OpenFOAM case

Rechecked the previously ambiguous n64/dt=0.0005 runner: neither its host
process nor a matching running/stopped Docker record exists now. Its preserved
log ends mid-step at 0.0185 s after 36 completed PIMPLE steps (37 time records),
with no exit receipt or completion marker. Captured the exact log SHA and both
successful state probes in
`evidence/environment/of13-high-gradient-n64-dt0p0005-container-recheck-2026-10-04.json`
and corrected the count in the status addendum. The case remains incomplete;
absence of a container is not evidence of numerical success or failure. Goal
remains active.

## Revision 352 — independently replay fourth smooth-control image

Downloaded Foundation 13 workflow artifact 11302697676 for source `0622352c`.
Independent replay passed for all six archived cases: protocol/archive hashes,
input and endpoint-field hashes, diagnostics, exact step counts, zero exits, and
the existing stopping-condition check. A fourth runtime image reproduces all
six scalar diagnostics per case exactly against the previous three-run matrix;
all raw archive digests differ. Receipt and run metadata are under
`evidence/of13-forced-periodic-control-hosted-0622352/`. Local quality remains
UNCERTAIN, the time-step sweep does not isolate temporal order, and this smooth
control says nothing about concentration or particle-scale behavior. The
OpenAI and three-target solver investigation remains active; no upstream defect
was justified by this control result.

## Revision 353 — test the “light as fluid” analogy against its actual equations

Audited the suggestion using primary photon-fluid and radiation-transport
papers. They describe three distinct regimes: free photons as a phase-space
transport/moment system; radiation viscosity in an optically thick
matter-scattering limit; and optical photon fluids whose Kerr-mediated NLSE
maps exactly to a compressible, inviscid, dispersive Madelung system. Derived
the latter's continuity, phase, and velocity equations and checked their
amplitude/phase identities symbolically with the locked SymPy environment. The
focused regression passes. This is a potentially useful controlled optical
analogue for steepening and dispersive regularization, but it has no viscous
Navier–Stokes term and no molecular-position observable; a dimensional and
forcing map to the OpenAI 3-D incompressible profile has not been established.
The report and receipt are
`reports/light-as-fluid-model-boundary-2026-10-04.md` and
`evidence/analytic-checks/fluid-of-light-hydrodynamic-bridge-2026-10-04.json`.
No simulation or physical-transition claim follows. Goal remains active.

## Revision 354 — identify the scalar photon-fluid swirl obstruction

Extended the optical-field algebra check: a smooth scalar phase has
`v=grad(phi)/k`, hence zero curl; an integer phase winding has quantized
circulation but requires a phase defect/intensity zero. For an axisymmetric
single-valued phase, the azimuthal velocity is identically zero. OpenAI's
source instead specifies a nontrivial axisymmetric swirl while retaining
smoothness across the axis. Thus the standard scalar photon-fluid model cannot
directly reproduce that regular swirl with the same symmetry and positive
intensity. This narrows the proposed analogy without ruling out vector or
multicomponent optical systems; no such mapping is established. The analytic
identities and regression pass, and the report now cites the primary OpenAI
paper for the swirl/smoothness properties. No experiment or particle claim
follows. Goal remains active.

## Revision 355 — independently replay fifth smooth-control image

Downloaded the Foundation 13 artifact for run 37200525739 and replayed all six
cases independently. Protocol and archive hashes, input and endpoint-field
hashes, stored diagnostics, exact step counts, zero exits, and the retrospective
stopping check all pass. All 36 scalar diagnostic values exactly match the
previous four matrices across a fifth distinct recorded image; the archive
hashes differ. Provenance, replay, and comparison are preserved in
`evidence/of13-forced-periodic-control-hosted-d138edc/`. This strengthens
cross-build reproducibility only. Local quality and temporal order remain
UNCERTAIN; no high-gradient, molecular, or physical claim is upgraded. Goal
remains active.

## Revision 356 — independently replay sixth smooth-control image

Downloaded and integrity-checked Foundation 13 workflow run 37201155941 for
source `661a3969e2466bb2473bb52ee32dbd1269813aca`; independent archive replay
passes all six cases, all input/endpoint digests and diagnostics, exact step
counts, zero exits and the retrospective standard stopping gate. Against the
fifth replay (37200525739), all 36 scalar diagnostics match exactly while all
case archive hashes and the recorded image differ. The ZIP checksum, expiry,
manifest, full build provenance, independent receipt and comparison are saved
in `evidence/of13-forced-periodic-control-hosted-661a396/`; raw archives remain
available in the linked Actions artifact until 2027-01-02. Hosted Python
verification at the same source also passes 439 tests, three skips and 89
subtests. One tiny n64 floating-secants cross-platform difference is preserved;
all exact sample/analytic checks pass. The smooth control still does not
exercise concentration, its temporal-order verdict remains UNCERTAIN, and
there is no new upstream defect or physical claim. Goal remains active.

## Revision 357 — complete and independently reanalyze the SU2 full-horizon CFL pair

Hosted run 37180101797 finished its two fresh 50-update, n=32, dt=0.001,
t=0.05 cases in the same immutable ARM64 image. Its image receipt matches image
ID, source, architecture, build-input digest, SU2 binary, patched source,
package inventory and compiler. Both cases exited zero and passed recorded
physical-update/time-grid checks. I downloaded and checked paired artifact
11303655387, then reran the raw-output review locally; the old archived baseline
also passed its separate replay. CFL=10 met the per-update inner residual limit
on 48/50 updates, while CFL=100 met it on 50/50. Both failed all four frozen
solution-quality gates; their four metric values differ by at most 5.85e-10.
Thus only inner-iteration convergence changed in this pair, not sampled solution
quality. Full raw paired evidence, independent review, image-match receipts,
metadata and a replay command are in
`evidence/su2-full-horizon-cfl-pair-37180101797/`. The pair is too limited to
establish general CFL behavior or an upstream defect; adjacent SU2 issues
#2353/#2932 concern different questions, so no issue was posted. Continuous
extrema and all broader cross-solver/physical goals remain open. Goal remains
active.

## Revision 358 — independently replay seventh Foundation 13 smooth-control build

Hosted run 37202786082 completed all six spatial and temporal cases from
`5b60a879d30aab6cb9e10a49f5ada64520c2728c` on a distinct ARM64 image. The
downloaded artifact passed local archive/diagnostic replay, including the
recorded input and endpoint hashes, exact time grids, zero exits and the
retrospective Foundation stopping gate. Against run 37201155941, all 36 scalar
metrics agree exactly while all case archive hashes differ. Replay, provenance,
comparison and retention metadata are saved in
`evidence/of13-forced-periodic-control-hosted-5b60a87/`. Spatial orders
reproduce; temporal order remains UNCERTAIN because the spatial error floor is
not separated. This smooth control does not test concentration, molecular
alignment, or a constitutive transition. The whole-repository objective stays
active.

## Revision 359 — analytically preflight concentration-width sensitivity

Extended the independent localized-MMS reference to the smooth periodic family
`h_m(q)=((1+cos(q))/2)^m`, retaining the original m=4 evaluation path exactly.
SymPy differentiation, solenoidality checks and a 444-test full suite pass.
The reference-only FD2 audit spans m=1,2,4,8,16,32 and n=16,32,64,128; m=4
reproduces the old receipt exactly. It reveals that m=32 at n=64 has only two
cells per highest envelope wavelength even though the aggregate peak floor is
under 5%, so peak metrics alone can hide unresolved modes. No solver was run
and no defect or physical claim is made. The new reference-width audit and
proposed mode-resolution guard are in
`reports/high-gradient-width-sweep-analytic-prefight-2026-10-04.md`; the next
step is to adapt OpenFOAM's analytic forcing to selected widths and preregister
the solver matrix with independently verified spatial support and sampling.
The whole-repository objective remains active.
