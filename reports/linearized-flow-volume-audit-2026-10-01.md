# Linearized material-flow volume and covariance audit

Date: 2026-10-01  
Source: `openai/NavierStokesAndEuler@f9e8bc5b38b6e212696e8a30e3e91517af887bbd`  
Verification: full `AxisForceSign.lean` extension in the pinned, network-isolated Lean checker.

## Formal result

The selected axis variational model has two transverse scale factors
`Q^(C/2)` and an axial scale factor `Q^(-C)`, together with a planar rotation.
Lean now proves

```
terminalScale(t0,C/2,t)^2 * terminalScale(t0,-C,t) = 1
```

for every `t0,t < 1` and real `C`. The left side is the diagonal scale-volume factor. The explicit planar
rotation in `axisDeformation` has unit area factor, and the two transverse
scales contribute the square of the first term; together these give unit
volume factor for the stated linearized map. The Lean theorem isolates the scale
product, while the covariance-product identity checks its Gaussian consequence.
A second Lean identity proves that the product of the three transported
isotropic Gaussian covariance eigenvalues remains `sigma^6`. The new declarations
are `ConcentrationAware.terminalScale_volume_factor` and
`ConcentrationAware.isotropic_covariance_determinant_preserved`; each has only
`propext`, `Classical.choice`, and `Quot.sound` in its axiom report. Full checker
output is archived at
`evidence/lean-verification/axis-volume-covariance-2026-10-01.log`.

## Interpretation limits

This machine-checks the linearized continuum variational map on the selected
trajectory. It supports the exact volume-preservation step in the existing
linearized-Gaussian positional-probability calculation. It does not itself prove
the Gaussian probability bound or a nonlinear finite-packet estimate; those
remain in their separately documented scopes. It does not model molecules,
finite particle size, molecular orientation, phase transitions, or changing
constitutive viscosity. The result therefore challenges the shortcut from
directional alignment to increased certainty around the packet center, but does
not determine real-particle statistics.
