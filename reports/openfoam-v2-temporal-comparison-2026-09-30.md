# OpenFOAM Foundation 13: frozen n=64 temporal-row comparison

The three archived Foundation 13 v2 high-gradient MMS cases at `n=64` were
replayed through the exact-field comparator at common endpoint `t=0.05` for
`dt = 0.001, 0.0005, 0.00025`. All three completed their 50, 100 and 200
steps, respectively, and pass both standard acceptance and the separately
defined local-quality gate. Archive and source-log hashes, matching
cell-centre arrays, and identical non-time input hashes are recorded in
[`../evidence/tests/high-gradient-of13-v2-temporal-comparison-2026-09-30.json`](../evidence/tests/high-gradient-of13-v2-temporal-comparison-2026-09-30.json).

The endpoint relative velocity errors against the analytic manufactured
solution are `0.00478066`, `0.00478409`, and `0.00479049` as `dt` decreases.
The normalized successive field differences are `1.3374e-5` and `9.4658e-6`,
which give a descriptive difference order of about `0.499`. The exact-error
ratios give descriptive orders near `-0.0010` and `-0.0019`; the error does
not visibly decrease with this timestep refinement. This combination suggests
that the endpoint error at this fixed spatial resolution is dominated by
contributions not removed by timestep refinement, but the three-point trend
does not isolate spatial error, nonlinear-iteration effects, or asymptotic
time-discretization error.

For this frozen benchmark, the local-gradient/vorticity accuracy gate passes
at n=64 for all three time steps. The matrix-level blind-spot criterion remains
`NOT_OBSERVED` at the adequately resolved n=64 and n=128 grids. This result
does not prove a universal solver property, an implementation defect, or any
physical singularity. The correct next numerical discriminator is a
same-grid intervention that varies temporal scheme or tightly controls
spatial/nonlinear error, with preregistered error norms and more than one
endpoint or refinement range.

Reproduce with:

```sh
work/reference-check-env/bin/python -m tools.compare_high_gradient_temporal
```
