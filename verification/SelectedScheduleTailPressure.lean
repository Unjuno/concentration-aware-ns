import NavierStokes.SchedulePressure
import NavierStokes.FuturePressureBounds

/-!
# The zero-exponent tail of the selected schedule

After the flattening endpoint, the pressure kernel is identically one. This
isolated source-bound lemma records the eta-independent tail contribution; it
does not bound its magnitude relative to the core amplitude.
-/

namespace ConcentrationAwareSelectedScheduleTail

open MeasureTheory Set
open NavierStokes

noncomputable def tailPressureContribution (d : OutgoingTail.TailData) : ℝ :=
  -(1 / 2 : ℝ) * ∫ y in Ici d.flattenEnd, SchedulePressure.clockWeight d y

theorem tail_integrand_constant (d : OutgoingTail.TailData) {y eta : ℝ}
    (hy : d.flattenEnd ≤ y) :
    SchedulePressure.clockWeight d y *
        PressureDatum.kernel (SchedulePressure.shapeExponent d y) eta =
      SchedulePressure.clockWeight d y := by
  rw [SchedulePressure.shapeExponent_after d hy]
  simp [PressureDatum.kernel]

theorem tail_pressure_independent_of_eta (d : OutgoingTail.TailData) (eta : ℝ) :
    -(1 / 2 : ℝ) *
        ∫ y in Ici d.flattenEnd,
          SchedulePressure.clockWeight d y *
            PressureDatum.kernel (SchedulePressure.shapeExponent d y) eta =
      tailPressureContribution d := by
  unfold tailPressureContribution
  congr 1
  apply setIntegral_congr_fun measurableSet_Ici
  intro y hy
  exact tail_integrand_constant d hy

/-- The actual schedule tail has a parameter-uniform exponential-envelope bound
    in terms of the clock weight at the flattening endpoint. -/
theorem tail_pressure_lower_bound (d : OutgoingTail.TailData) :
    -((5 / 8 : ℝ) * Real.exp (6 / 5) *
        SchedulePressure.clockWeight d d.flattenEnd) ≤
      tailPressureContribution d := by
  have hflat : 0 ≤ d.flattenEnd := by
    linarith [d.core.holdStart_pos,
      OutgoingTail.coreEndpoint_ge_hold d,
      OutgoingTail.flattenEnd_gt_core d]
  have hfuture := NavierStokes.FuturePressureBounds.future_clock_integral_le d hflat
  rw [tailPressureContribution, integral_Ici_eq_integral_Ioi]
  nlinarith

/-- The eta-independent tail is nonpositive, so the preceding estimate bounds
    its magnitude by its endpoint clock weight. -/
theorem tail_pressure_nonpos (d : OutgoingTail.TailData) :
    tailPressureContribution d ≤ 0 := by
  have hnonneg : 0 ≤ ∫ y in Ioi d.flattenEnd, SchedulePressure.clockWeight d y :=
    setIntegral_nonneg measurableSet_Ioi (fun y _ =>
      (SchedulePressure.clockWeight_pos d y).le)
  rw [tailPressureContribution, integral_Ici_eq_integral_Ioi]
  nlinarith

#print axioms tail_integrand_constant
#print axioms tail_pressure_independent_of_eta
#print axioms tail_pressure_lower_bound
#print axioms tail_pressure_nonpos

end ConcentrationAwareSelectedScheduleTail
