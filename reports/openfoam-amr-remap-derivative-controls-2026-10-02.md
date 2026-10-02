# OpenFOAM AMR derivative comparison against fixed-final-mesh controls

Date: 2026-10-02

Solver: OpenFOAM Foundation 13 package `20260624`, image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`

Protocol: `protocols/high-gradient-of13-v2.json`, SHA-256
`838ac4d91d8a816f96cebf02d780a9ec7df265ae3b45748d2a2c795c6d80d93d`

## Result

Replayed OpenFOAM's `grad(U)` and `vorticity` post-processing on the archived
dynamic-AMR endpoint cases and their fixed-final-mesh analytic-initialization
controls. No solver time integration was rerun. For each cell budget, the
dynamic and control archives have byte-identical points, faces, owner,
neighbour, boundary, cell centers, and cell volumes. They therefore share the
same final mesh and the same interior evaluation mask.

| Cell budget | Path | Velocity rel. L2, all cells | Gradient rel. L2, interior | Vorticity rel. L2, interior |
|---:|---|---:|---:|---:|
| 5,000 | dynamic AMR history | 37.0118% | 48.7234% | 54.6454% |
| 5,000 | analytic-initialized final-mesh control | 1.8784% | 7.3485% | 8.6300% |
| 100,000 | dynamic AMR history | 40.1117% | 89.7912% | 110.4208% |
| 100,000 | analytic-initialized final-mesh control | 0.4826% | 1.9784% | 2.3403% |

The gradient and vorticity errors are volume-weighted relative L2 comparisons
with the exact MMS point derivatives at cell centers, restricted to the same
interior subdomain used by the AMR Gauss-gradient study. The mask retains
4,416/16,640 cells (26.5385%)/42.1875% of volume at cap5000 and
22,560/101,760 cells (22.1735%)/42.1875% of volume at cap100000. These are
diagnostics, not the benchmark's predeclared
peak-error gates or continuous extrema.

The comparison shows that the final meshes can represent substantially more
accurate endpoint velocity and derivative fields when initialized directly
from the analytic solution. The dynamic-AMR history is associated with much
larger endpoint errors on those same meshes. It does **not** isolate mapping
alone: the static control has an accurate fine-mesh initial field, while the
dynamic case evolves first on the coarse mesh, maps, and then continues. The
difference includes coarse-history error, mapping, and later evolution. Thus
it narrows the mechanism toward the adaptive history rather than a simple
lack of final-mesh capacity, but does not identify one defective operation.
AMR quality attribution remains `UNCERTAIN`; no upstream issue or physical
interpretation follows.

## Derivative convention and independent check

The source-pinned Foundation 13 implementation at commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90` constructs Gauss gradients through
`outerProduct<vector, Type>` and forms each face contribution as `Sf * U`.
The pinned `Vector * Vector` implementation stores the spatial derivative
index first. The analytic reference here stores velocity component first,
`(grad U)[i,j] = dU_i/dx_j`; the `grad(U)` tensor is therefore transposed before
comparison. Treating the two storage conventions as identical would produce
incorrect component errors and curl.

As a separate consistency check, the OpenFOAM `vorticity` function output
matches the curl of the transposed `grad(U)` on all four cases to relative L2
between `2.20e-16` and `2.62e-16`. Re-running `grad(U)` on both dynamic archives
reproduces their originally archived solver field byte-for-byte. Source file
hashes, all archive hashes, output hashes, and post-processing log hashes are
in [`comparison.json`](../evidence/of13-amr-remap-gradient-controls-2026-10-02/comparison.json).

## Reproduction

From the repository root, with the locked Python verification dependencies,
Docker context `orbstack`, and the recorded Foundation 13 image available:

```sh
PYTHONPATH=. uv run --with-requirements requirements-verification-locked.txt \
  python -m tools.replay_amr_remap_gradient_controls \
  --work-root work/of13-amr-gradient-controls-replay-2026-10-02-final
```

The command verifies each archived tarball against its existing manifest,
extracts into a new work directory, runs `foamPostProcess` with networking
disabled, checks exact final-mesh identity and field conventions, validates
the dynamic archived gradients, and writes the comparison JSON and logs under
`evidence/of13-amr-remap-gradient-controls-2026-10-02/`. It does not run the
solver. The local Ubuntu dependency snapshot used to build the image is not
pinned, so recreating that image from the Dockerfile is not guaranteed to
produce the same image ID; this replay requires the captured image ID.

## Interpretation limits

- The exact gradients are pointwise at cell centers; this is not a cell-average
  derivative norm or a certified maximum.
- The controls do not match the dynamic case's coarse pre-map field and hence
  cannot assign the full error difference to remapping.
- The calculations establish a solver-path diagnostic only. They do not
  establish a software defect, singularity, molecular ordering, or viscosity
  transition.
