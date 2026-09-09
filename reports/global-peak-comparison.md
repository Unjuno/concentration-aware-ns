# Diagnostic peaks versus analytic global reference maxima

Reproduce with `python3 -m tools.compare_global_peaks`. Inputs and hashes are in
evidence/tests/global-peak-comparison.json; the analytic derivation is in
docs/reference-global-peaks.md. The formulas are evaluated in ordinary floating
point. These are diagnostic comparisons, not interval-certified gate outcomes.

OpenFOAM sampled FD2 gradient peak discrepancies are 41.14%, 13.12%, and 3.45%
at n16, n32, n64 with dt=.001. The completed SU2 n16 discrepancy is 37.45%.
The original one-sided underestimation values remain valid; the new derivation
identifies their reference values as exact global maxima.

PhysicsNeMo's sampled autograd gradient peaks differ from the global reference
peak by approximately 0.004%–0.065% across the five cases. This is a different
quantity from the roughly 0.9%–1.0% discrepancies against the reference sampled
on the same shifted evaluation lattice. A close maximum value does not prove
correct peak location, field values, incompressibility or residual convergence.
Nor does a finite set of network samples bound its continuous maximum. The
small numbers therefore do not upgrade the existing UNCERTAIN gate verdicts.

The two comparisons answer different questions and are both retained:

- Same-lattice reference peaks compare diagnostic sampling at matched locations.
- Global reference peaks compare the reported diagnostic maximum with the known
  maximum over the full spatial domain.

Neither is the supremum of the pointwise difference between the two fields.
