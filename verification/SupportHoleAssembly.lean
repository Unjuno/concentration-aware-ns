import NavierStokes.ActualCandidateAssembly

/-!
This extension connects the pinned actual stage-level exterior-zero lemmas to
the inner side of the selected active annulus, then transfers the selected
initialized sums, spatial curl, periodicization, and time activation as germs.
Uniform tube hypotheses remain separate obligations.
-/

noncomputable section

namespace ConcentrationAware

open NavierStokes
open Set Filter
open CorrectionInitialization.ActualPrimary
open scoped Topology

/-- If every stage vanishes on a neighborhood, local finiteness of the
cutoff sum makes the complete diagonal sum vanish there too. -/
theorem diagonal_sum_zero_of_stage_germs
    {E V : Type*} [TopologicalSpace E] [NormedAddCommGroup V] [NormedSpace ℝ V]
    {a : ℕ → ℝ} {q : E → ℝ} {A : ℕ → E → V} {w : E}
    (ha : Filter.Tendsto a Filter.atTop Filter.atTop)
    (hq : ContinuousAt q w) (hqw : 0 < q w)
    (hA : ∀ j, (fun y => A j y) =ᶠ[𝓝 w] fun _ => 0) :
    NavierStokes.SolenoidalDiagonal.potentialSum a q A =ᶠ[𝓝 w] fun _ => 0 := by
  obtain ⟨N, hN⟩ := NavierStokes.SolenoidalDiagonal.potentialSum_eventuallyEq_partial
    ha hq hqw A
  have hfinite : ∀ᶠ y in 𝓝 w, ∀ j ∈ Finset.range N, A j y = 0 :=
    (Filter.eventually_all_finset (Finset.range N)).2 (fun j _ => hA j)
  filter_upwards [hN, hfinite] with y hy hzero
  rw [hy]
  unfold NavierStokes.SolenoidalDiagonal.partialPotential
  apply Finset.sum_eq_zero
  intro j hj
  simp [NavierStokes.SolenoidalDiagonal.cutStage, hzero j hj]

/-- Every perturbative potential and direct stage of the actual witness is
zero when its normalized transverse radius lies below the active annulus. -/
theorem actual_stages_zero_below_active_radius
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualCandidateConstruction.physicalDomain B N0)
    (hinner : ActualCurrentWaveSupport.profileRadius h w <
      PrimaryTargetBounds.leftRadius nominal) :
    ActualCandidateAssembly.initialPotential B N0 w = 0 ∧
      (∀ j, ActualCandidateAssembly.positivePotential B N0 hN j w = 0) ∧
      (∀ j, ActualCandidateAssembly.directStages B N0 hN j w = 0) := by
  have hout : w ∉ ActualPolarCoverage.active := by
    intro ha
    have hr := (ActualCurrentWaveSupport.profileRadius_mem_iff_active hw.1).mpr ha
    exact (not_le_of_gt hinner) hr.1
  refine ⟨?_, ?_, ?_⟩
  · exact ActualCandidateAssembly.initialPotential_exterior B N0 hw.1 hw.2.le hout
  · intro j
    exact (ActualCandidateAssembly.positive_exterior B N0 hN j hw hout).1
  · intro j
    exact ActualCandidateAssembly.direct_exterior
      (ActualCandidateAssembly.meanCycleInput B N0 hN) j hw.1 hw.2.le hout

/-- The pointwise stage-hole theorem is stable on a neighborhood because both
the physical construction domain and the strict inner-radius condition are
open. -/
theorem actual_stage_zero_germs_below_active_radius
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualCandidateConstruction.physicalDomain B N0)
    (hinner : ActualCurrentWaveSupport.profileRadius h w <
      PrimaryTargetBounds.leftRadius nominal) :
    (ActualCandidateAssembly.initialPotential B N0) =ᶠ[𝓝 w]
        (fun _ => (0 : ProblemStatement.Space)) ∧
      (∀ j, ActualCandidateAssembly.positivePotential B N0 hN j =ᶠ[𝓝 w]
        fun _ => (0 : ProblemStatement.Space)) ∧
      (∀ j, ActualCandidateAssembly.directStages B N0 hN j =ᶠ[𝓝 w]
        fun _ => (0 : ProblemStatement.Space)) := by
  have hdomain := ActualCandidateConstruction.physicalDomain_open B N0
    |>.mem_nhds hw
  have hrad := ActualCurrentWaveSupport.profileRadius_continuousAt
    outgoing.data.h_pos outgoing.data.h_lt_half hw.1
  have hgap : ContinuousAt (fun y => PrimaryTargetBounds.leftRadius nominal -
      ActualCurrentWaveSupport.profileRadius h y) w := continuousAt_const.sub hrad
  have hgap_event : ∀ᶠ y in 𝓝 w,
      0 < PrimaryTargetBounds.leftRadius nominal -
        ActualCurrentWaveSupport.profileRadius h y :=
    hgap.eventually (lt_mem_nhds (sub_pos.mpr hinner))
  have hinner_event : ∀ᶠ y in 𝓝 w,
      ActualCurrentWaveSupport.profileRadius h y < PrimaryTargetBounds.leftRadius nominal :=
    hgap_event.mono (fun _ hy => (sub_pos.mp hy))
  refine ⟨?_, ?_, ?_⟩
  · filter_upwards [hdomain, hinner_event] with y hy hr
    exact (actual_stages_zero_below_active_radius B N0 hN hy hr).1
  · intro j
    filter_upwards [hdomain, hinner_event] with y hy hr
    exact (actual_stages_zero_below_active_radius B N0 hN hy hr).2.1 j
  · intro j
    filter_upwards [hdomain, hinner_event] with y hy hr
    exact (actual_stages_zero_below_active_radius B N0 hN hy hr).2.2 j

/-- On the hole, the initialized potential diagonal has the selected slow
base germ whenever the zeroth cutoff is on its plateau. -/
theorem actual_potential_sum_eq_base_germ_inside_hole
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℝ) (ha : Filter.Tendsto a Filter.atTop Filter.atTop)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualCandidateConstruction.physicalDomain B N0)
    (hinner : ActualCurrentWaveSupport.profileRadius h w <
      PrimaryTargetBounds.leftRadius nominal)
    (hsmall : |a 0 * PhysicalWaveSum.physicalQ h w| < 1 / 2) :
    SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
      (ActualCandidateAssembly.potentialStages B N0 hN) =ᶠ[𝓝 w]
      TailGaugePotential.finalPotential certificate modulation upper B := by
  have hq := (PhysicalWaveSum.physicalQ_smoothAt outgoing.data.h_pos
    outgoing.data.h_lt_half hw.1).continuousAt
  have hpos := PhysicalWaveSum.physicalQ_pos outgoing.data.h_pos
    outgoing.data.h_lt_half hw.1
  have hz := actual_stage_zero_germs_below_active_radius B N0 hN hw hinner
  change SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
    (GermCandidateAssembly.potentialStages certificate modulation upper B
      (ActualCandidateAssembly.initialPotential B N0)
      (ActualCandidateAssembly.positivePotential B N0 hN)) =ᶠ[𝓝 w] _
  exact GermCandidateAssembly.potentialSum_eq_base_germ ha hq hpos hz.1 hz.2.1 hsmall

/-- The direct angular diagonal vanishes as a germ throughout the same open
inner hole, by local finiteness and the stage-level zero theorem. -/
theorem actual_direct_sum_zero_germ_inside_hole
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℝ) (ha : Filter.Tendsto a Filter.atTop Filter.atTop)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualCandidateConstruction.physicalDomain B N0)
    (hinner : ActualCurrentWaveSupport.profileRadius h w <
      PrimaryTargetBounds.leftRadius nominal) :
    SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
      (ActualCandidateAssembly.directStages B N0 hN) =ᶠ[𝓝 w] fun _ => 0 := by
  have hq := (PhysicalWaveSum.physicalQ_smoothAt outgoing.data.h_pos
    outgoing.data.h_lt_half hw.1).continuousAt
  have hpos := PhysicalWaveSum.physicalQ_pos outgoing.data.h_pos
    outgoing.data.h_lt_half hw.1
  have hz := actual_stage_zero_germs_below_active_radius B N0 hN hw hinner
  exact diagonal_sum_zero_of_stage_germs ha hq hpos hz.2.2

/-- The complete activated periodic candidate has the selected base germ at
every hole point where the zeroth cutoff and spatial/time localization are
on their plateaus. -/
theorem actual_candidate_velocity_eq_base_germ_inside_hole
    (B N0 : ℕ)
    (hN : ActualCarrierGeometry.geometricThreshold ≤ N0)
    (a : ℕ → ℝ) (ha : Filter.Tendsto a Filter.atTop Filter.atTop)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ ActualCandidateConstruction.physicalDomain B N0)
    (hinner : ActualCurrentWaveSupport.profileRadius h w <
      PrimaryTargetBounds.leftRadius nominal)
    (hsmall : |a 0 * PhysicalWaveSum.physicalQ h w| < 1 / 2)
    (hlate : 3 / 4 < w.1)
    (hplateau : w.2 ∈ SpatialLocalization.plateau) :
    TimeLocalization.activatedVelocity (MixedPeriodicAssembly.periodicVelocity
      (SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
        (ActualCandidateAssembly.potentialStages B N0 hN))
      (SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
        (ActualCandidateAssembly.directStages B N0 hN))) =ᶠ[𝓝 w]
      FinalSlowBase.velocity certificate modulation upper B := by
  have hp := actual_potential_sum_eq_base_germ_inside_hole B N0 hN a ha
    hw hinner hsmall
  have hd := actual_direct_sum_zero_germ_inside_hole B N0 hN a ha hw hinner
  have hc := SolenoidalDiagonal.spatialCurl_eventuallyEq hp
  have htime : ∀ᶠ y : ProblemStatement.SpaceTime in 𝓝 w, y.1 < 1 :=
    (isOpen_lt continuous_fst continuous_const).mem_nhds hw.1
  have hm : MixedPeriodicAssembly.velocity
      (SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
        (ActualCandidateAssembly.potentialStages B N0 hN))
      (SolenoidalDiagonal.potentialSum a (PhysicalWaveSum.physicalQ h)
        (ActualCandidateAssembly.directStages B N0 hN)) =ᶠ[𝓝 w]
      FinalSlowBase.velocity certificate modulation upper B := by
    filter_upwards [hc, hd, htime] with y hy hdy hty
    simp only [MixedPeriodicAssembly.velocity, hy, hdy, add_zero]
    exact TailGaugePotential.finalPotential_sameCurl certificate modulation upper B hty
  exact (TimeLocalization.activatedVelocity_eventuallyEq_late _ hlate w.2).trans
    ((MixedPeriodicAssembly.periodicVelocity_eventuallyEq _ _ hplateau).trans hm)

end ConcentrationAware

#print axioms ConcentrationAware.actual_stages_zero_below_active_radius
#print axioms ConcentrationAware.diagonal_sum_zero_of_stage_germs
#print axioms ConcentrationAware.actual_stage_zero_germs_below_active_radius
#print axioms ConcentrationAware.actual_potential_sum_eq_base_germ_inside_hole
#print axioms ConcentrationAware.actual_direct_sum_zero_germ_inside_hole
#print axioms ConcentrationAware.actual_candidate_velocity_eq_base_germ_inside_hole
