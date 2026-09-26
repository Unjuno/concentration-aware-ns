# Connecting the axis deformation to the nonlinear flow

This note supplies a classical local-flow argument for the selected terminal
axis trajectory. The compact-neighborhood, ODE continuation and error-bound
arguments below are not yet formalized in Lean. Their hypotheses are mapped
to the source statements, rather than assumed from a numerical simulation.

## Source hypotheses and the common interval

Use the assembled velocity u in `actual_candidate_material_trajectory`,
with its B, N0, geometric-threshold hypothesis, schedule a tending to infinity,
and eta in (-1,1) satisfying the actual natural-axis root equation. Write
d=1-eta^2>0, D=1/2-h, and

    X(t) = (0,0,eta*((1-t)/d)^D).

The relevant extension statements are:

| Statement | What it supplies |
|---|---|
| `actual_candidate_terminal_base_germ` | Near each sufficiently late axis point, u equals the same selected base velocity in a spacetime neighborhood |
| `actual_candidate_material_trajectory` | X'=u(t,X(t)) for all sufficiently late t<1 |
| `actual_candidate_axis_jacobian` | The full spatial Jacobian along that axis |
| `actual_root_velocity_axial_hasDerivAt` and the selected-root coefficient identity | Axial rate g=C/(1-t) at the chosen root |
| `selectedAxisOmega_continuousOn` | Continuity of the rotation coefficient omega on t<1 |
| upstream `FinalSlowBase.velocity_smooth` | Smoothness of the selected base on the open spacetime domain t<1 |

All eventual statements use q_core approaching 0 from the right, with
t=1-d*q_core. A finite intersection of these eventual sets contains
0<q_core<epsilon for some epsilon>0. Hence there is a **single** t_star<1
on whose terminal interval (t_star,1) the required trajectory and Jacobian
identities hold. This is a classical extraction of an interval from the
eventual statements, not an effective numerical value of t_star.

To join the separate Jacobian and axial-rate statements, apply the full
spatial derivative to the axial basis vector and then project to the third
coordinate. The chain rule gives the derivative of z -> u_3(t,(0,0,z))
as hz. Uniqueness of that scalar derivative and the root axial-derivative
statement give hz=C/(1-t). The two transverse diagonal entries are therefore
-C/(2*(1-t)); the off-diagonal entries use the same selected-field omega.
This identifies the entire G on the common terminal interval.

At every point of that trajectory the neighborhood-equality statement gives
an open neighborhood where u equals the smooth base velocity. Intersect with
t<1 and take the union: it is an open set O containing the terminal graph,
and u is smooth on O. The added extension lemma
`actual_candidate_axis_contDiffAt` separately checks pointwise spacetime
smoothness of the assembled velocity along the eventual axis. The open-union
argument uses the stronger neighborhood equality already proved, not an
unsupported inference from pointwise derivatives alone.

## Compact tube and nearby trajectories

Fix t_star<t0<T<1. The graph K={(t,X(t)): t0<=t<=T} is compact and lies in O.
Choose rho>0 such that the closed spatial tube

    K_rho = {(t,x): t0<=t<=T, |x-X(t)|<=rho}

is contained in O. Such rho exists by compactness and openness. The tube is
compact. Let L>=0 bound the spatial derivative operator norm of u on it,
and M>=0 bound the operator norm of its second spatial derivative there.
Smoothness makes both bounds finite. These constants may depend on t0,T.

For an initial displacement h with |h|<rho*exp(-L*(T-t0)), local ODE
existence and uniqueness, followed by continuation in this compact tube,
gives a trajectory Y_h through X(t0)+h until T. To justify continuation,
set e_h=Y_h-X. The spatial segment joining X(t) and Y_h(t) is in the tube
as long as |e_h|<rho, so the derivative bound and Gronwall give

    |e_h(t)| <= exp(L*(t-t0))*|h| < rho.

Thus a first exit from the tube is impossible. The trajectory cannot cease
inside a compact subset of the smooth domain; local existence extends it.
This supplies a neighborhood of initial positions on which the same flow
Phi(t,t0,x) is defined throughout [t0,T].

## Difference quotient and the explicit error bound

Let F be the previously constructed unique solution of F'=G F, F(t0)=I,
where G(t)=D_x u(t,X(t)). Taylor's formula on the spatial segment yields

    e_h' = G e_h + R_h,       |R_h(t)| <= (M/2)*|e_h(t)|^2.

Set z_h=e_h-F*h. Then z_h(t0)=0 and z_h'=G z_h+R_h. With Delta=t-t0,
the inhomogeneous Gronwall bound implies

    |z_h(t)|
      <= (M/2)*|h|^2 * integral[t0,t] exp(L*(t-s)+2*L*(s-t0)) ds
      <= (M/2)*Delta*exp(2*L*Delta)*|h|^2.

The last expression also covers L=0 without division by L. The bound is
uniform on [t0,T]. Dividing by |h| and letting h tend to zero proves

    D_x Phi(t,t0,X(t0)) = F(t),       t0 <= t <= T.

This establishes the identification by difference quotients; it does not
assume the desired differentiability of the flow as an input. Since T<1
was arbitrary, the derivative along the reference trajectory has the
rotation/stretch formula at every later time below 1. The admissible
neighborhood of initial data can shrink with T; no common neighborhood
through the singular endpoint has been proved.

## Scope of the consequence

For the positive coefficient C of the selected root, with
Q=(1-t)/(1-t0), the singular values of this local flow derivative are
Q^(C/2), Q^(C/2), Q^(-C), and its determinant is one. This follows from the
classical identification above and the checked variational algebra. It is
not yet an end-to-end Lean theorem about Phi.

The quadratic remainder supplies a finite-neighborhood result for each
fixed T<1, but rho,L,M have no effective estimates here. It cannot certify
a fixed-size particle packet arbitrarily close to t=1. Neither the source
hypotheses nor this proof use the unresolved PressureData witness premise;
that premise is needed for the separate strict force-ratio sign claim.

No molecular degrees of freedom or constitutive evolution law appears in
this flow. The result concerns continuum material separations. In particular,
the local volume-preserving contraction/extension cannot itself establish
smaller particles, molecular orientation, or decreasing material viscosity.

## Refined estimate using the exact propagator

[The packet-bound note](axis-packet-bound.md) removes the transverse rotation
from the linear amplification factor and derives a nonlinear comparison bound.
Given a valid tube radius rho and Hessian bound M, it supplies an explicit
sufficient initial-displacement radius and error formula using C and t0,T.
It also distinguishes relative error in a contracting direction from error
normalized by the largest singular value. The actual rho and M remain
uncomputed; the refinement does not certify a particular packet yet.
