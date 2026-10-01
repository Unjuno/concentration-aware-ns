# OpenFOAM AMR same-run resolution replication — 2026-10-01

## Result

A second same-run first-refinement capture was performed on the frozen
Foundation 13 high-gradient MMS at `n=32`, using the same `t=0.002` first-map
event as the exploratory `n=16` capture. Before running OpenFOAM,
`tools.predict_amr_grid_candidates` predicted 10,368 sensor-eligible cells,
12,288 cells after the one-layer periodic face-neighbor buffer, and 118,784
cells after refining that set. The solver log records exactly 12,288 selected
cells and a mesh change from 32,768 to 118,784 cells. The independent predictor
also reproduces the archived n=16 selected count of 1,792.

At both resolutions, the post-map cell `U` values exactly match independent
piecewise-constant injection from the same run's captured pre-map parent field.
For n=32, the maximum relative parent-volume closure error is
`9.17e-15`; weighted relative L2 and maximum absolute injection differences
are both zero. This supports expected field-transfer behavior for these two
specific first-refinement events.

| Initial grid | Cells before → after map | Parent injection relative L2 | Coarse DOF vs exact cell averages | Mapped DOF vs exact cell averages | Mapped point-sample error |
|---:|---:|---:|---:|---:|---:|
| n=16 | 4,096 → 16,640 | 0 | 13.7834% | 42.4839% | 41.7955% |
| n=32 | 32,768 → 118,784 | 0 | 3.4942% | 21.0789% | 20.9906% |

The n=32 squared child-average DOF error decomposes into `0.001168` inherited
coarse-solution error plus `0.043264` exact parent-average-to-child-average
variation; the normalized cross term is `5.11e-18` and the identity residual
is `-5.11e-18`. As at n=16, the coarser DOFs are much closer to their own exact
cell averages than the injected values are to finer-cell averages. This is a
DOF comparison: it does not assume OpenFOAM's stored cell-associated `U` is
defined as an exact volume average, and it is not a continuous P0 error norm.

## Reproduction and evidence

- Run protocol: `protocols/high-gradient-of13-amr-same-run-map-v5-n32.json`
- Packaging addendum: `protocols/high-gradient-of13-amr-same-run-map-v5-n32-package-a1.json`
- Evidence: `evidence/of13-amr-same-run-map-v5-n32/`
- Predictor and analyzer: `tools/predict_amr_grid_candidates.py`,
  `tools/analyze_amr_same_run_map.py`
- Tests: `tests/test_predict_amr_grid_candidates.py`,
  `tests/test_amr_same_run_map_v5_n32.py`

The frozen v5 protocol SHA-256 is
`56831c3f34fceaaa45e1395ec850b4b96210aed5911164d6f007d9f9ed2ebf99` and is
reconstructed byte-for-byte from the checked-in file. It pins Foundation
source commit `18870c24d21c6b982e2cdec27b2f59738cca5f90`, the arm64 runtime image
and all generated case inputs. The solver exited zero and logged `End`; the
instrumented library load was confirmed.

The first packaging attempt used the v4 case-root name and created a 129 MiB
archive. That archive is retained under the ignored `work/` tree. The published
archive was rebuilt from the preserved run without rerunning the solver; it is
40.8 MB, contains all six cell-stage snapshots, inputs and logs, and omits the
large face CSVs and generated `dynamicCode`. Their full raw files and captured
hashes remain in the ignored run tree; this n=32 report makes no face-flux,
divergence, or spectrum claim. The post-run packaging change is separated into
the package addendum and does not alter the run protocol or scientific gate.

## Interpretation limits

The spatial comparison is a two-resolution replication of the same exploratory
first-refinement event, not a preregistered AMR convergence study. Both mapped
fields match parent injection, and the point-sample and exact-cell-average DOF
errors decrease at n=32; this is evidence about these cases only. It does not
establish a solver defect, general AMR accuracy, mathematical singularity,
physical blow-up, particle ordering, phase transition, or viscosity change.
The full AMR-quality gate remains UNCERTAIN pending a broader resolution and
time-step study and independent assessment of the solver/runtime stack.

The runner source was modified in the worktree during execution. Its captured
manifest records the parent commit and dirty path list, but not a byte-exact
worktree patch hash at execution. The frozen case inputs, protocol hash, solver
log, binary and all stage hashes are retained; this harness-provenance gap is
explicit and should be closed for future runs by recording the source overlay
hash before launch.
