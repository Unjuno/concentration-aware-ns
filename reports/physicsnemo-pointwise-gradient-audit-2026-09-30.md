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
