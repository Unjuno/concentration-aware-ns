import Mathlib

open Set Filter MeasureTheory
open scoped Topology

noncomputable section

namespace PacketProbability

/-- For a finite measure and a measurable nonnegative scalar observable, the
measure of shrinking strict sublevel sets tends to the mass of its zero set.
The reciprocal cutoff is reparameterized by `t → ∞` to use continuity from
above for measures. In the axis-packet application, `c` is the absolute axial
component of a unit direction, and `c = 0` is the exactly transverse set. -/
theorem sublevel_measure_tendsto_zero_atTop
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsFiniteMeasure μ]
    (c : Ω → ℝ) (hc : Measurable c) (hc_nonneg : ∀ x, 0 ≤ c x)
    (hzero : μ {x | c x = 0} = 0) :
    Tendsto (fun t : ℝ => μ {x | c x < (1 : ℝ) / max t 1}) atTop (𝓝 0) := by
  let A : ℝ → Set Ω := fun t => {x | c x < (1 : ℝ) / max t 1}
  have hanti : Antitone A := by
    intro t u htu x hx
    change c x < (1 : ℝ) / max u 1 at hx
    change c x < (1 : ℝ) / max t 1
    apply lt_of_lt_of_le hx
    apply one_div_le_one_div_of_le
    · exact lt_of_lt_of_le zero_lt_one (le_max_right t 1)
    · exact max_le_max htu le_rfl
  have hmeas (t : ℝ) : MeasurableSet (A t) := by
    dsimp [A]
    exact measurableSet_Iio.preimage hc
  have hinter : (⋂ t : ℝ, A t) = {x | c x = 0} := by
    ext x
    simp only [mem_iInter, Set.mem_ofPred_eq]
    constructor
    · intro hx
      have hle : c x ≤ 0 := by
        by_contra hnot
        have hpos : 0 < c x := lt_of_not_ge hnot
        obtain ⟨n, hn⟩ := exists_nat_gt (1 / c x)
        have hn' : (1 / c x) < (n : ℝ) + 1 := by
          exact lt_trans hn (by linarith)
        have hmul : 1 < c x * ((n : ℝ) + 1) := by
          have hmul' := mul_lt_mul_of_pos_left hn' hpos
          have hrecip : c x * (1 / c x) = 1 := by field_simp
          rw [hrecip] at hmul'
          linarith
        have hthreshold : (1 : ℝ) / ((n : ℝ) + 1) < c x := by
          apply (div_lt_iff₀ (by positivity : (0 : ℝ) < (n : ℝ) + 1)).2
          linarith
        have ht1 : 1 ≤ (n : ℝ) + 1 := by
          exact_mod_cast Nat.succ_le_succ (Nat.zero_le n)
        have hx_n : c x < (1 : ℝ) / max ((n : ℝ) + 1) 1 := by
          simpa [A] using hx ((n : ℝ) + 1)
        rw [max_eq_left ht1] at hx_n
        exact (not_lt_of_ge hthreshold.le) hx_n
      exact le_antisymm hle (hc_nonneg x)
    · intro hx t
      dsimp [A]
      rw [hx]
      positivity
  have hfinite : ∃ t, μ (A t) ≠ ⊤ := by
    refine ⟨0, ?_⟩
    exact measure_ne_top μ (A 0)
  have hlim := tendsto_measure_iInter_atTop (s := A)
    (fun t => (hmeas t).nullMeasurableSet) hanti hfinite
  rw [hinter, hzero] at hlim
  simpa [A, Function.comp_def] using hlim

end PacketProbability
