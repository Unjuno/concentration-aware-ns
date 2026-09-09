# SU2 localized study v1 — two completed cases

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
The 64³ and remaining time-step runs are still required before assessing the spatial/time
matrix. SU2 uses vertex samples, unlike OpenFOAM's cell centers, so the two coarse
runs must not be compared as if their sample points were identical.

The separate old-time forcing observation remains a time-contract question in
https://github.com/su2code/SU2/discussions/2890. It should not be presented as the
established cause of this case's entire error.

Evidence: evidence/su2-study-v1/n16-review.json and n16-dt0.001.tar.gz.

## n32 completed result

The n32, dt=0.001 case completed 50 updates to t=0.05 with exit code 0 and
SU2's Exit Success marker. The archive SHA256 matches summary.json, and all
five archived inputs match the diagnostic hashes. Periodic duplicates match.

| Quantity | Result |
|---|---:|
| Sampled velocity relative L2 error | 2.27715% |
| Completed updates meeting all four strict residual thresholds | 48 / 50 |
| FD2 gradient peak discrepancy versus exact reference peak | 11.2359% |
| FD2 vorticity peak discrepancy versus exact reference peak | 11.2412% |

Updates 0 and 1 reached Inner_Iter=2999 (3,000 iterations) without satisfying
all four strict log10 residual thresholds below -10. Later convergence does not
retroactively make these updates converged. The velocity error also exceeds the
frozen 2% criterion. Therefore this is not a conventional-PASS/local-FAIL finding.
The derivative discrepancies include postprocessing error and do not isolate a
solver defect or certify the continuous peak of the numerical solution.

The baseline protocol is unchanged. Higher-cap or altered-CFL controls must be
reported separately. The full matrix and acceptance review remain incomplete.
Evidence: evidence/su2-study-v1/n32-dt0.001.tar.gz and summary.json.
