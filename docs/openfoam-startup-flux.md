# Initial flux and pressure correction in the running OpenFOAM image

The source installed in the image used for the iteration-sensitivity experiment
connects the initial arithmetic-flux diagnostic to an actual constructor path.
`incompressibleFluid.C` constructs phi with READ_IF_PRESENT and the default
`linearInterpolate(U_) & mesh.Sf()`. No `0/phi` file exists in the copied case.
For its uniform orthogonal mesh and linear arithmetic face interpolation, this
is the flux whose discrete divergence was measured in
`evidence/tests/openfoam-initial-flux.json`.

The constructor body shown here validates momentum transport and computes the
Courant number; it does not itself perform a pressure projection. `prePredictor`
is empty. This limited inspection is not proof about every initialization hook
or base-class operation. A runtime snapshot before the first predictor is still
needed to verify the full lifecycle and numerical phi values directly.

`momentumPredictor.C` assembles ddt(U)+div(phi,U), momentum transport and the
manufactured source. `correctPressure.C` constructs phiHbyA from flux(HbyA)
plus interpolate(rAU)*ddtCorr(U,phi,Uf), solves a pressure Laplacian equation,
and updates phi and U separately:

```
phi = phiHbyA - pEqn.flux()
U = HbyA - rAtU*grad(p)
```

Consequently corrected face-flux continuity is not identical to centered
finite-difference divergence of saved cell-centered U. A nonzero FD2 divergence
must not be reported as failure of the solver's face-flux continuity equation.
The correction and its old-time flux term provide a concrete startup path to
investigate, but do not yet explain the observed temporal difference order.

The installed file hashes, line excerpts and running-image identity are recorded
in `evidence/tests/openfoam-startup-source.json`. Image identity was checked
against the experiment provenance. This audits installed source, not an
independent source-to-binary rebuild. No upstream defect is claimed.

## Constructor-only runtime observation

A diagnostic launcher now instantiates the installed incompressibleFluid solver,
writes registered phi and fvc::div(phi), and returns before setDeltaT or the
time loop. It links the installed solver libraries and does not alter their
constructor. The copied baseline cases have no 0/phi; their U inputs remain
byte-identical. No positive-time output directory is created.

At n=16,32,64, observed divergence agrees cellwise with the independent
arithmetic-flux calculation to 1.52e-14, 5.68e-14 and 1.34e-13 respectively,
below the preregistered absolute tolerance 1e-11. Thus the initially uncorrected
flux is now observed in the runtime constructor path, rather than merely
inferred from source. Later preSolve hooks are outside this observation.

The probe protocol, source preparation, execution and comparison are
`protocols/of13-startup-probe-v1.json`, `runtime/of13-startup-probe/prepare.py`,
`tools/run_openfoam_startup_probe.py` and `tools/check_openfoam_startup_probe.py`.
Build the copied launcher with wmake in the recorded image, mounting the probe
workspace at /probe; Make/files places startupProbe there. Source preparation
takes the installed foamRun directory and output app directory as arguments.
The image has no Python, so preparation runs on the host. The first failed
Python-in-container attempt and successful build are distinguished in the
build-result record. Three complete case archives, build log, image/executable
identities and comparison live in `evidence/of13-startup-probe-v1`.

This establishes an initialization mismatch between continuum solenoidality
and the solver's initial discrete flux. It still does not establish a solver
bug or explain the anomalous temporal order; a controlled treatment of the
startup projection would be needed for that attribution.
