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
