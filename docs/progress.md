# Progress

## 2026-09-09 — repository bootstrap

- User authorized repository creation after the initial read-only review.
- Host observed: Darwin arm64; git 2.54.0; GitHub account Unjuno.
- Docker daemon responds: linux aarch64. No solver/container has been executed.
- Initial PATH inspection did not find foamRun, simpleFoam or SU2_CFD.
- Primary source audit and draft protocol recorded.
- First deliverable: repository and conservative report checker.

## Remaining completion evidence

- Freeze full source pins, licenses, runtime images and protocol thresholds.
- Implement and independently verify reference/forcing and derivatives.
- Build OpenFOAM adapter; run full space/time studies and AMR controls.
- Implement SU2 and current PhysicsNeMo adapters and independent studies.
- Preserve real logs and reference/metric data in reproducible run manifests.
- Search duplicate upstream issues; submit only supported improvements.
- Publish complete audit with report URLs or reasons not to submit.

Neither a repository commit nor checker tests complete the benchmark goal.

## Analytic reference implementation

- Public repository created: https://github.com/Unjuno/concentration-aware-ns
- Implemented smooth periodic u, grad(u), curl(u) and analytic forcing in NumPy.
- Nine unit tests passed with `python3 -m unittest discover -s tests -v`.
  The finite-difference reconstruction uses three stencil widths and verifies
  approximately second-order error reduction. This is a formula consistency
  test, not the required three-grid CFD experiment.
- Broader independent reference verification, production parameter freezing,
  solver integration, run logs and upstream findings remain outstanding.

## OpenFOAM runtime and pilot setup

- Built the ARM64 runtime from Ubuntu 24.04 and the official Foundation
  `openfoam13_20260624_arm64.deb`, verifying the package SHA256.
- Built image ID:
  `sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`.
- Build log and observed official package index are in `evidence/environment/`.
- Added `tools/openfoam_case.py`: periodic 3D mesh, analytic initial velocity,
  laminar incompressible configuration and coded analytic forcing.
- Launched an 8^3-cell integration pilot at dt=0.001 through t=0.005 under a
  non-root container user. Completion is **not verified**. The initial blockMesh
  log remains empty and a separate Docker status request is also pending.
  Do not interpret this as a solver failure or restart a possibly live run.
- Runtime documentation/recipe are reproducible setup artifacts. Solver execution,
  C++ forcing correctness and the space/time studies remain unverified.
