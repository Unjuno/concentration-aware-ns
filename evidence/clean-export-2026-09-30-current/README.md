# Current tracked-only clean export

On 2026-09-30, commit `0bf73f202d39a796809f09780f6cd911d31aa437` was exported
with `git archive`, installed into a fresh virtual environment using
`requirements-verification-locked.txt`, and checked on macOS 26.6.2 arm64 with
Python 3.14.5. Report replay and all five additional checks completed with exit
code 0. The replay completed 26 steps, and all 125 tracked report/test-evidence
files were byte-identical before and after replay.

The public summary and individual command logs are in this directory. To repeat
the same fixed-revision check from the repository root, use a new destination:

```sh
python3 -m tools.check_clean_export \
  --revision 0bf73f202d39a796809f09780f6cd911d31aa437 \
  --locked \
  --destination work/clean-export-2026-09-30-replay
```

This validates same-host Python postprocessing and archived report consistency.
It does not rebuild or rerun OpenFOAM, SU2, or PhysicsNeMo; it does not rerun
Lean; and it does not upgrade any numerical-quality or physical verdict.
