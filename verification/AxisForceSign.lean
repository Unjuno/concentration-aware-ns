import NavierStokes.NaturalAxisData
import NavierStokes.NaturalProfile

/- This lemma checks only the sign of the derived scalar coefficient.
   It does not identify that coefficient with a velocity-field derivative. -/
namespace ConcentrationAware
open NavierStokes

 theorem axial_force_ratio_negative
    {h j eta : ℝ} {P : ℝ → ℝ}
    (small : NaturalAxisData.SmallParameters h j)
    (root_interval : eta ∈ Set.Ioo (-j / 4) (-j / 5))
    (root_eq : NaturalAxisData.H h j eta = 0)
    (pressure : P eta ≤ -1) (pressure_deriv : deriv P eta ≤ 0)
    {nu L A U d : ℝ}
    (hnu : 0 < nu) (hL : 0 < L) (hA : 0 < A)
    (hU : 0 < U) (hd : 0 < d) :
    -nu * NaturalAxisData.Z h j P eta / (L * A * U * d) < 0 := by
  have hz := NaturalAxisData.Z_at_root_lower small root_interval root_eq pressure pressure_deriv
  have hzpos : 0 < NaturalAxisData.Z h j P eta := by
    linarith [small.j_pos]
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_neg_of_pos (neg_neg_of_pos hnu) hzpos
  · positivity

theorem actual_axis_force_ratio_negative
    {h j eta nu : ℝ} {P : ℝ → ℝ}
    (small : NaturalAxisData.SmallParameters h j)
    (interval : eta ∈ Set.Ioo (-j / 4) (-j / 5))
    (root : NaturalAxisData.H h j eta = 0)
    (pressure : NaturalAxisData.PressureData P) (hnu : 0 < nu) :
    -nu * NaturalAxisData.Z h j P eta /
      (NaturalAxisData.L h eta * NaturalAxisData.A h *
       NaturalAxisData.U j eta * NaturalAxisData.d eta) < 0 := by
  have hen : eta < 0 := by linarith [interval.2, small.j_pos]
  have helo : -1 < eta := by linarith [interval.1, small.j_le]
  have heI : eta ∈ Set.Icc (-1 : ℝ) 1 := ⟨helo.le, by linarith⟩
  have hesq : eta ^ 2 < 1 := by nlinarith
  have hd : 0 < NaturalAxisData.d eta := by unfold NaturalAxisData.d; linarith
  have hA : 0 < NaturalAxisData.A h := by unfold NaturalAxisData.A; linarith [small.h_pos]
  have hD : 0 < NaturalAxisData.D h := by unfold NaturalAxisData.D; linarith [small.h_le]
  have hprod : h * eta ^ 2 ≤ h := by nlinarith [mul_nonneg small.h_pos.le (sub_nonneg.mpr hesq.le)]
  have hL : 0 < NaturalAxisData.L h eta := by unfold NaturalAxisData.L; nlinarith [small.h_le]
  have hU : 0 < NaturalAxisData.U j eta := by
    have hneg : NaturalAxisData.D h * eta < 0 := mul_neg_of_pos_of_neg hD hen
    unfold NaturalAxisData.H at root
    nlinarith
  exact axial_force_ratio_negative small interval root (pressure.negative eta heI)
    (pressure.deriv_nonpos heI hen) hnu hL hA hU hd

theorem exists_negative_axis_force_ratio
    {h j nu : ℝ} {P : ℝ → ℝ}
    (small : NaturalAxisData.SmallParameters h j)
    (pressure : NaturalAxisData.PressureData P) (hnu : 0 < nu) :
    ∃ eta : ℝ, eta ∈ Set.Ioo (-j / 4) (-j / 5) ∧
      NaturalAxisData.H h j eta = 0 ∧
      -nu * NaturalAxisData.Z h j P eta /
        (NaturalAxisData.L h eta * NaturalAxisData.A h *
         NaturalAxisData.U j eta * NaturalAxisData.d eta) < 0 := by
  obtain ⟨eta, hi, hr, _⟩ := NaturalAxisData.exists_root_with_positive_Z small pressure
  exact ⟨eta, hi, hr, actual_axis_force_ratio_negative small hi hr pressure hnu⟩

theorem natural_axis_radial_identity
    {h j scale eta : ℝ} {P amp : ℝ → ℝ}
    {f u v pr : ℝ × ℝ → ℝ}
    (solution : NaturalProfile.IsNaturalSolution h j scale P amp f u v pr)
    (point : (0, eta) ∈ NaturalProfile.domain scale)
    (uval : u (0, eta) = NaturalAxisData.U j eta)
    (pval : pr (0, eta) = P eta)
    (uderiv : NaturalAxisBridge.partialEta u (0, eta) = 4)
    (pderiv : NaturalAxisBridge.partialEta pr (0, eta) = deriv P eta) :
    2 * NaturalAxisData.L h eta * NaturalAxisBridge.partialY u (0, eta) =
      -NaturalAxisData.Z h j P eta := by
  have eqn := solution.axial_equation (0, eta) point
  simp only [NaturalAxisBridge.radialDifferential, NaturalProfile.transportH,
    Nat.cast_one, zero_mul, mul_zero, one_mul, zero_add, sub_zero, uval, pval,
    uderiv, pderiv] at eqn
  rw [eqn]
  unfold NaturalAxisData.Z NaturalAxisData.H
  ring

#print axioms natural_axis_radial_identity
#print axioms actual_axis_force_ratio_negative
#print axioms exists_negative_axis_force_ratio
end ConcentrationAware
