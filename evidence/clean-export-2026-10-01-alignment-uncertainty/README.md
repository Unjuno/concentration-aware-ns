# Fresh locked replay with alignment-uncertainty check — 2026-10-01

Commit `6e16c659393e6910b7947101be5469c272827d88` was exported from tracked
files, installed into a new virtual environment using
`requirements-verification-locked.txt`, and replayed on macOS 26.6.2 arm64,
Python 3.14.5. All 26 published-report replay steps and seven additional
checks exited zero. The seven checks include the new exact Gaussian
alignment-versus-position calculation. All 153 tracked reports and test
evidence files matched byte-for-byte (`changed_files: []`). The complete pytest
suite reported 151 passed, one skipped, and five subtests passed.

`result.json` records the exported commit, source and runner hashes, package
versions, commands, exit codes, and log hashes. This is a same-host replay of
Python post-processing and archived algebra; it did not rerun a solver,
training, or Lean proof and does not upgrade a scientific verdict.

To reproduce with another unused destination path:

```sh
work/reference-check-env/bin/python -m tools.check_clean_export \
  --revision 6e16c659393e6910b7947101be5469c272827d88 \
  --locked \
  --destination work/clean-export-reproduction
```
