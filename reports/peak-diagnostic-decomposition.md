# Do not identify a sampled FD2 peak deficit with solver error

Using the exact global reference maximum P, let R be the maximum after sampling
and applying FD2 to the exact reference, and C the reported computed-field FD2
maximum. The signed identity is

    (P-C)/P = (P-R)/P + (R-C)/P.

Reproduce with `python3 -m tools.decompose_peak_diagnostic`. Archived inputs and
all gradient/vorticity values are in evidence/tests/peak-diagnostic-decomposition.json.

For OpenFOAM at dt=.001, gradient percentages are:

| Grid | Exact-reference sampling + FD2 deficit | Difference between FD2 peaks | Total reported deficit |
|---|---:|---:|---:|
| 16³ | 41.9884% | -0.8436% | 41.1448% |
| 32³ | 13.9040% | -0.7839% | 13.1201% |
| 64³ | 3.7589% | -0.3112% | 3.4477% |

Thus the diagnostic applied to the exact field already produces a slightly
larger deficit than the computed-field diagnostic. The negative second term
means the computed FD2 peak is higher than the exact-reference FD2 peak. It does
not mean negative solver error or a more accurate computed field.

Maxima can occur at different locations, and the max operation is nonlinear.
These two scalar terms are not independent causal error components and do not
bound the pointwise field error. Nevertheless, the reference control is enough
to reject interpreting the 13.12% number as an isolated solver error. It primarily
identifies a limitation of this sampled finite-difference diagnostic; solver,
time-stepping and forcing errors require separate field comparisons.

This strengthens the existing decision not to file an OpenFOAM defect report.
It does not establish the broader hypothesis that a complete conventional
verification workflow accepts an inaccurate local quantity. Existing UNCERTAIN
gate outcomes remain unchanged.

The completed SU2 n16 and n32 archives are now included in the generated
decomposition. Their reference-FD2 gradient deficits are 28.1304% and 7.99182%,
while total computed-FD2 deficits are 37.4451% and 11.2359%. See
[the alternative spectral comparison](su2-spectral-gradient.md) for the same
velocity fields evaluated with a different derivative diagnostic.
