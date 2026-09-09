I have a small manufactured-solution reproducer and would like to clarify the intended time contract of `GetMMSSourceTerm` in single-zone first-order dual-time stepping. Is the callback intentionally evaluated at the old physical time, or should it receive the time of the updated solution?

This is related to the temporal-verification topic in [discussion #1441](https://github.com/su2code/SU2/discussions/1441), but isolates a spatially uniform, time-dependent source. I am not claiming that SU2's time integrator is inconsistent: both recurrences below are first-order consistent.

### Analytic control

On a periodic cube use `INC_NAVIER_STOKES`, constant density 1, viscosity 0.01, energy disabled, and

```
u(t,x) = (1+t^2, 0, 0), p=0, f(t,x)=(2t,0,0).
```

All spatial derivatives vanish, so the PDE reduces to `du_x/dt=2t`. Initialize `u_x=1` at time zero. After k updates of size h:

- Source at `(k-1)h`: `U_k = 1+h^2*k*(k-1)`.
- Source at `kh` (fully backward Euler): `U_k = 1+h^2*k*(k+1)`.
- Continuous exact value: `1+(kh)^2`.

Neither discrete recurrence is the exact continuous solution at finite h.

### Observed behavior

With the unmodified driver and source assembly in v8.5.0, commit `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`, the custom `USER_DEFINED_SOLUTION` control matches the old-time recurrence at every step within `2.7e-11`. All four reported residuals are below `10^-10` at each update.

| h | updates | final U_x | final history Cur_Time |
|---|---:|---:|---:|
| 0.1 | 5 | 1.200000000002 | 0.4 |
| 0.05 | 10 | 1.224999999997 | 0.45 |
| 0.025 | 20 | 1.237499999998 | 0.475 |

A diagnostic intervention changing only the single-zone `SetPhysicalTime` argument from `TimeIter*h` to `(TimeIter+1)*h` switches the results to the next-time recurrence within the same tolerance. This is a causal check, **not a proposed general fix**: restart, multizone, moving-grid and second-order behavior have not been tested.

Source inspection of master `bc15466602a687d6fb796d5df7a12ce3fde0949a` still shows the same [time assignment](https://github.com/su2code/SU2/blob/bc15466602a687d6fb796d5df7a12ce3fde0949a/SU2_CFD/src/drivers/CSinglezoneDriver.cpp#L120) and [MMS consumer](https://github.com/su2code/SU2/blob/bc15466602a687d6fb796d5df7a12ce3fde0949a/SU2_CFD/src/solvers/CIncEulerSolver.cpp#L1861). I have not rerun a fresh master executable.

### Reproducer and environment

[Fixed evidence commit](https://github.com/Unjuno/concentration-aware-ns/tree/d8f1b05):

- [Build and run instructions](https://github.com/Unjuno/concentration-aware-ns/blob/d8f1b05/runtime/su2-time-control/README.md), including the custom analytic helper.
- [Baseline raw cases and per-step diagnostics](https://github.com/Unjuno/concentration-aware-ns/tree/d8f1b05/evidence/su2-time-control-v1).
- [Intervention cases](https://github.com/Unjuno/concentration-aware-ns/tree/d8f1b05/evidence/su2-time-control-v1-corrected).

Each archive contains the config, 4³-element periodic mesh, restart fields, history, logs, command and exit code. Linux arm64 Ubuntu 24.04 container, GCC 13.3.0, double precision, MPI disabled, two OpenMP threads. Source archives and image IDs are recorded.

Would it be useful to document this callback/output time convention and add this uniform transient MMS as a regression case? If the old-time evaluation is intentional, an explicit example would help users avoid comparing an updated state against a reference at the displayed old time. If the intended callback time is the updated time, a fix would need to review all consumers and time schemes rather than applying the diagnostic edit blindly.
