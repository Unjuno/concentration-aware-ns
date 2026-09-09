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
