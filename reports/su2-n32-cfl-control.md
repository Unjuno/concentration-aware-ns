# SU2 n32 first-step CFL control

The preregistered single-step control completed with CFL=100 and the unchanged
3,000-iteration cap. All four log10 residuals fell below -10 after 1,441
iterations. The baseline CFL=10 first step exhausted 3,000 iterations without
meeting that threshold. Full inputs, outputs and logs are archived in
evidence/su2-n32-cfl-control-v1/case.tar.gz with its hash in summary.json.

The maximum velocity-component difference from the saved baseline first-step
field is 4.19e-8 at matched point IDs and coordinates. This comparison includes
an unconverged baseline; it is not an independent uncertainty bound. The control
velocity relative L2 error against the analytic field at t=.001 is 0.00214261.

This supports a configuration-level explanation for the baseline's initial
residual deficit in this one step. It does not prove full-horizon accuracy,
general optimality of CFL=100, or wall-clock speedup. The frozen baseline sweep
continues unchanged and must retain its unconverged initial steps in its report.

A direct configuration diff is saved in evidence/su2-n32-cfl-control-v1/config.diff.
Besides CFL=10 to 100, the control changes MAX_TIME=.05 to .001 and TIME_ITER=50
to 1, adds PARAVIEW_ASCII output, and changes output frequency from 50 to 1.
All other configuration lines match. The comparison concerns the common first
physical step, not runs with identical horizons or output workloads.
