import NavierStokes.NaturalAxisData
import NavierStokes.NaturalProfile
import NavierStokes.SlowBorelBase
import NavierStokes.FinalSlowBase

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

open scoped Topology

theorem natural_axis_radial_identity_from_solution
    {h j scale eta : ℝ} {P amp : ℝ → ℝ}
    {f u v pr : ℝ × ℝ → ℝ}
    (solution : NaturalProfile.IsNaturalSolution h j scale P amp f u v pr)
    (point : (0, eta) ∈ NaturalProfile.domain scale)
    (inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left
      NaturalAxisCoefficients.window.right) :
    2 * NaturalAxisData.L h eta * NaturalAxisBridge.partialY u (0, eta) =
      -NaturalAxisData.Z h j P eta := by
  have hu : (fun e => u (0, e)) =ᶠ[𝓝 eta] NaturalAxisData.U j := by
    filter_upwards [IsOpen.mem_nhds isOpen_Ioo inside] with e he
    exact solution.U_axis e he
  have hp : (fun e => pr (0, e)) =ᶠ[𝓝 eta] P := by
    filter_upwards [IsOpen.mem_nhds isOpen_Ioo inside] with e he
    exact solution.pressure_axis e he
  apply natural_axis_radial_identity solution point (solution.U_axis eta inside)
    (solution.pressure_axis eta inside)
  · change deriv (fun e => u (0, e)) eta = 4
    rw [hu.deriv_eq]
    exact (NaturalProfile.uStar_hasDerivAt j eta).deriv
  · exact hp.deriv_eq

theorem natural_radial_derivative_negative_at_root
    {h j scale eta : ℝ} {P amp : ℝ → ℝ}
    {f u v pr : ℝ × ℝ → ℝ}
    (solution : NaturalProfile.IsNaturalSolution h j scale P amp f u v pr)
    (point : (0, eta) ∈ NaturalProfile.domain scale)
    (inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left
      NaturalAxisCoefficients.window.right)
    (small : NaturalAxisData.SmallParameters h j)
    (interval : eta ∈ Set.Ioo (-j / 4) (-j / 5))
    (root : NaturalAxisData.H h j eta = 0)
    (pressure : NaturalAxisData.PressureData P) :
    NaturalAxisBridge.partialY u (0, eta) < 0 := by
  have hen : eta < 0 := by linarith [interval.2, small.j_pos]
  have helo : -1 < eta := by linarith [interval.1, small.j_le]
  have heI : eta ∈ Set.Icc (-1 : ℝ) 1 := ⟨helo.le, by linarith⟩
  have hesq : eta ^ 2 < 1 := by nlinarith
  have hprod : h * eta ^ 2 ≤ h := by
    nlinarith [mul_nonneg small.h_pos.le (sub_nonneg.mpr hesq.le)]
  have hL : 0 < NaturalAxisData.L h eta := by
    unfold NaturalAxisData.L
    nlinarith [small.h_le]
  have hz := NaturalAxisData.Z_at_root_lower small interval root
    (pressure.negative eta heI) (pressure.deriv_nonpos heI hen)
  have eqn := natural_axis_radial_identity_from_solution solution point inside
  have hzpos : 0 < NaturalAxisData.Z h j P eta := by linarith [small.j_pos]
  by_contra hn
  have hnonneg := mul_nonneg (mul_pos (by norm_num : (0:ℝ)<2) hL).le (le_of_not_gt hn)
  linarith

theorem natural_radial_derivative_quantitative
    {h j scale eta : ℝ} {P amp : ℝ → ℝ}
    {f u v pr : ℝ × ℝ → ℝ}
    (solution : NaturalProfile.IsNaturalSolution h j scale P amp f u v pr)
    (point : (0, eta) ∈ NaturalProfile.domain scale)
    (inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left
      NaturalAxisCoefficients.window.right)
    (small : NaturalAxisData.SmallParameters h j)
    (interval : eta ∈ Set.Ioo (-j / 4) (-j / 5))
    (root : NaturalAxisData.H h j eta = 0)
    (pressure : NaturalAxisData.PressureData P) :
    2 * NaturalAxisData.L h eta * NaturalAxisBridge.partialY u (0, eta) < -j / 5 := by
  have hen : eta < 0 := by linarith [interval.2, small.j_pos]
  have helo : -1 < eta := by linarith [interval.1, small.j_le]
  have heI : eta ∈ Set.Icc (-1 : ℝ) 1 := ⟨helo.le, by linarith⟩
  have hz := NaturalAxisData.Z_at_root_lower small interval root
    (pressure.negative eta heI) (pressure.deriv_nonpos heI hen)
  rw [natural_axis_radial_identity_from_solution solution point inside]
  linarith

theorem axial_component_derivative_tail
    {a : ℕ → ℕ} {h C : ℝ} {coeff : SlowBorelBase.Coefficients}
    {K : Set SlowBorelBase.Inner}
    (hh : 0 < h) (smooth : SlowBorelBase.SmoothCoefficients coeff)
    (admissible : SlowBorelBase.AdmissibleScales h
      (SlowBorelBase.coefficientBundle C coeff) K a) :
    ∃ J : ℕ, 1 ≤ J ∧ ∃ delta : ℝ, 0 < delta ∧
      ∀ q : ℝ, 0 < q → q < delta → ∀ w ∈ K,
      ‖iteratedFDeriv ℝ 1 (fun y =>
        SlowBorelBase.slowSum a h (SlowBorelBase.bundleComponent C coeff 5) y -
        SlowBorelBase.uncutPrefix h (SlowBorelBase.bundleComponent C coeff 5) J y) (q,w)‖ ≤
        (1/2 : ℝ)^J * q^(2*h) := by
  have ha := SlowBorelBase.admissible_component smooth admissible (5 : Fin 7)
  obtain ⟨J, hJ, _, delta, hd, bound⟩ :=
    SlowBorelBase.exists_ordinary_uncut_tail hh
      (SlowBorelBase.bundleComponent_smooth smooth C 5) ha 1 1 (2*h)
  exact ⟨J, hJ, delta, hd, fun q hq hqd w hw => bound 1 (by omega) q hq hqd w hw⟩

theorem selected_axial_component_derivative_tail
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
    (hh : 0 < F.data.h) :
    let a := FinalSlowBase.scales H v upper B
    let f := SlowBorelBase.bundleComponent W.axis.normalization
      (FinalSlowBase.coefficients H v) 5
    ∃ J : ℕ, 1 ≤ J ∧ ∃ delta : ℝ, 0 < delta ∧
      ∀ q : ℝ, 0 < q → q < delta →
      ∀ w ∈ SlowBorelBase.innerBox 0 (FinalSlowBase.boxRadius W upper),
      ‖iteratedFDeriv ℝ 1 (fun y => SlowBorelBase.slowSum a F.data.h f y -
        SlowBorelBase.uncutPrefix F.data.h f J y) (q,w)‖ ≤
        (1/2 : ℝ)^J * q^(2*F.data.h) := by
  exact axial_component_derivative_tail hh (FinalSlowBase.coefficients_smooth H v)
    (FinalSlowBase.scales_admissible H v upper B)

open scoped BigOperators

theorem finite_positive_prefix_tends_zero
    (h : ℝ) (hh : 0 < h) (J : ℕ) (c : ℕ → ℝ) :
    Filter.Tendsto (fun q : ℝ => ∑ j ∈ Finset.range J,
      q ^ (2*h*(j+1 : ℕ)) * c j) (𝓝 0) (𝓝 0) := by
  have each : ∀ j ∈ Finset.range J,
      Filter.Tendsto (fun q : ℝ => q ^ (2*h*(j+1 : ℕ)) * c j) (𝓝 0) (𝓝 0) := by
    intro j hj
    have exponent : 0 < 2*h*(j+1 : ℕ) := by positivity
    have hc : ContinuousAt (fun q : ℝ => q ^ (2*h*(j+1 : ℕ))) 0 := by
      exact Real.continuousAt_rpow_const _ _ (Or.inr exponent.le)
    have hz : (0 : ℝ) ^ (2*h*(j+1 : ℕ)) = 0 := Real.zero_rpow exponent.ne'
    simpa only [hz, zero_mul] using hc.tendsto.mul_const (c j)
  simpa using tendsto_finsetSum (Finset.range J) each

theorem finite_prefix_radial_derivative
    (h q baseDerivative : ℝ) (J : ℕ)
    (base : ℝ → ℝ) (f : ℕ → ℝ → ℝ) (c : ℕ → ℝ)
    (hb : HasDerivAt base baseDerivative 0)
    (hf : ∀ j ∈ Finset.range J, HasDerivAt (f j) (c j) 0) :
    HasDerivAt
      (fun X => base X + ∑ j ∈ Finset.range J,
        q ^ (2*h*(j+1 : ℕ)) * f j X)
      (baseDerivative + ∑ j ∈ Finset.range J,
        q ^ (2*h*(j+1 : ℕ)) * c j) 0 := by
  apply hb.add
  convert (HasDerivAt.sum fun j hj => (hf j hj).const_mul (q ^ (2*h*(j+1 : ℕ)))) using 1
  funext X
  simp only [Finset.sum_apply]

theorem finite_prefix_derivative_tends_leading
    (h baseDerivative : ℝ) (hh : 0 < h) (J : ℕ)
    (base : ℝ → ℝ) (f : ℕ → ℝ → ℝ) (c : ℕ → ℝ)
    (hb : HasDerivAt base baseDerivative 0)
    (hf : ∀ j ∈ Finset.range J, HasDerivAt (f j) (c j) 0) :
    Filter.Tendsto (fun q : ℝ => deriv
      (fun X => base X + ∑ j ∈ Finset.range J,
        q ^ (2*h*(j+1 : ℕ)) * f j X) 0)
      (𝓝 0) (𝓝 baseDerivative) := by
  have formula : ∀ q : ℝ, deriv
      (fun X => base X + ∑ j ∈ Finset.range J,
        q ^ (2*h*(j+1 : ℕ)) * f j X) 0 =
      baseDerivative + ∑ j ∈ Finset.range J, q ^ (2*h*(j+1 : ℕ)) * c j := by
    intro q
    exact (finite_prefix_radial_derivative h q baseDerivative J base f c hb hf).deriv
  simp_rw [formula]
  simpa only [add_zero] using
    (finite_positive_prefix_tends_zero h hh J c).const_add baseDerivative

theorem uncut_prefix_as_positive_sum
    (h q X eta : ℝ) (f : ℕ → SlowBorelBase.Inner → ℝ) (J : ℕ) :
    SlowBorelBase.uncutPrefix h f J (q,(X,eta)) =
      f 0 (X,eta) + ∑ j ∈ Finset.range J,
        q ^ (2*h*(j+1 : ℕ)) * f (j+1) (X,eta) := by
  unfold SlowBorelBase.uncutPrefix
  rw [Finset.sum_range_succ']
  simp only [SlowBorelBase.positiveCoefficient, Nat.add_one_ne_zero,
    ite_false, ite_eq_left, SlowBorelBase.powerCoefficient, smul_eq_mul, add_zero]

theorem uncut_prefix_derivative_tends_leading
    (h eta : ℝ) (hh : 0 < h) (J : ℕ)
    (f : ℕ → SlowBorelBase.Inner → ℝ) (c : ℕ → ℝ)
    (hf : ∀ j, HasDerivAt (fun X => f j (X,eta)) (c j) 0) :
    Filter.Tendsto (fun q : ℝ => deriv
      (fun X => SlowBorelBase.uncutPrefix h f J (q,(X,eta))) 0)
      (𝓝 0) (𝓝 (c 0)) := by
  simp_rw [uncut_prefix_as_positive_sum]
  exact finite_prefix_derivative_tends_leading h (c 0) hh J
    (fun X => f 0 (X,eta)) (fun j X => f (j+1) (X,eta))
    (fun j => c (j+1)) (hf 0) (fun j _ => hf (j+1))

theorem power_bounded_remainder_tends_zero
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (r : ℝ → E) (h C : ℝ) (hh : 0 < h)
    (bound : ∀ᶠ q in 𝓝[>] (0 : ℝ), ‖r q‖ ≤ C * q^(2*h)) :
    Filter.Tendsto r (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  have he : 0 < 2*h := by positivity
  have hc : ContinuousAt (fun q : ℝ => q^(2*h)) 0 :=
    Real.continuousAt_rpow_const _ _ (Or.inr he.le)
  have hz : (0 : ℝ)^(2*h) = 0 := Real.zero_rpow he.ne'
  apply squeeze_zero_norm' bound
  simpa only [hz, mul_zero] using
    (hc.tendsto.mono_left nhdsWithin_le_nhds).const_mul C

theorem axial_derivative_tail_tends_zero
    {a : ℕ → ℕ} {h C : ℝ} {coeff : SlowBorelBase.Coefficients}
    {K : Set SlowBorelBase.Inner} (w : SlowBorelBase.Inner) (hw : w ∈ K)
    (hh : 0 < h) (smooth : SlowBorelBase.SmoothCoefficients coeff)
    (admissible : SlowBorelBase.AdmissibleScales h
      (SlowBorelBase.coefficientBundle C coeff) K a) :
    ∃ J : ℕ, 1 ≤ J ∧ Filter.Tendsto (fun q : ℝ =>
      iteratedFDeriv ℝ 1 (fun y =>
        SlowBorelBase.slowSum a h (SlowBorelBase.bundleComponent C coeff 5) y -
        SlowBorelBase.uncutPrefix h (SlowBorelBase.bundleComponent C coeff 5) J y) (q,w))
      (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  obtain ⟨J, hJ, delta, hd, hb⟩ := axial_component_derivative_tail hh smooth admissible
  refine ⟨J, hJ, power_bounded_remainder_tends_zero _ h ((1/2 : ℝ)^J) hh ?_⟩
  filter_upwards [self_mem_nhdsWithin,
    Filter.Eventually.filter_mono nhdsWithin_le_nhds (gt_mem_nhds hd)] with q hq hqd
  exact hb q hq hqd w hw

theorem first_jet_radial_component_tends_zero
    (r : ℝ → ContinuousMultilinearMap ℝ
      (fun _ : Fin 1 => SlowBorelBase.Chart) ℝ)
    (hr : Filter.Tendsto r (𝓝[>] (0 : ℝ)) (𝓝 0)) :
    Filter.Tendsto (fun q => r q (fun _ => (0,(1,0))))
      (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  have hc : Continuous (fun L : ContinuousMultilinearMap ℝ
      (fun _ : Fin 1 => SlowBorelBase.Chart) ℝ => L (fun _ => (0,(1,0)))) := by
    fun_prop
  simpa only [Function.comp_def, ContinuousMultilinearMap.zero_apply] using hc.continuousAt.tendsto.comp hr

theorem chart_radial_derivative_eq_fderiv
    (g : SlowBorelBase.Chart → ℝ) (q X eta : ℝ)
    (hg : DifferentiableAt ℝ g (q,(X,eta))) :
    deriv (fun x => g (q,(x,eta))) X =
      fderiv ℝ g (q,(X,eta)) (0,(1,0)) := by
  have curve : HasDerivAt (fun x : ℝ => (q,(x,eta))) (0,(1,0)) X :=
    (hasDerivAt_const X q).prodMk ((hasDerivAt_id X).prodMk (hasDerivAt_const X eta))
  exact (hg.hasFDerivAt.comp_hasDerivAt X curve).deriv

#print axioms chart_radial_derivative_eq_fderiv
#print axioms first_jet_radial_component_tends_zero
#print axioms axial_derivative_tail_tends_zero
#print axioms power_bounded_remainder_tends_zero
#print axioms uncut_prefix_derivative_tends_leading
#print axioms uncut_prefix_as_positive_sum
#print axioms finite_prefix_derivative_tends_leading
#print axioms finite_prefix_radial_derivative
#print axioms finite_positive_prefix_tends_zero
#print axioms selected_axial_component_derivative_tail
#print axioms axial_component_derivative_tail
#print axioms natural_radial_derivative_quantitative
#print axioms natural_radial_derivative_negative_at_root
#print axioms natural_axis_radial_identity_from_solution
#print axioms natural_axis_radial_identity
#print axioms actual_axis_force_ratio_negative
#print axioms exists_negative_axis_force_ratio
end ConcentrationAware
