# When the fluid-of-light analogy is valid — and what it does not transfer

## Finding

The user's light-as-a-discrete-fluid suggestion has a real and mathematically
precise counterpart, but it denotes several different models. It is useful to
separate free radiation transport, radiation hydrodynamics, and optical photon
fluids in nonlinear media before relating any of them to the OpenAI
incompressible Navier–Stokes construction.

### 1. Free photons: kinetic transport and a moment hierarchy

For free radiation the natural state is a distribution over position and
photon momentum/direction. Its low moments are radiation energy density,
flux, and pressure tensor. The free-transport equations evolve energy and flux,
but they contain the pressure tensor as an additional unknown; a closure or
the underlying transfer equation is needed. This is a legitimate continuum
description of discrete photons, but it is a relativistic radiation-transport
system, not the incompressible material-velocity equation. In particular, the
momentum-direction distribution is not a list of molecular positions.

### 2. Radiation hydrodynamics: viscosity needs a coupling regime

Radiation can contribute viscous stress in an optically thick, scattering
medium. The kinetic derivation starts from a relativistic photon Boltzmann
equation and expands in mean free path; the cited derivation explicitly
requires repeated Thomson scattering and restricts its continuum correction
to scales larger than the radiation mean free path. Here radiation and
massive scatterers are interacting components. This provides an actual
radiation-viscosity mechanism in a declared regime, but it does not identify
the radiation field with a standalone incompressible Newtonian liquid or show
that matter molecules line up.

### 3. Optical photon fluids: an exact NLSE-to-hydrodynamic rewrite

In a paraxial, slowly varying optical field with a specified Kerr or related
nonlinearity, write the complex envelope as `psi=sqrt(rho)*exp(i*phi)`. For
the conservative defocusing convention

```
i psi_z + (1/(2 k)) psi_xx - g |psi|^2 psi = 0,  g > 0,
```

the exact Madelung equations on a region where `rho>0` are

```
rho_z + (rho v)_x = 0,                    v = phi_x/k,
v_z + v v_x = -(g/k) rho_x
             + (1/(2 k^2)) d_x[(sqrt(rho))_xx/sqrt(rho)].
```

The second term is dispersive “quantum pressure”. If it is negligible at the
resolved scales, the remaining equations have the form of a 1-D compressible,
inviscid fluid. They have no Navier–Stokes viscous Laplacian. The optical
nonlinearity is mediated by the material medium; the observable density is
intensity and the effective velocity is phase gradient. In fiber examples,
propagation distance is the evolution variable and retarded time is the fluid
coordinate. This is a powerful optical analogue and testbed, not ordinary
three-dimensional, incompressible material flow.

There is also a direct symmetry obstruction to copying the OpenAI swirl with a
single scalar optical field. Its effective velocity is a phase gradient. For
an axisymmetric, single-valued phase `phi(r,z)`, the angular derivative is
zero, hence `v_theta=(k r)^-1 partial_theta phi=0`. Introducing winding
`m*theta` instead gives `v_theta=m/(k r)`, circulation `2*pi*m/k`, and an
undefined phase on the axis; the ideal vortex therefore requires an intensity
zero there. The OpenAI paper's leading velocity is axisymmetric, has a
nontrivial azimuthal swirl, and is smooth across the axis. A standard scalar
photon-fluid Madelung field cannot directly reproduce that regular swirl while
preserving the same symmetry and positive intensity. Vector or multicomponent
optical models may have different degrees of freedom, but no mapping from one
of those models to the OpenAI profile has been proposed or validated here.

The published photon-superfluid piston experiment gives a concrete caution
for the user's “acceleration/ordering” intuition: steepening is balanced by
diffraction/dispersion, and its shock-like structures are dispersive shock
waves; their transitions are properties of that nonlinear optical equation
and its chosen operating regime. So “light has hydrodynamic variables” is
supported in these settings, while “light is generally a viscous fluid” and
“this makes matter positions deterministic/aligned” do not follow.

## Consequence for the Navier–Stokes hypothesis

An optical-fluid experiment could be a useful *analogue* for controlled wave
steepening, dispersive regularization, and phase/density diagnostics. To use
it as an analogue of the cited incompressible blow-up profile, one would still
need to establish a dimension- and coordinate-consistent mapping of the
governing equations, forcing, boundary conditions, viscosity, and observable
norms. The Kerr NLSE is conservative and dispersive, whereas the target
equation is viscous, 3-D, incompressible, and externally forced. No such map is
established here. The analogy therefore motivates a separate candidate
experiment but cannot validate the OpenAI construction or infer molecular
alignment, particle-position certainty, a constitutive transition, or
viscosity loss.

## Reproducibility

`tools/check_fluid_of_light_bridge.py` symbolically derives the real/imaginary
parts of the one-dimensional NLSE under the amplitude/phase substitution and
checks their equivalence to continuity and the dispersive Euler equation,
zero vorticity for a smooth scalar phase, and the circulation of a point phase
defect. The locked focused test and checker pass. The machine receipt is
`evidence/analytic-checks/fluid-of-light-hydrodynamic-bridge-2026-10-04.json`.
This verifies an equation rewrite only; it does not execute an optical model,
validate its experimental parameters, or test the OpenAI profile.

## Primary sources

- P. D. Larré et al., “The piston Riemann problem in a photon superfluid,”
  *Nature Communications* 13 (2022), DOI
  [10.1038/s41467-022-30734-5](https://www.nature.com/articles/s41467-022-30734-5).
  The paper specifies the defocusing NLSE, its Madelung variables, and observed
  dispersive-shock transitions in an optical fiber.
- P. E. Larré and I. Carusotto, “Propagation of a quantum fluid of light in a
  cavityless nonlinear optical medium,”
  [arXiv:1412.5405](https://arxiv.org/abs/1412.5405). The interaction is
  mediated by the Kerr `chi^(3)` nonlinearity of the optical medium.
- OpenAI, “Finite Time Blowup for Navier–Stokes,” v1, especially Sections 2.3
  and 4.3 for the azimuthal exterior and leading axisymmetric velocity:
  [proof paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf).
- E. R. Coughlin and M. C. Begelman, “The general relativistic equations of
  radiation hydrodynamics in the viscous limit,”
  [arXiv:1410.2892v2](https://arxiv.org/abs/1410.2892v2). The viscous correction
  is derived from photon transport with Thomson scattering in a diffusion
  limit.
- M. Petkova et al., “arepo-rt: radiation hydrodynamics on a moving mesh,”
  *MNRAS* 485 (2019),
  [DOI 10.1093/mnras/stz496](https://academic.oup.com/mnras/article/485/1/117/5303742),
  Eqs. (13)–(17) for the free-radiation energy/flux moment system.
