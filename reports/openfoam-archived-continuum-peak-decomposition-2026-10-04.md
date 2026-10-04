# Archived OpenFOAM peak diagnostics against the continuous reference

The N=4 analytic certificate supplies continuous reference maxima for the
frozen high-gradient MMS. The six archived Foundation 13 cases were replayed
from their hashed archives and their peak diagnostics decomposed into three
levels: exact analytic derivatives sampled at cell centers; FD2 applied to the
sampled exact velocity; and FD2 applied to the solver's cell-centered
velocity.

| Case | Exact derivative samples / continuum (grad, curl) | Reference FD2 / continuum (grad, curl) | Solver FD2 / continuum (grad, curl) | Standard / local gate |
|---|---:|---:|---:|---|
| n16, dt=.001 | 66.32%, 65.22% | 42.81%, 43.26% | 41.77%, 43.35% | PASS / FAIL |
| n32, dt=.001 | 90.66%, 90.47% | 81.72%, 82.10% | 81.34%, 82.16% | PASS / FAIL |
| n64, dt=.001 | 97.60%, 97.56% | 95.14%, 95.25% | 95.03%, 95.27% | PASS / PASS |
| n128, dt=.001 | 99.40%, 99.39% | 98.77%, 98.80% | 98.74%, 98.80% | PASS / PASS |
| n64, dt=.0005 | 97.60%, 97.56% | 95.14%, 95.25% | 95.03%, 95.27% | PASS / PASS |
| n64, dt=.00025 | 97.60%, 97.56% | 95.14%, 95.25% | 95.02%, 95.27% | PASS / PASS |

This separates three contributors to a sampled local-peak comparison. At n=64,
the exact reference derivatives at the cell centers capture about 97.6% of the
continuous peak. Applying the centered FD2 stencil to the exact sampled
velocity reduces the diagnostic to about 95.2%; the solver-field FD2 result is
near that stencil control. The two temporal refinements barely change this
peak diagnostic at fixed n=64, while n=128 increases it to about 98.8%.

The last column preserves the frozen gate results: all six cases pass standard
acceptance, local quality fails at n16/n32 and passes at n64/n128 and both n64
time refinements. The supplementary ratios are not continuous extrema of the
solver field, not estimates with certified error bars, and do not change the
gate thresholds. They neither prove an OpenFOAM defect nor a physical
concentration mechanism. In particular, the predefined adequate-grid
matrix rule remains `NOT_OBSERVED`.

Reproduce the archive checks, replay and table values with:

```sh
work/reference-check-env/bin/python -m tools.compare_openfoam_peaks_to_continuum \
  --output evidence/tests/openfoam-continuum-peak-decomposition-2026-10-04.json
work/reference-check-env/bin/python -m pytest -q \
  tests/test_openfoam_continuum_peak_decomposition.py
```

The JSON receipt contains the matrix index and protocol hashes, every case
archive SHA-256, the exact dimensional peak values, all three diagnostic
levels, and the rechecked standard/local gate decisions.
