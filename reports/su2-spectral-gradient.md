# SU2 derivative diagnostics: FD2 versus spectral reconstruction

The same completed n16 and n32 SU2 velocity archives were differentiated using
the real periodic trigonometric interpolant. Coordinates are independently
sorted and checked against the full endpoint-inclusive Cartesian lattice before
periodic duplicates are removed. Both cases have zero duplicate velocity
mismatch. The evaluation time is the completed-update time t=0.05; the old-time
forcing convention is unchanged.

| Grid | FD2 gradient peak deficit | Spectral gradient peak deficit | Spectral gradient relative L2 error at vertices | Exact-reference spectral gradient relative L2 error |
|---|---:|---:|---:|---:|
| 16³ | 37.4451% | 16.0654% | 16.4471% | 1.51585% |
| 32³ | 11.2359% | 3.43390% | 4.11109% | 0.00000234133% |

Peak deficits compare the sampled diagnostic maximum with the analytically
known global reference maximum. They do not bound the continuous maximum of
the reconstructed computed field. The L2 columns compare tensors at matching
vertices, which is a different quantity from comparing their scalar maxima.

For vorticity, the spectral peak deficits are 16.3764% and 3.43976%; the
corresponding relative L2 errors at vertices are 16.1250% and 4.07611%.
The analytic reference control uses the same grid and spectral operator, with
its derivative checked against the analytic formula. Its small n32 error
applies to that reference field, not to every possible numerical field.

The signed FD2 decomposition for SU2 gives:

| Grid | Reference sampling and FD2 deficit | Difference between FD2 peaks | Total deficit |
|---|---:|---:|---:|
| 16³ | 28.1304% | 9.31468% | 37.4451% |
| 32³ | 7.99182% | 3.24409% | 11.2359% |

These terms satisfy (P-C)/P=(P-R)/P+(R-C)/P, where P is the exact global
reference peak, R the reference FD2 peak and C the computed FD2 peak. This
identity is not a causal decomposition or a pointwise error bound. Nevertheless,
the reference control prevents attributing the full 11.24% deficit to SU2.
Changing the diagnostic on the same n32 field also moves the sampled peak
discrepancy across the protocol's 5% local threshold; it does not establish a
certified local PASS or justify changing the frozen protocol retrospectively.

Maximum absolute divergence of the spectral reconstruction is approximately
1.60229 for n16 and 0.0998507 for n32, compared with 0.00657974 and 2.62111e-9
for the analytic-reference reconstruction. This diagnostic differs from SU2's
native discrete continuity residual. No upstream defect is inferred from it.

Both completed cases still exceed the velocity L2 threshold, and n32 also fails
the residual criterion at two updates. The full three-resolution/time-step
matrix remains incomplete. Neither this diagnostic comparison nor the small
reference reconstruction error upgrades the acceptance gate.

Reproduce from the repository root:

```sh
python3 -m tools.compare_su2_spectral
python3 -m tools.decompose_peak_diagnostic
```

Evidence is in `evidence/tests/su2-spectral-gradient.json` and
`evidence/tests/peak-diagnostic-decomposition.json`, including archive identities.
The new vertex reader is tested with shuffled rows, a duplicated coordinate
replacing a missing one, and a discrepant periodic endpoint. Analytic sinusoidal
fields independently check derivative directions and components.
