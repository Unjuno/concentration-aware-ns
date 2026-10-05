# OpenFOAM stress interpolation and viscosity-jump scope audit

Date: 2026-10-03 08:24 UTC

Target: OpenFOAM Foundation 13; existing single-phase MMS remains pinned at `nu=0.01`
Disposition: related existing issue; no new upstream report

## What the upstream report covers

OpenFOAM Foundation issue [#2](https://github.com/OpenFOAM/OpenFOAM-13/issues/2)
reports large version-to-version differences and instability in `incompressibleVoF`
when phase viscosities differ substantially. The report identifies the
transpose-gradient stress-correction path, provides a serial squeeze-flow
reproducer, and links the implementation change
[`6592798`](https://github.com/OpenFOAM/OpenFOAM-13/commit/6592798ca0704aa6eaaaaf74ea3cc6a9553317dc).
That commit's stated aim is to make the explicit surface stress, momentum
matrix, wall-shear-stress and force-object evaluations consistent. The issue
is open and has no maintainer response in the current GitHub record.

This is directly adjacent to viscosity-jump and large-gradient numerics, but
it is a two-phase interface formulation. It is distinct from this benchmark's
smooth, single-phase manufactured field with constant viscosity. The attached
case was not run here, and the issue is not independently confirmed by this
audit.

## Exact interpolation identity

For two adjacent cell values and one shared linear face weight,

`I_w(f) = w f_P + (1-w) f_N`,

the generic product/interpolation difference is exactly

`I_w(a G) - I_w(a) I_w(G) = w(1-w) (a_P-a_N)(G_P-G_N)`.

The identity applies componentwise when `a` is a scalar coefficient such as
`alpha*rho*nuEff` and `G` is a tensor contribution such as a transpose-gradient
stress term, provided both factors use the same interpolation weights. A face
contraction by a fixed face-area vector preserves the identity componentwise.
The symbolic checker verifies the identity and its degeneracies. For smooth
affine `a` and `G`, the defect is exactly `w(1-w) h^2 a' G'`; it is second
order in cell spacing. For finite jumps in both factors, the face defect can
remain finite as the face approaches an unresolved interface.

That local algebra explains why changing the order of interpolation can alter
a discrete stress flux near a coefficient/gradient jump. It does not establish
that OpenFOAM's complete `fvc::dotInterpolate` path is algebraically identical
to the generic same-weight model on every mesh or interpolation scheme. Nor
does a nonzero face defect alone determine the assembled momentum solution,
convergence, or which formulation is preferable; the linked change explicitly
seeks consistency among stress consumers.

## Benchmark implication

With constant `nu`, the coefficient-jump factor is zero in the current frozen
MMS, so this mechanism does not explain its local concentration results. A
separate optional interface-viscosity benchmark could compare stress fluxes,
velocity-gradient error and interface-local refinement under a manufactured
piecewise-viscosity field. It should be reported separately from the smooth
MMS and judged against its own conservation, interface and refinement gates.
The current issue already tracks the reported version difference, so no
duplicate upstream report is appropriate.

This numerical discretization question is not evidence that physical viscosity
decreases as a body speeds up, that molecules align, or that the OpenAI
continuum construction transfers to matter. The main solver-quality verdict
and the particle-scale hypothesis remain unchanged.

The exact symbolic result is in
[`openfoam-stress-interpolation-covariance-2026-10-03.json`](../evidence/tests/openfoam-stress-interpolation-covariance-2026-10-03.json).

A subsequent [pinned-source and conservative-assembly audit](openfoam-stress-operator-source-link-2026-10-03.md)
connects the identity to the uncorrected linear explicit-correction path and
records extra terms for field-specific/corrected schemes. It adds exact
global-cancellation/local-norm controls, while still not reproducing the
upstream issue or the full momentum solution.
