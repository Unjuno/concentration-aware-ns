# A kinetic scale test for the molecular-alignment hypothesis — 2026-10-04

## Result

A useful falsifiable bridge from a continuum velocity gradient to molecular
kinetics is the dimensionless strain-over-collision rate

`chi = tau_coll * ||S||`,

where `S = (grad u + grad u^T)/2` and `tau_coll` is the molecular collision
time for a specified kinetic model and thermodynamic state. This is a
Chapman–Enskog ordering parameter, not an alignment order parameter. When
`chi << 1`, the near-equilibrium kinetic closure gives Newtonian viscous stress
proportional to `mu S`; as `chi` approaches order one, the first-order
near-equilibrium expansion can no longer be assumed accurate. That transition
is a reason to measure the full distribution or a molecular model, not a
deduction that the viscosity coefficient vanishes or molecules align.

## Derivation and limits

For a monatomic gas, write the local Maxwellian as `M(rho,u,T)` and the smooth-
flow kinetic expansion as `f = M + epsilon f^(1) + O(epsilon^2)`. The cited
wave–particle paper states that the moments of this expansion give
Navier–Stokes stress

`sigma_NS = -mu [grad u + (grad u)^T - (2/3)(div u) I]`.

In incompressible flow, this reduces to `sigma_NS = -2 mu S`. For its BGK
model, `tau_coll = mu/p`, hence

`||sigma_NS||/p = 2 tau_coll ||S||`

up to the chosen matrix norm. Therefore the dimensionless stress predicted by
the continuum constitutive law is small only while the collision-scale
gradient is small. This is an order estimate from the first-order expansion;
it is not a theorem that the full Boltzmann solution becomes singular at
`chi=1`, nor that higher-order corrections have a particular sign.

The paper uses two distinct ratios that must not be merged:

- `epsilon` is the nondimensional Knudsen parameter in the kinetic equation;
- `eta = ell/tau` is the wave–particle decomposition's chosen kinetic-horizon
  divided by relaxation time.

The paper's factor `(1+eta) exp(-eta)` is a near-equilibrium transport share
assigned to its particle component. It is not a measured molecular alignment,
not `chi`, and not the physical Knudsen number. A benchmark or proposed
follow-up that reports only this factor would not establish a particle
reordering transition.

## Discriminating experiment

Keep the present smooth manufactured Navier–Stokes benchmark unchanged. If a
separate kinetic extension is later justified, preregister a smooth flow with
known forcing and vary `chi` by changing strain and collision time
independently. Compare a Boltzmann or validated BGK solution with its
Navier–Stokes moment solution at matched density, mean velocity, temperature,
and boundaries. Save the distribution, stress tensor, heat flux, collision
model, and collision-time calibration. Report at least:

1. the relative non-equilibrium stress and heat-flux residuals against the
   constitutive closure;
2. an explicitly defined molecular-velocity or molecular-orientation
   alignment statistic, with finite-sample uncertainty;
3. spatial number-density and pair-correlation statistics, kept distinct from
   orientation and continuum line-element alignment.

Use independently seeded samples and an exact or verified kinetic reference
where available. If `chi` approaches one, the predeclared question is whether
the Navier–Stokes closure loses accuracy and whether any specified alignment
observable changes. A changed stress magnitude alone cannot distinguish a
changed rate of strain from a changed viscosity coefficient; estimate the
coefficient from an independent constitutive fit over a declared range.
Deterministic particle coordinates would require an additional observation
model and cannot be inferred from a one-particle distribution.

This proposed discriminator is a model-design inference from kinetic scaling,
not a result of the repository's CFD runs. It does not alter the current
three-solver acceptance gates or validate the OpenAI construction. A fixed
Newtonian viscosity in the PDE is a prescribed coefficient; whether an actual
material changes its constitutive response requires material-specific physics
and measurements.

## Source

Liu and Xu, *A wave–particle decomposition framework for multiscale kinetic
transport*, arXiv:2609.33622v1, especially equations (1)–(5), (22)–(30), and
the BGK specialization (31)–(36):
https://arxiv.org/html/2609.33622v1 . The paper is a v1 preprint. The
identification `tau_coll = mu/p` is specifically its BGK example; for another
collision model the transport coefficient and relaxation scale must be
derived from that model rather than assumed.
