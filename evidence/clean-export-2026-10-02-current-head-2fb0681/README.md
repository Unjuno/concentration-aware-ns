# Current tracked-only export at `2fb0681`

Commit `2fb068172a25d980f9eb52b5a519e8666e35fe79` was exported from tracked Git data into a new directory on macOS 26.6.2 arm64 with Python 3.14.5. The locked dependency install succeeded. All 37 report-replay steps and six additional checks exited zero; the checker found 188 report/test-evidence files unchanged. The full test suite then ran from the exported source and fresh environment: 201 passed, 1 skipped, and 5 subtests passed.

The tracked source archive SHA-256 is `a9be53e8ddc5e3e5d469843e59b41f8400ad48764dc3a1f00957f014c4c74df8`; runner SHA-256 is `babbc80755fa90c6eaee9e4289c8ee3b12ac663f11f427ce96652dc184edbf99`. Per-check exit codes, package versions, raw/sanitized log hashes, and the full-suite command are in `result.json`. The 1.7 GB tracked tar and fresh environment remain under ignored `work/`; this folder stores only the sanitized verification record and compact logs.

Reproduce from the repository root:

```sh
python3 -m tools.check_clean_export \
  --revision 2fb068172a25d980f9eb52b5a519e8666e35fe79 \
  --locked \
  --destination work/clean-export-reproduction
cd work/clean-export-reproduction/source
../venv/bin/python -m pytest -q tests
```

This validates tracked postprocessing and archived-data replay on the recorded host. It does not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, certify continuous extrema, or change scientific verdicts.
