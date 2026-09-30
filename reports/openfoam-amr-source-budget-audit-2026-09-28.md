# OpenFOAM Foundation 13 AMR cell-budget source audit

This source audit pins the AMR budget interpretation to Foundation 13 commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90`, specifically
[`refiner_fvMeshTopoChanger.C`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C).
It does not establish a defect or a measured outcome for the unrun high-gradient
AMR cases.

## Source behavior

The source computes the nominal number of candidate cells from
`(maxCells - currentGlobalCells) / 7`, because refining one hex cell adds seven
cells. If the candidate set exceeds this nominal allowance, the implementation
truncates it by refinement level, starting at level zero; the source comment
explicitly notes that it does not sort by error. It then calls consistent
refinement, which may add cells to satisfy the 2:1 constraint. The mesh-change
log reports the final number selected and the resulting old/new cell totals.
The refinement-selection path is guarded by `currentGlobalCells < maxCells`.

These are distinct stages: nominal candidate allowance, 2:1-consistent set, and
actual mesh cell count. Therefore `maxCells` is not a strict hard cap in this
implementation, and budget pressure does not mean candidates are ranked by
largest sensor value. Both statements describe the pinned implementation; they
do not say whether that policy is appropriate for a particular application.

## Reproducible budget arithmetic

For the archived v1 cap-5000 case, the initial mesh has 4096 cells. The nominal
allowance is `floor((5000 - 4096) / 7) = 129` candidate cells. Refining exactly
129 cells would give 4999 cells before any consistency expansion. This
arithmetic does not predict the actual v1 final count because the archived
summary does not preserve the full solver log, candidate set, or consistency
expansion history. It also does not infer a count of candidates blocked by the
budget.

## Evidence boundary

| Statement | Evidence | Status |
|---|---|---|
| One refined hex cell adds seven cells; candidate allowance uses division by seven | Pinned source | Direct source observation |
| Over-budget candidate list is truncated by refinement level before 2:1 consistency | Pinned source | Direct source observation |
| Consistency expansion can make final cell count exceed the nominal cap | Order of operations in pinned source | Source-based inference; no particular overshoot asserted |
| Cap-5000 nominal allowance from 4096 cells is 129 candidates | Arithmetic above | Reproducible calculation |
| Exact budget-blocked candidate count for v1 or high-gradient v2 | No preserved candidate list/log or completed v2 AMR run | UNOBSERVED |
| High-gradient AMR accuracy or solver defect | Three frozen v2 budget runs have not executed | UNTESTED; no defect claim |

`tools/analyze_amr.py` intentionally emits `blocked_candidate_count: UNOBSERVED`;
final cell totals alone cannot recover how many sensor candidates were dropped.
The older `evidence/of13-amr-v1/` cases use the Gaussian profile, and their
saved archives do not include `log.foamRun`, so they cannot fill this gap.

This source behavior is already summarized in `docs/audit.md` as an approximate
`maxCells` limit. No upstream issue is warranted from this source audit alone.

## High-gradient v2 event replay, 2026-09-30

The completed cap=100000 run now preserves per-event logs in
`evidence/of13-high-gradient-amr-event-audit-2026-09-30.json`. At its second
refinement check, current cells were 16,640, so the source allowance was
`floor((100000 - 16640)/7) = 11,908` candidate cells. The log says 12,416
cells were selected and the mesh grew to 103,552. In the pinned source, the
budget-limited branch appends candidates one complete refinement level at a
time and tests the allowance after appending that level
([selection loop, pinned source lines 900–940](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C#L900-L940)).
The selected excess is 508 cells, consistent with the whole-level grouping.
The subsequent `consistentRefinement` output count is the same 12,416 shown by
the log, so this event provides no evidence of a 2:1 cascade adding more
candidates.

The later `Selected 256 split points` message refers to points selected for
**unrefinement**, not additional refinement. Source selects split points whose
adjacent cells are no longer marked, then calls consistent unrefinement
([lines 944–994](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C#L944-L994)).
The next log line confirms the reduction from 103,552 to 101,760 cells. The
final count remains 1,760 above the configured value, while the transient
overshoot is explained by the level-group selection granularity in this
observed case. This is consistent with the pinned approximate-cap behavior;
it does not support an upstream defect claim. Exact sensor-eligible candidates
not selected by the level-group branch remain unobserved because the code does
not log their identities/count separately.
