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

**Correction, 2026-10-01:** review against the training implementation found
that the first version assigned input derivatives as though features were
interleaved by axis. The actual concatenation is all sine features followed by
all cosine features. The prior bound and its reported grid cost were therefore
not justified and are withdrawn. The corrected checker now rejects a changed
feature expression, uses the source's actual order, and includes a regression
case where the sine/cosine pair for one axis contributes jointly to a diagonal
Hessian entry. In that witness, the historical implementation returned `1/5`
while the corrected implementation returns `7/10`, confirming that the old
mapping could underbound. A second review caught that the earlier use of the
reference-peak lower bound `19` made the allowed tolerance too small for an
optimistic node-count floor. Those intermediate values were conservative for a
stricter threshold, not a lower bound on required nodes. The final record uses
a safe upper bound on the exact peak instead. The audit also confirms that the
training script bytes match frozen harness commit
`7d2723629264febdd6b7188b4e3897b6bd1716a8` before trusting its feature order.

The continuous-gradient-peak gap can be addressed in principle with a global
Lipschitz cover: bound the spatial Hessian of the derivative-error field, then
inflate the maximum on a regular grid by the largest within-cell variation. I
implemented that route for the exact frozen PhysicsNeMo architecture and saved
per-run rational bounds in
[`../evidence/tests/physicsnemo-global-hessian-coverage.json`](../evidence/tests/physicsnemo-global-hessian-coverage.json).

For each stored binary64 weight, the checker converts its exact value to a
`Fraction` and propagates componentwise first- and second-derivative bounds
through the three tanh layers and linear output. The input feature order is
`sin(x), sin(y), sin(z), cos(x), cos(y), cos(z), t/end`, matching the frozen
training code. It uses only
`|tanh'|<=1` and `|tanh''|<=1`; the time multiplier at the endpoint is exactly
`1/20`. Since the prediction is `u0+t*MLP` and the exact solution is
`exp(-t)*u0`, the error Hessian is `t*D2MLP + (1-exp(-t))*D2u0`. For the
analytic reference, with `beta=1/sigma^2=4`, each third
derivative of `exp(beta*(cos(y)-1))` is at most
`beta+3 beta^2+beta^3=116`, so every component of `D^2 u_ref` is bounded by
`5*116=580` after the cross product with `(1,2,3)`. Since
`1-exp(-1/20)<1/20`, the reference contribution to the error-Hessian bound is
at most `29`; the network contribution already includes the endpoint factor
`1/20`. Tests also compare the MLP bound to autograd Hessians at eight
deterministic points per saved checkpoint; this is only a sanity check, not the
proof of the global envelope.

If every component of `D^2(u_pred-u_ref)` is bounded by `B`, nearest-node
distance on an `N^3` periodic grid gives
`sup ||D(u_pred-u_ref)||_F <= max_grid ||D(u_pred-u_ref)||_F + 9*pi*B/N`.
The existing paper-and-pencil global-peak derivation gives the exact reference
gradient peak `4*sqrt(28)*exp(-1/20)` (it is not machine-checked). Since
`sqrt(28)<53/10` and `exp(-1/20)<20/21`, it is less than
`424/21<21`. This **upper** peak bound grants an
illustratively generous 5% tolerance of `21/20`. For a necessary node-count
floor, use `pi>3`, which implies the variation term exceeds `27*B/N`; setting
the sampled-grid error to zero gives `N>27*B/(21/20)` for this envelope. The
result is 9,465–13,743 points per axis across the 25 saved runs, or
`8.48e11–2.60e12` total points. This is a lower floor for this particular
global-Hessian cover, not a lower bound for every possible certificate and not
a completed cover or quality verdict. The observed eight-point Hessians are at most
`0.0168%` of their respective global network envelopes, confirming that this
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
