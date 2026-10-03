# Impact-scope map and falsification plan — 2026-10-03

This report maps what the current evidence does and does not reach. It is a
working impact inventory, not an exhaustive survey of every application or a
claim that the pinned Navier–Stokes construction is a physical flow.

## Evidence-to-impact map

| Area | Current evidence | Supported conclusion | Missing bridge / next falsifier |
|---|---|---|---|
| CFD verification and acceptance | OpenFOAM Foundation 13's frozen six-case uniform matrix has standard acceptance PASS in all six cases; its n=16 and n=32 cases fail the separately frozen sampled-local gate. The finer n=64/n=128 and temporal rows pass that local gate. | On this benchmark, a standard gate can pass while a preregistered sampled local-quality gate fails at coarse resolutions. This is an evaluation/under-resolution result, not a solver defect or singularity. | Complete independent replay and immutable release bundle; test whether local metrics add value across additional smooth concentration widths and adverse post-processing controls. See `reports/solver-matrix-coverage-2026-09-30.md`. |
| OpenFOAM AMR | Four same-run first-refinement events match parent-cell injection; the exact nested cell-average decomposition shows a resolution-dependent subcell-variation contribution. AMR quality attribution remains UNCERTAIN. | The archived value transfer is characterized for those events; no violated upstream contract is established. | Validate field semantics, time/flux effects, and a preregistered AMR local-error bound. The Mantis tracker was not exhaustively searchable. See `reports/openfoam-amr-nested-cell-average-error-2026-10-03.md`. |
| OpenFOAM two-phase viscosity jumps | Pinned source links the common-linear explicit correction to covariance `w(1-w) Δa [Sf & ΔG]`. A compatibility lemma makes the interface contracted jump zero for shared differentiable velocity traces and one-sided incompressibility. A compatible Couette FV resistance control has arithmetic flux error decreasing on 16/32/64 grids and exact harmonic resistance. | Independent tensor norm-growth controls are restricted by velocity compatibility. In the compatible shear case, the numerical coefficient effect enters the implicit diffusion term. The subsequent frozen Foundation 13 package operator probe reproduces the scalar arithmetic-chain error and harmonic equilibrium on 16/32/64 grids; it does not execute the full VoF model or existing Issue #2. | Package scalar probe is recorded in `reports/openfoam-interface-package-operator-2026-10-03.md`; harmonic uses an equilibrium start with zero PCG iterations. Full interface/pressure/phase coupling and disturbed-start controls remain separate. See `reports/incompressible-interface-stress-compatibility-2026-10-03.md`, the source-linked operator report and upstream [issue #2](https://github.com/OpenFOAM/OpenFOAM-13/issues/2). |
| OpenFOAM native scalar residual API | Fixed Foundation 13 package with constant-one field gives native residual 0.25 / 0.125 / 0.0625 while complete b-Au and physical flux are zero on 16/32/64 grids;25 source / 3 linked-library payloads verified, archive replay agrees. | The extra cyclic-source diagnostic prediction is reproduced. The mechanism has 2024 prior discussion; inspected normal solver/convergence statistics use separate paths. | Maintainer API intent, official-tracker status and external diagnostic-consumer use remain unresolved. No14/dev runtime or universal simulation failure is claimed. See `reports/openfoam-interface-package-operator-2026-10-03.md`. |
| SU2 | The audited v8.5.0 source-time behavior has an existing discussion and scoped follow-up; the MMS solver matrix has unresolved residual/accuracy concerns, with no complete all-gates PASS. | Time-source and convergence-protocol observations are already reported; they do not yet establish the proposed concentration blind spot as an independent SU2 defect. | Resolve inner-iteration effects and repeat the common smooth-concentration suite with source-time, temporal-order, and local-QoI controls. See `reports/su2-bdf2-source-time.md` and the existing [discussion #2890](https://github.com/su2code/SU2/discussions/2890). |
| Scientific ML / PhysicsNeMo | On the shifted grid, 19/25 archived models pass the frozen sampled comparison and six miss velocity L2; sampled gradient, vorticity and normalized-divergence limits pass for all 25. Continuous extrema and a PhysicsNeMo-specific preregistered acceptance threshold are absent. | The experiment does not show a sampled global-pass/local-fail blind spot; sampled checks do not certify continuous-field quality or training convergence. | Pre-register PhysicsNeMo-specific tolerances; add continuous/adaptive independent point search and held-out concentration regions; report seed and optimization variability. Existing odd-width spectrum issue #2007/PR #2008 is separate. |
| Pinned OpenAI mathematical construction | Source commit, licenses, proof closure and several extensions have been audited. A pressure-moment condition needed for the selected profile's strict viscous-force conclusion remains unproved; no theorem failure or counterexample is found. | Some consequences are conditional; the selected-field threshold is not yet established. This is neither a solver finding nor a refutation of the upstream theorem. | Prove or disprove the threshold for the actual selected profile, and independently audit any new proof kernel claims. See `reports/actual-profile-pressure-provenance-2026-10-01.md`. |
| Continuum material orientation | A prescribed rigid Jeffery director on the sphere has a conditional subcritical pole-limit argument with decaying rotational diffusion; the algebra is checked, while endpoint nonattainment and elliptic smoothing are analytical inputs. | An ideal orientation variable can align under the specified model. It does not locate molecules or prove finite-particle alignment in the audited flow. | Supply a measured/derived molecular rotational-diffusion law, particle-scale strain-uniformity bounds, translation-orientation coupling, and an observable-level experiment. See `docs/full-sphere-rotational-diffusion.md`. |
| Viscosity and phase transition | Exact affine and Burgers-vortex counterchecks show that directional alignment alone does not remove viscous terms from the continuum momentum balance. | Alignment by itself does not entail a constitutive-viscosity collapse, phase transition, or loss of viscosity. | Any such claim needs an independently specified constitutive model and validated material measurements; no inference from CFD pointwise gradients is sufficient. See `docs/affine-alignment-viscosity-counterexample.md` and `docs/burgers-vortex-alignment-viscous-balance.md`. |
| Engineering control / industrial equipment | No named controller or deployed plant is linked to the pinned mathematical construction or these benchmark cases. | There is no evidence here of a reachable operational hazard. | Identify an actual implementation, validated input envelope, actuator bandwidth, sensing resolution, and safety case before assessing applicability. |
| Light-as-fluid hypothesis | A related field already exists: experiments map paraxial propagation in nonlinear optical media to an effective two-dimensional Gross–Pitaevskii/nonlinear-Schrödinger fluid, with interactions mediated by the material response. | This makes “fluid of light” a real, useful neighboring research direction, but not evidence that free-space photons obey this repository's incompressible Navier–Stokes model. The effective optical fluid is governed by a different wave equation, dimensional mapping, interaction mechanism, and observables; it does not transfer the director-SDE result or imply molecular-position certainty. | If pursuing this branch, define the optical medium and its constitutive response, derive the paraxial/envelope equation and hydrodynamic variables, and compare predictions with optical measurements. Keep it as a separate model extension until that bridge is derived. See the primary experiment and review references below. |

## Adversarial review checklist

For each claimed local-acceptance blind spot, require all of the following:

1. Independently derive the manufactured forcing and verify divergence,
   periodicity, initial/boundary data, and every derivative used by the gate.
2. Freeze source commit, runtime image, mesh, timestep, stopping criteria,
   thresholds, and metric implementation before interpreting results.
3. Separate nonlinear/linear solver residuals, temporal and spatial error,
   derivative-reconstruction error, sampling error, and reference error.
4. Search for missed extrema with an independent method and report the sampled
   and certified quantities separately.
5. Attack the gate with sign, time-label, mesh-index, interpolation, stale-log,
   missing-artifact, and AMR-budget controls; ensure incomplete runs cannot pass.
6. Compare the standard gate and local gate per run. A benchmark PASS is not a
   product safety certification; an observed discrepancy is not proof of
   mathematical blow-up.

The current repository has controls for several items, but not every item is
closed for every backend or for continuous extrema. The relevant evidence and
remaining gaps are tracked in the linked reports and `docs/completion-audit.md`.

## Publication boundary

The repository and its commits are public, but this report is not an upstream
defect report or a claim of legal defensive-publication effect. Upstream posts
remain limited to reproducible, source-pinned findings with a duplicate check;
the current OpenFOAM AMR attribution and cross-solver physical extrapolations do
not meet that bar. The useful public deliverable is the reproducible protocol,
inputs, raw evidence, independent replayers, and explicit PASS/FAIL/UNCERTAIN
verdicts. Preserve immutable commit/archive hashes and state what has not been
verified. The repository remains the single canonical project location.

## Current next actions

1. Resolve AMR field/reconstruction semantics and freeze a prospective local
   quality gate on new inputs, including transfer, flux and post-step controls.
   Current archived AMR diagnostics remain exploratory. Hosted Python CI at
   `9e6e880` passed; that does not close these scientific requirements.
2. Finish requirement-by-requirement replay of each solver matrix and confirm
   the release archive from a clean export.
3. Recheck upstream default branches, issue trackers and contribution channels
   immediately before any further post. Do not create a duplicate issue for an
   existing SU2 discussion, PhysicsNeMo issue/PR, or an OpenFOAM observation
   that remains only UNCERTAIN.
4. Keep molecular, rheological, and industrial-control claims separate until
   their missing models and evidence exist; treat optical fluids as a distinct
   paraxial/NLSE model that needs its own benchmark and coupling derivation.

## Photon-fluid scope references

- D. Michel et al., [“Superfluid motion and drag-force cancellation in a fluid of light”](https://www.nature.com/articles/s41467-018-04534-9), *Nature Communications* 9, 2108 (2018): experiment in a bulk nonlinear photorefractive crystal; the paraxial field is modeled by a 2D Gross–Pitaevskii-type equation and its nonlinear optical response mediates effective photon interactions.
- Q. Glorieux et al., [“Paraxial fluids of light”](https://arxiv.org/abs/2504.06262) (arXiv:2504.06262, first posted 2025): surveys the NLSE-to-2D+1-GPE mapping and optical platforms. This is useful scope context, not a new result of the present benchmark.
- I. Carusotto and C. Ciuti, [“Quantum fluids of light”](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.85.299), *Reviews of Modern Physics* 85, 299 (2013): review of effective interacting photon-fluid platforms, including nonlinear media and microcavities.

## Analytical comparison: optical fluid versus viscous Navier–Stokes

A standard photon-fluid mapping starts from an envelope equation of
Gross–Pitaevskii/NLSE type, schematically

$$
i\hbar\,\partial_t\psi=
\left[-\frac{\hbar^2}{2m}\nabla^2+V+g|\psi|^2\right]\psi.
$$

Writing `psi=sqrt(rho) exp(i phi)` and defining
`v=(hbar/m) grad(phi)` gives, away from zeros of `psi`,

$$
\partial_t\rho+\nabla\!\cdot(\rho v)=0,
$$

$$
\partial_t v+(v\!\cdot\nabla)v
=-\frac{1}{m}\nabla(V+g\rho)
+\frac{\hbar^2}{2m^2}\nabla\!\left(\frac{\nabla^2\sqrt{\rho}}{\sqrt{\rho}}\right).
$$

This is a compressible, potential-flow hydrodynamic form with an interaction
pressure and a quantum-pressure term. It is not the incompressible viscous
Navier–Stokes equation: there is no Newtonian `nu*Delta(v)` term in this
conservative model. Absorption or a driven cavity adds model-specific source
and loss terms, which still need derivation before calling them viscosity.
For paraxial optics, the propagation coordinate plays the effective evolution
variable and the transverse plane supplies the spatial coordinates; the
mapping is not automatically a three-dimensional material flow. Thus the
published light-fluid field makes the user's analogy scientifically
interesting, but does not validate the proposed molecular-position or
viscosity-collapse inference. The NLSE/GPE mapping and hydrodynamic variables
are described in the [2025 review](https://arxiv.org/abs/2504.06262); an
experimental nonlinear-crystal platform is reported by Michel et al.
([2018](https://www.nature.com/articles/s41467-018-04534-9)).
