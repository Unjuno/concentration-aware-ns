# OpenFOAM 13 AMR stage snapshot v3

## Result

The pinned n=16 high-gradient AMR case completed with five snapshots around its
first refinement. The `mapped` snapshot is at `t=0.002`, immediately after
`mesh_.update()`; flux correction and later solver stages are at `t=0.003`
because `foamRun` increments time after `preSolve()`. Every snapshot contains
16,640 cells and 48,816 faces, with exactly matching recorded cell and face
geometry/connectivity.

The instrumented final `U`, `p`, `phi`, and `Uf` files match the frozen
uninstrumented first-refinement case byte-for-byte. This establishes
noninterference for this diagnostic run. Evidence and analysis are in
`evidence/of13-amr-stage-snapshot-v3/`; the raw solver archive is
`evidence/of13-amr-stage-snapshot-v3/amr-stage-snapshot.tar.gz`.
The generated provenance JSON contains an outdated checkpoint-description
string; its raw hash and the correction based on the executed protocol and
solver log are preserved in `evidence/of13-amr-stage-snapshot-v3/provenance-correction.json`.

| Stage | Physical time | Relative volume-L2 velocity error vs exact MMS |
|---|---:|---:|
| Immediately after mapping | 0.002 | 41.7955% |
| After `correctPhi` | 0.003 | 41.8156% |
| Before pressure correction | 0.003 | 41.7898% |
| After pressure correction | 0.003 | 39.9477% |
| After PIMPLE | 0.003 | 39.9477% |

Cell `U`, `p`, and face `Uf` are unchanged from mapping through `correctPhi`;
the face `phi` relative L2 change is 97.35%. A finite-volume divergence
reconstruction from the recorded owner/neighbour incidence and `phi` gives a
volume-weighted RMS `div(phi)` decrease from 0.9527 immediately after mapping
to 0.09664 after `correctPhi` (89.85%). Momentum prediction changes cell `U`
by 0.493% relative L2. Pressure correction changes it by 4.834% relative L2
and reduces the exact-MMS velocity error by 1.842 percentage points. The
pressure field changes substantially during its solve; the relative pressure
change uses a small pre-pressure norm and should not be read as an error ratio.

## Post-hoc parent-injection audit

An additional archive-based audit checks the mapped cell-centered velocity
against independent piecewise-constant injection from the earlier archived
uniform-grid `t=0.002` parent field. The audit validates both archive hashes and
finds a weighted relative L2 difference of `1.79e-16` (maximum absolute
difference `5.55e-17`). Injection of that parent field gives the same 41.7955%
point-sample error against exact MMS at child-cell centers as the captured
mapped field. An algebraic decomposition attributes most squared point-sample
discrepancy to changes in the exact reference between parent and child centers;
this is not a canonical finite-volume interpolation error estimate.

This is a **cross-run reconstruction**, not a direct v3 same-run pre-map
capture. The archived v1 parent run has the same hashes for 10 of 11 common
case inputs; the only differing common file is `system/controlDict`, whose
write interval changed from `0.001` to `0.003`. Final field output agrees, but
that does not prove the internal pre-map field was identical. A same-run
pre-map capture was still needed to make that attribution direct at the time;
the same-run gap was subsequently tested with v4. The added
audit and synthetic geometry checks are in
`tools/analyze_amr_stage_snapshots.py`,
`tests/test_amr_parent_injection.py`, and
`evidence/of13-amr-stage-snapshot-v3/analysis.json`.

At `t=0.002`, the v4 instrumented run records 4,096 coarse cells immediately
before `mesh_.update()` and 16,640 cells immediately after it. Mapping each
new cell to its geometrically containing pre-map parent gives exact equality
with captured mapped `U` (weighted relative L2 0 and max absolute difference
0); parent-to-child volume closure is `6.53e-15`. The velocity volume integral
changes by `2.91e-16` absolute; scaled by integrated speed, the net-integral
change is `8.10e-17`. Exact-MMS point-sample error at child centers is
41.7955%. The paired fields are from the same execution, directly identifying
the mapped cell-center values as piecewise-constant parent injection in this
case. This does not certify finite-volume cell averages, convergence, general
remapping behavior, or physical effects. Raw archive, recovered manifest,
protocol, and replayable analyzer are under
`evidence/of13-amr-same-run-map-v4-run3/`,
`protocols/high-gradient-of13-amr-same-run-map-v4.json`, and
`tools/analyze_amr_same_run_map.py`. Manifest recovery is disclosed: the solver
and archive completed, then the initial runner raised a post-run `KeyError`
while reading a missing protocol metadata key. The manifest was reconstructed
from preserved logs, exit status, hashes, and archive without rerunning the
solver. Because the runner failed before writing its manifest, the protocol
hash at the instant of execution is unavailable; the recovered manifest
records the current protocol hash separately and does not claim it is the
at-run hash. The solver input hashes, exact source-file hashes, binary hash,
log hash, and archive hash are preserved.

## Same-run exact finite-volume-average DOF comparison

The v4 `preMap` and `mapped` arrays were also compared with the analytic volume
average of the MMS over each respective cubic cell. The closed form integrates
the separable Fourier modes using sinc factors; its existing independent
tensor-Gauss check has maximum absolute difference `1.80e-16`. The preMap
coarse-cell stored values have relative L2 difference `13.7834%` from the
coarse-cell exact averages. After the same values are injected into refined
cells, the child-DOF difference from exact child averages is `42.4839%`, while
the point-sample metric at child centers is `41.7955%`.

For the child-average metric, the normalized squared error decomposes as
`0.015871` inherited parent DOF error plus `0.164617` exact parent-average to
child-average variation, with cross term about zero (`2.0e-17`) and identity
residual below `2.0e-17`. Thus this case's increase under the fine-cell DOF
average comparison is dominated by subcell variation revealed by refinement,
not by a change in the stored mapped velocity values. This is an alternate
finite-volume DOF comparison: OpenFOAM's `volVectorField` is cell-associated,
and this result does not establish that every evolved stored value is defined
as an exact cell average. It is not a continuous piecewise-constant error
norm, quality pass/fail, or defect verdict. Results and the formula-check hash
are in `evidence/of13-amr-same-run-map-v4-run3/analysis.json`.

## Separate `maxCells` behavior reproduction

The archived case's `dynamicMeshDict` sets `maxCells 5000`, starts from 4,096
cells, and the solver selects 1,792 cells, producing 16,640 cells. A post-hoc
isolated reproduction compiled `libfvMeshTopoChangers.so` from the pinned
Foundation source commit in the same arm64 runtime image, confirmed the loaded
library path, and again completed with 16,640 cells. The source's candidate
selection computes a budget in increments of seven cells, then can pass the
whole candidate level after that count crosses the budget. This reproduces
cap overshoot for this configuration. It does not establish the intended
global semantics of `maxCells`, a general OpenFOAM defect, an AMR quality
failure, or any physical effect. Full command, hashes, and limitations are in
the ignored raw run artifacts under `work/of13-maxcells-probe-v1/`. This
confirms the already documented approximate-cap, whole-level selection
semantics from `reports/openfoam-amr-source-budget-audit-2026-09-28.md`; it is
not a new upstream defect finding, so no duplicate issue was filed. An earlier
local draft interpreted the documented stop wording as a hard-cap promise,
but the existing project audit and complete event evidence explicitly classify
this behavior as approximate and non-defective. The draft was withdrawn. The
reproduction is supplemental evidence only.

## Interpretation limits

This separates the observed state changes for one first-refinement event. The
largest velocity discrepancy is already present in the mapped state, while
`correctPhi` changes face fluxes and strongly reduces reconstructed discrete
divergence without changing cell velocity. The pressure stage reduces the
velocity error in this case. These results do not establish whether the
remaining mapped-state discrepancy is interpolation error, gradient
reconstruction, time integration, source/model interaction, or another
mechanism. They do not demonstrate a general OpenFOAM defect, loss of PDE
regularity, molecular ordering, or a physical viscosity transition.

The module is compiled from pinned Foundation source and loaded ahead of the
packaged module, while the remaining runtime libraries come from a pinned
container image. Exact final-field agreement limits instrumentation concerns
for this case, but does not prove the packaged binary is generally equivalent
to all inspected source revisions. The one low-resolution event is not an AMR
convergence study; the AMR quality status remains UNCERTAIN. No upstream issue
is justified by this evidence alone.

Reproduce the case with `python3 -m tools.run_amr_stage_snapshot` and the
analysis with `python3 -m tools.analyze_amr_stage_snapshots` from a clean
checkout with the pinned source tree and image. Failed v1/v2 attempts are
preserved under their versioned `work/of13-amr-stage-snapshot-v1/` and
`work/of13-amr-stage-snapshot-v2/` paths.
