# Tracked-only export and full test replay for the upstream refresh

Commit `039ace23a542e82bfc81632d14673d05abea3cec` was exported from tracked
Git data into a fresh directory and locked virtual environment. On macOS
26.6.2 arm64 with Python 3.14.5, the report replay completed all 36 steps and
the additional SU2-standard and five axis/alignment checks exited zero. The
replay verifier found 171 published report/evidence files and no changed
files. The complete test suite then ran from the exported source: 187 passed,
1 skipped, and 5 subtests passed.

The sanitized `result.json` preserves the clean-export runner/archive hashes,
package versions, commands, exit codes, and log hashes. Logs are included for
the dependency installation, every replay check, and pytest. Absolute
workstation paths were replaced with `<REPO>`, `<USER_HOME>`, or `<TMP>`;
published per-log hashes are computed after sanitization.

Reproduce the tracked-only export from the repository root with:

```sh
python3 -m tools.check_clean_export \
  --revision 039ace23a542e82bfc81632d14673d05abea3cec \
  --locked \
  --destination work/clean-export-reproduction
```

Then run the full suite in the exported tree:

```sh
cd work/clean-export-reproduction/source
../venv/bin/python -m pytest -q tests
```

This verifies tracked Python postprocessing and archived-data audits on the
recorded host. It does not rebuild or rerun OpenFOAM/SU2, retrain
PhysicsNeMo, execute Lean, certify the unknown continuous finite-volume field,
or change any scientific acceptance verdict.
