# Early-time trace: two completed cases, final case pending

Protocol of13-startup-time-v1 retains the completed tight-tolerance n=64
initial fields and settings, changing only endTime to 0.001 and writeInterval
to each dt. It records every step's U, p and phi at dt=0.001,0.0005,0.00025.
This common-endpoint diagnostic does not alter startup projection or establish
its causal role in the long-run timestep differences.

The first two runs completed with exit zero and all 1 and 2 steps reporting
outer convergence. Their full input/log/field archives are preserved in
`evidence/of13-startup-time-v1`. The dt=0.00025 run remains pending: the host
runner and docker-run processes are alive, but no log.foamRun exists and the
container output log is empty. A separate docker-ps request also remains
pending. This is an execution-infrastructure observation, not a solver failure.
No duplicate run or Docker restart was performed.

The postprocessor `python3 -m tools.check_openfoam_startup_time` requires all
three completed cases before producing the comparison. The runner is
`python3 -m tools.run_openfoam_startup_time`; it rejects existing roots.
Preserve the current process until its actual terminal state is known.

## Completed-case startup signature

An archive-only replay now records every saved step of the two completed runs,
without attempting a three-level order estimate. At the first step:

| dt | Pressure max-minus-min | dt times pressure range | Relative velocity error |
|---:|---:|---:|---:|
| 0.001 | 4.90482721 | 0.00490482721 | 0.00255682952 |
| 0.0005 | 9.81041059 | 0.00490520530 | 0.00255551843 |

At the second dt=0.0005 step (t=0.001), pressure range falls to 0.389672216.
Reference pressure is zero; range is used to avoid dependence on pressure gauge.
The first-step inverse-dt pressure scaling, nearly constant dt*range, and
similar first-step velocity errors are consistent with a discrete startup
projection response. They are not proof that this mechanism causes the
long-run observed order: first steps are at different physical times, only two
timesteps are complete, and no causal intervention has been run. A large
startup pressure here is not evidence of continuum blow-up or physical hazard.

`python3 -m tools.check_openfoam_startup_partial` reads completed archives in
temporary directories and explicitly reports 2 of 3 cases and no evaluated
three-case order. Its output is `partial-step-diagnostics.json`; the missing
case remains pending and is not classified as passing or failing numerically.
