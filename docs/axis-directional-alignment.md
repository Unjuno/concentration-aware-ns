# Directional alignment in the selected continuum flow

This note tests one narrow reading of the user's particle-alignment idea. It
derives what the already-audited terminal-axis deformation says about continuum
material separations, and then asks what survives for a finite displacement. It
does not model molecules or a constitutive change.

## Infinitesimal separation

For a selected root trajectory and two times `t0 < t < 1`, put

```
Q = (1-t)/(1-t0),       0 < Q < 1.
```

The local flow derivative has singular values
`Q^(C/2), Q^(C/2), Q^(-C)` and determinant one. The transverse rotation is
orthogonal and does not change lengths in the transverse plane. Write an initial
separation as `h=(h_perp,h_z)`. When `h_z != 0`, its linearized angle to the
axis therefore satisfies

```
tan(theta(t)) = Q^(3*C/2) * |h_perp| / |h_z|.
```

Thus every infinitesimal direction with a nonzero axial component aligns with
the axis as `t` approaches 1. The entire transverse plane `h_z=0` is exceptional:
its linearized direction stays transverse while its length contracts. This is
directional alignment of infinitesimal continuum separations, not alignment of
all particles, increased certainty of absolute particle positions, or molecular
ordering. Volume is preserved; two directions contract while the third expands.

The source-derived exponent enclosure in [axis-stretch-range.md](axis-stretch-range.md)
has `C >= 7999999/2000000 > 1`. Consequently the integral in the finite-packet
comparison below grows without bound as `Q -> 0`.

The squared ratio identity for the actual deformation map is now a theorem in
`verification/AxisForceSign.lean` and passes the pinned Lean runner with only
`propext`, `Classical.choice`, and `Quot.sound`; the accepted run and exact
source hash are in `evidence/lean-verification/axis-force-sign.json`. In
formula form it proves

```
|| (F h)_perp ||^2 / |(F h)_z|^2
  = Q^(3*C) * |h_perp|^2 / |h_z|^2,
```

for `h_z != 0`. Together with the existing positive coefficient enclosure,
this formalizes the infinitesimal directional contraction/extension ratio.
The nonlinear finite-packet comparison below remains classical and conditional.

## What the finite-displacement estimate adds

Fix a compact terminal interval ending at `T<1`. Suppose a smooth tube of radius
`rho` around the reference trajectory has spatial Hessian bound `M`, and set
`k=M/2`, `delta=|h|`, and

```
a(t) = Q^(-C),
I(t) = integral[t0,t] a(s) ds,
beta(t) = k*delta*I(t),
epsilon(t) = k*delta^2*I(t)/(1-beta(t)).
```

The previously derived variation-of-constants bound is
`|Y(t)-X(t)-F(t)h| <= a(t)*epsilon(t)`, provided its comparison denominator
is positive and the trajectories remain in the tube. A sufficient tube
condition is

```
delta < rho / (a(T) + k*rho*I(T)).
```

Because the axial linear component has size `a(t)*|h_z|`, while the transverse
linear component has size `a(t)*Q^(3*C/2)*|h_perp|`, the triangle inequality
gives the conditional finite-packet bound

```
tan(theta_actual(T)) <=
  (Q^(3*C/2)*|h_perp| + epsilon(T)) / (|h_z| - epsilon(T)),
```

when `beta(T)<1`, the tube condition holds, and `epsilon(T)<|h_z|`. This bound
exhibits the missing scale competition: the linear transverse/axial ratio
shrinks, but the nonlinear remainder must shrink relative to the packet's
initial axial component. A packet nearly perpendicular to the axis is harder to
certify than one with a substantial axial component.

For a specified initial direction `theta0` to the unoriented axis, set
`s0=sin(theta0)`, `c0=cos(theta0)`, and choose a target angle
`0<theta_target<pi/2`, with `m=tan(theta_target)`. The finite-packet bound
certifies that target whenever

```
E = (m*c0 - Q^(3*C/2)*s0)/(1+m) > 0,
delta <= E/(k*I(T)*(1+E)),
delta < rho/(Q^(-C)+k*rho*I(T)).
```

The second inequality is omitted when `k*I(T)=0`; then the comparison error is
zero and the linear angle alone decides the target. If `E<=0`, the linearized
direction has not reached the requested target, so this sufficient finite-packet
bound cannot certify it at that time. The displayed radius is the minimum of an
angle-error limit and a tube-exit limit, and can be evaluated once `rho`, `M`,
`T`, and the initial direction are supplied. The exact rearrangements are
checked by the SymPy artifact below.

For `C>1`,

```
I(T) = (1-t0) * (Q^(1-C)-1)/(C-1) -> infinity as Q -> 0.
```

So for any fixed positive certified `k` and fixed `delta`, this sufficient
comparison eventually stops certifying `beta<1` near the endpoint. That is a
limitation of this bound, not proof that a finite packet must lose alignment or
leave the flow. The actual tube radius and Hessian bound have not been extracted
for the selected profile, and the classical finite-flow differentiation and
comparison are not an end-to-end Lean theorem.

If one hypothetically held both `rho>0` and `k>0` fixed while taking `Q` to
zero, the angle-error radius scales as `Q^(C-1)` for a fixed target strictly
above zero, while the tube radius scales as `rho*Q^C`; the tube condition would
be the stricter one. This is only a conditional scaling comparison: no such
uniform `rho` has been proved, and these asymptotics must not be treated as an
actual packet certificate.

For the selected construction's current existential bounds, the spatial tube
has `rho=rho0*Q^(1/2)` and the half-Hessian satisfies `k<=k0*Q^(-40)`.
Combining these with `Cstretch<4` gives a conservative common sufficient power
`delta<=K*Q^43` for each fixed initial direction with nonzero axial component
and fixed positive target angle, once the linear angle margin is positive. The
new specialization and prefactor forms are checked in
`evidence/tests/packet-radius-scaling.json`. The prefactors remain
non-effective, so this does not extend a fixed-size packet to the endpoint or
show that one loses alignment.

## Scientific boundary and next evidence

This strengthens the continuum statement from an infinitesimal direction
formula to a conditional finite-packet angle estimate. It still contains no
molecular positions, probability distribution, interparticle forces, phase
variables, or viscosity evolution. A molecular claim would require a kinetic or
molecular model and a validated matching from that model to these continuum
fields. A fixed-size continuum-packet claim first needs effective `rho(T)` and
`M(T)` bounds, then an independently checked finite-packet calculation. Solver
data cannot substitute for those bounds.

Under an additional isotropic random-direction model, the probability of an
infinitesimal separation lying within a fixed angle of the axis has a closed
form. The derivation also shows why this orientation probability does not mean
the absolute position density concentrates: the map has determinant one. See
[`particle-position-probability.md`](particle-position-probability.md) and its
symbolic artifact. The model remains about infinitesimal continuum directions,
not molecular positions or a finite packet.

`work/reference-check-env/bin/python -m tools.check_axis_directional_alignment`
checks the exact singular-value ratio, finite-angle expression and the
`C>1` asymptotic. The exact linear deformation identity is also Lean-checked;
the nonlinear flow estimate itself remains classical and conditional. Output:
`evidence/tests/axis-directional-alignment.json`.
