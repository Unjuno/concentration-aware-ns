import NavierStokes.NaturalAxisData

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

end ConcentrationAware
