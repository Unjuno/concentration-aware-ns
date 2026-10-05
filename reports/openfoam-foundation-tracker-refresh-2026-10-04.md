# OpenFOAM Foundation issue-tracker overlap check

**Checked:** 2026-10-04 UTC

The benchmark's prior upstream refresh explicitly left the Foundation's separate issue tracker unsearched. I followed the Foundation's README/reporting route to [OpenFOAM Issue Tracking](https://bugs.openfoam.org/) and ran focused public-search queries for dynamic refinement, `maxCells`, `maxRefinement`, mapped fields/refinement history, and gradient evaluation.

Search-indexed results exposed a few historical candidates:

| Ticket | Search-indexed description | Relation to this benchmark |
|---|---|---|
| [#4107](https://bugs.openfoam.org/view.php?id=4107) | Multiple `refinementRegions` use the maximum of their `maxRefinement` settings; the displayed response calls this a design decision. | Different setting and semantics from this benchmark's `maxCells` approximate budget and observed whole-level selection. Not a match. |
| [#3928](https://bugs.openfoam.org/view.php?id=3928) | `dynamicMesh` refiner does not write `refinementHistory` correctly; the indexed list marks it resolved in 2022. | This benchmark compares the immediate first mapping event and does not rely on a restarted history. Not a match. |
| [#141](https://bugs.openfoam.org/view.php?id=141) | An old `leastSquares` gradient report on an unstructured hexahedral mesh; the indexed record marks it fixed. | The benchmark's cited diagnostics use the Gauss gradient and independent MMS comparison. Different operator and old version. Not a match. |
| [#75](https://bugs.openfoam.org/view.php?id=75) | Old `dynamicRefineFvMesh` refinement-candidate scoring inconsistency, indexed as fixed in 1.7.x. | Historical selector behavior, not the pinned Foundation 13 run or its postprocessing metrics. Not a match. |

These results do not demonstrate a Foundation defect. In particular, none supplies evidence that the benchmark's measured AMR discrepancy is a reproducible violation of the Foundation 13 contract. The existing AMR cap behavior is already explained by source inspection as whole-level selection under an approximate cell budget; the exact-cell-average and Gauss-gradient audits are benchmark diagnostics, not expected runtime guarantees. No issue was filed.

The tracker search engine returned useful indexed summaries, but direct unauthenticated `view.php?id=...` retrieval in this environment returned the login page for the queried tickets. Therefore the ticket descriptions and historical dispositions above are based on indexed results, not a fresh full-page review. The tracker site says reports should include version, operating system, reproducible instructions, and evidence ruling out user error; this project currently has no new Foundation implementation defect meeting that bar. The search was targeted, not an exhaustive review of all Foundation tickets.

## Sources and retrieval limits

- [Foundation issue tracker and reporting guidance](https://bugs.openfoam.org/)
- [#4107](https://bugs.openfoam.org/view.php?id=4107), [#3928](https://bugs.openfoam.org/view.php?id=3928), [#141](https://bugs.openfoam.org/view.php?id=141), [#75](https://bugs.openfoam.org/view.php?id=75)
- [`openfoam-foundation-tracker-refresh-2026-10-04.json`](../evidence/upstream-refresh/openfoam-foundation-tracker-refresh-2026-10-04.json)
