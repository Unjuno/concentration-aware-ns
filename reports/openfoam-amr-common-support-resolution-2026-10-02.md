# OpenFOAM AMR first-map diagnostics on common physical support

## Question and protocol

Does the first-refinement Gauss-gradient/vorticity comparison change with
resolution when every grid uses the same physical evaluation region? Earlier
dated reports used a boundary exclusion of two *grid-dependent* base-cell
widths. Those within-run comparisons were paired consistently, but their
metrics were not directly comparable across n=16, 32, and 64.

Protocol `protocols/high-gradient-of13-amr-same-run-map-v7-n64.json` was
committed before the n=64 solver run in commit `ffc81a2cfe119204e7bf240310699ea739991656`.
Its SHA-256 is
`9cd80353a5f9cbcbcd82eb8309406b00d65df6b2fd34b4535671311b714fa4a7`. The
independent structured-grid predictor fixed 83,712 raw sensor cells, 91,392
buffered cells, and 901,888 mapped cells before execution. The target was
Foundation 13 source `18870c24d21c6b982e2cdec27b2f59738cca5f90`, in image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b` on
linux/arm64.

## Run and archive verification

The solver exited zero, logged `End`, and loaded the instrumented module. It
selected exactly 91,392 cells and refined 262,144 to 901,888 cells. Six stage
events were captured: same-run `preMap` and `mapped` at t=0.002, followed by
four PIMPLE stages at t=0.003; the final step logged convergence in five
iterations. The complete as-run archive is 996,285,706 bytes with SHA-256
`7f9cba57e985007c73d8b6e1baf217f18e5f0d33dec168fe59ed999959c5dbdf`. Its
hash was recomputed and all 59 tar members were fully read before it was
preserved under ignored `work/`. `manifest-as-run.json` retains the original
run record. For publication, a compact review archive keeps the map-time
preMap and mapped cell snapshots, mapped internal faces, inputs, and solver
log; it excludes preMap faces, all later PIMPLE snapshots, and `dynamicCode`.
The compact gzip tar is 278,621,920 bytes, SHA-256
`a9933f34d824cdd40adf10052fc121f62041bbf943a69b24102e3c141a26c6b5`; its
Zstandard stream is split into four GitHub-compatible parts, indexed by
`evidence/of13-amr-same-run-map-v7-n64/amr-stage-snapshot-n64-review.tar.gz.zst.parts.json`.
The reconstruction utility verified every part hash, the compressed-stream
hash, decompressed size/hash, and byte identity against the local compact tar.
The runner recorded a clean worktree at source commit `ffc81a2` and all input,
module, stage-snapshot, image, and log hashes in
`evidence/of13-amr-same-run-map-v7-n64/manifest-as-run.json`; current
`manifest.json` additionally records publication packaging.

The same-run mapping analysis finds zero relative-L2 and maximum-absolute
difference between mapped cell `U` and piecewise-constant injection of its
preMap parent value. Maximum parent-volume closure error is
`1.98e-14`. The analytic cell-average DOF discrepancy is 0.8802% before map
and 10.5016% after map; the point-sample discrepancy is 10.4905% after map.
These are discrete DOF and point-sample comparisons, not a claim that evolved
OpenFOAM cell values are mathematically defined as exact averages.

## Common-support derivative results

`tools/compare_amr_resolution_gauss.py` replays the three archived same-run
map pairs on one fixed region: cell centers farther than `pi/4` from every
periodic boundary. This margin equals two base-cell widths at n=16 and gives
the same retained physical volume fraction, 0.421875, for every grid and both
stages. The analyzer checks the archive hashes and matching interior volume
fraction. It also uses one operator for every preMap stage (centered periodic
differences) and one face-based Gauss operator for every mapped stage. This
avoids mixing saved preMap face reconstruction at some resolutions with
centered differences at another. Results are in
`evidence/of13-amr-resolution-comparison-2026-10-02.json`; analyzer SHA-256 is
recorded there with the Gauss operator implementation hash.

| n | Gauss-gradient relative L2, preMap → mapped | Vorticity relative L2, preMap → mapped |
|---:|---:|---:|
| 16 | 27.0806% → 48.3516% | 31.0782% → 54.3949% |
| 32 | 7.3439% → 24.2994% | 8.6245% → 27.9133% |
| 64 | 1.8830% → 12.1431% | 2.2121% → 14.0850% |

The adjacent-resolution observed slopes for gradient error are about 1.883 and
1.964 before mapping and 0.993 and 1.001 after mapping. Vorticity slopes are
about 1.849 and 1.963 before mapping and 0.963 and 0.987 after mapping. These are
three-point descriptive slopes for this field, time, boundary mask and
reconstruction; they are not an asymptotic order proof. The slower mapped
decrease is consistent with piecewise-constant parent injection: same-parent
child faces carry exactly the injected parent value and add no subcell slope.
It does not isolate or demonstrate a defect in OpenFOAM.

The Gauss operator uses captured face-interpolated `Uf` and oriented face
areas on the mapped mesh; uniform preMap values use centered periodic
differences, equivalent to the midpoint Gauss sum on the orthogonal grid. The
analytic gradient and vorticity are sampled at cell centers. Thus these are
operator-specific discrete reconstruction errors, not certified continuous
maxima or cell-integrated derivative norms. No AMR quality threshold was
preregistered, so no AMR quality PASS/FAIL is assigned. Spectral comparisons
on these nonuniform meshes remain unavailable pending a validated
reconstruction.

## Reproduction and limits

Run the n=64 event with the command in the frozen protocol, then replay:

```sh
CANS_AMR_STAGE_PROTOCOL=protocols/high-gradient-of13-amr-same-run-map-v7-n64.json \
  CANS_AMR_STAGE_EVIDENCE=evidence/of13-amr-same-run-map-v7-n64 \
  CANS_AMR_STAGE_RAW_ARCHIVE=work/of13-amr-same-run-map-v7-n64/archive-recovery/amr-stage-snapshot-n64-review.tar.gz \
  python3 -m tools.analyze_amr_same_run_map
CANS_AMR_STAGE_PROTOCOL=protocols/high-gradient-of13-amr-same-run-map-v7-n64.json \
  CANS_AMR_STAGE_EVIDENCE=evidence/of13-amr-same-run-map-v7-n64 \
  CANS_AMR_STAGE_RAW_ARCHIVE=work/of13-amr-same-run-map-v7-n64/archive-recovery/amr-stage-snapshot-n64-review.tar.gz \
  python3 -m tools.analyze_amr_gauss_gradient
python3 -m tools.compare_amr_resolution_gauss
```

On a clean clone, first reconstruct the compact archive into the local `work/`
path used in the commands above. Run this from the repository root:

```sh
python3 -m tools.reconstruct_amr_published_archive \
  evidence/of13-amr-same-run-map-v7-n64/amr-stage-snapshot-n64-review.tar.gz.zst.parts.json \
  work/of13-amr-same-run-map-v7-n64/archive-recovery/amr-stage-snapshot-n64-review.tar.gz
```

The utility verifies every split-part and compressed-stream hash, then checks
the reconstructed gzip tar size and SHA-256 before writing the destination.

The earlier n=16 v4 run has an explicitly recorded post-hoc protocol-hash
limitation; its raw archive hash is verified and the common-support replay
uses the current protocol separately. All runs are exploratory first-map
events, and the packaged OpenFOAM runtime is not proven source-equivalent as a
whole. The observations establish no continuous-field blow-up, molecular
alignment, phase transition, constitutive-viscosity change, or upstream
implementation defect. No upstream issue is warranted on this evidence.
