# Upstream reporting decisions — updated 2026-09-26

These decisions concern the pinned implementations and reproduced experiments.
They do not claim to identify every industrial consequence of a mathematical
construction. Numerical observations do not establish blow-up or physical danger.

| Target | Evidence and classification | Reporting decision |
|---|---|---|
| OpenFOAM Foundation 13 | The n32 uniform case has approximately 1.87% velocity L2 error but a sampled FD2 gradient peak at least 13.1% below an analytic continuum lower bound. Temporal convergence and derivative/sampling uncertainty prevent a full acceptance claim. AMR versus static-refined-mesh controls show an accuracy difference but do not isolate its implementation cause. | No defect report. Residual stopping does not promise discretization accuracy, and maxCells is approximate by source semantics. Report to the Foundation tracker only if a separate contract violation is isolated. |
| SU2 v8.5.0 | The uniform analytic time control distinguishes source evaluation at the old time from evaluation at the updated solution time. Both tested recurrences remain first-order consistent. This is a time-contract clarification, not proof of an inconsistent solver. | [Q&A 2890](https://github.com/su2code/SU2/discussions/2890) submitted with baseline, intervention and reproduction evidence. Live GraphQL now confirms a September 13 reply agreeing with the time-lag diagnosis and proposing a BDF2 regression. The earlier zero-comment record is historical. The new six-case uniform BDF2 control reproduces first-order lag error and second-order behavior under the diagnostic time shift; all inner residual thresholds pass. Results were [replied to the existing discussion](https://github.com/su2code/SU2/discussions/2890#discussioncomment-18613462). This is not maintainer acceptance of a general fix; see reports/su2-bdf2-source-time.md. The localized grid/time study now has all five runs archived; direct endpoint temporal differences have observed order 0.99916, with unconverged inner steps still recorded. This does not establish a new contract violation. |
| PhysicsNeMo v2.2.1 | Explicit time derivatives obey the documented PhysicsInformer contract; independent exact-field residual checks pass. Five trained networks have finite-sample errors, unresolved continuous peak bounds and fixed-budget/seed limitations. The experiment protocol did not explicitly preregister acceptance thresholds. | No framework defect report. These results support an additional validation example, but do not establish a new framework failure or a failure of the historical Taylor–Green example. Publishing the standalone benchmark is presently the supported improvement. |

OpenFOAM's README directs reports to bugs.openfoam.org; it is not interchangeable
with the OpenCFD project. PhysicsNeMo's pinned contribution policy and the prior
issue search are recorded in docs/audit.md. SU2 duplicate checking and the exact
submitted text are retained with reports/su2-mms-time-discussion.md and its
submission evidence. The September 26 BDF2 follow-up is recorded in evidence/su2-upstream-review/bdf2-reply-submission.json.

Reopening a decision requires new evidence: a reproducible violation of a stated
contract, or a concrete example change with evidence of its benefit and a fresh
duplicate check. A small residual, a single inaccurate network, or a sampled
maximum alone is insufficient. Missing studies remain missing; a decision not to
post does not complete those studies.

## PhysicsNeMo source refresh, 2026-09-28

The released v2.2.2 and current main (`426f7552da4b4fa675e404e8a4f437e27681b668`)
share the same `power_spectrum.py` hash, and the odd-width axis-centering defect
in Issue #2007 reproduces on both. PR #2008 already provides the direct fix and
targeted regression tests; we independently ran its revised function on even,
odd and rectangular shapes and observed the intended axis and transpose
invariance. Our independent reproduction was posted to the existing issue:
[comment](https://github.com/NVIDIA/physicsnemo/issues/2007#issuecomment-5861349072).
The PR is still open and behind current main, and we did not run the full
PhysicsNeMo suite. The benchmark uses even grid counts, so the odd-width defect
does not alter its current spectrum measurements. No duplicate defect report
or unrelated contribution was opened.

For boundary handling, PhysicsInformer issue #2001 and lower-level feature
issue #1852 / draft PR #1853 already cover the periodic-only limitation. The
current manufactured solution is periodic, so we leave that issue family to
its existing maintainers and report no new defect.

Current target/default-branch heads and focused duplicate searches are recorded
in `evidence/upstream-refresh/current-project-inventory-2026-09-28.json`. The
inventory is intentionally scoped and is not an exhaustive review of every open
issue in the three repositories.
