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

Reproduce the exact algebra with `python -m tools.check_affine_alignment_counterexample`.
The checker also runs wrong-pressure-sign and nonzero-Laplacian negative
controls and writes `evidence/tests/affine-alignment-counterexample.json`.
It is a SymPy check, not an independently formalized proof.
