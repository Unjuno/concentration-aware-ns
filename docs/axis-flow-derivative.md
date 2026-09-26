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
| `actual_root_common_terminal_interval` | One t_star<1 on whose entire terminal interval the material equation, spacetime smoothness, root Jacobian and base-field germ equality all hold |
| `actual_candidate_terminal_base_germ` | Near each sufficiently late axis point, u equals the same selected base velocity in a spacetime neighborhood |
| `actual_candidate_material_trajectory` | X'=u(t,X(t)) for all sufficiently late t<1 |
| `actual_root_axis_jacobian` | The full spatial Jacobian with the root coefficient g=C/(1-t) and selected rotation rate already substituted |
| `actual_root_deformation_hasDerivAt` | The explicit deformation solves the variational equation using that actual assembled-field derivative, eventually on the terminal axis |
| `selectedAxisOmega_continuousOn` | Continuity of the rotation coefficient omega on t<1 |
| upstream `FinalSlowBase.velocity_smooth` | Smoothness of the selected base on the open spacetime domain t<1 |

All eventual statements use q_core approaching 0 from the right, with
t=1-d*q_core. `eventually_scale_to_terminal_interval` now formalizes the
conversion: an interval 0<q_core<epsilon becomes 1-d*epsilon<t<1.
`actual_root_common_terminal_interval` applies it to the conjunction of the
four needed properties. The **single** t_star therefore works simultaneously
for the material equation, spacetime smoothness, identified Jacobian and
spacetime base-field germ throughout (t_star,1). This interval extraction is
Lean-checked; t_star is still existential, with no effective numerical value.

The separate Jacobian and axial-rate statements are now joined in Lean.
`selected_root_axis_jacobian` identifies partialZ(streamFactor) with C/(1-t)
through the ordinary axial derivative and substitutes it into the full matrix.
`actual_root_axis_jacobian` transfers that exact matrix through the spacetime
germ to the assembled field. Thus the diagonal entries and rotation rate in
G are identified in one formal statement, rather than only by the classical
chain-rule argument used in the previous revision.

`actual_root_deformation_hasDerivAt` then combines the matrix identity with
the constructed rotation/stretch derivative, so its right-hand side is
literally the spatial Frechet derivative of the actual assembled velocity
applied to the deformation. That lemma is an eventual-in-q statement. Although the
formula can use any t0<1 as its normalization time, it is an initial-value
solution for the actual field on [t0,T] only when t0 is also in the common
terminal interval. No assertion about an earlier portion of the actual flow
is inferred from eventual equality. The common-interval lemma now supplies
the shared terminal interval for the field identities, so t_star<t0<=T<1
is an explicit admissible initial-time condition for the classical flow
argument below.

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
