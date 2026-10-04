# Rotational diffusion under a singular idealized extensional strain

## Question and model boundary

The proposed molecular bridge is not settled by the continuum tangent map.
This note asks a narrower question: in an ideal local model for a prolate
director, does rotational Brownian diffusion prevent alignment when the
extensional strain rate grows like the audited `1/(1-t)` scale?

For a prolate Jeffery director in the axisymmetric strain
`E=diag(2 gamma,-gamma,-gamma)`, the deterministic polar-angle equation is

```
d beta/dt = -3*kappa*gamma(t)*sin(beta)*cos(beta),
kappa = (AR^2-1)/(AR^2+1).
```

Near the extension axis, use tangent-plane coordinates `X=(X1,X2)` with
`|X| approximately beta`. Linearizing the drift gives
`dX/dt = -lambda(t) X`, `lambda=3*kappa*gamma`. Add isotropic rotational
Brownian noise in this tangent plane:

```
dX_i = -alpha/tau * X_i dt + sqrt(2*D_r(t))*dW_i,
tau=1-t, tau0=1-t0, q=tau/tau0,
gamma=C/(2*tau), alpha=3*kappa*C/2.
```

This is a local small-angle stochastic director model, not a derivation of
molecular dynamics from the OpenAI field. It assumes a spatially uniform
axisymmetric strain over the particle, a prolate rigid director, dilute
noninteracting particles, and a prescribed rotational diffusion coefficient.
The tangent-plane approximation is only self-consistent while the angular
variance stays small.

## Exact second-moment calculation

If each tangent component has mean zero and variance `v(t)`, Itô's formula
gives

```
dv/dt = -2*alpha/tau * v + 2*D_r(t).
```

For constant rotational diffusion `D_r`, with `v(t0)=v0`, the exact solution
is

```
v(q) = v0*q^(2*alpha)
     + 2*D_r*tau0/(2*alpha-1) * (q-q^(2*alpha)),   alpha != 1/2;
v(q) = q*(v0 + 2*D_r*tau0*log(1/q)),               alpha = 1/2.
```

When `alpha>1/2` and `D_r>0`, Brownian forcing eventually dominates the
deterministic `q^(2*alpha)` variance and

```
v(q) ~ 2*D_r*tau0/(2*alpha-1) * q,
E[beta^2] ~ 2*v(q),
RMS(beta) ~ sqrt(4*D_r*tau0/(2*alpha-1))*q^(1/2).
```

Thus constant rotational diffusion weakens the deterministic alignment rate
from angular scale `q^alpha` to a noise-limited `q^(1/2)` in this model, but
does not prevent the angular variance from tending to zero as `q -> 0`. For
`0<alpha<1/2`, the deterministic variance power `q^(2*alpha)` remains the
leading term; at `alpha=1/2` it has the logarithmic correction above. If
`alpha=0`, there is no aligning drift and `v(q)=v0+2*D_r*tau0*(1-q)`.

The hypothesis can be made more adversarial by letting diffusion increase
toward the endpoint:

```
D_r(q) = D0*q^(-delta),   D0>0, delta>=0.
```

For `2*alpha+delta != 1`, the exact solution is

```
v(q) = v0*q^(2*alpha)
     + 2*D0*tau0/(2*alpha+delta-1)
         *(q^(1-delta)-q^(2*alpha)).
```

For `2*alpha+delta=1`, the corresponding solution is
`q^(2*alpha)*(v0+2*D0*tau0*log(1/q))`. Consequently, for every `alpha>0`:

- if `delta<1`, both leading powers are positive and `v(q) -> 0`;
- if `delta=1`, `v(q) -> D0*tau0/alpha`, a nonzero residual angular variance;
- if `delta>1`, this tangent-plane variance diverges, which signals that the
  small-angle regime breaks down rather than proving global isotropization.

The same threshold appears in the instantaneous rotational Péclet number:

```
Pe(q)=gamma/D_r ~ C/(2*D0*tau0) * q^(delta-1).
```

Flow dominates asymptotically when diffusion grows slower than `1/tau`
(`delta<1`); the two rates remain comparable at `delta=1`; faster diffusion
outgrows this strain in the linearized model when `delta>1`. For the source
stretch enclosure `C >= 3.9999995` and a prolate rod with `AR=10`,
`alpha=3*kappa*C/2 >= 2375999703/404000000 > 1/2`. That comparison only
selects the asymptotic branch; it does not specify `D_r`, an endpoint cutoff or
a real particle trajectory.

At any fixed physical cutoff `q_c>0`, the formula gives a finite nonzero
variance when `D_r>0`; perfect alignment is an endpoint limit of the ideal
model, not a finite-time measurement. A physical prediction would need the
particle size and aspect ratio, temperature, solvent viscosity, measured
`D_r`, strain history across the particle, interactions, and a defensible
continuum cutoff. If one additionally assumes a Stokes-Einstein relation
`D_r proportional to 1/eta`, then a viscosity law
`eta(q) proportional to q^delta` would enter this model through the same
threshold, but neither that constitutive law nor its coupling to the singular
flow is established here.

## Full-sphere correction when the tangent-plane variance grows

The `delta>1` branch above only says that the linearized tangent-plane
approximation leaves its small-angle regime. It does not identify the global
orientation law. The full-sphere Jeffery--Smoluchowski equation has now been
checked separately: for this prescribed strain and diffusion law, `delta=1`
gives a finite-width stationary density, while `delta>1` gives asymptotic
isotropization rather than divergent angular variance. For `delta<1`, an
asymptotic-pseudotrajectory argument narrows the sample-path limit set to the
equator or one extension pole, but the probability of the unstable-equator
exception remains unresolved. The exact laws and proofs are in
[`full-sphere-rotational-diffusion.md`](full-sphere-rotational-diffusion.md).
This upgrades the `delta>1` model conclusion without supplying a molecular
diffusivity law or a finite-particle transfer from the OpenAI velocity field.

## What the result says about alignment and viscosity

The tangent-plane calculation supplies a local small-angle bridge for
*orientation of idealized anisotropic particles*: under the singular strain
history, constant or subcritical-power rotational diffusion does not by
itself destroy the small-angle endpoint prediction. The full-sphere analysis
now resolves the diffusion-dominated `delta>1` regime and shows loss of
alignment in that imposed model. Together these provide falsifiable model
comparisons; neither establishes which diffusion scaling applies physically.

It still says nothing about absolute particle-center locations. It is not a
molecular theorem, a finite-size result in the spatially varying OpenAI field,
or a prediction at any accessible cutoff. The OpenAI paper describes the fluid
equations as a continuum model and says individual-particle tracking would be
needed beyond that model's singularity; the proof does not supply a molecular
ensemble or rotational-diffusion coefficient.

Alignment also does not determine viscosity. A carrier-fluid constitutive
coefficient can remain fixed while particle orientation changes. A dilute
rod suspension may have orientation-dependent extra stress, but quantifying
that requires concentration and a stress closure. A 2026 experimental and
theoretical study of cellulose nanocrystal rods measured strong flow-induced
birefringence at high Péclet number while reporting a Newtonian-like steady
flow field over its tested strain rates; that is evidence that orientational
order and bulk-flow constitutive response are distinct observables in those
conditions, not evidence about the OpenAI profile.

## Verification and primary references

`work/reference-check-env/bin/python -m tools.check_rotational_diffusion_alignment`
checks the ODE substitutions, branch formulas, diffusion-growth threshold,
and the aspect-ratio example with exact SymPy arithmetic. The result is
`evidence/tests/rotational-diffusion-alignment.json`. This is an exact check of
the stated reduced stochastic model, not a Fokker-Planck or molecular
simulation.

- OpenAI's source description of continuum scope and the singularity boundary:
  [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/).
- Recktenwald et al., *Colloidal rod dynamics under large amplitude
  oscillatory extensional flow*, Soft Matter 22 (2026), 1389–1401,
  [DOI: 10.1039/D5SM01122A](https://doi.org/10.1039/D5SM01122A). Their
  experiments and orientation-distribution simulations use rotational
  diffusion measured for cellulose nanocrystals; steady-flow measurements
  were Newtonian-like in the tested range.
- Calabrese et al., *Effects of Shearing and Extensional Flows on the
  Alignment of Colloidal Rods*, Macromolecules (2021),
  [DOI: 10.1021/acs.macromol.0c02155](https://doi.org/10.1021/acs.macromol.0c02155),
  for the measured flow-versus-rotational-diffusion Péclet comparison in dilute
  colloidal rods.
