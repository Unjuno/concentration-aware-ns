# Fresh tracked-only replay at 2026-10-01

Commit `33c460715ad6cc3f9f61303d94b85efc5be06f2b` was exported with
`git archive`, installed into a new virtual environment from
`requirements-verification-locked.txt`, and replayed on macOS 26.6.2 arm64,
Python 3.14.5. All 26 archived-input replay steps and six additional checks
exited zero. The regenerated reports and test evidence matched all 152 tracked
files byte-for-byte (`changed_files: []`). The full suite ran under pytest:
146 passed, one skipped, and five subtests passed.

`result.json` records the archive and runner hashes, package versions, commands,
exit codes, and log hashes. This verifies same-host Python postprocessing and
archived algebra/report outputs only. It did not rebuild or rerun OpenFOAM,
SU2, PhysicsNeMo, or Lean, and it does not upgrade any scientific verdict.

To reproduce from the repository root, use a new destination directory:

```sh
work/reference-check-env/bin/python -m tools.check_clean_export \
  --revision 33c460715ad6cc3f9f61303d94b85efc5be06f2b \
  --locked \
  --destination work/clean-export-reproduction
```
