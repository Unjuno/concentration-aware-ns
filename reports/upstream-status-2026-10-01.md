# Upstream issue and PR scope refresh — 2026-10-01

This is a live GitHub inventory refresh for the benchmark's existing three
solver targets plus the OpenAI source repository. It records issue overlap and
scope; it is not a claim that every open issue in these large projects was
independently reproduced. Snapshot data are in
`evidence/upstream-refresh/live-status-2026-10-01.json`.

## OpenFOAM Foundation 13

Observed `master` at `18870c24d21c6b982e2cdec27b2f59738cca5f90`. Its four open
issues are #2 (two-phase version inconsistency), #3 (organization migration),
#4 (AlmaLinux installation), and #5 (generated documentation/source mismatch).
Its sole open PR #7 changes the README. None matches the benchmark's tested
single-phase incompressible MMS or the AMR whole-level budget behavior. The
existing source audit finds that behavior consistent with the documented
approximate-cap selection path. No new report is warranted.

## SU2

Observed `master` at `bc15466602a687d6fb796d5df7a12ce3fde0949a`. The benchmark's
time-dependent MMS callback observation remains in the already-open [discussion
#2890](https://github.com/su2code/SU2/discussions/2890), which includes the
analytic old-time/new-time recurrences, residual controls, and a narrowly scoped
intervention. Existing issue [#2353](https://github.com/su2code/SU2/issues/2353)
tracks end-of-step evaluation of time-varying boundary conditions and motion for
implicit temporal schemes. These records overlap the broader time-contract
area, so no duplicate report was filed. Neither supports a general solver
inconsistency claim; the benchmark's separate residual and accuracy verdicts
remain as documented in the per-case reports.

Recent open issues #2937 and #2939 concern fixed-CL output freshness and a
variable-density pressure-solver Jacobian, respectively; neither applies to the
constant-density incompressible benchmark. Feature request #2932 asks for
maximum-residual locations, while this benchmark already postprocesses spatial
error and derivative fields against an analytic reference; it is not evidence
of a defect.

## NVIDIA PhysicsNeMo

Observed `main` at `536553acf5b03b68ec7283975ba7276d60056a36`.

- [Issue #2007](https://github.com/NVIDIA/physicsnemo/issues/2007) and [PR
  #2008](https://github.com/NVIDIA/physicsnemo/pull/2008) still track and fix
  the odd-width `power_spectrum` indexing defect. The PR is open and behind its
  base. Our archived spectrum cases use even widths, so this defect does not
  invalidate them.
- [Issue #2001](https://github.com/NVIDIA/physicsnemo/issues/2001) reports that
  `GradientsFiniteDifference`, `GradientsSpectral`, and `PhysicsInformer` use
  periodic wraparound without warning for non-periodic domains. It is related
  to existing [feature request #1852](https://github.com/NVIDIA/physicsnemo/issues/1852)
  and open [PR #1853](https://github.com/NVIDIA/physicsnemo/pull/1853), which
  adds a non-periodic lower-level boundary mode. Our benchmark is periodic and
  computes PINN derivatives with autograd at fixed analytic sample points; it
  does not use those grid-gradient backends. Thus the issue is a relevant guard
  for future bounded-domain cases, but not a defect in the current results.
- [Issue #1990](https://github.com/NVIDIA/physicsnemo/issues/1990) reports an
  import failure in the mesh Green–Gauss Warp custom-op path. A smoke import of
  the exact MLP module used by the archived benchmark succeeded in its pinned
  CPU/Torch 2.11.0 environment. This does not reproduce the issue's separate
  deforming-plate entry point and is not a general closure of the issue.

No duplicate issue or PR was filed. The current findings either already have
an upstream tracking item or do not affect the exercised periodic/autograd
benchmark path. The five-seed study remains `UNCERTAIN` because it has no
pre-registered PhysicsNeMo-specific acceptance threshold and does not certify
continuous extrema or optimizer convergence.

## OpenAI source repository

Observed `openai/NavierStokesAndEuler` `main` at
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; repository API reports Apache-2.0
and `has_issues=false`. This is the Lean formalization repository, not a CFD
solver. No software defect was reproduced in its source or formalization, and
GitHub issue reporting is disabled there. The mathematical transfer results
remain conditional as described in the analytic audit; they are not a solver
bug report.

## Reporting decision

No new upstream issue is justified by this refresh. The existing SU2 discussion
and issue, PhysicsNeMo issue/PR pairs, and OpenFOAM source-path audit are the
appropriate records for the current evidence. The benchmark's own PR #2, which
adds the Lean-checked cusp-ball Hessian transfer with conditional packet-scope
documentation, has Python CI passing; it is not an upstream solver patch.

## Same-day live node refresh (2026-09-30 23:45 UTC)

A direct GitHub GraphQL lookup rechecked the records most likely to change the
reporting decision. SU2 discussion #2890 still has one maintainer comment (the
last activity remains September 13); issue #2353 remains open, last updated
September 30. PhysicsNeMo issue #2007 remains open; linked PR #2008 remains
open and behind its base, with head `7407608723062dc11ba5332e9ff3774f42bb02d9`
and base `ff5d19d08123de47ca446caed1d70a225d540184`. These tracked records
still overlap the observed findings, so no duplicate was posted. Exact node
metadata are saved in
`evidence/upstream-refresh/live-status-2026-10-01T2345Z.json`.

## PhysicsNeMo odd-width fix recheck (2026-10-01 03:37 UTC)

The issue and fix PR remain open. Current `main` is now
`b08dd3f61ac44c784f7c03b0cc93947226365cad`; PR #2008 still targets base
`ff5d19d08123de47ca446caed1d70a225d540184`, has head
`7407608723062dc11ba5332e9ff3774f42bb02d9`, and is `BEHIND` with review
required. Comparing the PR head to current `main` reports divergence: 11
current-main commits are absent from the PR head, while two PR-head commits
are absent from current main.

I downloaded the exact `power_spectrum.py` files at both immutable SHAs and
reran `tools/reproduce_physicsnemo_issue_2007.py` with CPU Torch 2.11.0. On
current main, the 32x32 control passes but the 33x33 height/width cosine spectra
differ: the height peak is 10.0833, while the width case splits across 6.1875
and 5.0417; the seeded transpose-control maximum difference is 0.10945. The
existing PR head passes the same odd-size axis and transpose controls (maximum
difference 3.58e-7). This is a focused reproducer, not the full framework
suite. The benchmark's frozen spectral runs are even-width, so its results are
unchanged.

No new issue or duplicate comment was posted: #2007 and #2008 already cover
this defect and proposed fix, and the prior benchmark comment contains the
reproducer. The live metadata, immutable source hashes, and both outputs are
in `evidence/upstream-refresh/physicsnemo-live-recheck-2026-10-01T0337Z.json`
and `evidence/upstream-refresh/physicsnemo-2026-10-01T0335Z/{main,pr-2008}.json`.
