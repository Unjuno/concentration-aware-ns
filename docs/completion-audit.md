# Completion audit — interim, 2026-09-27

The project is **not complete**. This audit preserves the original three-target
scope and the user's analytic-priority requirement. Published artifacts and
measured behavior take precedence over prior progress summaries.

The table was refreshed on October 1; dated entries below retain historical
run scopes. The [impact-scope report](../reports/impact-scope.md) now maps each
finding to a supported improvement and the evidence required to extend it.

| Requirement | Inspected evidence | Current conclusion |
|---|---|---|
| One project repository | Current git remote, public Unjuno/concentration-aware-ns | Satisfied; upstream sources held as archives, no extra project fork |
| Source/version/license audit | docs/audit.md, runtime recipes, pinned source files | Three targets identified; runtime dependencies have stated reproducibility limits |
| Analytic reference and force | reference.py, symbolic, C++, autograd and energy/Fourier checks | Verified in stated scopes; no physical blow-up inference |
| OpenFOAM 3-space/multiple-time comparison | Five archives in evidence/of13-study-v1 | Runs complete; three tighter-iteration controls add 350 converged steps without changing endpoints materially or the observed order 0.493. Asymptotic temporal convergence remains unproved. |
| High-gradient OpenFOAM v2 space/time matrix | `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`; base manifest and temporal addendum | All six cases complete. n64 dt=.0005/.00025 both pass standard/local gates; the fixed three-step comparison is descriptive only. Matrix concern (standard PASS/local FAIL at both n64/n128) is NOT_OBSERVED. |
| OpenFOAM solver rerun reproducibility | [Single-case repeat archive, provenance and comparator](../evidence/of13-high-gradient-repeat-2026-10-01/README.md) | A fresh n=64, dt=.0005 run on the recorded image completed 100/100 steps. All four endpoint fields and five diagnostics reproduce byte-for-byte/exactly against the earlier archive. Comparator provenance checks and four hostile fixtures pass; only five declared raw archive members may differ. This is one-case reproducibility, not a general guarantee or physical validation. |
| AMR constraints and controls | AMR, event, fixed-mesh, and `div(phi)` manifests | Three budgets and two fixed-mesh controls complete. Whole-level selection explains the observed approximate-cap overshoot. Fixed-mesh errors fall to 1.88%/0.483% from AMR-path 37.0%/40.1%. Discrete endpoint and logged time-step continuity residuals remain tiny in all cases; this does not identify the momentum/transfer error source. Quality remains UNCERTAIN. |
| SU2 3-space/multiple-time comparison | All five archives; archive-review.json, diagnostic-replay.json, su2-time-comparison.json | Matrix complete and diagnostics replayed. Direct endpoint differences give observed order 0.99916; inner residual failures prevent an error certificate. |
| PhysicsNeMo 3-space/multiple-time sampling | Original five archives plus 20 preregistered added-seed archives; reports/physicsnemo-study-v1.md and physicsnemo-seed-control-v1.md | Five seeds per case complete. Spatial paired contrasts have mixed signs; temporal-node contrasts lower sampled velocity error in all five seeds, with small descriptive changes. Material seed sensitivity is observed. Optimizer convergence and continuous-peak uncertainty remain; acceptance stays UNCERTAIN. |
| Local derivatives and spectra | Native/autograd/FD2/spectral comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker; evidence/tests/gate-artifact-audit.json; internal timestamp-sequence audit; `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json` | Eleven reports (OpenFOAM n32, PhysicsNeMo five, SU2 five); all 93 artifact links match. Verdicts remain UNCERTAIN with gaps explicit. The run-level parser's duplicate/skipped-time false-pass was found synthetically and corrected. The current six-case OpenFOAM uniform matrix is complete; its four original fixed-step archives pass the sequence check, and the two later temporal addenda independently validate 100/100 and 200/200 completed steps. |
| Genuine upstream reporting | SU2 Q&A 2890 and issue #2353 with read-back verification | BDF2 order-reduction control and restart-dependent MAX_TIME stopping consequence reported; no general-fix claim |
| Other target report/no-report decisions | Interim audit and contribution policies | Explicit no-defect-report decisions for OpenFOAM and PhysicsNeMo are recorded in reports/upstream-disposition.md; the SU2 BDF2 finding is scoped separately |
| OpenAI construction audit and transfer | Independent NS kernel logs for both pins; current source-bound extension checks; docs/axis-flow-derivative.md; docs/packet-constant-dependencies.md; conditional Jeffery bridge in docs/fiber-vortex-literature-audit.md | Full axis Jacobian, explicit variational solution, inverse identity and eventual axis smoothness are Lean-checked. The cusp-ball theorem supplies a field-equality radius proportional to `sqrt(1-t)` and transfers the base endpoint Hessian exponent `kappa=40` to the full spacetime jet on that ball. `SpatialHessianTransfer.lean` composes the local `ContDiffAt` spatial restriction with the selected-field estimate and is Lean-checked with an axiom audit. The classical nonlinear packet comparison remains outside Lean, so `Cstretch+39` is a conditional, non-effective shrinking-packet allowance; `Cstretch<4` gives a more conservative conditional `Q^43` sufficient packet-radius power under the same envelopes. Neither gives a fixed-packet certificate. Nonlinear-flow identification remains classical; there is no end-to-end Lean flow theorem. The Jeffery model matches the infinitesimal angle exponent only under prescribed spatially uniform axisymmetric strain. The strict negative force-ratio limit still requires the unresolved actual-profile pressure premise. The pinned Euler challenge has passed recorded independent checks; this does not establish molecular or constitutive consequences. Executable finite-stage extraction remains unperformed. |
| User-proposed Burgers feedback and particle interpretation | `reports/recent-developments-and-hypothesis-audit-2026-09-28.md`; `tools/check_burgers_feedback_mapping.py`; arithmetic record in `evidence/tests/burgers-feedback-mapping.json` | Under an imposed linear strain, the Gaussian-vorticity width equation yields the familiar diffusion-versus-strain threshold. The extra `a=kappa W_peak` closure is not derived from Navier–Stokes; its parameterization matches the known singular Burgers-vortex family, which has spatially growing linear strain. The OpenAI-core comparison only tests pointwise vorticity on one selected trajectory, not global peak vorticity. No particle-probability, molecular alignment, phase-transition, or constitutive-viscosity result follows. |
| OpenFOAM n=64 endpoint pressure reconstruction | v3 frozen protocol, three Docker archives, and independent archive replay | All three dt cases exit 0; U/p/phi are byte-identical to same-dt baselines, and endpoint velocity algebra replays at 2.12e-16–2.15e-16 relative L2. Narrow endpoint gate passes; trajectory cause, molecular alignment, phase change, and material-viscosity claims remain unsupported. |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results; [fresh export record](../evidence/clean-export-2026-10-01-current/README.md) | The tracked-only clean export at `33c4607` passed 26 replay steps and all six additional checks in a fresh locked venv; all 152 report/test-evidence files were byte-identical. The replay now runs the complete pytest suite. Solver rebuild/reproduction remains separate. |

The latest fixed-revision clean-export summary and command logs are public in
[`evidence/clean-export-2026-09-30-current/`](../evidence/clean-export-2026-09-30-current/README.md).
This strengthens reproduction of tracked Python evidence only; it does not
reproduce a solver, training run or Lean build.

### Analytic result refreshed 2026-09-30

The OpenAI extension was re-run in the pinned Lean checker environment from the
current `verification/AxisForceSign.lean`; its 21,306-byte output is byte-equal
to `evidence/lean-verification/axis-force-sign.log`, and the source hash matches
`axis-force-sign.json`. It reports only `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorryAx`. The checked chain includes the selected
candidate's full axial Laplacian limit, material acceleration, and their ratio.
For a root in the prescribed interval, `actual_ratio_negative_of_local_Z`
proves a strictly negative, nonzero limit under the local pressure-moment
condition `Z>0`; `outgoing_root_Z_positive_iff_moment_threshold` gives its exact
moment inequality. This sharpens the sufficient premise from global
`PressureData`. Neither premise has been shown for the arbitrary
`FinalSlowBase.actualProfile` choice, so the conclusion remains conditional at
that selection boundary. It concerns viscous force divided by material
acceleration on one trajectory, not a constitutive-viscosity law or molecular
alignment. The `AxisForceSign.lean` ratio and moment-threshold proof closure
has now passed an independent nanoda check (85,455 declarations, zero
typechecker errors); its hash manifest and rerun script are in
`evidence/lean-verification/axis-force-nanoda-2026-09-30.json` and
`runtime/lean-verification/check_axis_force_nanoda.sh`. The separate
`SupportHoleAssembly.lean` cusp-ball and Hessian-transfer extensions have
pinned Lean elaboration and axiom-audit records, including the ten-declaration
v6 run cited below, and have now passed an independent nanoda check of 85,487
declarations with zero typechecker errors. Nanoda reported one pretty-printer
error (`Unable to print axioms`); the separate Lean audit printed the allowed
axioms for all ten target declarations. The run manifest and rerun script are
`evidence/lean-verification/support-hole-nanoda-2026-10-01.json` and
`runtime/lean-verification/check_support_hole_nanoda.sh`. Conditional
parameter assumptions remain. The local `ContDiffAt` restriction inequality
and its composition with the selected-field cusp-ball Hessian theorem are now
compiled and axiom-audited in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`.
The classical nonlinear packet comparison remains outside Lean. The
AxisForceSign, SupportHoleAssembly, and spatial-Hessian transfer checks are
distinct proof closures.

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.

Current report and exact-algebra replay covers eighteen steps, including all five SU2 archive
reviews, diagnostic replays, spectral derivatives, direct temporal differences
and gate generation, including the separate BDF2 control, root-pressure identities,
pressure-moment threshold, cone sign symmetry and archived Dirichlet boundary-time
pilot. The current 50 tests and 93 matching artifact links
verify their stated implementation and provenance scopes, not continuum accuracy.
PhysicsNeMo's missing preregistered threshold remains a limitation that cannot
be repaired retrospectively.

Remaining completion work:

1. Comparative audit now exists at reports/comparative-audit.md. Retain its
   bounded conclusions: no certified standard-PASS/local-FAIL case is established.
2. SU2 observed aggregate checks are now included in each case report with a
   hashed review artifact and archive-identity check. All five observed
   conjunctions fail. Their post-hoc definition remains distinct from a
   preregistered acceptance gate; continuous-peak and inner-iteration uncertainty
   remain. OpenFOAM and PhysicsNeMo standard-acceptance limitations remain recorded.
3. Independently review the new source-to-trajectory implication chain; symbolic
   identities do not cover theorem hypotheses. New Lean proofs now establish the chart derivative chain through the natural
   profile, including a root with eventual negative derivative, the selected base-field vector material trajectory, and its axis Laplacian identity. An independent symbolic Eulerian material-acceleration calculation agrees with the trajectory formula. Current Lean proofs establish the physical Laplacian/material-acceleration limit and strict negative sign under explicit root and PressureData assumptions. Unconditional instantiation for actualProfile remains unproved. Do not describe original kernel acceptance
   as verification of our new result.
4. Tracked-only export and fresh-venv postprocessing succeeded (see
   evidence/fresh-environment-check.json). SU2 discussion now has a September 13 response; the September 26 BDF2 follow-up reproduces the suggested order-reduction control and is posted with raw evidence. No general-fix endorsement is inferred. Full solver builds were not
   repeated by this postprocessing check.
5. Audit the requested impact analysis against what the evidence supports.
   No finite benchmark can establish all industrial or molecular consequences;
   reports/impact-scope.md now bounds findings by solver versions, cases and
   construction hypotheses. Effective finite-packet bounds and the actual-profile
   pressure premise remain unresolved; publication of the scope report does not
   discharge them.

September 27 reconciliation and replay: all thirteen archived-input replay
steps completed with exit code zero, including 36 tests and 93 matching artifact
links. Comparison values and localized verdicts did not change. Both existing
125-declaration Lean results still match the current extension source and log
hashes; no new Lean execution is claimed by this reconciliation. The comparative
report now includes the six BDF2 controls and distinguishes checked deformation
components from the classical nonlinear-flow argument. No new solver runs,
training runs, upstream messages or theorem changes occurred in this audit.

This remains an interim audit, not a declaration that all goal requirements
have been completed.

### Quantitative copy-support hole, 2026-09-28

The updated OpenAI source's `SupportData.sum_support` now feeds a new Lean
extension, `verification/SupportHole.lean`. The theorem
`copy_sum_zero_below_physical_hole` proves that a supported copy-family sum
vanishes whenever its physical transverse radius is below
`a*sqrt(physicalQ/2)`. The proof uses the dyadic active-band comparison and
the annulus-to-physical-radius identity, and compiled with the pinned checker
environment. This is a generic primitive-family result. It does not yet show
that all actual candidate stages, direct curls, and the full cutoff series
share one coefficient on a complete tube. The packet-radius transfer and
completion verdict therefore remain unresolved; see
`docs/packet-constant-dependencies.md`.

### Conditional cusp-tube chart estimate and source-bound correction

The similarity equation `tau=q-z^2 q^(2h)` yields the normalized coordinate
`F(eta)=eta*(1-eta^2)^(-D)`, `D=1/2-h`. Its derivative factors as
`(1-eta^2)^(-D-1)*(1-2*h*eta^2)`, bounded below by `1-2h>0` on `|eta|<1`.
This gives a uniform inverse bound: an axial displacement of at most
`c*sqrt(tau)` around the selected axis curve changes eta by at most
`c*tau^h/(1-2h)`. Conditional on a common primitive inner-support coefficient
`c0`, choose c smaller than both `c0` and the chart-margin allowance. For
sufficiently small tau, the full spatial ball of radius `c*sqrt(tau)` remains
inside the physical sublevel and spatial/time localization plateaus, and lies
inside the proposed support hole. The exact algebraic identities are checked
in `evidence/tests/support-hole-tube-geometry.json`; derivation and explicit
smallness conditions are in `docs/support-hole-tube-geometry.md`. The
conditional existential cusp-ball interval and actual selected-field local-
germ equality now pass the pinned Lean check and axiom audit in
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/`. It remains a shrinking-
ball continuum result with conditional parameters; it is not a finite-size
packet theorem or numerical packet certificate.

This audit also corrects a source-description error in an earlier note:
OpenAI's `SublevelShrinkingSupport` is an outer support bound (nonzero values
have radius at most the stated shrinking outer radius). It does not establish
an inner hole. The candidate hole depends on separate lower annulus bounds;
selected-stage transfer, cutoff sums, curl, and final-field equality remain
unproved.

Correction to analytic evidence: the force-ratio geometric factor d=1-eta²
was inverted in earlier revisions. Current symbolic and Lean sign checks
use -nu*d*Z/(L*A*U). The historical fresh-environment check-3.log records
the superseded formula and is retained as a run record, not evidence for
the corrected coefficient. The current axis-force symbolic JSON and Lean
verification JSON contain the corrected run. Strict negativity survives;
physical-force identification is checked conditionally; unconditional pressure instantiation remains incomplete. See the pressure-hypothesis retention audit in docs/openai-core-material-trajectory.md.

Verification-gate fault injection (2026-09-26):
`python3 -m unittest discover -s tests -p test_axis_verifier.py -v` passes five
checks. The recorded successful axiom output is accepted; a failed subprocess,
a missing required axiom report, a forbidden sorryAx, and source mutation during
the mocked run are rejected with CLI exit code 1. Fixtures and outputs live in
temporary directories, so this check does not overwrite published proof evidence.
These tests exercise the Python acceptance/exit-code path, not Lean itself, and
do not discharge the actual-profile pressure condition. No new Lean replay is
claimed from this test run.


Current-checkout report replay (2026-09-26): all twelve steps completed with
exit code 0, including 36 tests and all 88 artifact byte-identity checks.
Only the test log and its recorded hash changed during regeneration; generated
comparison values and gate reports were unchanged. The run is recorded in
`evidence/report-replay/summary.json`. It is a replay of archived-input
postprocessing, not a fresh solver, training, or Lean run. Historical fresh-venv
records retain their own earlier scope and are not relabeled as this run.


SU2 aggregate-review integration (2026-09-26): the report builder now carries
velocity, energy and all-step residual observations from
`evidence/tests/su2-standard-review.json`, hashes that artifact and checks that
each reviewed archive matches the case archive. It no longer incorrectly says
that energy review is absent from the report. This addition does not change the
conservative gate flags or promote post-hoc observed FAIL to a preregistered
standard-acceptance decision. The raw review can be regenerated separately with
`python -m tools.review_su2_standard` in the verification dependency environment.

The integration replay passed all twelve steps and 36 tests; all 93 artifact
links match (five additional SU2 aggregate-review links). All eleven gate
verdict files are unchanged.


The forcing-scope comparison is now explicit in
`reports/forcing-scope-audit.md`: the implemented manufactured force is analytic
for fixed positive sigma, while the construction and later regularity/density
results have different forcing quantifiers and hypotheses. This addresses part
of the impact audit without extending any numerical verdict to singularities.
Full follow-up-paper proof review and updated-source compatibility remain open.


BDF2 follow-up replay integration (2026-09-26): the common replay now has thirteen
steps, including raw-archive BDF2 recurrence and endpoint-error verification.
All thirteen completed successfully, with 36 tests and 93 gate artifact links.
The six BDF2 control runs are separate from the eleven localized acceptance
reports; their successful residual and recurrence checks do not change those
UNCERTAIN verdicts. The updated OpenAI assembly build and unchanged extension check have now completed successfully; see evidence/upstream-refresh/updated-verification-summary.json. New-pin independent Comparator/nanoda verification subsequently completed successfully for the R3 and periodic challenge; evidence/upstream-refresh/updated-comparator-result.json records it. Neither check discharges the pressure premise.


Clean-export refresh (2026-09-27, commit `60302db`): thirteen replay steps and
five additional checks exited zero in a fresh same-host environment. Strict
byte equality failed in six of 66 compared files. All inspected differences
were NumPy version metadata and propagated hashes; numeric results/verdicts
were unchanged. See `evidence/clean-export-2026-09-27/README.md` for the exact
scope, preserved failure, differences and logs. This adds reproducibility
evidence without discharging the open physical, analytic or formal premises.


Integrated pressure-analysis replay (2026-09-27): all sixteen steps exited zero,
including 45 tests and 93 matching artifact links. The three added algebra
checks reproduced their existing JSON exactly; existing comparison values and
gate reports were unchanged. The current replay requires
`requirements-verification.txt` for SymPy and SciPy. Logs and hashes are in
`evidence/report-replay/summary.json`. This is not a new clean-export, solver,
training or Lean run, and it does not resolve the actual-profile pressure gap.


Boundary-pilot replay integration: all seventeen steps completed with exit code
zero, including the raw two-variant/two-step boundary checker, 45 tests and
93 matching gate artifact links. This checker independently selects nodes by
mesh numbering and reads residuals and time labels from the archives. It adds
no temporal-order or restart claim. The existing localized gate verdicts remain
UNCERTAIN. Separately, the current 149-report Lean extension now derives actual
physical-ratio negativity from local Z>0, without global PressureData; the
actual outgoing weighted-moment threshold is equivalent to that local sign
condition. Its satisfaction for the selected profile remains unproved.


Restart-finding replay integration: the current eighteen-step replay completes
with 50 tests and 93 matching gate artifact links. Its restart step reruns the
raw checkers and accepts only the specific field-agreement/history-mismatch
result for both R=2 and R=3. Scientific history-time continuity remains FAIL;
reproduction success does not relabel it. Five fault tests reject wrong exit
codes, missing rows, wrong times and nonfinite/large field differences.
No new solver or Lean run is part of this integration.


Locked-dependency replay: at commit `5b8e305`, a fresh tracked-only export
passes eighteen replay steps and five additional checks; all 75 compared
report/test files match byte-for-byte. Evidence is in
`evidence/clean-export-2026-09-27-locked/`. This closes the observed dependency
version drift for that explicit same-host configuration. Supported-range
NumPy 2.5.3 failures remain preserved, and no cross-platform, solver-build,
training or Lean reproducibility conclusion is added.


## Current next-action audit after startup controls

The completed work narrows rather than closes the remaining numerical question.
The three tight-iteration runs and archive-only replay rule out a material
endpoint response to those specific tolerance changes. Constructor probes
establish the initial discrete face-flux mismatch. Two completed early-time
runs and an unfitted leading Poisson model support a startup pressure/velocity
response, but do not establish its causal role in later-time order reduction.
Spatial operator checks show this initialization correction shrinks with mesh
refinement; none of these results proves a physical singularity.

Required next evidence, in dependency order:

1. Resolve the actual state of the pending dt=0.00025 startup request. Its host
   process remains live and a Docker daemon ping timed out; no replacement run
   is justified solely from that observation. Preserve the two completed cases.
2. Complete the three-case common-endpoint startup comparison. The published
   comparator requires all cases; partial pressure/velocity evidence is labeled
   separately and cannot be promoted to a three-level result.
3. Execute the frozen initial-divergence intervention once Docker is responsive.
   All three prepared input manifests pass, and only initial U differs. A
   successful prediction would identify the initial impulse's dependency on
   initial discrete divergence, not certify the original MMS acceptance gate.
4. Only then select an experiment to test whether that startup mechanism affects
   the t=0.05 temporal result. Avoid treating a changed initial-value problem
   as a repair of the original benchmark or assuming its result in advance.

At the historical update, the common replay had 25 passing steps and 59 tests.
It includes a fresh six-archive OpenFOAM comparison reconstruction, the SU2
output-clock replay, exact uniform-prefix threshold algebra, and the localized
high-gradient MMS plus its independent symbolic-versus-NumPy derivative
comparison. It excludes solver runs for that new MMS case.
The analytic actualProfile moment/amplitude obligation and non-effective
packet constants remain unresolved. Whole-goal completion is not established.

### Startup intervention completion update

The original pending baseline completed without a task-issued runtime restart;
all three baseline and all three solenoidal control cases are now complete.
`reports/openfoam-solenoidal-startup-control.md` records the observed suppression
of the leading startup pressure impulse and its limits. Steps 1–3 in the
next-action list above are now satisfied. Step 4 (late-time causal attribution)
and the independent analytic obligations remain open. The new control archive
reader passes on the real six-archive comparison; this does not change any
original acceptance gate or claim whole-goal completion.

### Replay integration on 2026-09-28 JST

The common replay now includes the completed archive-only solenoidal startup
comparison: 22/22 steps pass using
`work/clean-export-2026-09-27-locked/venv/bin/python -m tools.replay_published_reports`.
The original system-Python attempt failed at step 15 because SymPy was absent;
its summary and error log remain in
`evidence/report-replay-missing-sympy-2026-09-28/`. This is an environment failure,
not a numerical finding. The successful run uses the existing locked-dependency
venv against the current checkout; it is not a new clean-export or solver replay.
The startup diagnostic JSON was regenerated without a tracked difference.
At this historical replay checkpoint the late-time v2 intervention was still
running; it completed afterward, as recorded in the following section.

### Late-time intervention result

All three v2 late-time controls are complete and the six-archive comparator
passes. Projecting initial U changes observed temporal order from 0.49291429
to 0.49948838; the late-time anomaly persists despite the early impulse
suppression. The planned initialization-sensitivity experiment is complete,
but it does not resolve the original temporal acceptance gap. See
`reports/openfoam-solenoidal-late-control.md`. Whole-goal completion remains
unproven, including the independent analytic obligations.

The common replay has been extended with the archive-only n=16 pressure
reconstruction pilot. In the locked-dependency environment, 23/23 replay steps
pass. The pilot proves byte-identical endpoint fields under diagnostic
instrumentation and verifies the final-call pressure/velocity algebra at
roundoff. It does not yet attribute the n=64 temporal discrepancy; an instrumented
three-dt run is now complete for its endpoint-only gate; see the update below.

### n=64 pressure endpoint reconstruction, 2026-09-28

The frozen v3 three-dt OpenFOAM 13 diagnostic matrix completed and its retained
archives independently replay. Each run exited zero and has same-dt byte identity
for endpoint U/p/phi. This closes that experiment's endpoint gate only; it does
not identify the temporal-order mechanism or support molecular/constitutive
claims. The locked environment completed all 23 configured report-replay steps. The
whole project remains incomplete under the unresolved analytic and solver gates
listed above. See `reports/openfoam-pressure-reconstruction.md` and
`evidence/of13-pressure-reconstruction-n64-v3/`.

### Directional-alignment audit, 2026-09-28

The selected continuum deformation now has an explicit angle formula for
infinitesimal separations and a conditional finite-packet angle bound with its
exceptional transverse subspace stated. The finite-packet bound still needs
effective tube-radius and Hessian constants and does not model molecules. Exact
linearized squared-ratio algebra passes the pinned Lean runner; the nonlinear
finite-packet estimate remains classical and conditional. The separate SymPy
identity checks are in `evidence/tests/axis-directional-alignment.json`. See
`docs/axis-directional-alignment.md` and
`evidence/lean-verification/axis-force-sign.json`.

The finite-packet note now converts a target angle into explicit angle-error
and tube-exit bounds on the initial radius. The formula is symbolically checked,
but selected-profile values for `rho(T)` and `M(T)` are still missing, so no
numerical packet is certified.

### Post-announcement density-paper intake, 2026-09-28

The current arXiv v4 of 2609.10262 and its linked formalization project were
inspected. The article claims force-space density thresholds from a compact
OpenAI forced-blowup input; its Lean repository maps 27 article results and the
latest recorded GitHub Actions run passed the architecture and Lean-contract
jobs. Our local external-source checks are static only; a local Lean build was
not run because the pinned Lean toolchain is unavailable in this environment.
The downstream formalization therefore does not independently verify the
OpenAI seed. “Dense” here refers to specified forcing norm topologies, not
probability or molecular alignment. The result supports keeping forcing input
identity and spectrum auditable across solver resolutions, but does not alter
the frozen benchmark gates, solver verdicts, or upstream-reporting decisions.
The version-history correction, dependency boundary and evidence record are
in `docs/openai-refresh-2026-09-28.md` and
`evidence/upstream-refresh/force-density-2026-09-28.json`. Whole-goal
completion remains unproven.

### Independent recent-work scan, 2026-09-28

The 20 September *Positive Defect Problem* preprint was reviewed alongside the
OpenAI source refresh. It provides a distinct, machine-checked reduction from
positive energy defect to an averaged fine-shell energy-flux floor, but says a
finite Galerkin computation cannot certify that uniform condition. No existing
MMS run tests this target, and the paper supplies no microscopic alignment
bridge. The finding is recorded as a research direction only; gates and
verdicts are unchanged. See the added subsection in
`docs/openai-refresh-2026-09-28.md`.

### Direction probability versus spatial concentration, 2026-09-28

The audited local deformation gives a conditional closed-form probability that
an isotropically sampled infinitesimal separation lies within a chosen angle of
the axis. Its limit is one as the singular time is approached. The same map has
unit determinant, so an initially isotropic Gaussian retains its peak density
and differential entropy while becoming transversely narrower and axially
wider. The symbolic identities pass in the reference-check environment. This
sharpens the user's direction-alignment idea while rejecting the inference that
it establishes concentrated absolute positions or molecular predictability.
Finite-packet and kinetic-model premises remain open; the acceptance gates and
solver verdicts are unchanged. See `docs/particle-position-probability.md`.

In the global affine tangent-map toy calculation, observation regions separate:
mass in any fixed-radius infinite axis tube tends to one, while mass in a fixed
finite cylinder is asymptotic to `sqrt(2/pi)*L*Q^C` and tends to zero. This
illustrates how transverse localization can coexist with increasing axial
uncertainty, unchanged peak density and constant differential entropy. The
actual nonlinear-flow theorem does not establish the affine map on an
unbounded Gaussian cloud. Symbolic limit checks pass after substituting
`z=Q^C`, which avoids a symbolic-exponent limitation in the CAS. No microscopic
or finite-packet claim is added.

### Conditional finite-packet radius scaling, 2026-09-28

The classical tube and angle-error sufficient conditions were combined under
explicit endpoint envelopes `rho(Q)=rho0*Q^r` and `k(Q)<=k0*Q^-kappa`.
Splitting `kappa-r-1` by sign gives a joint sufficient initial-radius power
`Q^(C+max(r,kappa-1))`; for `C>1`, this tends to zero. The new SymPy check
verifies the integral bound and piecewise exponent identities. Neither the
endpoint envelopes nor their constants are established for the selected
profile, and the result is not a fixed-packet counterexample. See
`docs/axis-packet-bound.md` and `evidence/tests/packet-radius-scaling.json`.

### Current archived-report replay and selected-profile gap, 2026-09-28

The locked-dependency replay was rerun against the current checkout:
`work/clean-export-2026-09-27-locked/venv/bin/python -m
tools.replay_published_reports`. All 23 configured steps exited successfully;
the acceptance-audit suite ran 54 tests and the artifact audit matched all 93
links. This is archived-input report and exact-algebra replay only. It does not
include new solver, training, or Lean execution and does not alter any scientific
verdict.

The source audit reconfirmed a material instantiation gap. In the pinned OpenAI
source, `FinalSlowBase.actualProfile` is `Classical.choice profileData_nonempty`;
the `ProfileData` record retains nominal, cone and modulation witnesses but no
explicit amplitude lower bound or `PressureData` field. Our Lean extension
constructs a separate pressure-qualified `ProfileData` from
`PreparedOutgoing.exists_prepared`, but explicitly does not identify it with the
upstream choice. Thus existence of a pressure-qualified profile does not yet
establish the negative force-ratio result for the selected profile. This is not
an upstream counterexample or evidence that no implication follows from the
retained fields; deriving that implication or changing the selected construction
remains open. The replay and source cross-reference are recorded in
`evidence/report-replay/summary.json`, `evidence/report-replay/tests.log`,
`docs/pressure-moment-threshold.md`, and `verification/AxisForceSign.lean`.

### Localized high-gradient manufactured solution, 2026-09-28

Added a second analytic periodic transient MMS candidate with vector potential
`A=(0,0,exp(-t) chi(y,z) sin(Nx)/N^2)`, where
`chi=((1+cos y)/2)^4 ((1+cos z)/2)^4`. Exact symbolic checks verify
divergence-free velocity, the time-dependent forced Navier–Stokes identity, its
selected derivative and vorticity formulas, and the envelope's finite Fourier
expansion. Orthogonality gives exact t=0 volume means for `N=4,8,16`. The
velocity supremum is bounded above by `exp(-t)*(1/N+2/N^2)`, while
`partial_x u_y` attains `exp(-t)` at the localized envelope center; this
analytically separates small velocity amplitude from an order-one local
derivative.

This case is now in `docs/protocol.md`, `tools/check_high_gradient_mms.py`,
`tests/test_high_gradient_mms.py` and `evidence/tests/high-gradient-mms.json`.
The locked report replay then had 25 successful steps and 59 tests. A second
implementation evaluates fields from hand-coded Fourier derivative formulas;
direct SymPy differentiation agrees for velocity, gradient, vorticity and
forcing at 65 seeded points for each `N`, with maximum component error below
`2.3e-16`. OpenFOAM's case generator now emits the matching time-dependent
`codedFvModel`, and a unit test reads back the generated cell initialization.
The original Foundation 13 matrix and quality thresholds are preserved in
`protocols/high-gradient-of13-v1.json`; before any solver run, the FD2
reference-only floor audit showed that n=16 and n=32 exceed the 5% gradient and
vorticity thresholds even for exact sampled data. The additive successor
`protocols/high-gradient-of13-v2.json` adds n=128, giving two spatial levels
(n=64,128) below both derivative floors; the reproducible audit is
`evidence/tests/high-gradient-fd2-resolution-floor.json`. A mock-mesh C++ compiler check is
available at `tools/check_high_gradient_openfoam_force.py`. It has not run:
the selected OrbStack Docker context did not answer `docker info` within 3 s,
recorded at `evidence/environment/openfoam-docker-preflight-2026-09-28.json`.
No daemon restart was attempted because running OrbStack processes were
present. A local minimal-type C++ mock checker is also prepared, but host
`/usr/bin/c++` is gated by the unaccepted Xcode license; no license state was
changed. Its preflight is in
`evidence/environment/high-gradient-compile-preflight-2026-09-28.json`.
Consequently no solver result or C++ compile result is claimed, and there is no
evidence that a solver misses the peak. The spatial/time matrix, AMR run,
threshold results and cross-solver comparisons remain open.

The high-gradient AMR path now uses the analytic `chi(y,z)` envelope as its
refinement sensor. `tools/openfoam_amr_case.py`, `tools/analyze_amr.py` and
`tools/run_high_gradient_amr.py` support the frozen 4096/5000/100000 cell
budgets and compare nonuniform fields to the exact time-dependent reference.
The six-case v2 uniform matrix also has a provenance-recording runner in
`tools/run_high_gradient_openfoam.py`; both runners check the immutable image
and require a clean committed source tree before creating a work tree. Case
generation, sensor wiring and the current test suite pass, but neither high-gradient
matrix has been run. The blocked-candidate count is explicitly `UNOBSERVED`
unless runtime evidence exposes it. Spectrum remains unavailable on the
nonuniform mesh without a validated reconstruction.
An offline analyzer control now verifies that the sampled central-FD2 component
peak differs from its exact cell-sample derivative peak by the predicted
`sin(N*dx)/(N*dx)` factor; the continuous full-gradient peak remains uncertified
and the result stays `UNCERTAIN`.

The uniform runner was invoked once after preparation; its bounded eight-second
Docker image-inspect preflight timed out and created no case tree. The exact
result is in `evidence/environment/openfoam-high-gradient-run-preflight-2026-09-28.json`.

The post-announcement mathematical and physical literature scan, including the
OpenAI source refresh and explicit molecular-bridge audit, is summarized in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`. That note also
corrects the live SU2 Q&A status: a maintainer replied on September 13 and the
author added the BDF2 control on September 26; GitHub has not marked an accepted
answer.

### High-gradient acceptance gate integration, 2026-09-28

The uniform analyzer now computes relative velocity, energy, FD2 gradient,
vorticity and sampled shell-spectrum errors, and the runner writes separate
standard-acceptance and local-quality verdicts. Standard acceptance requires
the requested endpoint, expected number of time steps, one PIMPLE convergence
record per step within the configured outer-corrector limit, and an `fvSolution`
whose outer-corrector count and absolute `p`/`U` residual controls match the
frozen protocol. This parser was tested against the preserved Foundation 13 n64
run archive as well as synthetic pass/fail/truncated/misconfigured logs. The matrix-level blind-spot verdict requires both
n=64 and n=128 to pass standard acceptance and fail local quality; these are
the two levels whose exact-reference FD2 floors clear the preregistered gradient
and vorticity thresholds. Missing evidence stays UNCERTAIN. All 68 tests and
the 25-step archived report replay passed. This is gate implementation evidence
only; the high-gradient OpenFOAM matrix and AMR sweep had not run at this
historical update.

### High-gradient OpenFOAM execution update, 2026-09-28

The original six-case uniform runner completed and archived the n=128,
dt=0.001 case at t=.05 with exit code 0, 50/50 PIMPLE-converged steps and an
`End` marker. Its standard acceptance and local-quality gates both PASS. The
coarse n=16 and n=32 cases remain standard PASS/local FAIL but are below the
preregistered exact-reference FD2 resolution floors; n=64 and n=128 at dt=.001
are standard PASS/local PASS. These observations do not reproduce a persistent
acceptance blind spot.

The runner then started n=64, dt=.0005 and stopped logging at t=.018. The
preserved log has 36 time records, 35 completed convergence records, and no
terminal marker or exit record. At the last live audit there was no observable
`foamRun` process, while the Docker client and Docker/OrbStack inventory/stop
requests remained unresponsive. The container's terminal state is unknown; its
partial inputs and logs remain preserved. The final dt=.00025 case and all
three high-gradient AMR budgets remain unrun. Accordingly, v2 remains
INCOMPLETE/UNCERTAIN, with no solver-defect or physical-singularity inference.
The completed n=128 archive is published as two checksummed Zstandard parts
under GitHub's per-file limit, with reconstruction instructions in
`evidence/of13-high-gradient-v2/README-n128-archive.md`.

### Current locked replay refresh, 2026-09-28

The locked same-host environment replayed all 25 configured report steps with
zero failures. Its unittest discovery ran 73 tests, and the artifact audit
matched all 93 links. The separate current verification environment passed 75
pytest tests and five subtests. The refreshed high-gradient MMS replay log
now includes selected-point Frobenius-gradient lower bounds; its independent
reference-comparison replay log records NumPy 2.5.2 from the locked environment. This replay
updates archived analytic/report artifacts only; it does not rerun any solver,
continue the stalled Docker case, or upgrade a scientific verdict.

A fresh tracked-only replay of commit `0a950128f0d49701d6323b8ccd58f71b7e20e715`
on 2026-09-28 also completed all 25 report steps, SU2 standard review, and four
symbolic axis checks with exit code zero. The strict 111-file byte comparison
returned nonzero for one field only: the tracked high-gradient reference JSON
records NumPy 2.5.3, while the locked environment regenerates it with NumPy
2.5.2. Removing that version string makes the JSON objects identical. This is
a preserved metadata-only reproducibility mismatch, not a numerical discrepancy
or a clean-export PASS; details and sanitized command outcomes are in
`evidence/clean-export-2026-09-28-current/`.

The locked metadata baseline was then regenerated under NumPy 2.5.2 and the
new support-hole geometry check was added to report replay. A fresh export of
commit `03ce175fcf26d17869de330720f2dfe8a49c4481` now passes: 26 replay steps,
85 unit tests, 113 compared report/test files, and zero changed files. This is
Python postprocessing/replay evidence only, not a solver, training or Lean
reproduction. Sanitized logs and hashes are preserved at
`evidence/clean-export-2026-09-28-cusp-tube/`.

### Analytic axis-margin continuation, 2026-09-30

`verification/SupportHoleAssembly.lean` now has three additional chart results:
`coordinateEta_lipschitz_z`, `coordinateEta_axis_center`, and
`coordinateEta_margin_of_axial_radius`. They compiled in the pinned upstream
Lean environment. The last theorem is conditional on an explicit scaled axial
radius bound and controls eta by `|eta0|+delta`; it does not prove that the
bound holds on the requested full space-time tube. The tube-to-sublevel,
transverse geometry, time-varying center and all-plateau obligations remain.
No new solver experiment or upstream finding is claimed. The pinned upstream
full `lake build` completed successfully with 11,424 jobs. Its replay log,
extension compile output, and `#print axioms` output for the three new lemmas
are preserved under `evidence/openai-lean-2026-09-30/`. The added lemmas depend
only on `[propext, Classical.choice, Quot.sound]`. The full build separately
warns that two Euler and two Navier--Stokes ComparatorChallenges declarations
use `sorry`; the exposed Navier--Stokes theorem declarations report only those
three standard Lean axioms. This does not imply independent review of the
source argument. The symbolic tube-geometry checker also passes under the
locked verification requirements with SymPy 1.14.0; its output explicitly
limits itself to exact identities and does not prove the full tube inclusion.
The formalization is in stacked PR
https://github.com/Unjuno/concentration-aware-ns/pull/2, based on the current
OpenFOAM runner PR branch because the support-hole extension is introduced
there. Its Python verification CI passed (run 36688606215). This is a
contribution to the benchmark repository; no defect issue was submitted to
OpenAI or a solver project because this work establishes a conditional
mathematical lemma rather than a reproducible upstream implementation defect.

### Conditional existential cusp-ball transfer, 2026-09-30

The later extension check supersedes the earlier statement above that the
whole-ball inclusion remained unformalized. The fresh pinned run
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/manifest.json` compiles and
audits eight declarations, including `selected_axis_center_small_eventually`,
`selected_velocity_germ_on_cusp_tube`, and `exists_admissible_cusp_radius`, with only
`[propext, Classical.choice, Quot.sound]`. Under fixed strict eta-margin and
active-annulus interior assumptions, it proves existence of `tau0>0` and
local-germ equality throughout every Euclidean ball of radius `c*sqrt(tau)`
for all `0<tau<tau0`; an admissible positive radius and margin exist for every
fixed `eta∈(-1,1)`. The interval is existential and parameter-dependent;
this is not a finite-size packet result, a molecular inference, or a solver
validation. The refreshed audit and derivation are in
`reports/openai-support-hole-assembly-audit.md` and
`docs/support-hole-tube-geometry.md`.

### Full spatial-ball eta margin, 2026-09-30

`coordinateEta_margin_of_euclidean_ball` in
`verification/SupportHoleAssembly.lean` now derives the one-dimensional axial
distance premise from a Euclidean norm bound centered on the actual axis-center
formula. It proves the similarity-coordinate margin for every point in a fixed
time slice of the full spatial ball. Its companion
`transverse_radius_le_of_euclidean_ball` bounds the physical transverse radius
by `sqrt(2)*c*sqrt(tau)`. The pinned Lean compile and axiom audit passed; see
`evidence/openai-lean-2026-09-30-spatial-ball-transverse/manifest.json`. These
discharge the ball-to-eta and transverse-radius steps. Exterior-domain, cutoff
and localization conditions and the full moving-tube transfer remain open.
No particle-position or molecular conclusion follows.

At the September 28 source-run snapshot, four of six cases were complete and
`n64-dt0.0005` was partial. That attempt is retained in place. The newer
September 30 cross-run status index below supersedes its completion count;
previous host PID observations are stale and are not treated as current
container state.

## 2026-09-30 initial temporal addendum snapshot — superseded

The original September 28 v2 manifest remains unchanged as a source-run
snapshot. The separate `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`
joined the four original complete cases with the independently archived
`n=64, dt=0.0005` case. At that snapshot, the quarter-step row and AMR cases
were still unrun. A later same-day addendum completed the `dt=0.00025` row and
the separate three-budget AMR/remap controls. The authoritative current index
is `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`; the
current cross-solver scope and remaining limitations are in
`reports/solver-matrix-coverage-2026-09-30.md`. The original partial attempt
and this earlier status record are preserved as historical evidence.

## 2026-10-01 current analytic and upstream-scope addendum

The pinned Lean extension now proves a selected-field equality ball of radius
`c*sqrt(1-t)` and transfers the actual-base full-spacetime Hessian rate
`C2*q^(-40)` throughout that ball on an existential terminal interval. The
October 1's `verification/SpatialHessianTransfer.lean` now composes that
full-spacetime estimate with a fixed-time spatial restriction and provides
`C2*q^(-40)` for the spatial Hessian on the same ball. The helper and composed
theorem passed Lean elaboration and axiom audit; details are in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`. The
classical nonlinear packet estimate remains separate, so `Cstretch+39` and
its conservative `Q^43` specialization are analysis-level conditional
shrinking-packet allowances with non-effective constants, not a fixed-size
packet theorem. The earlier full-spacetime theorem's ten-declaration axiom
audit remains in
`evidence/openai-lean-2026-09-30-cusp-hessian-v6/`.

The October 1 GitHub issue/PR inventory is recorded in
`reports/upstream-status-2026-10-01.md`. PhysicsNeMo issue #2001 already covers
periodic-only grid-gradient behavior on non-periodic domains; this benchmark
uses a periodic domain and autograd. Issue #2007's odd-width spectral behavior
does not touch its even-width outputs. A successful MLP import smoke on the
pinned environment does not replace the separate #1990 reproducer. No new
upstream report is warranted by the present evidence.

## 2026-10-01 follow-up literature: analytic forcing

Constantin, Ignatova and Vicol's [arXiv:2609.20803](https://arxiv.org/abs/2609.20803)
proves regularity near the proposed singular point under its stated anisotropic
Type-II bounds, exact axisymmetry in a collapsing core, and spatially analytic
forcing assumptions. Version 2's Appendix A crosswalks the Type-II, core,
force-regularity and pure-swirl/axis-value properties to the OpenAI manuscript
and explicitly disclaims verification of the construction's correctness. Our
separate note checks the implication chain and identity-theorem deduction
against both primary texts. Conditional on the cited properties and claimed
singularity, analytic forcing is excluded and the force is not identically
zero on neighborhood cylinders; the independent pure-swirl route excludes
common spatial analyticity on specified slabs without the blow-up hypothesis.
Neither route bounds force amplitude or establishes physical actuation,
particle alignment, viscosity change, or a solver defect. See
`reports/openai-analytic-forcing-bridge-2026-10-01.md` and
`evidence/openai-analytic-forcing-v2-audit.json`. OpenAI Lemma 10.2's zero
endpoint jets plus its smooth extension make the force flat at the point;
combined with conditional nonvanishing on every surrounding cylinder, this is
a flat-at-the-point but locally active force. It still supplies no positive
amplitude lower bound.

## 2026-10-01 independent archive replay

The targeted replay suite was rerun from `work/reference-check-env`. OpenFOAM's
four original time-series archives match the frozen schedules; SU2's five
diagnostic records replay exactly, with temporal order `0.99916` still
uncertified due to per-step residual misses; all five AMR/remap archives pass
hash/tree verification; and PhysicsNeMo's five saved checkpoint/evaluation
pairs match their run archives. PhysicsNeMo derivative comparisons remain
sample-only, not continuous-extremum bounds. No solver was rerun. The full
results and scope limits are recorded in
`reports/solver-matrix-coverage-2026-09-30.md`.

## PhysicsNeMo continuous-peak certificate feasibility

The new exact-rational global Hessian cover audit processes all 25 frozen
checkpoints and saves per-case weight/archive hashes and bounds in
`evidence/tests/physicsnemo-global-hessian-coverage.json`. Under a hypothetical
5% comparator, even a perfect-sample uniform-grid Lipschitz cover would need
at least 9,465–13,743 nodes per axis under this envelope, so it is not a practical
continuous-error certificate. Eight-point autograd checks sanity-check the
network envelope but do not certify it; the analytic inequalities provide the
bound. The illustrative threshold is not PhysicsNeMo-preregistered and no
acceptance status changes. Review found and corrected an input feature-order
error in the first envelope; its old bounds are withdrawn. The checker now
validates the frozen source expression and the regression suite covers the
actual grouped sine/cosine mapping. A corrected optimistic floor uses an upper
bound on the reference peak and lower bound on pi; local interval subdivision
remains untested.

## External verification-method update

An arXiv preprint submitted 2026-09-14 claims all-time smoothness for named
families of periodic initial data using finite Fourier comparison paths and
exact-arithmetic a-posteriori enclosures. It is a bounded-family result, not
global regularity for all data and not a direct counterexample to the distinct
forced blowup claim. The preprint says a reproducibility archive will be
created before journal submission; no such package is linked from its current
arXiv record, so we have not independently checked its proof or code. The
proof architecture may inform local/adaptive whole-domain coverage for our
continuous-peak question, but the theorem itself does not transfer to our
manufactured case. See
`reports/recent-navier-stokes-verification-developments-2026-10-01.md`.
The OpenAI source repository also has both Issues and Discussions disabled,
so the planned upstream issue round has no GitHub issue/discussion route there.
