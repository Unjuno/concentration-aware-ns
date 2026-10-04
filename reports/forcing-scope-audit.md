# Forcing assumptions and the scope of the benchmark

This audit separates three mathematical objects that must not be interchanged:
the manufactured benchmark, the pinned OpenAI construction, and hypotheses in
post-announcement regularity and density papers. It does not prove those papers.

## What the implemented reference actually supplies

For fixed sigma>0 and nu>0, tools/reference.py defines

    psi(x,t) = exp(-t + sum_i(cos(x_i-pi)-1)/sigma^2),
    u = grad(psi) cross (1,2,3),   p = 0,
    f = -u + (u dot grad)u - nu Delta u.

These are analytic functions of real space and time: exp, cos and sin are
analytic, and the formulas involve finite sums, products and derivatives with
fixed nonzero sigma. Periodicity gives bounded spatial derivatives of every
fixed order on the torus over every compact time interval. In particular f has
a finite uniform spatial C2 bound over the finite benchmark run. This is an
analytic argument about the formula, not a certified floating-point bound for
computed solver fields. As sigma tends to zero, these bounds need not remain
uniform; each current run uses a fixed positive sigma.

This reference has an explicit smooth solution and no finite-time concentration
singularity. The measured discrepancies test numerical approximation and
postprocessing of that solution. They cannot establish breakdown of the PDE.
The reference is not claimed to meet the shrinking-core axisymmetry and angular
mean hypotheses of the later regularity theorem, so that theorem is not being
used as its regularity certificate.

## Comparison with follow-up results

| Object | What is fixed or varied | Supported use here | Unsupported inference |
|---|---|---|---|
| Manufactured benchmark | Fixed analytic forcing, initial data and positive sigma for each case; numerical resolution varies | Isolate solver and derivative-observation errors against the known solution | Numerical error implies a singular exact solution |
| Pinned OpenAI witness | A specially constructed smooth force and flow; formal target checked at the recorded commit | Analyze that construction under explicitly tracked hypotheses | Every smooth or analytic force has the same behavior |
| Constantin–Ignatova–Vicol, Theorem 1.1 | Analytic forcing, uniform spatial C2 bound, anisotropic angular-mean bounds and exact core symmetry | Identify which additional assumptions exclude this mechanism | Analytic forcing alone proves general 3D global regularity |
| Cao–Chi–Nie force-density result, arXiv v4 | The smooth force varies; the density theorem takes the OpenAI compact forced blowup as an input and proves approximation thresholds in specified Sobolev topologies | Keep forcing realization/spectrum and per-grid input identity auditable; distinguish the topology of forcing perturbations from solution-discretization error | A likelihood of blowup, particle-position probability law, molecular alignment, or failure of a solver under one fixed force |
| Duraiswami similarity comparison | A reduced core/boundary-value formulation | Compare derivative operators and radial/axial viscous powers | Establish molecular alignment, phase transition or the full construction's realizability |

Primary sources: [regularity paper, v1](https://arxiv.org/html/2609.20803v1),
[density paper, v4](https://arxiv.org/abs/2609.10262v4),
[similarity study, v1](https://arxiv.org/html/2609.17642v1).
The claims and version changes found during the refresh are recorded in
research-refresh-2026-09-26.md and the
[2026-09-28 source and formalization refresh](../docs/openai-refresh-2026-09-28.md).
Full local proof replay of these papers remains open.

## Consequences for the work plan

Keep current measured accuracy reports attached to their fixed forcing and pins.
Add no blow-up warning to a solver merely because a nearby force in a weak norm
might admit breakdown. Before using any density result, identify the exact norm,
what varies, and whether the claimed perturbation corresponds to the numerical
error actually measured. Before invoking the regularity result, check all its
symmetry, growth, regularity and forcing assumptions, not just analyticity.

The source-derived pressure threshold for actualProfile remains a separate gap.
Analyticity of our manufactured forcing neither supplies that pressure bound nor
invalidates the smooth-forced construction. The benchmark results and conditional
Lean extension therefore retain their existing verdicts. No new upstream defect
report follows from this comparison alone.

## Weak-topology density versus actuator-scale forcing — 2026-10-05

The full text of Cao–Chi–Nie v4 adds a useful quantitative caveat to the force-
density statement above. Their rescaled seed is

    F_epsilon(x,t) = epsilon^(-3) F((x-x0)/epsilon,
                                     (t-t_epsilon)/epsilon^2),

with a cutoff correction `H_epsilon` whose pointwise amplitude is
`O(epsilon^(-2))`. Since the seed force `F` is nonzero, their Remark 3.13 gives

    ||g_epsilon-g||_(L-infinity in space-time)
      >= epsilon^(-3)||F||_infinity - C epsilon^(-2) -> infinity.

At the same time, the scaling estimate for the seed in
`L^1_t dot-H^s_x` is `O(epsilon^(1/2-s))`; it tends to zero for `s<1/2`, the
same threshold as the density theorem. Thus the theorem's “nearby forces” can
be close in its stated weak topology while their peak amplitude diverges; the
paper also notes that this family has no uniform bounds on all derivatives.
This is not a contradiction: the topology deliberately does not control those
stronger observables.

This strengthens the operational boundary: topology-density is not a
probability, robustness under bounded actuator amplitudes, or evidence that a
physical flow follows the construction. A physically relevant reachability
claim would need explicit dimensional bounds on force amplitude, spatial and
temporal bandwidth, energy input, and the material response. This calculation
does not show such a bounded-control realization exists. The preprint starts
from the OpenAI blow-up seed, so the result remains conditional on that input
and is not independent validation of it.

Primary source: Cao, Chi and Nie, [*Density of Forces Producing Navier–Stokes
Blowup*, arXiv:2609.10262v4](https://arxiv.org/html/2609.10262v4), equations
(20), (43), Theorem 4.1 and Remark 3.13. This is a source-level scaling audit;
no new PDE proof, actuator model, or solver run is claimed.
