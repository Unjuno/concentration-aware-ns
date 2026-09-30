# PhysicsNeMo: sampled pointwise derivative-field audit

The existing five fixed-budget PINN runs save 262,144 independent evaluation
points each. Their analytic-autograd derivative reports already contain two
different diagnostics: the relative difference between sampled peak
magnitudes, and the largest pointwise absolute difference between computed
and exact derivative tensors. The audit in
[`../evidence/tests/physicsnemo-local-field-audit-2026-09-30.json`](../evidence/tests/physicsnemo-local-field-audit-2026-09-30.json)
reopened every run archive and verified the checkpoint and evaluation-array
hashes against each derivative report.

Across the five cases, sampled peak-magnitude errors are about 0.91–0.97% for
both gradient and vorticity. The maximum pointwise gradient-field difference,
normalized by the exact sampled gradient peak, is 1.24–1.26%; the analogous
vorticity quantity is 1.20–1.24%. The peak-magnitude metric is therefore
smaller than the worst sampled vector-field discrepancy in these runs. Both
metrics are useful: the former compares peak levels, while the latter can
detect spatial/component mismatch that a peak-only summary hides.

These are finite-sample observations on the saved evaluation set, not
continuous extrema, confidence bounds, or certified relative errors at each
point. In particular, the denominator is one fixed exact sampled peak, not
the exact local magnitude at each point. The acceptance verdict remains
`UNCERTAIN`: the v1 protocol did not preregister PhysicsNeMo-specific
thresholds, the 5% comparator was borrowed from OpenFOAM, and the PINN does
not enforce incompressibility exactly. No solver defect or molecular/physical
conclusion follows.

Reproduce with:

```sh
work/reference-check-env/bin/python -m tools.audit_physicsnemo_local_fields
```

## Global Hessian-cover feasibility audit

The continuous-gradient-peak gap can be addressed in principle with a global
Lipschitz cover: bound the spatial Hessian of the derivative-error field, then
inflate the maximum on a regular grid by the largest within-cell variation. I
implemented that route for the exact frozen PhysicsNeMo architecture and saved
per-run rational bounds in
[`../evidence/tests/physicsnemo-global-hessian-coverage.json`](../evidence/tests/physicsnemo-global-hessian-coverage.json).

For each stored binary64 weight, the checker converts its exact value to a
`Fraction` and propagates componentwise first- and second-derivative bounds
through the three tanh layers and linear output. It uses only
`|tanh'|<=1` and `|tanh''|<=1`; the time multiplier at the endpoint is exactly
`1/20`. For the analytic reference, with `beta=1/sigma^2=4`, each third
derivative of `exp(beta*(cos(y)-1))` is at most
`beta+3 beta^2+beta^3=116`, so every component of `D^2 u_ref` is bounded by
`5*116=580` after the cross product with `(1,2,3)`. Hence the derivative-error
Hessian entry bound is the sum of those two bounds. Tests also compare the MLP
bound to autograd Hessians at eight deterministic points per saved checkpoint;
this is only a sanity check, not the proof of the global envelope.

If every component of `D^2(u_pred-u_ref)` is bounded by `B`, nearest-node
distance on an `N^3` periodic grid gives
`sup ||D(u_pred-u_ref)||_F <= max_grid ||D(u_pred-u_ref)||_F + 9*pi*B/N`.
Using `pi<22/7` and the exact peak
`4*sqrt(28)*exp(-1/20) > 4*(26/5)*(19/20) > 19`, plus an illustrative 5%
comparison tolerance, the variation term alone requires
30,821–37,878 points on each axis across the 25 saved runs: about
`2.93e13–5.43e13` regular-grid evaluations even if the derivative error at
every grid node were zero. The observed eight-point Hessians are at most
`0.0123%` of their respective global network envelopes, confirming that this
global bound is extremely loose for these models.

This is a negative result about the efficiency of this particular *global*
certificate, not about model accuracy. Five percent is borrowed from the
OpenFOAM comparator and is not a preregistered PhysicsNeMo threshold; no prior
verdict changes. The audit neither certifies continuous extrema nor implies
that adaptive interval subdivision is infeasible. The next useful attempt is
a local interval/branch-and-bound calculation around the peak candidates, with
outward-rounded arithmetic and a documented stopping criterion. Reproduce the
exact-rational envelope with
`work/physicsnemo-env/bin/python -m tools.audit_physicsnemo_global_hessian_bound`;
the pure propagation unit tests run in the reference environment.
