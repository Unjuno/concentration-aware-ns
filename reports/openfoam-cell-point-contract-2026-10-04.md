# OpenFOAM cellPoint source contract and missing geometry — 2026-10-04

A named built-in interpolation is relevant to the previous point-gradient
witness: Foundation 13 `cellPoint` combines cell-centre values with shared
vertex values by tetrahedral barycentric interpolation. Under a valid finite
conforming, nondegenerate tetrahedral partition, its idealized real-arithmetic
field is continuous piecewise affine and Lipschitz, and interpolates each cell
centre. It is a specific candidate for the previous bound, not a canonical
continuum interpretation of every solver field.

**Actual-case application remains unverified:** all four original mean-quality
raw archives lack polyMesh members. Their final decomposition, fallback
behavior and actual cellPoint evaluations therefore cannot be certified from
these archives. The source also has a degenerate-tetrahedron fallback which
can destroy exact centre interpolation. These are explicit conditions, not
reasons to label the solver defective.

## Pinned source trace

Eight files were compared byte-for-byte to Git blobs at
`18870c24d21c6b982e2cdec27b2f59738cca5f90`.
Their SHA256 digests and immutable URLs are in
[analysis.json](../evidence/of13-cell-point-contract-v1/analysis.json).
All carry GPL-3.0-or-later source notices; no upstream source was changed or
copied into this evidence package.

- [`interpolationCellPoint.H`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/interpolation/interpolation/interpolationCellPoint/interpolationCellPoint.H)
  declares the `cellPoint` runtime name and describes tetrahedral linear
  interpolation using centre and vertex values.
- `interpolationCellPointI.H` implements the weighted sum of one cell value
  and three vertex values. In exact arithmetic a centre's barycentric
  coordinates are (1,0,0,0), so that sum reproduces the cell value.
- `interpolationCellPoint.C` initializes the point interpolator and tet base
  addressing. `interpolationVolPointInterpolation.C` builds one point field
  through volPointInterpolation (or accepts a supplied point field).
- `tetIndicesI.H` constructs tetrahedra with the cell centre as first vertex;
  the other three vertices come from the face triangle. Owner/neighbour
  reversal swaps triangle orientation. `polyMeshTetDecomposition.C` is the
  decomposition path. Consistent shared-face triangles and point values are
  needed to identify their affine traces.
- `cellPointWeight.C` searches tetrahedra and, if necessary, falls back to the
  nearest one. In
  [`tetrahedronI.H`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/OpenFOAM/meshes/primitiveShapes/tetrahedron/tetrahedronI.H),
  point-to-barycentric conversion tests the determinant against `small`;
  a near-degenerate tetrahedron returns four equal quarter weights. The
  resulting interpolation need not equal the stored centre value.

The source identification is a bounded trace of these files. It is not a
formal verification of C++, compiled binary equivalence, all search behavior,
all boundary conditions or every mesh accepted by OpenFOAM.

## Exact affine controls

For a shared triangular face at z=0, let its scalar trace be
`F(x,y)=p+(q-p)*x+(r-p)*y`. Two synthetic tetrahedra have centre vertices
(0,0,-1), (0,0,1), with values a,b. The affine fields are

```text
w_minus = F(x,y) + (p-a)*z
w_plus  = F(x,y) + (b-p)*z.
```

SymPy checks exact centre interpolation, equal face traces, and
`d_z w_minus + d_z w_plus = b-a`. The triangle inequality then gives
`max(abs(d_z w_minus),abs(d_z w_plus)) >= abs(b-a)/2`.
All 125 integer triples a,b,p in [-2,2] pass the exact scalar chord control.
These componentwise affine identities explain the regularity/interpolation
mechanism; they are not an execution of upstream code on the archived mesh.

The quarter-weight fallback's centre error is
`(a+p+q+r)/4-a`, which is not identically zero. A separate independent negative
control uses two constant cell patches with values -1 and +1: both classical
interior derivatives are zero, while the point chord is one and the face has
a jump. This verifies why continuity/Lipschitz regularity is indispensable.
A cell-constant representation cannot inherit the continuous chord theorem.

## Archive check and next required capture

All four raw archives and every member digest were verified against their
original manifests. Each archive contains zero members with `/polyMesh/` in
the name. The frozen archiver saves initial dictionaries, logs, final U/p,
stage CSVs and module files, rather than the full evolved mesh. This is an
evidence limitation; it does not prove the actual meshes were degenerate.

The n64 [point witness](openfoam-amr-point-gradient-bound-2026-10-04.md)'s
46.1968% lower bound therefore remains conditional. To apply it to a named
idealized cellPoint reconstruction, one must validate the actual conforming
nondegenerate partition and shared point field, or otherwise establish the
needed Lipschitz and endpoint properties. Floating implementations require
explicit endpoint discrepancy/rounding accounting; source-level exact
barycentric identities alone cannot supply that. There is no pointwise curl
transfer or original gate upgrade.

A [prospective capture specification](../evidence/of13-cell-point-contract-v1/prospective-capture-requirements.json)
now lists the effective mesh files, tet addressing/coordinates, point values,
centre and shared-face tests, fallback counters, scheme selection and binary
identity needed for the next successor experiment. It is a specification only;
no such run is claimed. Original archives and frozen source files stay unchanged.
The local Docker observability limitation does not change any solver verdict.

## Reproduction and scope

Numerical source: `5207235c60417112cb35e620df8e9ecde37b8d75`.
The original CFD source remains `3566f89058071910a41bb68010eb258c7bbc3d74`.
Use an upstream checkout at the immutable pin and the original four-case raw
archive map, then run:

```bash
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_cell_point_contract \
  --upstream /absolute/path/OpenFOAM-13 --raw-map /absolute/path/raw-map.json \
  --output /absolute/path/new-result \
  --source-commit 5207235c60417112cb35e620df8e9ecde37b8d75
```

The complete locked benchmark suite passed **312 tests, 1 skipped, 83 subtests**.
Compile checks and `git diff --check` passed. Logs and source hashes are in
[the evidence package](../evidence/of13-cell-point-contract-v1/README.md).

The audit executes symbolic controls and source/archive hash verification.
It intentionally uses read-only Git; no clean-export replay, actual cellPoint
C++ evaluation, new CFD run or full upstream suite is claimed. This narrows
source interpretation and identifies exact missing runtime evidence. It does
not show a violated contract, singularity, particle alignment or viscosity
change. The full benchmark goal remains open.
