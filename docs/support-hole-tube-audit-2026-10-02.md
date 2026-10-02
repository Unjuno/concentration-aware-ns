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
domain. The transverse radius is at most `rho*sqrt(tau)`, while `q>=tau`.
Taking `rho=c/2` places the tube strictly inside the candidate hole
`r<c*sqrt(q)`.

The sublinear envelope, tube axial-power inequality, source-chart identity,
and actual `physicalQ` lower/conditional upper bounds are now Lean-checked in
[`SupportHoleTube.lean`](../verification/SupportHoleTube.lean), with the
source hash and axiom report in
[`support-hole-tube.json`](../evidence/lean-verification/support-hole-tube.json).
The remaining tube input is the trajectory-center estimate
`|z_X(t)|<=B*tau^D` and its combination with the spatial distance bound; the
generic Lean lemma accepts those as hypotheses but does not yet instantiate
the actual selected root trajectory.

## Consequence and remaining gates

If those conditions are established uniformly, the Lean-checked germ transfer
gives equality of the full candidate velocity and base on a tube of radius
`rho(Q)=(c/2)*sqrt(1-t0)*sqrt(Q)`, so `r=1/2`. The base Hessian rate
`kappa=40` then applies there. The existing packet comparison gives the
conditional sufficient initial radius order `Q^(Cstretch+39)`.

Still required before reporting that exponent as an established property of
the assembled construction:

1. A Lean derivation of the selected trajectory-center bound and conversion
   from the spatial tube norm to the transverse `profileRadius` inequality.
2. Uniform Lean proofs of physical-domain membership and the cutoff/spatial
   plateau hypotheses on that tube.
3. Numerical or executable values for the positive constants if a concrete
   finite packet, rather than a conditional asymptotic order, is claimed.

Thus the previous argument from compactness alone remains insufficient, but
the source support hole appears to offer a real quantitative replacement. The
current status is **promising conditional route; not yet formally closed**.

## Update — selected localized candidate germ transfer checked (2026-10-02)

Lean now checks the selected initialized potential sum, direct angular sum, curl, periodicization, and time activation transfer: the full candidate velocity equals its base as a germ inside the actual support hole, assuming physical-domain membership, cutoff plateau, late time, and spatial localization. The quantitative tube argument has not yet established these conditions uniformly or instantiated the selected trajectory-center scaling. The finite-packet exponent and all solver/upstream-audit conclusions remain conditional on their independent gates.
