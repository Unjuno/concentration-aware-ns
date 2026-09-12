# Comparative audit of the frozen benchmark matrices

The three completed matrices do not establish a certified instance of standard
acceptance passing while continuous local accuracy fails. They do establish
reproducible discrepancies between aggregate errors, sampled derivative
indicators and solver/training stopping criteria. All conclusions below refer
to the pinned versions and configured smooth manufactured problem, not other
flows or physical singularities.

| Target | Completed comparison | Main observation | Limitation affecting acceptance |
|---|---|---|---|
| OpenFOAM Foundation 13 | Three spatial resolutions; three time steps at n64; AMR and fixed-refined controls | n32 velocity error 1.87001% and energy error 0.201044% meet the 2% aggregate thresholds, while its FD2 gradient peak deficit is about 13.12% | Exact-field FD2/sampling alone has a 13.90% deficit. The discrepancy is not isolated solver error; temporal observed order is about 0.493 |
| SU2 v8.5.0 | Three spatial resolutions; three time steps at n64 | Direct temporal field differences give observed order 0.99916. n64 velocity/energy errors meet 2% thresholds | No case meets velocity, energy and every-step residual checks simultaneously. These runs do not supply an established standard-PASS counterexample |
| PhysicsNeMo v2.2.1 | Three spatial collocation densities; three temporal node counts | Five fixed-budget networks have final velocity errors about 1.80–2.00%; sampled autograd peak errors are about 1% | Density is not discretization convergence; optimization/seed uncertainty and missing preregistered acceptance thresholds remain |

## What the derivative comparisons mean

The smooth reference has analytically derived continuous gradient and vorticity
maxima. Differentiating the sampled reference with the same postprocessor
separates a diagnostic control from the computed-field result. In particular,
OpenFOAM's coarse FD2 peak discrepancy cannot be attributed solely to its PDE
solver. Alternative spectral derivatives reduce that diagnostic contribution,
but their maxima are still evaluated on a finite grid. A small reference-control
error does not bound the derivative error for every computed field.

PhysicsNeMo's autograd avoids a finite-difference stencil but does not locate all
continuous extrema or prove an accurate learned solution. For all three targets,
finite-sample residuals, energy, spectra and peak diagnostics remain distinct
observations. They cannot be substituted for each other in an acceptance claim.
The gate's UNCERTAIN result records those evidentiary gaps; it does not hide the
individual measured threshold violations.

## Classification and reporting

- OpenFOAM: evaluation-method limitation and unresolved adaptive-history error
  attribution. No demonstrated implementation-contract violation; no defect
  report. The approximate maxCells behavior agrees with inspected semantics.
- SU2: source-time contract clarification, with a separate controlled reproducer.
  [Discussion 2890](https://github.com/su2code/SU2/discussions/2890) is the upstream
  report. Both source-time variants in the control were first-order consistent;
  no general inconsistency claim follows from the observed time offset.
- PhysicsNeMo: model/training and evaluation limitations in this configuration.
  Explicit caller-supplied time derivatives agree with the documented API.
  No framework defect demonstrated; the standalone validation benchmark is
  the published contribution.

These are decisions from reproduced evidence. A claim about all affected
industries, light, molecular alignment or phase transitions would exceed it.
The separate OpenAI construction analysis derives an axial material trajectory,
infinitesimal deformation and a nonzero limiting axial viscous-force ratio.
That new consequence is hand-derived and symbolically checked; the independent
kernel acceptance of the original NS target does not verify our extension.

## Evidence and reproduction

Read [OpenFOAM](openfoam-study-v1.md), [SU2](su2-study-v1-interim.md),
[PhysicsNeMo](physicsnemo-study-v1.md), and
[upstream disposition](upstream-disposition.md) for details. Raw archives and
input hashes are in the corresponding evidence directories. Run
`python3 -m tools.replay_published_reports` for the twelve-step report replay;
this does not rerun solvers or train networks. Run
`python -m tools.review_su2_standard` with NumPy/SciPy for the additional SU2
aggregate review, and `python -m tools.check_axis_force` with SymPy 1.14.0 for
our axial-force algebra check. These two checks are not included in that replay.

The remaining public-reproduction and analytic-hypothesis reviews are recorded
in [completion audit](../docs/completion-audit.md). This comparative report
consolidates the available results; it is not certification of missing bounds
or a declaration that the entire project goal is complete.
