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
  domain. This covers the angular/stream means represented by those families.
- `ActualValidBandWaves.active_zero_germs` and
  `ActualSignedExterior.cycle_zero_germs` give zero germs outside the actual
  active annulus. The lower edge of that annulus is the positive
  `PrimaryTargetBounds.leftRadius`; `profileRadius` is transverse physical
  radius divided by `sqrt(physicalQ)`.

Consequently the common *candidate* coefficient

```
c = min(leftRadius/(4*sqrt(2)), patch.a/4) > 0
```

is consistent with every primitive perturbation family in the selected
assembly. Pointwise sums preserve this hole. The source also has the needed
local-sum mechanisms: `GermCandidateAssembly.potentialSum_eq_base_germ`,
`LocalAngularDiagonal.sum_zero_germ`, and spatial locality of curl. However,
the actual witness has not yet been instantiated through those lemmas with a
single c and one common tube. That remains a Lean proof obligation.

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

This resolves the *geometric scaling calculation on paper*, conditional on the
common primitive support-hole theorem and the actual selected cutoff plateau.
It avoids inferring a power thickness from pointwise openness. No machine-checked
proof of this bound or its source-coordinate identification has yet been added.

## Consequence and remaining gates

If the common-hole assembly lemma is proved, the fields of every perturbation
stage vanish throughout this tube. Local finiteness then makes the potential
sum equal to the selected base there, and the direct angular sum vanishes;
curl preserves equality on the open tube. The base Hessian rate `kappa=40`
then applies there. The tube has `rho(Q)=(c/2)*sqrt(1-t0)*sqrt(Q)`, so `r=1/2`.
The existing packet comparison consequently gives the conditional sufficient
initial radius order `Q^(Cstretch+39)`.

Still required before reporting that exponent as an established property of
the construction:

1. A checked common lower-support constant for every initial, particular,
   signed, mean, and direct field in the exact selected witness.
2. A Lean proof of the `q<=S*tau` tube estimate and its identification with
   the actual `physicalQ` chart.
3. A Lean assembly transfer through the initialized potential sum, direct
   angular sum, curl, and local periodic/time cutoffs, including the selected
   cutoff plateau hypothesis.
4. Numerical or executable values for the positive constants if a concrete
   finite packet, rather than a conditional asymptotic order, is claimed.

Thus the previous argument from compactness alone remains insufficient, but
the source support hole appears to offer a real quantitative replacement. The
current status is **promising conditional route; not yet formally closed**.
