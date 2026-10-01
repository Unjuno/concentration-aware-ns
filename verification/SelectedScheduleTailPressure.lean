import NavierStokes.SchedulePressure
import NavierStokes.FuturePressureBounds
import NavierStokes.OutgoingPulseBounds
import NavierStokes.OutgoingCone
import NavierStokes.PreparedOutgoing
import NavierStokes.FinalSlowBase

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

noncomputable def tailRelativeCoefficient (d : OutgoingTail.TailData) : ℝ :=
  (5 / 32 : ℝ) * d.core.lam ^ 60 *
    Real.exp (2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
      (1 + 2 * d.core.lam) * OutgoingTail.flattenLength)

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

/-- The explicit `P^2` coefficient is uniformly small under the exponential
    lambda cap used internally by the source's tail-threshold construction. -/
theorem tail_relative_coefficient_small (d : OutgoingTail.TailData)
    (hcap : d.core.lam ≤
      Real.exp (-(Real.exp d.core.m + 12 + 3 / 5)) / 4) :
    (5 / 32 : ℝ) * d.core.lam ^ 60 *
      Real.exp (2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength) ≤ 1 / 100 := by
  let X : ℝ := Real.exp d.core.m + 12 + 3 / 5
  have hX : d.core.m ≤ X := by
    dsimp [X]
    have h := Real.add_one_le_exp d.core.m
    linarith
  have hexpXpos : 0 < Real.exp X := Real.exp_pos _
  have hexpCancel : Real.exp (-X) * Real.exp X = 1 := by
    rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]
  have hprod : d.core.lam * Real.exp X ≤ 1 / 4 := by
    have h := mul_le_mul_of_nonneg_right hcap hexpXpos.le
    calc
      d.core.lam * Real.exp X ≤ Real.exp (-X) / 4 * Real.exp X := h
      _ = 1 / 4 := by
        calc
          _ = (Real.exp (-X) * Real.exp X) / 4 := by ring
          _ = _ := by rw [hexpCancel]
  have hinv : 4 * Real.exp X ≤ 1 / d.core.lam :=
    (le_div_iff₀ d.core.lam_pos).2 (by nlinarith [hprod])
  have hreciprocal : 52 * Real.exp X ≤ 13 / d.core.lam := by
    have h := mul_le_mul_of_nonneg_left hinv (by norm_num : (0 : ℝ) ≤ 13)
    calc
      52 * Real.exp X = 13 * (4 * Real.exp X) := by ring
      _ ≤ 13 * (1 / d.core.lam) := h
      _ = 13 / d.core.lam := by ring
  have hexpMonotone : Real.exp d.core.m ≤ Real.exp X := Real.exp_le_exp.mpr hX
  have hreciprocal' : 52 * Real.exp d.core.m ≤ 13 / d.core.lam :=
    (mul_le_mul_of_nonneg_left hexpMonotone (by norm_num : (0 : ℝ) ≤ 52)).trans
      hreciprocal
  have hdecay : 0 ≤ (1 + 2 * d.core.lam) * OutgoingTail.flattenLength := by
    exact mul_nonneg (by nlinarith [d.core.lam_pos]) OutgoingTail.flattenLength_pos.le
  have hexponent :
      2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength ≤ -50 := by
    have hmexp : 1 ≤ Real.exp d.core.m := by
      have h := Real.add_one_le_exp d.core.m
      linarith [d.core.m_pos]
    nlinarith [hreciprocal', hdecay]
  have hpow : d.core.lam ^ 60 ≤ 1 :=
    pow_le_one₀ d.core.lam_pos.le (by linarith [d.core.lam_lt])
  have hexpBound : Real.exp (
      2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength) ≤ Real.exp (-50) :=
    Real.exp_le_exp.mpr hexponent
  have hexp50 : 51 ≤ Real.exp (50 : ℝ) := by
    have h := Real.add_one_le_exp (50 : ℝ)
    norm_num at h ⊢
    exact h
  have hexpNeg50 : Real.exp (-50 : ℝ) ≤ 1 / 51 := by
    rw [Real.exp_neg]
    simpa only [one_div] using one_div_le_one_div_of_le (by norm_num) hexp50
  have hproduct := mul_le_mul hpow hexpBound (Real.exp_pos _).le (by norm_num)
  have hscaled : (5 / 32 : ℝ) * d.core.lam ^ 60 *
      Real.exp (2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength) ≤
      (5 / 32 : ℝ) * Real.exp (-50 : ℝ) := by
    calc
      _ = (5 / 32 : ℝ) *
          (d.core.lam ^ 60 * Real.exp (2 * Real.exp d.core.m - 4 / 5 -
            13 / d.core.lam - (1 + 2 * d.core.lam) * OutgoingTail.flattenLength)) := by ring
      _ ≤ (5 / 32 : ℝ) * (1 * Real.exp (-50 : ℝ)) :=
        mul_le_mul_of_nonneg_left hproduct (by norm_num)
      _ = _ := by ring
  calc
    _ ≤ (5 / 32 : ℝ) * (1 / 51) :=
      le_trans hscaled (mul_le_mul_of_nonneg_left hexpNeg50 (by norm_num))
    _ ≤ 1 / 100 := by norm_num

/-- The profile-cone conclusion of the pinned ordered selector, factored so its
    lambda threshold can be explicitly capped without weakening that result. -/
def OrderedProfileConeProperty (P m K lam0 : ℝ) : Prop :=
  ∀ F : OutgoingProfile.Profile,
    F.data.core.P = P → F.data.core.m = m → F.coefficientBound = K →
    F.data.core.wait = 60 * Real.log (1 / F.data.core.lam) →
    F.data.core.lam < lam0 →
    F.data.h ≤ OutgoingCone.heightThreshold m F.data.core.lam →
    ∀ left : ℝ, left ≤ 0 →
      ∃ XR0 : ℝ, 0 < XR0 ∧ ∀ XR : ℝ, XR0 < XR →
        OutgoingCone.ProfileCleanCone F XR left

/-- A valid ordered profile-cone threshold can always be reduced to the
    exponential cap used inside the source's tail-smallness construction. -/
theorem exists_ordered_profile_cone_rate_capped :
    ∃ M : ℝ, 0 < M ∧ ∀ m : ℝ, M ≤ m → ∀ P : ℝ,
      OutgoingEntranceCone.amplitudeThreshold m ≤ P → ∀ K : ℝ, 0 < K →
      ∃ lam0 : ℝ, 0 < lam0 ∧
        lam0 ≤ Real.exp (-(Real.exp m + 12 + 3 / 5)) / 4 ∧
        OrderedProfileConeProperty P m K lam0 := by
  obtain ⟨M, hM, H⟩ := OutgoingCone.exists_ordered_profile_cone
  refine ⟨M, hM, ?_⟩
  intro m hm P hP K hK
  obtain ⟨lam0, hlam0, Hlam⟩ := H m hm P hP K hK
  let incoming : ℝ := Real.exp (-(Real.exp m + 12 + 3 / 5)) / 4
  have hincoming : 0 < incoming := by
    dsimp [incoming]
    positivity
  refine ⟨min lam0 incoming, lt_min hlam0 hincoming, min_le_right _ _, ?_⟩
  intro F hFP hFm hFK hwait hlam hh left hleft
  exact Hlam F hFP hFm hFK hwait
    (lt_of_lt_of_le hlam (min_le_left _ _)) hh left hleft

/-- Prepared outgoing data plus the exact wait and lambda-cap witnesses that
    the upstream prepared-profile record currently omits. -/
structure RateCappedPreparedProfile where
  prepared : PreparedOutgoing.PreparedProfile
  wait_identity : prepared.profile.data.core.wait =
    60 * Real.log (1 / prepared.profile.data.core.lam)
  lambda_cap : prepared.profile.data.core.lam ≤
    Real.exp (-(Real.exp prepared.profile.data.core.m + 12 + 3 / 5)) / 4

/-- Re-run the upstream prepared-profile selection with a threshold reduced to
    the source's incoming cap, retaining that cap alongside the same profile. -/
theorem exists_rate_capped_prepared_profile :
    Nonempty RateCappedPreparedProfile := by
  classical
  obtain ⟨M, hM, hcone⟩ := exists_ordered_profile_cone_rate_capped
  let P : ℝ := max 2 (OutgoingEntranceCone.amplitudeThreshold M)
  have hP2 : 2 ≤ P := le_max_left _ _
  have hPpos : 0 < P := lt_of_lt_of_le (by norm_num) hP2
  have hPamp : OutgoingEntranceCone.amplitudeThreshold M ≤ P := le_max_right _ _
  let caps := hcone M le_rfl P hPamp
  let cap : ℝ → ℝ := fun K =>
    if hK : 0 < K then Classical.choose (caps K hK) else 1
  have hcap : ∀ K : ℝ, 0 < K → 0 < cap K := by
    intro K hK
    dsimp only [cap]
    rw [dite_eq_left hK]
    exact (Classical.choose_spec (caps K hK)).1
  have hcapRate : ∀ K : ℝ, 0 < K → cap K ≤
      Real.exp (-(Real.exp M + 12 + 3 / 5)) / 4 := by
    intro K hK
    dsimp only [cap]
    rw [dite_eq_left hK]
    exact (Classical.choose_spec (caps K hK)).2.1
  obtain ⟨K, B, H, core, hK, hB, hH, hcP, hcm, hwait, hlam, _hsmall,
      _h2H, hheight, hHsmall, hfamily⟩ :=
    ScheduledProfileChoice.exists_scheduled_family_below P M hPpos hM cap hcap
      (fun core => OutgoingCone.heightThreshold M core.lam)
      (fun core => OutgoingCone.heightThreshold_pos M core.lam_pos)
  obtain ⟨F, hcore, hh, hFK, hschedule, hspec, hterminal⟩ := hfamily H hH le_rfl
  have hFP : F.data.core.P = P := by rw [hcore, hcP]
  have hFm : F.data.core.m = M := by rw [hcore, hcm]
  have hFwait : F.data.core.wait = 60 * Real.log (1 / F.data.core.lam) := by
    rw [hcore]
    exact hwait
  have hFlam : F.data.core.lam < Classical.choose (caps K hK) := by
    rw [hcore]
    simpa only [cap, dite_eq_left hK] using hlam
  have hFheight : F.data.h ≤ OutgoingCone.heightThreshold M F.data.core.lam := by
    rw [hh, hcore]
    exact hheight
  have hclean := (Classical.choose_spec (caps K hK)).2.2 F hFP hFm hFK hFwait hFlam hFheight
  have hrateK : Classical.choose (caps K hK) ≤
      Real.exp (-(Real.exp M + 12 + 3 / 5)) / 4 := by
    simpa only [cap, dite_eq_left hK] using hcapRate K hK
  let prepared : PreparedOutgoing.PreparedProfile := {
    profile := F
    bound := B
    bound_pos := hB
    specification := hspec
    schedule := hschedule
    terminal := hterminal
    amplitude_lower := by rw [hFP]; exact hP2
    height_upper := by rw [hh]; exact hHsmall
    clean := hclean }
  have hFcap : F.data.core.lam ≤
      Real.exp (-(Real.exp F.data.core.m + 12 + 3 / 5)) / 4 := by
    calc
      F.data.core.lam ≤ Classical.choose (caps K hK) := hFlam.le
      _ ≤ Real.exp (-(Real.exp M + 12 + 3 / 5)) / 4 := hrateK
      _ = Real.exp (-(Real.exp F.data.core.m + 12 + 3 / 5)) / 4 := by rw [hFm]
  exact ⟨⟨prepared, hFwait, hFcap⟩⟩

theorem pulse_decay_coefficient_eq (d : OutgoingTail.TailData) :
    (5 / 32 : ℝ) * Real.exp (6 / 5) *
        (d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 *
        Real.exp (-(1 + 2 * d.core.lam) *
          (d.core.pulseLength + OutgoingTail.flattenLength)) =
      d.core.P ^ 2 * tailRelativeCoefficient d := by
  have hExpSquare : Real.exp (Real.exp d.core.m + 12) ^ 2 =
      Real.exp (2 * Real.exp d.core.m + 24) := by
    rw [pow_two, ← Real.exp_add]
    congr 1; ring
  have hLamSquare : (d.core.lam ^ 30) ^ 2 = d.core.lam ^ 60 := by
    calc
      (d.core.lam ^ 30) ^ 2 = d.core.lam ^ (30 * 2) := by rw [← pow_mul]
      _ = d.core.lam ^ 60 := by norm_num
  have hDecay : -(1 + 2 * d.core.lam) *
      (d.core.pulseLength + OutgoingTail.flattenLength) =
      -13 / d.core.lam - 26 -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength := by
    dsimp [OutgoingSchedule.Parameters.pulseLength]
    field_simp [d.core.lam_pos.ne']
    ring
  have hExpCombine : Real.exp (6 / 5) *
      Real.exp (2 * Real.exp d.core.m + 24) *
      Real.exp (-13 / d.core.lam - 26 -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength) =
      Real.exp (2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
        (1 + 2 * d.core.lam) * OutgoingTail.flattenLength) := by
    rw [← Real.exp_add, ← Real.exp_add]
    congr 1; ring
  rw [tailRelativeCoefficient]
  rw [show (d.core.P * Real.exp (Real.exp d.core.m + 12) * d.core.lam ^ 30) ^ 2 =
      d.core.P ^ 2 * Real.exp (Real.exp d.core.m + 12) ^ 2 *
        (d.core.lam ^ 30) ^ 2 by ring]
  rw [hExpSquare, hLamSquare, hDecay]
  calc
    _ = d.core.P ^ 2 * ((5 / 32 : ℝ) * d.core.lam ^ 60 *
        (Real.exp (6 / 5) * Real.exp (2 * Real.exp d.core.m + 24) *
          Real.exp (-13 / d.core.lam - 26 -
            (1 + 2 * d.core.lam) * OutgoingTail.flattenLength))) := by ring
    _ = d.core.P ^ 2 * ((5 / 32 : ℝ) * d.core.lam ^ 60 *
        Real.exp (2 * Real.exp d.core.m - 4 / 5 - 13 / d.core.lam -
          (1 + 2 * d.core.lam) * OutgoingTail.flattenLength)) := by rw [hExpCombine]
    _ = _ := by ring

theorem tail_pressure_lower_bound_small (d : OutgoingTail.TailData)
    (hwait : d.core.wait = 60 * Real.log (1 / d.core.lam))
    (hcap : d.core.lam ≤
      Real.exp (-(Real.exp d.core.m + 12 + 3 / 5)) / 4) :
    -(d.core.P ^ 2 / 100) ≤ tailPressureContribution d := by
  have hbound := tail_pressure_lower_bound_from_pulse_decay d hwait
  rw [pulse_decay_coefficient_eq] at hbound
  have hsmall := tail_relative_coefficient_small d hcap
  have hP2 : 0 ≤ d.core.P ^ 2 := sq_nonneg _
  have hmul := mul_le_mul_of_nonneg_left hsmall hP2
  have hneg := neg_le_neg hmul
  calc
    -(d.core.P ^ 2 / 100) = -(d.core.P ^ 2 * (1 / 100 : ℝ)) := by ring
    _ ≤ -(d.core.P ^ 2 * tailRelativeCoefficient d) := hneg
    _ ≤ tailPressureContribution d := hbound

theorem rate_capped_prepared_tail_pressure_small
    (d : RateCappedPreparedProfile) :
    -(d.prepared.profile.data.core.P ^ 2 / 100) ≤
      tailPressureContribution d.prepared.profile.data :=
  tail_pressure_lower_bound_small d.prepared.profile.data
    d.wait_identity d.lambda_cap

/-- A rate-capped prepared profile can be carried through the pinned nominal
    cone and finite-modulation constructions into the full source ProfileData
    record, while retaining an equality back to the prepared outgoing profile. -/
structure RateCappedProfileData where
  capped : RateCappedPreparedProfile
  data : FinalSlowBase.ProfileData
  outgoing_eq : data.outgoing = capped.prepared.profile

/-- The capped selector is compatible with all later pinned constructions;
    the resulting existential record still does not identify
    `FinalSlowBase.actualProfile`, which is selected independently below. -/
theorem exists_rate_capped_profile_data : Nonempty RateCappedProfileData := by
  classical
  obtain ⟨capped⟩ := exists_rate_capped_prepared_profile
  obtain ⟨nominal, hnominal⟩ :=
    NominalConeAssembly.exists_certificate capped.prepared
  obtain ⟨loop, modulation, hcone⟩ :=
    ModulatedProfileAssembly.exists_of_certificate nominal hnominal
  let data : FinalSlowBase.ProfileData := {
    outgoing := capped.prepared.profile
    nominal := nominal
    certificate := hnominal
    loop := loop
    modulation := modulation
    fullTrueCone := hcone }
  exact ⟨⟨capped, data, rfl⟩⟩

theorem rate_capped_profile_data_tail_pressure_small
    (d : RateCappedProfileData) :
    -(d.data.outgoing.data.core.P ^ 2 / 100) ≤
      tailPressureContribution d.data.outgoing.data := by
  rw [d.outgoing_eq]
  exact rate_capped_prepared_tail_pressure_small d.capped

/-- The same conditional tail estimate bounds the positive clock-weight mass
    after flattening by P^2/50. This remains a statement about the existential
    rate-capped profile, not the independently selected actualProfile. -/
theorem rate_capped_profile_data_tail_mass_upper_bound
    (d : RateCappedProfileData) :
    (∫ y in Ici d.data.outgoing.data.flattenEnd,
      SchedulePressure.clockWeight d.data.outgoing.data y) ≤
      d.data.outgoing.data.core.P ^ 2 / 50 := by
  have hpressure := rate_capped_profile_data_tail_pressure_small d
  have hmass : 0 ≤ ∫ y in Ici d.data.outgoing.data.flattenEnd,
      SchedulePressure.clockWeight d.data.outgoing.data y :=
    setIntegral_nonneg measurableSet_Ici (fun y _ =>
      (SchedulePressure.clockWeight_pos d.data.outgoing.data y).le)
  unfold tailPressureContribution at hpressure
  nlinarith

#print axioms tail_integrand_constant
#print axioms tail_pressure_independent_of_eta
#print axioms tail_pressure_lower_bound
#print axioms tail_pressure_nonpos
#print axioms clockWeight_flattenEnd_eq
#print axioms tail_pressure_lower_bound_from_pulse_decay
#print axioms tail_relative_coefficient_small
#print axioms exists_ordered_profile_cone_rate_capped
#print axioms pulse_decay_coefficient_eq
#print axioms tail_pressure_lower_bound_small
#print axioms rate_capped_prepared_tail_pressure_small
#print axioms exists_rate_capped_prepared_profile
#print axioms exists_rate_capped_profile_data
#print axioms rate_capped_profile_data_tail_pressure_small
#print axioms rate_capped_profile_data_tail_mass_upper_bound

end ConcentrationAwareSelectedScheduleTail
