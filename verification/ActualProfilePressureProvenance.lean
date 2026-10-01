import NavierStokes.FinalSlowBase

/-!
# Pressure-amplitude provenance at the final profile selection

The construction path contains an outgoing profile with the strong bound
`core.P >= 2`.  This theorem deliberately states the existential result only:
`FinalSlowBase.ProfileData` and its `actualProfile` choice do not currently
carry that bound as a field.
-/

namespace ConcentrationAwarePressureProvenance

open NavierStokes

theorem exists_final_profile_data_with_pressure_amplitude :
    ∃ D : FinalSlowBase.ProfileData, 2 ≤ D.outgoing.data.core.P := by
  obtain ⟨d⟩ := PreparedOutgoing.exists_prepared
  obtain ⟨W, hW⟩ := NominalConeAssembly.exists_certificate d
  obtain ⟨ld, v, hv⟩ := ModulatedProfileAssembly.exists_of_certificate W hW
  exact ⟨⟨d.profile, W, hW, ld, v, hv⟩, d.amplitude_lower⟩

theorem actual_profile_is_a_profile_data :
    FinalSlowBase.actualProfile.outgoing.data.core.P > 0 := by
  exact FinalSlowBase.actualProfile.outgoing.data.core.P_pos

#print axioms exists_final_profile_data_with_pressure_amplitude
#print axioms actual_profile_is_a_profile_data

end ConcentrationAwarePressureProvenance
