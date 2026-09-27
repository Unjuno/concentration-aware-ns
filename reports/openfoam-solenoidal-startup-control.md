# Initial discrete-divergence intervention

All three frozen control cases completed with exit 0, complete End logs, and
1/1, 2/2 and 4/4 converged steps. The archive-only checker verifies the original
prepared input hashes before measuring any fields. Reproduce with
`python3 -m tools.check_openfoam_solenoidal_control`.

Only initial U differs from the baseline. The minimum-L2 projection changes its
relative norm by about 0.0026324 and reduces centered discrete divergence below
1e-12. Pressure, forcing, periodic boundary dictionaries and solver settings are
retained. This is a changed initial-value problem, not an original MMS accuracy
acceptance case.

| dt | Original first-step impulse RMS | Control impulse RMS | Control/original | Control first-step pressure range |
|---|---:|---:|---:|---:|
| 0.001 | 2.71564144e-4 | 8.22690044e-6 | 0.0302945 | 0.39100573 |
| 0.0005 | 2.71561436e-4 | 4.11802094e-6 | 0.0151642 | 0.39141438 |
| 0.00025 | 2.71585278e-4 | 2.06010573e-6 | 0.00758548 | 0.39160805 |

Impulse means dt times the RMS of pressure after subtracting its spatial mean.
Cells have equal volume. First-step observations occur at t=dt, not a common
physical time. The baseline impulse stays approximately constant; the control
impulse approximately halves with dt while its pressure range stays bounded
across this triple. This supports the preregistered prediction that removing
initial discrete divergence removes the leading inverse-dt startup response.
It does not prove a dt-to-zero limit or uniquely isolate divergence from every
other feature altered by the projected initial velocity.

The control first-step relative velocity increments from its own initial field
are 0.00100192035, 0.00050125118 and 0.000250698367. No original-reference error
score is assigned. The three controls and baseline archives, hashes, complete
step measurements, protocol and preparation manifest are preserved under
`evidence/of13-solenoidal-startup-control-v1/`,
`evidence/of13-startup-time-v1/`, and the associated protocol/preparation paths.

The numerical mechanism is now supported by an intervention as well as source
inspection and a leading Poisson model. Whether it causes the late t=0.05
observed temporal order remains unresolved. No OpenFOAM implementation defect,
physical singularity, molecular alignment or viscosity reduction is established.
Quality remains UNCERTAIN; no new upstream report is justified by this result
alone.
