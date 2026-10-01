# Pressure-qualified profile re-selection

Date: 2026-10-01
Upstream source pin: `openai/NavierStokesAndEuler@f9e8bc5b38b6e212696e8a30e3e91517af887bbd`

## Result

`verification/QualifiedProfilePressure.lean` defines a new noncomputable `ProfileData` selection by choosing a `PreparedOutgoing.PreparedProfile`, then a nominal cone certificate and its complete modulation witness. The prepared record retains `2 <= core.P`; this bound now survives in the new selected record. Applying the previously checked uniform-amplitude theorem proves that this selected record has a natural-axis root where `Z > 0`.

The replay command is `runtime/lean-verification/check_qualified_profile_pressure.sh`. It concatenates `AxisForceSign.lean` with the new extension and checks the combined file in the isolated pinned-source Lean environment; the latest run exits 0. All five extension declarations report only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. `slow_base_viscous_acceleration_ratio_limit` proves that, along the selected material curve, the ratio of viscosity times spatial Laplacian to material acceleration has a finite limit. `exists_qualified_slow_base_negative_ratio` combines it with the pressure-qualified root and proves that this limit is strictly negative for positive viscosity. `exists_qualified_slow_base_ratio_magnitude_limit` further proves that the absolute value of the ratio tends to a strictly positive constant, so the ratio does not vanish. The source hashes and axiom output are recorded in `evidence/lean-verification/qualified-profile-pressure-2026-10-01.log`.

The ratio is for the selected `FinalSlowBase.velocity` base field and its natural material trajectory. It has not been transferred through the periodic/correction assembly to an actual periodic field.

## Interpretation and limits

This does not prove the pressure sign for OpenAI's existing `FinalSlowBase.actualProfile`, which is defined by a different `Classical.choice profileData_nonempty`. It supplies an alternative, pressure-qualified choice that could be used if the upstream construction intended the final selection to retain its prepared witness. Changing that choice would change the identified object, so no theorem about the original fixed profile may be inferred from this extension. The negative sign is for the signed ratio `nu * Δu / (∂t u + u·∇u)`; it is not a viscosity law, a claim that viscous effectiveness collapses, or an instability result.

The result remains inside the formal profile construction. A nonzero limiting magnitude for this ratio is not itself a theorem about constitutive viscosity or all possible meanings of “viscous effectiveness”; it only rules out interpreting this particular ratio as tending to zero. It does not imply molecular alignment, particle-position certainty, phase transition, a constitutive viscosity change, a CFD defect, or blow-up. No upstream report is warranted: we found a useful alternate witness selection, not an upstream false theorem or code defect.
