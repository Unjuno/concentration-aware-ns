# Completion audit — interim, 2026-09-09

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
| SU2 3-space/multiple-time comparison | Live study-v1 process and per-step history | Incomplete; n16 still running at this audit |
| PhysicsNeMo 3-space/multiple-time sampling | Five archives and reports/physicsnemo-study-v1.md | Matrix complete; optimizer/seed and continuum-peak uncertainty remain |
| Local derivatives and spectra | Native/autograd/FD2 comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker and 25 passing unit tests | Implemented triage; real final per-target gate reports still required |
| Genuine upstream reporting | SU2 Q&A 2890 with read-back verification | Time-contract question submitted; no blanket defect claim |
| Other target report/no-report decisions | Interim audit and contribution policies | No demonstrated defect yet; final conclusions remain to be reconciled |
| OpenAI construction audit and transfer | Pinned predicates, witness interface, scaling derivation | Source/elementary analytic audit only; proof closure and finite-stage extraction not verified |
| Reproducible public deliverables | Runtime instructions, scripts, 25 readable archives | Substantial artifacts published; final report and replay coverage still incomplete |

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.
