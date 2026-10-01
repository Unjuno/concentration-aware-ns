# Concentration-Aware Navier–Stokes Verification Benchmark

An evidence-first audit of whether conventional convergence or validation
criteria can pass while local quantities of interest remain inaccurate.

**Status: all three comparison matrices are archived; final evidence review
is ongoing. No general solver defect,
mathematical singularity or real-world hazard is claimed.**

Priority: OpenFOAM Foundation 13, followed by SU2 and NVIDIA PhysicsNeMo.
Use smooth, analytically forced, three-dimensional incompressible manufactured
solutions; compare space/time refinement, local gradients, vorticity and spectra.

- [Goal and completion requirements](GOAL.md)
- [Verification protocol](docs/protocol.md)
- [Source audit and candidate findings](docs/audit.md)
- [Progress](docs/progress.md)
- [Requirement-by-requirement completion audit](docs/completion-audit.md)
- [Three-target comparative audit](reports/comparative-audit.md)
- [Cross-solver matrix coverage, AMR upper-state and upstream disposition](reports/solver-matrix-coverage-2026-09-30.md)
- [PhysicsNeMo comparison](reports/physicsnemo-study-v1.md)
- [SU2 time-contract discussion](https://github.com/su2code/SU2/discussions/2890)
- [Analytic interpretation and self-audit](docs/analytic-self-audit.md)
- [Flat-but-active analytic-forcing bridge to the OpenAI construction](reports/openai-analytic-forcing-bridge-2026-10-01.md)
- [OpenAI material trajectory and viscous-force analysis](docs/openai-core-material-trajectory.md)
- [Axis-tube concentration versus bounded-position probability](docs/linearized-axis-tube-concentration.md)
- [OpenAI natural-core deformation analysis](docs/openai-core-deformation.md)
- [Exact counterexample: alignment does not imply reduced viscosity](docs/affine-alignment-viscosity-counterexample.md)
- [Burgers vortex: alignment with nonzero viscous balance](docs/burgers-vortex-alignment-viscous-balance.md)
- [Burgers vortex tracer-position probabilities](docs/burgers-vortex-position-probability.md)
- [Exact global reference peaks](docs/reference-global-peaks.md)
- [FD2 diagnostic decomposition](reports/peak-diagnostic-decomposition.md)
- [Independent spectral derivative comparison](reports/openfoam-spectral-gradient.md)
- [SU2 FD2 and spectral derivative comparison](reports/su2-spectral-gradient.md)
- [Upstream reporting decisions](reports/upstream-disposition.md)

## Acceptance report checker

Python 3.10+. The report checker needs no third-party dependencies; the analytic
reference and its tests need NumPy.

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 tools/acceptance_gate.py examples/unverified.json
```

The example intentionally returns `UNCERTAIN` (exit 2). The checker consumes
evidence reports with hashed artifact references and error intervals; it does not
run a solver or determine whether an evidence review is true. See
[gate v2](docs/acceptance-gate-v2.md). It is triage, not certification.

`tools/reference.py` implements the analytic velocity, velocity gradient,
vorticity and forcing. Its tests check periodicity, divergence and second-order
convergence of a separate finite-difference reconstruction of the PDE forcing.
These checks validate formula consistency; they do not constitute solver runs.

The affine counterexample uses an exact unbounded-domain Navier–Stokes solution
to test the logical inference from material-line alignment to reduced viscosity.
Its SymPy checker and negative controls are reproducible with
`python -m tools.check_affine_alignment_counterexample`; this does not infer
molecular behavior or replace component-wise term analysis of the selected
construction.

The Burgers-vortex calculation is a stronger analytical countercheck: its
nonzero azimuthal viscous diffusion exactly balances azimuthal advection even
while the axis deformation aligns infinitesimal directions. Reproduce it with
`python -m tools.check_burgers_vortex_balance`.

The exact passive-tracer probability check further distinguishes localization
relative to an infinite axis from probability inside a fixed bounded volume;
reproduce it with `python -m tools.check_burgers_vortex_tracer_probability`.

## Continuous integration

Pull requests run the Python verification suite on Python 3.12 through
`.github/workflows/python-verification.yml`. This covers analytic formulas,
acceptance gates, archive/reader logic and generated case inputs. It does not
launch OpenFOAM, SU2 or PhysicsNeMo, and cannot turn an unrun solver matrix into
a PASS.

## Replay published report generation

After installing requirements-verification.txt, run from the repository root:

```sh
python3 -m tools.replay_published_reports
```

This runs the tests, reconstructs the global-peak and derivative comparisons from
archived fields, reviews and replays completed SU2 diagnostics and the
Dirichlet boundary-time pilot, reproduces the specific restart-history mismatch,
checks OpenFOAM's six-case fixed/time-step archives and AMR archive tree hashes,
rechecks all five SU2 cases and the five PhysicsNeMo sampled-derivative
checkpoint/evaluation pairs, rebuilds all three acceptance reports, and checks
the analytic identities and every gate artifact hash. Each step records both
the exact interpreter argv and a portable `python3` replay command. Logs and
step exit codes are saved in evidence/report-replay. It does not rerun solvers,
train networks or validate the OpenAI proof. Scientific `UNCERTAIN` results
remain so.
Scientific UNCERTAIN results remain so.

## Contribution and publication

Separate bugs, documented limitations, configuration errors, missing evaluation,
and untested hypotheses. Preserve negative results. An upstream report requires
a minimal reproducer, pinned source revision, environment, raw output and a
duplicate search. Follow the upstream reporting channel. Never mass-post
speculative findings.

Original files use MIT; upstream software retains its own licenses. Do not copy
upstream source into this repository without preserving its applicable terms.
The optional verification dependency `python-flint==0.9.0` is used for the
experimental Arb interval audit. The package metadata reports MIT and
LGPL-3.0-or-later components; its maintainers describe Python-FLINT as MIT and
bundled FLINT/Arb as LGPL-2.1-or-later. This repository imports the package for
verification and does not redistribute its binary wheel.

The pinned OpenAI Navier–Stokes challenge passed the recorded independent check;
see [verification result and scope](reports/openai-ns-independent-verification.md).
This result is separate from the report replay and numerical benchmark gates.

## Additional analytic and aggregate checks

Install `requirements-verification.txt` in a separate Python environment, then run:

```sh
python -m tools.review_su2_standard
python -m tools.check_axis_force
python -m tools.check_axis_dissipation
python -m tools.check_axis_deformation
python -m tools.check_axis_packet_bound
python -m tools.check_packet_radius_scaling
python -m tools.check_particle_position_probability
```

These checks are separate from the eighteen-step report and exact-algebra replay. The force and
dissipation checks verify symbolic algebra, not the complete source-hypothesis
chain or molecular applicability. The particle-probability check assumes
isotropic infinitesimal directions; its Gaussian position statistics are a
global affine tangent-map toy model, not a finite-packet prediction for the
nonlinear flow. The aggregate review does not
certify continuous numerical-field energy.

The current [analytic connection](docs/axis-flow-derivative.md) distinguishes
Lean-checked component lemmas from the classical nonlinear-flow argument.
The [comparative audit](reports/comparative-audit.md) includes the separate SU2
BDF2 reproducer; the eleven localized acceptance verdicts remain UNCERTAIN.

The tracked-only export at commit `a9ff4ab` was also checked in a newly
created virtual environment: dependency installation, the twelve-step replay
and all three additional checks succeeded. See
[evidence](evidence/fresh-environment-check.json) for exact versions and logs.
This validates postprocessing on the recorded host; it does not rerun the
PDE solvers or independently prove the new analytic consequence.


The [2026-09-27 clean-export replay](evidence/clean-export-2026-09-27/README.md)
tests fixed commit `60302db` with thirteen replay steps and five additional
checks in a fresh environment. All commands succeeded, but strict byte equality
failed in six of 66 compared files: NumPy version metadata and dependent hashes
changed. Inspected numeric results and verdicts were unchanged. The failed
strict result and original logs are preserved rather than relabeled as PASS.


For byte-level reproduction of the recorded Python postprocessing baseline,
use `requirements-verification-locked.txt`. The ordinary verification requirements
retain their supported NumPy range. A tracked-only, fresh-venv check is:

```sh
python3 -m tools.check_clean_export --locked --destination work/clean-export-locked
```

The fixed-commit check at `5b8e305` passes all 75 compared report/test files
unchanged; see `evidence/clean-export-2026-09-27-locked/README.md`. Its scope is
same-host Python postprocessing, not solver, training or Lean reproduction.
