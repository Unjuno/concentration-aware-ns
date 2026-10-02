# Completion audit — interim, 2026-09-27

The project is **not complete**. This audit preserves the original three-target
scope and the user's analytic-priority requirement. Published artifacts and
measured behavior take precedence over prior progress summaries.

The table is current as of September 28; dated entries below retain historical
run scopes. The [impact-scope report](../reports/impact-scope.md) now maps each
finding to a supported improvement and the evidence required to extend it.

| Requirement | Inspected evidence | Current conclusion |
|---|---|---|
| One project repository | Current git remote, public Unjuno/concentration-aware-ns | Satisfied; upstream sources held as archives, no extra project fork |
| Source/version/license audit | docs/audit.md, runtime recipes, pinned source files | Three targets identified; runtime dependencies have stated reproducibility limits |
| Analytic reference and force | reference.py, symbolic, C++, autograd and energy/Fourier checks | Verified in stated scopes; no physical blow-up inference |
| OpenFOAM 3-space/multiple-time comparison | Five archives in evidence/of13-study-v1 | Runs complete; three tighter-iteration controls add 350 converged steps without changing endpoints materially or the observed order 0.493. Asymptotic temporal convergence remains unproved. |
| AMR constraints and controls | Three AMR plus two fixed-refined-mesh archives | Runs complete; dynamic initialization/remapping attribution unresolved |
| SU2 3-space/multiple-time comparison | All five archives; archive-review.json, diagnostic-replay.json, su2-time-comparison.json | Matrix complete and diagnostics replayed. Direct endpoint differences give observed order 0.99916; inner residual failures prevent an error certificate. |
| PhysicsNeMo 3-space/multiple-time sampling | Five archives and reports/physicsnemo-study-v1.md | Matrix complete; optimizer/seed and continuum-peak uncertainty remain |
| Local derivatives and spectra | Native/autograd/FD2/spectral comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker; 65 tests in the latest locked clean export; evidence/tests/gate-artifact-audit.json | Fourteen reports (including three high-gradient AMR cases); all 117 artifact links match. Verdicts remain UNCERTAIN with gaps explicit. |
| Genuine upstream reporting | SU2 Q&A 2890 and issue #2353 with read-back verification | BDF2 order-reduction control and restart-dependent MAX_TIME stopping consequence reported; no general-fix claim |
| Other target report/no-report decisions | Interim audit and contribution policies | Explicit no-defect-report decisions for OpenFOAM and PhysicsNeMo are recorded in reports/upstream-disposition.md; the SU2 BDF2 finding is scoped separately |
| OpenAI construction audit and transfer | Independent NS kernel logs for both pins; current source-bound extension checks; docs/axis-flow-derivative.md; docs/packet-constant-dependencies.md | Full axis Jacobian, explicit variational solution, inverse identity and eventual axis smoothness are Lean-checked. Variational uniqueness on compact terminal intervals is Lean-checked. The updated source velocity-rate theorem gives a base-field endpoint Hessian exponent `kappa=40`, but the assembled-field base-equality tube has no established lower-radius envelope as `T` approaches 1; the previous `Q^(Cstretch+39)` transfer is withdrawn. Nonlinear-flow identification remains classical; there is no end-to-end Lean flow theorem or fixed-size packet certificate. The strict negative force-ratio limit still requires the unresolved actual-profile pressure premise. The pinned Euler challenge has passed the recorded independent checks; this does not establish molecular or constitutive consequences. Executable finite-stage extraction remains unperformed. |
| OpenFOAM n=64 endpoint pressure reconstruction | v3 frozen protocol, three Docker archives, and independent archive replay | All three dt cases exit 0; U/p/phi are byte-identical to same-dt baselines, and endpoint velocity algebra replays at 2.12e-16–2.15e-16 relative L2. Narrow endpoint gate passes; trajectory cause, molecular alignment, phase change, and material-viscosity claims remain unsupported. |
| High-gradient AMR gate/provenance reconciliation | [AMR result report](../reports/of13-high-gradient-amr-v1.md), [provenance audit](../reports/of13-high-gradient-amr-provenance-audit.md), archived case manifest and gate reports | The discrete cell-center volume-weighted velocity metric has a scoped threshold FAIL in all three cases; other quality metrics remain unbounded and overall AMR quality is UNCERTAIN. Parent threshold/budget protocols predate the campaign, but tracked chronology does not independently prove the exact high-gradient sensor protocol was frozen before execution. No OpenFOAM defect is established. |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results; `evidence/reproducibility/clean-export-fdedfb6.json` | Comparative report published. Locked same-host current clean export at `fdedfb6b` reproduces 119/119 compared files, with 25/25 replay steps and eight commands successful; 14 gate reports link to 117 matching artifacts. The historical supported-range dependency drift failure remains preserved. Solver-build and training reproduction remain separate. |

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

### Latest locked clean-export replay, 2026-10-02

The first fresh export from commit `f2b009078f07660c39e7b24ffa94eb2d700f9f03`
ran all eight clean-export commands successfully and replayed all 25 report
steps, but detected that the tracked artifact-link audit was stale: it recorded
93 links while the current reports contain 117. Regenerated
`evidence/tests/gate-artifact-audit.json` from all 14 gate reports; all 117
references match their target bytes. A second clean export from
`fdedfb6b701cd6c0a2043fb645a40179ee7391ab` then passed with 119 compared files,
zero changes, all eight commands successful, 25 replay steps and 65 tests.
The sanitized run manifest is
[`clean-export-fdedfb6.json`](../evidence/reproducibility/clean-export-fdedfb6.json).
Scope is locked Python postprocessing on the recorded macOS host; no solver
build, training, or Lean execution is included.

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

The current common replay has 25 passing steps and 57 tests. It includes a fresh
six-archive OpenFOAM comparison reconstruction, the SU2 output-clock replay,
exact uniform-prefix threshold algebra, and the localized high-gradient MMS
plus its independent symbolic-versus-NumPy derivative comparison. It excludes
solver runs for that new MMS case.
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
The locked report replay now has 25 successful steps and 57 tests. A second
implementation evaluates fields from hand-coded Fourier derivative formulas;
direct SymPy differentiation agrees for velocity, gradient, vorticity and
forcing at 65 seeded points for each `N`, with maximum component error below
`2.3e-16`. OpenFOAM's case generator now emits the matching time-dependent
`codedFvModel`, and a unit test reads back the generated cell initialization.
The new Foundation 13 matrix and quality thresholds are frozen in
`protocols/high-gradient-of13-v1.json`; a mock-mesh C++ compiler check is
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
