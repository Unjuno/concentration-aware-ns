# SU2 localized study v1 — three completed cases

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

## Raw-data diagnostic replay

Run `python3 -m tools.replay_su2_diagnostics` to extract the necessary regular
files into a temporary directory and recompute all diagnostics for completed
cases. The n16 and n32 outputs exactly match their archived JSON values in the
recorded environment, including velocity, derivatives, spectrum and history
checks. `evidence/su2-study-v1/diagnostic-replay.json` records archive and source
hashes. This verifies reproducible postprocessing with the same implementation;
it is not independent validation of that implementation or a new solver run.


## n64, dt=0.001 completed result

The frozen n64 case completed all 50 updates. Its archive hash and input hashes
pass the integrity review, and raw-field diagnostic replay exactly matches the
archived diagnostics. Velocity relative L2 error is 0.362505%, below the 2%
threshold. FD2 gradient and vorticity peak discrepancies are 2.55164% and
2.55168%; spectral peak discrepancies are 0.453976% and 0.454013%.
These sampled comparisons are not certified continuous reconstructed-field peaks.
Periodic duplicate values match exactly. Residual thresholds were met in 48/50
updates; the first two failed. The remaining two time-step cases are still
required, so no final quality or hypothesis PASS is assigned.

## All five frozen runs completed: endpoint temporal comparison

All five archives now pass byte-integrity review and exact diagnostic replay.
The n64 runs at dt=0.001, 0.0005 and 0.00025 reach t=0.05, with respectively
48/50, 97/100 and 193/200 steps meeting all four strict residual criteria.
Completion does not imply convergence of every inner solve.

Direct differences of endpoint velocity fields on the verified periodic n64
vertex lattice give RMS vector differences 5.3558517845476045e-5 and
2.6794894751638003e-5 for successive halvings. Their observed order is
0.9991578874547687. Relative L2 differences to the finer field are
0.00014348070046906172 and 0.00007178225425111923.

This is consistent with first-order endpoint behavior for this sequence,
but is not an error certificate: inner solves include unconverged steps,
only two successive differences are available, and spatial/model error remains.
The velocity errors against the exact solution slightly increase across these
time refinements; that fact alone would miss the near-first-order differences
between the computed fields. Do not estimate order from differences of error
norms. No acceptance verdict is upgraded.

Reproduce with `python3 -m tools.compare_su2_time`. The JSON evidence includes
archive hashes, convergence counts and both differences in
`evidence/tests/su2-time-comparison.json`.

## Evidence-linked gates for every frozen case

`python3 -m tools.build_su2_report` writes all five schema-2 gate/verdict pairs.
Each includes residual-step counts, observed velocity error, sampled spectral
derivative diagnostics, the archived case hash and eight evidence links.
All current verdicts remain UNCERTAIN. This does not erase measured threshold
violations: n16 and n32 exceed the protocol's 2% velocity tolerance, and all
n64 runs plus n32 contain steps failing the frozen residual criterion.

The derivative metric intervals are explicitly [0, unbounded], because no
continuous reconstructed-field peak-error certificate is available. The zero
is the trivial lower bound, not a measured zero error. Sampled spectral peak
deficits remain observations and are not passed as certified error intervals.
The derivative, space/time and full standard-review flags remain false.
The full report replay now includes these gates and checks 88 artifact links.

## Observed aggregate acceptance review

`python -m tools.review_su2_standard` (NumPy/SciPy environment) compares the
archived sample mean energy with the analytic continuum integral and checks
the frozen velocity/energy thresholds alongside all-step residual convergence.

| Case | Velocity error | Energy error | Every step converged |
|---|---:|---:|---|
| n16 dt=.001 | 10.1648% | 12.0279% | Yes |
| n32 dt=.001 | 2.2772% | 2.4642% | No |
| n64 dt=.001 | 0.3625% | 0.3551% | No |
| n64 dt=.0005 | 0.3647% | 0.3553% | No |
| n64 dt=.00025 | 0.3660% | 0.3553% | No |

No case meets all three observed checks. The conjunction is an explicit audit
convention, not a retroactively preregistered definition of standard acceptance.
This prevents presenting these runs as established examples of standard PASS
with local FAIL. Their individual errors and residual failures remain useful
benchmark evidence and do not by themselves establish a solver defect.
Energy quadrature and solution error are combined; continuous numerical-field
energy is not certified. Schema-2 conservative verdicts remain unchanged.
Evidence: evidence/tests/su2-standard-review.json, with archive SHA256 values.
