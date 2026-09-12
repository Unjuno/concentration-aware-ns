import NavierStokes.AxisymmetricResidual
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

open scoped Topology ContDiff

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

theorem radial_derivative_limit_of_first_jet
    (g : SlowBorelBase.Chart → ℝ) (eta : ℝ)
    (smooth : ∀ q : ℝ, 0 < q → DifferentiableAt ℝ g (q,(0,eta)))
    (limit : Filter.Tendsto (fun q : ℝ => iteratedFDeriv ℝ 1 g (q,(0,eta)))
      (𝓝[>] (0 : ℝ)) (𝓝 0)) :
    Filter.Tendsto (fun q : ℝ => deriv (fun X => g (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  have component := first_jet_radial_component_tends_zero _ limit
  apply component.congr'
  filter_upwards [self_mem_nhdsWithin] with q hq
  rw [iteratedFDeriv_one_apply]
  exact (chart_radial_derivative_eq_fderiv g q 0 eta (smooth q hq)).symm

theorem axial_radial_tail_tends_zero
    {a : ℕ → ℕ} {h C eta : ℝ} {coeff : SlowBorelBase.Coefficients}
    {K : Set SlowBorelBase.Inner} (hw : (0,eta) ∈ K)
    (hh : 0 < h) (smooth : SlowBorelBase.SmoothCoefficients coeff)
    (admissible : SlowBorelBase.AdmissibleScales h
      (SlowBorelBase.coefficientBundle C coeff) K a) :
    ∃ J : ℕ, 1 ≤ J ∧ Filter.Tendsto (fun q : ℝ =>
      deriv (fun X =>
        SlowBorelBase.slowSum a h (SlowBorelBase.bundleComponent C coeff 5) (q,(X,eta)) -
        SlowBorelBase.uncutPrefix h (SlowBorelBase.bundleComponent C coeff 5) J (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 0) := by
  obtain ⟨J, hJ, limit⟩ := axial_derivative_tail_tends_zero (0,eta) hw hh smooth admissible
  refine ⟨J, hJ, radial_derivative_limit_of_first_jet _ eta ?_ limit⟩
  intro q hq
  have hf := SlowBorelBase.bundleComponent_smooth smooth C (5 : Fin 7)
  have hs := SlowBorelBase.slowSum_smoothAt admissible.strictMono hf h (y := (q,(0,eta))) hq
  have hp : ContDiffAt ℝ ∞
      (SlowBorelBase.uncutPrefix h (SlowBorelBase.bundleComponent C coeff 5) J)
      (q,(0,eta)) := by
    unfold SlowBorelBase.uncutPrefix
    apply ((hf 0).comp contDiff_snd).contDiffAt.add
    exact ContDiffAt.sum (fun j _ => SlowBorelBase.positiveCoefficient_smoothAt hf h j hq)
  exact (hs.sub hp).differentiableAt (by simp)

theorem axial_radial_derivative_tends_leading
    {a : ℕ → ℕ} {h C eta : ℝ} {coeff : SlowBorelBase.Coefficients}
    {K : Set SlowBorelBase.Inner} (hw : (0,eta) ∈ K)
    (hh : 0 < h) (smooth : SlowBorelBase.SmoothCoefficients coeff)
    (admissible : SlowBorelBase.AdmissibleScales h
      (SlowBorelBase.coefficientBundle C coeff) K a) :
    Filter.Tendsto (fun q : ℝ => deriv (fun X =>
      SlowBorelBase.slowSum a h (SlowBorelBase.bundleComponent C coeff 5) (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ))
      (𝓝 (deriv (fun X => SlowBorelBase.bundleComponent C coeff 5 0 (X,eta)) 0)) := by
  let f := SlowBorelBase.bundleComponent C coeff 5
  have hf : ∀ j, ContDiff ℝ ∞ (f j) := SlowBorelBase.bundleComponent_smooth smooth C 5
  have curve : HasDerivAt (fun X : ℝ => (X,eta)) (1,0) 0 :=
    (hasDerivAt_id 0).prodMk (hasDerivAt_const 0 eta)
  have hd : ∀ j, DifferentiableAt ℝ (fun X => f j (X,eta)) 0 := by
    intro j
    exact ((hf j).differentiable (by simp)).differentiableAt.comp 0 curve.differentiableAt
  obtain ⟨J, _, ht⟩ := axial_radial_tail_tends_zero hw hh smooth admissible
  have hp := (uncut_prefix_derivative_tends_leading h eta hh J f
    (fun j => deriv (fun X => f j (X,eta)) 0)
    (fun j => (hd j).hasDerivAt)).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  have total := ht.add hp
  simp only [zero_add] at total
  apply total.congr'
  filter_upwards [self_mem_nhdsWithin] with q hq
  have hs : DifferentiableAt ℝ (fun X => SlowBorelBase.slowSum a h f (q,(X,eta))) 0 := by
    have hc : HasDerivAt (fun X : ℝ => (q,(X,eta))) (0,(1,0)) 0 :=
      (hasDerivAt_const 0 q).prodMk curve
    exact ((SlowBorelBase.slowSum_smoothAt admissible.strictMono hf h
      (y := (q,(0,eta))) hq).differentiableAt (by simp)).comp 0 hc.differentiableAt
  have hprefix : DifferentiableAt ℝ (fun X => SlowBorelBase.uncutPrefix h f J (q,(X,eta))) 0 := by
    simp_rw [uncut_prefix_as_positive_sum]
    exact (finite_prefix_radial_derivative h q _ J (f := fun j X => f (j+1) (X,eta))
      (base := fun X => f 0 (X,eta)) (c := fun j => deriv (fun X => f (j+1) (X,eta)) 0)
      (hd 0).hasDerivAt (fun j _ => (hd (j+1)).hasDerivAt)).differentiableAt
  change deriv (fun X => SlowBorelBase.slowSum a h f (q,(X,eta)) -
    SlowBorelBase.uncutPrefix h f J (q,(X,eta))) 0 + _ = _
  have he := deriv_sub hs hprefix
  change deriv (fun X => SlowBorelBase.slowSum a h f (q,(X,eta)) -
    SlowBorelBase.uncutPrefix h f J (q,(X,eta))) 0 = _ at he
  rw [he]
  exact sub_add_cancel _ _

theorem selected_axial_radial_derivative_tends_leading
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (hh : 0 < F.data.h) (heta : eta ∈ Set.Icc (-1 : ℝ) 1) :
    let a := FinalSlowBase.scales H v upper B
    let f := SlowBorelBase.bundleComponent W.axis.normalization
      (FinalSlowBase.coefficients H v) 5
    Filter.Tendsto (fun q : ℝ => deriv
      (fun X => SlowBorelBase.slowSum a F.data.h f (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 (deriv (fun X => f 0 (X,eta)) 0)) := by
  have hr : 0 ≤ FinalSlowBase.boxRadius W upper :=
    (FinalSlowBase.terminal_pos W).le.trans (le_max_right _ _)
  have hw : (0,eta) ∈ SlowBorelBase.innerBox 0 (FinalSlowBase.boxRadius W upper) :=
    ⟨⟨le_rfl, hr⟩, heta⟩
  exact axial_radial_derivative_tends_leading hw hh
    (FinalSlowBase.coefficients_smooth H v)
    (FinalSlowBase.scales_admissible H v upper B)

theorem deriv_eq_of_nonnegative_agreement
    (f g : ℝ → ℝ) (hf : DifferentiableAt ℝ f 0) (hg : DifferentiableAt ℝ g 0)
    (agree : ∀ x : ℝ, 0 ≤ x → f x = g x) : deriv f 0 = deriv g 0 := by
  have he : derivWithin f (Set.Ici 0) 0 = derivWithin g (Set.Ici 0) 0 :=
    derivWithin_congr (fun x hx => agree x hx) (agree 0 le_rfl)
  rw [hf.derivWithin (uniqueDiffWithinAt_Ici 0),
    hg.derivWithin (uniqueDiffWithinAt_Ici 0)] at he
  exact he

theorem selected_leading_derivative_eq_modulated
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (eta : ℝ)
    (heta : |eta| ≤ 1) :
    deriv (fun X => SlowBorelBase.bundleComponent W.axis.normalization
      (FinalSlowBase.coefficients H v) 5 0 (X,eta)) 0 =
    deriv (fun X => v.profiles.U (X,eta)) 0 := by
  have hp : (0,eta) ∈ ld.domain.carrier :=
    ld.domain_nonnegative (p := (0,eta)) le_rfl (ld.parameters_contains (abs_le.mp heta))
  have curve : HasDerivAt (fun X : ℝ => (X,eta)) (1,0) 0 :=
    (hasDerivAt_id 0).prodMk (hasDerivAt_const 0 eta)
  have hv : DifferentiableAt ℝ (fun X => v.profiles.U (X,eta)) 0 :=
    ((v.profiles.U_smooth.contDiffAt (ld.domain.isOpen.mem_nhds hp)).differentiableAt
      (by simp)).comp 0 curve.differentiableAt
  refine deriv_eq_of_nonnegative_agreement _ _ ?_ hv ?_
  · have hf := SlowBorelBase.bundleComponent_smooth
      (FinalSlowBase.coefficients_smooth H v) W.axis.normalization (5 : Fin 7) 0
    have curve : HasDerivAt (fun X : ℝ => (X,eta)) (1,0) 0 :=
      (hasDerivAt_id 0).prodMk (hasDerivAt_const 0 eta)
    exact (hf.differentiable (by simp)).differentiableAt.comp 0 curve.differentiableAt
  · intro X hX
    simpa [SlowBorelBase.bundleComponent, SlowBorelBase.coefficientBundle,
      FinalSlowBase.coefficients] using
      (EntranceAlignedBase.modulated_zero_fields H v (p := (X,eta)) hX heta).2.1

theorem selected_axial_radial_derivative_tends_modulated
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (hh : 0 < F.data.h) (heta : eta ∈ Set.Icc (-1 : ℝ) 1) :
    Filter.Tendsto (fun q : ℝ => deriv (fun X =>
      SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) F.data.h
        (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
        (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 (deriv (fun X => v.profiles.U (X,eta)) 0)) := by
  have limit := selected_axial_radial_derivative_tends_leading H v upper eta B hh heta
  dsimp only at limit
  rw [selected_leading_derivative_eq_modulated H v eta (abs_le.mpr heta)] at limit
  exact limit

theorem modulated_axis_derivative_eq_original
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (eta : ℝ) :
    deriv (fun X => v.profiles.U (X,eta)) 0 =
      deriv (fun X => W.profiles.U (X,eta)) 0 := by
  have hlo : 0 < ld.modulation.left :=
    (div_pos (by norm_num : (0 : ℝ) < 4) W.axis.scale_pos).trans ld.after_initial
  have he : (fun X => v.profiles.U (X,eta)) =ᶠ[𝓝 (0 : ℝ)]
      (fun X => W.profiles.U (X,eta)) := by
    filter_upwards [gt_mem_nhds hlo] with X hX
    exact (v.fields_outside (p := (X,eta)) (by intro hp; linarith [hp.1])).2
  exact he.deriv_eq

theorem selected_axial_radial_derivative_tends_original
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (hh : 0 < F.data.h) (heta : eta ∈ Set.Icc (-1 : ℝ) 1) :
    Filter.Tendsto (fun q : ℝ => deriv (fun X =>
      SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) F.data.h
        (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
        (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 (deriv (fun X => W.profiles.U (X,eta)) 0)) := by
  have limit := selected_axial_radial_derivative_tends_modulated H v upper eta B hh heta
  rw [modulated_axis_derivative_eq_original v eta] at limit
  exact limit

theorem original_axis_derivative_eq_natural
    {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
    (eta : ℝ) :
    deriv (fun X => W.profiles.U (X,eta)) 0 =
      deriv (fun X => W.axis.natural.profile.family.U (X,eta)) 0 := by
  have hlo : 0 < 4 / W.axis.scale := div_pos (by norm_num) W.axis.scale_pos
  have he : (fun X => W.profiles.U (X,eta)) =ᶠ[𝓝 (0 : ℝ)]
      (fun X => W.axis.natural.profile.family.U (X,eta)) := by
    filter_upwards [gt_mem_nhds hlo, gt_mem_nhds NominalProfile.Xi_pos] with X hX hXi
    exact (W.controls.physical_before_Xi W.separated (p := (X,eta)) hXi.le).1.trans
      (W.controls.seed_initial (p := (X,eta)) hX.le).2
  exact he.deriv_eq

theorem selected_axial_radial_derivative_tends_natural
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (hh : 0 < F.data.h) (heta : eta ∈ Set.Icc (-1 : ℝ) 1) :
    Filter.Tendsto (fun q : ℝ => deriv (fun X =>
      SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) F.data.h
        (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
        (q,(X,eta))) 0)
      (𝓝[>] (0 : ℝ)) (𝓝 (deriv (fun X => W.axis.natural.profile.family.U (X,eta)) 0)) := by
  have limit := selected_axial_radial_derivative_tends_original H v upper eta B hh heta
  rw [original_axis_derivative_eq_natural W eta] at limit
  exact limit

theorem selected_natural_derivative_negative
    {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F) (eta : ℝ)
    (point : (0,eta) ∈ NaturalProfile.domain W.axis.scale)
    (inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left NaturalAxisCoefficients.window.right)
    (interval : eta ∈ Set.Ioo (-W.axis.j / 4) (-W.axis.j / 5))
    (root : NaturalAxisData.H F.data.h W.axis.j eta = 0)
    (pressure : NaturalAxisData.PressureData F.axisDatum) :
    deriv (fun X => W.axis.natural.profile.family.U (X,eta)) 0 < 0 := by
  exact natural_radial_derivative_negative_at_root W.axis.natural.profile.family.natural
    point inside W.axis.small interval root pressure

theorem selected_axial_radial_derivative_eventually_negative
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (heta : eta ∈ Set.Icc (-1 : ℝ) 1)
    (point : (0,eta) ∈ NaturalProfile.domain W.axis.scale)
    (inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left NaturalAxisCoefficients.window.right)
    (interval : eta ∈ Set.Ioo (-W.axis.j / 4) (-W.axis.j / 5))
    (root : NaturalAxisData.H F.data.h W.axis.j eta = 0)
    (pressure : NaturalAxisData.PressureData F.axisDatum) :
    ∀ᶠ q in 𝓝[>] (0 : ℝ), deriv (fun X =>
      SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) F.data.h
        (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
        (q,(X,eta))) 0 < 0 := by
  have limit := selected_axial_radial_derivative_tends_natural H v upper eta B
    W.axis.small.h_pos heta
  exact limit.eventually (gt_mem_nhds
    (selected_natural_derivative_negative W eta point inside interval root pressure))

theorem exists_selected_root_with_negative_radial_derivative
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
    (hP : 2 ≤ F.data.core.P) :
    ∃ eta : ℝ, eta ∈ Set.Ioo (-W.axis.j / 4) (-W.axis.j / 5) ∧
      NaturalAxisData.H F.data.h W.axis.j eta = 0 ∧
      ∀ᶠ q in 𝓝[>] (0 : ℝ), deriv (fun X =>
        SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) F.data.h
          (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
          (q,(X,eta))) 0 < 0 := by
  have pressure := F.natural_axis_pressureData hP
  obtain ⟨eta, interval, root, _⟩ :=
    NaturalAxisData.exists_root_with_positive_Z W.axis.small pressure
  have hen : eta < 0 := by linarith [interval.2, W.axis.small.j_pos]
  have helo : -1 < eta := by linarith [interval.1, W.axis.small.j_le]
  have heta : eta ∈ Set.Icc (-1 : ℝ) 1 := ⟨helo.le, by linarith⟩
  have inside : eta ∈ Set.Ioo NaturalAxisCoefficients.window.left
      NaturalAxisCoefficients.window.right := by
    change -11 / 10 < eta ∧ eta < 11 / 10
    constructor <;> linarith
  have point : (0,eta) ∈ NaturalProfile.domain W.axis.scale := by
    change (W.axis.scale * 0, eta) ∈ Set.Ioo (-20 : ℝ) 20 ×ˢ
      Set.Ioo NaturalAxisCoefficients.window.left NaturalAxisCoefficients.window.right
    exact ⟨by norm_num, inside⟩
  exact ⟨eta, interval, root, selected_axial_radial_derivative_eventually_negative
    H v upper eta B heta point inside interval root pressure⟩

theorem prepared_root_with_negative_radial_derivative
    (prepared : PreparedOutgoing.PreparedProfile)
    {W : NominalProfile.Witness prepared.profile}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ) :
    ∃ eta : ℝ, eta ∈ Set.Ioo (-W.axis.j / 4) (-W.axis.j / 5) ∧
      NaturalAxisData.H prepared.profile.data.h W.axis.j eta = 0 ∧
      ∀ᶠ q in 𝓝[>] (0 : ℝ), deriv (fun X =>
        SlowBorelBase.slowSum (FinalSlowBase.scales H v upper B) prepared.profile.data.h
          (SlowBorelBase.bundleComponent W.axis.normalization (FinalSlowBase.coefficients H v) 5)
          (q,(X,eta))) 0 < 0 := by
  exact exists_selected_root_with_negative_radial_derivative H v upper B prepared.amplitude_lower

theorem physical_axial_laplacian_on_axis
    {B F U : AxisymmetricFields.Profile} {t : ℝ}
    (hB : AxisymmetricResidual.SliceC2 B t)
    (hF : AxisymmetricResidual.SliceC2 F t)
    (hU : AxisymmetricResidual.SliceC2 U t) (z : ℝ) :
    ProblemStatement.spatialLaplacian (AxisymmetricResidual.velocity B F U) t
      (AxisymmetricResidual.pack 0 0 z) 2 =
      2 * AxisymmetricFields.partialS U (t,(0,z)) +
      AxisymmetricFields.partialZ (AxisymmetricFields.partialZ U) (t,(0,z)) := by
  rw [AxisymmetricResidual.spatialLaplacian_velocity hB hF hU]
  simp [AxisymmetricResidual.laplaceScalar, AxisymmetricFields.profilePoint,
    AxisymmetricFields.radialEnergy]

theorem stream_axial_radial_derivative_on_axis
    (H : AxisymmetricFields.Profile) (t z : ℝ)
    (hH : DifferentiableAt ℝ H (t,(0,z)))
    (hS : DifferentiableAt ℝ (AxisymmetricFields.partialS H) (t,(0,z))) :
    AxisymmetricFields.partialS
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) (t,(0,z)) =
      2 * AxisymmetricFields.partialS H (t,(0,z)) := by
  have coord : HasFDerivAt (fun p : AxisymmetricFields.ProfilePoint => p.2.1)
      ((ContinuousLinearMap.fst ℝ ℝ ℝ).comp (ContinuousLinearMap.snd ℝ ℝ (ℝ × ℝ)))
      (t,(0,z)) := by
    exact hasFDerivAt_fst.comp (t,(0,z)) hasFDerivAt_snd
  have hd := hH.hasFDerivAt.add (coord.mul hS.hasFDerivAt)
  have he := congrArg (fun L => L (0,(1,0))) hd.fderiv
  change (fderiv ℝ (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)
    (t,(0,z))) (0,(1,0)) = _ at he
  change (fderiv ℝ (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)
    (t,(0,z))) (0,(1,0)) = _
  rw [he]
  simp [AxisymmetricFields.partialS]
  ring

theorem axial_slice_derivative_eq_partialZ
    (G : AxisymmetricFields.Profile) (t s z : ℝ)
    (hG : DifferentiableAt ℝ G (t,(s,z))) :
    deriv (fun w => G (t,(s,w))) z = AxisymmetricFields.partialZ G (t,(s,z)) := by
  have curve : HasDerivAt (fun w : ℝ => (t,(s,w))) (0,(0,1)) z :=
    (hasDerivAt_const z t).prodMk ((hasDerivAt_const z s).prodMk (hasDerivAt_id z))
  exact (hG.hasFDerivAt.comp_hasDerivAt z curve).deriv

theorem axial_second_derivative_eq_slice
    (G : AxisymmetricFields.Profile) (t z : ℝ)
    (hG : ∀ w : ℝ, DifferentiableAt ℝ G (t,(0,w)))
    (hZ : DifferentiableAt ℝ (AxisymmetricFields.partialZ G) (t,(0,z))) :
    AxisymmetricFields.partialZ (AxisymmetricFields.partialZ G) (t,(0,z)) =
      deriv (fun w => deriv (fun a => G (t,(0,a))) w) z := by
  rw [← axial_slice_derivative_eq_partialZ _ t 0 z hZ]
  congr 1
  funext w
  exact (axial_slice_derivative_eq_partialZ G t 0 w (hG w)).symm

theorem stream_axial_second_derivative_on_axis
    (H : AxisymmetricFields.Profile) (t z : ℝ)
    (hH : ∀ w : ℝ, DifferentiableAt ℝ H (t,(0,w)))
    (hU : ∀ w : ℝ, DifferentiableAt ℝ
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) (t,(0,w)))
    (hHZ : DifferentiableAt ℝ (AxisymmetricFields.partialZ H) (t,(0,z)))
    (hUZ : DifferentiableAt ℝ (AxisymmetricFields.partialZ
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)) (t,(0,z))) :
    AxisymmetricFields.partialZ (AxisymmetricFields.partialZ
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)) (t,(0,z)) =
    AxisymmetricFields.partialZ (AxisymmetricFields.partialZ H) (t,(0,z)) := by
  rw [axial_second_derivative_eq_slice _ t z hU hUZ,
    axial_second_derivative_eq_slice H t z hH hHZ]
  simp only [zero_mul, add_zero]

theorem physical_stream_laplacian_on_axis
    (H B F : AxisymmetricFields.Profile) (t z : ℝ)
    (hB : AxisymmetricResidual.SliceC2 B t)
    (hF : AxisymmetricResidual.SliceC2 F t)
    (hU : AxisymmetricResidual.SliceC2
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) t)
    (hH : ∀ w : ℝ, DifferentiableAt ℝ H (t,(0,w)))
    (hS : DifferentiableAt ℝ (AxisymmetricFields.partialS H) (t,(0,z)))
    (hHZ : DifferentiableAt ℝ (AxisymmetricFields.partialZ H) (t,(0,z)))
    (hUZ : DifferentiableAt ℝ (AxisymmetricFields.partialZ
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)) (t,(0,z))) :
    ProblemStatement.spatialLaplacian (AxisymmetricResidual.velocity B F
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)) t
      (AxisymmetricResidual.pack 0 0 z) 2 =
      4 * AxisymmetricFields.partialS H (t,(0,z)) +
      AxisymmetricFields.partialZ (AxisymmetricFields.partialZ H) (t,(0,z)) := by
  have hUd : ∀ w : ℝ, DifferentiableAt ℝ
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) (t,(0,w)) := by
    intro w
    simpa [AxisymmetricFields.profilePoint, AxisymmetricFields.radialEnergy] using
      hU.differentiable (AxisymmetricResidual.pack 0 0 w)
  rw [physical_axial_laplacian_on_axis hB hF hU z,
    stream_axial_radial_derivative_on_axis H t z (hH z) hS,
    stream_axial_second_derivative_on_axis H t z hH hUd hHZ hUZ]
  ring

theorem physical_stream_laplacian_of_sliceC2
    (H B F : AxisymmetricFields.Profile) (t z : ℝ)
    (hB : AxisymmetricResidual.SliceC2 B t)
    (hF : AxisymmetricResidual.SliceC2 F t)
    (hH : AxisymmetricResidual.SliceC2 H t)
    (hU : AxisymmetricResidual.SliceC2
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) t) :
    ProblemStatement.spatialLaplacian (AxisymmetricResidual.velocity B F
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p)) t
      (AxisymmetricResidual.pack 0 0 z) 2 =
      4 * AxisymmetricFields.partialS H (t,(0,z)) +
      AxisymmetricFields.partialZ (AxisymmetricFields.partialZ H) (t,(0,z)) := by
  have atAxis (G : AxisymmetricFields.Profile) (hg : AxisymmetricResidual.SliceC2 G t)
      (w : ℝ) : ContDiffAt ℝ 2 G (t,(0,w)) := by
    simpa [AxisymmetricFields.profilePoint, AxisymmetricFields.radialEnergy] using
      hg (AxisymmetricResidual.pack 0 0 w)
  have directional (G : AxisymmetricFields.Profile) (hg : AxisymmetricResidual.SliceC2 G t)
      (direction : AxisymmetricFields.ProfilePoint) :
      DifferentiableAt ℝ (fun p => fderiv ℝ G p direction) (t,(0,z)) := by
    exact (((atAxis G hg z).fderiv_right (m := 1) (by norm_num)).clm_apply
      contDiffAt_const).differentiableAt (by norm_num)
  exact physical_stream_laplacian_on_axis H B F t z hB hF hU
    (fun w => (atAxis H hH w).differentiableAt (by norm_num))
    (directional H hH (0,(1,0))) (directional H hH (0,(0,1)))
    (directional _ hU (0,(0,1)))

theorem selected_stream_sliceC2
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t : ℝ) (B : ℕ)
    (ht : t < 1) :
    AxisymmetricResidual.SliceC2
      (SlowBorelBase.streamFactor (FinalSlowBase.scales H v upper B) F.data.h
        W.axis.normalization (FinalSlowBase.coefficients H v)) t := by
  intro x
  have hh1 : F.data.h < 1 / 2 := by linarith [W.axis.small.h_le]
  have hs := SlowBorelBase.physicalProfile_smoothAt
    (FinalSlowBase.scales_admissible H v upper B).strictMono W.axis.small.h_pos hh1
    (SlowBorelBase.bundleComponent_smooth (FinalSlowBase.coefficients_smooth H v)
      W.axis.normalization (0 : Fin 7)) (-CoordinateAlgebra.A F.data.h)
    (p := AxisymmetricFields.profilePoint t x) ht
  exact hs.of_le (by simp)

theorem selected_stream_axial_velocity_sliceC2
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t : ℝ) (B : ℕ)
    (ht : t < 1) :
    let stream := SlowBorelBase.streamFactor (FinalSlowBase.scales H v upper B) F.data.h
      W.axis.normalization (FinalSlowBase.coefficients H v)
    AxisymmetricResidual.SliceC2
      (fun p => stream p + p.2.1 * AxisymmetricFields.partialS stream p) t := by
  intro stream x
  have hh1 : F.data.h < 1 / 2 := by linarith [W.axis.small.h_le]
  have hs : ContDiffAt ℝ ∞ stream (AxisymmetricFields.profilePoint t x) :=
    SlowBorelBase.physicalProfile_smoothAt
      (FinalSlowBase.scales_admissible H v upper B).strictMono W.axis.small.h_pos hh1
      (SlowBorelBase.bundleComponent_smooth (FinalSlowBase.coefficients_smooth H v)
        W.axis.normalization (0 : Fin 7)) (-CoordinateAlgebra.A F.data.h) ht
  have hder : ContDiffAt ℝ 2 (AxisymmetricFields.partialS stream)
      (AxisymmetricFields.profilePoint t x) := by
    exact (hs.fderiv_right (m := 2) (by simp)).clm_apply contDiffAt_const
  exact (hs.of_le (by simp)).add ((contDiffAt_snd.fst).mul hder)

theorem selected_transverse_profiles_sliceC2
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t : ℝ) (B : ℕ)
    (ht : t < 1) :
    let a := FinalSlowBase.scales H v upper B
    let d := FinalSlowBase.coefficients H v
    AxisymmetricResidual.SliceC2
      (fun p => AxisymmetricFields.partialZ (SlowBorelBase.streamFactor a F.data.h W.axis.normalization d) p / 2) t ∧
    AxisymmetricResidual.SliceC2
      (fun p => -AxisymmetricFields.partialS (SlowBorelBase.swirlPotential a F.data.h W.axis.normalization d) p) t := by
  intro a d
  have hh1 : F.data.h < 1 / 2 := by linarith [W.axis.small.h_le]
  have smooth (i : Fin 7) (b : ℝ) (x : ProblemStatement.Space) :=
    SlowBorelBase.physicalProfile_smoothAt
      (FinalSlowBase.scales_admissible H v upper B).strictMono W.axis.small.h_pos hh1
      (SlowBorelBase.bundleComponent_smooth (FinalSlowBase.coefficients_smooth H v)
        W.axis.normalization i) b (p := AxisymmetricFields.profilePoint t x) ht
  constructor
  · intro x
    exact (((smooth 0 (-CoordinateAlgebra.A F.data.h) x).fderiv_right
      (m := 2) (by simp)).clm_apply contDiffAt_const).div_const 2
  · intro x
    exact (((smooth 1 (1 / 2 - CoordinateAlgebra.A F.data.h) x).fderiv_right
      (m := 2) (by simp)).clm_apply contDiffAt_const).neg

theorem selected_profile_velocity_laplacian_on_axis
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t z : ℝ) (B : ℕ)
    (ht : t < 1) :
    let a := FinalSlowBase.scales H v upper B
    let d := FinalSlowBase.coefficients H v
    let stream := SlowBorelBase.streamFactor a F.data.h W.axis.normalization d
    let swirl := SlowBorelBase.swirlPotential a F.data.h W.axis.normalization d
    ProblemStatement.spatialLaplacian (AxisymmetricResidual.velocity
      (fun p => AxisymmetricFields.partialZ stream p / 2)
      (fun p => -AxisymmetricFields.partialS swirl p)
      (fun p => stream p + p.2.1 * AxisymmetricFields.partialS stream p)) t
      (AxisymmetricResidual.pack 0 0 z) 2 =
      4 * AxisymmetricFields.partialS stream (t,(0,z)) +
      AxisymmetricFields.partialZ (AxisymmetricFields.partialZ stream) (t,(0,z)) := by
  intro a d stream swirl
  have transverse := selected_transverse_profiles_sliceC2 H v upper t B ht
  exact physical_stream_laplacian_of_sliceC2 stream _ _ t z transverse.1 transverse.2
    (selected_stream_sliceC2 H v upper t B ht)
    (selected_stream_axial_velocity_sliceC2 H v upper t B ht)

theorem curl_velocity_eq_profile_velocity
    (H K : AxisymmetricFields.Profile) (t : ℝ) (x : ProblemStatement.Space)
    (hH : DifferentiableAt ℝ H (AxisymmetricFields.profilePoint t x))
    (hK : DifferentiableAt ℝ K (AxisymmetricFields.profilePoint t x)) :
    AxisymmetricFields.velocity H K (t,x) =
    AxisymmetricResidual.velocity (fun p => AxisymmetricFields.partialZ H p / 2)
      (fun p => -AxisymmetricFields.partialS K p)
      (fun p => H p + p.2.1 * AxisymmetricFields.partialS H p) (t,x) := by
  ext i
  fin_cases i <;> dsimp only
  · change AxisymmetricFields.velocity H K (t,x) 0 = _
    rw [AxisymmetricFields.velocity_zero H K t x hH hK]
    simp [AxisymmetricResidual.velocity, AxisymmetricResidual.componentX,
      AxisymmetricResidual.lift]
    ring
  · change AxisymmetricFields.velocity H K (t,x) 1 = _
    rw [AxisymmetricFields.velocity_one H K t x hH hK]
    simp [AxisymmetricResidual.velocity, AxisymmetricResidual.componentY,
      AxisymmetricResidual.lift]
    ring
  · change AxisymmetricFields.velocity H K (t,x) 2 = _
    rw [AxisymmetricFields.velocity_two H K t x hH hK]
    simp [AxisymmetricResidual.velocity, AxisymmetricResidual.lift,
      AxisymmetricFields.profilePoint]

theorem selected_base_velocity_slice_eq
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t : ℝ) (B : ℕ)
    (ht : t < 1) :
    let a := FinalSlowBase.scales H v upper B
    let d := FinalSlowBase.coefficients H v
    let stream := SlowBorelBase.streamFactor a F.data.h W.axis.normalization d
    let swirl := SlowBorelBase.swirlPotential a F.data.h W.axis.normalization d
    (fun x => SlowBorelBase.baseVelocity a F.data.h W.axis.normalization d (t,x)) =
    (fun x => AxisymmetricResidual.velocity
      (fun p => AxisymmetricFields.partialZ stream p / 2)
      (fun p => -AxisymmetricFields.partialS swirl p)
      (fun p => stream p + p.2.1 * AxisymmetricFields.partialS stream p) (t,x)) := by
  intro a d stream swirl
  funext x
  have hh1 : F.data.h < 1 / 2 := by linarith [W.axis.small.h_le]
  have hk := SlowBorelBase.physicalProfile_smoothAt
    (FinalSlowBase.scales_admissible H v upper B).strictMono W.axis.small.h_pos hh1
    (SlowBorelBase.bundleComponent_smooth (FinalSlowBase.coefficients_smooth H v)
      W.axis.normalization (1 : Fin 7)) (1 / 2 - CoordinateAlgebra.A F.data.h)
    (p := AxisymmetricFields.profilePoint t x) ht
  exact curl_velocity_eq_profile_velocity stream swirl t x
    ((selected_stream_sliceC2 H v upper t B ht).differentiable x)
    (hk.differentiableAt (by simp))

theorem selected_base_velocity_laplacian_on_axis
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper t z : ℝ) (B : ℕ)
    (ht : t < 1) :
    let a := FinalSlowBase.scales H v upper B
    let d := FinalSlowBase.coefficients H v
    let stream := SlowBorelBase.streamFactor a F.data.h W.axis.normalization d
    ProblemStatement.spatialLaplacian
      (SlowBorelBase.baseVelocity a F.data.h W.axis.normalization d) t
      (AxisymmetricResidual.pack 0 0 z) 2 =
      4 * AxisymmetricFields.partialS stream (t,(0,z)) +
      AxisymmetricFields.partialZ (AxisymmetricFields.partialZ stream) (t,(0,z)) := by
  have formula := selected_profile_velocity_laplacian_on_axis H v upper t z B ht
  have he := selected_base_velocity_slice_eq H v upper t B ht
  dsimp only at formula he ⊢
  unfold ProblemStatement.spatialLaplacian ProblemStatement.spatialDerivative at formula ⊢
  rw [he]
  exact formula

theorem selected_stream_radial_derivative_physical
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
    (p : SlowBorelBase.Chart) (hp : p.1 < 1) :
    let a := FinalSlowBase.scales H v upper B
    let d := FinalSlowBase.coefficients H v
    AxisymmetricFields.partialS (SlowBorelBase.streamFactor a F.data.h W.axis.normalization d) p =
    SlowBorelBase.physicalProfile a F.data.h (-CoordinateAlgebra.A F.data.h - 1)
      (fun j => SimilarityProfile.partialX
        (SlowBorelBase.bundleComponent W.axis.normalization d 0 j)) p := by
  have hh1 : F.data.h < 1 / 2 := by linarith [W.axis.small.h_le]
  exact SlowBorelBase.partialS_physicalProfile
    (FinalSlowBase.scales_admissible H v upper B).strictMono W.axis.small.h_pos hh1
    (SlowBorelBase.bundleComponent_smooth (FinalSlowBase.coefficients_smooth H v)
      W.axis.normalization (0 : Fin 7)) (-CoordinateAlgebra.A F.data.h) hp

open MeasureTheory in
 theorem radial_derivative_compact_integral
    {s : Set ProfileHistories.Point} {G : ProfileHistories.Point → ℝ → ℝ}
    (hs : IsOpen s)
    (hG : ∀ p ∈ s, ∀ t ∈ Set.Icc (0 : ℝ) 1,
      ContDiffAt ℝ ∞ (fun z : ProfileHistories.Point × ℝ => G z.1 z.2) (p,t))
    {p : ProfileHistories.Point} (hp : p ∈ s) :
    ProfileHistories.radialPartial (fun q => ∫ t in (0 : ℝ)..1, G q t) p =
      ∫ t in (0 : ℝ)..1, ProfileHistories.radialPartial (fun q => G q t) p := by
  have hi : IntervalIntegrable (fun t => fderiv ℝ (fun q => G q t) p) volume 0 1 :=
    ((ProfileHistories.compact_parameter_fderiv_continuous hG).comp
      (continuous_const.prodMk continuous_id).continuousOn
      (fun _ ht => ⟨hp,ht⟩)).intervalIntegrable_of_Icc zero_le_one
  unfold ProfileHistories.radialPartial
  rw [(ProfileHistories.compact_parameter_integral_hasFDerivAt hs hG hp).fderiv]
  exact ContinuousLinearMap.intervalIntegral_apply hi (1,0)

theorem average_radial_derivative_at_axis
    (D : ProfileHistories.RadialDomain) (F : ProfileHistories.Field)
    (hF : ContDiffOn ℝ ∞ F D.carrier) (eta : ℝ) (hp : (0,eta) ∈ D.carrier) :
    ProfileHistories.radialPartial (ProfileHistories.average F) (0,eta) =
      (1/2 : ℝ) * ProfileHistories.radialPartial F (0,eta) := by
  unfold ProfileHistories.average
  rw [radial_derivative_compact_integral D.isOpen
    (ProfileHistories.average_integrand_smooth D hF) hp]
  have integrand (r : ℝ) :
      ProfileHistories.radialPartial (fun q => F (r*q.1,q.2)) (0,eta) =
      r * ProfileHistories.radialPartial F (0,eta) := by
    have hf := (hF.contDiffAt (D.isOpen.mem_nhds hp)).differentiableAt (by simp)
    have hc : HasFDerivAt (fun q : ℝ × ℝ => (r*q.1,q.2))
        ((r • ContinuousLinearMap.fst ℝ ℝ ℝ).prod (ContinuousLinearMap.snd ℝ ℝ ℝ)) (0,eta) := by
      exact (hasFDerivAt_fst.const_mul r).prodMk hasFDerivAt_snd
    have hf2 : HasFDerivAt F (fderiv ℝ F (0,eta)) (r*0,eta) := by simpa using hf.hasFDerivAt
    have hd := hf2.comp (0,eta) hc
    have he := congrArg (fun L => L (1,0)) hd.fderiv
    change (fderiv ℝ (fun q => F (r*q.1,q.2)) (0,eta)) (1,0) = _ at he
    unfold ProfileHistories.radialPartial
    rw [he]
    simp
    simpa only [Prod.smul_mk, smul_eq_mul, mul_one, mul_zero] using
      (fderiv ℝ F (0,eta)).map_smul r (1, (0 : ℝ))
  simp_rw [integrand]
  rw [intervalIntegral.integral_mul_const]
  norm_num [integral_id]

theorem bundle_average_derivative_at_axis
    (C : ℝ) (d : SlowBorelBase.Coefficients)
    (hd : SlowBorelBase.SmoothCoefficients d) (j : ℕ) (eta : ℝ) :
    SimilarityProfile.partialX (SlowBorelBase.bundleComponent C d 0 j) (0,eta) =
      (1/2 : ℝ) * SimilarityProfile.partialX (SlowBorelBase.bundleComponent C d 5 j) (0,eta) := by
  have he := average_radial_derivative_at_axis SlowBorelBase.globalRadialDomain
    (d.axial j) (hd.axial j).contDiffOn eta (Set.mem_univ _)
  have h0 : SlowBorelBase.bundleComponent C d 0 j = ProfileHistories.average (d.axial j) := by
    funext w
    simp [SlowBorelBase.bundleComponent, SlowBorelBase.coefficientBundle]
  have h5 : SlowBorelBase.bundleComponent C d 5 j = d.axial j := by
    funext w
    simp [SlowBorelBase.bundleComponent, SlowBorelBase.coefficientBundle]
  rw [h0,h5]
  exact he

theorem selected_bundle_average_derivative_at_axis
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (j : ℕ) (eta : ℝ) :
    SimilarityProfile.partialX (SlowBorelBase.bundleComponent W.axis.normalization
      (FinalSlowBase.coefficients H v) 0 j) (0,eta) =
      (1/2 : ℝ) * SimilarityProfile.partialX (SlowBorelBase.bundleComponent W.axis.normalization
        (FinalSlowBase.coefficients H v) 5 j) (0,eta) := by
  exact bundle_average_derivative_at_axis W.axis.normalization _
    (FinalSlowBase.coefficients_smooth H v) j eta

theorem slowSum_axis_proportional
    {a : ℕ → ℕ} (ha : StrictMono a) (h q eta c : ℝ) (hq : 0 < q)
    (f g : ℕ → SlowBorelBase.Inner → ℝ)
    (he : ∀ j, f j (0,eta) = c * g j (0,eta)) :
    SlowBorelBase.slowSum a h f (q,(0,eta)) =
      c * SlowBorelBase.slowSum a h g (q,(0,eta)) := by
  obtain ⟨N, hN⟩ := SlowBorelBase.slowSum_finite_at_scale ha h hq
  rw [hN f, hN g]
  simp_rw [he]
  rw [mul_add, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro j hj
  ring

theorem averaged_derivative_slowSum_at_axis
    {a : ℕ → ℕ} (ha : StrictMono a) (h q eta C : ℝ) (hq : 0 < q)
    (d : SlowBorelBase.Coefficients) (hd : SlowBorelBase.SmoothCoefficients d) :
    SlowBorelBase.slowSum a h
      (fun j => SimilarityProfile.partialX (SlowBorelBase.bundleComponent C d 0 j)) (q,(0,eta)) =
      (1/2 : ℝ) * SlowBorelBase.slowSum a h
        (fun j => SimilarityProfile.partialX (SlowBorelBase.bundleComponent C d 5 j)) (q,(0,eta)) := by
  exact slowSum_axis_proportional ha h q eta (1/2) hq _ _
    (fun j => bundle_average_derivative_at_axis C d hd j eta)

theorem selected_averaged_derivative_sum_tends_natural
    {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W)
    {ld : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness ld) (upper eta : ℝ) (B : ℕ)
    (heta : eta ∈ Set.Icc (-1 : ℝ) 1) :
    Filter.Tendsto (fun q : ℝ => SlowBorelBase.slowSum
      (FinalSlowBase.scales H v upper B) F.data.h
      (fun j => SimilarityProfile.partialX (SlowBorelBase.bundleComponent W.axis.normalization
        (FinalSlowBase.coefficients H v) 0 j)) (q,(0,eta)))
      (𝓝[>] (0 : ℝ))
      (𝓝 ((1/2 : ℝ) * deriv (fun X => W.axis.natural.profile.family.U (X,eta)) 0)) := by
  have limit := (selected_axial_radial_derivative_tends_natural H v upper eta B
    W.axis.small.h_pos heta).const_mul (1/2 : ℝ)
  apply limit.congr'
  filter_upwards [self_mem_nhdsWithin] with q hq
  have ha := (FinalSlowBase.scales_admissible H v upper B).strictMono
  have hd := FinalSlowBase.coefficients_smooth H v
  rw [(SlowBorelBase.hasDerivAt_slowSum_X ha F.data.h
    (SlowBorelBase.bundleComponent_smooth hd W.axis.normalization (5 : Fin 7)) hq 0 eta).deriv]
  exact (averaged_derivative_slowSum_at_axis ha F.data.h q eta W.axis.normalization hq
    (FinalSlowBase.coefficients H v) hd).symm

#print axioms selected_averaged_derivative_sum_tends_natural
#print axioms slowSum_axis_proportional
#print axioms averaged_derivative_slowSum_at_axis
#print axioms bundle_average_derivative_at_axis
#print axioms selected_bundle_average_derivative_at_axis
#print axioms average_radial_derivative_at_axis
#print axioms radial_derivative_compact_integral
#print axioms selected_stream_radial_derivative_physical
#print axioms selected_base_velocity_laplacian_on_axis
#print axioms selected_base_velocity_slice_eq
#print axioms curl_velocity_eq_profile_velocity
#print axioms selected_profile_velocity_laplacian_on_axis
#print axioms selected_transverse_profiles_sliceC2
#print axioms selected_stream_axial_velocity_sliceC2
#print axioms selected_stream_sliceC2
#print axioms physical_stream_laplacian_of_sliceC2
#print axioms physical_stream_laplacian_on_axis
#print axioms stream_axial_second_derivative_on_axis
#print axioms axial_slice_derivative_eq_partialZ
#print axioms axial_second_derivative_eq_slice
#print axioms stream_axial_radial_derivative_on_axis
#print axioms physical_axial_laplacian_on_axis
#print axioms prepared_root_with_negative_radial_derivative
#print axioms exists_selected_root_with_negative_radial_derivative
#print axioms selected_axial_radial_derivative_eventually_negative
#print axioms selected_natural_derivative_negative
#print axioms original_axis_derivative_eq_natural
#print axioms selected_axial_radial_derivative_tends_natural
#print axioms modulated_axis_derivative_eq_original
#print axioms selected_axial_radial_derivative_tends_original
#print axioms selected_axial_radial_derivative_tends_modulated
#print axioms deriv_eq_of_nonnegative_agreement
#print axioms selected_leading_derivative_eq_modulated
#print axioms selected_axial_radial_derivative_tends_leading
#print axioms axial_radial_derivative_tends_leading
#print axioms axial_radial_tail_tends_zero
#print axioms radial_derivative_limit_of_first_jet
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
