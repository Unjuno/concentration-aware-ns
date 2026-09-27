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
