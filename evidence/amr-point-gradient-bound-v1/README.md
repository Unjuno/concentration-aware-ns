# Conditional point-interpolation gradient witnesses

Source `3711beb25d67daff4a04104b5ba983e2b4c98d5b`; original CFD source
`3566f89058071910a41bb68010eb258c7bbc3d74`. Four final archived fields at t=0.05
have Arb96 gradient-error chord witnesses on exact binary64-decoded point data.
No exact cell-average interpretation is imposed.

- `analysis.json`: selected point pairs, decoded velocity vectors, exact rational
  interval endpoints, absolute/relative lower bounds and conditions.
- `audit.log`, `test-suite.log`: completed audit and 311-test suite (1 skip,
  83 subtests passed).
- `isolate_replay.py`, `isolation.json`, `replay.log`: Git-directory-free selected
  export replay with Python process/network/Git-open guards; analysis JSON is
  byte-identical to the original.
- `validation.json`: source and evidence hashes, commands, scope.

Dependencies are the same host's locked verification environment. External raw
archives are input data checked against all archive/member hashes. No new CFD
or whole-history replay is claimed. The interpolation condition is not an
established upstream reconstruction contract; original solver gates remain
unchanged. See [report](../../reports/openfoam-amr-point-gradient-bound-2026-10-04.md).
