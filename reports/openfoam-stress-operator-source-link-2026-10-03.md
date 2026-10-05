# Source-linked stress-flux and conservative-assembly controls

Date: 2026-10-03

Disposition: analytical operator controls; existing upstream Issue #2 remains
unreproduced here. No solver or upstream post was performed.

A subsequent [incompressible-interface compatibility audit](incompressible-interface-stress-compatibility-2026-10-03.md)
proves that the fixed contracted tensor jump used by the synthetic planar
control is excluded under continuous velocity, common differentiable
tangential traces and one-sided incompressibility. It also gives a compatible
piecewise-shear control for the implicit diffusion term. Read that constraint
before interpreting the independent-tensor norm-growth example.

## Pinned source trace

The source capture binds 22 file/revision pairs to immutable raw URLs, SHA-256,
calculated Git blob IDs and line counts. All 13 current-source files match the
local source tree byte for byte. The source file `linearViscousStress.C` at
change `6592798ca0704aa6eaaaaf74ea3cc6a9553317dc` is byte-identical to the
current pinned file at `18870c24d21c6b982e2cdec27b2f59738cca5f90`. This is
public-source identity, not equivalence to the installed Foundation package.
The source headers declare GPL-3.0-or-later; the files themselves are not
vendored in the evidence record.

Let `a=alpha*rho*nuEff` and `G=dev2(T(grad(U)))`. The parent of the change,
[`909a5f5`](https://github.com/OpenFOAM/OpenFOAM-13/blob/909a5f52bd9f2a059c35da16b1caeff287c5af9b/src/MomentumTransportModels/momentumTransportModels/linearViscousStress/linearViscousStress.C#L80-L100),
passes the cell tensor `-a*G` to `divDevTauCorr`. Its
[`momentumTransportModel`](https://github.com/OpenFOAM/OpenFOAM-13/blob/909a5f52bd9f2a059c35da16b1caeff287c5af9b/src/MomentumTransportModels/momentumTransportModels/momentumTransportModel.C#L142-L163)
already converts that tensor through `fvc::flux` before `fvm::divc`.
[`fvc::flux`](https://github.com/OpenFOAM/OpenFOAM-13/blob/909a5f52bd9f2a059c35da16b1caeff287c5af9b/src/finiteVolume/finiteVolume/fvc/fvcFluxTemplates.C#L44-L54)
selects an interpolation scheme using a `flux(field-name)` key. This parent
trace must not be simplified to an assumed direct volume-tensor divergence;
it is also not a reproduction of the entire version-12/version-13 issue case.

The [current explicit correction](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/MomentumTransportModels/momentumTransportModels/linearViscousStress/linearViscousStress.C#L89-L113)
first interpolates `a`, then multiplies that face coefficient by
`fvc::dotInterpolate(Sf,G)`, with the negative stress sign. Each expression
can select a [field-name interpolation entry](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/interpolation/surfaceInterpolation/surfaceInterpolation/surfaceInterpolate.C#L78-L90).
The [linear scheme](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/interpolation/surfaceInterpolation/schemes/linear/linear.H#L90-L97)
returns the common mesh weights, independently of the field. The
[internal-face contraction kernel](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/interpolation/surfaceInterpolation/surfaceInterpolationScheme/surfaceInterpolationScheme.C#L224-L300)
uses the owner/neighbour weighted tensor contracted with the same face vector.
The [scheme wrapper](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/interpolation/surfaceInterpolation/surfaceInterpolationScheme/surfaceInterpolationScheme.C#L325-L353)
adds a separate correction for corrected schemes.

## Exact face difference and its conditions

For common uncorrected linear weights and the same endpoint tensor values,
the new-minus-parent negative correction flux is exactly

`delta_F = w(1-w)(a_P-a_N) [Sf & (G_P-G_N)]`.

The checker verifies all three contracted vector components. Under the
documented smooth single-phase constant-coefficient, default-linear benchmark
settings, the coefficient difference vanishes. This mechanism does not explain
that frozen benchmark's observed coarse-grid local errors.

Common weights are a substantive premise. With `delta_a=a_P-a_N` and
`delta_G=G_P-G_N`, independently selected weights `p`, `x`, `y` for the product,
coefficient and tensor give the uncorrected component difference

`(p-y)*a_N*delta_G + (p-x)*G_N*delta_a + (p-x*y)*delta_a*delta_G`.

Corrections `C_product`, `C_coefficient`, `C_gradient` add
`C_product-C_coefficient*I_y(G)-C_gradient*I_x(a)-C_coefficient*C_gradient`.
Thus even constant `a` need not cancel if the product/tensor weights or
corrections differ. A fixed exact counterexample has `a_P=a_N=2`,
`G_P=0,G_N=1`, `p=x=1/2,y=3/4`, giving difference `1/2`.

Noncoupled boundary faces use patch values instead of the two-cell blend.
For a coupled face, the simple identity additionally requires coherent product
endpoint values in a common coordinate frame. Multi-donor or nonconformal
neighbour maps need not commute with multiplication: a synthetic equal blend
of endpoint pairs `(a,G)=(1,3),(3,1)` gives blended product `3`, but product
of blends `4`. This is a control for the missing premise, not a reproduction
of a particular coupled-patch implementation.

## Conservative assembly does not bound the local difference

The current source routes the correction through
[`fvm::divc`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/finiteVolume/fvm/fvmDiv.C#L101-L122),
`fvc::div(surface-field)`, and
[`surfaceIntegrate`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/finiteVolume/fvc/fvcSurfaceIntegrate.C#L43-L75).
On a stationary mesh with `Vsc=V`, an internal-face difference contributes
`+delta_F/V_P` to its owner and `-delta_F/V_N` to its neighbour. The checker
verifies exact cancellation of the volume-weighted signed sum on a three-cell,
two-face graph. The matrix source from `fvm::Su` has the corresponding negative
volume factor; the displayed density is the divergence/LHS correction
convention, not a prediction of particle acceleration.

Consider a prescribed planar face mismatch with a fixed contracted component
`c` per unit face area, fixed interface area `A`, cubic cells of width `h`,
and one layer on each side. Then `A/h^2` faces have `delta_F=h^2*c`; the two
cell layers have residual-density differences `+c/h` and `-c/h`. Exactly,

`signed integral = 0`,
`volume L1 = 2*A*abs(c)`,
`volume L2^2 = 2*A*c^2/h`,
`Linf = abs(c)/h`.

For the smooth linear test function `phi=x` across the layers, the signed
action is `-A*c*h`, which tends to zero. Consequently the synthetic local norm
growth coexists with global conservation and weak cancellation. It cannot be
interpreted as a continuum blow-up or solution-error divergence. It does show
why a signed global balance alone is an inadequate diagnostic of this local
operator mismatch.

## Product-constant control and next evidence

Prescribe independent coefficient/tensor component values
`a_P=1,a_N=r,G_P=t,G_N=t/r`, so both endpoint products equal `t`.
Product interpolation preserves `t`, while separately interpolating the
factors gives

`t*[1+w(1-w)*(r+1/r-2)]`.

At `w=1/2,r=100`, the ratio is exactly `10201/400=25.5025`. This exact
overshoot is a partial-flux control. The chosen tensor is not proven to be
`dev2(T(grad(U)))` for a compatible continuous incompressible velocity, and
the implicit Laplacian, normal-gradient term, boundaries, pressure coupling
and solved velocity are not compared. No formulation is declared defective or
preferable from this control.

A next numerical test would need an independently manufactured,
interface-compatible velocity/coefficient pair and its full stress/forcing,
then separately compare correction flux, total traction, conservation and
solution error across spatial/time refinement. Its protocol and tolerances
must be frozen before production. The existing
[Issue #2](https://github.com/OpenFOAM/OpenFOAM-13/issues/2) remains the proper
related record; these exact controls do not justify a duplicate report.

## Replay

The symbolic checker passes ten exact controls. Five tests independently
exercise product-constant contrast, mismatched weights, face cancellation,
planar refinement scaling and rejection of changed source bytes.

```sh
work/reference-check-env/bin/python -m pytest -q tests/test_openfoam_stress_operator.py
work/reference-check-env/bin/python -m tools.audit_openfoam_stress_operator
# Optional current-source identity recheck; source files are not needed for algebra replay:
work/reference-check-env/bin/python -m tools.audit_openfoam_stress_operator \
  --source-root work/openfoam13-source-20260624
```

The source manifest is
`evidence/upstream-refresh/openfoam-stress-operator-source-2026-10-03.json`;
the exact result is
`evidence/tests/openfoam-stress-operator-controls-2026-10-03.json`.
To rebuild the source identity check elsewhere, download each current-role
`raw_url` from that manifest to its `path`, verify its SHA-256, and run the
optional command against that root. Default report replay recomputes algebra
and binds the captured manifest hash; it does not refetch upstream sources,
execute the packaged solver, or reproduce the attached squeeze-flow case.
