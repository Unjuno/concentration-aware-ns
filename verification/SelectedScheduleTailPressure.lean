import NavierStokes.SchedulePressure
import NavierStokes.FuturePressureBounds
import NavierStokes.OutgoingPulseBounds

/-!
# The zero-exponent tail of the selected schedule

After the flattening endpoint, the pressure kernel is identically one. This
isolated source-bound lemma records eta-independence, an endpoint-weight
envelope, and a conditional pulse-amplitude bound for the tail contribution.
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

/-- At the flattening endpoint, the clock weight is the decayed pulse amplitude
    squared, with the factor 1/4 from the axial normalization. -/
theorem clockWeight_flattenEnd_eq (d : OutgoingTail.TailData) :
    SchedulePressure.clockWeight d d.flattenEnd =
      (OutgoingSchedule.pulseAmplitude d.core ^ 2 / 4) *
        Real.exp (-(1 + 2 * d.core.lam) *
          (d.core.pulseLength + OutgoingTail.flattenLength)) := by
  have hstart : d.core.pulseStart ≤ d.flattenEnd := by
    dsimp [OutgoingTail.TailData.flattenEnd, OutgoingSchedule.Parameters.endpoint]
    linarith [d.core.pulseLength_pos, OutgoingTail.flattenLength_pos]
  have hrad := OutgoingSchedule.radialAmplitude_hold
    d.core.dropLength_pos.le d.core.pulseStart_ge_hold hstart
    (P := d.core.P) (lam := d.core.lam)
  have hdiff : d.flattenEnd - d.core.pulseStart =
      d.core.pulseLength + OutgoingTail.flattenLength := by
    dsimp [OutgoingTail.TailData.flattenEnd, OutgoingSchedule.Parameters.endpoint]
    ring
  rw [SchedulePressure.clockWeight,
    OutgoingTail.finalAngular_uniform_wait d 0 le_rfl
      (le_of_lt (OutgoingTail.releaseStart_gt_flattenEnd d)), hrad,
    OutgoingSchedule.pulseAmplitude, hdiff]
  have hexp : Real.exp (-(1 / 2 + d.core.lam) *
      (d.core.pulseLength + OutgoingTail.flattenLength)) ^ 2 =
      Real.exp (-(1 + 2 * d.core.lam) *
        (d.core.pulseLength + OutgoingTail.flattenLength)) := by
    rw [pow_two, ← Real.exp_add]
    congr 1; ring
  calc
    _ = OutgoingSchedule.radialAmplitude d.core.P d.core.dropLength d.core.lam
          d.core.pulseStart ^ 2 *
        Real.exp (-(1 / 2 + d.core.lam) *
          (d.core.pulseLength + OutgoingTail.flattenLength)) ^ 2 / 4 := by ring
    _ = _ := by rw [hexp]; ring

/-- With the source's exact logarithmic wait, the endpoint tail bound can be
    written as a multiple of the core amplitude squared. -/
theorem tail_pressure_lower_bound_from_pulse_decay (d : OutgoingTail.TailData)
    (hwait : d.core.wait = 60 * Real.log (1 / d.core.lam)) :
    -((5 / 32 : ℝ) * Real.exp (6 / 5) *
        (d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 *
        Real.exp (-(1 + 2 * d.core.lam) *
          (d.core.pulseLength + OutgoingTail.flattenLength))) ≤
      tailPressureContribution d := by
  have hamp := OutgoingPulseBounds.pulseAmplitude_small d.core hwait
  have hapos := OutgoingSchedule.pulseAmplitude_pos d.core
  have hbpos : 0 < d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30 := by
    exact mul_pos (mul_pos d.core.P_pos (Real.exp_pos _))
      (pow_pos d.core.lam_pos _)
  have hs1 := mul_le_mul_of_nonneg_left hamp hapos.le
  have hs2 := mul_le_mul_of_nonneg_right hamp hbpos.le
  have hsquare : OutgoingSchedule.pulseAmplitude d.core ^ 2 ≤
      (d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 := by
    nlinarith
  have hdiv : OutgoingSchedule.pulseAmplitude d.core ^ 2 / 4 ≤
      (d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 / 4 :=
    div_le_div_of_nonneg_right hsquare (by norm_num)
  have hclock : SchedulePressure.clockWeight d d.flattenEnd ≤
      ((d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 / 4) *
        Real.exp (-(1 + 2 * d.core.lam) *
          (d.core.pulseLength + OutgoingTail.flattenLength)) := by
    rw [clockWeight_flattenEnd_eq]
    exact mul_le_mul_of_nonneg_right hdiv (Real.exp_pos _).le
  have hcoef : 0 ≤ (5 / 8 : ℝ) * Real.exp (6 / 5) := by positivity
  have hneg := neg_le_neg (mul_le_mul_of_nonneg_left hclock hcoef)
  calc
    _ = -(((5 / 8 : ℝ) * Real.exp (6 / 5)) *
        (((d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 / 4) *
          Real.exp (-(1 + 2 * d.core.lam) *
            (d.core.pulseLength + OutgoingTail.flattenLength)))) := by ring
    _ ≤ -(((5 / 8 : ℝ) * Real.exp (6 / 5)) *
        SchedulePressure.clockWeight d d.flattenEnd) := hneg
    _ ≤ tailPressureContribution d := tail_pressure_lower_bound d

#print axioms tail_integrand_constant
#print axioms tail_pressure_independent_of_eta
#print axioms tail_pressure_lower_bound
#print axioms tail_pressure_nonpos
#print axioms clockWeight_flattenEnd_eq
#print axioms tail_pressure_lower_bound_from_pulse_decay

end ConcentrationAwareSelectedScheduleTail
