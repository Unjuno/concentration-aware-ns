# Concentration-Aware Navier–Stokes Verification Benchmark

An evidence-first audit of whether conventional convergence or validation
criteria can pass while local quantities of interest remain inaccurate.

**Status: active benchmark execution. OpenFOAM and PhysicsNeMo comparison
matrices are archived; the SU2 matrix is running. No general solver defect,
mathematical singularity or real-world hazard is claimed.**

Priority: OpenFOAM Foundation 13, followed by SU2 and NVIDIA PhysicsNeMo.
Use smooth, analytically forced, three-dimensional incompressible manufactured
solutions; compare space/time refinement, local gradients, vorticity and spectra.

- [Goal and completion requirements](GOAL.md)
- [Verification protocol](docs/protocol.md)
- [Source audit and candidate findings](docs/audit.md)
- [Progress](docs/progress.md)
- [Requirement-by-requirement completion audit](docs/completion-audit.md)
- [PhysicsNeMo comparison](reports/physicsnemo-study-v1.md)
- [SU2 time-contract discussion](https://github.com/su2code/SU2/discussions/2890)
- [Analytic interpretation and self-audit](docs/analytic-self-audit.md)
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

## Replay published report generation

After installing requirements.txt, run from the repository root:

```sh
python3 -m tools.replay_published_reports
```

This runs the tests, reconstructs the global-peak and derivative comparisons from
archived fields, reviews and replays completed SU2 diagnostics, rebuilds the
OpenFOAM and PhysicsNeMo gates, and checks every gate artifact hash. Logs and
step exit codes are saved in evidence/report-replay. It does not rerun solvers,
train networks or validate the OpenAI proof. SU2 replay covers completed archives
only; its case count must be checked against the required five-case matrix.
Scientific UNCERTAIN results remain so.

## Contribution and publication

Separate bugs, documented limitations, configuration errors, missing evaluation,
and untested hypotheses. Preserve negative results. An upstream report requires
a minimal reproducer, pinned source revision, environment, raw output and a
duplicate search. Follow the upstream reporting channel. Never mass-post
speculative findings.

Original files use MIT; upstream software retains its own licenses. Do not copy
upstream source into this repository without preserving its applicable terms.

The pinned OpenAI Navier–Stokes challenge passed the recorded independent check;
see [verification result and scope](reports/openai-ns-independent-verification.md).
This result is separate from the report replay and numerical benchmark gates.
