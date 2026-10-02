# Re-audit of the support-hole tube route

This is a source-bound analytic audit of the proposed repair to the finite
packet tube-radius gap. It is not a completed Lean theorem or a numerical
certificate. The OpenAI construction is pinned at
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.

## Correct distinction in the source

`MixedDiagonalExtensions.SublevelShrinkingSupport` is an *outer* support
estimate: a nonzero value at small `physicalQ` can occur only at radius at
most `C*sqrt(physicalQ)`. By itself it says nothing about a zero region near
the axis. The relevant inner-hole facts are separate:

- `InitialPhysicalData` supplies `LocalPhysicalCopyBounds.SupportData` for the
  actual initial potential family. The extension
  `verification/SupportHole.lean` proves the resulting copy sum is zero below
  `a*sqrt(physicalQ/2)`.
- `ActualMeanStageData.coefficient_vanishes` proves each actual native mean
  coefficient is zero below `(patch.a/4)*sqrt(physicalQ)` on its stated slow
  domain. More strongly for the selected construction, its exterior assembly
  lemmas place the stream and angular means outside the active annulus.
- `ActualValidBandWaves.active_zero_germs` and
  `ActualSignedExterior.cycle_zero_germs` give zero germs outside the actual
  active annulus. The lower edge of that annulus is the positive
  `PrimaryTargetBounds.leftRadius`; `profileRadius` is transverse physical
  radius divided by `sqrt(physicalQ)`.

The common coefficient for the exact selected stage fields is therefore

```
c = PrimaryTargetBounds.leftRadius > 0
```

and its stage-level implication is now Lean-checked in
[`SupportHoleAssembly.lean`](../verification/SupportHoleAssembly.lean): the
initial potential, every positive-potential stage, and every direct angular
stage vanish pointwise whenever `profileRadius<leftRadius` within the actual
physical domain. This is stronger and more specific than combining generic
primitive lower radii. `SupportHoleAssembly.lean` now Lean-checks the selected
transfer at the germ level: the initialized potential sum equals the base
germ, the direct angular sum vanishes, and the complete periodic and time
activated candidate velocity equals the base germ. These implications require
the pointwise physical-domain, zeroth-cutoff plateau, late-time, and spatial
localization conditions stated in the theorem. Pinned source hashes and axiom
reports are in
[`support-hole-assembly.json`](../evidence/lean-verification/support-hole-assembly.json).

## Quantitative chart-domain check

The previously uncertain domain-width step has a direct route. Put
`a=2h`, `D=(1-a)/2=1/2-h`, `tau=1-t`, and let the axial trajectory be

```
z_X(t) = eta*(tau/d)^D,       d=1-eta^2>0.
```

On a spatial tube of radius `rho*sqrt(tau)` around this axis, with `0<tau<=1`,
the axial coordinate satisfies

```
|z| <= K*tau^D,       K=|eta|*d^(-D)+rho,
```

because `D<1/2` implies `sqrt(tau)<=tau^D`. The pinned coordinate equation is
`tau=q-z^2*q^a`, so `q>=tau`. With `s=q/tau`, the same equation gives

```
s = 1 + z^2*tau^(a-1)*s^a <= 1 + K^2*s^a.
```

Since `0<a<1`, this implies

```
q <= S*tau,    S=max(2,(2*K^2)^(1/(1-a))).
```

Indeed, if `s<2` the bound is immediate; if `s>=2`, then
`s/2 <= K^2*s^a`. Therefore choosing `t0` so
`S*(1-t0)<qbig` keeps this entire shrinking tube in the local `q<qbig`
domain. The earlier `sqrt(tau)` tube does **not** automatically fit inside
the hole: `r<=rho*sqrt(tau)` and `q>=tau` only give
`r<=rho*sqrt(q)`, so strict inclusion requires the additional coefficient
condition `rho<c`. The axial `q<=S*tau` estimate supplies no such constant
margin. A corrected transverse tube of radius `rho*tau`, `0<rho<c`, does fit:
on the distinguished root axis `q=tau/d`, where `d=1-eta^2` and `0<d<=1`,
so `q>=tau` and `tau<=sqrt(q)` for `tau<=1`.
`transverse_tau_tube_inside_selected_hole` checks
`r<=rho*tau < c*sqrt(q)` in Lean. This tube shrinks with terminal time; it
is not a fixed-width particle packet.

The sublinear envelope, tube axial-power inequality, source-chart identity,
and actual `physicalQ` lower/conditional upper bounds are now Lean-checked in
[`SupportHoleTube.lean`](../verification/SupportHoleTube.lean), with the
source hash and axiom report in
[`support-hole-tube.json`](../evidence/lean-verification/support-hole-tube.json).
The pinned `AxisForceSign.lean` separately proves the actual selected root
trajectory and eventual base-germ transfer. To lift the scalar result to a
Euclidean spatial tube, use the radial projection norm bound (with its
explicit constant) and the global lower bound `physicalQ>=tau`; closeness of
`physicalQ` to its root-axis value is not required for the support-hole
inequality. The separate upper bound `q<=S*tau` is still needed to stay in the
construction sublevel.

## Consequence and remaining gates

If these conditions are established uniformly, the selected trajectory theorem
gives base equality on an open spacetime neighborhood of each axis point. The
`rho*tau` transverse support-hole argument yields a candidate terminal tube
radius proportional to `Q`, hence `r=1`. Combined conditionally with the base
Hessian rate `kappa=40`, the packet comparison gives the sufficient initial
radius order `Q^(Cstretch+39)`. This is a shrinking packet scale, not a claim
about fixed-size molecular alignment.

Still required before reporting that exponent as an established property of
the assembled construction:

1. Lift the scalar support-hole inequality to the 3D radial projection using
   its norm bound, choosing the Euclidean tube coefficient below half the
   support-hole coefficient.
2. Uniformly prove physical-domain membership using `q<=S*tau`, then the
   zeroth-cutoff plateau, late-time condition, spatial plateau, and required
   regularity bounds on that tube.
3. Numerical or executable values for the positive constants if a concrete
   finite packet, rather than a conditional asymptotic order, is claimed.

Thus the previous argument from compactness alone remains insufficient, but
the source support hole appears to offer a real quantitative replacement. The
current status is **promising conditional route; not yet formally closed**.

## Update — selected localized candidate germ transfer checked (2026-10-02)

Lean checks the selected initialized potential sum, direct angular sum, curl, periodicization, and time activation transfer as a germ under explicit conditions. The pinned `AxisForceSign.lean` also proves an eventual terminal base germ and material trajectory for the actual selected construction. Separately, `SupportHoleTube.lean` proves a `rho*tau` transverse-radius inequality on the distinguished root chart. The bridge from that scalar inequality to the actual full-space support-hole condition, uniformly on a tube with all domain/cutoff/plateau hypotheses, remains unproved. The packet exponent and all solver/upstream-audit conclusions remain conditional on their independent gates.
