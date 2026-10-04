# SU2 transient MMS adapter — pilot executed

Pinned upstream: v8.5.0 / 12eb826f049ef7f67df974dfcb44cf36ee07c0f8.
The source, Eigen and MEL archives are checksum-verified, with Meson pinned to 1.8.2.
Ubuntu transitive packages are not snapshot-pinned; preserve built image identity.

`docker build --platform linux/arm64 -t concentration-aware-ns:su2 runtime/su2`

mms.patch modifies SU2's USER_DEFINED_SOLUTION extension for our periodic 3D
reference with sigma=0.5, nondimensional rho=1 and nu=0.01. The patch retains
SU2's LGPL-2.1-or-later licensing; it is not covered by the root MIT license.
Source is retained inside the image. No second Git repository is created.

Build completed and both pilots exited successfully. The 1000-inner-iteration
pilot reached all four residual thresholds at every step. The mapping between
MMS time, history time and the updated solution remains unresolved; no local
quality verdict is assigned. See docs/progress.md and evidence/su2.
This adapter is our experiment, not an upstream SU2 change or proven bug fix.

## Shared Fourier-envelope MMS

`high_gradient.patch` is a separate adapter for the cross-solver reference in
`protocols/su2-shared-high-gradient-v1.json`. It fixes frequency N=4 and
implements the same analytic velocity and momentum forcing used by the
OpenFOAM and PhysicsNeMo high-gradient cases. Its helper was compiled with GCC
and matched the independent NumPy evaluator at 257 seeded points; this check
does not cover SU2 linking, the solver residual path, or time integration.

Build it with:

```sh
docker build --platform linux/arm64 -f runtime/su2/Dockerfile.high-gradient -t cans-su2-high-gradient runtime/su2
```

The candidate study retains the historical Gaussian adapter and archives each
case, run log, time history, sampled quality metrics, protocol hash, and image
identity separately. The source patch remains under SU2's LGPL-2.1-or-later
terms.

After downloading a completed matrix artifact, replay its archive and
postprocessing checks with:

```sh
python -m tools.replay_su2_high_gradient_study --root path/to/run --output evidence/tests/su2-shared-high-gradient-replay.json
```
