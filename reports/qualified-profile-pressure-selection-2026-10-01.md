# Pressure-qualified profile re-selection

Date: 2026-10-01
Upstream source pin: `openai/NavierStokesAndEuler@f9e8bc5b38b6e212696e8a30e3e91517af887bbd`

## Result

`verification/QualifiedProfilePressure.lean` defines a new noncomputable `ProfileData` selection by choosing a `PreparedOutgoing.PreparedProfile`, then a nominal cone certificate and its complete modulation witness. The prepared record retains `2 <= core.P`; this bound now survives in the new selected record. Applying the previously checked uniform-amplitude theorem proves that this selected record has a natural-axis root where `Z > 0`.

The replay command is `runtime/lean-verification/check_qualified_profile_pressure.sh`. It concatenates `AxisForceSign.lean` with the new extension and checks the combined file in the isolated pinned-source Lean environment; the latest run exits 0. Both new theorem reports contain only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. The current source hashes and full axiom output are recorded in `evidence/lean-verification/qualified-profile-pressure-2026-10-01.log`.

## Interpretation and limits

This does not prove the pressure sign for OpenAI's existing `FinalSlowBase.actualProfile`, which is defined by a different `Classical.choice profileData_nonempty`. It supplies an alternative, pressure-qualified choice that could be used if the upstream construction intended the final selection to retain its prepared witness. Changing that choice would change the identified object, so no theorem about the original fixed profile may be inferred from this extension.

The result remains inside the formal profile construction. It does not imply molecular alignment, particle-position certainty, phase transition, a constitutive viscosity change, a CFD defect, or blow-up. No upstream report is warranted: we found a useful alternate witness selection, not an upstream false theorem or code defect.
