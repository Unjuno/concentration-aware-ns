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

## Follow-up: published evidence commit `0d1d164`

After publishing this evidence bundle, the resulting commit
`0d1d1648cad91d99f79e62abfe5193ebe3af619b` was independently exported and
replayed. The follow-up record is in [`current-head-0d1d164/`](current-head-0d1d164/).
Again, all 36 replay steps passed and 171 tracked report/evidence files were
unchanged. The diff from the full-pytest commit `039ace2` to `0d1d164` contains
only goal/completion documentation and this evidence bundle; no Python source
or test files changed. The 187-pass full-suite log above therefore applies to
the same source and tests, while the follow-up specifically rechecks the
published evidence replay at `0d1d164`.
