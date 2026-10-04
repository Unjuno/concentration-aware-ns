# Executed n16 cellPoint reconstruction capture — 2026-10-04

The planned successor is now executed. The unchanged n16 mean-quality recipe
was run on an isolated ARM64 GitHub VM, followed by a compiled, read-only
Foundation 13 cellPoint probe. Final mesh instances, point values, tetrahedral
addressing and centre/shared-face evaluations are publicly archived. This
closes the missing-mesh **capture** gap for the new n16 case, not for the
original unarchived meshes or the larger-resolution cases.

Capture source: `4999a4db38d0ac41a5f253a6665f6701d64f561c`.
Independent analyzer source: `2e39697f0638018aad622b27964fc5a5986ccfe6`.
[Hosted run 37143558038](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37143558038)
completed both change detection and the capture job successfully; every build,
case-run, probe and artifact step succeeded. Package source remains
OpenFOAM-13 `18870c24d21c6b982e2cdec27b2f59738cca5f90`.

## Preservation controls

The wrapper verifies all twenty original numerical recipe source-file hashes
before using the existing runner. No original source/input/protocol is altered.
The fresh n16 input hashes and final U/p hashes match the earlier original
n16 case byte-for-byte. The original capture-disabled control also produces
byte-identical U/p. The probe container mounts the final case read-only and
its before/after U/p hashes are identical.

Eight installed interpolation source files match the immutable upstream pin.
The existing base runner additionally checks the package/module and stock
library fingerprints. This is recorded provenance, not a general theorem that
all released binaries were built from every inspected source file. The probe
is compiled against the packaged runtime and its binary digest is preserved.
The data package includes the applicable GPL license and our probe source.

## Native and independent measured checks

| Quantity | Result |
| --- | ---: |
| Final cells | 16,640 |
| Mesh points | 20,209 |
| Tetrahedra | 207,488 |
| Internal faces | 48,816 |
| Native near-degenerate tet count | 0 |
| Invalid face-base indices | 0 |
| Minimum recorded absolute determinant | 0.003784945883825494 |
| Native `small` | 2.220446049250313e-16 |
| Maximum centre interpolation difference | 5.575472776331846e-17 |
| Maximum internal-face owner/neighbour difference | 3.818485674639095e-15 |
| Maximum relative cell/tet volume-sum mismatch | 1.0541403013968078e-14 |
| Shared internal-face triangle owner/neighbour matches | All |

The C++ probe records stored U, sampled cellPoint values, shared point values,
mesh coordinates, tet vertices/determinants and face traces. The independent
Python analyzer verifies finite data and label/count integrity, every shared
triangle's owner/neighbour vertex identity, centre/face summary consistency and
cell-wise sums of absolute tet volumes. It does not accept face-sample agreement
as a substitute for triangle connectivity. The initial local and locked-environment
analysis JSON are byte-identical.

Three regression controls check reversed triangle orientation, rejection of a
wrong shared vertex even when face samples remain zero, and detection of a
degenerate tet plus volume deficit. The complete locked benchmark suite passes
**315 tests, 1 skipped, 83 subtests** on the analyzer commit. Compilation checks,
`git diff --check` and the hosted C++ build pass. This is not OpenFOAM's complete
upstream test suite.

## Public evidence and replay

The [release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-cell-point-capture-v1-4999a4d)
contains the complete 17,269,083-byte bundle, with SHA256
`ad1fb32afd6e9cb1f799945fa2967d09150fc567bd3daa11e0a62029a268e830`.
GitHub's asset digest and byte count match the locally generated bundle.
The new base raw archive and every member hash, the mesh archive and all
fourteen members, and the captured-file hashes were checked after download.
The effective final `0.05/polyMesh` and initial `constant/polyMesh` are both
preserved, including final refinement data. Raw CSVs, installed-source receipts,
build/run logs and source are in the bundle; small records and validation receipts
are in [tracked evidence](../evidence/of13-cell-point-capture-v1-n16/README.md).

To repeat the full successor on an ARM64 Docker host, check out the capture
source and the pinned upstream source, install the locked dependencies, build
`runtime/of13-interface-operator` as an ARM64 image, then run with fresh paths:

```bash
python -m tools.run_of13_cell_point_capture \
  --image concentration-aware-ns:of13-cell-point-v1 \
  --source /absolute/path/pinned-OpenFOAM-13 \
  --work /absolute/path/new-work --evidence /absolute/path/new-evidence
```

The runner enforces the old resource requirements and limits the offline probe
to 3 CPUs, 12 GiB and 600 seconds. The case directory is read-only for the
probe. To independently analyze the downloaded capture-evidence directory at
the analyzer commit:

```bash
python -m tools.analyze_of13_cell_point_capture \
  --evidence /absolute/path/capture-evidence --output /absolute/path/new-analysis.json
```

## What remains unproved

This is runtime capture plus floating/topology checks, not an outward-enclosed
proof of the full geometric partition. Native determinant observations are
not an interval proof; the tetrahedron search's complete branch history is not
instrumented. Matching face samples alone cannot prove global continuity.
Further exact geometry/rounding analysis is needed before transferring the
[conditional gradient witness](openfoam-amr-point-gradient-bound-2026-10-04.md)
as a named continuous-field certificate on these data. The prior n64 lower
bound is not automatically validated by this n16 experiment.

The built-in interpolation is a named reconstruction, not an established
canonical continuous solver solution. No pointwise curl transfer, new solver
quality threshold, upstream defect or physical consequence follows. The
original acceptance decisions remain unchanged. Larger cases, exact continuous
reconstruction validation, other solver quality and analytic/physical
obligations remain open under the full goal.
