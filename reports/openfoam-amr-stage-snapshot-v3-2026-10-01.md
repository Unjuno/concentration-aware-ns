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
