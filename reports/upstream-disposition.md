# Upstream reporting decisions — updated 2026-09-26

These decisions concern the pinned implementations and reproduced experiments.
They do not claim to identify every industrial consequence of a mathematical
construction. Numerical observations do not establish blow-up or physical danger.

| Target | Evidence and classification | Reporting decision |
|---|---|---|
| OpenFOAM Foundation 13 | The n32 uniform case's FD2 deficit exceeds the reference-only stencil floor; all six high-gradient v2 uniform cases are complete, with n64/n128 passing standard and local gates. Three AMR runs have high errors, while same-mesh analytic-initialized controls reduce error to 1.88%/0.483%. The cap100000 event is explained by whole-level candidate grouping and subsequent unrefinement in pinned source. | No defect report. AMR quality remains UNCERTAIN and the exact field-transfer/remapping component is not isolated. The observed maxCells overshoot matches source behavior. Keep investigating without claiming a violated contract. |
| SU2 v8.5.0 | The uniform analytic time control distinguishes source evaluation at the old time from evaluation at the updated solution time. Both tested recurrences remain first-order consistent. This is a time-contract clarification, not proof of an inconsistent solver. | [Q&A 2890](https://github.com/su2code/SU2/discussions/2890) submitted with baseline, intervention and reproduction evidence. Live GraphQL now confirms a September 13 reply agreeing with the time-lag diagnosis and proposing a BDF2 regression. The earlier zero-comment record is historical. The new six-case uniform BDF2 control reproduces first-order lag error and second-order behavior under the diagnostic time shift; all inner residual thresholds pass. Results were [replied to the existing discussion](https://github.com/su2code/SU2/discussions/2890#discussioncomment-18613462). This is not maintainer acceptance of a general fix; see reports/su2-bdf2-source-time.md. The localized grid/time study now has all five runs archived; direct endpoint temporal differences have observed order 0.99916, with unconverged inner steps still recorded. This does not establish a new contract violation. |
| NVIDIA PhysicsNeMo | Explicit time derivatives obey the documented PhysicsInformer contract; independent exact-field residual checks pass. The odd-width spectrum defect reproduces on current main and is already tracked by issue #2007. Existing PR #2008 fixes the focused reproducer, but remains OPEN, BEHIND main and review-required; only focused controls, not the full framework suite, were run. | No duplicate issue. Focused evidence was added to the existing PR conversation. Do not treat focused CI or a deterministic reproducer as full framework validation or maintainer acceptance. |

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

The issue #2007 reproduction is now directly rerunnable with
`work/physicsnemo-env/bin/python -m tools.reproduce_physicsnemo_issue_2007`;
its source hash, odd/even controls, and transpose results are in
`evidence/upstream-refresh/physicsnemo-issue-2007-reproduction.json`. As of the
latest live metadata check, issue #2007 remains open and PR #2008 remains open,
unmerged, and behind `main`. Since the existing PR contains the targeted fix,
we do not file a duplicate issue or PR. The full upstream test suite remains
unrun, so this disposition is limited to the focused reproducer and current
targeted review.

The same reproducer was run against the exact PR #2008 head
`7407608723062dc11ba5332e9ff3774f42bb02d9`. Its source hash is
`f66a9028c0a18804471c260a32aed1e3b0e9b59655df0c821d4bb904cdd8c983`; the odd
and even axis-mode controls and odd/even transpose controls all pass. The
separate result is `evidence/upstream-refresh/physicsnemo-pr2008-fix-validation.json`.
This verifies the focused counterexample is repaired by the existing diff, not
that the whole framework or PR has passed its full test suite.

## PhysicsNeMo current-main refresh, 2026-09-30

The exact current-main source still reproduces the already-tracked odd-width
Issue #2007. The existing PR #2008 head passes the same fixed controls but is
still open and behind main. We added a fresh data point to that PR discussion;
no duplicate report is appropriate. Details, commands, source hashes and raw
outputs are in `reports/physicsnemo-refresh-2026-09-30.md` and
`evidence/upstream-refresh/current-project-inventory-2026-09-30.json`.

## Three-project status refresh, 2026-09-30

The live state was reread after completing the high-gradient AMR controls:

- **OpenFOAM Foundation 13:** the current Foundation 13 open-issue inventory
  has four entries; none establishes a duplicate for the measured AMR behavior.
  The refinement-level selection and unrefinement event match the approximate
  `maxCells` source semantics (see the source-pinned event replay in
  `openfoam-amr-source-budget-audit-2026-09-28.md`). The large AMR-path velocity
  errors remain a benchmark finding with UNCERTAIN quality attribution, not a
  demonstrated upstream contract violation. No new issue was filed.
- **SU2:** `master` still resolves to
  `bc15466602a687d6fb796d5df7a12ce3fde0949a`. Q&A #2890 remains the existing
  report and contains the September 13 maintainer agreement with the source-time
  diagnosis; existing issue #2353 contains later BDF2 and MAX_TIME/restart-clock
  follow-ups. No duplicate issue was filed. These are scoped time-contract and
  output-clock findings, not proof of a general solver defect.
- **PhysicsNeMo:** issue #2007 remains OPEN. PR #2008 remains OPEN with head
  `7407608723062dc11ba5332e9ff3774f42bb02d9`, targets an older main base, and
  is marked BEHIND and review-required. The September 30 current-main CPU
  reproducer and PR-head comparison are in
  `physicsnemo-refresh-2026-09-30.md`; focused PR checks passed, while a full
  framework suite and a rerun against a later main commit are not claimed. The
  existing PR is the appropriate reporting destination; no duplicate issue was
  filed.

These checks update status and reporting decisions only. A fully reproducible
release bundle and the remaining analytic and solver-specific uncertainty work
are still open.
