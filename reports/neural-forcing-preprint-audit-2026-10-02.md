# Audit of the neural-forcing Navier–Stokes preprint (2026-10-02)

## Finding and scope

This is a primary-source scope audit of Beibei Li, *The Neural Forcing for Three-Dimensional Incompressible Navier-Stokes finite time blowup*, arXiv:2609.23934v1 (submitted 2026-09-20). It is not an independent proof verification, a solver reproduction, or evidence for the OpenAI construction. The arXiv record exposes no associated code or data link; this review used the versioned public text and its stated claims.

The useful contribution for this project is a clearly stated sufficient-condition chain. If a smooth continuum solution has a positive integrated decrease of reciprocal maximum vorticity on every required prefix, then the Riccati comparison prevents smooth continuation past a finite comparison time. If that strict continuum certificate persists on a nonempty open set of frozen forcing parameters, and the output law assigns positive mass to every such open set, positive-probability blow-up follows. This is a conditional theorem structure, not a consequence of a large finite-grid vorticity value.

## What the preprint does and does not establish for its examples

The paper itself distinguishes two routes. Its refinement route would transfer a finite-resolution trajectory to the continuum only after rigorous, candidate-specific enclosures control quantities such as endpoint maximum-vorticity error, time reconstruction, production error, and the corrected certificate margin. Section 7.10 explicitly says those concrete error values have not been substituted for the archived Differentiable and PPO-Clip trajectories. The observed finite-resolution coefficients and replay agreement therefore remain diagnostics; the manuscript does not show that either archived example has a positive validated continuum margin.

Its logically separate direct-continuum route is valid conditionally once a continuum loss theorem actually establishes a strict positive reciprocal-vorticity certificate and its robustness. The paper explains this closure implication, but existence of a finite-dimensional neural-loss minimizer is not feasibility of the zero-certificate set. Sections 6.5–6.7 expressly separate those claims, and note that a combined training objective may trade certificate loss against its base loss. I found no candidate-specific proof in the text that the direct route's continuum loss reaches zero on a nonempty open set. Thus the abstract conditional closure is not an unconditional certification of the named trained trajectories.

The preprint also sets a forcing amplitude cap of `10^21` in its chosen units. This is a mathematical admissibility bound in that paper, not a calibrated laboratory forcing, a realizability result, or a bridge to molecular ordering or constitutive viscosity. The forcing is frozen before the probability argument; repeated closed-loop resampling is explicitly outside its theorem.

## Relation to the OpenAI construction and our hypothesis

The neural-forcing manuscript concerns a different periodic forced-flow family and does not verify OpenAI's construction. Its usable conceptual overlap is methodological: identify a candidate numerically, freeze the forcing, and demand a continuum certificate with explicit error control before interpreting apparent concentration as singularity. This supports the benchmark's separation of solver output from continuum conclusions.

Nothing in this preprint supports the proposed inference that diverging continuum velocity makes molecules line up, gives deterministic molecular positions, changes a material's constitutive viscosity, or makes light behave as a fluid. Those questions require separate models and observables. For the cited incompressible smooth flow, the pre-singular Lagrangian flow map remains volume-preserving; that does not make individual finite particles a one-dimensional lattice.

## Disposition

Record this as a conditional analytical framework and an unresolved candidate-specific certification claim. It identifies no bug in OpenFOAM, SU2, or PhysicsNeMo, so no upstream issue or PR is warranted. A useful follow-up would require the authors' exact frozen forcing/checkpoints, reproducible replay inputs, interval-validated continuum error bounds, and a strictly positive margin; until then, finite-resolution plots are not proof evidence. This review does not alter the CFD acceptance gates.

## Sources

- Li, arXiv:2609.23934v1, submitted 2026-09-20: <https://arxiv.org/abs/2609.23934> and <https://arxiv.org/html/2609.23934>
- OpenAI announcement and its continuum-versus-microscopic model distinction: <https://openai.com/index/navier-stokes-solution/>
- Existing benchmark scope audit for the distinct OpenAI witness and analyticity result: [`openai-analytic-forcing-bridge-2026-10-01.md`](openai-analytic-forcing-bridge-2026-10-01.md)

