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
