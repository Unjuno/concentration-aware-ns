# Native cellPoint position replay and enclosed local neighborhood — 2026-10-04

The local idealized affine witness is now connected to an **executed native
position-query replay at 19 points**. Separately, Arb128 encloses a radius-1/128
Euclidean ball around the exact decoded-node centroid inside the target
candidate tetrahedron and outside every other candidate of captured cell 5332.
These close a local candidate-overlap gap and provide finite native branch/value
evidence. They do not certify all floating inputs or global mesh continuity.

## Actual read-only native execution

[Hosted run 37146624489](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37146624489)
completed successfully from source `4bea7e3731e7e19ac1741f928f82845332f0fe71`
on an isolated Ubuntu ARM64 runner. It downloaded the existing public n16
capture bundle, checked SHA256
`ad1fb32afd6e9cb1f799945fa2967d09150fc567bd3daa11e0a62029a268e830`,
verified its frozen manifest and every raw/mesh member, and restored the original
configuration, final fields and initial/final mesh instances. No solver evolution
or forcing evaluation was run. The final U and p before/after hashes equal the
original capture; the case mount is read-only.

The runtime uses the same frozen Dockerfile and checksum-pinned Foundation 13
package. Nine installed interpolation/decomposition source files match upstream
`18870c24d21c6b982e2cdec27b2f59738cca5f90`; the stock `libfiniteVolume.so` and
`libOpenFOAM.so` match the original capture's stock-binary receipts. The probe
source, compilation log, executable digest, package list and image identity are
preserved. Captured coordinates and nodal values exactly equal the earlier
[local derivative witness](cell-point-local-derivative-2026-10-04.md).

The fixed query set is the native rounded centroid plus positive/negative
coordinate displacements at h=2^-8, 2^-12 and 2^-16: nineteen points. For every
query the native `cellPointWeight` exposes the same ordered face vertices
14487, 14486, 5089. The position overload agrees **exactly** with the explicit
tetrahedron overload at native barycentric coordinates. Reconstructed weighted
values differ by at most 2.78e-17 per component; the smallest recorded weight
is 0.21021126422702344. The target determinant is nonzero, and native debug logs
record no nearest-tetrahedron fallback.

A separate native scan records all twelve candidate tetrahedra and the source's
acceptance predicates at each query. Its first accepted candidate is consistently
face 22295 / tetPt 2, matching the exposed addressing. This scan and debug output
support the finite branch result; they are not instrumentation of every internal
instruction or a rigorous rounding bound.

| Central-difference step | Maximum component discrepancy from floating affine Jacobian |
| --- | --- |
| 2^-8 | 1.887379141862766e-15 |
| 2^-12 | 2.398081733190338e-14 |
| 2^-16 | 8.415490526658687e-13 |

These are floating secant diagnostics. The frozen verifier requires absolute
component discrepancy <=1e-8 and native weighted/explicit value discrepancies
<=2e-14. None is an interval derivative certificate for a floating program.

Cross-host reanalysis passes every frozen condition, with two NumPy
secant-reference diagnostic differences of 1.39e-16 and 1.11e-16. All remaining
analysis content agrees. Both original and independent JSON are retained;
**cross-host JSON byte identity fails**, and is not silently replaced by a
compatible result. The native CSVs remain hash-verified unchanged data.

## Exact idealized neighborhood

The analytic numerical source is `6e7dedaa61d684dd193f334e7c1195347c661f89`.
It hash-checks all original capture files and takes all twelve candidates of
cell 5332. For each decoded tetrahedron, the edge-column matrix inverse defines
its four affine barycentric weights lambda_i(x) and constant gradients g_i.
For any x in the closed Euclidean ball of radius R around c,

`lambda_i(c) - R*||g_i|| <= lambda_i(x) <= lambda_i(c) + R*||g_i||`.

Arb128 encloses the matrix inverse, all weights and gradient norms. At exact
c=(p0+p1+p2+p3)/4 and R=1/128, every weight of candidate 1 (CSV row 71793) has
lower bound at least **0.1704225**. Every other candidate has a weight whose
upper bound is at most **-0.1937302** everywhere on the ball. Thus exactly the
named target contains the ball, with strict inequalities. Exact rational
endpoints and candidate identities are in
[analysis.json](../evidence/cell-point-local-neighborhood-v1/analysis.json).
The largest squared distance of any decoded native query point is below
1.526e-5, strictly less than R^2=1/16384; every native candidate identity matches
the analytic list at every query.

This proves local real-arithmetic uniqueness among the complete **captured
candidate list of one cell**. It supplies a neighborhood on which the named
idealized affine derivative is defined, strengthening the earlier isolated
interior-point result. It does not extend the earlier **95.1187% gradient /
9.1092% curl error lower bounds at the centroid** to every point in this ball.
No exact cell-average assumption is used. No automatic cell-location or global
mesh partition proof is supplied.

## Verification and reproduction

Eight query-verifier/archive controls reject wrong addressing despite matching
values, missing queries/scans, false acceptance, constant substituted values,
changed archive digests, traversal and link members. Four analytic controls
exercise a known isolated tetrahedron, overlapping candidates, a ball crossing
a face and a degenerate candidate. The full locked suite passes **330 tests,
1 skipped, 85 subtests**. Compile checks and `git diff --check` pass. A guarded
Git-directory-free selected export reproduces the analytic neighborhood JSON
byte for byte with locked same-host dependencies; this is distinct from the
cross-host floating diagnostics above.

Use the [original public capture release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-cell-point-capture-v1-4999a4d),
the frozen protocol and source revisions. The native workflow restores the
bundle and runs:

```sh
python -m tools.run_of13_cell_point_query \
  --bundle /absolute/path/cell-point-capture-n16-4999a4d.tar.gz \
  --image concentration-aware-ns:of13-cell-point-query-v1 \
  --source /absolute/path/pinned-OpenFOAM-13 \
  --work /absolute/path/fresh-query-work \
  --evidence /absolute/path/fresh-query-evidence
python -m tools.analyze_of13_cell_point_query \
  --evidence /absolute/path/fresh-query-evidence
python -m tools.audit_cell_point_local_neighborhood \
  --capture /absolute/path/capture-evidence \
  --output /absolute/path/fresh-neighborhood-evidence \
  --source-commit 6e7dedaa61d684dd193f334e7c1195347c661f89
```

The source directory must make the pinned upstream Git objects available.
The Docker image is built with `runtime/of13-interface-operator/Dockerfile`.
Large original mesh/field data remain in the existing public release; all small
native replay outputs, build/source/binary receipts and independent checks are
tracked in [native evidence](../evidence/of13-cell-point-query-v1-n16/).

## Remaining scope and upstream disposition

Arbitrary floating input selection/rounding, other cells, global continuity,
larger n32/n64 captures, whole-domain extrema and original gates remain open.
A cellPoint interpolant is a named reconstruction, not an upstream promise that
stored fields constitute an exact continuum solution. This is evaluation
coverage evidence, not a reproduced implementation defect; no new upstream
issue is justified. The three-project comparison, mathematical/physical
interpretation and full-goal completion requirements remain unchanged.
