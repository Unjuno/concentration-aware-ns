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

## Scientific boundary and next evidence

This strengthens the continuum statement from an infinitesimal direction
formula to a conditional finite-packet angle estimate. It still contains no
molecular positions, probability distribution, interparticle forces, phase
variables, or viscosity evolution. A molecular claim would require a kinetic or
molecular model and a validated matching from that model to these continuum
fields. A fixed-size continuum-packet claim first needs effective `rho(T)` and
`M(T)` bounds, then an independently checked finite-packet calculation. Solver
data cannot substitute for those bounds.

`work/reference-check-env/bin/python -m tools.check_axis_directional_alignment`
checks the exact singular-value ratio, finite-angle expression and the
`C>1` asymptotic. The check is algebraic support for this note; the nonlinear
flow estimate itself remains classical and conditional. Output:
`evidence/tests/axis-directional-alignment.json`.
