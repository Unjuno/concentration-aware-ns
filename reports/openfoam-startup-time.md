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
