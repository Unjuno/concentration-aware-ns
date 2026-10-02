import Mathlib

noncomputable section

namespace ConcentrationAware

/-- At a locally `C^m` spacetime point, restricting the iterated Frechet jet
to the fixed-time spatial slice does not increase its norm. This local form
does not require the field to be smooth outside a neighborhood of `(t,x)`. -/
theorem spatial_jet_norm_le_spacetime_jet_norm_at
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [NontrivialTopology E]
      [NormedAddCommGroup F] [NormedSpace ℝ F]
    (u : ℝ × E → F) (m : ℕ) (t : ℝ) (x : E)
    (hu : ContDiffAt ℝ m u (t, x)) :
    ‖iteratedFDeriv ℝ m (fun y : E => u (t, y)) x‖ ≤
      ‖iteratedFDeriv ℝ m u (t, x)‖ := by
  let L : E →L[ℝ] ℝ × E := ContinuousLinearMap.inr ℝ ℝ E
  let shift : ℝ × E → ℝ × E := fun z => z + (t, 0)
  let f : ℝ × E → F := u ∘ shift
  have huWithin : ContDiffWithinAt ℝ m u Set.univ (t, x) := hu
  obtain ⟨s, hsN, hsmooth⟩ :=
    (contDiffWithinAt_iff_contDiffOn_nhds (f := u) (s := Set.univ) (x := (t, x))
      (by simp)).mp huWithin
  have hsN' : s ∈ nhds (t, x) := by simpa using hsN
  obtain ⟨v, hvs, hvOpen, hwv⟩ := mem_nhds_iff.mp hsN'
  have huOn : ContDiffOn ℝ m u v := hsmooth.mono hvs
  let S : Set (ℝ × E) := shift ⁻¹' v
  let sliceDomain : Set E := L ⁻¹' S
  have hshift : ContDiff ℝ m shift := contDiff_id.add contDiff_const
  have hS : IsOpen S := by
    exact hvOpen.preimage hshift.continuous
  have hsliceDomain : IsOpen sliceDomain := by
    exact hS.preimage L.continuous
  have hfOn : ContDiffOn ℝ m f S := by
    exact huOn.comp hshift.contDiffOn (by
      intro z hz
      exact hz)
  have hLx : L x ∈ S := by
    change shift (L x) ∈ v
    simpa [shift, L] using hwv
  have hxSlice : x ∈ sliceDomain := hLx
  have hL : ‖L‖ = 1 := by
    simpa [L] using (ContinuousLinearMap.norm_inr ℝ ℝ E)
  have hslice : (fun y : E => u (t, y)) = f ∘ L := by
    funext y
    simp [f, shift, L]
  have hcomp := L.iteratedFDerivWithin_comp_right hfOn hS.uniqueDiffOn
    hsliceDomain.uniqueDiffOn hLx (i := m) le_rfl
  have hcompGlobal :
      iteratedFDeriv ℝ m (f ∘ L) x = iteratedFDerivWithin ℝ m (f ∘ L) sliceDomain x :=
    (iteratedFDerivWithin_of_isOpen m hsliceDomain hxSlice).symm
  have hfGlobal : iteratedFDerivWithin ℝ m f S (L x) = iteratedFDeriv ℝ m f (L x) :=
    iteratedFDerivWithin_of_isOpen m hS hLx
  have htranslate : iteratedFDeriv ℝ m f (L x) = iteratedFDeriv ℝ m u (t, x) := by
    change iteratedFDeriv ℝ m (fun z => u (z + (t, 0))) (L x) = _
    rw [iteratedFDeriv_comp_add_right m (t, 0) (L x)]
    simp [L]
  calc
    ‖iteratedFDeriv ℝ m (fun y : E => u (t, y)) x‖ =
        ‖iteratedFDerivWithin ℝ m (f ∘ L) sliceDomain x‖ := by
          rw [hslice, ← hcompGlobal]
    _ = ‖(iteratedFDerivWithin ℝ m f S (L x)).compContinuousLinearMap
          (fun _ => L)‖ := by rw [hcomp]
    _ ≤ ‖iteratedFDerivWithin ℝ m f S (L x)‖ * ‖L‖ ^ m := by
          simpa [Finset.prod_const, Fintype.card_fin] using
            (ContinuousMultilinearMap.norm_compContinuousLinearMap_le
              (iteratedFDerivWithin ℝ m f S (L x)) (fun _ => L))
    _ = ‖iteratedFDeriv ℝ m u (t, x)‖ := by
          rw [hL, one_pow, hfGlobal, htranslate]
          simp

end ConcentrationAware
