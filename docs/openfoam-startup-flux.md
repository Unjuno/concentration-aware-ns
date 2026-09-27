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

A dedicated build command now removes the dependency on a live solver container:

```sh
python3 -m tools.build_openfoam_startup_probe
python3 -m tools.run_openfoam_startup_probe
python3 -m tools.check_openfoam_startup_probe
```

Use a fresh checkout/work directory with the baseline work cases restored and
the exact locally available image ID recorded in build-result.json. Existing
probe work/evidence directories are deliberately rejected. The build tool
extracts source from a newly created, unstarted container of that exact image,
removes that temporary container, prepares source on the host, then builds
without network access. It does not fall back to the current mutable image tag.

A fresh build in `work/of13-startup-probe-rebuild` completed with exit zero and
produced a byte-identical diagnostic executable. The replay commands, build log
and hash comparison are archived as `rebuild-*` files. This is reproducibility
within the same recorded runtime image, not a rebuild of OpenFOAM itself from
independently fetched sources or a cross-platform reproducibility guarantee.

## Why the cell-divergence diagnostic can remain nonzero

In the leading startup model, pressure impulse pi solves L_h pi = D_c U0,
where L_h is the nearest-neighbor face-flux Laplacian. The cell update is
U*=U0-G_c pi, with centered cell gradient G_c. On a periodic uniform mesh,
L_h has symbol -4 sum(sin(theta_j/2)^2)/dx², whereas D_c G_c has symbol
-sum(sin(theta_j)^2)/dx². Therefore the residual cell divergence has multiplier

```
D_c U* = [sum sin(theta_j/2)^4 / sum sin(theta_j/2)^2] D_c U0
```

mode by mode away from the zero mode. The multiplier is between zero and one,
but generally nonzero. This follows from sin(theta)^2=4s(1-s), with
s=sin(theta/2)^2. It is an operator distinction, not a failed pressure solve.
It gives an L2 contraction of this divergence for the model; it does not imply
pointwise contraction at every cell or apply automatically to the full solver.

The n=64 initial field gives model-corrected maximum cell divergence 0.00291994
versus 0.0567239 initially, while corrected face-flux divergence is below
4.6e-16. Direct real-space cell correction and the residual-symbol formula agree
to 3.8e-15. These quantities are recorded in the `operator_review` portion of
`evidence/of13-startup-time-v1/poisson-model.json`. This is still the leading
startup model, not a newly observed full-solver face-flux result. It explains
why the two diagnostics must be separated in the acceptance analysis.
