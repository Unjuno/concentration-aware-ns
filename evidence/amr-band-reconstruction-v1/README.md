# Named AMR band reconstruction evidence

Numerical source: `21754518dbecefc3fed8c19badb97f28756ccb26`.

- `analysis.json`: all twelve states, both sampling grids, derivative Parseval
  checks, peak formula endpoints, discarded P0 mass and Helmholtz diagnostics.
- `validation.json`: exact source/input/artifact identities, commands, environment,
  full suite result and byte-identical selected-export replay.
- `isolate_replay.py`, `isolation.json`, `clean-export-replay.log`: accepted
  Git-directory-free export replay with Python process/network/Git-open guards.
- `initial-incomplete-export.log`: dependency-file omission stopped the first
  launch before analysis; preserved as failed operational evidence.
- `audit.log`, `full-suite.log`: original executed diagnostic and local suite.

Reproduce from the recorded numerical commit with the locked dependencies:

```bash
python -m tools.audit_amr_band_reconstruction --output /new/output/path --source-commit 21754518dbecefc3fed8c19badb97f28756ccb26
```

The output directory must not already exist. For the selected-export check,
use `git archive` with all paths listed in `validation.json`, extract under
`source/`, put `isolate_replay.py` beside it, and execute the recorded command
from `source/`. The archive hash binds the exported file set; no Git access is
needed during numerical replay. Dependency provisioning precedes the guard.

This is a named finite-band reconstruction, with floating analytic bound
formulas and no interval-rounding certificate or original solver quality PASS.
See [report](../../reports/openfoam-amr-band-reconstruction-2026-10-03.md).
