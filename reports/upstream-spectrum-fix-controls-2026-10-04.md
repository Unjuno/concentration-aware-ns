# Live upstream refresh and stronger spectrum-fix verdict — 2026-10-04

A self-audit found a weak fix rule in this benchmark's focused PhysicsNeMo
reproducer: `not reproduced` could pass when the old failure pattern disappeared
because other controls were broken. The rule now requires positive finite spectra
and every even/odd axis and transpose symmetry control. This corrects our
verification tool; it is not a newly discovered upstream defect.

## Executed adversarial validation

| Exact source | Old odd-width pattern reproduced | All fix controls pass | Expected verdict |
| --- | --- | --- | --- |
| PhysicsNeMo main b45a5c810c741e6b41f8515be24c51121f8fc21f | Yes | No | Reproduction PASS |
| Existing PR #2008 head 7407608723062dc11ba5332e9ff3774f42bb02d9 | No | Yes | Focused fix PASS |
| Deliberately invalid zero-spectrum control | No | No | Fixed expectation rejected, exit 1 |

The zero function returns zero spectra for every input, hence passes symmetry
comparisons while conveying no information about the input. The old negative
rule would accept it as fixed. Its execution now produces a failed fix verdict,
with exit 1 and preserved output. Eleven pure-Python controls additionally
reject each required symmetry failure, nonfinite spectra, zero and negative power.
The valid-current-source and PR functions were loaded from freshly downloaded
immutable GitHub content references, without editing either upstream file.
Runs use CPU Torch 2.11.0; numerical source is
`fa15e1ebae0dcadd5844200a6a847bc1eaa10d2b`.

The main file SHA256 remains
`13e7847c62b9285daafdf88307bd548e0f18e1f5d4fa0bf33f3552303deb8552`;
the fix file remains
`f66a9028c0a18804471c260a32aed1e3b0e9b59655df0c821d4bb904cdd8c983`.
Previous focused-fix records already contain successful required controls, so
the stricter rerun supports their narrow conclusion. It does not retrospectively
turn those runs into full-framework validation. New fields in the evidence state
the stronger rule explicitly; original records remain untouched.

## Live upstream disposition

Fresh GitHub API reads, with cache-bypass headers and unique query strings, show:

- OpenFOAM Foundation 13 head remains `18870c24d21c6b982e2cdec27b2f59738cca5f90`.
  The latest input audit still supplies no new contract violation warranting a
  defect report. No new issue was submitted.
- SU2 master remains `bc15466602a687d6fb796d5df7a12ce3fde0949a`.
  [Discussion #2890](https://github.com/su2code/SU2/discussions/2890) is unanswered
  in GitHub's answer field, with one comment and one reply. The existing diagnosis
  and BDF2 follow-up are preserved; no new maintainer reply appeared in this read.
  [PR #2857](https://github.com/su2code/SU2/pull/2857) remains closed and unmerged.
  These states are not acceptance or rejection of our full benchmark conclusions.
- PhysicsNeMo main advanced to `b45a5c810c741e6b41f8515be24c51121f8fc21f`, but its
  [spectrum function](https://github.com/NVIDIA/physicsnemo/blob/b45a5c810c741e6b41f8515be24c51121f8fc21f/physicsnemo/metrics/general/power_spectrum.py)
  blob remains `fb3e8cda3bc7916b8e56833dda240cb74463fabb`.
  [Issue #2007](https://github.com/NVIDIA/physicsnemo/issues/2007) and
  [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008) remain open; the PR
  is two commits ahead and fourteen behind current main, with a diverged relation.
  Latest release remains v2.2.2. Existing periodic-boundary Issue #2001, Issue
  #1852 and draft PR #1853 remain open. No duplicate report is justified.

The benchmark's frozen even-width spectra and periodic operators remain separate
from the odd-width and nonperiodic-boundary issue families. Current code and
tracking were checked, not the exhaustive issue history or all three upstream
test suites. See [live metadata](../evidence/physicsnemo-spectrum-fix-controls-2026-10-04/live-status.json).

## Reproduction

Fetch `physicsnemo/metrics/general/power_spectrum.py` from each immutable source
commit above and verify the SHA256 before running. With CPU Torch installed:

```bash
python -m tools.reproduce_physicsnemo_issue_2007 \
  --source-file /absolute/path/main-power_spectrum.py \
  --source-reference b45a5c810c741e6b41f8515be24c51121f8fc21f \
  --output /absolute/path/new-main-result.json
python -m tools.reproduce_physicsnemo_issue_2007 --expect-fixed \
  --source-file /absolute/path/pr2008-power_spectrum.py \
  --source-reference 7407608723062dc11ba5332e9ff3774f42bb02d9 \
  --output /absolute/path/new-fix-result.json
```

Running with `--expect-fixed` against the published zero-spectrum negative
control must exit 1. The fix requirement is stronger than before but remains a
focused symmetry check: it does not certify normalization, physical wavenumber
accuracy, all shapes/dtypes/devices, or the full framework. No new CFD/PINN
training run is included. Source hashes and logs are preserved in the
[evidence package](../evidence/physicsnemo-spectrum-fix-controls-2026-10-04/README.md).
Full locked benchmark suite: **308 passed, 1 skipped, 83 subtests passed**.
Compile checks and `git diff --check` pass. This is the benchmark suite, not
any target framework's complete suite.

The full concentration-aware goal, continuous reconstruction quality and
analytic/physical obligations remain open.
