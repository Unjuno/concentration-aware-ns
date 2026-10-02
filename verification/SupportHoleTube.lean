import NavierStokes.SimilarityCoordinates
import NavierStokes.PhysicalWaveSum

/-!
This file checks the scalar envelope used in the support-hole tube estimate.
It does not assert that the selected OpenAI witness has already been
transferred through its complete stage assembly.
-/

namespace ConcentrationAware

noncomputable def supportHoleScale (a K : ℝ) : ℝ :=
  max 2 ((2 * K ^ 2) ^ ((1 - a)⁻¹))

/-- A sublinear power inequality has an explicit global upper envelope. -/
theorem scalar_sublinear_envelope {a K s : ℝ}
    (ha1 : a < 1) (hs : 0 < s)
    (hineq : s ≤ 1 + K ^ 2 * s ^ a) :
    s ≤ supportHoleScale a K := by
  by_cases hsmall : s < 2
  · exact hsmall.le.trans (le_max_left _ _)
  · have hs2 : 2 ≤ s := le_of_not_gt hsmall
    have hpow : 0 < s ^ a := Real.rpow_pos_of_pos hs _
    have hhalf : s / 2 ≤ K ^ 2 * s ^ a := by nlinarith
    have hratio : s / (s ^ a) ≤ 2 * K ^ 2 := by
      rw [div_le_iff₀ hpow]
      nlinarith
    have hdiv : s / (s ^ a) = s ^ (1 - a) := by
      calc
        s / (s ^ a) = s ^ (1 : ℝ) / (s ^ a) := by rw [Real.rpow_one]
        _ = s ^ (1 - a) := by rw [Real.rpow_sub hs]
    have hsub : s ^ (1 - a) ≤ 2 * K ^ 2 := by rw [← hdiv]; exact hratio
    have hexp : 0 < (1 - a)⁻¹ := inv_pos.mpr (sub_pos.mpr ha1)
    have hmono := Real.rpow_le_rpow (Real.rpow_nonneg hs.le _) hsub hexp.le
    have hleft : (s ^ (1 - a)) ^ ((1 - a)⁻¹) = s := by
      rw [← Real.rpow_mul hs.le]
      have he : (1 - a) * (1 - a)⁻¹ = 1 := by
        exact mul_inv_cancel₀ (ne_of_gt (sub_pos.mpr ha1))
      rw [he, Real.rpow_one]
    have hlarge : s ≤ (2 * K ^ 2) ^ ((1 - a)⁻¹) := by
      rw [← hleft]
      exact hmono
    exact hlarge.trans (le_max_right _ _)

/-- The similarity-coordinate identity turns a scaled axial bound into a
linear-in-time upper bound for the positive similarity coordinate. -/
theorem similarity_coordinate_upper_of_scaled_axial
    {a K τ z q : ℝ} (ha1 : a < 1)
    (hτ : 0 < τ) (hq : 0 < q)
    (hz : z ^ 2 ≤ K ^ 2 * τ ^ (1 - a))
    (he : NavierStokes.SimilarityCoordinates.forwardScalar a z q = τ) :
    q ≤ supportHoleScale a K * τ := by
  have hsum : q = τ + z ^ 2 * q ^ a := by
    dsimp [NavierStokes.SimilarityCoordinates.forwardScalar] at he
    linarith
  let s : ℝ := q / τ
  have hs : 0 < s := div_pos hq hτ
  have hqs : q = s * τ := by
    dsimp [s]
    field_simp
  have hcoef : z ^ 2 * τ ^ (a - 1) ≤ K ^ 2 := by
    calc
      z ^ 2 * τ ^ (a - 1) ≤ (K ^ 2 * τ ^ (1 - a)) * τ ^ (a - 1) :=
        mul_le_mul_of_nonneg_right hz (Real.rpow_nonneg hτ.le _)
      _ = K ^ 2 := by
        rw [mul_assoc, ← Real.rpow_add hτ]
        have hexp : (1 - a) + (a - 1) = 0 := by ring
        rw [hexp, Real.rpow_zero]
        ring
  have hqpow : q ^ a = s ^ a * τ ^ a := by
    rw [hqs, Real.mul_rpow hs.le hτ.le]
  have hqdiv : q / τ = 1 + z ^ 2 * (q ^ a / τ) := by
    calc
      q / τ = (τ + z ^ 2 * q ^ a) / τ := congrArg (fun x : ℝ => x / τ) hsum
      _ = 1 + z ^ 2 * (q ^ a / τ) := by field_simp
  have hqpowdiv : q ^ a / τ = s ^ a * τ ^ (a - 1) := by
    rw [hqpow, Real.rpow_sub hτ, Real.rpow_one]
    ring
  have hseq : s = 1 + (z ^ 2 * τ ^ (a - 1)) * s ^ a := by
    calc
      s = q / τ := rfl
      _ = 1 + z ^ 2 * (q ^ a / τ) := hqdiv
      _ = 1 + z ^ 2 * (s ^ a * τ ^ (a - 1)) := by rw [hqpowdiv]
      _ = 1 + (z ^ 2 * τ ^ (a - 1)) * s ^ a := by ring
  have hineq : s ≤ 1 + K ^ 2 * s ^ a := by
    calc
      s = 1 + (z ^ 2 * τ ^ (a - 1)) * s ^ a := hseq
      _ ≤ 1 + K ^ 2 * s ^ a := by
        have hspow : 0 ≤ s ^ a := Real.rpow_nonneg hs.le _
        nlinarith [hcoef]
  have henvelope := scalar_sublinear_envelope ha1 hs hineq
  dsimp [s] at henvelope
  exact (div_le_iff₀ hτ).mp henvelope

/-- For `0<tau<=1`, the half-power tube width is no larger than the
similarity axial scale exponent. -/
theorem sqrt_tau_le_sublinear_power {a τ : ℝ}
    (ha0 : 0 < a) (hτ : 0 < τ) (hτ1 : τ ≤ 1) :
    Real.sqrt τ ≤ τ ^ ((1 - a) / 2) := by
  rw [Real.sqrt_eq_rpow]
  exact Real.rpow_le_rpow_of_exponent_ge hτ hτ1 (by linarith)

/-- A center-scale bound and a `sqrt(tau)` tube imply the axial hypothesis
needed by `similarity_coordinate_upper_of_scaled_axial`. -/
theorem axial_coordinate_bound_of_tube {a τ z z0 B ρ : ℝ}
    (ha0 : 0 < a) (hτ : 0 < τ) (hτ1 : τ ≤ 1)
    (hρ : 0 ≤ ρ)
    (hcenter : |z0| ≤ B * τ ^ ((1 - a) / 2))
    (htube : |z - z0| ≤ ρ * Real.sqrt τ) :
    |z| ≤ (B + ρ) * τ ^ ((1 - a) / 2) := by
  have hsqrt := sqrt_tau_le_sublinear_power ha0 hτ hτ1
  calc
    |z| = |(z - z0) + z0| := by congr 1; ring
    _ ≤ |z - z0| + |z0| := abs_add_le _ _
    _ ≤ ρ * Real.sqrt τ + B * τ ^ ((1 - a) / 2) := add_le_add htube hcenter
    _ ≤ ρ * τ ^ ((1 - a) / 2) + B * τ ^ ((1 - a) / 2) := by
      gcongr
    _ = (B + ρ) * τ ^ ((1 - a) / 2) := by ring

/-- The source's scalar similarity equation transfers an axial tube bound
into the explicit upper envelope for `q`. -/
theorem similarity_coordinate_upper_of_tube
    {a K τ z q : ℝ} (ha1 : a < 1)
    (hK : 0 < K) (hτ : 0 < τ) (hq : 0 < q)
    (hz : |z| ≤ K * τ ^ ((1 - a) / 2))
    (he : NavierStokes.SimilarityCoordinates.forwardScalar a z q = τ) :
    q ≤ supportHoleScale a K * τ := by
  have hpow := Real.rpow_nonneg hτ.le ((1 - a) / 2)
  have hsq := (sq_le_sq₀ (abs_nonneg z) (mul_nonneg hK.le hpow)).mpr hz
  have hz2 : z ^ 2 ≤ K ^ 2 * τ ^ (1 - a) := by
    calc
      z ^ 2 = |z| ^ 2 := (sq_abs z).symm
      _ ≤ (K * τ ^ ((1 - a) / 2)) ^ 2 := hsq
      _ = K ^ 2 * τ ^ (1 - a) := by
        rw [mul_pow, ← Real.rpow_mul_natCast hτ.le]
        congr 1
        ring
  exact similarity_coordinate_upper_of_scaled_axial ha1 hτ hq hz2 he

/-- The pinned `physicalQ` is exactly the positive root of the source's
similarity scalar equation at each preterminal spacetime point. -/
theorem physicalQ_forwardScalar {h : ℝ} {w : NavierStokes.ProblemStatement.SpaceTime}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hw : w.1 < 1) :
    NavierStokes.SimilarityCoordinates.forwardScalar (2 * h) (w.2 2)
      (NavierStokes.PhysicalWaveSum.physicalQ h w) = 1 - w.1 := by
  change NavierStokes.SimilarityCoordinates.forwardScalar (2 * h) (w.2 2)
    (NavierStokes.SimilarityCoordinates.coordinateQ (2 * h) (1 - w.1, w.2 2)) = 1 - w.1
  exact (NavierStokes.SimilarityCoordinates.coordinateQ_spec
    (by linarith) (by linarith) (sub_pos.mpr hw)).2

/-- The actual physical similarity coordinate is bounded below by elapsed
time, independently of the axial position. -/
theorem physicalQ_ge_elapsed {h : ℝ} {w : NavierStokes.ProblemStatement.SpaceTime}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hw : w.1 < 1) :
    1 - w.1 ≤ NavierStokes.PhysicalWaveSum.physicalQ h w := by
  have he := physicalQ_forwardScalar hh hh1 hw
  have hq := NavierStokes.PhysicalWaveSum.physicalQ_pos hh hh1 hw
  have hterm : 0 ≤ (w.2 2) ^ 2 *
      (NavierStokes.PhysicalWaveSum.physicalQ h w) ^ (2 * h) :=
    mul_nonneg (sq_nonneg _) (Real.rpow_nonneg hq.le _)
  dsimp [NavierStokes.SimilarityCoordinates.forwardScalar] at he
  linarith

/-- The analytic tube estimate specialized to the actual source chart. -/
theorem physicalQ_le_supportHoleScale {h K : ℝ} {w : NavierStokes.ProblemStatement.SpaceTime}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hK : 0 < K)
    (ht : 0 ≤ w.1) (hw : w.1 < 1)
    (hz : |w.2 2| ≤ K * (1 - w.1) ^ ((1 - 2 * h) / 2)) :
    NavierStokes.PhysicalWaveSum.physicalQ h w ≤
      supportHoleScale (2 * h) K * (1 - w.1) := by
  have hτ : 0 < 1 - w.1 := sub_pos.mpr hw
  have hτ1 : 1 - w.1 ≤ 1 := by linarith
  have hq := NavierStokes.PhysicalWaveSum.physicalQ_pos hh hh1 hw
  exact similarity_coordinate_upper_of_tube (by linarith) hK hτ hq hz
    (physicalQ_forwardScalar hh hh1 hw)

end ConcentrationAware

#print axioms ConcentrationAware.scalar_sublinear_envelope
#print axioms ConcentrationAware.similarity_coordinate_upper_of_scaled_axial
#print axioms ConcentrationAware.sqrt_tau_le_sublinear_power
#print axioms ConcentrationAware.axial_coordinate_bound_of_tube
#print axioms ConcentrationAware.similarity_coordinate_upper_of_tube
#print axioms ConcentrationAware.physicalQ_forwardScalar
#print axioms ConcentrationAware.physicalQ_ge_elapsed
#print axioms ConcentrationAware.physicalQ_le_supportHoleScale
