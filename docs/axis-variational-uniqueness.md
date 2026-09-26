# Uniqueness of the axial variational solution

This is a classical analytic proof with an independent exact-algebra check.
It supplements the Lean-checked construction of a solution in
`verification/AxisForceSign.lean`. The uniqueness argument below has **not**
yet been formalized in Lean. No numerical trajectory is used.

The algebraic inverse itself is now Lean-checked as
`axisDeformation_inverse`, under r != 0 and s != 0, against both source pins.
Each complete extension run reports 124 declarations, with no `sorryAx`.
This establishes the inverse identity, not the entire uniqueness argument.

## Statement and proof

Fix real C and t0 < 1. Let omega be continuous on (-infinity,1), and define

    q(t) = (1-t)/(1-t0) > 0,
    r(t) = q(t)^(C/2), s(t) = q(t)^(-C),
    theta(t) = integral from t0 to t of omega(u) du.

Let R(theta) rotate the first two coordinates by theta and fix the third.
Set F(t)=R(theta(t))*diag(r(t),r(t),s(t)). Then F(t0)=I and

    F' = G F,        G = [ -g/2   -omega   0
                           omega  -g/2   0
                             0      0    g ],    g=C/(1-t).

The preceding derivative and initial-value claims are already checked by
`integratedDeformation_hasDerivAt` and `integratedDeformation_initial`.
The chosen selected-field omega satisfies continuity by
`selectedAxisOmega_continuousOn`.

Both r and s are strictly positive for every t<1. Therefore the inverse is

    J(t) = diag(1/r(t),1/r(t),1/s(t))*R(theta(t))^T.

Direct differentiation, using r'=-gr/2, s'=gs and theta'=omega, gives
J'=-JG. Let y be any differentiable solution of y'=Gy on an interval
I contained in (-infinity,1) that contains t0, with y(t0)=d. Then

    (J y)' = J' y + J y' = -J G y + J G y = 0.

The ordinary mean value theorem applied to each real coordinate on the
segment between t0 and any t in I implies J(t)y(t)=J(t0)d=d. Consequently
**y(t)=F(t)d**, proving uniqueness on I. For closed interval endpoints,
continuity at the endpoints and differentiability on the interior suffice.
Applying the argument to each column gives uniqueness of the matrix
initial-value problem F'=GF, F(t0)=I as well.

No bound on omega over the entire interval t<1, finite limit of theta at 1,
or integrability through t=1 is used. Every segment ending at t<1 is compact
and the integral defining theta exists there. The proof asserts nothing at
the singular endpoint itself. Uniqueness does not require C>0; contraction
and extension below do.

## Exact geometric consequences

Orthogonality of R gives F^T F=diag(r^2,r^2,s^2). Its singular values are
r,r,s because r,s>0. Also det(F)=r^2*s=q^(C-C)=1. For C>0 and t increasing
to 1, transverse lengths shrink and axial lengths grow.

For an initial displacement d with d3 != 0, the angle to the unoriented
axis obeys

    transverse length / axial length
      = q^(3*C/2) * sqrt(d1^2+d2^2) / abs(d3) -> 0.

For d3=0 the displacement remains transverse: there is no general statement
that every vector aligns. This is alignment of infinitesimal separation
directions, not molecular orientation or shrinking individual particles.

An isotropic covariance sigma^2*I propagated by this linear map becomes
sigma^2*diag(r^2,r^2,s^2). Its determinant is sigma^6, while its axial
variance grows when C>0. Directional concentration therefore does not yield
improved certainty of all three position coordinates. This covariance
calculation concerns a linear model, not a finite distribution evolved by
the nonlinear field.

## What is still needed for the actual nonlinear flow

The explicit Jacobian along the selected axis and its eventual transfer to
the assembled field are checked separately in Lean. This note does not
silently identify a solution of a linear equation with a nonlinear flow
derivative. That step needs a common time interval, a neighborhood of the
material trajectory where the velocity has the regularity required for
differentiable dependence on initial data, and the variational equation

    d/dt D_x Phi(t,t0,x0) = D_x u(t,Phi(t,t0,x0))*D_x Phi(t,t0,x0).

Once those facts and the coefficient identity D_x u=G are supplied, the
uniqueness result above identifies D_x Phi with F. A neighborhood may depend
on the chosen terminal time T<1. No uniform neighborhood up to t=1 or bound
on the nonlinear remainder for a fixed finite packet follows from this
argument. These remain outstanding obligations, alongside formalizing
uniqueness itself. The independent pressure-witness gap also remains open.

## Reproduction and limits of the check

From the repository root, in an environment installed from
`requirements-verification.txt`:

```sh
python -m tools.check_axis_deformation
```

`evidence/tests/axis-deformation.json` records eight exact symbolic residuals
and three deliberate sign/rate perturbations that must be rejected. The
checker verifies the inverse, differential and geometric algebra for
arbitrary real g and omega and positive r,s. It does not verify the mean
value theorem, interval hypotheses, the nonlinear flow's regularity, or a
material constitutive law. Those limits prevent an algebra PASS from being
reported as a new Navier–Stokes proof or reduced viscosity.

## Subsequent connection to the nonlinear flow

[The flow-derivative note](axis-flow-derivative.md) now supplies the classical
compact-tube and difference-quotient argument under the actual terminal-axis
hypotheses. It obtains a quadratic finite-displacement remainder on every
fixed interval ending at T<1. The complete connection is not Lean-formalized,
and the neighborhood size and derivative bounds are not effective estimates.
This advances the classical identification obligation above without asserting
uniform control of a fixed packet up to the singular endpoint.
