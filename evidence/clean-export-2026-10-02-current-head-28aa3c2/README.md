# Current-head tracked-only replay

Replayed fixed commit `28aa3c2de78264d243598aaf9064918f7e3a8d1b` on macOS 26.6.2 arm64 with Python 3.14.5 and the locked postprocessing requirements. All 38 published-report replay steps and seven additional checks exited successfully. The audit compared 196 tracked report/test-evidence files and found no byte changes. `result.json` records command outcomes, package versions, the tracked archive SHA-256, and sanitized log hashes.

Reproduce from the repository root (choose a new, nonexistent destination):

```sh
python3 -m tools.check_clean_export \
  --revision 28aa3c2de78264d243598aaf9064918f7e3a8d1b \
  --locked \
  --destination work/clean-export-reproduction
```

This validates tracked Python postprocessing and archived-evidence replay on the recorded host. The check does not rebuild or rerun OpenFOAM/SU2, retrain PhysicsNeMo, execute Lean, or upgrade any scientific verdict. It does not run the full pytest suite. The tracked source tarball is intentionally not published here; its SHA-256 is recorded in `result.json` and the command regenerates it from Git.
