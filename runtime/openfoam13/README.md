# OpenFOAM Foundation 13 runtime

Build on a Docker linux/arm64 host:

```sh
docker build --platform linux/arm64 -t concentration-aware-ns:of13 runtime/openfoam13
docker run --rm concentration-aware-ns:of13 foamRun -help
```

The Ubuntu base digest and Foundation DEB SHA256 are pinned. The package index
observed at setup is in `evidence/environment/`. Transitive Ubuntu dependency
versions are resolved at build time and recorded inside `/opt/package-versions.txt`;
this Dockerfile does not claim bit-for-bit rebuild reproducibility. Preserve the
built image ID and package list with actual runs. Source-to-binary equivalence
with the audited Git commit still needs verification.

This is our packaging recipe around an official Foundation package, not an
official OpenFOAM Docker image. No host system packages are installed.

From the repository root, `runtime/openfoam13/run-pilot.sh` generates a fresh
8^3-cell case and launches blockMesh followed by foamRun. NumPy is required for
generation. Run only when `work/of13-pilot` is absent; the generator refuses to
overwrite existing evidence. Coded forcing compiles as a non-root user matching
the host UID. This pilot's completion has not yet been verified; see progress.

The localized high-gradient manufactured profile can be generated without
changing the existing Gaussian case:

```sh
python3 -m tools.openfoam_case work/of13-high-gradient-pilot \
  --n 16 --profile high-gradient --frequency 4
```

The original unrun matrix is preserved as `protocols/high-gradient-of13-v1.json`.
The active successor matrix and quality thresholds are in
`protocols/high-gradient-of13-v2.json`; a reference-only FD2 floor audit added
n=128 so both n=64 and n=128 meet the 5% derivative thresholds even on exact
sampled data. See `evidence/tests/high-gradient-fd2-resolution-floor.json`.
Before solver execution, compile and
compare the `codedFvModel` forcing with the independent symbolic/NumPy
reference using `python3 -m tools.check_high_gradient_openfoam_force`. That
checker requires the pinned local OpenFOAM image and Docker; it tests a mock
mesh/equation, not a PDE run or the live solver's source sign convention.

Run the frozen six-case uniform matrix with
`python3 -m tools.run_high_gradient_openfoam`. It creates a new
`work/of13-high-gradient-v2` tree only after verifying the local image and
records the immutable image ID, source commit, protocol hash, inputs, commands,
logs and diagnostic outputs. It requires a clean committed source tree before
preflight so the recorded revision names the source actually used. Each case
will report standard run acceptance separately from velocity, energy, gradient,
vorticity and shell-spectrum quality. A blind spot is classified as reproduced
only if standard acceptance passes and local quality fails at both n=64 and
n=128, after the exact-reference FD2 floor audit confirms those levels clear
the derivative thresholds. Execution is in progress: the four spatial rows and the `dt=0.0005` temporal addendum are complete;
`dt=0.00025` remains unstarted. The original snapshot remains at
`evidence/of13-high-gradient-v2/manifest.json`, while the additive current
status is `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`;
no matrix-level verdict is available.

If a long temporal case is interrupted after spatial cases have completed, do
not overwrite the original tree. A single-row successor can be run from a clean
committed tree with
`python3 -m tools.run_high_gradient_temporal_case --dt 0.0005 --run-root work/of13-high-gradient-v2-temporal-20260930-dt0005`
(or `--dt 0.00025` and a distinct root). This freezes the same v2 protocol and
image, records the parent-matrix manifest hash, requires all expected time
steps, converged outer loops, `End`, and endpoint fields, and verifies its
archive. A completed addendum is still only one temporal case; it does not
change the six-row matrix to COMPLETE until the other row is also validated
and the other matrix rows are independently checked. The current validated
`dt=0.0005` addendum is under
`evidence/of13-high-gradient-v2-temporal-addendum/`; its run summary explicitly
keeps the overall matrix incomplete.

Generate and run the frozen AMR budget sweep with
`python3 -m tools.run_high_gradient_amr`. It creates a new
`work/of13-high-gradient-amr-v2` tree only after verifying a clean committed
source tree and the local image. The analytic sensor is the prescribed
`chi(y,z)` envelope; the report records observed levels/budgets and explicitly
leaves blocked refinement candidates `UNOBSERVED` if OpenFOAM does not expose
them.

The AMR generator requires `refine_interval >= 2`. In the inspected Foundation
13 startup path, the mesh refiner can query its sensor before the first
`fvModels.correct()` call has registered the coded sensor field. The default
interval leaves one update step to initialize that field before refinement;
this is a source-order safeguard, not an observed solver defect or a completed
runtime validation. The pinned refiner implementation looks up the configured
field by name in
[`refiner_fvMeshTopoChanger.C`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C).
Runtime startup and AMR behavior still require execution against the pinned
image.
