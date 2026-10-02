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

/-- The analytic amplitude has no positive lower bound uniform over all
normalizations above a finite threshold. This records exactly what the
entrance-existence quantifier does not provide; it says nothing about the
one finite normalization stored by a selected `AxisStage`. -/
theorem no_uniform_lower_bound_over_normalizations
    (h j σ Λ η threshold : ℝ) :
    ¬ ∃ m : ℝ, 0 < m ∧ ∀ C : ℝ, threshold ≤ C →
      m ≤ NaturalAxisCoefficients.realAmplitude h j σ Λ C η := by
  intro hex
  obtain ⟨m, hm, hbound⟩ := hex
  let e := Real.exp (Λ * NaturalAxisCoefficients.realPhase h j σ η)
  let C := max (threshold + 1) (2 * e / m + 1)
  have he : 0 < e := Real.exp_pos _
  have hCthreshold : threshold ≤ C := by
    change threshold ≤ max (threshold + 1) (2 * e / m + 1)
    exact (by linarith : threshold ≤ threshold + 1).trans (le_max_left _ _)
  have hCpos : 0 < C := by
    have hsecond : 0 < 2 * e / m + 1 := by positivity
    change 0 < max (threshold + 1) (2 * e / m + 1)
    exact hsecond.trans_le (le_max_right _ _)
  have hlarge : 2 * e / m < C := by
    change 2 * e / m < max (threshold + 1) (2 * e / m + 1)
    exact (by linarith : 2 * e / m < 2 * e / m + 1).trans_le (le_max_right _ _)
  have hproduct : 2 * e < m * C := by
    have h := (div_lt_iff₀ hm).mp hlarge
    nlinarith
  have hsmall : NaturalAxisCoefficients.realAmplitude h j σ Λ C η < m := by
    unfold NaturalAxisCoefficients.realAmplitude
    change e / C < m
    exact (div_lt_iff₀ hCpos).2 (by nlinarith)
  exact (not_lt_of_ge (hbound C hCthreshold)) hsmall

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
#print axioms no_uniform_lower_bound_over_normalizations

end ConcentrationAwarePressureProvenance
