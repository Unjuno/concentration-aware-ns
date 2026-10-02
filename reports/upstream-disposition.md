# Upstream reporting decisions — refreshed 2026-10-01

These decisions concern the pinned implementations and reproduced experiments.
They do not claim to identify every industrial consequence of a mathematical
construction. Numerical observations do not establish blow-up or physical danger.

| Target | Evidence and classification | Reporting decision |
|---|---|---|
| OpenFOAM Foundation 13 | The n32 uniform case's FD2 deficit exceeds the reference-only stencil floor; all six high-gradient v2 uniform cases are complete, with n64/n128 passing standard and local gates. Same-run AMR audits at n16/32/64/128 show mapped cell values exactly match piecewise-constant parent injection; a nested exact-cell-average identity attributes most child-DOF error to smooth-reference subcell variation, with the variation term halving as n doubles. Same-mesh analytic-initialized controls reduce AMR-path error to 1.88%/0.483%. The cap100000 event is explained by whole-level candidate grouping and subsequent unrefinement in pinned source. | No defect report. The remap value-transfer step is isolated for four captured first-refinement events, but AMR quality remains UNCERTAIN: stored cell DOFs are not assumed to be exact averages, no AMR threshold was preregistered, and other temporal/flux/pressure effects are not certified. The observed maxCells overshoot matches source behavior. See `reports/openfoam-amr-nested-cell-average-error-2026-10-03.md`; do not claim a violated contract. |
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
  has four entries. In particular, issue #5 concerns generated documentation
  for `src/meshTools/meshSearch`, not the `fvMeshTopoChangers/refiner` logic
  measured here; the other open issues also do not match this AMR behavior.
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

### Live status recheck, 2026-09-30 11:48 UTC

The read-only inventory was refreshed after the benchmark matrix replay.
OpenFOAM's four open issues still do not concern the exercised refinement path;
its only open pull request changes `README.org`. SU2 discussion #2890 remains
unanswered in GitHub's metadata despite the maintainer's diagnosis, and issue
#2353 remains open with our scoped restart/MAX_TIME observations already
recorded. PhysicsNeMo issue #2007 and PR #2008 remain open; the PR is mergeable
but behind its recorded base, and its latest review metadata is from the
Copilot reviewer bot. The exact heads, timestamps, and disposition are in
`evidence/upstream-refresh/live-status-2026-09-30T1148Z.json`. No new upstream
report is justified by this status-only refresh.

The live read-only status check was repeated at 2026-09-30 10:31:46 UTC and is
preserved in
`evidence/upstream-refresh/live-status-2026-09-30.json`. The audited OpenFOAM
master and SU2 master still match their source pins; SU2's existing discussion
contains both the maintainer diagnosis and our BDF2 follow-up. PhysicsNeMo
main/issue/PR states and its divergence from PR #2008 are recorded there.

## Three-project release/status refresh, 2026-10-01

A read-only query of the official project APIs confirms that SU2's latest
release remains v8.5.0, the exact benchmark pin; issue #2353 is still open and
the existing discussion #2890 remains the correct location for the reported
time-source observations. OpenFOAM Foundation 13's repository currently lists
four open issues and one README pull request. The reviewed two-phase-version
and generated-documentation issues do not describe our single-phase MMS or
AMR behavior; the other issues concern migration and installation. The GitHub
API reports `NOASSERTION` for repository license metadata, while the pinned
package/source audit records GPL-3.0-or-later file headers. No matching defect
was found.

PhysicsNeMo v2.2.2 is now the latest release, one commit beyond the benchmark's
v2.2.1 pin. The delta is limited to the package version, corrected PyPI install
hint text and associated tests; it does not change the CFD model, residual
formulation, or power-spectrum implementation used in this audit. Current main
still has the same `power_spectrum.py` Git blob as the benchmark pin. Odd-width
issue #2007 remains open and its focused fix PR #2008 remains open, two commits
ahead and ten behind current main. The benchmark uses even-width grids, so this
known defect does not affect its current spectrum measurements. The existing
issue and PR remain the appropriate upstream records; no duplicate issue was
filed.

The exact commit IDs, API status fields, file hashes, queried items, and
reproduction queries are preserved in
[`evidence/upstream-refresh/three-project-inventory-2026-10-01.json`](../evidence/upstream-refresh/three-project-inventory-2026-10-01.json).
This refresh updates versions and tracking state; it is not a new solver run,
full source audit, or PhysicsNeMo acceptance verdict.

## Three-project live refresh, 2026-10-01 08:28 UTC

The focused GitHub inventory was reread after the prior disposition. The audited
source heads are unchanged: OpenFOAM Foundation 13 remains at
`18870c24d21c6b982e2cdec27b2f59738cca5f90`, SU2 master at
`bc15466602a687d6fb796d5df7a12ce3fde0949a`, and PhysicsNeMo main at
`b08dd3f61ac44c784f7c03b0cc93947226365cad`. The repository API reports
`NOASSERTION` for the first two license identifiers, so their pinned `COPYING`
files were read directly: OpenFOAM declares GPL-3.0-or-later and SU2 declares
LGPL-2.1. PhysicsNeMo's pinned `LICENSE.txt` declares Apache-2.0.

The four listed OpenFOAM GitHub issues still do not match the AMR observation;
its README directs bug reports to the separate bugs.openfoam.org tracker, so
this is explicitly not an exhaustive search of that system. SU2 Discussion
#2890's `updatedAt` is September 30, but its thread still contains the known
September 13 maintainer diagnosis and September 26 BDF2 author reply, with no
later comment or accepted fix observed. PhysicsNeMo issue #2007 and PR #2008
remain open, and the PR remains behind its base; no duplicate finding was
posted. Full metadata, pinned license-file blob IDs and scope notes are in
`evidence/upstream-refresh/current-project-inventory-2026-10-01T0828Z.json`.

This refresh changes no scientific verdict and justifies no new upstream post.

## Three-project focused refresh, 2026-10-02 JST

The read-only refresh in
[`evidence/upstream-refresh/three-project-inventory-2026-10-02.json`](../evidence/upstream-refresh/three-project-inventory-2026-10-02.json)
confirms OpenFOAM Foundation 13 and SU2 still point to their audited default-
branch commits. PhysicsNeMo main advanced one commit; its only changed paths
are three example READMEs, and the audited `power_spectrum.py` blob is
unchanged. Existing records remain current: SU2 Discussion #2890 and Issue
#2353, and PhysicsNeMo Issue #2007 and PR #2008. No duplicate post is
justified.

For OpenFOAM, the research browser's direct fetch of `bugs.openfoam.org`
returned HTTP 403. A later direct HTTP check of its all-issues page redirected
to the tracker login form (302 then 200), confirming that an exhaustive current
Mantis listing is not available in this environment. Focused searches found
older or differently-scoped AMR reports (including the resolved 1.7.x mapping
report and a multiple-cellZone `maxRefinement` question), but no matching
report for the present v13 observations. This is useful duplicate screening,
not an exhaustive tracker audit; no new report was filed. No scientific
verdict changed.

## OpenFOAM AMR derivative controls, 2026-10-02

Replayed Foundation 13 `grad(U)`/`vorticity` on the two dynamic-AMR endpoint
archives and their fixed-final-mesh analytic-initialization controls. Each pair
has byte-identical final mesh geometry and cell centers/volumes. Dynamic cases
show larger sampled derivative errors than their static controls, but the
control does not isolate remapping from coarse-history error and subsequent
evolution. The evidence narrows the benchmark-path attribution without
demonstrating an upstream contract violation. AMR quality remains UNCERTAIN;
no new Foundation bug report was filed. See
`reports/openfoam-amr-remap-derivative-controls-2026-10-02.md` and its replay
evidence.

## OpenFOAM Foundation current-version and tracker-policy refresh, 2026-10-02

The Foundation's current release is v14; its GitHub source repository advanced
to `162fa7a2e51e9c9a86c3000efdd885907f7d1acc` on September 30. The v14 repo
has one unrelated open issue and two open pull requests; its `COPYING` file
declares GPL-3.0-or-later even though GitHub's license API says
`NOASSERTION`. The official contribution guide directs effective development
to `OpenFOAM-dev`, asks for reproducible test cases and tests, and requires a
Contributor Agreement for significant fixes or new developments.

The benchmark has one v14 `n=64`, `dt=0.001` compatibility probe. Its
version-banner-normalized endpoint fields and five sampled diagnostics match
Foundation 13 exactly. There is no v14 space/time matrix or v14 AMR audit, and
continuous extrema remain uncertified. No defect was reproduced and no report
was filed. Current release, source, issue/API and tracker-login observations
are in [`openfoam-foundation-current-2026-10-02.json`](../evidence/upstream-refresh/openfoam-foundation-current-2026-10-02.json);
the full scope decision is in
[`openfoam-foundation-current-upstream-audit-2026-10-02.md`](openfoam-foundation-current-upstream-audit-2026-10-02.md).


## Live upstream refresh, 2026-10-02 23:36 UTC

The targeted live inventory is saved in
`evidence/upstream-refresh/live-status-2026-10-02.json`. OpenFOAM Foundation
13 and SU2 default branches remain at their audited heads. The four visible
OpenFOAM issues do not concern the measured AMR path. SU2's existing
Discussion #2890 and Issue #2353 remain the right records; no duplicate is
warranted.

PhysicsNeMo main advanced to `83d6a337eecfc70e215ed1978af8dba9a38580fb` on
October 1. The current `power_spectrum.py` still has SHA-256
`13e7847c62b9285daafdf88307bd548e0f18e1f5d4fa0bf33f3552303deb8552`; a fresh
CPU replay reproduces the 33-wide axis asymmetry while the 32-wide control
passes. The existing Issue #2007 tracks it. PR #2008's fixed source
(`7407608723062dc11ba5332e9ff3774f42bb02d9`) passes the same focused control,
but remains open, review-required, and based on an older main commit. This is
not a full PhysicsNeMo test-suite result; no duplicate issue or PR was opened.

The two fresh PhysicsNeMo JSON replays bind the source hashes and exact outputs.
OpenAI's public formalization repository still reports only its original two
commits in this check. These are status and focused-reproduction updates, not an
exhaustive upstream review or a new defect claim.
