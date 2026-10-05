# PhysicsNeMo global gradient cover budget sweep — 2026-10-05

## Result

The adaptive Arb cover was rerun at 16,384 and 32,768 leaves on the same
frozen `n64-nt17` checkpoint and periodic domain used by the 8,192-leaf run.
The fixed candidate-point lower bound is `0.25092778047`; the full-cover upper
bound improved from `7.2739533` (8,192 leaves) to `5.8803816` (16,384) and
`4.5772401` (32,768). The corresponding upper/lower ratios are `28.99`,
`23.43`, and `18.24`. The configured 10% enclosure gap remains unmet.

The 16,384- and 32,768-leaf jobs took about 363 and 770 seconds, respectively,
and evaluated 32,705 and 65,473 intervals. The 32,768-leaf run used 65,470
direct interval evaluations and only 2 quadratic-Taylor evaluations. The
configured width threshold was `0.1`; it was therefore almost never reached.
This is a measurable reduction in the global upper bound, but not a tight
maximum certificate and not evidence of a model defect.

A targeted local preflight explains why simply lowering the Taylor threshold
is not an established global fix. At the candidate center, halfwidth `0.1`
gave direct/Taylor upper bounds `5.8022 / 15.4909`, while halfwidth `0.05`
gave `3.2344 / 1.4313`, halfwidth `0.025` gave `1.8239 / 0.3684`, and
halfwidth `0.0125` gave `1.0120 / 0.2688`. Taylor is tighter on these smaller
boxes, but this local comparison does not show that switching methods will
improve the adaptive full-domain cover within a practical budget.

## Evidence and limits

The exact JSON records are in
`evidence/tests/physicsnemo-global-cover-16384-2026-10-05.json` and
`evidence/tests/physicsnemo-global-cover-32768-2026-10-05.json`. They include
frozen archive/checkpoint hashes, candidate point and lower bound, domain,
method counts, tool hash, runtime, and the explicit result
`CERTIFIED_ENCLOSURE_GAP_REMAINS`. The 8,192-leaf baseline remains preserved
in `evidence/tests/physicsnemo-gradient-global-cover-2026-10-01.json`.

All runs use the same `[-16/5,16/5]^3` cover of the periodic domain and Arb
outward interval operations. The fixed-point lower bound is not asserted to
be the global maximum. Arb has not been independently checked as a formal
proof kernel, and no PhysicsNeMo acceptance threshold was preregistered.
Therefore the PhysicsNeMo quality verdict remains `UNCERTAIN`; this sweep
neither validates nor falsifies the model's claimed accuracy, and it gives no
basis for molecular-scale alignment or material-transition claims.
