# Impact-scope map and falsification plan — 2026-10-03

This report maps what the current evidence does and does not reach. It is a
working impact inventory, not an exhaustive survey of every application or a
claim that the pinned Navier–Stokes construction is a physical flow.

## Evidence-to-impact map

| Area | Current evidence | Supported conclusion | Missing bridge / next falsifier |
|---|---|---|---|
| CFD verification and acceptance | OpenFOAM Foundation 13's frozen six-case uniform matrix has standard acceptance PASS in all six cases; its n=16 and n=32 cases fail the separately frozen sampled-local gate. The finer n=64/n=128 and temporal rows pass that local gate. | On this benchmark, a standard gate can pass while a preregistered sampled local-quality gate fails at coarse resolutions. This is an evaluation/under-resolution result, not a solver defect or singularity. | Complete independent replay and immutable release bundle; test whether local metrics add value across additional smooth concentration widths and adverse post-processing controls. See `reports/solver-matrix-coverage-2026-09-30.md`. |
| OpenFOAM AMR | Four same-run first-refinement events match parent-cell injection; the exact nested cell-average decomposition shows a resolution-dependent subcell-variation contribution. AMR quality attribution remains UNCERTAIN. | The archived value transfer is characterized for those events; no violated upstream contract is established. | Validate field semantics, time/flux effects, and a preregistered AMR local-error bound. The Mantis tracker was not exhaustively searchable. See `reports/openfoam-amr-nested-cell-average-error-2026-10-03.md`. |
| SU2 | The audited v8.5.0 source-time behavior has an existing discussion and scoped follow-up; the MMS solver matrix has unresolved residual/accuracy concerns, with no complete all-gates PASS. | Time-source and convergence-protocol observations are already reported; they do not yet establish the proposed concentration blind spot as an independent SU2 defect. | Resolve inner-iteration effects and repeat the common smooth-concentration suite with source-time, temporal-order, and local-QoI controls. See `reports/su2-bdf2-source-time.md` and the existing [discussion #2890](https://github.com/su2code/SU2/discussions/2890). |
| Scientific ML / PhysicsNeMo | On the shifted grid, 19/25 archived models pass the frozen sampled comparison and six miss velocity L2; sampled gradient, vorticity and normalized-divergence limits pass for all 25. Continuous extrema and a PhysicsNeMo-specific preregistered acceptance threshold are absent. | The experiment does not show a sampled global-pass/local-fail blind spot; sampled checks do not certify continuous-field quality or training convergence. | Pre-register PhysicsNeMo-specific tolerances; add continuous/adaptive independent point search and held-out concentration regions; report seed and optimization variability. Existing odd-width spectrum issue #2007/PR #2008 is separate. |
| Pinned OpenAI mathematical construction | Source commit, licenses, proof closure and several extensions have been audited. A pressure-moment condition needed for the selected profile's strict viscous-force conclusion remains unproved; no theorem failure or counterexample is found. | Some consequences are conditional; the selected-field threshold is not yet established. This is neither a solver finding nor a refutation of the upstream theorem. | Prove or disprove the threshold for the actual selected profile, and independently audit any new proof kernel claims. See `reports/actual-profile-pressure-provenance-2026-10-01.md`. |
| Continuum material orientation | A prescribed rigid Jeffery director on the sphere has a conditional subcritical pole-limit argument with decaying rotational diffusion; the algebra is checked, while endpoint nonattainment and elliptic smoothing are analytical inputs. | An ideal orientation variable can align under the specified model. It does not locate molecules or prove finite-particle alignment in the audited flow. | Supply a measured/derived molecular rotational-diffusion law, particle-scale strain-uniformity bounds, translation-orientation coupling, and an observable-level experiment. See `docs/full-sphere-rotational-diffusion.md`. |
| Viscosity and phase transition | Exact affine and Burgers-vortex counterchecks show that directional alignment alone does not remove viscous terms from the continuum momentum balance. | Alignment by itself does not entail a constitutive-viscosity collapse, phase transition, or loss of viscosity. | Any such claim needs an independently specified constitutive model and validated material measurements; no inference from CFD pointwise gradients is sufficient. See `docs/affine-alignment-viscosity-counterexample.md` and `docs/burgers-vortex-alignment-viscous-balance.md`. |
| Engineering control / industrial equipment | No named controller or deployed plant is linked to the pinned mathematical construction or these benchmark cases. | There is no evidence here of a reachable operational hazard. | Identify an actual implementation, validated input envelope, actuator bandwidth, sensing resolution, and safety case before assessing applicability. |
| Light-as-fluid hypothesis | No electromagnetic, kinetic-photon, or radiative-transfer model is present in this repository's Navier–Stokes evidence. | The fluid analogy is currently a separate untested hypothesis. It cannot inherit the director-SDE or incompressible-flow conclusions. | State a precise Maxwell/kinetic constitutive model, observables, boundary conditions, and a falsifiable comparison before adding it to the benchmark scope. |

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

1. Resolve the queued hosted workflow or record why it remains unavailable;
   the local test run is not a substitute for hosted CI.
2. Finish requirement-by-requirement replay of each solver matrix and confirm
   the release archive from a clean export.
3. Recheck upstream default branches, issue trackers and contribution channels
   immediately before any further post. Do not create a duplicate issue for an
   existing SU2 discussion, PhysicsNeMo issue/PR, or an OpenFOAM observation
   that remains only UNCERTAIN.
4. Keep the molecular, rheological, industrial-control, and light hypotheses
   separate until their missing models and evidence exist.
