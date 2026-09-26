# SU2 BDF2 source-time control — 2026-09-26

A reply to [discussion 2890](https://github.com/su2code/SU2/discussions/2890#discussioncomment-18418174)
prompted this follow-up. The live API now records one comment; the earlier cached
zero-comment view was stale. The reply proposed testing whether lagged MMS forcing
reduces BDF2 temporal order. We independently reproduced that behavior in the
pinned v8.5.0 single-zone, static periodic uniform MMS control.

The solution is u=(1+t²,0,0), p=0, forcing=(2t,0,0), ending at T=0.5.
Only TIME_MARCHING changes from the earlier control to
DUAL_TIME_STEPPING-2ND_ORDER. The existing diagnostic image changes the driver's
physical time to (TimeIter+1)*dt; it is not a proposed general fix.
The protocol was written before these six runs. Both image IDs, commands,
configurations, restart fields, history, logs and exit codes are archived.

| dt | Original endpoint max error | Time-shift endpoint max error |
|---|---:|---:|
| 0.1 | 0.08506172841 | 0.004979423888 |
| 0.05 | 0.04625006353 | 0.001249978856 |
| 0.025 | 0.02406250002 | 0.0003125000269 |

Observed orders are 0.87905, 0.94267 for the original and 1.99408, 1.99998 for
the intervention. Every saved step has all four log10 residuals below -10.
Spatial spreads stay below 5.30e-11. This control avoids the unconverged inner
iterations present in the separate localized benchmark.

## Exact recurrence including startup

With h=dt and the repeated initial history U[-1]=U[0]=1, the original satisfies
3U[k]-4U[k-1]+U[k-2]=4h²(k-1). Its error against 1+(kh)² is

    e[k] = -2kh² + (3/2)h²(1-3^(-k)).

At fixed T=kh this is -2Th+O(h²), hence first order. The time-shift recurrence
has right side 4h²k and error

    e[k] = (1/2)h²(1-3^(-k)).

The remaining second-order term accounts for startup; it is not evidence of
incorrect BDF2 interior differentiation. Exact rational checks verify each
recurrence and both initial states. All saved numerical states agree with the
respective prediction within 5.40e-11 (a bound including spatial spread).
Thus the initial-history assumption is checked against every saved step.

## Reproduction and scope

Build the two existing images per runtime/su2-time-control/README.md, then run:

```
python3 -m tools.run_su2_bdf2_control
python3 -m tools.run_su2_bdf2_control --corrected
python3 -m tools.check_su2_bdf2_control
```

The first two refuse existing output roots. The checker can replay the committed
archives: it checks archive hashes, solver exit codes, the selected scheme, raw
restart means/spreads, raw residual histories and exact recurrence predictions.
Results are in evidence/tests/su2-bdf2-control.json. Input protocol is
protocols/su2-bdf2-control-v1.json; raw archives are under
evidence/su2-bdf2-control-v1 and evidence/su2-bdf2-control-v1-corrected.

This establishes order reduction for this time-dependent MMS and pinned runtime
(commit 12eb826f049ef7f67df974dfcb44cf36ee07c0f8). It does not establish behavior
of all SU2 source terms, current master binaries, moving grids, boundary states,
restart, multizone or compressible solvers. Separating stored-state time from
target time deserves review across those consumers before proposing a patch.
No claim about concentration, mathematical blow-up or physical viscosity follows.

The BDF2 checker is included in `python3 -m tools.replay_published_reports`.
The integrated replay passed all thirteen steps and 36 tests. Endpoint errors
used for convergence orders are recomputed from raw restart velocities, with
finite-value, complete-case and complete-step checks. The strengthened replay
leaves all reported BDF2 values unchanged. This adds postprocessing verification,
not another solver run.

The [time-consumer scope audit](su2-time-consumer-scope.md) independently matches
three relevant source files to the pinned runtime revision and separates the
source, verification-error and Dirichlet-boundary consumers. Its proposed
boundary/restart regressions remain unperformed; it does not expand the scope
of the six archived runs.
