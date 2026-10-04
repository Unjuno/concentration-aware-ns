# Research refresh: kinetic bridge and vorticity amplification — 2026-10-04

## Search scope

Queried the official arXiv Atom API at 2026-10-04 05:54 UTC for
`all:"Navier-Stokes"` submitted from 2026-09-27 through 2026-10-04. The
response contained 32 records. The raw response, exact query URL and SHA-256
are preserved in `evidence/upstream-refresh/arxiv-ns-window-2026-10-04.xml`
and its adjacent manifest. This bounded title/abstract search cannot establish
that no relevant paper exists outside the index query or date window.

## A useful continuum-to-kinetic bridge

Liu and Xu, arXiv:2609.33622v1, define an exact split of a kinetic distribution
`f=W+P`: `W` is the equilibrium contribution along a finite kinetic horizon,
and `P` is its exact complement. The combined conservation equations and
particle equation remain equivalent to the kinetic equation at every horizon.
The dimensionless horizon/relaxation ratio `eta` shifts transport between the
components; near equilibrium the paper derives an explicit residual particle
transport fraction `(1+eta) exp(-eta)`. Its full-Boltzmann companion,
arXiv:2609.35894v1, extends the construction beyond relaxation models. The
first framework also writes out radiative-transfer and neutron-transport
versions; those are transport-with-source models, not a Navier–Stokes fluid of
vacuum photons.

This is a mathematically legitimate route for asking when a continuum
closure ceases to capture kinetic detail: specify the collision model,
relaxation time, spatial/temporal horizon, and the distribution observables,
then compare `W+P` against its macroscopic moments. It makes “particle
position” a distribution or sampling question with an explicit stochastic or
kinetic model. It does not say that a diverging continuum gradient aligns
molecules, makes their positions deterministic, or changes their material's
viscosity. The transport remainder is an evolving part of `f`; it is not a
constitutive viscosity switch. Both papers are v1 preprints, and the reported
flow calculations are not independent replications in this repository.

Dimarco et al., arXiv:2610.00811v1, offer a related but distinct low-Mach
micro–macro relaxation model with a Grad-13 moment closure and an
asymptotic-preserving scheme. The paper states stability and consistency in
the incompressible Navier–Stokes limit and reports one- and two-dimensional
experiments over Knudsen and Mach regimes. This reinforces a possible future
kinetic-vs-continuum comparison, but its moment closure does not resolve all
molecular positions and does not model the OpenAI construction.

## What changed-gradient turbulence calculations can and cannot test

Chiarini, arXiv:2609.39826v1, studies homogeneous isotropic turbulence using an
explicitly modified Navier–Stokes momentum equation with an added, scale-
dependent force that selectively suppresses vorticity amplification while
retaining vortex tilting. The reported DNS uses an in-house second-order
finite-difference solver, third-order Runge–Kutta stepping, and 512^3/1024^3
grids. The abstract reports weaker small-scale gradients and fewer extreme
events as amplification is suppressed, disappearance of the classical energy
dissipation anomaly, but persistence of multifractal intermittency through
vortex-line reorganization. This is relevant evidence that peak amplification,
energy dissipation, and geometric complexity are separable observables.

It is a preprint's numerical result for a deliberately modified equation and
a turbulent statistical regime. It is not a theorem about smooth-forced
finite-time blowup, a reproduced result from the audited solvers, or evidence
that the Newtonian viscosity coefficient suddenly drops. In its equations the
viscosity parameter is set by Reynolds number; the intervention is an added
forcing in the vorticity dynamics. Its useful benchmark lesson is to report
local-gradient/extreme-value, energy/enstrophy, spectrum, and geometry metrics
separately and to declare the equation being solved.

## Disposition for this repository

These sources sharpen the follow-up map without changing any existing solver
verdict or upstream disposition. Keep the three-target manufactured-solution
benchmark on its current incompressible Navier–Stokes specification. A later
separate kinetic extension could pair a declared Boltzmann/BGK case with its
Navier–Stokes limit and compare distribution moments and kinetic residuals as
`Kn` and horizon vary. Do not retrofit that model into the present CFD gate or
claim it validates the OpenAI profile. No upstream software issue is indicated
by these papers, so none was filed.

Primary sources:

- Liu and Xu, [arXiv:2609.33622v1](https://arxiv.org/abs/2609.33622),
  full text https://arxiv.org/html/2609.33622v1.
- Liu and Xu, [arXiv:2609.35894v1](https://arxiv.org/abs/2609.35894),
  full text https://arxiv.org/html/2609.35894v1.
- Dimarco et al., [arXiv:2610.00811v1](https://arxiv.org/abs/2610.00811),
  full text https://arxiv.org/html/2610.00811v1.
- Chiarini, [arXiv:2609.39826v1](https://arxiv.org/abs/2609.39826),
  full text https://arxiv.org/html/2609.39826v1.
