# Foundation 13 interface operator probe

This custom utility exercises a specified stationary scalar diffusion operator
on an aligned Cartesian Couette control. It reads `U`, `shear`, `mu`, and
`constantControl` at the case's start time; generated cases must use time zero.
The intended data are `x in [-1,1]`, `mu=1/100` on the two halves,
`U=(0,tau*x/mu,0)`, `shear=U_y`, positive coefficients and nonzero `tau`.
The x walls have exact fixed values and y/z patches are conformal,
translational cyclic pairs. The intended constant control is one in every cell
and at both fixed walls. Neither control supplies a pressure, phase transport,
constitutive law, or full momentum solve.

The utility source was checked against Foundation 13 commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90`. Source authoring does not establish
compilation, source/package equivalence, or a successful execution. Preserve
the actual package, image, build and execution evidence separately.

## Build and invocation

`Dockerfile` uses the same immutable base and official Foundation package as
`runtime/openfoam13/Dockerfile`, with a bounded resumed download and the same
final package SHA256 check. Its acquisition change follows hosted run
37117700448, which stopped during a partial transfer before compilation. The
frozen recipe/harness commit and actual image ID are recorded independently.


After loading the Foundation 13 environment, compile from this directory with
`wmake`; `Make/files` writes `/probe/interfaceOperatorProbe`. The only required
runtime argument is the standard case argument:

```sh
/probe/interfaceOperatorProbe -case /probe/cases/nx16
```

This utility is serial. Case `fvSchemes` must specify `Gauss linear` gradients,
linear interpolation, `orthogonal` normal gradients and `Gauss linear
orthogonal` Laplacians. The utility requests the explicit key
`laplacian(muFace,shear)` for every matrix and uses the solver dictionary
`mesh.solution().solverDict("shear")`, including for renamed solution fields.
There is no relaxation or reference-cell modification. Each mode starts from
an independent copy of the input exact-nodal shear field. The constant control
is assembled and sampled without a solve.

Arithmetic `muFace` is `fvc::interpolate(mu)`. Harmonic `muFace` is a complete
copy of that surface field, including every boundary patch, with internal
coefficients replaced by
`1/((1-w)/mu_owner+w/mu_neighbour)`. Here `w` is the ordinary owner interpolation
weight; reversing it implements the series-resistance distances. On the
uniform interface the coefficient is `200/101`. Boundary values stay copied
because both sides of each translational periodic pair have the same material
coefficient, and the fixed walls each meet only one material. This conditional
construction is not a general coupled-patch harmonic implementation.

## JSON schema version 1

The five output files are:

- `probe/arithmetic/before.json`
- `probe/arithmetic/after.json`
- `probe/harmonic/before.json`
- `probe/harmonic/after.json`
- `probe/constant/before.json`

Each file is valid JSON with finite numbers at 17-digit stream precision.
Vectors are `[x,y,z]`; tensors use
`[xx,xy,xz,yx,yy,yz,zx,zy,zz]`. Cell arrays use the native cell order. Every
face array uses the native global face order: internal faces first, then the
boundary ranges specified by each patch's `start` and `size`.

```text
schemaVersion: 1
mode: arithmetic | harmonic | constant
stage: before | after
fieldName: actual renamed scalar field
operator: negative_fvm_laplacian
fieldDimensions, equationDimensions: seven dimension exponents
cells:
  centres[N][3], volumes[N], values[N], rawDiag[N], completeDiag[N],
  source[N], nativeResidual[N], divPhysicalFluxTimesVolume[N]
internalMatrix:
  owner[Ni], neighbour[Ni], upper[Ni], lower[Ni], symmetric, hasLower
faces:
  centres[Nf][3], areas[Nf][3], owner[Nf], neighbour[Nf], gamma[Nf],
  deltaCoeffs[Nf], snGrad[Nf], physicalFlux[Nf], matrixFlux[Nf]
patches:
  [{name, type, fieldType, start, size, coupled, faceCells[],
    internalCoeffs[], boundaryCoeffs[], neighbourValues[]}]
solverPerformance:
  null before a solve and for the constant control;
  {initialResidual, finalResidual, iterations} after a solve
explicitCorrection:
  null for the constant control;
  {coefficientMode: arithmetic, gradU[N][9], dev2TransposeGradU[N][9],
   separateFlux[Nf][3], parentProductFlux[Nf][3],
   divSeparateTimesVolume[N][3], divParentProductTimesVolume[N][3]}
```

Boundary `faces.neighbour` entries are `-1`. Patch `type` is the mesh patch
type; `fieldType` records the scalar boundary-condition type. Coupled
`neighbourValues` are the actual `patchNeighbourField()` values; other patches
have empty arrays. The independent replayer must reconstruct cyclic neighbour
cell addresses from the preserved geometry and patch topology.

## Operator and residual conventions

The matrix is `-fvm::laplacian(muFace,shear)`: positive diagonal and negative
off-diagonal for this scalar control. Its raw `source` excludes boundary
completion. `completeDiag` is `fvMatrix::D()`, including patch internal
coefficients. A complete independent system adds noncoupled `boundaryCoeffs`
to the RHS and coupled `-boundaryCoeffs` at each neighbour column. A fixed-wall
boundary coefficient already includes its prescribed value. Do not multiply
it by that value again. Const lduMatrix accessors expose symmetric lower/upper
coefficients without allocating different matrix storage.

`physicalFlux=muFace*magSf*snGrad(shear)` is outward-oriented positive diffusion
flux; `matrixFlux` from this negative-Laplacian matrix has the opposite sign.
At a fixed wall, `deltaCoeffs=2/h`, so the conductance is
`2*muFace*area/h`. `divPhysicalFluxTimesVolume` is cell-integrated physical
flux balance, not a residual density or a normalized solver residual.

The native scalar `fvMatrix::residual()` is deliberately saved without
adjustment. In the pinned source, `fvScalarMatrix.C:188-205` uses the ldu
interface residual and then calls `addBoundarySource` with the default
`couples=true`. Under scalar translational cyclic coupling, source inspection
predicts an additional `sum(boundaryCoeffs*neighbourValue)` beyond complete
`b-Au`. The scalar solve instead uses `addBoundarySource(...,false)` in
`fvScalarMatrix.C:155-170`. The generic residual template adds the same boundary
source before rather than after the ldu call; it is not the scalar execution
path used here. These are source-level predictions to check against the actual
package, not an execution result or an established upstream defect. In the
specified `Ny=Nz=2`, unit transverse-width constant control, each cell's y and
z cyclic conductance is `h`; native residual is predicted to be `2*h`, while
complete matrix and physical-flux residuals are zero.

## Explicit correction diagnostic

For each Couette snapshot, the utility copies input `U`, replaces its internal
y component by that snapshot's shear values, evaluates its boundaries and
computes `G=dev2(T(fvc::grad(U)))`. It saves the negative stress corrections
`-interpolate(mu)*dotInterpolate(Sf,G)` and `fvc::flux(-mu*G)`. Both comparisons
use the arithmetic coefficient expression, even when the separately solved
scalar diffusion matrix uses harmonic coefficients. This preserves the
common-linear source comparison without silently changing two operators.

The x-face correction is zero for this shear structure. Individual y-cyclic
correction vectors can be nonzero and cancel in divergence. The Gauss
gradient estimator near the derivative kink need not equal the exact
continuum gradient. Save and compare those quantities separately. Matrix
balance, solve residuals, face interpolation error and solution error answer
different questions; none alone supplies a particle-scale or viscosity claim.

The final nonempty stdout line is `INTERFACE_OPERATOR_PROBE_COMPLETE`, emitted
only after all five snapshots have been written successfully.
