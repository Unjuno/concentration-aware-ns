# Continuous error bound for one OpenFOAM reconstruction — v3

## Scope

This audit certifies an explicit real, periodic, cell-centered trigonometric
interpolant through the **serialized endpoint U values** in the frozen
Foundation 13 archives. It does not certify the unrounded solver state, the
OpenFOAM finite-volume field, face interpolation, or any canonical OpenFOAM
continuous reconstruction. The v2 verdicts and thresholds are unchanged; no
solver was rerun.

The archived cell-center coordinates differ from the ideal uniform lattice by
at most `3.89e-15` in the cases checked. The interpolation assigns the archived
values to the ideal cell-center lattice. The exact manufactured velocity has
Fourier modes only through wavenumber 4, below the Nyquist frequency in all
three grids, so its own interpolant equals the continuum reference exactly.

## Bound

For the interpolation error `e(x)=sum_k e_hat[k] exp(i k·x)`, the triangle
inequality and the Frobenius norm give

```text
sup_x ||grad e(x)||_F <= sum_k |k| ||e_hat[k]||_2.
```

The pointwise inequality `||curl e||_2 <= sqrt(2) ||grad e||_F` gives the
corresponding vorticity bound. Every coefficient and DFT operation is enclosed
with 128-bit Arb/Acb balls. The analytic peak denominators use rigorous lower
bounds from sampled analytic gradient/vorticity components; a sampled
component cannot exceed the continuum peak. Even-grid Nyquist samples use real
sine representatives; splitting a Nyquist coefficient across its aliased
positive and negative modes leaves the weighted coefficient sum unchanged.

| Cells per axis | Gradient relative supremum upper bound | Vorticity relative supremum upper bound | Compared with frozen 5% derivative threshold |
|---:|---:|---:|---|
| 16 | 15.0375% | 19.0470% | Above for both |
| 32 | 2.6027% | 3.2779% | Below for both |
| 64 | 0.6221% | 0.7823% | Below for both |

These are bounds on the **continuous derivative error of this named
interpolant**, not on OpenFOAM's finite-volume field. They explain how a
continuous inter-sample statement can be made without treating sampled maxima
as continuous maxima. At n=32 the alternative reconstruction's derivative
error is bounded below the frozen 5% threshold, while the frozen FD2 diagnostic
fails because its reference-only stencil floor is about 9.86% for gradient and
9.25% for vorticity. This reconstruction sensitivity does not imply a solver
defect. Other frozen acceptance metrics still apply; the n=32 velocity error
remains above its 2% threshold.

## Reproduction

Run `python3 -m tools.audit_openfoam_trig_supremum` in the pinned verification
environment. The exact decimal solver/reference samples, archive hashes,
protocol/source hashes, precision, denominator enclosures and result balls are
recorded in `evidence/tests/openfoam-trig-supremum-arb-v3.json`. The report is
included in `tools.replay_published_reports`.

This is a certificate for one explicit reconstruction of three archived data
sets. It does not select that reconstruction as the physical or numerical
field represented by OpenFOAM's finite-volume solution, and it supplies no
claim about singularity, blow-up, molecular alignment, viscosity change or
physical hazard.
