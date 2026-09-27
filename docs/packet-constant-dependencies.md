# Extracting the constants needed for a packet certificate

The [packet estimate](axis-packet-bound.md) requires a spacetime tube where
the actual assembled field equals its smooth base, a tube radius rho, and a
uniform spatial Hessian bound M. This audit identifies which source results
supply existence and which data still lack numerical certificates.

Source inspection was refreshed on 2026-09-28 against OpenAI commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, the only commit after the prior
pin `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` (188 Lean files changed or
added). The refresh adds actual-base velocity and pressure jet-rate estimates
to the evidence inventory below. No coefficient values or ODE trajectory were
sampled to infer bounds.

The current source-bound extension reports record the checks of the stated
lemmas against both pins. These are checks of identities and the acceptance
path, not numerical extraction.

## A uniform derivative bound can be transferred

`SlowBorelBase.compact_jet_bound` gives, for a smooth function on an open
domain and any compact subset K, a uniform bound for each prescribed
iterated derivative order. `FinalSlowBase.velocity_smooth` supplies smoothness
on `BaseResidual.past`, the open spacetime domain t<1.

The extension `compact_jet_bound_from_selected_base_germs` now joins those
facts to neighborhood equality: if the assembled velocity agrees locally
with that selected base at every point of compact K contained in t<1, then

    exists M >= 1, for every w in K: ||D^m u(w)|| <= M.

This is a uniform bound over K, not separate unrelated constants at its
points. Its hypothesis is neighborhood equality throughout K. Equality on
the axis alone would not supply a bound on a tube. The classical open-union
and compact-tube construction in the flow note supplies such a K existentially.

At m=2 the new lemma `spatial_jet_norm_le_spacetime_jet_norm` formalizes the
restriction to fixed-time spatial directions via the norm-one linear map
v -> (0,v). Thus the same existential bound controls the spatial Hessian on
K, provided the stated neighborhood-equality hypothesis holds.

The refreshed upstream source also contains `ActualBaseVelocityBounds` and
`ActualBasePressureBounds`. These give polynomial-in-similarity-radius bounds
for each prescribed derivative order on the actual base fields, including a
whole-endpoint pressure rate after gluing to the heat exterior. They narrow
the analytic growth question but remain existential `JetRate`/`FiniteJetRate`
statements: compact derivative maxima and the selected profile/scales are not
numerically enclosed or made executable by those estimates. They do not
establish `PressureData` for `actualProfile`, nor produce a spacetime tube
radius or chart lower bound.

### Endpoint rate transferred to shrinking packets

There is a further conditional consequence when the actual-base rate is joined
to the selected-root trajectory. At derivative order two,
`ActualBaseVelocityBounds.velocity_rate` uses
`heatLoss(2)=(4*2+2)*(2+2)=40`, so it supplies an existential endpoint bound

```
||D^2 u(w)|| <= C2*q(w)^(-40)
```

for all w in some unspecified endpoint neighborhood. The locally checked
`spatial_jet_norm_le_spacetime_jet_norm` transfers this to the spatial Hessian.
The similarity identity is `tau=q*(1-eta^2)` with `|eta|<1`; hence `q>=tau`
and on `[t0,T]` the half-Hessian factor is at most
`k(Q) <= (C2/2)*tau0^(-40)*Q^(-40)`, where `tau0=1-t0` and
`Q=(1-T)/tau0`.

The selected center curve is `X(s)=K*(1-s)^D`, with
`K=eta/(1-eta^2)^D` and `D=(1-2h)/2` in `[0.499,0.5)`. For a fixed `rho0>0`,
choose the interval start `t0` sufficiently close to 1 and use the constant
radius `rho(Q)=rho0*Q^D` over `[t0,T]`. Since `Q^D <= ((1-s)/tau0)^D` for
`s<=T`, the spatial distance from the tube to the terminal point is at most
`(|K|+rho0)*tau0^D`. The time-coordinate distance is at most `tau0`, and
`tau0<=tau0^D` for `0<tau0<=1` and `D<1`. Thus the full spacetime distance is
at most `(1+|K|+rho0)*tau0^D`. The tube fits the existential endpoint
neighborhood after choosing `t0` sufficiently close to 1. This proves
the endpoint-envelope hypotheses of the classical packet comparison
existentially, with `r=D` and `kappa=40`.

Substitution into the already checked envelope algebra gives the sufficient
initial packet-radius power
`delta(Q)=O(Q^(Cstretch+39))`, where `Cstretch` is the axis stretching
coefficient in `docs/axis-stretch-range.md`. This is roughly a power of 43.
The exact exponent is retained because the coefficient is not exactly four.
This is a real analytic strengthening over leaving the tube/Hessian exponents
wholly hypothetical: it derives a shrinking-packet envelope from the pinned
source's rate statement and the exact chart/trajectory geometry.

It still gives no explicit prefactor, no numerical interval for `t0`, no
particular positive `rho0`, and no executable packet certificate. The
source-rate constant and endpoint neighborhood are existential; the argument
that the nonlinear flow follows its tangent map remains classical. Because
`delta(Q)` tends to zero, this does not certify a fixed-size packet up to the
singular time and does not imply molecular alignment or a constitutive law.

## Finite-stage cutoff with a known chart lower bound

There is also a useful finite reduction. Suppose q_chart>=qmin>0 throughout
a proposed compact tube, and the natural-valued cutoff schedule a is strictly
increasing. Then a(j)>=j. Choose a natural J with J*qmin>1. For every j>=J,

    a(j)*q_chart >= j*qmin >= J*qmin > 1.

`SlowBorelBase.powerStage_jet_zero` then makes every derivative order of
that cutoff stage zero. The new extension lemma
`cutoff_stage_jets_zero_above_index` checks this implication for arbitrary
scalar coefficients, exponents and derivative orders.

The subsequent extension now checks the complete scalar finite-sum replacement:
`slowSum_eq_cutPrefix_of_index` identifies `slowSum` with `cutPrefix` whenever
q_chart>0 and J*q_chart>1. The source `cutPrefix J` includes indices 0 through
J; its index-J term is zero under this condition. The leading profile is
retained separately. No uncut prefix is substituted for the cutoff prefix.

`slowSum_eventuallyEq_cutPrefix_of_index` establishes equality on a common
neighborhood, and `slowSum_jet_eq_cutPrefix_of_index` transfers all derivative
orders. No coefficient regularity premise is needed for these locality
identities; using the resulting derivatives as classical smooth derivatives
still requires the existing smoothness facts. Finally,
`physicalProfile_eventuallyEq_cutPrefix_of_index` retains neighborhood equality
after the physical-chart composition and multiplication by its q-power.

A valid qmin must bound the chart coordinate on the **whole tube**. Substituting
its value only on the axis would leave a gap. Equality for the scalar physical
profiles is not yet an executable finite formula for the complete assembled
velocity with every primitive, spatial curl and profile parameter extracted.

This reduction avoids estimating an infinite tail on a compact interval away
from t=1. It does not make the remaining coefficient functions or cutoff
scales numerically available by itself.

## Why this is not yet a numerical packet certificate

| Input | Inspected source evidence | Missing numerical content |
|---|---|---|
| Profile and modulation | `FinalSlowBase.actualProfile` uses `Classical.choice profileData_nonempty` | An executable representative or certified enclosures for the selected coefficient functions |
| Base cutoff scales | `EntranceAlignedBase.scales` uses `Classical.choose exists_admissibleScales`; `FinalSlowBase.scales_spec` retains admissibility | Values or upper/lower interval certificates for the finite active scales |
| Template derivative bound | `SlowBorelBase.exists_template_jet_bound` takes a compact continuous-derivative bound | A computed enclosure for that compact maximum |
| Physical tube | Terminal base-germ transfer and compactness give a neighborhood | Explicit radius and chart-coordinate lower bound valid throughout it |
| Finite-prefix Hessian | Finitely many smooth terms and chart derivatives | Certified derivative enclosures after composition and multiplication |

The existing `exists_cartesian_profile_tail` theorem is another possible
route, but its J, delta and C are existential and depend on admissible scales
and compact chart-derivative bounds. It is not an already available numerical
Hessian constant. Likewise the stress-weighted estimates cannot be substituted
for a velocity Hessian estimate without proving the relevant derivative link.

These are limits of the extracted evidence, not a theorem that numerical
realization is impossible. A future certificate can provide rho, qmin, the
finite active data and derivative enclosures, then use the explicit packet
inequality. The existence/transfer, stage-vanishing and scalar finite-prefix
locality steps are formalized. No particular finite packet is certified, and no pressure
condition or material-viscosity conclusion follows from these bounds.

## Source anchors

- [Compact derivative bounds and cutoff jets](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/SlowBorelBase.lean)
- [Chosen scales](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/EntranceAlignedBase.lean)
- [Actual profile and smooth base velocity](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/FinalSlowBase.lean)
