/-!
# A pressure-qualified selection of complete profile data

This constructs a new noncomputable selection from the prepared outgoing
witness through nominal-cone and modulation assembly. It is deliberately not
identified with `FinalSlowBase.actualProfile`, whose fixed choice is defined
from `profileData_nonempty`.
-/

namespace ConcentrationAwareQualifiedProfile

open NavierStokes

noncomputable def prepared : PreparedOutgoing.PreparedProfile :=
  Classical.choice PreparedOutgoing.exists_prepared

noncomputable def profileData : FinalSlowBase.ProfileData := by
  classical
  let d : PreparedOutgoing.PreparedProfile := prepared
  let w : NominalProfile.Witness d.profile := Classical.choose (NominalConeAssembly.exists_certificate d)
  let hw : NominalConeAssembly.Certificate w := Classical.choose_spec (NominalConeAssembly.exists_certificate d)
  let hmod := ModulatedProfileAssembly.exists_of_certificate w hw
  let ld : ModulatedProfileAssembly.LoopData w := Classical.choose hmod
  let hv := Classical.choose_spec hmod
  let v : ModulatedProfileAssembly.Witness ld := Classical.choose hv
  let hc := Classical.choose_spec hv
  exact ⟨d.profile, w, hw, ld, v, hc⟩

theorem amplitude_lower : 2 ≤ profileData.outgoing.data.core.P := by
  classical
  simpa [profileData, prepared] using prepared.amplitude_lower

theorem exists_root_with_positive_pressure_sign :
    ∃ eta : ℝ,
      eta ∈ Set.Ioo (-profileData.nominal.axis.j/4) (-profileData.nominal.axis.j/5) ∧
      NaturalAxisData.H profileData.outgoing.data.h profileData.nominal.axis.j eta = 0 ∧
      0 < NaturalAxisData.Z profileData.outgoing.data.h profileData.nominal.axis.j
        profileData.outgoing.axisDatum eta := by
  obtain ⟨eta, hinterval, hroot, _⟩ :=
    NaturalAxisData.exists_unique_root profileData.nominal.axis.small
  have hamplitude : (9:ℝ)/40 ≤ profileData.outgoing.data.core.P :=
    le_trans (by norm_num : (9:ℝ)/40 ≤ 2) amplitude_lower
  have hz := ConcentrationAware.outgoing_root_Z_positive_of_uniform_amplitude profileData.outgoing
    profileData.nominal.axis.j eta profileData.nominal.axis.small hinterval hroot hamplitude
  exact ⟨eta, hinterval, hroot, hz⟩

#print axioms amplitude_lower
#print axioms exists_root_with_positive_pressure_sign

end ConcentrationAwareQualifiedProfile
