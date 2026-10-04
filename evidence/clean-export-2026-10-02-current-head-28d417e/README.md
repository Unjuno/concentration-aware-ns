# Tracked-only clean export at current audit head

Commit `28d417e0ef4e9fccf2876cb0d2cc3c087045c1bf` was exported from tracked Git data into a fresh directory and locked virtual environment on macOS 26.6.2 arm64 with Python 3.14.5. All 37 report-replay steps and six additional checks exited successfully. The report/test-evidence comparison found 182 files and no changes. The full test suite inside report replay reported 200 passed, 1 skipped, and 5 subtests passed.

`result.json` records the archive and runner hashes, dependency versions, check commands, exit codes, and hashes of the sanitized top-level logs. `replay-steps/` contains the per-step output and replay summary. Absolute workstation paths were replaced in published logs.

Reproduce from the repository root:

```sh
python3 -m tools.check_clean_export \
  --revision 28d417e0ef4e9fccf2876cb0d2cc3c087045c1bf \
  --locked \
  --destination work/clean-export-reproduction
```

This verifies tracked Python postprocessing and archived-data audits on the recorded host. It does not rebuild or rerun OpenFOAM or SU2, retrain PhysicsNeMo, execute Lean, certify the unknown continuous finite-volume field, or change any scientific verdict.
