# OpenFOAM Foundation 13 runtime and reproduction

This is the benchmark's Docker packaging recipe for the official
OpenFOAM Foundation Debian package. It is not an official OpenFOAM image.
The solver is Foundation 13 (`openfoam13` package `20260624`, arm64); source
headers/package identify GPL-3.0-or-later. This audit did not establish
source-to-binary equivalence between the installed Debian package and the
separately inspected upstream Git tree.

## Recorded runtime provenance

The completed v2 matrix used Linux/arm64 image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`.
The recipe pins the Ubuntu 24.04 base image by digest and the Foundation DEB
URL and SHA256. Its build log, installed package-version inventory and package
index are retained at:

- `evidence/environment/openfoam-build.log`
- `evidence/environment/runtime-packages.txt`
- `evidence/environment/openfoam-packages-arm64.txt`

The runtime package inventory SHA256 is
`5d49d34475cb8a55d605f78892160d512534881b32f79dfbd8580a945ccb9d23`; the
Foundation DEB SHA256 is
`6da0f6460fbc33c8995cbc97caba52c6cb0342f52ed02ff57530d9d62e9ef360`.
The Ubuntu apt indexes used during image construction were not snapshot-pinned.
Rebuilding later can therefore produce a different dependency set and image
ID. Compare the resulting package inventory and image ID before treating a new
run as an exact runtime reproduction. Per-run harness commit, image ID,
Docker CLI and protocol hashes are in the corresponding run manifests.

## Reproduce the uniform matrix

Run on a Linux/arm64 Docker host. Install Python verification dependencies
using `requirements-verification-locked.txt`, build the runtime image, then
check its image ID and package inventory against the values above:

```sh
python3 -m pip install -r requirements-verification-locked.txt
docker build --platform linux/arm64 -t concentration-aware-ns:of13 runtime/openfoam13
docker image inspect concentration-aware-ns:of13 --format '{{.Id}} {{.Os}}/{{.Architecture}}'
docker run --rm --entrypoint cat concentration-aware-ns:of13 /opt/package-versions.txt
```

The completed run used harness commit
`0e0288f98209f856931352ebfa5dad0f1aad0014`, frozen protocol
`protocols/high-gradient-of13-v2.json`, and six rows: n=16, 32, 64, 128 at
`dt=0.001`, plus n=64 at `dt=0.0005` and `0.00025`. To run a fresh full
matrix from that clean source revision, check out that commit in this same
repository, confirm the working tree is clean, and run:

```sh
python3 -m tools.run_high_gradient_openfoam
```

The runner refuses to overwrite its output directory. Set
`CANS_OF13_RUN_ROOT` to a new path for another run. It records input hashes,
commands, container logs, completion status and diagnostics. The already
published results and cross-run status are in
`evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`; the older
`manifest.json` is intentionally retained as a historical snapshot and marks
the later temporal rows incomplete.

## Reproduce the AMR and fixed-final-mesh controls

The three AMR runs used harness commit
`265611cd160a7e139b6950c918e6dc1d90056d97` and the same v2 protocol/image.
From a clean checkout of that revision and a new work root:

```sh
CANS_OF13_AMR_RUN_ROOT=work/of13-high-gradient-amr-v2-20260930 python3 -m tools.run_high_gradient_amr
```

Then run the two fixed-final-mesh controls, which require the AMR outputs above:

```sh
CANS_REMAP_PROTOCOL=protocols/high-gradient-of13-remap-control-v2.json CANS_OF13_REMAP_RUN_ROOT=work/of13-high-gradient-remap-control-v2-20260930e python3 -m tools.run_remap_control
```

Both runners refuse to overwrite existing work roots. The raw adaptive and
fixed-mesh cases are published as verified tarballs under
`evidence/of13-high-gradient-amr-v2-2026-09-30/` and
`evidence/of13-high-gradient-remap-control-v2-2026-09-30/`. Replay their
archive/tree integrity checks without a solver using:

```sh
python3 -m tools.verify_openfoam_amr_archives
```

The AMR pilot found that final cell counts can exceed nominal `maxCells` at
adaptation synchronization points. The run did not expose blocked candidate
counts, and nonuniform-grid spectra lack a validated reconstruction; AMR
quality remains `UNCERTAIN`. See
`reports/solver-matrix-coverage-2026-09-30.md` for results and limitations.

## What rebuild and replay do not prove

The recorded archives let a third party replay all published diagnostics
without rerunning OpenFOAM. A new run on a rebuilt image is a fresh reproduction
unless the image ID and package inventory match the recorded environment.
Neither the archived results nor a repeated run proves a general solver defect,
mathematical blow-up, molecular alignment, constitutive-viscosity change or
physical hazard.

## Reproduce the first-refinement stage snapshots

`protocols/high-gradient-of13-amr-stage-snapshot-v3.json` defines a diagnostic
that captures cell `U/p` and face `phi/Uf` immediately after topology mapping,
after `correctPhi`, before and after pressure correction, and after the full
PIMPLE step. The instrumented module is generated from the pinned source tree
without modifying that tree, then built against the recorded arm64 runtime
image. The instrumentation only writes snapshots; it does not change equation
assembly. The runner records loader evidence that the instrumented module was
used and preserves a fresh case archive under
`evidence/of13-amr-stage-snapshot-v3/`. The first v1 attempt completed the
solver but failed the capture-count gate: `topoChanged()` had already reset at
the mapped callback, and unrestricted pressure hooks wrote once per PIMPLE
iteration. Its raw case and logs remain preserved under
`work/of13-amr-stage-snapshot-v1/`; v2 removes the reset-sensitive gate and
captures the first and final outer iterations explicitly.

The v2 attempt also completed but exposed a time-ordering detail: `preSolve()`
and its mapping callback run at `t=0.002`, before `foamRun` advances the clock;
later callbacks run at `t=0.003`. The v3 protocol records this explicitly.
Both earlier attempts remain preserved in their versioned work directories.

With a clean checkout, the pinned Foundation source clone available at
`work/openfoam13-source-20260624`, and the recorded Docker image installed, run
`python3 -m tools.run_amr_stage_snapshot`. The runner refuses to overwrite its
work or evidence paths. Stage attribution is accepted only if the final fields
are later verified against the frozen uninstrumented first-refinement control;
the runner's stage-capture status alone does not assert noninterference. The
packaged Foundation binary and inspected source are still not proven
equivalent, and this single n=16 mechanism probe is not an AMR convergence or
defect verdict.
