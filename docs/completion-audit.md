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
| SU2 3-space/multiple-time comparison | Live study-v1 process and per-step history | Incomplete; n16 completed and archived, n32 container confirmed running; remaining cases pending |
| PhysicsNeMo 3-space/multiple-time sampling | Five archives and reports/physicsnemo-study-v1.md | Matrix complete; optimizer/seed and continuum-peak uncertainty remain |
| Local derivatives and spectra | Native/autograd/FD2 comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker and 28 passing unit tests | OpenFOAM n32 and all five PhysicsNeMo reports generated; 48 artifact hashes verified. SU2 reports pending |
| Genuine upstream reporting | SU2 Q&A 2890 with read-back verification | Time-contract question submitted; no blanket defect claim |
| Other target report/no-report decisions | Interim audit and contribution policies | No demonstrated defect yet; final conclusions remain to be reconciled |
| OpenAI construction audit and transfer | Pinned predicates, witness interface, scaling derivation | Pinned NS challenge accepted by nanoda, Lean default kernel and Comparator with exit code 0; see reports/openai-ns-independent-verification.md. Finite-stage extraction and Euler challenge not independently verified |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results | Substantial artifacts published; final report and replay coverage still incomplete |

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.

Latest gate-link audit: `python3 -m tools.audit_gate_artifacts` independently
checks all linked files even when scientific review flags are false. All 48 links
in the six current gate reports match their recorded SHA256 values. This removes
one reproducibility uncertainty only; it does not upgrade any scientific verdict.
PhysicsNeMo's frozen protocol lacks an explicit acceptance-threshold declaration;
the new gate reports preserve that gap instead of claiming retrospective
preregistration.
