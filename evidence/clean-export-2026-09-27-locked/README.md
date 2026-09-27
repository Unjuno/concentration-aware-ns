# Locked tracked-only postprocessing replay

Fixed commit: `5b8e305`. Fresh venv and tracked-only export on the same host
and Python interpreter. The opt-in dependency file records NumPy 2.5.2,
SciPy 1.16.2, SymPy 1.14.0 and mpmath 1.3.0.

All 18 replay steps and five additional checks exit zero. The strict comparison
of 75 report/test files passes with no changed files. Fifty tests and 93 gate
artifact links pass within the replay; the restart scientific time failure is
reproduced, not relabeled. Result, package versions and hashed logs are preserved.

This is not an all-files, cross-platform, solver-build, training, or Lean
reproduction claim. Logs and runtime timing metadata are outside the 75-file
byte comparison. The prior supported-range failure with NumPy 2.5.3 remains
archived separately and is not erased.

```sh
python3 -m tools.check_clean_export --revision 5b8e305 --locked --destination work/clean-export-locked-reproduction
```
