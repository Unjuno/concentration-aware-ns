# Executable recheck of published matrix evidence — 2026-10-04

The single command `python -m tools.verify_published_cell_point_matrix --output NEW_DIRECTORY --source-commit VERIFIER_COMMIT` now rechecks all three larger-case native records and recomputes all three uniform idealized-ball error enclosures. It uses the published small CSVs/protocols/witnesses; it does not download or rerun CFD. Preserve a fresh output directory and use the locked verification dependencies.

Native source identities are compared with the earlier independently pinned n16 map, including installed-file cardinality; target release and runtime receipt identities must agree. The native analyzer verifies output hashes, complete candidate sets, nineteen scheduled points, exact rational certified-ball membership, target vertices, weighted and explicit interpolation values, and secants. New controls reject self-asserted source substitution and duplicate installed sources. This is a verification of published finite samples and receipts, not a new native binary execution or an independent reconstruction of all captured mesh candidates.

The analytic tool reuses the hash-bound prior neighborhood certificate and recomputes the reference-derivative box enclosure and uniform error lower bounds. All three analytic JSONs are required to match the published records byte for byte; cross-host floating secant diagnostics are allowed to differ within their unchanged validity checks and both sets of measurements are retained. A different analytic JSON causes failure and preserves partial evidence; a status label alone cannot pass.

Verifier source `f014b60a` passes the local full command for all three cases. The local verification receipt is in `evidence/published-cell-point-matrix-recheck-v1`. Hosted Python CI now runs this command after its full test suite and uploads outputs/logs even on failure, allowing a fresh Linux-host check of the same published evidence. Hosted recheck completion remains unproved until its exact run/commit and artifact are inspected. Global mesh partition, universal floating search, whole-domain error extrema and physical/proof obligations remain open.

Full local suite: **362 passed, 1 skipped, 89 subtests**.

A Git-directory-free selected export of frozen verifier source `f014b60a` also passes the complete recheck. Its full verification JSON matches the earlier local receipt byte for byte under Python process/network/Git-open guards. Exported source-file hashes, guard source and isolation receipt are preserved. This strengthens source/data reproducibility on the same host; fresh-host CI run 37154392234 is still executing and has not yet established its result.

The fresh-host v1 recheck subsequently failed on analytic n32 endpoint equality despite all 362 tests passing. Failure is preserved; see `published-cell-point-dyadic-bounds-2026-10-04.md` for the additive conservative v2 method. No v1 cross-host exact reproducibility is claimed.
