# Material-state model follow-up — 2026-10-05

## Finding

The 1 October preprint by Banerjee, Chakrabortty, Mahato and Raja Sekhar G P,
[The Vanishing-Diffusion Limit of an Incompressible Visco-Morphoelastic System:
Weak Solutions and a Jaumann Defect](https://arxiv.org/abs/2610.01487), is a
useful new mathematical reference for the user's idea of tracking an evolving
material state alongside an incompressible flow. It couples velocity to an
Eulerian effective-strain tensor transported by a Zaremba–Jaumann rate and a
Kelvin–Voigt stress. The constitutive law has fixed viscosity coefficients
`mu_1, mu_2` and elastic coefficients; the internal strain evolves under a
separately prescribed remodeling law.

The paper proves weak existence for its diffusion-regularized model. In the
vanishing-diffusion limit, its scalar trace variable converges strongly, but
the deviatoric Jaumann commutator is a product of only weakly convergent
factors. The authors retain that unresolved limit as a distributional defect
term and give additional strong-convergence conditions that would make the
defect vanish. This is a mathematical compactness result, not a finding that a
real fluid's viscosity changes anomalously.

## Relation to the user's hypothesis

This paper illustrates the extra ingredients needed to connect flow to
material response: a state variable, an objective transport law, a remodeling
law, and a constitutive stress coupling. Even in this explicit model, the
viscosities are parameters rather than functions that switch when particles
align. It contains no molecular positions, particle-orientation statistics,
phase transition, or alignment-triggered viscosity drop. Its weak-limit defect
marks information not identified by the available estimates; it is not
evidence of hidden particle ordering.

The result is also separate from OpenAI's forced Navier–Stokes construction.
It considers a bounded-domain visco-morphoelastic system with its own internal
strain and boundary conditions. It neither verifies nor contradicts the
OpenAI theorem, and it is not a simulation of that theorem's profile.

## Exact pressure-gauge reduction of the constitutive stress

The preprint's incompressible Kelvin–Voigt stress is
`sigma = mu_1 D(v) + lambda E + 2 mu tr(E) I`; its bulk-viscosity term
vanishes because `div(v)=0`. Decompose the symmetric effective strain as
`E = F + (q/3) I`, where `q=tr(E)` and `tr(F)=0`. Direct substitution gives

```
lambda E + 2 mu tr(E) I
  = lambda F + ((lambda + 6 mu)/3) q I.
```

For constant coefficients, the isotropic term contributes only a gradient
`((lambda+6 mu)/3) grad(q)` to momentum. Defining
`p_eff = p - ((lambda+6 mu)/3) q` absorbs that contribution exactly. Since
`div(D(v)) = (1/2) Delta(v)` for an incompressible velocity, the momentum
equation reduces to

```
rho D_t(v) + grad(p_eff)
  = (mu_1/2) Delta(v) + lambda div(F) + f.
```

Thus the trace part of the internal strain has no direct non-pressure force in
this incompressible, constant-coefficient model. The deviatoric internal strain
can add an elastic force, and the trace still enters the *evolution* of the
deviator through the paper's stretching term, so this is not a decoupling of the
full system. The shear-viscosity coefficient `mu_1` remains fixed in the
constitutive equation; this model supplies no viscosity-switch mechanism.
This exact stress decomposition is an algebraic reading of the paper's stated
model, not a new theorem or an empirical claim.

## Source and status check

The arXiv record identifies this as version 1, submitted 2026-10-01. It is a
preprint; this repository has not independently checked its proof. A bounded
arXiv API search for 1–5 October 2026 returned eight records matching
`all:"Navier-Stokes"`; this paper was the closest material-state result. The
search found no result for the exact proposed Part II title, and the distinctive
phrase “Residual Correction via Oscillatory Pulses” returned only Part I,
arXiv:2609.35406v2. These queries do not constitute an exhaustive literature
search.

The official [OpenAI/NavierStokesAndEuler repository](https://github.com/openai/NavierStokesAndEuler)
still reports main at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, last pushed
2026-09-10. Its GitHub metadata has Issues and Discussions disabled, so the
current research does not identify a reportable upstream issue there. PR #4
for this benchmark remains open at `88cb0532d2d493df1eabf182c51904ca2ad8b43d`;
its Python, exact-control and changes checks are successful. Skipped
optional solver jobs remain skipped and are not new validation.

A separate status check found the prior pinned OpenAI Lean-audit workflow
`37233433718` completed as **cancelled**, so it supplies no Lean result. The
five-case SU2 workflow `37230949147` was still **in progress** at its last
update, 2026-10-04 20:25 UTC; neither status changes the literature finding.

The raw arXiv Atom responses and GitHub metadata hashes are preserved in
`evidence/upstream-refresh/openai-ns-arxiv-refresh-2026-10-05.json` and its
adjacent `.atom.xml` files. This refresh changes no CFD verdict, acceptance
threshold, or interpretation of the OpenAI proof.
