# Research update — 2026-10-02

This note records a source refresh and two adjacent research tracks. It does not
change any solver verdict or claim a new defect in OpenFOAM, SU2 or PhysicsNeMo.

## OpenAI construction and the user's geometric interpretation

The current public [OpenAI/NavierStokesAndEuler repository](https://github.com/openai/NavierStokesAndEuler)
describes Lean formalizations accompanying the Navier–Stokes and Euler papers.
OpenAI's [announcement](https://openai.com/index/navier-stokes-solution/) and
[Navier–Stokes paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)
state a forced, incompressible continuum result: smooth forcing and zero initial
velocity, bounded kinetic energy, and unbounded velocity as a finite terminal
time is approached. The paper's inner-core description does contain a
geometrically slenderizing vortex: its radial and axial scales behave as
`(1-t)^(1/2)` and `(1-t)^(1/2-h)`, respectively, so their ratio tends to zero.
This is a real anisotropic concentration of a continuum-flow region and may be
the geometric feature behind the user's intuition.

That statement is not a molecular trajectory model. Slenderness of the core or
alignment of infinitesimal separation directions does not establish alignment
of molecules, certainty of absolute particle positions, a phase transition, or
a change in the constitutive viscosity. The existing conditional analysis is
careful about this distinction in
[`docs/particle-position-probability.md`](particle-position-probability.md)
and [`docs/axis-flow-derivative.md`](axis-flow-derivative.md). The previous
position-density result is a toy affine ensemble; its finite-packet transfer
still lacks the required neighborhood and derivative bounds.

The ChatGPT share URL supplied in the conversation timed out when fetched on
2026-10-02. No claims or instructions from that page were used. Its contents
remain unverified.

## Adjacent result: fluid models of light

Treating light collectively as a fluid is an established, technically real
research area, rather than a new consequence of the Navier–Stokes blow-up
construction. In photon-fluid systems, optical nonlinearities or cavity
light–matter coupling provide effective interactions; under a paraxial or
cavity model, the field equation can map to Gross–Pitaevskii-like hydrodynamics.
For a bulk Kerr medium, the propagation coordinate plays the role of time, and
the commonly used model is conservative and includes optical diffraction
(quantum pressure). Those assumptions differ from three-dimensional viscous
Navier–Stokes in physical time. A many-photon fluid description can therefore
be useful without asserting that individual photons literally form a
molecular fluid.

Experiments have reported suppressed scattering/drag in photon-fluid
superfluid regimes. This resembles the user's “viscous effect suddenly weakens”
intuition at a broad phenomenological level, but the cited mechanism is a
nonlinear-wave superfluid criterion and collective optical interaction. It is
not evidence that the OpenAI Navier–Stokes construction reduces material
viscosity or that molecular alignment causes such suppression. A viable bridge
would need a specified optical platform, governing equation, mapping of
parameters and observables, and a test that separates diffraction, nonlinearity,
loss and any effective dissipation.

The analytic crosswalk derives the Madelung equations and shows that the
paraxial optical model is compressible, irrotational, two-dimensional in space,
and includes diffraction/quantum pressure, with propagation distance as its
evolution coordinate. It also separates infinitesimal axis alignment from
finite-packet transfer and absolute-position certainty; see
[`reports/analytic-hypothesis-crosswalk-2026-10-02.md`](../reports/analytic-hypothesis-crosswalk-2026-10-02.md).

Sources: [Carusotto & Ciuti, *Quantum fluids of light*, Rev. Mod. Phys. (2013)](https://doi.org/10.1103/RevModPhys.85.299);
[Michel et al., *Superfluid light in bulk nonlinear media*, Proc. R. Soc. A (2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4123774/);
[Vocke et al., experimental superfluid motion and drag-force cancellation (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5974130/).

## Adjacent result: SU2 source-time semantics

The user's [SU2 Discussion #2890](https://github.com/su2code/SU2/discussions/2890)
now includes a BDF2 follow-up. The associated reproducible evidence and bounded
interpretation are already in [`reports/su2-bdf2-source-time.md`](../reports/su2-bdf2-source-time.md).
In the pinned SU2 v8.5.0 single-zone control, a time-dependent uniform MMS
source evaluated at the stored/old time produces observed first-order temporal
error despite small reported residuals; a one-line target-time intervention
recovers approximately second-order behavior for that control. This is a
concrete time-integration and verification-contract issue, not a concentration
finding or evidence against all SU2 source consumers. The source-time fix is
not general until target time, output time, restart, boundary and other
consumers are audited.

## Benchmark-framework developments

NVIDIA's 2026 [PhysicsNeMo CFD module](https://nvidia.github.io/physicsnemo/blog/2026/05/29/physicsnemo-cfd/)
adds a config-driven model-evaluation workflow and promotes field, integral and
physics-aware diagnostics plus edge-case challenge cases. This provides a
practical integration target for the later surrogate-model phase. It also
means that “mean loss can miss physics” is not by itself a novel claim; any
upstream contribution should demonstrate a specific gap in a pinned workflow
with a reproducible challenge and measured result.

## Implications for this repository

- A local review found that the first high-gradient AMR sensor implementation
  did not equal its documented reference quantity. Since
  `u_y=-exp(-t)*chi*cos(N*x)/N`, the selected sensor `(partial_x u_y)^2` is
  `exp(-2t)*chi^2*sin(N*x)^2`; the generator used only one decay/envelope
  factor. The source expression and metadata are now corrected, and a regression
  check compares the expression with the analytic derivative. The earlier
  Gaussian AMR runs did not use the incorrect high-gradient sensor. This was a
  benchmark-generator defect, not an OpenFOAM finding. The corrected
  high-gradient AMR cases and their adverse but unresolved errors are recorded
  in [`reports/of13-high-gradient-amr-v1.md`](../reports/of13-high-gradient-amr-v1.md).
- Keep the smooth high-gradient MMS as a solver-verification stress case. It
  does not reproduce the OpenAI witness or test its singularity claim. The
  OpenFOAM Foundation 13 spatial, temporal and AMR matrices now have completed
  runs. Source-backed standard acceptance passes the completed cases, while the
  AMR velocity L2 metric fails its frozen threshold; the discrepancy is scoped
  to this coarse-base matrix and needs a better-controlled interpolation study.
- Keep the OpenAI source audit, the conditional material-trajectory calculation,
  and the optical-fluid track separate, with explicit model-transfer steps.
- Do not send an upstream defect report based on these adjacent results alone.
- Review the frozen OpenFOAM v1 peak metrics before interpreting any pilot run
  as a quality verdict.

The symbolic conversion audit is executable as
`python -m tools.check_optical_madelung`; its equations and scope are recorded in
`evidence/tests/optical-madelung.json`. It checks the 2D continuity and
compressible momentum identities from the assumed paraxial NLSE, including the
quantum-pressure term. It does not derive the paraxial approximation from
Maxwell equations or test an optical device.
