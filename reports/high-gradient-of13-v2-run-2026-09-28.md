# High-gradient OpenFOAM v2 run status

Run started 2026-09-28 against the frozen protocol
`protocols/high-gradient-of13-v2.json` using source commit
`0e0288f98209f856931352ebfa5dad0f1aad0014` and container image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`
(`linux/arm64`). The exact commands, generated case inputs, raw logs, endpoint
fields and per-case diagnostics are archived under
`evidence/of13-high-gradient-v2/`. Archive hashes and the run-environment
manifest are in its `manifest.json`.

## Completed cases at the snapshot

| Grid / time step | Standard acceptance | Local quality | Main observed errors |
|---|---|---|---|
| n=16, dt=0.001 | PASS | FAIL | velocity L2 8.88%; gradient peak 37.0%; vorticity peak 33.5% |
| n=32, dt=0.001 | PASS | FAIL | gradient peak 10.3%; vorticity peak 9.18% |
| n=64, dt=0.001 | PASS | PASS | velocity L2 0.478%; gradient peak 2.64%; vorticity peak 2.35% |

All three cases reached the requested end time and recorded 50 PIMPLE-converged
steps. The n=16 and n=32 derivative discrepancies are classified as
underresolution: before execution, the reference-only periodic FD2 audit
predicted that those grids exceed the 5% derivative thresholds. The n=64
case, which clears that stencil-floor condition, passes every preregistered
local-quality threshold. These coarse-grid failures do not reproduce an
acceptance blind spot or establish a software defect.

## Incomplete cases and interpretation

At the manifest snapshot, n=128/dt=0.001 had entered its first physical step
and completed velocity and pressure solves in the first PIMPLE iteration, but
had not emitted a convergence record or another time-step record. Its
`log.foamRun` then remained unchanged for more than 25 minutes. The host
`docker run` client remained live, while separate Docker `top`, `stats` and
`inspect` requests did not return during the observation window. This is an
execution/runtime stall with no terminal container state: no exit code, solver
verdict, or OOM result is inferred. The active runner and incomplete case were
left intact; OrbStack and unrelated containers were not restarted or stopped.

The two n=64 smaller-time-step cases had not started. Consequently the full
spatial/time matrix is incomplete, and the persistent-blind-spot gate remains
`UNCERTAIN`. In particular, n=128 must finish and the dt triple must run before
the frozen hypothesis rule can be applied. The unarchived n=128 partial tree
remains under ignored `work/of13-high-gradient-v2/n128-dt0.001`; the evidence
manifest records its observed step count and log hash. The reusable
`tools/archive_high_gradient_openfoam.py` archives only cases whose runner exit,
step count, convergence count, `End` marker and endpoint fields all pass its
completion checks; it verifies archive contents against source files before
reporting them.

## Later live-run observation (2026-09-28 01:48 UTC)

The same original runner and Docker client PIDs remained live; no replacement
container was started. The n=128 case had reached `Time = 0.009s`, with five
outer correctors recorded for completed steps through 0.008s. The step ending
at 0.009s was still inside its PIMPLE loop at the latest log read. The previous
logged step reported `ExecutionTime = 498.94 s` and `ClockTime = 2309 s`;
the host run had been active for roughly 44 minutes. These timings make the
remaining 41 steps impractical to finish promptly on this run, but the live
process is not a terminal failure. No exit code, completed-case archive, or
quality verdict is available. The two smaller-dt cases remain unstarted and the
matrix remains INCOMPLETE/UNCERTAIN. Preserve the partial tree and process for
later observation; don't infer a solver defect from runtime cost.

## Analytic reference follow-up

Separately, the exact high-gradient MMS identities were extended to report the
Frobenius-gradient norm and vorticity at a selected analytic point, explicitly
as lower bounds on their continuous maxima rather than asserting global
maximality. A short derivation and both replay commands are in
`docs/high-gradient-analytic-checks.md`. The symbolic identities pass, and an
independently coded Fourier evaluator agrees with direct SymPy differentiation
for velocity, full gradient, vorticity and forcing at the recorded points.
These are continuum formula checks, not solver integration or a numerical
acceptance verdict.
