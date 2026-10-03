# Larger native position queries and uniform local error — 2026-10-04

[Hosted run 37153721711](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37153721711) completes all three larger-target replays on exact source `560a786f35749dcc0c1d24ebcc6839a1edcd0f77`. Each executes nineteen position queries from saved fields without CFD evolution. Independently checked probe binary hashes, nine installed source identities (against the earlier independently pinned n16 map), stock-library receipts and unchanged field identities pass. Every query is inside the Arb-enclosed radius-1/4096 ball by exact decoded-float rational arithmetic. A strengthened auditor at `456b09a` requires the complete set of twelve native candidates to equal the enclosed set for each query, rejecting missing/extra candidates and query IDs.

All 57 queries select the intended vertices and first candidate. Native position and explicit-overload values agree exactly in the recorded outputs; independent weighted-value discrepancies are at most 1.38778e-17. Floating secant discrepancies are below 1.57e-12 against the affine map, comfortably within the unchanged 1e-8 diagnostic tolerance. Hosted and local diagnostics are not claimed byte-identical: n32/n64 have small floating differences, and both original hosted analyses and local analyses are preserved with difference receipts. Native finite samples are verified; agreement for every floating search input remains unproved.

A separate analytic enclosure at source `d4f10ea` now extends the earlier pointwise error to **every point in the proved idealized ball**. The affine gradient is constant there; Arb128 encloses the analytic reference gradient on a containing coordinate box. Summing squared componentwise absolute infima gives conservative Frobenius gradient/direct-curl norm lower bounds without multiplying sign-crossing intervals as if they were squares. The containing box need not remain in the target tetrahedron: it only encloses reference derivatives, whereas the error conclusion is restricted to the certified ball.

| Case | Uniform gradient-error lower bound | Uniform curl-error lower bound |
|---|---:|---:|
| n32, dt .001 | 86.3198% | 9.9237% |
| n64, dt .001 | 48.8078% | 6.5413% |
| n32, dt .0005 | 85.2408% | 9.6880% |

Percentages are rounded down and normalized by the same analytic global reference-peak upper bounds as earlier point witnesses. They concern the decoded-node real-affine cellPoint field on a nonzero-volume ball, not all-domain percentage errors, global extrema or native arithmetic derivatives. All three analytic JSONs reproduce byte for byte in a guarded Git-directory-free same-host selected export. Controls exercise zero-crossing intervals, exact norms and broad uncertainty; no sharp-minimum claim is made. These exploratory local results do not prove nonconvergence, singularity, molecular alignment or a viscosity law, and do not upgrade original acceptance gates.

Evidence: `evidence/cell-point-matrix-native-query-v1` contains complete small native CSVs, logs and source/binary/field receipts; probe binaries remain in hosted artifacts with recorded digests. `evidence/cell-point-uniform-ball-error-v1` contains analytic enclosures and guarded replay receipts. Public capture bundles and their hashes remain in the earlier release. Reproduction uses locked verification dependencies, matrix protocols and tools `run_of13_cell_point_matrix_query`, `analyze_of13_cell_point_matrix_query`, and `audit_cell_point_uniform_ball_error`; preserve fresh output directories and the full frozen SHA in receipt arguments.

No new upstream defect is established: actual search agrees at the exercised samples. The demonstrated issue remains the difference between a residual/mean acceptance result and local pointwise field quality. Global mesh/continuity/error maxima, general floating search behavior, remaining proof identities and physical hypotheses stay open. The complete goal remains active.

The full local suite after these changes passes: **359 passed, 1 skipped, 89 subtests**.
