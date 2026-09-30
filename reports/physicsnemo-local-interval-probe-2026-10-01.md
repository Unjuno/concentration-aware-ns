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

This validates a point evaluation and the implementation's basic local
behavior. A degenerate interval has no useful width for bounding nearby
coordinates. No nonzero neighbourhood was certified for the trained model, no
branch-and-bound cover was built over the periodic domain, and the global
continuous gradient/vorticity extrema remain unknown. The mpmath interval
backend has not been independently validated as a formal proof kernel. No
acceptance threshold was preregistered for PhysicsNeMo, so the quality verdict
remains `UNCERTAIN`; this point probe does not alter any solver finding.
