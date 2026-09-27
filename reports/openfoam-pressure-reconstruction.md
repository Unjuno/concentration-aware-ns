
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
