# Completion audit — interim, 2026-09-12

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
| Evidence-linked acceptance gate | v2 checker; 31 tests in the recorded replay; gate-artifact-audit.json | Eleven reports (OpenFOAM n32, PhysicsNeMo five, SU2 five); all 88 artifact links match. Verdicts remain UNCERTAIN with gaps explicit. |
| Genuine upstream reporting | SU2 Q&A 2890 with read-back verification | Time-contract question submitted; no blanket defect claim |
| Other target report/no-report decisions | Interim audit and contribution policies | No demonstrated defect yet; final conclusions remain to be reconciled |
| OpenAI construction audit and transfer | Independent NS kernel logs; docs/openai-core-material-trajectory.md; symbolic force/dissipation checks | Original NS target verified. Additional trajectory, strain and full axial viscous-force ratio remain hand-derived. New pinned Lean proofs cover the selected slow-sum radial derivative limit, its natural-profile identification and eventual negative sign at an existing root. Euler and finite-stage extraction remain unperformed. |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results | Comparative report published; tracked-only export and fresh-venv postprocessing pass. Solver-build reproduction and analytic-hypothesis review remain separate |

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.

Current report replay covers twelve steps, including all five SU2 archive
reviews, diagnostic replays, spectral derivatives, direct temporal differences
and gate generation. The recorded 31 tests and 88 matching artifact links
verify their stated implementation and provenance scopes, not continuum accuracy.
PhysicsNeMo's missing preregistered threshold remains a limitation that cannot
be repaired retrospectively.

Remaining completion work:

1. Comparative audit now exists at reports/comparative-audit.md. Retain its
   bounded conclusions: no certified standard-PASS/local-FAIL case is established.
2. Reconcile standard-acceptance checks: current false review flags cannot be
   interpreted as completed reviews merely because verdict files exist. Preserve
   observed failures separately from unknown continuous-peak accuracy.
3. Independently review the new source-to-trajectory implication chain; symbolic
   identities do not cover theorem hypotheses. New Lean proofs now establish the chart derivative chain through the natural
   profile, including a root with eventual negative derivative. They do not yet
   establish the physical Laplacian/material-acceleration limit. Do not describe original kernel acceptance
   as verification of our new result.
4. Tracked-only export and fresh-venv postprocessing succeeded (see
   evidence/fresh-environment-check.json). SU2 discussion read-back is refreshed
   with no comments; no endorsement is inferred. Full solver builds were not
   repeated by this postprocessing check.
5. Audit the requested impact analysis against what the evidence supports.
   No finite benchmark can establish all industrial or molecular consequences;
   explicitly bound findings by solver versions, cases and construction hypotheses.

This remains an interim audit, not a declaration that all goal requirements
have been completed.
