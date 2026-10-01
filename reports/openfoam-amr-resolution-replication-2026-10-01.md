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

A fixed-first-map-time temporal-step control at `n=32`, `dt=0.0005` was also
completed. `refineInterval=4` kept the first map at `t=0.002`; the solver-stage
snapshots are at `t=0.0025`. The solver again selected 12,288 cells and reached
118,784 cells. Parent injection remains exact and the maximum relative
parent-volume closure is `9.17e-15`.

| `dt` | Coarse DOF vs exact cell averages | Mapped DOF vs exact cell averages | Mapped point-sample error |
|---:|---:|---:|---:|
| 0.001 | 3.494218% | 21.078943% | 20.990564% |
| 0.0005 | 3.496856% | 21.079361% | 20.990984% |

These small differences compare discrete pre-map histories only. Halving `dt`
doubles the number of pre-map steps and `refineInterval` is changed to preserve
the same map time, so this is not a formal temporal order study or an isolated
one-variable intervention. It adds no temporal accuracy gate and does not
change the AMR quality verdict.

## Interior Gauss-gradient and vorticity diagnostic

The retained preMap and mapped face data were used to calculate a discrete
Gauss gradient. At the uniform preMap stage, centered periodic differences
from the captured cell `U` are equivalent to arithmetic-midpoint face
interpolation on the orthogonal grid. At the mapped stage, the calculation
uses captured internal-face `Uf` and oriented `S`, adding opposite
owner/neighbour contributions and dividing by cell volume. Vorticity is the
curl of this reconstructed gradient. Both are compared with the analytic MMS
point gradient/curl at cell centers.

For a fair within-run comparison, both stages use the same physical interior
mask: cell centers must be more than two initial-grid widths from every
periodic boundary. This yields the same retained volume fraction at preMap and
mapped for each resolution; cyclic boundary faces are absent from the captured
face table. The metrics therefore cover 42.1875% of the n=16 domain and
66.9922% of the n=32 domain, and they are volume weighted only on those
subdomains.

| Initial grid / `dt` | Gauss-gradient relative L2: preMap → mapped | Vorticity relative L2: preMap → mapped |
|---|---:|---:|
| n=16 / 0.001 | 26.3494% → 48.3516% | 31.0782% → 54.3949% |
| n=32 / 0.001 | 8.7188% → 22.0848% | 9.0557% → 21.5574% |
| n=32 / 0.0005 | 8.7197% → 22.0856% | 9.0557% → 21.5571% |

At n=32, 147,456 of 352,128 captured mapped internal faces (41.8757%) join
children of the same parent cell. On those faces, `Uf` equals the injected
parent value exactly (max absolute difference 0). The mapping therefore
creates no velocity variation across those subcell interfaces. The rise in
this Gauss-gradient diagnostic after mapping is consistent with refining a
piecewise-constant parent field without adding subcell slope information; it
does not identify a defect. The two time-step controls give nearly identical
gradient/curl errors at the fixed map time.

This is a specified finite-volume reconstruction diagnostic, not necessarily
the solver's configured/stored `grad(U)`, not a cell-integrated derivative
norm, and not a general AMR accuracy result. It says nothing about singularity,
particle ordering, phase transition, or a material viscosity law. The
reproducible analyzer is `tools/analyze_amr_gauss_gradient.py`; its bounded
outputs are `gauss-gradient-audit.json` in each n=16/n=32 evidence directory.

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
- Fixed-map-time time-step control: `protocols/high-gradient-of13-amr-same-run-map-v6-n32-dt0005.json`,
  `evidence/of13-amr-same-run-map-v6-n32-dt0005/`
- Predictor and analyzer: `tools/predict_amr_grid_candidates.py`,
  `tools/analyze_amr_same_run_map.py`, `tools/analyze_amr_gauss_gradient.py`
- Tests: `tests/test_predict_amr_grid_candidates.py`,
  `tests/test_amr_same_run_map_v5_n32.py`

The frozen v5 protocol SHA-256 is
`56831c3f34fceaaa45e1395ec850b4b96210aed5911164d6f007d9f9ed2ebf99` and is
reconstructed byte-for-byte from the checked-in file. It pins Foundation
source commit `18870c24d21c6b982e2cdec27b2f59738cca5f90`, the arm64 runtime image
and all generated case inputs. The solver exited zero and logged `End`; the
instrumented library load was confirmed.

The first packaging attempt used an incorrect case-root name and exceeded the
hosting size limit; those archives are retained under the ignored `work/`
tree. The final published archives were rebuilt from the preserved runs
without rerunning either solver. They are 36.5 MB (dt=.001) and 36.0 MB
(dt=.0005), and contain the same-run preMap/mapped cell pair, mapped internal
faces needed for the Gauss-gradient audit, inputs, and logs. The uniform preMap
gradient is reconstructed from cell `U`; preMap face CSVs, later-stage
diagnostic cell/face CSV snapshots, and generated `dynamicCode` are excluded
from these n=32 archives. Native OpenFOAM checkpoint directories remain in
the case tarballs and are not the captured stage CSVs. Complete raw files and hashes remain under ignored `work/` and
the raw manifest/log. Published numerical claims use only the included
same-run mapping pair and mapped internal faces; no later PIMPLE-stage
field/flux, divergence, or spectrum claim is made. Package addenda `package-a4`
are separate from the as-run protocols and do not change solver inputs or
acceptance.

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
