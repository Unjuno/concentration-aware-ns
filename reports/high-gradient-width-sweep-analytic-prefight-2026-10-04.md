# Analytic preflight for a localized-envelope width sweep — 2026-10-04

The current localized MMS fixes its transverse envelope to
`chi(y,z)=h_4(y)h_4(z)`, where `h_m(q)=((1+cos(q))/2)^m`. I generalized the
independent NumPy reference evaluator to integer `m` while preserving the
original `m=4` coefficient path. The differentiated Fourier series agrees
with direct SymPy differentiation at test points for `m=2,4,8`; the velocity
gradient remains divergence-free. The local tests and locked full suite pass.

Before any solver run, `tools.audit_high_gradient_width_sweep` evaluated the
exact field at the existing cell-center grids `n=16,32,64,128` for six widths.
Its independent reference-only peak comparison is recorded at
`evidence/tests/high-gradient-width-sweep-reference-only.json`. The `m=4`
values exactly reproduce the existing frozen FD2-floor receipt, providing a
regression check. Near the peak, the equivalent Gaussian width is
`sigma=sqrt(2/m)`.

| m | sigma | n=64 gradient/vorticity FD2 peak floor | n=128 floor | cells per highest envelope wavelength at n=64/n=128 |
|---:|---:|---:|---:|---:|
| 1 | 1.4142 | 2.548% / 2.478% | 0.641% / 0.623% | 64 / 128 |
| 2 | 1.0000 | 2.542% / 2.424% | 0.639% / 0.610% | 32 / 64 |
| 4 | 0.7071 | 2.525% / 2.365% | 0.635% / 0.595% | 16 / 32 |
| 8 | 0.5000 | 2.508% / 2.405% | 0.631% / 0.605% | 8 / 16 |
| 16 | 0.3536 | 2.762% / 2.909% | 0.700% / 0.739% | 4 / 8 |
| 32 | 0.2500 | 4.704% / 4.773% | 1.249% / 1.254% | 2 / 4 |

All six widths fail the 5% reference-only peak-floor check at n=16 and n=32.
The first four pass that check at n=64 and n=128. However, the m=32 n=64 row
is a warning: the aggregate peak-floor metric falls just below 5% despite only
two cells per highest envelope wavelength. At the Nyquist mode, periodic
centered FD2 estimates a zero derivative for a nonzero single Fourier mode.
Thus an aggregate peak test can conceal unresolved high-frequency content.
For a single mode, solving `sin(theta)/theta=0.95` gives
`theta=0.5519109786...`, or about 11.39 cells per wavelength for a 5%
FD2 derivative-symbol error. This is a conservative mode-level screen, not a
continuous-extrema certificate or a complete multi-mode error bound.

This preflight did not run OpenFOAM, SU2 or PhysicsNeMo; it does not establish
solver acceptance, cross-target comparability, a software defect, or any
physical claim. It shows why a width-sweep protocol must freeze a
shortest-wavelength resolution condition alongside local peak thresholds.

## OpenFOAM uniform-grid adapter extension

The case generator now accepts an `envelope_power` parameter for the uniform
high-gradient profile. It writes the exact initial field from the independent
NumPy evaluator and generates Fourier coefficients for the C++ `fvModels`
forcing. The historical `m=4` path retains its existing generated-code branch.
Tests compare generated initial fields for `m=2` and compile the generated
forcing at `m=2` and `m=8` against the independent reference. The local Apple
compiler is unavailable until its Xcode license is accepted, so that compiler
parity test is skipped locally; corrected hosted Linux parity passed at
`fdbd4e9c`. The analyzer now reads the case power for its reference solution
and only claims a certified continuum peak for the historical m=4 formula.
Regression tests caught the previous default-m=4 analyzer behavior. No width
sweep has been run. The separate AMR generator remains on its
historical fixed envelope; AMR width generalization is still open.

Protocol `protocols/high-gradient-of13-width-v1.json` is now frozen for m=1,2,4
with 15 deduplicated space/time cases. The exact-sampled FD2 preflight passes
the existing 5% gradient/vorticity floors at n=64 and n=128 for every width;
n=32 deliberately remains a coarse comparison and fails those reference-only
floors. Continuous extrema are not certified. A workflow-dispatch job in the repository’s existing Foundation 13 control
workflow runs on ARM64 and preserves full case archives and partial evidence;
PR-triggered runs continue to exercise the existing smooth-control job. The
remaining solver run will independently record source timing, sampling phase,
spectral tails and local acceptance.

Replay commands:

```sh
uv run --python 3.14 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_high_gradient_width_sweep
uv run --python 3.14 --with-requirements requirements-verification-locked.txt \
  python -m pytest -q tests
```

Hosted parity diagnostic and correction (2026-10-04): the first Linux C++ run
(`37205965405`, pre-fix commit `d93c1c88`) compiled but found maximum force
errors 2.1212e-2 at m=2 and 1.0679e-2 at m=8. Inspection traced both to the
generic derivative helper retaining the constant Fourier mode for derivative
orders 1–3. Commit `fdbd4e9c` now initializes that coefficient only for order
zero. The corrected test passed on hosted Linux in run `37207039671` at commit
`fdbd4e9c`; the generated C++ forcing for both m=2 and m=8 is now below the
1e-10 absolute-error gate against the independent NumPy reference. The complete
Python verification job passed (447 tests, three skips, 89 subtests). This host
mock still does not establish compatibility with Foundation headers or live
solver behavior.

## Related developments checked beyond the OpenAI announcement

A current-literature check on 2026-10-04 found two directly related 2026
preprints. Cao, Chi and Nie's [Density of Forces Producing Navier--Stokes
Blowup](https://arxiv.org/abs/2609.10262), submitted 2026-09-09 and revised
2026-09-22, starts from OpenAI's compact forced example and proves density of
blow-up-producing smooth forces in a relative time-integrated spatial
$L^1_tH^s_x$ topology for $s<1/2$ (with a sharp threshold in their setting).
This is a genuine further mathematical consequence if the starting example
and transfer argument are correct, but it depends on that example and does
not independently validate its construction, classify generic initial data
under one fixed force, or establish a molecular mechanism.

Lei and Ren's [Part I profile construction](https://arxiv.org/abs/2609.35406),
submitted 2026-09-28, presents itself as a readable derivation of the profile
construction in OpenAI's manuscript. Its abstract says the cancellation by
oscillatory pulses is deferred to a companion Part II. Treat it as an
expository reconstruction in progress, not a completed independent audit.

A useful neighboring benchmark is Chen and Hou's [computer-assisted
singularity result for 3D axisymmetric Euler](https://authors.library.caltech.edu/records/40zbk-gep55),
published 2025-07-08. It concerns inviscid Euler (and 2D Boussinesq), not
viscous Navier--Stokes, but demonstrates why machine-checked bounds around a
numerically constructed profile are stronger evidence than grid growth alone.

For the light-as-fluid hypothesis, the 2025 review [Paraxial fluids of
light](https://doi.org/10.1016/bs.aamop.2025.04.002) describes an effective
mapping from nonlinear optical propagation to a 2D+1 Gross--Pitaevskii / fluid
description. Experiments also report [Joule--Thomson expansion of a photon
gas](https://doi.org/10.1038/s41567-024-02736-1). These are meaningful
photon-fluid and optical-analogue platforms with their own interaction and
medium assumptions. They do not mean photons in vacuum form a material liquid,
nor that an incompressible Navier--Stokes singularity predicts molecular
ordering or a viscosity collapse in an ordinary fluid.
