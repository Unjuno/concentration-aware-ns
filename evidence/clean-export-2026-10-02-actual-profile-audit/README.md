# Tracked-only export and full test replay for the actual-profile audit

Commit `e24c2b6f37a0a4d0573f11686f37f8072b599a1a` was exported from tracked Git data into a fresh directory and locked virtual environment. On macOS 26.6.2 arm64 with Python 3.14.5, the report replay completed all 36 steps and the additional SU2-standard and five axis/alignment checks exited zero. The replay verifier found 176 published report/evidence files and no changed files. The full test suite ran from the exported source: 199 passed, 1 skipped, and 5 subtests passed.

The sanitized `result.json` preserves runner/archive hashes, package versions, commands, exit codes, and hashes of the published logs. Absolute workstation paths were replaced with placeholders; published per-log hashes are computed after sanitization.

Reproduce from the repository root with:

```sh
python3 -m tools.check_clean_export \
  --revision e24c2b6f37a0a4d0573f11686f37f8072b599a1a \
  --locked \
  --destination work/clean-export-reproduction
cd work/clean-export-reproduction/source
../venv/bin/python -m pytest -q tests
```

This verifies tracked Python postprocessing and archived-data audits on the recorded host. It does not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, certify the unknown continuous finite-volume field, or change any scientific acceptance verdict.
