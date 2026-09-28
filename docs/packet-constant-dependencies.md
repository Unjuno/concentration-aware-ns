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

### Endpoint Hessian rate and the missing tube-radius transfer

At derivative order two, `ActualBaseVelocityBounds.velocity_rate` uses
`heatLoss(2)=(4*2+2)*(2+2)=40`. It supplies an existential endpoint bound
`||D^2 u_base(w)|| <= C2*q(w)^(-40)` on an unspecified neighborhood for the
selected smooth base velocity. The locally checked
`spatial_jet_norm_le_spacetime_jet_norm` transfers this to the spatial Hessian.
On the similarity chart, `tau=q*(1-eta^2)` and `|eta|<1`, so `q>=tau`.
Consequently, wherever the assembled field is known to equal that base, the
half-Hessian factor on `[t0,T]` is at most
`(C2/2)*tau0^(-40)*Q^(-40)`, with `tau0=1-t0` and `Q=(1-T)/tau0`.

This does **not** establish the earlier claimed tube radius
`rho(Q)=rho0*Q^D` or the resulting `Q^(Cstretch+39)` packet-radius order for
the assembled field. `actual_candidate_terminal_base_germ` gives neighborhood
equality at each point of the selected trajectory. For every fixed compact
terminal interval, compactness and openness yield some positive tube radius;
they give no lower bound on how that radius depends on `T` as `T` approaches
1. The tube's geometric closeness to the endpoint only places it inside the
base's endpoint-rate neighborhood; it does not place it inside the separate
open union where the assembled field equals the base. These two neighborhoods
cannot be conflated.

This is a genuine quantifier issue: an open neighborhood of every point on a
nonclosed terminal graph need not have any power-law thickness near its limit.
For example, the open set
`O={(t,x): t<1, |x-X(t)|<exp(-1/(1-t))}` contains a spatial neighborhood of
each graph point. On `[t0,T]` its largest uniform tube radius is at most
`exp(-1/(1-T))`, which decays faster than every power of
`Q=(1-T)/(1-t0)`. This example is not a model of the constructed velocity; it
shows why openness and compactness alone cannot prove the missing power lower
bound.

The generic algebra in `tools.check_packet_radius_scaling` remains valid under
its explicit assumptions. To instantiate it for this construction, one still
needs a quantitative lower envelope for the assembled-field base-equality
tube radius (or another direct Hessian estimate for the assembled field) as
well as the classical nonlinear-flow argument. Until then the packet exponent
is conditional on such an envelope, not an established result for the selected
construction. No fixed-size packet or molecular conclusion follows.

The finite-stage cutoff lemmas do not close this gap by themselves. If a whole
tube has `q_chart>=qmin`, choosing `J=floor(1/qmin)+1` makes every stage
`j>=J` vanish there because `a(j)>=j` and `J*qmin>1`. But the retained prefix
has O(1/qmin) stages, and the axis-zero germ hypotheses give a possibly
stage- and point-dependent neighborhood for each retained stage. The checked
finite-prefix identities preserve equality and jets; they provide neither a
uniform neighborhood radius for that growing prefix nor numerical derivative
enclosures. A quantitative support-width theorem uniform over the relevant
stages, or direct bounds for the assembled field, is still required.

## New support-hole route inspected on 2026-09-28

The pinned source has a potentially stronger route than the finite-prefix
germ argument: its actual perturbation ingredients have **positive inner
support radii**, not merely axis-zero germs. The relevant exact source facts
are:

- Initial copy potentials use `InitialPhysicalData.innerRadius =
  PrimaryTargetBounds.leftRadius / 4`. Their `SupportData.geometry_support`
  puts every nonzero copy term in a normalized annulus. Since the active band
  obeys `physicalQ/2 <= Q_n`, physical radius is at least the annular inner
  radius times `sqrt(Q_n)`, hence at least
  `PrimaryTargetBounds.leftRadius/(4*sqrt(2))*sqrt(physicalQ)`.
- Actual particular fields use `BandAnnulus` support in
  `ActualCurrentWaveSupport`: nonzero terms have
  `profileRadius >= PrimaryTargetBounds.leftRadius`. The signed exterior field
  is supported in `ActualPolarCoverage.active`, whose lower edge is
  `activeLeft`; the identity `profileRadius^2/2 = cartesianChart_X` gives the
  same physical-radius bound. Since
  `profileRadius = physical radius/sqrt(physicalQ)`, both are outside
  `PrimaryTargetBounds.leftRadius*sqrt(physicalQ)` on their valid regions.
- Every constructed angular/stream mean family uses
  `ActualMeanStageData.innerRadius = (ActualInitialization.geometry.patch.a/4)
  * sqrt(physicalQ)`, and `coefficient_vanishes` proves the scalar coefficient
  is zero below that radius.

Thus a candidate common support-hole coefficient for all these primitive
components is

    c0 = min(leftRadius/(4*sqrt(2)), patch.a/4) > 0.

At any point in their validity regions, every perturbation component vanishes
when its transverse radius `r < c0*sqrt(physicalQ)`. The chart identity
`tau = q*(1-eta^2)` gives `physicalQ=q >= tau`; hence a spatial tube around an
axial center curve with

    rho(Q) = (c0*sqrt(tau0)/2) * sqrt(Q),
    tau = tau0*Q,

would lie strictly inside this support hole, provided the tube remains in the
bands/domains where the cited support facts apply. On such a tube, the
perturbation **fields themselves**, not only their germs at the axis, are zero.
If all stage and direct-field sums inherit this common pointwise support hole,
the assembled velocity equals its smooth base there. This would provide the
previously missing power-law tube envelope with `r=1/2`; combined with the
base Hessian rate `kappa=40`, the generic packet exponent would again be
`Cstretch+39`, conditionally on all remaining hypotheses and constants.

The initial-copy part is now formalized in
`verification/SupportHole.lean` as
`copy_sum_zero_below_physical_hole`. It states that any `CopyFamily` satisfying
the pinned `SupportData` contract is exactly zero when its physical radius is
below `a*sqrt(physicalQ/2)`. It was compiled against the pinned OpenAI source
and Lean environment after deriving the witness through
`SupportData.sum_support`, `labelRegion_active_relation`, and the explicit
annulus-to-physical-radius scale identity. This proves a generic primitive
copy-family implication, not that every actual stage satisfies one uniform
parameter tuple.

The full support-hole transfer is **not yet proved**. The source extension
does not yet prove the common-hole implication through the full
`ActualCandidateAssembly`/`GermCandidateAssembly` cutoff series on a complete
spacetime tube, including valid-band/domain coverage and the direct curl field.
The exact numeric value of `leftRadius` and `patch.a` is also non-effective.
Therefore keep the published packet exponent withdrawn until that aggregate
implication and the tube's domain conditions are formalized and checked.

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

### Follow-up source map: common-support assembly theorem

A closer pass through the updated source found a stronger assembly interface
than the previous paragraph suggested. `PhysicalStageSupport.actual_patch_support`
gives a shared outer-radius constant for every stage once the native-radius
bounds and common-band inequalities are supplied. More generally,
`candidate_support_inputs` transfers this to the literal initial field, every
potential stage, every `rawSeries` direct stage, and the pressure stages through
explicit `EqOn` representation hypotheses. Its output is precisely
`SublevelShrinkingSupport`, which is an **outer** support bound: nonzero values
must have transverse radius at most `C*sqrt(physicalQ)`. It does not prove an
inner support hole. The inner-hole route instead uses separate annulus lower
bounds for each primitive family.

The selected assembly already exposes many of the required representation facts:
`ActualCandidateAssembly.initialPotential_support`,
`positivePotential_support`, and `directStages_support` give generic outer
support statements; `potentialStages_zero/succ` and `directStages_eq` identify
the actual stage sequences; `positivePotential_on_chart` and
`direct_on_chart` relate them to physical chart pieces; and
`ActualCandidateAssembly.witness` consumes the stage support and endpoint data
for its final cutoff schedule. These are strong structural ingredients, and
make a blanket claim that “the support hole is not transferred through any
stages” inaccurate.

The remaining theorem is narrower: transfer the shared positive **inner**
coefficient through the actual representations, selected cutoff sums, spatial
curl and final localization. The classical chart geometry for a whole
`c*sqrt(1-t)` cusp tube is derived in
[`support-hole-tube-geometry.md`](support-hole-tube-geometry.md), conditional on
that coefficient. Its exponent and derivative identities have a symbolic
check, but the tube argument is not yet formalized in Lean and no end-to-end
source theorem states that the final assembled velocity equals its base on
that tube. Accordingly, the packet exponent remains conditional until the
selected-series transfer and final-field equality are checked.

### Follow-up: stage-uniform inner support coefficient

A closer read of the pinned `ActualCandidateAssembly` and support files
establishes a common coefficient for the primitive corrections; the older
claim that this coefficient still had to be extracted stage by stage was too
broad:

- The initialized copy potential has the exact exterior identity
  `InitialPhysicalData.potential_zero_exterior`. Its physical-copy annulus
  gives the lower transverse-radius coefficient
  `leftRadius/(4*sqrt(2))` relative to `sqrt(physicalQ)`.
- At every positive stage `j`, the particular potential is built from the
  same `ActualPrimary.nominal` annulus (`particular_zero_germs`), and the signed
  potential is zero off that same `ActualPolarCoverage.active` annulus
  (`signed_zero_germs`). The former is derived for the actual representative
  by `ActualCurrentWaveSupport.current_field_active_germs`.
- The temporal/rank mean stream families use the fixed initialization patch;
  `ActualMeanStageData.innerRadius` is `(patch.a/4)*sqrt(physicalQ)` and
  `coefficient_vanishes` proves the coefficient is zero below it. The actual
  stream/direct stage constructors expose the corresponding fields.

Thus a common geometric hole coefficient for these primitives is

    c0 = min(leftRadius/(4*sqrt(2)), patch.a/4) > 0.

This is a source-derived positive existential constant, not a numerical value.
Each selected stage's correction terms have zero germs whenever the physical
transverse radius lies strictly below `c0*sqrt(physicalQ)`. The source also
proves component decompositions such as `positivePotential_curl`; the remaining
work is to package the per-stage zero germs uniformly on the tube, pass them
through the selected infinite cutoff sums (including derivatives of the
potential sum), and verify the direct-field, periodic spatial and time
localization transfers. This corrects the previous blanket wording about
missing selected-uniform constants, but does not yet prove an assembled-field
tube or restore the conditional packet exponent.

Pinned source locations: [`InitialPhysicalData.lean`
(`potential_support`, `potential_zero_exterior`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/InitialPhysicalData.lean),
[`ActualCandidateAssembly.lean`
(`particular_zero_germs`, `signed_zero_germs`, `positivePotential_curl`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualCandidateAssembly.lean),
[`ActualCurrentWaveSupport.lean`
(`current_field_active_germs`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualCurrentWaveSupport.lean),
and [`ActualMeanStageData.lean`
(`innerRadius`, `coefficient_vanishes`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualMeanStageData.lean).

No numerical packet or material interpretation follows from these structural
lemmas alone.
