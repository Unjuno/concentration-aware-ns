# PhysicsNeMo issue #2007 follow-up — 2026-09-30

## Live source and report state

- Current `main`: `eb8f95897eed9887295cb8110ba1017d2d670b58` (2026-09-30).
- Issue #2007 remains open: https://github.com/NVIDIA/physicsnemo/issues/2007.
- Fix PR #2008 remains open, targets `ff5d19d08123de47ca446caed1d70a225d540184`, head `7407608723062dc11ba5332e9ff3774f42bb02d9`, and GitHub reports it `BEHIND` with review required.
- The PR head was not changed since the previous review. No full framework suite was run.

## Current-main reproduction

Fetched `physicsnemo/metrics/general/power_spectrum.py` from the exact current-main commit and ran the checked-in CPU reproducer with Torch 2.11.0:

```sh
work/physicsnemo-env/bin/python -m tools.reproduce_physicsnemo_issue_2007 \
  --source-file /tmp/physicsnemo-main-eb8f95897eed.py \
  --source-reference 'NVIDIA/physicsnemo main eb8f95897eed9887295cb8110ba1017d2d670b58' \
  --output evidence/upstream-refresh/physicsnemo-main-issue-2007-validation-2026-09-30.json
```

On a 33x33 single-mode field with wavenumber 5, the height-axis peak is 10.083 while the width-axis energy is split between 6.188 and 5.042; the transposed-array maximum difference is 0.1094484 and fails the fixed tolerance. The 32x32 transpose control passes with maximum difference `2.3842e-7`. Current-main source SHA256 is `13e7847c62b9285daafdf88307bd548e0f18e1f5d4fa0bf33f3552303deb8552`.

For comparison, the identical control was rerun against the exact existing PR #2008 head. The 33x33 transpose difference is `3.5763e-7`, and both odd/even symmetry controls pass. Its source SHA256 is `f66a9028c0a18804471c260a32aed1e3b0e9b59655df0c821d4bb904cdd8c983`.

Raw structured outputs:

- `evidence/upstream-refresh/physicsnemo-main-issue-2007-validation-2026-09-30.json`
- `evidence/upstream-refresh/physicsnemo-pr2008-fix-validation-2026-09-30.json`

## Classification and disposition

This confirms the already-reported odd-width implementation defect remains present on current main and that the existing PR's focused change repairs this reproducer. It does not show a new defect, because issue #2007 and PR #2008 already track the exact behavior and fix. The result was added to the existing PR conversation as a current-main refresh; no duplicate issue or PR was opened. The benchmark's present spectra use even uniform sizes, so this issue does not invalidate those measurements. This is a focused deterministic check, not an endorsement of the entire PR or a full PhysicsNeMo test pass.
