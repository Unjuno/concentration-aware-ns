# PhysicsNeMo local interval point probe — 2026-10-01

## Result

An exploratory interval implementation for the spatial Jacobian of the
PhysicsNeMo prediction error was checked against two independent paths: the
repository's analytic manufactured-solution field and PyTorch autograd for a
frozen checkpoint. Four unit tests pass, including a small tanh-network
derivative, two additional reference points, interval-width contraction as the
box shrinks, and restoration of the interval context after rejected input.

For `n64-nt17`, the audit searched the 262,144 saved evaluation coordinates
and selected `(3.079742548222244, 2.9815677777975633,
3.276092089071606)`, the sample with the largest Frobenius norm of the
pointwise gradient error (`0.2509277804721862`). It then independently
re-evaluated that exact point with PyTorch autograd. The largest componentwise
difference between the interval midpoint and the autograd error Jacobian was
`2.1649348980190553e-15`. The widest degenerate point interval was
`1.968028581623586e-59` at 60 decimal digits.

The audit also evaluated symmetric nonzero-width boxes around this candidate.
At half-width `1e-4`, the largest component interval width was `0.00493` and
the Frobenius upper bound assembled from component intervals was `0.25513`,
compared with a sparse-sample maximum of `0.25094`. At half-width `0.01`,
those values grew to `0.47538` and `0.74676`, while the sparse-sample maximum
was `0.25179`. Thus the direct interval extension becomes loose as the box
widens.

For the half-width `0.01` parent box, equal subdivision reduced the maximum
cellwise Frobenius upper bound from `0.74676` (one cell) to `0.49169` (8
cells), `0.36686` (64 cells), and `0.30732` (512 cells). The maximum component
interval width fell from `0.47538` to `0.06186`. Nine autograd samples per
neighborhood scale were checked and all fell inside their computed component
intervals with a `1e-7` floating comparison tolerance. Those sampled checks
are diagnostic, not a proof that the intervals enclose all points or that the
domain is covered. At 512 boxes the local upper bound is still about 22% above
the sparse-sample maximum, before paying for any broader domain cover.

The reproducible machine record is
[`../evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json`](../evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json),
with archive, checkpoint, and evaluation hashes. Run it from the repository
root with the pinned source tree available:

```sh
PYTHONPATH=.:work/physicsnemo-source \
  work/physicsnemo-env/bin/python tools/audit_physicsnemo_interval_probe.py
```

The formula used is `D(u_pred-u_ref)=t D(MLP)+(1-exp(-t))D u0`, since the
frozen ansatz is `u_pred=u0+t*MLP` and the reference is `u_ref=exp(-t)u0`.
The local implementation uses interval arithmetic for trigonometric features,
the three tanh layers, and the analytic reference Jacobian.

## Limits

This validates selected point evaluations and explores finite boxes around one
sampled candidate. It does not create a complete branch-and-bound proof: the
local boxes cover only a small neighborhood, sparse autograd points cannot
validate an interval extension, and the mpmath interval backend has not been
independently validated as a formal proof kernel. No domain-wide cover was
built and the global continuous gradient/vorticity extrema remain unknown. No
acceptance threshold was preregistered for PhysicsNeMo, so the quality verdict
remains `UNCERTAIN`; this probe does not alter any solver finding.
