import NavierStokes.ActualMeanStageData
import NavierStokes.LocalPhysicalCopyBounds

/-!
This extension proves the quantitative support-hole implication for an actual
copy-family sum. It is deliberately smaller than the assembled-field tube
claim: stage-series/domain coverage is audited separately.
-/

namespace ConcentrationAware

open NavierStokes

theorem copy_sum_zero_below_physical_hole
    {H : ℕ} {K : Type*}
    {f : PhysicalCopyBounds.CopyFamily H K}
    {a b h r0 Z : ℝ} {Δ : ℕ}
    (support : LocalPhysicalCopyBounds.SupportData f a b h r0 Z Δ)
    (ha : 0 < a) (hh : 0 < h) (hh1 : h < 1 / 2)
    {w : ProblemStatement.SpaceTime}
    (hw : w ∈ PhysicalWaveSum.preterminal)
    (hsmall : DirectAngularDiagonal.radius w <
      a * Real.sqrt (PhysicalWaveSum.physicalQ h w / 2)) :
    f.sum a h r0 w = 0 := by
  by_contra hne
  obtain ⟨I, k, hamp, hann, hlabel⟩ := support.sum_support hw hne
  have hq := PhysicalWaveSum.physicalQ_pos hh hh1 hw
  have hband := PhysicalWaveSum.labelRegion_active_relation hlabel
  have hrad : a ≤ PolarCharts.radius
      (PhysicalGraphBounds.scaledRadial I.1.val.1 w) :=
    hann.2.trans (PolarCharts.norm_le_radius _)
  have hscale := ActualMeanStageData.physical_radius_scale I.1.val.1 w
  have hroot : Real.sqrt (PhysicalWaveSum.physicalQ h w / 2) ≤
      Real.sqrt (ChartScales.Q I.1.val.1) :=
    Real.sqrt_le_sqrt hband.1
  have hge : a * Real.sqrt (PhysicalWaveSum.physicalQ h w / 2) ≤
      DirectAngularDiagonal.radius w := by
    calc
      a * Real.sqrt (PhysicalWaveSum.physicalQ h w / 2) ≤
          a * Real.sqrt (ChartScales.Q I.1.val.1) :=
        mul_le_mul_of_nonneg_left hroot ha.le
      _ ≤ Real.sqrt (ChartScales.Q I.1.val.1) *
          PolarCharts.radius (PhysicalGraphBounds.scaledRadial I.1.val.1 w) := by
        rw [mul_comm a]
        exact mul_le_mul_of_nonneg_left hrad (Real.sqrt_nonneg _)
      _ = DirectAngularDiagonal.radius w := hscale.symm
  exact (not_lt_of_ge hge) hsmall

end ConcentrationAware
