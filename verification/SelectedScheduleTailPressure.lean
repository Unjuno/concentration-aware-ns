import NavierStokes.SchedulePressure

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

#print axioms tail_integrand_constant
#print axioms tail_pressure_independent_of_eta

end ConcentrationAwareSelectedScheduleTail
