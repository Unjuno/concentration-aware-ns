# OpenFOAM Foundation 14 compatibility probe (2026-10-02)

## Result

A single `n=64`, `dt=0.001`, `endTime=0.05` case completed with Foundation 14
package `20260724` on Linux/arm64. All 50 time steps reached the configured
PIMPLE convergence criterion (maximum five outer correctors), and the standard
acceptance gate passed. The local sampled-quality gate also passed:

- velocity relative L2 error: 0.4781% (2% limit)
- cell-sampled gradient peak relative error: 2.6404% (5% limit)
- cell-sampled vorticity peak relative error: 2.3488% (5% limit)
- energy sample error: 0.02419% (2% limit)
- shell-spectrum relative L1 error: 0.02419% (5% limit)

These values are exactly equal to the published Foundation 13 `n=64`,
`dt=0.001` diagnostic values. The endpoint ASCII fields `U`, `p`, `phi`, `C`,
`Ccx`, `Ccy`, and `Ccz` are also byte-identical after normalizing only the
OpenFOAM banner's version number. Their raw hashes differ because the header
records version 13 versus 14. This exact one-case match is a compatibility
observation, not evidence of version-wide equivalence.

## Correct solver and source comparison

The archived case's `system/controlDict` selects `incompressibleFluid`, not
`isothermalFluid`. Although the Foundation v14 release notes mention
improvements to `isothermalFluid`, those changes are not the direct solver
path tested here.

A source comparison of Foundation 13 commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90` with the Foundation 14 package tag
`20260724` found the `incompressibleFluid` module refactored from
`fluidSolver` to `basicFluidSolver`, explicit field dimensions added, and MRF
handling switched to `MRFZones`. Its `moveMesh.C` also removes the explicit
`MRF.update()` call and checks `mesh.poly().topoChanged()`. This benchmark uses
a static mesh and contains no MRF configuration, so those changes are not
exercised by the probe. `correctPressure.C` is unchanged between those two
module snapshots. The one-case equality is consistent with the paths this
case exercises; it is not a test of the changed MRF or moving-mesh behavior.

## Limits and disposition

This probe covers one spatial resolution and one time step. The continuous
full-gradient maximum is not certified; reported local extrema are sampled at
cell centers. It does not establish a general solver defect, singularity,
molecular alignment, or a constitutive-viscosity change. No upstream issue is
warranted by this result. A separate v14 multi-resolution/time-step study
remains future work. The existing Foundation 13 six-case result and its
`NOT_OBSERVED` classification remain unchanged.

The exact run inputs, command, raw output archive, runtime inventory, source
comparison summary, and reproduction harness are under
`evidence/of14-high-gradient-v1/`; the image recipe is
`runtime/openfoam14/Dockerfile`.
