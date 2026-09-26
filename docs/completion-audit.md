# Completion audit — interim, 2026-09-26

The project is **not complete**. This audit preserves the original three-target
scope and the user's analytic-priority requirement. Published artifacts and
measured behavior take precedence over prior progress summaries.

| Requirement | Inspected evidence | Current conclusion |
|---|---|---|
| One project repository | Current git remote, public Unjuno/concentration-aware-ns | Satisfied; upstream sources held as archives, no extra project fork |
| Source/version/license audit | docs/audit.md, runtime recipes, pinned source files | Three targets identified; runtime dependencies have stated reproducibility limits |
| Analytic reference and force | reference.py, symbolic, C++, autograd and energy/Fourier checks | Verified in stated scopes; no physical blow-up inference |
| OpenFOAM 3-space/multiple-time comparison | Five archives in evidence/of13-study-v1 | Runs complete; asymptotic temporal convergence not established |
| AMR constraints and controls | Three AMR plus two fixed-refined-mesh archives | Runs complete; dynamic initialization/remapping attribution unresolved |
| SU2 3-space/multiple-time comparison | All five archives; archive-review.json, diagnostic-replay.json, su2-time-comparison.json | Matrix complete and diagnostics replayed. Direct endpoint differences give observed order 0.99916; inner residual failures prevent an error certificate. |
| PhysicsNeMo 3-space/multiple-time sampling | Five archives and reports/physicsnemo-study-v1.md | Matrix complete; optimizer/seed and continuum-peak uncertainty remain |
| Local derivatives and spectra | Native/autograd/FD2/spectral comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker; 36 tests in the current replay; evidence/tests/gate-artifact-audit.json | Eleven reports (OpenFOAM n32, PhysicsNeMo five, SU2 five); all 93 artifact links match. Verdicts remain UNCERTAIN with gaps explicit. |
| Genuine upstream reporting | SU2 Q&A 2890 with read-back verification | Time-contract question submitted; no blanket defect claim |
| Other target report/no-report decisions | Interim audit and contribution policies | No demonstrated defect yet; final conclusions remain to be reconciled |
| OpenAI construction audit and transfer | Independent NS kernel logs; docs/openai-core-material-trajectory.md; symbolic force/dissipation checks | Original NS target verified. The selected base-field material trajectory and its transfer to the actual activated periodic field are now Lean-verified; strain remains hand-derived; the full physical axial viscous-force ratio is Lean-checked under explicit pressure assumptions. Root existence and the local pressure-threshold equivalence are checked, but the actual profile threshold remains unproved. New pinned Lean proofs cover the selected slow-sum radial derivative limit, its natural-profile identification and eventual negative sign at an existing root. Euler and finite-stage extraction remain unperformed. |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results | Comparative report published; tracked-only export and fresh-venv postprocessing pass. Solver-build reproduction and analytic-hypothesis review remain separate |

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.

Current report replay covers twelve steps, including all five SU2 archive
reviews, diagnostic replays, spectral derivatives, direct temporal differences
and gate generation. The current 36 tests and 93 matching artifact links
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
   explicitly bound findings by solver versions, cases and construction hypotheses.

This remains an interim audit, not a declaration that all goal requirements
have been completed.

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
