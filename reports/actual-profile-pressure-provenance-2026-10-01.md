# Actual-profile pressure-threshold provenance audit

Date: 2026-10-01  
Upstream source: `openai/NavierStokesAndEuler` at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`  
Benchmark status: analytic extension audit; no CFD run or physical interpretation.

## Question

The pressure-moment derivation gives a sufficient local sign condition when the selected outgoing amplitude satisfies `b >= 9/40`. Does the pinned construction prove this for `FinalSlowBase.actualProfile`?

## Lean result

`verification/ActualProfilePressureProvenance.lean` was compiled in the isolated checker using the pinned source volume. It establishes:

1. There exists a `FinalSlowBase.ProfileData` assembled from `PreparedOutgoing.exists_prepared`, `NominalConeAssembly.exists_certificate`, and `ModulatedProfileAssembly.exists_of_certificate` whose outgoing core amplitude is at least 2.
2. For `FinalSlowBase.actualProfile`, the currently available conclusion is `core.P > 0`, obtained from `actualProfile.outgoing.data.core.P_pos`.

Both declarations report only `propext`, `Classical.choice`, and `Quot.sound`. The exact checker output is in `evidence/lean-verification/actual-profile-pressure-provenance-2026-10-01.log`; the replay command is `runtime/lean-verification/check_actual_profile_pressure_provenance.sh`.

## Interpretation and limits

The first existential result does not transfer its amplitude inequality to the separate `Classical.choice` used for `actualProfile`. This is a witness-provenance gap in the extension. It is not evidence that `actualProfile` violates `b >= 2` or `b >= 9/40`; no counterexample or impossibility theorem was constructed. The threshold condition remains unproved for the selected profile. A possible proof route is to retain `PreparedProfile.amplitude_lower` through the certificate/profile records and define the final selection from the enriched record, or derive the weaker moment bound from the conditions already retained.

This result concerns a proof obligation in the benchmark's analysis extension. It is not an OpenAI repository defect, an upstream theorem refutation, a CFD failure, or evidence for molecular alignment or a viscosity transition. The pinned source-dataflow record is `evidence/upstream-refresh/pressure-witness-dataflow-2026-09-28.json`; the exact pressure threshold and earlier limitations are in `docs/pressure-moment-threshold.md`.

## Upstream disposition

The OpenAI repository has Issues and Discussions disabled in the October 1 inventory. No upstream report was submitted. Even if a channel existed, the current result concerns how our extension carries a witness, not a demonstrated error in upstream source or theorem.

## Live source and retained-field recheck

A fresh GitHub API read at 2026-10-01 08:08 UTC confirmed that `main` is still
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, matching the source used by the
isolated Lean checker. The repository still declares Apache-2.0 and has both
Issues and Discussions disabled. The response fields and time are archived in
`evidence/upstream-refresh/openai-live-recheck-2026-10-01T0808Z.json`.

The source dataflow remains: `PreparedProfile` stores `amplitude_lower`, while
`FinalSlowBase.ProfileData` stores the outgoing, nominal, certificate, loop,
modulation and full-cone fields but no amplitude proof. Its `actualProfile` is
chosen from `Nonempty ProfileData`. The nominal witness also retains its
construction fields, so absence of a dedicated amplitude field is not a proof
that no downstream implication exists. It does mean the prepared witness's
bound cannot simply be projected from the selected record; a theorem deriving
the required local moment/amplitude threshold from retained properties is still
needed. This distinction does not show that the chosen amplitude is small.

## Related run-state correction

The current OpenFOAM six-case matrix remains complete according to `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`. The historic n64, `dt=0.0005` partial attempt is superseded by its archived 100/100-step completed rerun. No matrix verdict changes.

## 2026-10-02 pinned-field audit

The three upstream files used to trace the selection were re-hashed in the
isolated checker source. Their SHA-256 values exactly match the archived
2026-09-28 source inventory:

| Source | SHA-256 |
|---|---|
| `PreparedOutgoing.lean` | `b17ae08fd3e31ae75821d47fe801901a226d7ebe8f2fff8f442fc8751ad1a069` |
| `NominalConeAssembly.lean` | `ad0f8947723416c950c1e3cbb82bac8c83b03ef25fa5aba495a3e29508b14cb5` |
| `FinalSlowBase.lean` | `d46846fea27ac623967e008301789edc4c52f915e63e2ba1f5f8f73df3d95314` |

The schema distinction is concrete. `PreparedOutgoing.PreparedProfile` stores
`amplitude_lower : 2 ≤ profile.data.core.P`. `FinalSlowBase.ProfileData`
instead stores an `OutgoingProfile.Profile`, nominal witness, cone
certificate, modulation loop, modulation witness and full-cone proof. The
nominal witness retains an `AxisStage`, whose preparation includes analytic
coefficient inputs and a large-scale entrance-existence condition, but it does
not retain the prepared-profile object or its amplitude proof. The certificate
is a proposition about cone regions. The current fixed `actualProfile` is
chosen from `Nonempty ProfileData`.

This shows why the existing existential proof cannot simply be projected onto
`actualProfile`; it does not establish that the threshold is mathematically
false or impossible to recover. Two legitimate proof routes remain: derive
`P ≥ 9/40` (or the exact pressure-moment condition) from the retained
`ProfileData` fields, including the all-large-scale entrance property; or
change the local construction path to carry `PreparedProfile` through final
selection and then recheck every theorem depending on that selection. The
already checked alternate `ConcentrationAwareQualifiedProfile.profileData`
only proves the second route for a separate selection and is not evidence
about `FinalSlowBase.actualProfile`. No counterexample, full periodic-flow
pressure conclusion, or molecular/constitutive consequence is established.

## 2026-10-02 retained-preparation route audit

A deeper source pass checked whether the stored nominal axis stage could
recover the lost lower bound. `NominalProfile.Witness.axis` is an
`AxisStage`; its `preparation` stores `AnalyticInputs`, a scale bound, and an
`entrances` field asserting nonempty `NaturalEntrance.EntranceProfile` values
for every sufficiently large normalization and admissible coefficient bound.
Those entrance profiles retain the `source_lower`, `slope_positive`, and
`cone_margin` inequalities. This is substantially more information than the
bare positive-amplitude theorem, so it remains a plausible route to a derived
lower bound.

The type boundary is nevertheless unchanged: `prepare_axis` consumes
`hP : 2 ≤ F.data.core.P` to build the preparation, but `AxisPreparation`,
`AxisStage`, `Witness`, and `FinalSlowBase.ProfileData` do not store that proof
or a `PreparedOutgoing.PreparedProfile`. `AnalyticInputs` stores coefficient
families indexed by the actual pressure function, but has no numeric lower
bound field. `ideal_prefix_entranceProfile` itself is a construction theorem
whose input includes `hB : 2 ≤ B`; it does not establish that an arbitrary
retained entrance record implies the same inequality. I found no named theorem
in the pinned source deriving `2 ≤ core.P` from these retained fields. That
search is not a proof that no derivation exists.

The exact pinned source SHA-256 values rechecked for this path are:

| Source | SHA-256 |
|---|---|
| `NaturalAxisCoefficients.lean` | `cf762100d7de681f34aba5dcfeecac4b81e6b5d2cda8ec781236e4b3fdd3d9fd` |
| `NaturalEntrance.lean` | `05d4871c68cbf59486ba5a34fe42c3c3963218e2ba7be2408363d5f8a8f26af3` |
| `NominalProfile.lean` | `59f2977035db50e680ee38cf4503c47497e50a58a6043d083fdd8755dac06c88` |
| `NominalConeAssembly.lean` | `ad0f8947723416c950c1e3cbb82bac8c83b03ef25fa5aba495a3e29508b14cb5` |
| `FinalSlowBase.lean` | `d46846fea27ac623967e008301789edc4c52f915e63e2ba1f5f8f73df3d95314` |

The actual-profile pressure sign therefore remains conditional. The next
proof attempt should either establish the required moment threshold directly
from the universally retained entrance inequalities, or carry a prepared
profile witness into the final choice. Until one succeeds, do not apply the
separate existential-profile pressure theorem to `actualProfile`.

## Analytic content of the retained entrance margin

The retained `cone_margin` is not itself a scalar amplitude condition. In the
pinned source, `NaturalEntrance.coneSize` is `p1 + p2^2 / p1`; after rewriting
through the regular source-integral stocks, the entrance theorem gives
`9/4 < q + n^2/q`. This constrains derivatives and values of the constructed
profile fields at the entrance section. The fields depend on the pressure
datum through `CoefficientProfile.scaled`, so the condition is not independent
of the pressure construction; however, no direct algebraic step from this
cone inequality to the outgoing core amplitude is currently identified.

Likewise, `NaturalAxisData.PressureData` consists of pressure smoothness,
`P(eta) <= -1`, and the sign condition `0 <= eta * deriv P(eta)`. It has no
amplitude parameter. The ideal-prefix theorem constructs this record from
`B >= 2`, but its stated direction is sufficient construction, not a converse.
This type-level observation alone does not rule out a converse using the
integral representation of the pressure and the retained scaled-solution
identities. The concrete remaining proof bridge is therefore one of:
(1) use those identities to derive a quantitative lower bound on the ideal
prefix mass/core amplitude from the selected entrance fields; or (2) make the
selection retain the prepared amplitude witness and transfer it through the
final profile record. Until that bridge is proved, the pressure sign remains
conditional.

## A countermodel to the pressure-data-only converse

The weaker route through `PressureData` alone can be ruled out. Fix any
`0 < B < 2`, put `g(y) = B^2 exp(y/5)` on `y <= 0`, add a nonnegative tail of
mass `2` on `[1,2]`, and set the exponent to `1` on the prefix and `0` on the
tail (zero elsewhere). This is an admissible nonnegative integrable schedule
with exponents in `[0,1]`. Since `kernel 0 eta = 1` and
`kernel 1 eta = (1+eta^2)^(-2)`, its pressure is exactly

`P(eta) = -1 - (5/2) B^2 (1+eta^2)^(-2)`.

It is smooth, satisfies `P(eta) <= -1`, and
`eta * P'(eta) = 10 B^2 eta^2 (1+eta^2)^(-3) >= 0`, despite `B < 2`.
Thus the three fields of `NaturalAxisData.PressureData`, even combined with
the ideal-prefix identity and generic `PressureDatum.Admissible`, do not imply
the prefix amplitude threshold. This countermodel does **not** satisfy the
full selected `SchedulePressure` / `CoefficientProfile` / `EntranceProfile`
construction and is not a counterexample to `actualProfile`; it rules out
only the pressure-data-only converse. Any remaining derivation must use the
additional schedule-shape, scaled-solution, or entrance-field constraints.
The exact symbolic replay is `tools/check_pressure_data_amplitude_countermodel.py`,
with its SymPy 1.14.0 result in
`evidence/tests/pressure-data-amplitude-countermodel-2026-10-02.json`; the
check is also included in `tools/replay_published_reports.py`.

## Connection to the pinned schedule's zero-exponent tail

The generic countermodel uses a tail term independent of `eta`. The pinned
constructed schedule has the same *form* of contribution after flattening:
`SchedulePressure.shapeExponent_after` gives exponent zero for
`y >= flattenEnd`, and `SchedulePressure.angular_square_factorization`
rewrites the pressure integrand as `clockWeight * kernel(shapeExponent, eta)`.
Since `kernel 0 eta = 1`, the region `Ici flattenEnd` contributes the constant
`-(1/2) * integral clockWeight` independently of `eta`. This makes the
pressure-data-only obstruction directly relevant to the schedule's analytic
structure. It does not show that this contribution is freely adjustable:
`clockWeight` is built from the same `TailData` and outgoing profile. The
remaining analytical target is to bound this tail contribution quantitatively
relative to `core.P^2` under the retained schedule constraints, or otherwise
derive the needed root-pressure inequality without recovering `core.P >= 2`.
The identity is Lean-checked against the pinned sources in
`verification/SelectedScheduleTailPressure.lean`; its replay and axiom audit
are `runtime/lean-verification/check_selected_schedule_tail_pressure.sh` and
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`.

The follow-up replay adds a quantitative one-sided bound using the actual
schedule's uniform future-clock estimate:

`-(5/8) * exp(6/5) * clockWeight(flattenEnd) <= tailPressureContribution <= 0`.

Both endpoints are Lean-checked against the same pinned source. This is a
parameter-uniform envelope in terms of the endpoint clock weight, not yet a
bound relative to `core.P^2`: the normalized estimate still depends on the
selected schedule's pulse amplitude and parameter thresholds. The bound
narrows the next proof obligation but does not establish the actual-profile
root-pressure sign.

The endpoint weight identity now closes one part of that normalization. If
the source's exact wait condition `wait = 60 * log(1/lam)` holds, the pinned
`pulseAmplitude_small` estimate yields the Lean-checked bound

`tailPressureContribution >= -(5/32) * exp(6/5) * (P * exp(exp(m)+12) * lam^30)^2 * exp(-(1+2*lam)*(13/lam + flattenLength))`.

Equivalently, the coefficient multiplying `P^2` is
`(5/32) * lam^60 * exp(2*exp(m) - 4/5 - 13/lam - (1+2*lam)*flattenLength)`.
This is an explicit conditional `P^2`-relative bound, but it is not yet shown
to be uniformly small under the final selected-profile hypotheses: the
`m`- and `lam`-dependent factor remains, and the wait identity is an explicit
hypothesis of this lemma. It therefore does not close the pressure-sign or
actual-profile witness-transfer gap.

## Rate-capped prepared selector follow-up — 2026-10-02

The pinned source's `TailCone.exists_tail_smallness_threshold` constructs an
incoming threshold using
`exp(-(exp(m)+12+3/5))/4`, but the public ordered-profile and prepared-profile
results do not retain that numerical cap. A Lean extension therefore takes
the minimum of the source's valid ordered profile-cone threshold and this
incoming cap, then reruns the existing scheduled-family selection. The
resulting `RateCappedPreparedProfile` retains the same prepared-profile
fields plus proofs of the exact wait identity and lambda cap.

Under that cap, Lean proves the explicit coefficient multiplying `P^2` is
at most `1/100`, and proves existence of a source-derived prepared profile
whose zero-exponent tail contribution is at least `-P^2/100`. The new
declarations use only `[propext, Classical.choice, Quot.sound]` and contain no
`sorryAx`. This establishes an existential capped selection, not a property
of the pinned `FinalSlowBase.actualProfile`: its classical-choice path still
uses the ordinary profile-data record, and the prepared witness, amplitude
lower bound, wait identity, and cap are not transferred into that record.
Accordingly the actual-profile root-pressure premise remains open, as do any
solver-validity or physical/molecular conclusions. The exact replay and
source hashes are in
`evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`.

Pinned-source hashes for the identities used here:

| Source | SHA-256 |
|---|---|
| `SchedulePressure.lean` | `d4146daa477827b6f69c752510699becf1c97973f96e50f8636991958fa1e159` |
| `PressureDatum.lean` | `a1ad3e25e569532b0dc21c71f5f8e0092bb8abd2096f03c3469639d2435a2513` |
| `TailEnergyBounds.lean` | `cc2771933c88bef01f7957b4903e28c84ec8ed588c9ae757c17b519e458abd1d` |
| `OutgoingTail.lean` | `450c6d0cea94de6ebaad98d199bfa5b45b1cbc249decec3fd44b796ddd43eba5` |
| `OutgoingSchedule.lean` | `680379d41f5ecb928f53278860c807e3344e9bcaefbcd6c4bbcc493f812bc552` |
| `FuturePressureBounds.lean` | `e55060a6239e37b56308ab631949c20174d4231c6f209eaa005ce182c32d5c86` |
| `OutgoingPulseBounds.lean` | `c7a25e38f34f1c6d7f3a3f0de830cee9979155956c80896014558b61e27de478` |
