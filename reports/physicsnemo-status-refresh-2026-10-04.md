# PhysicsNeMo live status refresh — 2026-10-04

**Checked:** 2026-10-04 03:02 UTC through GitHub API/CLI.  
**Main:** `b45a5c810c741e6b41f8515be24c51121f8fc21f` (commit date October 2).  
**Purpose:** reconcile existing numerical findings and avoid duplicate upstream reporting.

The nonperiodic-grid-gradient feature request #1852 has now closed, but the
closure is administrative: the stale bot closed it 14 days after labeling it
stale, with `state_reason=not_planned`. There is no maintainer technical
resolution in the issue comments. The related consumer-facing issue #2001
remains open. Its proposed implementation PR #1853 is still an old draft, open
since July and reported unmergeable. The closure of #1852 therefore does not
mean the boundary behavior was fixed or rejected on technical grounds; the
remaining issue/PR already cover the feature and affected consumer.

The odd-width spectrum defect remains tracked by issue #2007, and its focused
fix remains open in PR #2008. GitHub reports the PR branch two commits ahead
and fourteen behind current main, with base `ff5d19d`; its focused checks pass,
but this is not a full PhysicsNeMo suite run. The benchmark currently uses even
uniform grid widths, so the odd-width bug does not invalidate its existing
spectral measurements. Reproduction, axis-symmetry controls, and that scope
limit remain in the prior issue-thread comment and the earlier evidence record.

No duplicate issue or status-only comment was posted. The #1852 stale closure
is recorded as maintenance state, not as a new defect or as a fix. The #2007
and #2001 discoveries already have tracking issues, and their current PRs
remain the appropriate upstream vehicles. Exact API fields and timestamps are
archived in
`evidence/upstream-refresh/physicsnemo-status-2026-10-04T0302Z.json`.

## Sources

- [Issue #1852](https://github.com/NVIDIA/PhysicsNeMo/issues/1852)
- [Issue #2001](https://github.com/NVIDIA/PhysicsNeMo/issues/2001) and [PR #1853](https://github.com/NVIDIA/PhysicsNeMo/pull/1853)
- [Issue #2007](https://github.com/NVIDIA/PhysicsNeMo/issues/2007) and [PR #2008](https://github.com/NVIDIA/PhysicsNeMo/pull/2008)
