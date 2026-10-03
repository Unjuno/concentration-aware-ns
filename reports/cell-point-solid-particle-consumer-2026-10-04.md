# Pinned solid-particle carrier interpolation — 2026-10-04

A concrete Foundation 13 consumer uses the same named velocity interpolator as the captured benchmark. At source pin `18870c24d21c6b982e2cdec27b2f59738cca5f90`, [solidParticleCloud.C](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/lagrangian/solidParticle/solidParticleCloud.C) constructs `interpolationCellPoint<vector>` for the carrier velocity U, and scalar interpolators for density and kinematic viscosity. This identifies a source-level application of the interpolation family; it does not establish that this cloud is present in the archived benchmark case or execute particles.

[solidParticle.C](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/lagrangian/solidParticle/solidParticle.C) obtains Uc through the explicit barycentric/tet overload. It tracks with the particle's own U_, then updates that velocity through drag and buoyancy. The supplied interpolator is carried by [solidParticleI.H](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/lagrangian/solidParticle/solidParticleI.H). All three files match pinned Git blobs byte for byte; source hashes, immutable links and exact line locations are stored in `evidence/cell-point-particle-consumer-v1`.

The source update has the scalar/component form

    U_new = (U_old + dt*(Dc*Uc + body))/(1 + dt*Dc).

Holding Dc and body fixed, its carrier-velocity sensitivity is

    dU_new/dUc = dt*Dc/(1 + dt*Dc).

For nonnegative finite dt and Dc this lies in [0,1). SymPy verifies the derivative and twenty exact rational controls. This is a conditional algebraic sensitivity, not an actual particle-error bound: the implemented Dc depends on relative speed through Reynolds number, diameter, viscosity and densities. Moving geometry, changing Dc, tracking and boundary interactions are not frozen in the real algorithm.

Consequently the earlier nonzero divergence of an idealized carrier interpolant cannot be substituted directly for a solid-particle flow-map volume rate. The particles are not passive material elements advected by Uc. Likewise d_ is a solid-particle diameter and nu is read from a carrier field; this model does not derive fluid viscosity from molecular positions or particle alignment. The synthetic benchmark's velocity-gradient lower bounds do not quantify trajectory errors in this unexecuted cloud.

Classification: source-level consumer identified / bounded conditional sensitivity. No new implementation defect or violated divergence-preservation contract is demonstrated, and no upstream issue is posted. A proper next experiment would first freeze particle properties, carrier-field provenance, initial positions/velocities, gravity, boundaries and time stepping, then compare matched analytic/interpolated carrier inputs with actual tracking. That experiment is not performed here and its scope must not be substituted for existing solver or proof results.

Reproduce with locked verification dependencies and `python -m tools.audit_cell_point_particle_consumer --source PINNED_UPSTREAM_CHECKOUT --output NEW_DIRECTORY --source-commit ANALYSIS_COMMIT`. Analysis source is `39de0fe` (full SHA in the receipt). A selected own-tools export reproduces the complete JSON byte for byte while intentionally retaining read access to the explicitly supplied upstream Git checkout. This is not the earlier process/network/Git-isolated replay and is not a compiled cloud validation. Compilation of the Python tool, source identity/signature checks, exact symbolic controls and `git diff --check` pass. The full goal remains active.

Preceding publication 910485bb subsequently passes hosted CI run 37156115323, including all 375 tests, v2 analytic equality and the rational scalar chain. Executed merge/source closures match. These are checks of the preceding benchmark/replayers, not a compiled solid-particle experiment. Receipts are in `evidence/affine-divergence-hosted-ci-v1`.
