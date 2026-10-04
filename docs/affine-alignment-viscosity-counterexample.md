# Exact affine counterexample: alignment does not imply reduced viscosity

The implication under audit is: if fluid elements align under accelerating
strain, then viscosity must become less effective. A simple exact solution of
the incompressible Navier–Stokes equations disproves that implication by itself.
It is a mathematical counterexample to the inference, not a model of the
OpenAI construction, a finite-energy flow, or molecular behavior.

On all of `R^3`, fix `a>0`, any constant kinematic viscosity `nu>=0`, and set

```
u(x,y,z) = (-a x, -a y, 2 a z),
p(x,y,z) = -(a^2/2)(x^2+y^2+4z^2).
```

The velocity gradient is `A=diag(-a,-a,2a)`, so `div u=tr(A)=0` and
`Delta u=0`. The steady material acceleration is `(u·grad)u=A^2 x`, while
`-grad p=A^2 x`. Therefore

```
partial_t u + (u·grad)u = -grad p + nu Delta u
```

holds identically for every `nu`; the viscous force is exactly zero. This
solution has nonzero constant constitutive viscosity. Nothing in the solution
makes that coefficient decrease. The example does not show viscosity becoming
ineffective in a flow with nonzero viscous force; it shows alignment alone
cannot establish such a change.

The material map over elapsed time `s` is
`F(s)=diag(exp(-a s),exp(-a s),exp(2a s))`, with determinant one. A material
separation with nonzero axial component has transverse-to-axial ratio
multiplied by `exp(-3a s)`, so its direction approaches the axis. Yet its
volume-preserving deformation has two contracting and one expanding axes, and
the viscosity coefficient remains `nu`. The solution and its pressure are
unbounded at spatial infinity and have infinite energy; prescribed affine
boundary data on a bounded region would be needed to use it as a finite-domain
example. It makes no molecular or finite-particle claim.

This falsifies only the standalone logical bridge “alignment implies reduced
viscosity.” Testing a specific solution still requires the actual viscous,
advective, and forcing terms, their spatial scales, and a nonzero denominator
for any proposed relative-effectiveness ratio. A continuum velocity field
contains no molecular ensemble or constitutive transition law.

## Absolute speed is not a constitutive threshold

There is a separate issue with saying that viscosity changes once “the fluid
reaches a certain speed.” For forced incompressible Navier–Stokes,

```
partial_t u + (u·grad)u = -grad p + nu Delta u + f,
```

take any constant observer velocity `V` and define
`u'(x',t)=u(x'+Vt,t)-V`, `p'(x',t)=p(x'+Vt,t)`, and
`f'(x',t)=f(x'+Vt,t)`. The chain rule gives
`partial_t u' = partial_t u + V·grad u` and
`(u'·grad')u' = ((u-V)·grad)u`; their sum is exactly
`partial_t u + (u·grad)u`. Also `grad' u'=grad u` and
`Delta' u'=Delta u`, so the transformed fields solve the same equation with
the same constant `nu`, while the measured velocity magnitude changes with
the observer. The symmetric rate-of-strain tensor
`D=(grad u + grad u^T)/2` is unchanged by this boost.

Thus a threshold based only on absolute `|u|` is frame-dependent. If “speed”
means speed relative to a wall, or is shorthand for local shear rate, it can be
physically meaningful, but the wall/gap or strain-rate measure, material,
temperature, pressure, and constitutive law must then be specified. Particular
non-Newtonian fluids can shear-thin; that behavior is an additional material
model and is not implied by the constant-`nu` Navier–Stokes singularity
construction. In nonequilibrium molecular-dynamics simulations of squalane
under elastohydrodynamic-lubrication conditions, molecular alignment saturates
after viscosity has fallen by roughly a factor of three, while a thermally
activated Eyring-type mechanism accounts for much larger viscosity reductions
in the reported high-viscosity regime. This material- and regime-specific
result is evidence against treating alignment as a universal cause of a sharp
viscosity collapse, not a claim that alignment never contributes in other
materials. See Jadhao and Robbins, [*Rheological properties of liquids under
conditions of elastohydrodynamic lubrication*](https://arxiv.org/abs/1903.03996).
Reproduce the boost identities with
`python -m tools.check_galilean_viscosity_invariance`; the exact symbolic
results and assumptions are saved in
`evidence/tests/galilean-viscosity-invariance.json`.

The selected-construction axis calculation has a related exact distinction:
for its linearized volume-preserving propagator, an isotropic Gaussian's
orientation concentrates toward the axis while its probability in any fixed
ball around the center tends to zero as `Q^C`. Its covariance determinant and
Gaussian differential entropy stay constant. See
[`openai-core-material-trajectory.md`](openai-core-material-trajectory.md#exact-positional-probability-check-in-the-linearized-gaussian-model)
for the calculation and its nonlinear-scope limit.

Reproduce the exact algebra with `python -m tools.check_affine_alignment_counterexample`.
The checker also runs wrong-pressure-sign and nonzero-Laplacian negative
controls and writes `evidence/tests/affine-alignment-counterexample.json`.
It is a SymPy check, not an independently formalized proof.
