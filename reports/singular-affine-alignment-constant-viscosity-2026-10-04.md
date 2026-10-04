# Exact affine blow-up foil: line alignment does not imply density or rheology — 2026-10-04

## Result

There is an exact, elementary incompressible Navier–Stokes field on
`R^3 x [t0,T)` for every constant `nu > 0`:

```
s = T - t
u(x,y,z,t) = (-x/s, -y/s, 2z/s)
p(x,y,z,t) = -3z^2/s^2.
```

It is smooth for each `t<T`, has `div u = 0`, and has
`Delta u = 0`. Direct differentiation gives
`partial_t u + (u dot grad)u = (0,0,6z/s^2)` and
`grad p = (0,0,-6z/s^2)`, so the forced-equation residual is exactly zero
for any fixed viscosity. Its velocity-gradient operator norm is `2/s` and
diverges as `t` approaches `T`.

The flow map from `t0`, with `Q=(T-t)/(T-t0)`, is
`F(t)=diag(Q,Q,Q^-2)`. Thus `det F=1`: volume is preserved. A material line
with any nonzero axial component has transverse-to-axial ratio multiplied by
`Q^3`, so generic infinitesimal directions align with the z-axis. But an
initial isotropic Gaussian tracer ensemble has covariance
`sigma^2 diag(Q^2,Q^2,Q^-4)`, whose determinant is unchanged. Its peak density
therefore stays exactly constant as its shape contracts transversely and
stretches axially. The velocity alignment calculation supplies no point-mass
concentration. The equation's parameter `nu` also remains fixed; in this
example the Laplacian vanishes, so the viscous term is inactive.

For the Gaussian example specifically,
`rho(t,x,y,z) = rho(0) exp[-(x^2+y^2)/(2 sigma^2 Q^2) - z^2 Q^4/(2 sigma^2)]`;
its peak is `rho(0)` for every `t<T`, even as its level sets become highly
anisotropic.

## What this does and does not establish

This is a compact analytic counterexample to treating “large or singular
velocity gradient,” “alignment of infinitesimal continuum directions,”
“particle-position concentration,” and “material viscosity change” as the
same conclusion. It does **not** refute or verify OpenAI's construction. The
affine field grows linearly in space, has infinite kinetic energy, and does
not decay at infinity, so it is outside the finite-energy decaying-data class
of the Clay problem. A Gaussian tracer ensemble is an added passive-scalar
model, not a molecular distribution. The constant-viscosity statement is a
property of the assumed Newtonian PDE, not a prediction about a real material.

The user's hypothesized local alignment in the OpenAI construction remains a
different statement: the existing analytic work identifies alignment of
infinitesimal continuum separations along a selected axis trajectory, with an
isotropic direction-law result under explicit assumptions. It does not give
molecular orientations, finite-size particle maps uniform to the singular
time, or a constitutive stress law. Those missing bridges still require
separate models and evidence.

## Verification

`tools/check_singular_affine_alignment.py` writes a reproducible SymPy replay
receipt. It checks incompressibility, the full PDE residual, the
variational ODE, determinant, line-ratio factor, covariance and Gaussian peak
density, with a negative control whose viscous Laplacian is nonzero. SymPy
1.14.0 reports `PASS`; the focused test also passes. Receipt:
[`singular-affine-alignment-2026-10-04.json`](../evidence/analytic-checks/singular-affine-alignment-2026-10-04.json).

The public OpenAI announcement describes its result as a smooth-forced
three-dimensional construction; the OpenAI formalization repository's current
`main` was independently checked at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.
This affine example has neither that forcing class nor those initial-data
properties. The OpenAI GitHub repository has issues disabled, so there is no
valid issue channel there. No upstream report is warranted by this analytic
foil, which identifies no software defect.

Sources: [OpenAI announcement](https://openai.com/index/navier-stokes-solution/),
[OpenAI formalization repository](https://github.com/openai/NavierStokesAndEuler).
