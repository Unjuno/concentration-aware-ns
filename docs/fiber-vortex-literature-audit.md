# Scope audit: finite fibers in Burgers-like vortices

## Primary-source finding

The 2026 paper [“Dancing fibres in a microscale Burgers-like vortex”](https://doi.org/10.1017/jfm.2026.11342)
studies a finite flexible filament in a prescribed, zero-Reynolds-number
Stokes-flow analogue called a *spiralet*. Its flow is built from regularized
rotlet and stresslet singularities and is designed to resemble a Burgers
vortex in a selected plane. The paper explicitly distinguishes this field
from the exact Navier–Stokes Burgers vortex. The filament is represented by a
Kirchhoff rod with hydrodynamic interactions, and its motion feeds back on
the Stokes flow.

For a centered, symmetric filament, the authors report spinning and
deformation followed by near-vertical alignment, defined by the principal
axis coming within one degree of the vortex axis. Off-center/asymmetric
filaments exhibit a wider range of shapes, including helical buckling. The
alignment time depends on the elastoviscous parameters. This is evidence for
orientation dynamics of a *finite flexible fiber in this model*, not proof of
universal particle alignment.

## Relevance and boundary

This is a useful nearby result for the broad intuition that vortex-driven
flows can orient extended objects. It does not model molecules, an isotropic
passive-tracer cloud, a constitutive change in viscosity, phase transition,
or the OpenAI manufactured Navier–Stokes profile. The fiber has length,
bending stiffness, hydrodynamic interactions, and finite-size feedback;
those ingredients are absent from a material-line/tangent-map calculation.
The authors present a numerical study and propose future experimental
investigation; it is not an experimental confirmation of molecular ordering.

Accordingly, the literature expands the *possible research bridge* from
continuum vortex kinematics to finite fibers, but does not close the microscopic
bridge in this project. A more direct comparison is now available in a separate
rigid-fiber study. Aulnette et al. combine microfluidic measurements, a
Jeffery-equation analysis and bead-model simulations for rigid, neutrally
buoyant fibers in a stationary Burgers-like cross-slot vortex. The reported
fibers have aspect ratios 10–100, diameters about 2–4 micrometres and lengths
40–500 micrometres. Their experiments use a 25 wt% glycerol-water mixture and
base-flow Reynolds numbers 40–80 (the paper's particle-Reynolds estimate spans
0.05–12); the measured strain rate varies about 150 to 115 s^-1 along a half
channel width, and fitted averages are about 100 s^-1 in the experiment and
120 s^-1 in the simulations. The authors report simultaneous precession from
vorticity and orientation alignment from strain. Over their tested range,
Jeffery's theory describes orientation well, with small length-dependent
corrections: longer fibers rotate slightly slower and align slightly faster
than the local Jeffery prediction. Larger fibers also show weaker radial decay
even in simulations without particle inertia. Their bead-model simulations
assume `Re_p << 1`, whereas the experimental estimate spans 0.05–12; the
authors report viscous effects dominate orientation in their tested cases.
That is bounded evidence for those conditions, not proof that inertia is
absent or generally irrelevant. The paper warns that sufficiently long fibers
may sample varying gradients and violate the locally uniform-flow assumption;
it does not identify a universal critical length. The Aulnette et
al. study is an arXiv v2 preprint (15 July / revised 3 August 2026), not an
experiment on the OpenAI field or on molecules.

## Conditional analytical bridge to the continuum tangent map

For an ideal axisymmetric extensional flow with strain tensor
`E=diag(2 gamma,-gamma,-gamma)`, Jeffery's director equation for a prolate
rigid particle is

```
dp/dt = Omega p + kappa (E p - (p . E p) p),
kappa = (AR^2 - 1)/(AR^2 + 1).
```

If `beta` is the angle from the extension axis, axial vorticity contributes
azimuthal precession but not the polar angle. Direct substitution gives
`d beta/dt = -3 kappa gamma sin(beta) cos(beta)`, hence
`tan(beta(t))/tan(beta(t0)) = exp(-3 kappa integral(gamma ds))`.
The OpenAI construction's checked infinitesimal deformation ratio is
`tan(theta(t))/tan(theta(t0)) = Q^(3 C/2)`, where
`Q=(1-t)/(1-t0)`. If, as an additional idealization, a finite Jeffery particle
experienced the spatially uniform axisymmetric strain
`gamma(t)=C/(2(1-t))`, its angle law would be
`tan(beta(t))/tan(beta(t0)) = Q^(3 kappa C/2)`. The slender limit
`kappa -> 1` matches the continuum tangent-map exponent exactly. This is a
mathematical correspondence between two kinematic laws, not a derivation of a
Jeffery model for the constructed flow.

For an imposed isotropic distribution of initial unoriented directors and a
fixed target angle `0 < beta_star < pi/2`, let
`a=Q^(3*kappa*C/2)`. Since `|cos(beta_0)|` is uniform on `[0,1]`, direct
integration gives

```
P(beta(t) <= beta_star) = 1 - a/sqrt(a^2 + tan(beta_star)^2).
```

For every fixed prolate aspect ratio (`kappa>0`) and `C>0`, this tends to one
as `Q -> 0`; the sphere has `kappa=0` and no distinguished director. This
probability comes from the added initial-director law and ideal Jeffery ODE.
It is not a probability law supplied by Navier–Stokes, and does not describe
molecular orientation or absolute particle positions. Thermal rotational
diffusion can change the limit; under the reduced tangent-plane model with
`D_r ~ (1-t)^(-delta)`, the variance threshold is `delta=1`, as recorded in
`docs/rotational-diffusion-alignment-cutoff.md`. These are separate model
assumptions, not a microscopic derivation.

For the aspect ratios 10 and 100 measured in the rigid-fiber study,
`kappa=99/101` and `9999/10001`; the ideal Jeffery alignment rate is therefore
within about 2% of the slender-particle limit. In that regime, aspect ratio
alone changes the local Jeffery rate only modestly. Absolute length can still
matter through finite-size sampling of nonuniform gradients, inertia, Brownian
rotation, flexibility and hydrodynamic interaction. The cited experiment and
model address micron-scale fibers, not molecular degrees of freedom or a
stress-derived change in fluid viscosity.

The measured fiber lengths `L=40–500 micrometres` are not uniformly small
relative to the fitted Burgers-vortex core length. Using the paper's mixture
values `rho=1059 kg/m^3`, `eta=1.79 mPa s` and local strain rates
`gamma=115–150 s^-1` in `r_gamma=sqrt(2 nu/gamma)`, `nu=eta/rho`, gives the
approximate range `r_gamma=150–171 micrometres` and `L/r_gamma=0.23–3.33`.
This ratio is a useful finite-size descriptor, not a predicted transition
threshold. It helps explain why measured orientation can remain close to the
Jeffery law while migration and small orientation-rate corrections depend on
fiber length.

The missing bridge is decisive: Jeffery's equation uses the velocity gradient
across a finite object's neighborhood (and idealizes it as locally uniform),
whereas the OpenAI proof establishes the flow derivative along a trajectory.
Our finite-packet note has only conditional radius/Hessian bounds on each
terminal interval; it has no effective, fixed-size tube through the singular
time. Thus the exact agreement in the `kappa -> 1` formula motivates a future
finite-fiber calculation only after a spatial-uniformity and particle-dynamics
model is supplied. It does not show that finite fibers, molecules, or material
viscosity align/change in the OpenAI construction. No change to solver
acceptance follows from either fiber paper.

## Source details

- Primary source: [Journal of Fluid Mechanics article](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/dancing-fibres-in-a-microscale-burgerslike-vortex/8F92E5502602BE02BCE4515B0DBF3D58)
- DOI: `10.1017/jfm.2026.11342`
- Published 30 March 2026; open access under CC BY.
- Rigid-fiber comparison: [Aulnette et al., arXiv:2607.14298v2](https://arxiv.org/abs/2607.14298v2), *Orientation Dynamics of Rigid Fibers in a Microfluidic Burgers-like Vortex*; submitted 15 July and revised 3 August 2026.
- Exact Jeffery/tangent-map comparison and the derived `L/r_gamma` range are reproduced by `python -m tools.check_jeffery_axisymmetric_bridge`; assumptions and values are archived in `evidence/tests/jeffery-axisymmetric-bridge.json`.
