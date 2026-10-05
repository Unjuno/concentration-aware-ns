# Tracked-only clean export after archive-backed temporal replay fix

The tracked-only export of pre-fix commit `46691344f203f504f18f04829531e9be1dfc7646`
failed at replay step 8 (`openfoam_temporal_triplet`): the comparator read an
ignored `work/of13-high-gradient-v2` directory despite the frozen case tarballs
being present in the public tree. The failed run is retained under `pre-fix/`.

Commit `e5f4aab6c6411266c6300abe6c79023a77e4411e` fixes this by extracting the
three SHA-256-checked public case archives into fresh temporary directories,
checking completion and source-log hashes, and deriving the matrix verdict
from the joined and base manifests. Regression tests reject wrong case roots,
absolute paths, and traversal entries.

The post-fix tracked-only export passed on macOS 26.6.2 arm64 with Python
3.14.5. It installed the locked verification dependencies into a fresh venv,
completed all 36 report-replay steps plus the six additional checks, and found
no changed files among 170 tracked report and `evidence/tests` files. The full
suite reported 187 passed, 1 skipped, and 5 subtests passed. Exact commands,
package versions, hashes, and exit codes are in `result.json`; the individual
step logs are in `report-replay/`.

For the public copy, absolute workstation and temporary-directory prefixes in
logs and command records are replaced with `<REPO>`, `<USER_HOME>`, `<TMP>`, or
`<PRIVATE_TMP>`. Per-log hashes in the published records were recomputed over
these sanitized copies; archive and source-code hashes remain the run's
original SHA-256 values.

Reproduce from the repository root with a new destination:

```sh
python3 -m tools.check_clean_export \
  --revision e5f4aab6c6411266c6300abe6c79023a77e4411e \
  --locked \
  --destination work/clean-export-reproduction
```

This verifies tracked Python postprocessing and archived algebra only. It does
not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, certify a
continuous CFD error, or change a scientific solver verdict.
