# Current tracked-only export at `5cb3d65`

Commit `5cb3d65c2b4c065df1cc21ed4ec68dde3b603d7b` was exported from Git tracked data into a new directory on macOS 26.6.2 arm64 with Python 3.14.5. Locked dependencies installed successfully. All 37 report-replay steps and six additional checks exited zero, with all 189 compared report/test-evidence files unchanged. The suite from the fresh exported source reported 201 passed, 1 skipped, and 5 subtests passed; a separate direct run in the same fresh environment also passed.

Tracked source archive SHA-256: `d5e985a110af96e9d3df5db5a4bcacefdf352410e2e8c44c536030e63c390c78`. Runner SHA-256: `babbc80755fa90c6eaee9e4289c8ee3b12ac663f11f427ce96652dc184edbf99`. Commands, package versions, raw/published log hashes, and full-suite summary are in `result.json`. The archive and environment remain under ignored `work/`; this folder contains the sanitized record and logs.

Reproduce from the repository root:

```sh
python3 -m tools.check_clean_export \
  --revision 5cb3d65c2b4c065df1cc21ed4ec68dde3b603d7b \
  --locked \
  --destination work/clean-export-reproduction
cd work/clean-export-reproduction/source
../venv/bin/python -m pytest -q tests
```

This validates tracked postprocessing and archived-data replay on the recorded host. It does not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, certify continuous extrema, or change scientific verdicts.
