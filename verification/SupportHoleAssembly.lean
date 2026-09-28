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
exterior. The separate cusp-tube geometry note supplies conditions under which
a proposed tube lies in this exterior; this file does not formalize those
geometric inequalities.
-/

noncomputable section

namespace ConcentrationAware

open NavierStokes
open NavierStokes.CorrectionInitialization.ActualPrimary
open Filter Set
open scoped Topology

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
