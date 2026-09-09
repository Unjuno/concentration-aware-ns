# SU2 localized study v1 — first completed case

The n16, dt=0.001 case completed 50 updates to t=0.05. All four residual thresholds
were met at each update, and duplicated periodic values match exactly. The
archive hash was checked against the run summary before extracting this review.

| Quantity | Result |
|---|---:|
| Sampled velocity relative L2 error | 10.1648% |
| Energy error versus continuum reference | 12.0279% |
| FD2 gradient peak error at analytic sample maxima | 37.4451% |
| FD2 vorticity peak error at analytic sample maxima | 37.5841% |
| Exact-reference samples' FD2 gradient peak error | 28.1304% |

The velocity error already exceeds the declared 2% criterion. Therefore this case
is not a reproduced miss by the full conventional accuracy criteria, despite
iterative residual convergence. Derivative postprocessing contributes materially,
and no upstream implementation fault is inferred from this coarse-grid result.
The 32³ and remaining runs are still required before assessing the spatial/time
matrix. SU2 uses vertex samples, unlike OpenFOAM's cell centers, so the two coarse
runs must not be compared as if their sample points were identical.

The separate old-time forcing observation remains a time-contract question in
https://github.com/su2code/SU2/discussions/2890. It should not be presented as the
established cause of this case's entire error.

Evidence: evidence/su2-study-v1/n16-review.json and n16-dt0.001.tar.gz.

## n32 in-progress convergence observation

The first completed time-history row has Inner_Iter=2999 (3,000 iterations),
with log10 residuals P=-9.553895816, U=-9.421828648, V=-9.443823823,
W=-9.466627999. None passes the frozen strict -10 threshold. The preserved
first-step history and `n32-progress-convergence.json` record this observation.
The run remains in progress; no final field accuracy is inferred. Later steps
converging would not retroactively make this step converged. The baseline protocol
is unchanged. Any higher-cap or altered-CFL follow-up must be reported separately
and cannot replace the frozen run without preserving its outcome.
