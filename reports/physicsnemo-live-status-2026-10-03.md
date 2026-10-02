# PhysicsNeMo live issue and source refresh

Checked 2026-10-03 against GitHub's API. Main remains at
`83d6a337eecfc70e215ed1978af8dba9a38580fb`; the audited
`physicsnemo/metrics/general/power_spectrum.py` blob is still
`fb3e8cda3bc7916b8e56833dda240cb74463fabb`. The known odd-width center-index
problem therefore remains in the source. Existing Issue #2007 is open. Its
focused fix PR #2008 is open with review required. Relative to current main,
GitHub reports the PR branch as diverged: two commits ahead and twelve behind,
with merge base `ff5d19d08123de47ca446caed1d70a225d540184`. No new issue or
contribution is needed from this benchmark; the finding is already reported.

The periodic-boundary gradient concern is also already tracked. Issue #2001
(the `PhysicsInformer`/consumer-facing behavior) remains open. Lower-level
boundary-mode Issue #1852 remains open with a stale label; linked PR #1853 is
still open as a draft. These are existing records for the behavior, so no
additional duplicate was filed. The current benchmark uses periodic operators
for periodic data and even widths for spectra; neither issue changes its
present measurements.

Exact queried states and object IDs are recorded in
`evidence/upstream-refresh/physicsnemo-current-status-2026-10-03T-live.json`.
This is a focused upstream refresh, not an exhaustive repository audit, a new
runtime reproduction, or a full PhysicsNeMo test-suite result.
