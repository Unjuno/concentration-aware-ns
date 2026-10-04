# SU2 high-gradient matrix runtime budget check

As of 2026-10-04 22:40 UTC, workflow run
[37230949147](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37230949147)
had completed its n16 case and was still executing the frozen solver step for
n32-dt0.001 and all three n64 cases. The workflow has a 360-minute per-case
job limit. The jobs had entered the solver step between 20:20 and 20:26 UTC;
the three n64 jobs had therefore spent about 2 h 15 min to 2 h 20 min in that
step. This is an as-of snapshot, not a terminal status.

The same run provides one completed timing reference. Its n16-dt0.001 solver
step ran from 20:19:14 to 21:18:03 UTC (58 min 49 s), completing 50 physical
updates. The archived history records 112,201 total inner iterations (between
1,650 and 2,999 per update); the solver log is about 10.2 MB. The elapsed time
per inner iteration averaged about 31 ms on that job. This is a single-run
measurement, not a stable performance benchmark.

A crude cell-update proportional estimate multiplies that elapsed time by
about 8 from n16 to n32 and 64 from n16 to n64, since the three-dimensional
mesh sizes have those cell-count ratios. It gives roughly 7.8 hours for n32
and 62.7 hours for n64-dt0.001, before the 2x and 4x time-update counts in the
two n64 temporal cases. This extrapolation is deliberately only a scheduling
warning: SU2 inner-iteration counts, cache behavior, runner variability and
parallel efficiency can change scaling substantially. Still, observed n32/n64
runtime already exceeds 2 hours, so completion within each 6-hour job limit is
not demonstrated and looks doubtful under this simple model.

The current runner prints a START line, redirects all SU2 output to the local
`solver.log`, and prints END only after the solver exits. The workflow uploads
the case directory in an `always()` step, so partial logs should be preserved
if the job reaches a terminal state, but there is no live solver iteration or
heartbeat telemetry in Actions while it runs. The active jobs must be allowed
to reach their own terminal state before treating them as timed out or
replacing them. A successor should preserve the frozen cases and image while
adding observable progress or bounded restartable segments; changing the
inner-iteration cap would change the experiment and requires a separately
frozen protocol.

This is a compute-budget/observability concern, not a solver correctness
finding. No conclusion about the PDE, concentration, singularity, molecular
ordering, phase transition, or physical viscosity follows from runtime.
