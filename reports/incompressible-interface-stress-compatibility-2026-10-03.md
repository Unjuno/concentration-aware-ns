# Incompressible interface compatibility and an exact planar shear control

Date: 2026-10-03

This adds a compatibility constraint missing from the independent-tensor
controls in `openfoam-stress-operator-source-link-2026-10-03.md`. It also
derives a compatible weak continuum solution and solves a specified FV
resistance chain exactly. No OpenFOAM binary or upstream reproducer was run.

## A compatible gradient jump has zero normal transpose correction

Let `A_ij=partial_j U_i` use the mathematical velocity-gradient convention.
At a planar interface with unit normal `n`, assume that velocity is continuous,
has a common differentiable tangential trace, and has piecewise C1 one-sided
gradients. For every tangential vector `t`, differentiating the common trace
gives `[A]t=0`. Hence the gradient jump has the form `[A]=b outer n`.
If velocity is incompressible on both sides, then
`0=tr([A])=b dot n`.

The pinned source's Gauss gradient uses derivative index first. The exact
continuum gradient in that convention is `grad_FOAM_exact(U)=A.T`; this does
not identify the numerical `fvc::grad(U)` estimator with the exact gradient
for an arbitrary sampled field. Its
[`vector & tensor`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/OpenFOAM/primitives/Tensor/TensorI.H#L483-L494)
contraction is the row product, and
[`dev2`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/OpenFOAM/primitives/Tensor/TensorI.H#L590-L594)
subtracts two thirds of the trace. Therefore, exactly,

`n.T*[dev2(T(grad_FOAM_exact(U)))] = n.T*dev2([A])`
`= (b dot n)*n.T/3 = 0`.

The differential trace argument is an explicit analytical premise; SymPy
checks the rank-one, trace and contraction algebra for arbitrary symbolic
vectors, including tangent jumps represented by a cross product.

Consequently a fixed nonzero jump in the normal-contracted explicit tensor is
not admissible for this continuum class. With bounded piecewise C2 derivatives
and normal-aligned adjacent samples, the contracted difference is `O(h)`.
A bounded coefficient jump with common linear weights then produces a face
flux mismatch `O(h^3)` in 3D and a correction-density mismatch `O(1)` in the
two neighbouring cell layers. For fixed interface area, the volume L1 mismatch
is `O(h)` and volume L2 squared is `O(h)`. The earlier `1/h` residual-density
control prescribed a fixed independent tensor jump; it is not transferred to
this compatible class. Discrete gradient errors, mismatched schemes, slip or
discontinuous velocity traces, and inaccurate interface normals remain outside
the lemma.

## A compatible piecewise-viscosity Couette solution

Take `x in [-1,1]`, interface `x=0`, density one, positive constant
`mu_left` and `mu_right` on the two sides, and

`U=(0, tau*x/mu_side, 0)`, `p=constant`, `forcing=0`.

The relative ratios below require `tau != 0`. The checker rejects zero
traction or a symbolic traction without a nonzero assumption rather than
returning undefined relative metrics.

This velocity is continuous and divergence-free, its convective term is zero,
and its viscous shear traction is `mu_side*partial_x U_y=tau` on both sides.
Normal velocity is zero, so the prescribed material interface stays stationary.
The full stress has continuous normal traction and zero distributional
divergence. The velocity is piecewise smooth with a derivative kink; this is
a weak interface solution, separate from the original smooth MMS benchmark.

Here `n=(1,0,0)`, `A_yx=tau/mu_side`, and `n.T*A=0`. The exact explicit
transpose-gradient correction is zero. The shear traction resides in the
normal-derivative/implicit diffusion part. Thus a coefficient-contrast effect
in this control must be traced to that part rather than assigned to a jump
of the exact contracted explicit tensor.

## Exact two-point FV stencil and three-grid solution

The captured scalar-coefficient
[`Gauss Laplacian specialization`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/finiteVolume/laplacianSchemes/gaussLaplacianScheme/gaussLaplacianSchemes.C#L35-L56)
passes `gamma*magSf` and the normal-gradient distance coefficient into the
[uncorrected matrix kernel](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/finiteVolume/laplacianSchemes/gaussLaplacianScheme/gaussLaplacianScheme.C#L45-L65).
The
[`snGrad` kernel](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/finiteVolume/snGradSchemes/snGradScheme/snGradScheme.C#L119-L133)
uses the neighbour-minus-owner difference. With an orthogonal Cartesian mesh,
an uncorrected normal gradient, and specified fixed-value wall data, this
reduces to the scalar face conductance `mu_face/h` (unit area).
The source trace establishes that conditional stencil model; it does not
execute its packaged implementation.

For an even uniform `n`-cell grid, `h=2/n`, with the interface on a face,
the exact centre values give the interface secant
`tau*(1/mu_left+1/mu_right)/2`. Arithmetic coefficient interpolation yields
the face traction ratio

`Q = (mu_left+mu_right)^2/(4*mu_left*mu_right)`.

At contrast 100, `Q=10201/400=25.5025`. This is the face flux evaluated
on the exact centre values. The solved discrete field adjusts to the common
flux of its resistance chain. Including half-cell wall resistances,

`R_h=(1-h/2)*(1/mu_left+1/mu_right)+2*h/(mu_left+mu_right)`,

and its common shear flux satisfies

`tau_h/tau = 1/[1-(h/2)*((mu_right-mu_left)/(mu_right+mu_left))^2]`.

Therefore `1 <= tau_h/tau < n/(n-1)` for positive unequal viscosities, and
the relative flux error is first order in `h`, with

`lim_(h->0) ((tau_h/tau-1)/h) = (mu_right-mu_left)^2/[2*(mu_right+mu_left)^2]`.

| Cells | h | Solved arithmetic relative flux error | Harmonic flux/cell-value error |
|---|---|---|---|
| 16 | 1/8 | 6.3885539% | exactly zero |
| 32 | 1/16 | 3.0954013% | exactly zero |
| 64 | 1/32 | 1.5241119% | exactly zero |

The harmonic interface coefficient
`2/(1/mu_left+1/mu_right)` exactly equals the series resistance of the
two half cells. It recovers the continuum flux and every reference cell value
in this aligned piecewise-linear control. This comparison does not recommend
a blanket scheme replacement on general nonorthogonal, moving, mixed-density
or VoF meshes.

All cell flux balances of either solved chain are exactly zero. Thus exact
discrete balance is compatible with the arithmetic solution's finite error.
The large exact-nodal face mismatch also does not determine the solved-field
error. Viscosity is prescribed throughout; the calculation changes the
numerical resistance, not the material's constitutive viscosity.

## Evidence and next operator check

Seven further pinned-source files match the local tree by hash, including the
tensor convention and scalar Laplacian/normal-gradient kernels. The evidence
manifest is `evidence/upstream-refresh/openfoam-interface-diffusion-source-2026-10-03.json`.
Ten exact controls and five tests pass. The tests independently assemble and
solve the stiffness matrix at n=6 and n=12 for both interface means, checking
the resistance-chain values and zero residual exactly. The 16/32/64 results
are rational arithmetic; their displayed percentages are rounded conversions.

```sh
work/reference-check-env/bin/python -m pytest -q tests/test_interface_stress_compatibility.py
work/reference-check-env/bin/python -m tools.check_interface_stress_compatibility
```

The result is `evidence/tests/interface-stress-compatibility-2026-10-03.json`.
A next preregistered package-level test should compare the actual face
coefficient, normal gradient, computed explicit gradient term, assembled
matrix and solved shear field on aligned orthogonal grids, preserving source,
package and boundary data. That could isolate discrete-gradient and diffusion
effects before attempting the full existing squeeze-flow case. The current
analysis establishes no violated upstream contract and supplies no new Issue.
