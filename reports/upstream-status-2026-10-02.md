# Upstream status and dispositions — 2026-10-02

This is a bounded refresh of the public records directly relevant to the
benchmark, not an exhaustive review of every open ticket in each project.

| Project | Live status checked | Disposition |
|---|---|---|
| OpenFOAM Foundation 13 | The benchmark remains pinned to source commit `18870c24d21c6b982e2cdec27b2f59738cca5f90`, also current GitHub `master`. The bounded GitHub list has four open issues and one README PR, none matching this MMS or coded forcing; README directs bug reports to the separate `bugs.openfoam.org` tracker. AMR quality still lacks a preregistered acceptance threshold. | No new report: the endpoint is exploratory and its derivative diagnostic does not establish a solver defect. The separate issue tracker was not exhaustively searched in this refresh. |
| SU2 | `master` remains `bc15466602a687d6fb796d5df7a12ce3fde0949a`, and latest release is v8.5.0. Discussion [#2890](https://github.com/su2code/SU2/discussions/2890) is closed with state reason `resolved`, but no accepted answer is selected. Issues [#2353](https://github.com/su2code/SU2/issues/2353) (time-varying boundary/motion endpoint) and [#2932](https://github.com/su2code/SU2/issues/2932) (maximum-residual location output) remain open. | Existing discussion and adjacent issues cover source-time and residual-observability topics. No duplicate report; the benchmark has not demonstrated a general SU2 defect or fix. |
| NVIDIA PhysicsNeMo | Latest release is v2.2.2. `main` is `83d6a337eecfc70e215ed1978af8dba9a38580fb`; the odd-width `power_spectrum.py` blob remains `fb3e8cda3bc7916b8e56833dda240cb74463fabb` / SHA-256 `13e7847c62b9285daafdf88307bd548e0f18e1f5d4fa0bf33f3552303deb8552`. Issue [#2007](https://github.com/NVIDIA/physicsnemo/issues/2007) remains open and has an updated reproduction note. Fix [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008) remains open, behind main, and review-required. | The known odd-width defect still reproduces on 33×33 and the even 32×32 control passes. Our benchmark uses even grids, so this has no demonstrated impact on its current results. No duplicate issue; the full upstream suite was not run. |
| OpenAI Lean repository | GitHub currently reports main `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, Apache-2.0, `has_issues=false`, and `has_discussions=false`. | No upstream post route. The remaining work is independent scrutiny of the mathematical construction and its consequences; Lean compilation is not itself an external mathematical review. |

PhysicsNeMo's focused replay is
`evidence/upstream-refresh/physicsnemo-main-issue-2007-validation-2026-10-02-83d6a33.json`.
The current project-head, issue, PR and SU2 discussion fields are also recorded
in `evidence/upstream-refresh/upstream-status-2026-10-02.json`. These snapshots
establish the checked records and versions only; they are not claims that all
project issues were searched exhaustively.
