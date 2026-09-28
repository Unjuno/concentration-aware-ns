# A quantitative cusp tube from the OpenAI construction's similarity chart

This note derives the geometric part of a possible support-hole transfer. It
does **not** prove that every selected perturbation stage, its spatial curl, and
the final activated periodic field vanish on the tube. Those assembly facts
remain a separate formalization obligation. No particle or material-property
conclusion follows.

## Similarity-coordinate identity

At a point with τ=1-t>0 and axial coordinate z, the pinned source defines q by

    τ = q - z² q^(2h),        0 < h < 1/2.

Put D=1/2-h and η=z/q^D. Since 2D+2h=1, this becomes

    τ = q(1-η²),        q = τ/(1-η²).

In particular q≥τ. The equivalent normalized axial coordinate is

    z/τ^D = F(η),        F(s)=s(1-s²)^(-D),  -1<s<1.

Direct differentiation gives

    F'(s)=(1-s²)^(-D-1) (1-2h s²) ≥ 1-2h > 0.

Here D>0, so the first factor is at least one, while
`1-2h s² >= 1-2h`. Thus F is strictly increasing and its inverse is
`1/(1-2h)`-Lipschitz by the mean value theorem.

## Tube around the selected axis trajectory

Fix the source trajectory parameter η₀∈(-1,1), set
`d=1-η₀²`, and write

    X(t)=(0,0, η₀ ((1-t)/d)^D).

For a point in the spatial ball `|x-X(t)| <= c sqrt(τ)`, its axial
coordinate z satisfies

    |F(η)-F(η₀)| = |z-z₀|/τ^D <= c τ^h.

The equality uses `z₀/τ^D=F(η₀)`; the bound uses
`1/2-D=h`. If `τ<=1`, the inverse estimate yields

    |η-η₀| <= c/(1-2h).

Let `δ=(1-|η₀|)/2` and choose
`0<c<min(c₀,(1-2h)δ)`, where `c₀>0` is a common inner-support
coefficient for all perturbation primitives. Then
`|η| <= |η₀|+δ < 1`, and with
`s₀=1-(|η₀|+δ)²>0`,

    τ <= q <= τ/s₀.

For any point in that ball the transverse radius r also satisfies
`r<=c sqrt(τ)<c₀ sqrt(q)`. Thus the entire spatial ball lies strictly
inside the proposed common support hole, provided the primitive support
statements apply at every point.

The ball also lies in the selected construction's physical sublevel and
localization plateau for all sufficiently small τ. For example it suffices
to impose the positive bounds

    τ < s₀ qbig,       τ < 1/4,       c²τ < 1/32,
    c sqrt(τ) < 1/16,
    |η₀|(τ/d)^D < 1/16.

The last condition is omitted when η₀=0. Each left side tends to zero
with τ, so a single positive τ₀ exists; for every
`0<1-t<τ₀`, the whole closed spatial ball lies in `q<qbig`, has
`radialSquare<1/32`, and has `|z|<1/8`. These are the physical sublevel,
time-activation, and spatial-plateau conditions used by the construction.

Consequently the **geometric** obstacle is resolved conditionally: an
inner-support theorem for all primitive corrections would give a cusp tube of
radius `c sqrt(1-t)` on which those corrections vanish. Since the inequality
is strict throughout the closed ball, each point has an open neighborhood
inside the zero region, which is also needed before concluding that the curl
of a vanishing potential is zero.

## Exact status and next proof obligation

The source gives the chart identity and inner annulus bounds for the initial
copy waves, actual mean families, particular waves, and signed exterior terms.
A source reread at the same pin now identifies one stage-independent candidate
coefficient for all primitive corrections:

    c₀ = min(leftRadius/(4*sqrt(2)), patch.a/4) > 0.

The copy term uses `InitialPhysicalData.potential_zero_exterior` and its
physical-copy annulus; every positive particular/signed stage is zero outside
the same nominal active annulus; and the actual mean stream stages share the
fixed initialization-patch lower radius. The existing Lean extension proves
the generic copy-sum inner-hole implication, while upstream assembly lemmas
already provide pointwise or germ-zero statements for the actual primitive
terms. These facts strengthen the support-hole premise beyond an axis-only
germ argument.

The remaining gap is now specifically the transfer to the complete selected
field: package the uniform stage-zero region through the selected infinite
cutoff sums and derivatives of the potential sum, then through direct-field,
periodic spatial localization and time activation. No end-to-end Lean theorem
yet states that the final activated velocity equals its base on the full cusp
tube. This is not an executable numerical certificate; the selected constants
are existential, so no numerical tube radius is claimed.

Source lemmas are pinned in [`InitialPhysicalData.lean`
(`potential_zero_exterior`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/InitialPhysicalData.lean),
[`ActualCandidateAssembly.lean`
(`particular_zero_germs`, `signed_zero_germs`, `positivePotential_curl`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualCandidateAssembly.lean),
[`ActualCurrentWaveSupport.lean`
(`current_field_active_germs`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualCurrentWaveSupport.lean),
and [`ActualMeanStageData.lean`
(`innerRadius`, `coefficient_vanishes`)](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/ActualMeanStageData.lean).

The algebraic identities `2D+2h=1`, the chart-factor identity, and the
derivative factorization are independently checked by
`tools/check_support_hole_tube_geometry.py`; its output is recorded at
`evidence/tests/support-hole-tube-geometry.json`. Those symbolic checks do not
verify the inequalities, the source-support instantiation, or the final-field
transfer.

## Pinned source

The chart equation is `SimilarityCoordinates.forwardScalar` with parameter
`a=2h`; the normalized variable is `SimilarityCoordinates.coordinateEta` with
exponent `(1-a)/2=D`. The physical maps are defined in `SimilarityProfile.q`
and `SimilarityProfile.eta`. These files are pinned at:

- [SimilarityCoordinates.lean](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/SimilarityCoordinates.lean)
- [SimilarityProfile.lean](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/SimilarityProfile.lean)

The selected axis trajectory identity used here is in
[`docs/openai-core-material-trajectory.md`](openai-core-material-trajectory.md)
and its Lean extension `verification/AxisForceSign.lean`; that material-flow
argument is separately classified as a hand-derived consequence, not an
upstream theorem.
