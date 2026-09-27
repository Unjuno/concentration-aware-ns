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

## Leading discrete Poisson model

On the fixed periodic grid, if rAU=dt+O(dt²) and HbyA=U0+O(dt),
and the remaining corrected-flux terms do not change the leading startup
balance, the pressure equation suggests

```
L_h pi = D_h U0, mean(pi)=0,
p = pi/dt + O(1).
```

Here D_h is centered divergence of arithmetic face flux and L_h is the uniform
nearest-neighbor Laplacian. These are a leading-balance model's assumptions,
not proved asymptotics of the full PIMPLE iteration. The model is solved using
the exact discrete Fourier symbol -sum(4*sin(k_j*dx/2)^2/dx²), not a continuum
Laplacian substituted for the discrete operator. Real-space residual is below
4.6e-16. The input is only initial U, not fitted observed pressure.

Comparing pi with gauge-centered dt*p at each run's first step gives relative
L2 differences 0.0302216 (dt=0.001) and 0.0151275 (dt=0.0005), with directional
cosines 0.999543 and 0.999886. The residual approximately halves with dt. The
predicted impulse range is 0.00490576, compared with 0.00490483 and 0.00490521.
This is more specific support for a startup projection interpretation than the
range scaling alone. It is a post-hoc model comparison, not a calibrated
acceptance test or evidence about the missing third run. It does not explain
the later temporal-order behavior by itself.

`python3 -m tools.check_openfoam_startup_poisson` reproduces the model and
records pressure/initial-field hashes in `poisson-model.json`. Finite-dt
transport, forcing and the full ddtCorr/PIMPLE behavior remain outside this
leading model. No singular physical pressure follows from a fixed-grid
initialization response as dt is changed.

## Velocity-side check of the same leading model

The same pi predicts a cell velocity correction -G_h pi, using centered
cell-gradient G_h. Its norm relative to the recorded initial U is 0.00255493239.
No observed velocity is fitted to construct this correction. Subtracting the
known continuum evolution exp(-dt)*U0 from each first-step velocity, the
relative residual against -G_h pi is 0.0337911 and 0.0169169 for dt=0.001
and 0.0005. The respective direction cosines are 0.999429 and 0.999857.
Thus both pressure impulse and velocity error approach the same leading
startup balance over these two runs, with approximately halving discrepancies.

The predicted 0.2555% initial correction is a fixed-grid discrete effect; it
is not a proof of a nonzero continuum limit. These first-step comparisons are
at different physical times. In addition, the collocated G_h,D_h composition
is not the nearest-neighbor pressure Laplacian L_h, so this cell-velocity map
must not be called an exact discrete Helmholtz projection without specifying
the relevant face/cell operators. The full solver uses corrected face flux
and cell velocity separately. Causal intervention and the later-time behavior
remain unresolved; Docker's third-case request is still pending.
