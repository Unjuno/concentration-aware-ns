# Verified n32 native capture and bounded-batch derivative audit — 2026-10-04

The original n32-dt0.001 recipe now has an independently verified native
cellPoint capture and public complete data. Its selected idealized affine
piece has enclosed local gradient/curl error lower bounds of **86.3341% /
9.9634%** of the analytic global reference peaks at its centroid. The full
fine/temporal matrix is still **INCOMPLETE / UNCERTAIN**: n64 is active and
n32 half-step is queued at this observation. This is not a nonconvergence or
implementation-defect result.

## Execution and capture integrity

[Hosted matrix run 37147687736](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37147687736),
job 111275277372, succeeds from runtime source
`4e60b23065811d488fe6890ad59af698a81c35b8`. Independent analysis verifies the
original twenty recipe source hashes, original initial-input and final U/p
byte identity, normal container exit, unchanged fields before/after the read-
only probe, every raw archive member and every mesh member. Eight installed
interpolation source hashes match the previously independently pinned source.
The downloaded probe binary hash matches the runtime capture receipt.

The final native mesh has 116,992 cells, 129,953 points, 1,432,320 tetrahedra
and 346,776 internal faces. Every recorded shared-face triangle matches its
owner/neighbour vertex identities. Native degenerate/invalid-base counts are
zero. Centre interpolation error is at most 1.12e-16; sampled shared-face
trace difference at most 3.76e-15. Floating cell/tet volume sums differ by
at most 2.73e-14 relative. These are integrity/topology diagnostics, not an
outward-enclosed global partition or continuity proof.

The complete [public release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-cell-point-capture-matrix-v1-4e60b23)
contains `cell-point-capture-n32-dt0.001-4e60b23.tar.gz`, 120,041,496 bytes,
SHA256 `45ebd5a9432956ad46d7419e3eed6884ac9f2ac4d100cb327bf4cae0dbddb317`.
GitHub's remote asset digest and size match the local bundle. It retains
original fields/inputs/logs, all fourteen initial/final mesh members, every
native CSV, source/binary receipts, OpenFOAM GPL license and unchanged probe
source. The binary is omitted with its digest retained. Small receipts are
tracked in [n32 evidence](../evidence/of13-cell-point-capture-matrix-v1/n32-dt0.001/).
The release explicitly describes a partial matrix.

## Bounded-batch local derivative audit

Numerical source `24af332bb51bae0aa84bb1bbfaff48b9e5f44c31` verifies capture
hashes, original input/field identity and the frozen recipe before analysis.
It retains decoded cell/point coordinate and velocity arrays, then reads only
10,000 tetrahedral rows at a time. Every label, row count, finite value and
native determinant is checked. Floating affine solves and independent analytic
centroid gradients select one gradient-error witness. This is a complete
centroid screen, not a global maximum certificate. The selected four nodes,
Jacobian, exact centroid, determinant and gradient/curl errors are recomputed
with Arb96 from exact decoded binary64 data. No exact cell-average assumption
is used. Curl is computed directly from the derivative-error tensor.

| Case | Screened pieces | Selected CSV row | Gradient error lower / reference peak | Curl error lower / reference peak |
| --- | ---: | ---: | ---: | ---: |
| n16-dt0.001 | 207,488 | 71,793 | 95.1187% | 9.1092% |
| n32-dt0.001 | 1,432,320 | 1,374,797 | 86.3341% | 9.9634% |

Quoted percentages are rounded down from exact rational lower endpoints.
The n32 target is cell 112198, face 134881, tetPt 2, with ordered mesh vertices
122968, 47284, 125035. Its centroid is approximately
(3.7920005076533045, 0.11044661672776629, 6.14819499784565).
These norms concern error at selected centroids divided by analytic **global**
reference peaks; they are not peak-value differences or whole-domain error
percentages. Curl is measured at a gradient-selected point, not its own maximum.

The n16 selected row and full interval witness content exactly match the prior
all-at-once audit. Five controls verify batch boundaries, complete finite rows,
headers and node ordering/coverage. The full locked suite passes **339 tests,
1 skipped, 89 subtests**; compile checks and `git diff --check` pass. Both case
analysis JSONs reproduce byte for byte under a guarded same-host selected Git
export without .git. Required recipe/source identities are included and checked;
external capture data are hash-verified. This is Python audit-hook isolation,
not universal C-level isolation or another CFD execution. The resident node
arrays and a whole-program memory benchmark remain separate; no fixed RSS
limit is claimed.

Run from the numerical source with fresh output directories:

```sh
python -m tools.audit_cell_point_capture_derivative \
  --capture /absolute/path/capture-evidence \
  --output /absolute/path/fresh-local-witness \
  --source-commit 24af332bb51bae0aa84bb1bbfaff48b9e5f44c31 \
  --chunk-size 10000
```

Exact rational endpoints, module-origin guards, logs and validation receipts
are in [bounded-batch evidence](../evidence/cell-point-derivative-batches-v1/).
Native selection/local-neighborhood evidence exists for the earlier n16 target;
it is not automatically transferred to the different n32 target. Other cell
geometry, global continuity, native rounding and continuous extrema remain open.

## Interpretation and remaining matrix

The n32 data establish an additional local discrepancy in a named idealized
cellPoint reconstruction. The original residual/mean-quality gates and their
P0 Gauss tensors are unchanged. The two gradient lower bounds decrease, but
neither is a certified global maximum; the two curl samples use different
points. Consequently no convergence rate, persistent fine-resolution failure
or temporal-independence conclusion follows. n64 and half-step execution,
independent checks and corresponding local witnesses must be completed first.
No new upstream defect is established and no duplicate issue is justified.
The three-project, analytic/physical and whole-goal requirements remain active.
