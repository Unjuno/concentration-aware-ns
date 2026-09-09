# Alternative derivative control for uniform OpenFOAM fields

`python3 -m tools.compare_openfoam_spectral` reads the archived fields, verifies
cell-center ordering and differentiates their real trigonometric interpolants.
The same operation is applied to exact reference samples. Even-grid Nyquist
cosines use zero nodal first derivative. Independent resolved-mode tests cover
shifted rectangular grids and that convention.

At dt=.001, gradient relative L2 errors at the verified sample points are:

| Grid | Computed field spectral derivative vs analytic gradient | Exact reference spectral derivative vs analytic gradient |
|---|---:|---:|
| 16³ | 0.1103905 | 0.00613694 |
| 32³ | 0.0364009 | 4.94e-9 |
| 64³ | 0.00969271 | 1.62e-14 |

These are gradient-field errors at samples, not differences of scalar maxima.
At n32 and n64 the exact-reference control has very small differentiation error,
whereas the computed field still differs from the analytic gradient. This is
more informative about that field difference than attributing an FD2 peak deficit
to the solver. It still combines the numerical solution, forcing, time integration
and interpolation choices; it does not isolate a software defect.

All five archived cases were evaluated. Evidence, archive hashes and diagnostic
peaks are in evidence/tests/openfoam-spectral-gradient.json. No conclusion about
continuous intersample error or an asymptotic temporal regime is assigned, and
this additional diagnostic does not change frozen acceptance thresholds.

## Vorticity and interpolant divergence

The same gradient tensor gives the following additional diagnostics at dt=.001:

| Grid | Vorticity relative L2 error at samples | Max absolute spectral divergence | Exact-reference spectral divergence control |
|---|---:|---:|---:|
| 16³ | 0.0820121 | 1.07951 | 0.0342579 |
| 32³ | 0.0333806 | 0.259365 | 2.47e-8 |
| 64³ | 0.00900724 | 0.0525131 | 6.01e-13 |

Divergence is nondimensional and not normalized by a declared acceptance scale.
It describes the trigonometric interpolant of cell-centered velocity. It is not
the finite-volume face-flux continuity residual enforced by the solver. A nonzero
value does not itself demonstrate a discrete conservation bug. The n16 reference
control also has visible aliasing; n32/n64 controls are much smaller. These
measurements preserve the distinction between the reconstructed field's
incompressibility and the solver's native discrete constraint.
