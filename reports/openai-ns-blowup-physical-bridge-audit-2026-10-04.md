# OpenAI Navier–Stokes blow-up and physical-bridge audit (2026-10-04)

## Decision

The newly published construction is mathematically about a forced,
three-dimensional incompressible continuum solution. It is not a molecular
simulation and it does not establish that molecules align, that particle
positions become deterministic, or that a real material undergoes a phase
transition or viscosity collapse. Its physical description is inward spiral
and axial stretching of a shrinking vortex core, with velocity and vorticity
growing while the core's total kinetic energy tends to zero.

The September 15, 2026 arXiv preprint by Ramani Duraiswami is a relevant new
physical-bridge investigation. It studies the leading-order similarity profile
and a porous-wall analogue, proposes cavitation/shock observables, and gives
order-of-magnitude arrest estimates. It is a single-author preprint, not a
peer-reviewed experimental validation. It says the full forced finite-viscosity
evolution was not computed, the construction's stress cone is not realized by
the paper's smooth matched profiles, and whether that annulus can be built at
finite scales remains open. Treat its estimates as hypotheses with explicit
model limits.

## What the primary sources establish

OpenAI's paper states a theorem for every positive viscosity: a smooth,
compactly supported external force and zero initial velocity produce a smooth
solution up to finite time with bounded kinetic energy and unbounded
`L-infinity` velocity as the singular time is approached. Its stated geometry
has a shrinking, increasingly slender vortex core, inward spiral, axial flow,
and shear-amplified oscillatory pulses. The proof's velocity field describes a
continuum. Although the OpenAI explanatory page says that a real fluid cannot
move infinitely fast and that a particle-level description would then be
needed, neither that page nor the theorem specifies the microscopic outcome.
That does not imply ordering or certainty of molecule locations.

The Duraiswami preprint's abstract and discussion report these points:

- It solves selected leading-order similarity-profile problems and compares
  them with an exact steady swirl geometry; these are stationary/profile
  calculations, not a time-marching realization of the full forced theorem.
- Its smooth matched core can satisfy selected moment identities, but the
  stress-cone condition fails on those smooth profiles. The paper says the
  OpenAI-style radial oscillation/pulse construction is needed to supply that
  stress, and it does not verify the full finite-scale forced annulus.
- For an illustrative water case (1 m/s swirl at 1 cm), it estimates
  cavitation around a 0.6–0.8 mm core radius, far before molecular scales; for
  air, it estimates compressibility/shock before molecular scales. These are
  leading-order/profile estimates with stated dependence on annulus content,
  not experimental observations or a validated prediction for a specific
  device.
- The paper lists unresolved numerical/formulation items, including an
  unconverged strong-swirl spectrum and the state beyond a fold. Its code and
  tests are linked, but the paper says raw run outputs are available from the
  author on request; this audit has not independently rerun those calculations.

These findings strengthen the need to keep the continuum theorem, discrete
solver behavior, and constitutive/molecular physics as separate questions. A
velocity norm tending to infinity is not a statement that a particle becomes
more locatable. Continuum blow-up means the chosen continuum model loses
regularity; molecular ordering would need a microscopic model and an observable
for orientational order. A viscosity drop would need a specified constitutive
law and independent rheological evidence. Neither follows from the benchmark
errors or from the theorem's divergence.

## Disposition and next checks

This source review supports no defect claim against OpenAI, OpenFOAM, SU2, or
PhysicsNeMo. The OpenFOAM uniform-grid six-case archive replay is independently
reproduced in this repository and found no fine-grid standard-pass/local-quality
blind spot under its frozen thresholds. The five-case SU2 shared-MMS workflow
is still running; its results must be replay-verified before interpretation.
Neither benchmark tests molecular dynamics or non-Newtonian rheology.

Useful next work, if the goal is to test the proposed physical bridge, is to
extract the theorem's explicit similarity scalings, then separately build a
dimensionally consistent cutoff map for compressibility/cavitation and for
molecular Knudsen-scale breakdown. Keep uncertainty in the annulus stress
realizability visible. Only after those checks should one choose an atomistic
or constitutive simulation; such a simulation must be treated as a model to
validate, not as independent truth. Do not report molecular alignment,
particle-location determinism, phase transition, or viscosity collapse unless
the relevant microscopic/constitutive observable is directly calculated or
measured.

## Sources

- OpenAI, [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/), 2026-09-08, and its [proof paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).
- Ramani Duraiswami, [Self-similar swirl between contracting porous walls: the GD1998 exact Navier–Stokes solution revisited in the similarity variables of the OpenAI 2026 forced blow-up construction](https://arxiv.org/abs/2609.17642), arXiv:2609.17642, submitted 2026-09-15. Preprint; computational claims and physical estimates above are attributed to the author, not independently verified here.
