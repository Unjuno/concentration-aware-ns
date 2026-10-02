# Burgers vortex: alignment with persistent viscous balance

This analytic countercheck strengthens the affine example in
[`affine-alignment-viscosity-counterexample.md`](affine-alignment-viscosity-counterexample.md).
Here the azimuthal viscous term is nonzero and exactly balances azimuthal
advection, while the axis deformation aligns infinitesimal material directions.
The result shows that alignment does not by itself imply a vanishing relative
viscous contribution.

The classical Burgers vortex is an exact steady incompressible Navier–Stokes
solution. Its cylindrical velocity is

```
u_r = -gamma r,
u_theta = Gamma/(2 pi r) [1 - exp(-gamma r^2/(2 nu))],
u_z = 2 gamma z,
```

for `gamma, nu, Gamma > 0`. A current Journal of Fluid Mechanics article
states this solution and its parameters explicitly; see its [Burgers-vortex
definition](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/dancing-fibres-in-a-microscale-burgerslike-vortex/8F92E5502602BE02BCE4515B0DBF3D58).
The pressure gradients that make the radial and axial equations hold are

```
p_r = -gamma^2 r + u_theta^2/r,
p_z = -4 gamma^2 z.
```

These are compatible because the radial expression depends only on `r` and
the axial one only on `z`. The divergence is zero. The radial and axial
accelerations are balanced by these pressure gradients, while the azimuthal
equation reduces to

```
u_r (d_r u_theta + u_theta/r)
  = nu (d_rr u_theta + (d_r u_theta)/r - u_theta/r^2)
  = -Gamma gamma^2 r/(2 pi nu) exp(-gamma r^2/(2 nu)).
```

For every `r>0`, this viscous diffusion is nonzero and equals the azimuthal
advection term exactly. Along inward-moving radii `r(t)=r0 exp(-gamma t)`,
both magnitudes tend to zero as the trajectory approaches the axis, but their
ratio remains one at every finite time. The viscosity parameter `nu` remains
constant; the core scale depends on it. Thus absolute term size and relative
balance are different observables.

At the axis, `u_theta/r -> Omega = Gamma gamma/(4 pi nu)`. The velocity-gradient
matrix there has a transverse block `[-gamma,-Omega; Omega,-gamma]` and axial
rate `2 gamma`. Its flow derivative has transverse scale `exp(-gamma t)`,
axial scale `exp(2 gamma t)`, determinant one, and transverse-to-axial ratio
factor `exp(-3 gamma t)`. Therefore infinitesimal separations with a nonzero
axial component align with the vortex axis while the nonzero viscous and
advective terms remain in exact balance off the axis.

The alignment also holds along an off-axis material trajectory, so it need not
be inferred by juxtaposing different particles. A trajectory starting at
radius `r0>0` has `r(t)=r0 exp(-gamma t)` and azimuthal angle
`theta(t)=theta0+Theta(t,r0)`, where

```
Theta(t,r0) = integral_0^t [u_theta(r0 exp(-gamma s)) /
                              (r0 exp(-gamma s))] ds.
```

Differentiating this flow map gives the radial-to-azimuthal shear coefficient
`S(t)=r0 partial_{r0}Theta`, whose limit is finite:

```
S(infinity) = Gamma/(2 pi gamma r0^2) [1-exp(-gamma r0^2/(2 nu))]
              - Gamma/(4 pi nu).
```

In initial and final orthonormal cylindrical bases, the deformation gradient is

```
F(t) = [[exp(-gamma t), 0, 0],
        [exp(-gamma t) S(t), exp(-gamma t), 0],
        [0, 0, exp(2 gamma t)]].
```

Because `S(t)` is continuous and has a finite limit, it stays bounded on
`t>=0`. For any initial infinitesimal separation with a nonzero axial
component, the ratio of its transverse component to its axial component is
therefore `O(exp(-3 gamma t))` and tends to zero. On that same off-axis
trajectory, `r(t)>0` at every finite time, so the azimuthal viscous and
advective terms are both nonzero and exactly equal throughout the evolution.
Their absolute magnitudes decrease along the trajectory, but the relative
balance does not.

This is an idealized unbounded-domain solution with linear strain at infinity
and infinite total energy. It does not provide a finite-energy periodic test,
a molecular model, a phase-transition mechanism, or evidence about the selected
OpenAI construction. It does, however, directly falsify the proposed universal
bridge from axis alignment to weaker relative viscosity. Any claim about the
selected construction must calculate its own terms and scales.

Reproduce the cylindrical identities and axis linearization with
`python -m tools.check_burgers_vortex_balance`. The SymPy 1.14.0 result,
assumptions, residuals and sign negative controls are saved in
`evidence/tests/burgers-vortex-balance.json`. This symbolic verification
checks the displayed formulas; it is not a formal proof assistant result.
