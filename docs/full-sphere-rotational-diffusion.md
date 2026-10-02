# Full-sphere check of rotational diffusion near a reciprocal-time strain

## Scope

This is a rigid, prolate Jeffery director in an imposed spatially uniform,
axisymmetric extension. It tests what the earlier tangent-plane stochastic
model can and cannot say when its predicted angular variance leaves the
small-angle regime. It is not a molecular model and does not identify this
imposed flow with the OpenAI construction. Jeffery's deterministic particle
orientation law is the starting point; the orientation-distribution/Fokker-
Planck treatment with rotary Brownian motion has a classical precedent in
Hinch and Leal's spheroid analysis. Neither source validates the transfer to a
singular, spatially varying field.

## Time-changed sphere equation

Let `p` be a unit director on `S^2`, `x=p_z`, aspect-ratio parameter
`kappa=(AR^2-1)/(AR^2+1)>0`, and

```
E(t)=diag(2 gamma(t), -gamma(t), -gamma(t)),
gamma(t)=C/(2 tau),
tau=1-t.
```

Jeffery's equation gives

```
dp/dt = kappa*(E p - (p.E.p)*p)
       = 3*kappa*gamma*(x*e_z - x^2*p).
```

Set `s=log(tau0/tau)`, so `dt/ds=tau`, and prescribe rotational diffusion
`D_r(t)=D0*tau^(-delta)`, with `D0>0`. The probability density relative to
surface area then obeys

```
partial_s rho = -div_S(b*rho) + d(s)*Delta_S rho,
b(p)=a*(x*e_z-x^2*p),
a=3*kappa*C/2,
d(s)=D0*tau0^(1-delta)*exp((delta-1)*s).
```

The symbolic checker verifies this change of clock, the zonal identity
`Delta_S(x^2)=2-6*x^2`, and `div_S b=a*(1-3*x^2)`.

## Critical and diffusion-dominated regimes

At `delta=1`, diffusion in `s` is the positive constant `D0`. The drift is a
surface gradient:

```
b=(a/2)*grad_S(x^2).
```

Consequently the zero-current stationary density is
`rho_inf(p)=Z^(-1)*exp(chi*x^2)`, where `chi=a/(2*D0)`. Since the diffusion is
elliptic on the compact connected sphere, this is the unique invariant
density and the distribution converges to it. It has enhanced probability
near both extension poles, but for finite `chi` it is not a pair of point
masses. For an unoriented director and a two-pole cone of half-angle
`beta_star`, put `c=cos(beta_star)`. The limiting probability is

```
P(|x| >= c) = integral_c^1 exp(chi*x^2) dx / integral_0^1 exp(chi*x^2) dx
            = 1 - erfi(sqrt(chi)*c)/erfi(sqrt(chi)),
```

with its continuous `chi=0` limit `1-c`. Thus the tangent-plane nonzero
residual variance at `delta=1` is qualitatively consistent with a finite-width
orientation law, though its numerical variance need not match the exact
spherical distribution.

For `delta>1`, `d(s)` grows exponentially. Assume a normalized initial density
in `L2(S^2)`; parabolic smoothing gives the regularity needed below for later
times. The sphere Laplacian has a positive spectral gap on mean-zero functions.
If `f=rho-1/(4*pi)` and
`Y=||f||_2^2/2`, integration by parts gives

```
Y' = -d(s)||grad f||_2^2
     - (1/2) integral_S2 (div_S b) f^2 dA
     - (1/(4*pi)) integral_S2 f*(div_S b) dA.
```

The drift divergence is bounded. Poincare's inequality and Young's inequality
therefore yield, for sufficiently large `d(s)`, constants `lambda,K>0` such
that `Y' <= -lambda*d(s)*Y + K/d(s)`. Since `d(s)->infinity`, scalar
comparison gives `Y->0`; hence the density tends to the uniform surface
density in `L2(S^2)`. In this full-sphere model, the limiting two-pole-cone
probability is then `1-c`, the isotropic value.

This refines the earlier tangent-plane statement: its `delta>1` variance
divergence marks failure of the small-angle approximation. It is not physical
infinite orientation variance. Under the specified full-sphere model, the
stronger diffusion instead washes out the alignment and restores isotropy.
The transition at `delta=1` is conditional on the chosen coefficient law; no
temperature-, particle-size- or solvent-based argument here establishes that
real molecular rotational diffusivity has any such singular scaling.

For `delta<1`,

```
integral_0^infinity d(s) ds = D0*tau0^(1-delta)/(1-delta) < infinity,
```

while the imposed strain clock is infinite. In the ambient `R^3` representation
of spherical Brownian motion, the martingale term therefore has finite
quadratic variation and converges almost surely; the Ito correction
`-2*d(s)*p` is absolutely integrable. On every bounded future time window,
the remaining perturbation tends uniformly to zero. Gronwall's inequality
then shows that the sample path is an asymptotic pseudotrajectory of the
deterministic Jeffery ODE.

For that ODE, `x=p_z` satisfies `x'=a*x*(1-x^2)`. The function `V=x^2` has
`V'=2*a*x^2*(1-x^2)`, strictly positive except on the equator and the two
poles. The limit-set theorem for precompact asymptotic pseudotrajectories and
the strict-Lyapunov result imply that the sample-path limit set is either
contained in the equator, or is one of the poles. This narrows the unresolved
case but does not prove almost-sure alignment: the analysis here does not rule
out convergence to the unstable equator. The equator-avoidance theorem must
be checked against the exact continuous-time, decaying-noise hypotheses
before claiming that exception has probability zero. Benaïm's Theorem 9.1
does prove nonconvergence to certain repelling sets for a discrete-time
Robbins–Monro process under gain, regularity, and unstable-direction noise
conditions. Those hypotheses are not a theorem for this continuous-time,
state-dependent sphere SDE, so that result does not close the equator gap.
The ODE/APT framework comes from Benaïm and Hirsch; its limit-set results are
summarized and extended for stochastic processes by Benaïm. Our
square-integrable-noise argument is specific to the present sphere SDE.

## What this does not establish

The model assumes the gradient is spatially uniform over the entire finite
particle, ignores translation-orientation coupling, interactions, flexibility,
inertia, and boundaries, and prescribes `D_r` independently of the flow. A
pointwise continuum derivative along one trajectory supplies none of these
particle-scale assumptions. This result establishes no deterministic particle
positions, molecular ordering, phase transition, constitutive-viscosity
change, or implication for solver acceptance. The exact algebra replay is
`python -m tools.check_spherical_orientation_diffusion`; its output is
`evidence/tests/spherical-orientation-diffusion-2026-10-03.json`.

## Primary sources

- G. B. Jeffery, [“The motion of ellipsoidal particles immersed in a viscous fluid”](https://doi.org/10.1098/rspa.1922.0078), *Proceedings of the Royal Society A* 102 (1922), 161–179.
- E. J. Hinch and L. G. Leal, [“The effect of Brownian motion on the rheological properties of a suspension of non-spherical particles”](https://doi.org/10.1017/S002211207200271X), *Journal of Fluid Mechanics* 52 (1972), 683–712. Their analysis derives orientation distributions for rigid spheroids with rotary Brownian motion in steady shear; it is precedent for the modeling framework, not for the singular-flow limit derived here.
- M. Benaïm and M. W. Hirsch, [“Asymptotic pseudotrajectories and chain recurrent flows, with applications”](https://doi.org/10.1007/BF02218617), *Journal of Dynamics and Differential Equations* 8 (1996), 141–176; M. Benaïm, [“Dynamics of stochastic approximation algorithms”](https://www.numdam.org/item/SPS_1999__33__1_0.pdf), *Séminaire de Probabilités XXXIII* (1999), 1–68. These provide the limit-set/strict-Lyapunov framework; applying them to this nonautonomous spherical SDE uses the finite-quadratic-variation estimate above.
