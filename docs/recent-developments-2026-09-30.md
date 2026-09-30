# Navier–Stokes developments checked on 2026-09-30

## Current primary-source status

The OpenAI repository `openai/NavierStokesAndEuler` still identifies its contents as Lean formalizations of its Navier–Stokes and Euler manuscripts. Its observed `main` commit remains `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` (2026-09-10); the current README states the forced Navier–Stokes results on both `R^3` and the torus, and the unforced Euler result. The OpenAI announcement says it does not intend to claim the Millennium Prize. Clay's 2026-09-11 statement says the problem has “apparently been settled,” but that evaluation and credit assignment are deliberately unhurried. These are separate statuses: publication and formalization are available, while prize adjudication is not complete.

Sources: [OpenAI announcement](https://openai.com/index/navier-stokes-solution/), [OpenAI Lean repository](https://github.com/openai/NavierStokesAndEuler), [Clay statement](https://www.claymath.org/news/navier-stokes-announcement/).

## New explanatory preprint

On 2026-09-28, Zhen Lei and Xiao Ren posted [arXiv:2609.35406](https://arxiv.org/abs/2609.35406), a readable treatment of the profile-construction part of OpenAI's manuscript. Its abstract describes smooth axisymmetric profiles, a divergence-form residual plus a remainder flat to infinite order on fixed similarity sectors, an admissible stress cone, and a new linear model. It explicitly says that the oscillatory-pulse residual-cancellation argument is deferred to a companion Part II. This is a useful explanatory development, not an independent completion or peer review of the whole argument.

## Independent analyses and programmatic-search criteria

Two further September preprints are relevant to how far the blow-up claim can
be interpreted. Cao and Chi's [arXiv:2609.10262](https://arxiv.org/abs/2609.10262)
study smooth forces that generate classical breakdown from rest for a fixed
viscosity and time horizon. They characterize density of such forces in an
inherited time-integrated spatial `H^s` topology, with threshold `s < 1/2` on
the three-dimensional torus. This is a statement about a set of forcing data
for the already constructed forced problem; it is not a probability law on
physical fluids, evidence of generic unforced blow-up, or a model of molecular
alignment.

The [Positive Defect Problem](https://arxiv.org/abs/2609.23868) sets out
necessary conditions and admissibility criteria for a *programmatic search*
for unforced Navier–Stokes blow-up. It links a positive defect target to a
time-averaged lower bound on Littlewood–Paley energy flux and explains why no
finite computation alone certifies the needed Galerkin-uniform statement.
This is a research framework, not a reported unforced blow-up construction.
It gives us a useful negative control for benchmark conclusions: finite-grid
solver behavior, even with a striking local peak, cannot certify continuum
breakdown or identify a physical singularity.

These papers are independent mathematical follow-ups, not peer review of
OpenAI's Lean development and not validation of the CFD runs in this repository.

## What the physical description does and does not support

OpenAI's paper describes the constructed **continuum velocity field** as an axisymmetric vortex: near the core, flow spirals inward and moves axially outward on either side of a dividing layer. The radial scale is `ell_r ~ tau^(1/2)` while the axial scale is `ell_z ~ tau^(1/2-h)`, so `ell_r/ell_z ~ tau^h -> 0`; the core becomes a slender column as the singular time is approached. This gives a real, mathematically specified analogue of axial stretching and increasingly concentrated structure.

The same paper does not say that viscosity simply switches off. For fixed positive viscosity, the angular Reynolds number grows like `tau^(-h)`, while the radial Reynolds number stays `O(1)`. It says radial diffusion and radial/axial transport remain in the leading balance; axial diffusion becomes weaker relative to radial diffusion. Thus any claim of a universal abrupt loss of viscous action would overstate the result.

These are statements about a designed, externally forced continuum solution. They do not establish molecular alignment, predict a real fluid's molecular positions, or imply that blow-up solutions arise in ordinary physical conditions. Incompressibility means `div u = 0`; while the smooth flow map exists before blow-up, its Jacobian determinant is one. The anisotropic vortex shape therefore cannot by itself be read as material volume collapse or molecular ordering. A later Lagrangian analysis supplies one specific observable: the selected axis trajectory and the derivative of the flow map along it. This does not turn the Eulerian core into a material set.

There is a sharper implication for the proposed “particle alignment” reading: the paper defines its shrinking core by **fixed similarity-coordinate bounds** at each time, so this is an Eulerian region, not a fixed set of material parcels. Its volume scales like `tau^(3/2-h)` and tends to zero. Since the velocity is divergence-free, the flow map preserves the volume of each transported material set for every `t<1`; therefore the shrinking core cannot itself be interpreted as the same material particles being compressed into a line. Particles can enter and leave this changing core, and the stated axial outflow explicitly carries incoming fluid away.

For the selected axis trajectory, the audited tangent map has singular values `Q^(C/2), Q^(C/2), Q^(-C)` and determinant one, where `Q=(1-t)/(1-t0)`. An infinitesimal separation with nonzero axial component therefore has its transverse-to-axial ratio reduced by `Q^(3C/2)`. If initial infinitesimal directions are additionally distributed isotropically, the probability of lying within any fixed nonzero angle of the axis tends to one. This is a precise tangent-direction alignment result, not molecular orientation or absolute-position certainty; see [`particle-position-probability.md`](particle-position-probability.md).

The later cusp-ball extension also gives a selected-field equality neighborhood of radius `c*sqrt(1-t)` and an existential full-spacetime Hessian bound `C2*q^(-40)` there. At the September 30 snapshot the spatial restriction was not yet composed with that transfer. The October 1 `SpatialHessianTransfer.lean` now proves the corresponding fixed-time spatial Hessian bound on the same ball, with an axiom audit. The classical packet comparison and constants remain conditional and non-effective; no fixed-size packet alignment through the singular time follows. See [`axis-packet-bound.md`](axis-packet-bound.md) and [`packet-constant-dependencies.md`](packet-constant-dependencies.md).

Source: [OpenAI paper, §2 “Physical description of the blowup”](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).

## Flexible-fiber literature cross-check

A 2026 JFM paper reports alignment and other shape dynamics for finite
flexible fibers in a prescribed zero-Re Stokes-flow “spiralet,” a Burgers-like
analogue rather than the exact Burgers vortex. This gives a relevant
finite-object research lead, while leaving molecular alignment, changing
viscosity, experiments, and transfer to the OpenAI profile unsupported. The
model distinction and implications are recorded in
[`fiber-vortex-literature-audit.md`](fiber-vortex-literature-audit.md).

## Molecular-rheology cross-check

Jadhao and Robbins' nonequilibrium molecular-dynamics study of squalane
under elastohydrodynamic-lubrication conditions reports alignment saturation
after viscosity has fallen by roughly a factor of three; viscosity can then
continue falling substantially with little further alignment. It is a
material- and regime-specific result, not a constitutive law for the OpenAI
flow or evidence that continuum stretching causes molecular alignment. The
original scope assessment is in
[`../reports/recent-developments-and-hypothesis-audit-2026-09-28.md`](../reports/recent-developments-and-hypothesis-audit-2026-09-28.md).

## OpenFOAM temporal-row archive recheck

The temporal addendum records n64 cases at `dt=0.0005` and `dt=0.00025` as
100/100 and 200/200 converged steps, respectively, with standard acceptance
and local quality both passing. This recheck confirmed each archive SHA-256
against its manifest and found the `End` marker in each archived solver log.
These are validated single rows under the frozen protocol, not a proof of
asymptotic time order or a general solver verdict; see
`evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`.

## Audit implications

1. Treat the slender-core and componentwise Reynolds-number scalings as analytical targets for independent derivation and numerical postprocessing, not as molecular-scale conclusions.
2. Test particle trajectories separately from Eulerian norms: seed the Lagrangian ODE at fixed similarity coordinates, report the selected particle families and finite-time trajectory statistics, and check numerical trajectory error independently of the PDE discretization error.
3. Keep solver acceptance and continuum-singularity claims distinct. No computed blow-up or physical hazard follows from large finite-resolution gradients.
4. Keep the profile paper's stated scope distinct from the complete forcing/residual-cancellation construction; track the companion Part II before describing it as an independent end-to-end proof review.

## 2026-10-01: conditional regularity result for analytic forcing

Constantin, Ignatova and Vicol's 2026-09-17 preprint
[arXiv:2609.20803](https://arxiv.org/abs/2609.20803) proves regularity near a
candidate singular point assuming the anisotropic Type-II bounds and exact
axisymmetry in a collapsing core identified in OpenAI's construction, when the
forcing is spatially real analytic. This constrains any construction satisfying
those hypotheses: its force cannot be analytic locally uniformly in time (or
vanish identically near the point) if it remains bounded in `C^2` to the
singular time. It does not contradict a merely `C∞` force, and we have not
verified the hypotheses against OpenAI's actual force. Treat this as a
conditional mathematical check, not a molecular interpretation. Full caveats
are in the [hypothesis audit](../reports/recent-developments-and-hypothesis-audit-2026-09-28.md).
