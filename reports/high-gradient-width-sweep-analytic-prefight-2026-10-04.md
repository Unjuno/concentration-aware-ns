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
parity test is explicitly skipped locally and is pending the hosted Linux test.
No width sweep has been run. The separate AMR generator remains on its
historical fixed envelope; AMR width generalization is still open.

Before execution, select widths whose finest grids meet the frozen
shortest-wavelength condition, then independently verify source timing,
sampling phase, spectral tails and continuous-peak search.

Replay commands:

```sh
uv run --python 3.14 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_high_gradient_width_sweep
uv run --python 3.14 --with-requirements requirements-verification-locked.txt \
  python -m pytest -q tests
```
