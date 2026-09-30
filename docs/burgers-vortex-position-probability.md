# Exact tracer-position probability in the Burgers vortex

This calculation asks whether transverse localization means that particle
positions become fully determinate. It uses the exact Burgers-vortex flow map
and an explicitly imposed initial distribution of passive tracers. It is not a
molecular model, does not include Brownian motion, inertia or interactions, and
does not transfer to the pinned OpenAI construction.

For a tracer starting at cylindrical coordinates `(r0, theta0, z0)`, the exact
position flow is

```
r(t) = r0 exp(-gamma t),
z(t) = z0 exp(2 gamma t),
theta(t) = theta0 + integral_0^t u_theta(r0 exp(-gamma s)) /
                                  (r0 exp(-gamma s)) ds.
```

The angle increment depends on radius but does not alter the radius. The
physical volume Jacobian is one: the coordinate Jacobian in `(r,theta,z)` is
`exp(gamma t)`, while the cylindrical volume factor `r(t)/r0` is
`exp(-gamma t)`. Thus an initially centered, isotropic Gaussian position
ensemble with variance `sigma^2` in each Cartesian coordinate remains an
anisotropic Gaussian with density

```
rho_t(r,z) = (2 pi sigma^2)^(-3/2)
             exp(-(exp(2 gamma t) r^2 + exp(-4 gamma t) z^2)/(2 sigma^2)),
```

and covariance `diag(sigma^2 exp(-2 gamma t), sigma^2 exp(-2 gamma t),
sigma^2 exp(4 gamma t))`. Its covariance determinant, differential entropy,
and peak density are unchanged. Transverse distances contract; axial spread
grows.

For a fixed radius `R>0`, the probability of being inside the **infinite**
axis tube is

```
P(r(t) <= R) = 1 - exp(-R^2 exp(2 gamma t)/(2 sigma^2)) -> 1.
```

For a cylinder that also has a fixed finite half-length `L>0`, independence of
the Gaussian axial coordinate gives

```
P(r(t) <= R and |z(t)| <= L)
  = (1 - exp(-R^2 exp(2 gamma t)/(2 sigma^2)))
    erf(L exp(-2 gamma t)/(sqrt(2) sigma))
  ~ sqrt(2/pi) (L/sigma) exp(-2 gamma t) -> 0.
```

So probability relative to the axis can approach one while probability in a
fixed bounded three-dimensional observation region approaches zero. This is
not universal positional certainty; the answer depends on the observation
geometry. The calculation illustrates anisotropic deterministic advection of
an imposed tracer ensemble, not molecular alignment or a constitutive change
in viscosity.

The velocity profile is the classical exact Burgers vortex; a published
Journal of Fluid Mechanics article states this profile and its axial strain
and viscosity parameters [explicitly](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/dancing-fibres-in-a-microscale-burgerslike-vortex/8F92E5502602BE02BCE4515B0DBF3D58).

Reproduce the flow-Jacobian, density, covariance and probability limits with
`python -m tools.check_burgers_vortex_tracer_probability`. The SymPy 1.14.0
results are saved in `evidence/tests/burgers-vortex-tracer-probability.json`.
