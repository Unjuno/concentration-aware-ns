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
underestimate the continuous reference maxima by approximately 13.12% and 13.17%.
The center values are now proved to be exact reference maxima in
`docs/reference-global-peaks.md` (analytic derivation, not machine checked).
For the gradient, sampling and FD2 applied to the exact field already produce a
13.90% deficit; the computed FD2 peak is slightly higher than that control.
Consequently the 13.12% figure must not be labeled isolated solver error.
See `reports/peak-diagnostic-decomposition.md` for the signed decomposition and
its limits: differences of maxima are not pointwise field errors.

The temporal field differences are small, but their observed ratio gives an order
of approximately 0.493 rather than demonstrating the expected asymptotic regime.
The full space/time verification requirement therefore remains unresolved.
Continuous reference maxima are analytically known; bounds for the reconstructed
numerical field and a complete numerical uncertainty budget remain unavailable. The conservative v2 gate reports UNCERTAIN, even though specific
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

## Directional temporal check

The archived timestep differences are not simply one common leading error
vector scaled by the timestep. With a=U(dt)-U(dt/2), b=U(dt/2)-U(dt/4),
`python3 -m tools.check_openfoam_temporal_alignment` finds cosine(a,b)=0.88310,
best-fit a≈1.24277*b, and ||a-2b||/||a||=0.71391. The component of a orthogonal
to b is 46.92% of ||a||. Input hashes match the earlier temporal comparison.
These are post-hoc consistency diagnostics, not new acceptance thresholds or
proof of the cause. They strengthen the reason not to extrapolate a
first-order temporal error bound from this triple.

The cases already write 16 significant digits. Current linear/outer absolute
stopping tolerances are 1e-10/1e-8 with at most 12 outer correctors. A frozen
follow-up protocol, `protocols/of13-iteration-sensitivity-v1.json`, retains the
same three timesteps and changes these to 1e-12/1e-10 and 40 correctors. It
will compare same-dt field shifts and temporal directions before attributing
the observed order to time discretization. That follow-up has not yet run.

The iteration-sensitivity follow-up has now completed its dt=0.001 case:
exit zero, all 50 physical steps report outer convergence, and final cell
centers match the original. The same-dt final velocity relative field shift
is 6.55046e-15; relative reference errors are 0.00491374447113238 (original)
and 0.00491374447113237 (tight). Thus the stricter settings do not materially
change this endpoint. This is one completed case, not a three-step temporal
conclusion; the two smaller timesteps remain in progress. The completed raw
archive and `first-case-comparison.json` are saved in
`evidence/of13-iteration-sensitivity-v1`.
