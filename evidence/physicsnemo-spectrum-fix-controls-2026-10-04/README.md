# Current-source spectrum and adversarial fix controls

Numerical source: `fa15e1ebae0dcadd5844200a6a847bc1eaa10d2b`.

The live main function still reproduces existing Issue #2007. Existing PR #2008
passes all six symmetry checks and positive-finite spectrum checks. An invalid
zero-spectrum function is symmetric but must be rejected: the former
`not reproduced` rule accepted it, while the corrected rule exits 1.

`main-reproduction.json`, `pr2008-validation.json` and `zero-spectrum-rejected.json`
record the focused CPU Torch controls. `zero-spectrum-control.py` is an authored
negative control, not upstream code. `live-status.json` records the scoped fresh
upstream inventory. This does not run the complete PhysicsNeMo suite, certify
general radial-spectrum accuracy or change the benchmark's frozen even-grid data.
Old evidence is preserved. See the [report](../../reports/upstream-spectrum-fix-controls-2026-10-04.md).
