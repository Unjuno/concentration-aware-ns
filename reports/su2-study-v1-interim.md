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
