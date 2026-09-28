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
CFD solvers. At the latest observation the existing n=128 Foundation 13 job
remains live at t=0.033s.

## Revision 12 — high-gradient AMR input-generation checks

Three new unit tests exercise the high-gradient AMR case generator: sensor
creation/update and boundary correction, refinement limits/budget, and the
minimum refine interval needed to initialize the sensor. They pass but do not
test OpenFOAM's runtime adaptation or mesh-level/budget behavior. The original
uniform n=128 process remains live and has reached t=0.027s; uniform/time and
high-gradient AMR solver matrices remain incomplete.
