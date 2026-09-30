# Goal — revision 2, 2026-09-09

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
