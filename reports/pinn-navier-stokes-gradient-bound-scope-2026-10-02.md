# PINN Navier–Stokes gradient-bound scope audit

Date: 2026-10-02  
Purpose: verify the theoretical motivation cited in the user-supplied proposal; no solver or model was run for this audit.

## Primary-source finding

De Ryck, Jagtap and Mishra, *Error estimates for physics-informed neural
networks approximating the Navier–Stokes equations*, IMA Journal of Numerical
Analysis 44(1), 83–119 (2024; first published 18 January 2023), analyze PINN
approximations of classical incompressible Navier–Stokes solutions. Their
Theorem 3.4 gives an (L^2)-type stability/error estimate whose Grönwall
factor contains

`exp(T * (2 d^2 ||∇u||_{L∞(D×[0,T])} + 1))`.

Remark 3.5 explicitly observes that a classical solution may still have a very
large `||∇u||∞`, for example for complicated solutions with strong vorticity,
and says the theorem then indicates that the generalization error might be
large. The theorem is conditional and its estimate also depends on residuals,
boundary/interface terms, and regularity/solution assumptions; it is not a
claim that every high-gradient flow defeats a PINN. The paper's Theorem 3.10
states a training-to-error estimate for a classical solution on the torus and
includes regularity and network-dependent constants.

## Relation to this benchmark

This source supports adding local-gradient and vorticity metrics as a
complement to aggregate PINN loss and velocity error. It does not establish
that a small measured training loss is insufficient under the theorem's full
hypotheses, and it does not show that the current PhysicsNeMo configuration
violates a theorem. Our PhysicsNeMo runs are a finite-budget, fixed-architecture
experiment: sampled gradient errors are around 1%, held-out residuals are
reported separately, exact incompressibility is not enforced, and continuous
peak errors are not certified. The measurements remain descriptive; their
5% comparator was borrowed from the OpenFOAM protocol and was not preregistered
for PhysicsNeMo.

This result is methodological motivation, not an upstream defect report,
proof of blow-up, or evidence about molecular ordering or constitutive
viscosity. No upstream report is warranted from this literature audit alone.

## Sources and replay boundary

- Published journal metadata and abstract: [Oxford Academic](https://academic.oup.com/imajna/article/44/1/83/6989836).
- Full author manuscript: [arXiv:2203.09346](https://arxiv.org/abs/2203.09346), especially Theorem 3.4, equation (3.26), Remark 3.5, and Theorem 3.10.
- Structured observation record: `evidence/upstream-refresh/pinn-navier-stokes-gradient-bound-2026-10-02.json`.

The paper was inspected as a primary source; no independent reproduction of its
proof or theorem constants was performed. This note narrows the claim in the
proposal and leaves the overall benchmark goal active.
