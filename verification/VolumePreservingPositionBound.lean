import Mathlib

open MeasureTheory

namespace VolumePreservingPosition

/-- Any initial law dominated by K times volume retains that same spatial
domination under a measurable volume-preserving map. This bounds the chance
that passive tracers enter any measurable target set, including a target that
moves with time. -/
theorem transported_mass_bound
    {Ω : Type*} [MeasurableSpace Ω]
    (μ vol : Measure Ω) (flow : Ω → Ω) (K : ENNReal)
    (hflow : Measurable flow)
    (hdom : ∀ s, MeasurableSet s → μ s ≤ K * vol s)
    (hpres : ∀ s, MeasurableSet s → vol (flow ⁻¹' s) = vol s)
    (s : Set Ω) (hs : MeasurableSet s) :
    μ (flow ⁻¹' s) ≤ K * vol s := by
  calc
    μ (flow ⁻¹' s) ≤ K * vol (flow ⁻¹' s) :=
      hdom (flow ⁻¹' s) (hs.preimage hflow)
    _ = K * vol s := by rw [hpres s hs]

end VolumePreservingPosition

#print axioms VolumePreservingPosition.transported_mass_bound
