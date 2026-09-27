
## n=16 noninterference and algebra pilot

The isolated diagnostic library was built from the pinned image and loaded from
`/diag/lib/libincompressibleFluid.so`; the original installed library was not
modified. The n=16, dt=0.001, t=0.05 case completed 50/50 converged steps.
Endpoint U, p and phi match the original case byte-for-byte. Ten write-time
pressure-correction calls were recorded at the endpoint, each reporting
`consistent=false`.

Archive-only reconstruction gives relative L2 residual
`||U_before_constraints-(HbyA-rAtU*grad(p))||/||U|| = 2.16e-16` and max absolute
residual `8.88e-16`. The post-constraint velocity is unchanged at the recorded
precision; endpoint U, relaxed pressure and corrected phi match their recorded
snapshots exactly. Pressure relaxation changed pressure by zero in this case.
Thus instrumentation passes the preregistered noninterference check and
reproduces the actual final-call velocity assignment. These are n=16 pilot
results only; they do not explain the n=64 accumulated temporal discrepancy.
The archive and replay output are in `evidence/of13-pressure-reconstruction-pilot-v6/`.


## n=64 endpoint extension (partial, 2026-09-28)

A frozen protocol extended the n=16 diagnostic to the original n=64 three-dt cases. The first `dt=0.001` run reached `End` after 50 converged steps and recorded 14 write-time correction calls. Its first runner used Docker `--rm` and then failed to inspect the removed container, so the exit status is unavailable. The endpoint diagnostic fields and run logs are preserved as `evidence/of13-pressure-reconstruction-n64-v1/n64-dt0.001-unverified-exit.tar.gz`; this case remains UNCERTAIN. The diagnostic library was subsequently rebuilt from the same source used in the n=16 pilot and its hash matches that source; however, repeated Docker image-inspect timeouts occurred before any v2 solver case started. The remaining two dt values have no diagnostic evidence. The v2 build and execution state are recorded in `evidence/of13-pressure-reconstruction-n64-v2/execution-status.json`.

Forensic reconstruction of the preserved endpoint gives a relative velocity-update identity residual of `2.12e-16` and max absolute residual `8.88e-16`. The pressure correction, pressure relaxation, and constraints match the recorded final fields to roundoff (observed relative changes 0); `U`, `p`, and `phi` are byte-identical to the same-dt baseline. These checks establish endpoint algebra and diagnostic noninterference for this preserved case only. They do not explain the temporal-order result: 14 correction calls occur at the final output time, earlier trajectory corrections were not retained, and the n=64 dt triple is incomplete. The archived-field replay is `PYTHONPATH=. python3 tools/replay_openfoam_pressure_n64_partial.py`; its output is `evidence/of13-pressure-reconstruction-n64-v1/dt0.001-forensic-review.json`. Protocol v2 was frozen for a retry, but the runner timed out during image inspection before starting any cases; see `evidence/of13-pressure-reconstruction-n64-v2/execution-status.json`.
