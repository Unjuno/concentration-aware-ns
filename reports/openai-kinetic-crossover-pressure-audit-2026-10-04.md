# Kinetic crossover scaling and pressure-variable audit — 2026-10-04

## Question

Can the OpenAI continuum core scaling be converted into a molecular
nonequilibrium threshold, and can the incompressible pressure be used to set
that threshold?

## Source-side rate scale

OpenAI's paper uses remaining time `s = 1-t` and gives
`|u_r|/ell_r = O(s^-1)` and `|u_z|/ell_z \u224d s^-1` for its leading core
profile (Section 2.1). Let

```
Gamma_core(s) = max(|u_r|/ell_r, |u_z|/ell_z),
```

with fixed dimensional reference scales restored by a factor `kappa/t_ref`.
The published scaling then gives `Gamma_core \u224d (kappa/t_ref) s^-1`.
This is the paper's characteristic transport/deformation rate. It is not a
newly computed bound on the full symmetric-gradient norm `|S|`; obtaining such
a bound needs a nonzero component of the dimensionless symmetrized profile
gradient and control of possible cancellations.

For a specified kinetic relaxation model define

```
chi(s) = tau_rel(s) Gamma_core(s).
```

If `tau_rel` is bounded below by a positive constant near `s=0`, then `chi`
grows at least like `s^-1` and crosses any fixed order-one comparison level
before the continuum singular time. If `tau_rel(s)=tau_0 s^alpha`, the model
prediction is `chi(s) \u224d (kappa tau_0/t_ref) s^(alpha-1)`: it diverges only for
`alpha<1`, remains order one for `alpha=1`, and tends to zero for `alpha>1`.
The candidate crossover `s_c \u2248 kappa tau_0/t_ref` in the constant-time case
is an order-of-magnitude boundary, not a universal material prediction or a
proof that a kinetic solution loses regularity there. It is quantitatively
useful only if it falls in a time range where the core scaling applies; if it
does not, the kinetic regime may already be present when that asymptotic range
begins.

The associated local spatial Knudsen ratio is a different quantity. If the
mean free path scales as `lambda(s)=lambda_0 s^beta` and
`ell_r(s)=L_0 s^(1/2)`, then

```
Kn_r(s) = lambda(s)/ell_r(s)
        = (lambda_0/L_0) s^(beta-1/2).
```

It diverges for `beta<1/2`, is constant at `beta=1/2`, and vanishes for
`beta>1/2`. For fixed mean free path, `beta=0`, the formal order-one crossing is
`s_Kn=(lambda_0/L_0)^2`. Without the independent values and state dependence
of `tau_rel` and `lambda`, these two crossovers cannot be ordered. Neither
ratio is a molecular-orientation statistic.

## The pressure variables cannot be identified

The cited Liu–Xu v1 BGK example sets its relaxation time to
`tau_rel = mu/p_th`, where `p_th = rho T` belongs to a compressible kinetic
gas model with a Maxwellian temperature and energy equation. The OpenAI theorem
is an incompressible constant-density equation in which pressure enforces the
divergence constraint; it has no kinetic temperature or equation of state.
Therefore substituting the OpenAI pressure field into `mu/p_th` is not
justified. A physical `p_th`, collision kernel, density/temperature path,
mean free path, and any orientation dynamics would have to be specified
separately. In particular, the theorem's fixed kinematic viscosity does not
determine a molecular relaxation time by itself.

Liu–Xu's separate parameter `eta=ell_h/tau_rel` is a kinetic-horizon to
relaxation-time ratio. For BGK, `(1+eta) exp(-eta)` is the near-equilibrium
fraction of a relaxation transport flux assigned to the decomposition's
`P` component; `P` is an exact distribution remainder, not a count of
molecules at known positions or an orientation order parameter. The paper's
exact split `f=W+P` preserves the distribution, but its artificial
wave/particle terminology does not imply spatial alignment.

## What follows, and what does not

The analytic scale comparison provides a useful *conditional warning*: if a
physical material has a nonvanishing collision time while it is driven through
the theorem's shrinking-core rate, a near-equilibrium Navier–Stokes closure
cannot be presumed uniformly valid all the way to `T`. This is consistent with
the need for a kinetic or material-specific description near a scale crossing.
It does not determine the post-crossover evolution, molecule positions,
orientation, density concentration, effective viscosity, or whether an actual
experiment can realize the constructed forcing. The exact incompressible
passive-tracer density invariant in `docs/incompressible-tracer-density-invariant.md`
remains a separate result under its smooth-flow assumptions.

## Reproducibility and limits

`python -m tools.check_kinetic_crossover_scaling` symbolically checks the power
law classifications and dimensional crossover expressions. Its machine record
is `evidence/analytic-checks/kinetic-crossover-scaling-2026-10-04.json`. The
script checks algebra only; it does not verify OpenAI's proof, compute the
profile's symmetric-gradient norm, solve a kinetic equation, choose material
parameters, or validate either cited preprint's numerical examples.

## Primary sources

- OpenAI, *Finite Time Blowup for Navier–Stokes*, v1, Section 2.1, pp. 3–4,
  especially the core/rate scales: <https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf>.
- Liu and Xu, *A wave–particle decomposition framework for multiscale kinetic
  transport*, arXiv:2609.33622v1, Eqs. (1)–(3), (22)–(37), especially the
  BGK relaxation law and the meaning of `eta` and `P`:
  <https://arxiv.org/html/2609.33622v1>.
