# Enclosed local cellPoint affine derivative witness — 2026-10-04

One actual n16 capture tetrahedron now supplies an Arb96 local derivative-error
witness for the **idealized real-arithmetic affine piece** of cellPoint's explicit
barycentric overload. At its strict interior centroid, gradient Frobenius error
is at least **95.1187%** of the analytic reference's global peak and curl error
at least **9.1092%** of the analytic reference's global curl peak. Quotes are
rounded down from exact rational lower endpoints. These are error-field norms
at a point, not differences between peak values or original gate upgrades.

## Exact local definition

The native capture source is `4999a4db38d0ac41a5f253a6665f6701d64f561c`;
the data come from the [executed successor](openfoam-cell-point-capture-n16-2026-10-04.md).
Tet CSV row 71793 has cell 5332 and face 22295. Its four nodes are the decoded
cell centre followed by its three decoded mesh vertices. Nodal velocity values
are the decoded stored cell value followed by captured shared point values.
These are precisely the inputs of the source's explicit barycentric weighted
sum, interpreted in real arithmetic. No exact cell-average assumption is used.

Let A have rows p_i-p_0, and D have rows U_i-U_0 for i=1,2,3. The affine
Jacobian is G=(A^-1 D)^T. Its evaluation point is (p_0+p_1+p_2+p_3)/4, with
strictly positive quarter barycentric weights. Arb encloses the edge-matrix
determinant around 0.003784945883825610906844409461 and excludes zero, so the
local inverse and interior point are well-defined. This A orientation differs
from the probe's native point-to-barycentric determinant convention.

The analytic gradient is independently evaluated using g=cos(q/2)^8,
g'=-4*cos(q/2)^7*sin(q/2), and
 g''=14*cos(q/2)^6*sin(q/2)^2-2*cos(q/2)^8.
The reference uses N=3 and exact decimal t=0.05. For E=G-grad(u), the local
curl error is directly
`(E[2,1]-E[1,2], E[0,2]-E[2,0], E[1,0]-E[0,1])`.
Its norm is enclosed independently of the Frobenius norm. This is not a curl
inference from the earlier point-chord lower bound.

The absolute error lower endpoints are divided by upper endpoints of the
already audited global reference peak bounds:
`exp(-0.05)*sqrt(86/81)` for gradient, and
`exp(-0.05)*sqrt(122/81)` for curl. The data, coordinates, matrix entries and
exact rational interval endpoints are in
[analysis.json](../evidence/cell-point-local-derivative-v1/analysis.json).

## Search, replay and validation

A floating batched solve screens all 207,488 captured pieces at their centroids
and selects one gradient-error witness. It does not certify the global maximum
or the best curl witness. The selected tet's gradient, determinant, centroid,
reference derivative and both error norms are then recomputed with Arb96 from
exact binary64-decoded data. Every capture file hash is checked before use.

Three independent controls recover a known vector affine map under vertex
permutations, compare the independent analytic gradient with the Fourier
reference, and reject a degenerate tetrahedron. The full locked benchmark
suite passes **318 tests, 1 skipped, 83 subtests**. Compile checks and
`git diff --check` pass. A selected Git export without .git reproduces the
analysis JSON byte-for-byte under Python audit-hook checks for subprocess,
socket, spawn/fork and Git-object opens. Tools modules originate inside the
export; data are external hash-checked capture files. This uses same-host
locked dependencies, not an independent CFD execution or whole-history replay.

Numerical source: `dc61811614770da398324339665a48a4d4ffb098`.
Download and verify the [capture release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-cell-point-capture-v1-4999a4d),
then run from this source with a fresh output directory:

```bash
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_cell_point_local_derivative \
  --evidence /absolute/path/capture-evidence --output /absolute/path/new-witness \
  --source-commit dc61811614770da398324339665a48a4d4ffb098
```

## Interpretation boundary

This proves a local property of the explicitly defined affine piece family.
It does not certify which tetrahedron the floating position-query search
selects at the centroid, nor a full nonoverlapping global partition or global
continuity. The point-query branch and floating evaluation errors require
separate checks. The named affine reconstruction also does not become the
canonical continuous solution of the solver merely because cellPoint exists.

No new CFD run is included. This n16 result neither validates larger-case
cellPoint behavior nor changes the original solver gates. It does not establish
a new upstream defect, nonconvergence, blow-up, molecular alignment or viscosity
change. Larger runtime cases, global geometry/rounding validation, other solver
quality and analytic/physical obligations remain open under the full goal.
