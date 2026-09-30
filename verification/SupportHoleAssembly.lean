import NavierStokes.ActualCandidateAssembly
import NavierStokes.ActualExteriorPrefix
import NavierStokes.AxisPreservation
import NavierStokes.DirectAngularDiagonal
import NavierStokes.MixedPeriodicAssembly
import NavierStokes.SpatialLocalization
import NavierStokes.TimeLocalization

/-!
This extension composes the pinned source's exterior-stage identities with
local finiteness, the zeroth cutoff plateau, curl, and the two outer
localizations. It proves a local base-field equality on the actual open
exterior. This file formalizes the pointwise chart identity, its eta-margin
upper bound, and a fixed-time spatial Lipschitz estimate. It does not prove a
uniform margin over the full moving cusp tube.
-/

noncomputable section

namespace ConcentrationAware

open NavierStokes
open NavierStokes.CorrectionInitialization.ActualPrimary
open Filter Set
open scoped Topology

/-- The implicit similarity equation pulled back to the actual Cartesian
coordinates, with eta left in the source's normalized-coordinate form. -/
theorem physicalQ_time_identity {w : ProblemStatement.SpaceTime}
    (ht : w ∈ PhysicalWaveSum.preterminal) :
    1 - w.1 = PhysicalWaveSum.physicalQ outgoing.data.h w *
      (1 - SimilarityCoordinates.coordinateEta (2 * outgoing.data.h) (1 - w.1, w.2 2) ^ 2) := by
  have hid := SimilarityCoordinates.tau_coordinate_identity
    (mul_pos (by norm_num : (0 : ℝ) < 2) outgoing.data.h_pos)
    (by linarith [outgoing.data.h_lt_half] : 2 * outgoing.data.h < 1)
    (p := (1 - w.1, w.2 2)) (sub_pos.mpr ht)
  simpa [PhysicalWaveSum.physicalQ, AxisymmetricFields.profilePoint,
    SimilarityProfile.q] using hid

/-- A uniform normalized-axial margin gives an upper bound for the physical
similarity scale. -/
theorem physicalQ_le_of_eta_margin {w : ProblemStatement.SpaceTime}
    (ht : w ∈ PhysicalWaveSum.preterminal) {beta : ℝ}
    (hbeta : 0 ≤ beta) (hbeta1 : beta < 1)
    (heta : |SimilarityCoordinates.coordinateEta (2 * outgoing.data.h) (1 - w.1, w.2 2)| ≤ beta) :
    PhysicalWaveSum.physicalQ outgoing.data.h w ≤ (1 - w.1) / (1 - beta ^ 2) := by
  have hq := PhysicalWaveSum.physicalQ_pos outgoing.data.h_pos outgoing.data.h_lt_half ht
  have hid := physicalQ_time_identity ht
  have hetaBounds := abs_le.mp heta
  have hetaSq : SimilarityCoordinates.coordinateEta (2 * outgoing.data.h) (1 - w.1, w.2 2) ^ 2 ≤ beta ^ 2 := by
    nlinarith
  have hden : 0 < 1 - beta ^ 2 := by nlinarith
  rw [hid]
  apply (le_div_iff₀ hden).2
  have hprod : 0 ≤ PhysicalWaveSum.physicalQ outgoing.data.h w *
      (beta ^ 2 - SimilarityCoordinates.coordinateEta (2 * outgoing.data.h) (1 - w.1, w.2 2) ^ 2) :=
    mul_nonneg hq.le (sub_nonneg.mpr hetaSq)
  nlinarith

/-- On a fixed positive-time slice, normalized axial position is Lipschitz in
the physical axial coordinate. The scale loss is exactly the chart power. -/
theorem coordinateEta_lipschitz_z {a tau z z' : ℝ}
    (ha : 0 < a) (ha1 : a < 1) (htau : 0 < tau) :
    |SimilarityCoordinates.coordinateEta a (tau, z) -
      SimilarityCoordinates.coordinateEta a (tau, z')| ≤
      |z - z'| / ((1 - a) * tau ^ ((1 - a) / 2)) := by
  let f : ℝ → ℝ := fun x => SimilarityCoordinates.coordinateEta a (tau, x)
  let f' : ℝ → ℝ := fun x =>
    (1 - SimilarityCoordinates.coordinateEta a (tau, x) ^ 2) /
      (SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
        SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)))
  have hD : 0 < (1 - a) / 2 := by linarith
  have hL : 0 < (1 - a) * tau ^ ((1 - a) / 2) := by positivity
  have hderiv : ∀ x ∈ Set.Icc (min z z') (max z z'), HasDerivWithinAt f (f' x)
      (Set.Icc (min z z') (max z z')) x := by
    intro x _
    exact (SimilarityCoordinates.coordinateEta_hasDerivAt_z ha ha1 htau).hasDerivWithinAt
  have hbound : ∀ x ∈ Set.Icc (min z z') (max z z'), ‖f' x‖ ≤ 1 / ((1 - a) * tau ^ ((1 - a) / 2)) := by
    intro x _
    have hq := SimilarityCoordinates.coordinateQ_spec ha ha1 (p := (tau, x)) htau
    have hetaSq := SimilarityCoordinates.coordinateEta_sq_lt_one ha ha1 (p := (tau, x)) htau
    have hid := SimilarityCoordinates.tau_coordinate_identity ha ha1 (p := (tau, x)) htau
    have hqge : tau ≤ SimilarityCoordinates.coordinateQ a (tau, x) := by
      dsimp [SimilarityCoordinates.forwardScalar] at hid
      nlinarith [sq_nonneg (SimilarityCoordinates.coordinateEta a (tau, x))]
    have hpow : tau ^ ((1 - a) / 2) ≤
        SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) :=
      Real.rpow_le_rpow htau.le hqge hD.le
    have hslope := SimilarityCoordinates.scalarSlope_eq_L ha ha1 (p := (tau, x)) htau
    have hslopeBound : 1 - a ≤
        SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)) := by
      rw [hslope]
      nlinarith
    have hden : (1 - a) * tau ^ ((1 - a) / 2) ≤
        SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
          SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)) := by
      calc
        (1 - a) * tau ^ ((1 - a) / 2) ≤ (1 - a) * SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) :=
          mul_le_mul_of_nonneg_left hpow (by linarith)
        _ ≤ SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
          SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)) :=
          by simpa only [mul_comm] using
            (mul_le_mul_of_nonneg_left hslopeBound (Real.rpow_nonneg hq.1.le _))
    have hdenpos : 0 < SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
        SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)) :=
      mul_pos (Real.rpow_pos_of_pos hq.1 _) (by linarith [hslopeBound])
    have hnum0 : 0 ≤ 1 - SimilarityCoordinates.coordinateEta a (tau, x) ^ 2 :=
      by nlinarith
    have hnum1 : 1 - SimilarityCoordinates.coordinateEta a (tau, x) ^ 2 ≤ 1 := by nlinarith
    have hcross : (1 - SimilarityCoordinates.coordinateEta a (tau, x) ^ 2) *
        ((1 - a) * tau ^ ((1 - a) / 2)) ≤
        SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
          SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)) := by
      have hprod := mul_nonneg (sub_nonneg.mpr hnum1) hL.le
      nlinarith
    change ‖(1 - SimilarityCoordinates.coordinateEta a (tau, x) ^ 2) /
      (SimilarityCoordinates.coordinateQ a (tau, x) ^ ((1 - a) / 2) *
        SimilarityCoordinates.scalarSlope a x (SimilarityCoordinates.coordinateQ a (tau, x)))‖ ≤ _
    rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg hnum0 hdenpos.le)]
    exact (div_le_div_iff₀ hdenpos hL).2 (by simpa only [one_mul] using hcross)
  let lo := min z z'
  let hi := max z z'
  have hz : z ∈ Set.Icc lo hi := ⟨min_le_left _ _, le_max_left _ _⟩
  have hz' : z' ∈ Set.Icc lo hi := ⟨min_le_right _ _, le_max_right _ _⟩
  have hmean := norm_image_sub_le_of_norm_deriv_le_segment' hderiv
    (fun x hx => by
      simpa only [Real.norm_eq_abs] using hbound x ⟨hx.1, hx.2.le⟩)
  have hzmean := hmean z hz
  have hz'mean := hmean z' hz'
  have htriangle : ‖f z - f z'‖ ≤ ‖f z - f lo‖ + ‖f z' - f lo‖ := by
    calc
      ‖f z - f z'‖ = ‖(f z - f lo) - (f z' - f lo)‖ := by congr 1; ring
      _ ≤ _ := norm_sub_le _ _
  have hsum : (z - lo) + (z' - lo) = hi - lo := by
    dsimp [lo, hi]
    by_cases h : z ≤ z'
    · rw [min_eq_left h, max_eq_right h]
      ring
    · have h' : z' ≤ z := le_of_not_ge h
      rw [min_eq_right h', max_eq_left h']
      ring
  have hdist : hi - lo = |z - z'| := by
    dsimp [lo, hi]
    by_cases h : z ≤ z'
    · rw [min_eq_left h, max_eq_right h, abs_of_nonpos (sub_nonpos.mpr h)]
      ring
    · have h' : z' ≤ z := le_of_not_ge h
      rw [min_eq_right h', max_eq_left h', abs_of_nonneg (sub_nonneg.mpr h')]
  have hnorm : ‖f z - f z'‖ = |f z - f z'| := Real.norm_eq_abs _
  change ‖f z - f z'‖ ≤ _
  calc
    |f z - f z'| = ‖f z - f z'‖ := by rw [Real.norm_eq_abs]
    _ ≤ ‖f z - f lo‖ + ‖f z' - f lo‖ := htriangle
    _ ≤ (1 / ((1 - a) * tau ^ ((1 - a) / 2))) * ((z - lo) + (z' - lo)) := by
      rw [Real.norm_eq_abs] at hzmean hz'mean
      have hzabs : ‖f z - f lo‖ = |f z - f lo| := Real.norm_eq_abs _
      have hz'abs : ‖f z' - f lo‖ = |f z' - f lo| := Real.norm_eq_abs _
      calc
        ‖f z - f lo‖ + ‖f z' - f lo‖ ≤
            (1 / ((1 - a) * tau ^ ((1 - a) / 2))) * (z - lo) +
              (1 / ((1 - a) * tau ^ ((1 - a) / 2))) * (z' - lo) := by
                rw [hzabs, hz'abs]
                exact add_le_add hzmean hz'mean
        _ = _ := by ring
    _ = |z - z'| / ((1 - a) * tau ^ ((1 - a) / 2)) := by rw [hsum, hdist]; ring

/-- The source-normalized similarity coordinate equals a prescribed value at
its analytic axis center. -/
theorem coordinateEta_axis_center {h tau eta : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (htau : 0 < tau)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1) :
    SimilarityCoordinates.coordinateEta (2*h)
      (tau, eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)) = eta := by
  have hd : 0 < 1 - eta^2 := by nlinarith [heta.1, heta.2]
  let q := tau / (1 - eta^2)
  have hq : 0 < q := div_pos htau hd
  have hpowers : (q ^ (CoordinateAlgebra.D h)) ^ 2 * q ^ (2*h) = q := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hq.le, ← Real.rpow_add hq]
    have he : CoordinateAlgebra.D h * (2 : ℝ) + 2*h = 1 := by
      unfold CoordinateAlgebra.D
      ring
    norm_num only [Nat.cast_ofNat]
    rw [he, Real.rpow_one]
  have hforward : SimilarityCoordinates.forwardScalar (2*h)
      (eta*q^(CoordinateAlgebra.D h)) q = q*(1-eta^2) := by
    unfold SimilarityCoordinates.forwardScalar
    rw [mul_pow]
    nlinarith [hpowers]
  have hQ : SimilarityCoordinates.coordinateQ (2*h) (tau, eta*q^(CoordinateAlgebra.D h)) = q := by
    apply (SimilarityCoordinates.eq_coordinateQ (by positivity) (by linarith)
      htau hq ?_).symm
    rw [hforward]
    dsimp [q]
    field_simp [q]
  rw [show eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h) =
      eta * q ^ (CoordinateAlgebra.D h) by rfl]
  unfold SimilarityCoordinates.coordinateEta
  rw [hQ]
  have hexp : CoordinateAlgebra.D h = (1 - 2*h) / 2 := by
    unfold CoordinateAlgebra.D
    ring
  rw [hexp]
  field_simp [Real.rpow_pos_of_pos hq _]

/-- A pointwise axial-radius condition transfers an axis eta margin to the
whole fixed-time axial interval. This isolates the remaining geometric step:
derive the displayed radius inequality uniformly for the desired tube. -/
theorem coordinateEta_margin_of_axial_radius {h tau eta z δ : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (htau : 0 < tau)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1)
    (hradius : |z - eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)| /
        ((1 - 2*h) * tau ^ ((1 - 2*h) / 2)) ≤ δ) :
    |SimilarityCoordinates.coordinateEta (2*h) (tau,z)| ≤ |eta| + δ := by
  have ha : 0 < 2*h := by linarith
  have ha1 : 2*h < 1 := by linarith
  have hcenter := coordinateEta_axis_center hh hh1 htau heta
  have hdiff := coordinateEta_lipschitz_z ha ha1 htau
    (z := z) (z' := eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h))
  have hden : (1 - 2*h) / 2 = (1 - (2*h)) / 2 := by ring
  have hscale : (1 - 2*h) * tau ^ ((1 - 2*h) / 2) =
      (1 - 2*h) * tau ^ ((1 - (2*h)) / 2) := by rw [hden]
  rw [hcenter] at hdiff
  have hstep : |SimilarityCoordinates.coordinateEta (2*h) (tau,z) - eta| ≤ δ := by
    calc
      |SimilarityCoordinates.coordinateEta (2*h) (tau,z) - eta| ≤
          |z - eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)| /
            ((1 - 2*h) * tau ^ ((1 - 2*h) / 2)) := by
        rw [hscale]
        exact hdiff
      _ ≤ δ := hradius
  calc
    |SimilarityCoordinates.coordinateEta (2*h) (tau,z)| =
        |(SimilarityCoordinates.coordinateEta (2*h) (tau,z) - eta) + eta| := by congr 1; ring
    _ ≤ |SimilarityCoordinates.coordinateEta (2*h) (tau,z) - eta| + |eta| := abs_add_le _ _
    _ ≤ δ + |eta| := add_le_add hstep (le_refl _)
    _ = |eta| + δ := by ring

/-- The analytic tube scaling turns an axial spatial radius `c*sqrt(tau)`
into a uniform eta margin for every `tau <= 1`. -/
theorem coordinateEta_margin_of_sqrt_axial_radius {h tau eta z c : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (htau : 0 < tau) (htau1 : tau ≤ 1)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1) (hc : 0 ≤ c)
    (hball : |z - eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)| ≤
      c * Real.sqrt tau) :
    |SimilarityCoordinates.coordinateEta (2*h) (tau,z)| ≤
      |eta| + c / (1 - 2*h) := by
  have hD : 0 < CoordinateAlgebra.D h := by
    unfold CoordinateAlgebra.D
    linarith
  have halpha : 0 < 1 - 2*h := by linarith
  have hden : 0 < (1 - 2*h) * tau ^ ((1 - 2*h) / 2) := by positivity
  have hexp : CoordinateAlgebra.D h + h = (1 : ℝ) / 2 := by
    unfold CoordinateAlgebra.D
    ring
  have hpow : tau ^ ((1 : ℝ) / 2) =
      tau ^ (CoordinateAlgebra.D h) * tau ^ h := by
    rw [← Real.rpow_add htau]
    congr 1
    exact hexp.symm
  have hscale : Real.sqrt tau / tau ^ (CoordinateAlgebra.D h) = tau ^ h := by
    rw [Real.sqrt_eq_rpow, hpow]
    field_simp [Real.rpow_pos_of_pos htau (CoordinateAlgebra.D h)]
  have hscale_le : Real.sqrt tau / tau ^ (CoordinateAlgebra.D h) ≤ 1 := by
    rw [hscale]
    exact Real.rpow_le_one htau.le htau1 (by linarith)
  have hscaledRadius :
      |z - eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)| /
        ((1 - 2*h) * tau ^ ((1 - 2*h) / 2)) ≤ c / (1 - 2*h) := by
    calc
      _ ≤ (c * Real.sqrt tau) / ((1 - 2*h) * tau ^ ((1 - 2*h) / 2)) :=
        div_le_div_of_nonneg_right hball hden.le
      _ = (c / (1 - 2*h)) *
          (Real.sqrt tau / tau ^ (CoordinateAlgebra.D h)) := by
        rw [show (1 - 2*h) / 2 = CoordinateAlgebra.D h by
          unfold CoordinateAlgebra.D; ring]
        field_simp [ne_of_gt (Real.rpow_pos_of_pos htau _)]
      _ ≤ (c / (1 - 2*h)) * 1 :=
        mul_le_mul_of_nonneg_left hscale_le (div_nonneg hc halpha.le)
      _ = c / (1 - 2*h) := by ring
  exact coordinateEta_margin_of_axial_radius hh hh1 htau heta hscaledRadius

/-- On the actual selected construction's open physical exterior, the
cutoff-summed, periodic, activated candidate has the selected smooth-base germ
whenever the first potential cutoff is on its unit plateau. -/
theorem selected_inner_exterior_velocity_germ
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℕ)
    (ha : Tendsto (fun j => (a j : ℝ)) atTop atTop)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualExteriorPrefix.exteriorDomain
      (ActualCandidateConstruction.residualBand B N0))
    (hsmall : |(a 0 : ℝ) * PhysicalWaveSum.physicalQ h w| < 1 / 2)
    (hplateau : w.2 ∈ SpatialLocalization.plateau)
    (ht : 3 / 4 < w.1) :
    TimeLocalization.activatedVelocity
      (MixedPeriodicAssembly.periodicVelocity
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ h)
          (ActualCandidateAssembly.potentialStages B N0 hN))
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ h)
          (ActualCandidateAssembly.directStages B N0 hN))) =ᶠ[𝓝 w]
      (FinalSlowBase.velocity certificate modulation upper B) := by
  let A := ActualCandidateAssembly.potentialStages B N0 hN
  let D := ActualCandidateAssembly.directStages B N0 hN
  let ASum := SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
    (PhysicalWaveSum.physicalQ h) A
  let BSum := SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
    (PhysicalWaveSum.physicalQ h) D
  have hq : ContinuousAt (PhysicalWaveSum.physicalQ h) w :=
    (PhysicalWaveSum.physicalQ_smoothAt outgoing.data.h_pos outgoing.data.h_lt_half
      hw.1.1).continuousAt
  have hqpos : 0 < PhysicalWaveSum.physicalQ h w :=
    PhysicalWaveSum.physicalQ_pos outgoing.data.h_pos outgoing.data.h_lt_half hw.1.1
  have hExterior := ActualCandidateAssembly.exteriorStages B N0 hN
  have hA0 : A 0 =ᶠ[𝓝 w]
      (TailGaugePotential.finalPotential certificate modulation upper B) :=
    ActualExteriorPrefix.eqOn_exterior_germ hExterior.potential_zero hw
  have hApos : ∀ j : ℕ, j ≠ 0 → A j =ᶠ[𝓝 w] fun _ => 0 := by
    intro j hj
    cases j with
    | zero => exact (hj rfl).elim
    | succ j =>
        exact ActualExteriorPrefix.eqOn_exterior_germ (hExterior.potential_succ j) hw
  have hfirst := AxisPreservation.potentialSum_eq_first_near ha hq hqpos hApos
  have hcut := (SmoothCutoffs.scaledCutoff_eventually_one hsmall).comp_tendsto hq
  have hcutStage : SolenoidalDiagonal.cutStage (fun j => (a j : ℝ))
      (PhysicalWaveSum.physicalQ h) A 0 =ᶠ[𝓝 w] A 0 := by
    filter_upwards [hcut] with z hz
    change SmoothCutoffs.scaledCutoff (a 0) (PhysicalWaveSum.physicalQ h z) = 1 at hz
    simp only [SolenoidalDiagonal.cutStage, hz, one_smul]
  have hAsum : ASum =ᶠ[𝓝 w]
      (TailGaugePotential.finalPotential certificate modulation upper B) :=
    hfirst.trans (hcutStage.trans hA0)
  have hDzero : ∀ j : ℕ, D j =ᶠ[𝓝 w] fun _ => 0 := by
    intro j
    exact ActualExteriorPrefix.eqOn_exterior_germ (hExterior.direct_zero j) hw
  have hBsum : BSum =ᶠ[𝓝 w] fun _ => 0 :=
    DirectAngularDiagonal.potentialSum_zero_germ ha hq hqpos D hDzero
  have hcurl := SolenoidalDiagonal.spatialCurl_eventuallyEq hAsum
  have hBaseCurl :
      SpatialCurl.spatialCurl (TailGaugePotential.finalPotential certificate modulation upper B)
        =ᶠ[𝓝 w] (FinalSlowBase.velocity certificate modulation upper B) := by
    filter_upwards [PhysicalWaveSum.preterminal_open.mem_nhds hw.1.1] with z hz
    exact TailGaugePotential.finalPotential_sameCurl certificate modulation upper B hz
  have hMixed : MixedPeriodicAssembly.velocity ASum BSum =ᶠ[𝓝 w]
      (FinalSlowBase.velocity certificate modulation upper B) := by
    have hsum : MixedPeriodicAssembly.velocity ASum BSum =ᶠ[𝓝 w]
        SpatialCurl.spatialCurl (TailGaugePotential.finalPotential certificate modulation upper B) := by
      change (fun z => SpatialCurl.spatialCurl ASum z + BSum z) =ᶠ[𝓝 w]
        (fun z => SpatialCurl.spatialCurl
          (TailGaugePotential.finalPotential certificate modulation upper B) z)
      filter_upwards [hcurl, hBsum] with z hc hb
      rw [hc, hb, add_zero]
    exact hsum.trans hBaseCurl
  have hPeriodic := (MixedPeriodicAssembly.periodicVelocity_eventuallyEq ASum BSum hplateau).trans hMixed
  have hActivated :=
    (TimeLocalization.activatedVelocity_eventuallyEq_late
      (MixedPeriodicAssembly.periodicVelocity ASum BSum) ht w.2).trans hPeriodic
  simpa only [A, D, ASum, BSum] using hActivated

/-- A strict physical-radius bound puts a point below the inner edge of the
actual selected annulus. This converts the radius/Q chart identity used by
the source into the exterior premise required by the field-transfer theorem.
-/
theorem selected_inner_exterior_velocity_germ_of_radial_hole
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℕ)
    (ha : Tendsto (fun j => (a j : ℝ)) atTop atTop)
    {w : ProblemStatement.SpaceTime}
    (ht : w ∈ PhysicalWaveSum.preterminal)
    (hq : PhysicalWaveSum.physicalQ h w <
      ChartScales.Q (ActualCandidateConstruction.residualBand B N0))
    (hr : PhysicalWaveSum.physicalPosition w 0 ^ 2 /
      (2 * PhysicalWaveSum.physicalQ h w) <
        NominalConeAssembly.activeLeft nominal)
    (hsmall : |(a 0 : ℝ) * PhysicalWaveSum.physicalQ h w| < 1 / 2)
    (hplateau : w.2 ∈ SpatialLocalization.plateau)
    (htime : 3 / 4 < w.1) :
    TimeLocalization.activatedVelocity
      (MixedPeriodicAssembly.periodicVelocity
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ h)
          (ActualCandidateAssembly.potentialStages B N0 hN))
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ h)
          (ActualCandidateAssembly.directStages B N0 hN))) =ᶠ[𝓝 w]
      (FinalSlowBase.velocity certificate modulation upper B) := by
  have hnotActive : w ∉ ActualPolarCoverage.active := by
    intro hw
    have hchart : (SlowBorelBase.cartesianChart h w).2.1 ∈
        Set.Icc (NominalConeAssembly.activeLeft nominal)
          (NominalConeAssembly.activeRight nominal) := by
      simpa only [ActualPolarCoverage.active, Set.mem_ofPred_eq] using hw
    have hleft := hchart.1
    rw [← ActualCandidateAssembly.physicalRadiusX_eq] at hleft
    exact (not_lt_of_ge hleft) hr
  have hdomain : w ∈ ActualExteriorPrefix.exteriorDomain
      (ActualCandidateConstruction.residualBand B N0) :=
    ActualExteriorPrefix.mem_exteriorDomain.mpr ⟨ht, hq, hnotActive⟩
  exact selected_inner_exterior_velocity_germ B N0 hN a ha hdomain hsmall hplateau htime

end ConcentrationAware
