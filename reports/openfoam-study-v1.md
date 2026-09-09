# OpenFOAM study v1 — completed runs, incomplete acceptance evidence

The fixed smooth manufactured problem completed all five uniform cases at t=0.05.
All physical steps recorded outer convergence. This establishes the configured
iteration criterion, not continuum accuracy by itself.

| Grid | dt | Relative velocity L2 | Relative mean-energy error versus continuum |
|---|---:|---:|---:|
| 16³ | 0.001 | 0.0654077 | 0.00753547 |
| 32³ | 0.001 | 0.0187001 | 0.00201044 |
| 64³ | 0.001 | 0.00491374 | 0.000493223 |
| 64³ | 0.0005 | 0.00491960 | 0.000464438 |
| 64³ | 0.00025 | 0.00492265 | 0.000449393 |

For the 32³ case, velocity and energy errors are below the preregistered 2%
aggregate thresholds. Nevertheless, the reported FD2 gradient and vorticity peaks
underestimate the continuous maxima by at least approximately 13.12% and 13.17%,
using analytic center-value lower bounds. This is a concrete diagnostic disparity.
It is not evidence that the solver alone caused the peak error: exact-field
sampling and FD2 account for an important part of the discrepancy.

The temporal field differences are small, but their observed ratio gives an order
of approximately 0.493 rather than demonstrating the expected asymptotic regime.
The full space/time verification requirement therefore remains unresolved.
Continuous peak upper bounds and a complete numerical uncertainty budget are also
unavailable. The conservative v2 gate reports UNCERTAIN, even though specific
aggregate thresholds and a one-sided peak discrepancy are individually observed.
No claim of a fully reproduced acceptance failure or upstream bug is assigned.

The AMR budget and fixed-refined-mesh controls are complete. They show that final
mesh geometry alone does not explain the adaptive-history error; initialization,
interpolation and dynamic flux corrections remain combined confounders. The
approximate maxCells behavior is consistent with the inspected source example.
No new implementation-contract violation is established, so no OpenFOAM bug report
has been filed. The project's stated reporting channel is bugs.openfoam.org.

Evidence: evidence/of13-study-v1, evidence/of13-amr-v1,
evidence/of13-remap-control-v1 and the continuum-energy, time-comparison and
peak-lower-bound JSON files in evidence/tests. Reproduce the triage from the
repository root with:

```
python3 tools/acceptance_gate.py reports/openfoam-n32-gate.json --artifact-root .
```

Exit 2 is the expected result. Hash-matched review artifacts do not make the
scientific review infallible, and the unresolved flags must not be set merely to
obtain a desired verdict.
