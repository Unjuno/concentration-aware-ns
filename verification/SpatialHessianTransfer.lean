import SupportHoleAssembly
import SpatialJetRestriction

noncomputable section

namespace ConcentrationAware

open NavierStokes
open NavierStokes.CorrectionInitialization.ActualPrimary
open Filter Set
open scoped Topology

/-- Transfer the cusp-ball full spacetime Hessian estimate to its fixed-time
spatial Hessian. Local smoothness follows from the selected-field germ equality
on that ball; the generic restriction estimate is then applied pointwise. -/
theorem selected_cusp_ball_actual_spatial_hessian_rate
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℕ)
    (ha : Tendsto (fun j => (a j : ℝ)) atTop atTop)
    {eta c beta : ℝ} (heta : eta ∈ Set.Ioo (-1 : ℝ) 1)
    (hc : 0 < c) (hbeta : 0 ≤ beta) (hbeta1 : beta < 1)
    (hmargin : |eta| + c / (1 - 2 * outgoing.data.h) ≤ beta)
    (hcactive : c ^ 2 < NominalConeAssembly.activeLeft nominal) :
    ∃ tau0 > 0, ∃ C ≥ 0, ∀ {tau : ℝ}, 0 < tau → tau < tau0 →
      ∀ {w : ProblemStatement.SpaceTime}, w.1 = 1 - tau →
        ‖w.2 - (eta * (tau / (1 - eta ^ 2)) ^
          (CoordinateAlgebra.D outgoing.data.h)) •
          ProblemStatement.coordinateVector 2‖ ≤ c * Real.sqrt tau →
        ‖iteratedFDeriv ℝ 2
          (fun y : ProblemStatement.Space =>
            selectedCandidateVelocity B N0 hN (fun j => (a j : ℝ)) (w.1, y)) w.2‖ ≤
          C * (PhysicalWaveSum.physicalQ outgoing.data.h w) ^ (-40 : ℝ) := by
  obtain ⟨tauRate, hRatePos, C, hC, hRate⟩ :=
    selected_cusp_ball_actual_hessian_rate B N0 hN a ha heta hc hbeta hbeta1
      hmargin hcactive
  obtain ⟨tauGerm, hGermPos, hGerm⟩ :=
    selected_velocity_germ_on_cusp_tube B N0 hN a ha heta hc hbeta hbeta1
      hmargin hcactive
  let tau0 := min tauRate tauGerm
  have hTau0 : 0 < tau0 := by dsimp [tau0]; positivity
  refine ⟨tau0, hTau0, C, hC, ?_⟩
  intro tau htau hlt w hwt hball
  have hltRate : tau < tauRate := lt_of_lt_of_le hlt (min_le_left _ _)
  have hltGerm : tau < tauGerm := lt_of_lt_of_le hlt (min_le_right _ _)
  have hFull := hRate htau hltRate hwt hball
  have hEq := hGerm htau hltGerm hwt hball
  have hwPast : w ∈ BaseResidual.past := by
    change w.1 < 1 ∧ w.2 ∈ Set.univ
    constructor
    · rw [hwt]
      linarith
    · simp
  have hPastOpen : IsOpen BaseResidual.past := by
    rw [BaseResidual.past]
    exact isOpen_Iio.prod isOpen_univ
  have hPastNhds : BaseResidual.past ∈ 𝓝 w := hPastOpen.mem_nhds hwPast
  have hBaseSmooth : ContDiffAt ℝ 2
      (FinalSlowBase.velocity certificate modulation upper B) w :=
    ((FinalSlowBase.velocity_smooth certificate modulation upper B).contDiffAt hPastNhds).of_le
      (by simp)
  have hCandidateEq :
      selectedCandidateVelocity B N0 hN (fun j => (a j : ℝ)) =ᶠ[𝓝 w]
        FinalSlowBase.velocity certificate modulation upper B := by
    simpa [selectedCandidateVelocity] using hEq
  have hCandidateSmooth : ContDiffAt ℝ 2
      (selectedCandidateVelocity B N0 hN (fun j => (a j : ℝ))) w :=
    hBaseSmooth.congr_of_eventuallyEq hCandidateEq
  have hSpatial := spatial_jet_norm_le_spacetime_jet_norm_at
    (selectedCandidateVelocity B N0 hN (fun j => (a j : ℝ))) 2 w.1 w.2 hCandidateSmooth
  exact le_trans hSpatial hFull

end ConcentrationAware
