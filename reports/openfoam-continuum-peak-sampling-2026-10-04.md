# Cell-center sampling of the certified N=4 reference peaks

The exact global-peak certificate for the high-gradient Fourier MMS now gives a
continuous reference against which the existing cell-center sampling can be
measured. For the protocol's periodic uniform grids at `t=0.05`, the maximum
analytic gradient and vorticity norms sampled at cell centers capture the
following fractions of their certified continuous maxima:

| Cells per axis | Gradient peak captured | Vorticity peak captured |
|---:|---:|---:|
| 16 | 66.3242% | 65.2161% |
| 32 | 90.6557% | 90.4683% |
| 64 | 97.6041% | 97.5621% |
| 128 | 99.3972% | 99.3871% |

This isolates a reference-sampling effect: the reference's exact derivatives
are evaluated only at cell centers by the archived uniform-grid analyzer, so
coarse grids do not see the full continuous reference peak. It does not measure
solver error, bound a numerical solution between cells, or show that a solver
has missed a peak. The existing acceptance and local-quality thresholds are
unchanged; their sampled same-grid comparisons remain the frozen benchmark.

The OpenFOAM analyzer now emits separate certified N=4 continuum-peak fields
and reference-sampling fractions. Other frequencies receive null values for
these certificate-specific fields. The historical `reference_*_peak_cell_samples`
values and every gate input keep their previous definitions.

Reproduce the table and raw values with:

```sh
work/reference-check-env/bin/python -m tools.measure_high_gradient_peak_sampling \
  --output evidence/tests/high-gradient-cell-center-peak-sampling.json
work/reference-check-env/bin/python -m pytest -q \
  tests/test_high_gradient_peak_sampling.py \
  tests/test_openfoam_high_gradient_case.py
```

The generated JSON records the reference-evaluator and continuum-certificate
SHA-256 values. The continuous maxima are proved in
[`high-gradient-global-peaks-analytic-certificate-2026-10-04.md`](high-gradient-global-peaks-analytic-certificate-2026-10-04.md).
