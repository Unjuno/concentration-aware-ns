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

Its frozen spatial/time matrix and quality thresholds are in
`protocols/high-gradient-of13-v1.json`. Before solver execution, compile and
compare the `codedFvModel` forcing with the independent symbolic/NumPy
reference using `python3 -m tools.check_high_gradient_openfoam_force`. That
checker requires the pinned local OpenFOAM image and Docker; it tests a mock
mesh/equation, not a PDE run. The separate
`python3 -m tools.check_high_gradient_openfoam_sign` audit reads the momentum
equation and matrix subtraction code from the exact runtime image to check the
assembled forcing sign. It does not prove source-to-binary equivalence.
