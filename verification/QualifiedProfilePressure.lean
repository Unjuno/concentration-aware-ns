/-!
# A pressure-qualified selection of complete profile data

This constructs a new noncomputable selection from the prepared outgoing
witness through nominal-cone and modulation assembly. It is deliberately not
identified with `FinalSlowBase.actualProfile`, whose fixed choice is defined
from `profileData_nonempty`.
-/

namespace ConcentrationAwareQualifiedProfile

open NavierStokes
open Filter
open scoped Topology

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

/-- The reconstructed slow-base field has a finite axiswise limit for the
viscous Laplacian divided by material acceleration. This is a selected-base
statement, not a claim about the original fixed profile or a full PDE solution. -/
theorem slow_base_viscous_acceleration_ratio_limit
    (upper nu eta : ℝ) (B : ℕ) (hnu : 0 < nu)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1)
    (root : NaturalAxisData.H profileData.outgoing.data.h
      profileData.nominal.axis.j eta = 0)
    (hU : NaturalAxisData.U profileData.nominal.axis.j eta ≠ 0) :
    let u := FinalSlowBase.velocity profileData.certificate profileData.modulation upper B
    let curve := fun t : ℝ => AxisymmetricResidual.pack 0 0
      (eta*((1-t)/(1-eta^2))^(CoordinateAlgebra.D profileData.outgoing.data.h))
    Filter.Tendsto (fun q : ℝ =>
      nu*ProblemStatement.spatialLaplacian u (1-q*(1-eta^2))
        (curve (1-q*(1-eta^2))) 2 /
        ((ProblemStatement.temporalDerivative u (1-q*(1-eta^2))
            (curve (1-q*(1-eta^2))) +
          ProblemStatement.advection u (1-q*(1-eta^2))
            (curve (1-q*(1-eta^2)))) 2))
      (nhdsWithin (0 : ℝ) (Set.Ioi 0))
      (nhds ((nu*(2*deriv (fun X => profileData.nominal.axis.natural.profile.family.U
        (X,eta)) 0) /
        (CoordinateAlgebra.A profileData.outgoing.data.h *
          NaturalAxisData.U profileData.nominal.axis.j eta/(1-eta^2))))) := by
  intro u curve
  let h := profileData.outgoing.data.h
  let j := profileData.nominal.axis.j
  let W := profileData.nominal
  let H := profileData.certificate
  let v := profileData.modulation
  have hd : 0 < 1-eta^2 := by nlinarith [heta.1, heta.2]
  have hA : CoordinateAlgebra.A h ≠ 0 := by
    unfold CoordinateAlgebra.A
    linarith [W.axis.small.h_pos]
  let coefficient := CoordinateAlgebra.A h * NaturalAxisData.U j eta/(1-eta^2)
  have hcoeff : coefficient ≠ 0 := div_ne_zero (mul_ne_zero hA hU) (by linarith)
  have hlap := ConcentrationAware.selected_normalized_axis_laplacian_limit
    H v upper eta B heta
  have hlimit := ((hlap.const_mul nu).div_const coefficient)
  apply hlimit.congr'
  have hacc : ∀ᶠ q : ℝ in nhdsWithin (0 : ℝ) (Set.Ioi 0),
      let t := 1-q*(1-eta^2)
      (ProblemStatement.temporalDerivative u t (curve t) +
        ProblemStatement.advection u t (curve t)) 2 =
        coefficient*q^(-CoordinateAlgebra.A h-1) := by
    filter_upwards [self_mem_nhdsWithin] with q hq
    dsimp only
    let t := 1-q*(1-eta^2)
    have ht : t < 1 := by dsimp [t]; nlinarith [mul_pos hq hd]
    have htrajectory := ConcentrationAware.selected_base_material_trajectory
      H v upper eta t B ht heta root
    have hvelocity := ConcentrationAware.selected_base_axis_velocity_time_derivative
      H v upper eta t B ht heta
    have hopen : IsOpen BaseResidual.past := isOpen_Iio.prod isOpen_univ
    have hpoint : (t, curve t) ∈ BaseResidual.past := ⟨ht, Set.mem_univ _⟩
    have hsmooth := (FinalSlowBase.velocity_smooth H v upper B).contDiffAt
      (hopen.mem_nhds hpoint)
    have hu : DifferentiableAt ℝ u (t, curve t) := by
      exact hsmooth.differentiableAt (by simp)
    have hchain := ConcentrationAware.material_curve_chain_rule u curve t hu htrajectory
    have hden := hvelocity.unique hchain
    have hqt : (1-t)/(1-eta^2) = q := by dsimp [t]; field_simp; ring
    rw [hqt] at hden
    have hden' := congrArg (fun x : ProblemStatement.Space => x 2) hden
    change (AxisymmetricResidual.pack 0 0 _) 2 = _ at hden'
    rw [AxisymmetricResidual.pack_two] at hden'
    change (ProblemStatement.temporalDerivative u t (curve t) +
      ProblemStatement.advection u t (curve t)) 2 = _
    rw [← hden']
  filter_upwards [hacc, self_mem_nhdsWithin] with q hden hq
  have hqt : (1-(1-q*(1-eta^2)))/(1-eta^2) = q := by field_simp; ring
  have hcurve : curve (1-q*(1-eta^2)) =
      AxisymmetricResidual.pack 0 0 (eta*q^(CoordinateAlgebra.D h)) := by
    dsimp [curve]
    rw [hqt]
  rw [hden]
  rw [hcurve]
  have hp : q^(-CoordinateAlgebra.A h-1) =
      (q^(CoordinateAlgebra.A h+1))⁻¹ := by
    rw [show -CoordinateAlgebra.A h-1 = -(CoordinateAlgebra.A h+1) by ring,
      Real.rpow_neg hq.le]
  rw [hp]
  field_simp
  ring

theorem exists_qualified_slow_base_negative_ratio
    (upper nu : ℝ) (B : ℕ) (hnu : 0 < nu) :
    ∃ eta : ℝ,
      eta ∈ Set.Ioo (-profileData.nominal.axis.j/4)
        (-profileData.nominal.axis.j/5) ∧
      NaturalAxisData.H profileData.outgoing.data.h
        profileData.nominal.axis.j eta = 0 ∧
      ∃ ell : ℝ, ell < 0 ∧
        let u := FinalSlowBase.velocity profileData.certificate profileData.modulation upper B
        let curve := fun t : ℝ => AxisymmetricResidual.pack 0 0
          (eta*((1-t)/(1-eta^2))^(CoordinateAlgebra.D profileData.outgoing.data.h))
        Filter.Tendsto (fun q : ℝ =>
          nu*ProblemStatement.spatialLaplacian u (1-q*(1-eta^2))
            (curve (1-q*(1-eta^2))) 2 /
            ((ProblemStatement.temporalDerivative u (1-q*(1-eta^2))
                (curve (1-q*(1-eta^2))) +
              ProblemStatement.advection u (1-q*(1-eta^2))
                (curve (1-q*(1-eta^2)))) 2))
          (nhdsWithin (0 : ℝ) (Set.Ioi 0)) (nhds ell) := by
  obtain ⟨eta, interval, root, hz⟩ := exists_root_with_positive_pressure_sign
  have hnu' : nu > 0 := hnu
  have hen : eta < 0 := by
    have := profileData.nominal.axis.small.j_pos
    linarith [interval.2]
  have helo : -1 < eta := by
    have := profileData.nominal.axis.small.j_le
    linarith [interval.1]
  have heta : eta ∈ Set.Ioo (-1 : ℝ) 1 := ⟨helo, by linarith [hen]⟩
  have hD : 0 < NaturalAxisData.D profileData.outgoing.data.h := by
    unfold NaturalAxisData.D
    linarith [profileData.nominal.axis.small.h_le]
  have hgeom : 0 < 1-eta^2 := by nlinarith [heta.1, heta.2]
  have hU : 0 < NaturalAxisData.U profileData.nominal.axis.j eta := by
    have he := root
    unfold NaturalAxisData.H NaturalAxisData.d at he
    nlinarith [mul_neg_of_pos_of_neg hD hen, hgeom]
  have hA : 0 < CoordinateAlgebra.A profileData.outgoing.data.h := by
    unfold CoordinateAlgebra.A
    linarith [profileData.nominal.axis.small.h_pos]
  have inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left
      NaturalAxisCoefficients.window.right := by
    change -(11:ℝ)/10 < eta ∧ eta < (11:ℝ)/10
    constructor <;> linarith
  have point : (0,eta) ∈ NaturalProfile.domain profileData.nominal.axis.scale := by
    change (profileData.nominal.axis.scale*0,eta) ∈
      Set.Ioo (-20:ℝ) 20 ×ˢ Set.Ioo NaturalAxisCoefficients.window.left
        NaturalAxisCoefficients.window.right
    exact ⟨by norm_num, inside⟩
  have pressure := profileData.outgoing.natural_axis_pressureData amplitude_lower
  have hderiv := ConcentrationAware.selected_natural_derivative_negative
    profileData.nominal eta point inside interval root pressure
  let ell : ℝ := nu*(2*deriv (fun X =>
      profileData.nominal.axis.natural.profile.family.U (X,eta)) 0) /
      (CoordinateAlgebra.A profileData.outgoing.data.h *
        NaturalAxisData.U profileData.nominal.axis.j eta/(1-eta^2))
  have hden : 0 < CoordinateAlgebra.A profileData.outgoing.data.h *
      NaturalAxisData.U profileData.nominal.axis.j eta/(1-eta^2) :=
        div_pos (mul_pos hA hU) hgeom
  have hnum : nu*(2*deriv (fun X =>
      profileData.nominal.axis.natural.profile.family.U (X,eta)) 0) < 0 :=
    mul_neg_of_pos_of_neg hnu (mul_neg_of_pos_of_neg (by norm_num) hderiv)
  have hell : ell < 0 := by
    dsimp [ell]
    exact div_neg_of_neg_of_pos hnum hden
  have hratio := slow_base_viscous_acceleration_ratio_limit upper nu eta B hnu'
    heta root hU.ne'
  exact ⟨eta, interval, root, ell, hell, by simpa [ell] using hratio⟩

/-- At the same qualified root, the magnitude of the viscous/acceleration
ratio tends to a strictly positive constant. Thus its negative sign does not
mean that this ratio vanishes. -/
theorem exists_qualified_slow_base_ratio_magnitude_limit
    (upper nu : ℝ) (B : ℕ) (hnu : 0 < nu) :
    ∃ eta : ℝ,
      eta ∈ Set.Ioo (-profileData.nominal.axis.j/4)
        (-profileData.nominal.axis.j/5) ∧
      NaturalAxisData.H profileData.outgoing.data.h
        profileData.nominal.axis.j eta = 0 ∧
      ∃ magnitudeLimit : ℝ, 0 < magnitudeLimit ∧
        let u := FinalSlowBase.velocity profileData.certificate profileData.modulation upper B
        let curve := fun t : ℝ => AxisymmetricResidual.pack 0 0
          (eta*((1-t)/(1-eta^2))^(CoordinateAlgebra.D profileData.outgoing.data.h))
        Filter.Tendsto (fun q : ℝ => |nu*ProblemStatement.spatialLaplacian u
          (1-q*(1-eta^2)) (curve (1-q*(1-eta^2))) 2 /
          ((ProblemStatement.temporalDerivative u (1-q*(1-eta^2))
              (curve (1-q*(1-eta^2))) +
            ProblemStatement.advection u (1-q*(1-eta^2))
              (curve (1-q*(1-eta^2)))) 2)|)
          (nhdsWithin (0 : ℝ) (Set.Ioi 0)) (nhds magnitudeLimit) := by
  obtain ⟨eta, interval, root, ell, hell, hratio⟩ :=
    exists_qualified_slow_base_negative_ratio upper nu B hnu
  refine ⟨eta, interval, root, -ell, neg_pos.mpr hell, ?_⟩
  simpa [abs_of_neg hell] using hratio.abs

#print axioms amplitude_lower
#print axioms exists_root_with_positive_pressure_sign
#print axioms slow_base_viscous_acceleration_ratio_limit
#print axioms exists_qualified_slow_base_negative_ratio
#print axioms exists_qualified_slow_base_ratio_magnitude_limit

end ConcentrationAwareQualifiedProfile
