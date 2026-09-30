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

/-- A Euclidean ball around the axis trajectory controls its axial coordinate,
so the fixed-time eta-margin estimate applies to every point in that ball. -/
theorem coordinateEta_margin_of_euclidean_ball {h tau eta c : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (htau : 0 < tau) (htau1 : tau ≤ 1)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1) (hc : 0 ≤ c)
    {x : ProblemStatement.Space}
    (hball : ‖x - (eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)) •
      ProblemStatement.coordinateVector 2‖ ≤ c * Real.sqrt tau) :
    |SimilarityCoordinates.coordinateEta (2*h) (tau, x 2)| ≤
      |eta| + c / (1 - 2*h) := by
  let z0 := eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)
  have hcoord : (x - z0 • ProblemStatement.coordinateVector 2).ofLp 2 =
      x.ofLp 2 - z0 := by
    simp [z0, ProblemStatement.coordinateVector]
  have hcomponent : |x 2 - z0| ≤
      ‖x - z0 • ProblemStatement.coordinateVector 2‖ := by
    have hnorm := PiLp.norm_apply_le
      (x - z0 • ProblemStatement.coordinateVector 2) 2
    rw [hcoord] at hnorm
    simpa only [Real.norm_eq_abs] using hnorm
  have haxial : |x 2 - eta * (tau / (1 - eta^2)) ^ (CoordinateAlgebra.D h)| ≤
      c * Real.sqrt tau := by
    simpa [z0] using hcomponent.trans hball
  exact coordinateEta_margin_of_sqrt_axial_radius hh hh1 htau htau1 heta hc haxial

/-- An axial-centered Euclidean ball also bounds the physical transverse
radius. The bound is deliberately stated with `sqrt 2`, obtained from the two
coordinate projections; no material-volume contraction is asserted. -/
theorem transverse_radius_le_of_euclidean_ball {tau eta c : ℝ}
    {x : ProblemStatement.Space}
    (hball : ‖x - eta • ProblemStatement.coordinateVector 2‖ ≤
      c * Real.sqrt tau) :
    DirectAngularDiagonal.radius (1 - tau, x) ≤ Real.sqrt 2 * c * Real.sqrt tau := by
  let v := x - eta • ProblemStatement.coordinateVector 2
  have hcoord0 : v.ofLp 0 = x.ofLp 0 := by
    simp [v, ProblemStatement.coordinateVector]
  have hcoord1 : v.ofLp 1 = x.ofLp 1 := by
    simp [v, ProblemStatement.coordinateVector]
  have hn0 := PiLp.norm_apply_le v 0
  have hn1 := PiLp.norm_apply_le v 1
  rw [hcoord0] at hn0
  rw [hcoord1] at hn1
  have hx0 : |x 0| ≤ ‖v‖ := by simpa only [Real.norm_eq_abs] using hn0
  have hx1 : |x 1| ≤ ‖v‖ := by simpa only [Real.norm_eq_abs] using hn1
  have hr0 := Real.sq_sqrt (show 0 ≤ (x 0)^2 + (x 1)^2 by positivity)
  have hradius : DirectAngularDiagonal.radius (1 - tau, x) ^ 2 =
      (x 0)^2 + (x 1)^2 := by
    unfold DirectAngularDiagonal.radius PolarCharts.radius
    rw [Real.sq_sqrt (by positivity)]
    simp [PhysicalGraphBounds.radialProjection_apply]
  have hrnonneg := DirectAngularDiagonal.radius_nonneg (1 - tau, x)
  have hnormnonneg : 0 ≤ ‖v‖ := norm_nonneg _
  have hx0sq : (x.ofLp 0)^2 ≤ ‖v‖^2 := by
    have h := (sq_le_sq₀ (abs_nonneg (x.ofLp 0)) hnormnonneg).2 hx0
    simpa [sq_abs] using h
  have hx1sq : (x.ofLp 1)^2 ≤ ‖v‖^2 := by
    have h := (sq_le_sq₀ (abs_nonneg (x.ofLp 1)) hnormnonneg).2 hx1
    simpa [sq_abs] using h
  have hbound : DirectAngularDiagonal.radius (1 - tau, x) ^ 2 ≤ 2 * ‖v‖^2 := by
    rw [hradius]
    nlinarith
  have hroot : DirectAngularDiagonal.radius (1 - tau, x) ≤ Real.sqrt 2 * ‖v‖ := by
    have hsqrt2 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg _
    have hsquare : (Real.sqrt 2 * ‖v‖)^2 = 2 * ‖v‖^2 := by
      rw [mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    exact (sq_le_sq₀ hrnonneg (mul_nonneg hsqrt2 hnormnonneg)).mp
      (hbound.trans_eq hsquare.symm)
  calc
    DirectAngularDiagonal.radius (1 - tau, x) ≤ Real.sqrt 2 * ‖v‖ := hroot
    _ ≤ Real.sqrt 2 * (c * Real.sqrt tau) :=
      mul_le_mul_of_nonneg_left hball (Real.sqrt_nonneg _)
    _ = Real.sqrt 2 * c * Real.sqrt tau := by ring

/-- The same Euclidean ball bounds displacement in its axial coordinate. -/
theorem axial_deviation_le_of_euclidean_ball {tau eta c : ℝ}
    {x : ProblemStatement.Space}
    (hball : ‖x - eta • ProblemStatement.coordinateVector 2‖ ≤
      c * Real.sqrt tau) :
    |x 2 - eta| ≤ c * Real.sqrt tau := by
  have hcoord : (x - eta • ProblemStatement.coordinateVector 2).ofLp 2 =
      x.ofLp 2 - eta := by
    simp [ProblemStatement.coordinateVector]
  have hnorm := PiLp.norm_apply_le
    (x - eta • ProblemStatement.coordinateVector 2) 2
  rw [hcoord] at hnorm
  exact hnorm.trans hball

/-- The two spatial-ball bounds put every point strictly below the selected
active annulus and bound its physical similarity scale. This is a pointwise
geometry result; the cutoff and outer-localization conditions are separate. -/
theorem cusp_ball_point_in_physical_exterior
    {tau eta c beta : ℝ} (htau : 0 < tau) (htau1 : tau ≤ 1)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1) (hc : 0 ≤ c)
    (hbeta : 0 ≤ beta) (hbeta1 : beta < 1)
    (hmargin : |eta| + c / (1 - 2 * outgoing.data.h) ≤ beta)
    {w : ProblemStatement.SpaceTime} (hwt : w.1 = 1 - tau)
    (hball : ‖w.2 - (eta * (tau / (1 - eta^2)) ^
      (CoordinateAlgebra.D outgoing.data.h)) • ProblemStatement.coordinateVector 2‖ ≤
        c * Real.sqrt tau)
    (hcactive : c ^ 2 < NominalConeAssembly.activeLeft nominal)
    (horizon : tau < (1 - beta ^ 2) *
      ChartScales.Q (ActualCandidateConstruction.residualBand B N0)) :
    w ∈ PhysicalWaveSum.preterminal ∧
      PhysicalWaveSum.physicalQ outgoing.data.h w <
        ChartScales.Q (ActualCandidateConstruction.residualBand B N0) ∧
      PhysicalWaveSum.physicalQ outgoing.data.h w ≤ tau / (1 - beta ^ 2) ∧
      PhysicalWaveSum.physicalPosition w 0 ^ 2 /
        (2 * PhysicalWaveSum.physicalQ outgoing.data.h w) <
          NominalConeAssembly.activeLeft nominal := by
  have ht : w ∈ PhysicalWaveSum.preterminal := by
    change w.1 < 1
    rw [hwt]
    linarith
  have hEta := coordinateEta_margin_of_euclidean_ball
    outgoing.data.h_pos outgoing.data.h_lt_half htau htau1 heta hc hball
  have hetaBound : |SimilarityCoordinates.coordinateEta (2 * outgoing.data.h)
      (1 - w.1, w.2 2)| ≤ beta := by
    simpa [hwt] using hEta.trans hmargin
  have hqle := physicalQ_le_of_eta_margin ht hbeta hbeta1 hetaBound
  have hqleTau : PhysicalWaveSum.physicalQ outgoing.data.h w ≤
      tau / (1 - beta ^ 2) := by
    simpa [hwt] using hqle
  have hqpos := PhysicalWaveSum.physicalQ_pos
    outgoing.data.h_pos outgoing.data.h_lt_half ht
  have hden : 0 < 1 - beta ^ 2 := by nlinarith
  have hqsmall : PhysicalWaveSum.physicalQ outgoing.data.h w <
      ChartScales.Q (ActualCandidateConstruction.residualBand B N0) := by
    calc
      PhysicalWaveSum.physicalQ outgoing.data.h w ≤ tau / (1 - beta ^ 2) := hqleTau
      _ < ChartScales.Q (ActualCandidateConstruction.residualBand B N0) :=
        (div_lt_iff₀ hden).2 (by nlinarith [horizon])
  have hchart := physicalQ_time_identity ht
  have hha : 0 < 2 * outgoing.data.h := mul_pos (by norm_num) outgoing.data.h_pos
  have hha1 : 2 * outgoing.data.h < 1 := by linarith [outgoing.data.h_lt_half]
  have hetaSq := SimilarityCoordinates.coordinateEta_sq_lt_one
    (a := 2 * outgoing.data.h) hha hha1 (p := (1 - w.1, w.2 2))
      (sub_pos.mpr ht)
  have hchartTau : tau = PhysicalWaveSum.physicalQ outgoing.data.h w *
      (1 - SimilarityCoordinates.coordinateEta (2 * outgoing.data.h)
        (1 - w.1, w.2 2) ^ 2) := by
    calc
      tau = 1 - w.1 := by rw [hwt]; ring
      _ = _ := hchart
  have hqge : tau ≤ PhysicalWaveSum.physicalQ outgoing.data.h w := by
    rw [hchartTau]
    nlinarith [mul_nonneg hqpos.le (sq_nonneg (SimilarityCoordinates.coordinateEta
      (2 * outgoing.data.h) (1 - w.1, w.2 2)))]
  have hrad := transverse_radius_le_of_euclidean_ball
    (tau := tau) (eta := eta * (tau / (1 - eta ^ 2)) ^
      (CoordinateAlgebra.D outgoing.data.h)) (c := c) hball
  have hradNonneg := DirectAngularDiagonal.radius_nonneg w
  have hboundNonneg : 0 ≤ Real.sqrt 2 * c * Real.sqrt tau := by positivity
  have hradSq := (sq_le_sq₀ hradNonneg hboundNonneg).mpr hrad
  have hradSqBound : DirectAngularDiagonal.radius w ^ 2 ≤ 2 * c ^ 2 * tau := by
    calc
      DirectAngularDiagonal.radius w ^ 2 ≤ (Real.sqrt 2 * c * Real.sqrt tau) ^ 2 := hradSq
      _ = 2 * c ^ 2 * tau := by
        rw [mul_pow, mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2),
          Real.sq_sqrt htau.le]
  have hratio : PhysicalWaveSum.physicalPosition w 0 ^ 2 /
      (2 * PhysicalWaveSum.physicalQ outgoing.data.h w) ≤ c ^ 2 := by
    have hposition : PhysicalWaveSum.physicalPosition w 0 = DirectAngularDiagonal.radius w := by
      rfl
    rw [hposition]
    apply (div_le_iff₀ (by positivity :
      0 < 2 * PhysicalWaveSum.physicalQ outgoing.data.h w)).2
    nlinarith [sq_nonneg c]
  exact ⟨ht, hqsmall, hqleTau, hratio.trans_lt hcactive⟩

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

/-- Compose the finite-ball estimates with the selected-field exterior germ.
The cutoff plateau, spatial plateau, and late-time conditions are derived from
explicit shrinking-scale bounds; the smallness hypotheses remain explicit. -/
theorem selected_velocity_germ_of_cusp_ball_point
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℕ)
    (ha : Tendsto (fun j => (a j : ℝ)) atTop atTop)
    {tau eta c beta : ℝ} (htau : 0 < tau) (htau1 : tau ≤ 1)
    (heta : eta ∈ Set.Ioo (-1 : ℝ) 1) (hc : 0 ≤ c)
    (hbeta : 0 ≤ beta) (hbeta1 : beta < 1)
    (hmargin : |eta| + c / (1 - 2 * outgoing.data.h) ≤ beta)
    {w : ProblemStatement.SpaceTime} (hwt : w.1 = 1 - tau)
    (hball : ‖w.2 - (eta * (tau / (1 - eta^2)) ^
      (CoordinateAlgebra.D outgoing.data.h)) • ProblemStatement.coordinateVector 2‖ ≤
        c * Real.sqrt tau)
    (hcactive : c ^ 2 < NominalConeAssembly.activeLeft nominal)
    (horizon : tau < (1 - beta ^ 2) *
      ChartScales.Q (ActualCandidateConstruction.residualBand B N0))
    (hcutScale : tau < (1 - beta ^ 2) /
      (2 * max 1 (a 0 : ℝ)))
    (htimeScale : tau < 1 / 4)
    (hcenter : |eta * (tau / (1 - eta ^ 2)) ^
      (CoordinateAlgebra.D outgoing.data.h)| < 1 / 16)
    (haxialRadius : c * Real.sqrt tau < 1 / 16)
    (hradialScale : 2 * c ^ 2 * tau < 1 / 32) :
    TimeLocalization.activatedVelocity
      (MixedPeriodicAssembly.periodicVelocity
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ outgoing.data.h)
          (ActualCandidateAssembly.potentialStages B N0 hN))
        (SolenoidalDiagonal.potentialSum (fun j => (a j : ℝ))
          (PhysicalWaveSum.physicalQ outgoing.data.h)
          (ActualCandidateAssembly.directStages B N0 hN))) =ᶠ[𝓝 w]
      (FinalSlowBase.velocity certificate modulation upper B) := by
  obtain ⟨ht, hq, _, hr⟩ := cusp_ball_point_in_physical_exterior
    htau htau1 heta hc hbeta hbeta1 hmargin hwt hball hcactive horizon
  have hs : 0 < 1 - beta ^ 2 := by nlinarith
  have hM : 0 < 2 * max 1 (a 0 : ℝ) := by positivity
  have hcutCross : tau * (2 * max 1 (a 0 : ℝ)) < 1 - beta ^ 2 :=
    (lt_div_iff₀ hM).mp hcutScale
  have hqUpper : PhysicalWaveSum.physicalQ outgoing.data.h w ≤
      tau / (1 - beta ^ 2) := by
    exact (cusp_ball_point_in_physical_exterior htau htau1 heta hc hbeta hbeta1
      hmargin hwt hball hcactive horizon).2.2.1
  let A : ℝ := a 0
  have hA : 0 ≤ A := by positivity
  have hAmax : A ≤ max 1 A := le_max_right _ _
  have hmaxRatio : max 1 A * (tau / (1 - beta ^ 2)) < 1 / 2 := by
    rw [show max 1 A * (tau / (1 - beta ^ 2)) =
      (max 1 A * tau) / (1 - beta ^ 2) by ring]
    exact (div_lt_iff₀ hs).2 (by nlinarith [hcutCross])
  have hcutValue : 0 ≤ A * PhysicalWaveSum.physicalQ outgoing.data.h w :=
    mul_nonneg hA (le_of_lt (PhysicalWaveSum.physicalQ_pos
      outgoing.data.h_pos outgoing.data.h_lt_half ht))
  have hsmallValue : A * PhysicalWaveSum.physicalQ outgoing.data.h w < 1 / 2 := by
    calc
      A * PhysicalWaveSum.physicalQ outgoing.data.h w ≤
          A * (tau / (1 - beta ^ 2)) :=
        mul_le_mul_of_nonneg_left hqUpper hA
      _ ≤ max 1 A * (tau / (1 - beta ^ 2)) :=
        mul_le_mul_of_nonneg_right hAmax (div_nonneg htau.le hs.le)
      _ < 1 / 2 := hmaxRatio
  have hsmall : |(a 0 : ℝ) * PhysicalWaveSum.physicalQ outgoing.data.h w| < 1 / 2 := by
    simpa only [A, abs_of_nonneg hcutValue] using hsmallValue
  have htime : 3 / 4 < w.1 := by rw [hwt]; linarith
  have hrad := transverse_radius_le_of_euclidean_ball
    (tau := tau) (eta := eta * (tau / (1 - eta ^ 2)) ^
      (CoordinateAlgebra.D outgoing.data.h)) (c := c) hball
  have hrad' : DirectAngularDiagonal.radius w ≤ Real.sqrt 2 * c * Real.sqrt tau := by
    have hpair : w = (1 - tau, w.2) := by exact Prod.ext hwt rfl
    rw [hpair]
    exact hrad
  have hradNonneg := DirectAngularDiagonal.radius_nonneg w
  have hradBoundNonneg : 0 ≤ Real.sqrt 2 * c * Real.sqrt tau := by positivity
  have hradSq := (sq_le_sq₀ hradNonneg hradBoundNonneg).mpr hrad'
  have hradialSq : DirectAngularDiagonal.radius w ^ 2 ≤ 2 * c ^ 2 * tau := by
    calc
      DirectAngularDiagonal.radius w ^ 2 ≤ (Real.sqrt 2 * c * Real.sqrt tau) ^ 2 := hradSq
      _ = 2 * c ^ 2 * tau := by
        rw [mul_pow, mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2),
          Real.sq_sqrt htau.le]
  have hradEq : SpatialLocalization.radialSquare w.2 =
      DirectAngularDiagonal.radius w ^ 2 := by
    calc
      SpatialLocalization.radialSquare w.2 = w.2 0 ^ 2 + w.2 1 ^ 2 := rfl
      _ = PolarCharts.radius (PhysicalGraphBounds.radialProjection w) ^ 2 :=
        by simpa [PhysicalGraphBounds.radialProjection_apply] using
          (PolarCharts.radius_sq (PhysicalGraphBounds.radialProjection w)).symm
      _ = DirectAngularDiagonal.radius w ^ 2 := rfl
  have hradPlateau : SpatialLocalization.radialSquare w.2 < 1 / 32 := by
    rw [hradEq]
    exact hradialSq.trans_lt hradialScale
  have haxialDev := axial_deviation_le_of_euclidean_ball
    (tau := tau) (eta := eta * (tau / (1 - eta ^ 2)) ^
      (CoordinateAlgebra.D outgoing.data.h)) (c := c) hball
  have hz : |w.2 2| < 1 / 8 := by
    have htriangle : |w.2 2| ≤
        |w.2 2 - eta * (tau / (1 - eta ^ 2)) ^
          (CoordinateAlgebra.D outgoing.data.h)| +
        |eta * (tau / (1 - eta ^ 2)) ^ (CoordinateAlgebra.D outgoing.data.h)| := by
      calc
        |w.2 2| = |(w.2 2 - eta * (tau / (1 - eta ^ 2)) ^
          (CoordinateAlgebra.D outgoing.data.h)) +
          eta * (tau / (1 - eta ^ 2)) ^ (CoordinateAlgebra.D outgoing.data.h)| := by congr 1; ring
        _ ≤ _ := abs_add_le _ _
    apply lt_of_le_of_lt htriangle
    calc
      |w.2 2 - eta * (tau / (1 - eta ^ 2)) ^ (CoordinateAlgebra.D outgoing.data.h)| +
          |eta * (tau / (1 - eta ^ 2)) ^ (CoordinateAlgebra.D outgoing.data.h)| ≤
        c * Real.sqrt tau + |eta * (tau / (1 - eta ^ 2)) ^
          (CoordinateAlgebra.D outgoing.data.h)| := by nlinarith [haxialDev]
      _ < 1 / 16 + 1 / 16 := add_lt_add haxialRadius hcenter
      _ = 1 / 8 := by norm_num
  have hplateau : w.2 ∈ SpatialLocalization.plateau := by
    change SpatialLocalization.radialSquare w.2 < 1 / 32 ∧ |w.2 2| < 1 / 8
    exact ⟨hradPlateau, hz⟩
  exact selected_inner_exterior_velocity_germ_of_radial_hole
    B N0 hN a ha ht hq hr hsmall hplateau htime

end ConcentrationAware
