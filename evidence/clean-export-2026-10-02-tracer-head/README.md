# Tracked-only clean export at the tracer-analysis head

Commit `84a3cc6e4bffad458466441201e3b45bcdd77fc6` was exported from tracked Git data into a new directory and a fresh virtual environment using the locked verification requirements. On macOS 26.6.2 arm64 with Python 3.14.5, all 37 published-report replay steps and six additional checks exited 0. The checker found 178 tracked report/test-evidence files and no byte changes. The full suite in that same exported source reported 200 passed, 1 skipped, and 5 subtests passed.

`result.json` records the commit, source archive hash, environment, sanitized commands, package versions, exit codes, and log hashes. Logs replace the workstation checkout path with `<REPO>`; their hashes are computed over the published copies.

Reproduce from the repository root with:

```sh
python3 -m tools.check_clean_export \
  --revision 84a3cc6e4bffad458466441201e3b45bcdd77fc6 \
  --locked \
  --destination work/clean-export-reproduction
cd work/clean-export-reproduction/source
../venv/bin/python -m pytest -q tests
```

This validates tracked Python postprocessing and archived-evidence audits on the recorded host. It does not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, certify continuous extrema, or change any scientific acceptance verdict.
