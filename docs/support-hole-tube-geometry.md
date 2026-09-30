# A quantitative cusp tube from the OpenAI construction's similarity chart

This note derives the geometric part of a possible support-hole transfer. The
selected-stage-to-final-field transfer is checked conditionally on the actual
open exterior in `verification/SupportHoleAssembly.lean`; this note does not yet
prove that every point in the proposed moving tube satisfies that theorem's
exterior and plateau hypotheses. No particle or material-property conclusion
follows.

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

The upper-bound implication from a uniform eta margin has now been checked in
Lean as `physicalQ_le_of_eta_margin` in
`verification/SupportHoleAssembly.lean`: if `|eta|<=beta<1`, then
`q<=tau/(1-beta²)`. The proof uses the pinned source's exact implicit chart
identity and is independent of simulation. Taking
`beta=|eta₀|+delta` yields the `q<=tau/s₀` estimate needed by the whole-tube
argument.

For any point in that ball the transverse radius r also satisfies
`r<=c sqrt(τ)<c₀ sqrt(q)`. Thus the entire spatial ball lies strictly
inside the proposed common support hole, provided the primitive support
statements apply at every point.

The ball also lies in the selected construction's physical sublevel, zeroth
cutoff plateau, and localization plateau for all sufficiently small τ. For
selected schedule `a`, it suffices to impose the positive bounds

    τ < s₀ Q_res,       τ < 1/4,       c²τ < 1/32,
    c sqrt(τ) < 1/16,
    τ < s₀/(2*max(1,(a(0):ℝ))),
    |η₀|(τ/d)^D < 1/16.

Here `Q_res = ChartScales.Q(residualBand B N0)` is the actual upper bound in
`ActualExteriorPrefix.exteriorDomain`; the source gives
`qbig = 2*Q_res`. This distinction matters: `q<qbig` alone does not imply
membership in the exterior domain required by the checked transfer theorem.
The `a(0)` bound uses `q<=τ/s₀` and enforces `a(0)q<1/2`; using
`max(1,(a(0):ℝ))` keeps the bound valid even if an admissible schedule starts at
zero. The last condition is omitted when η₀=0. Each left
side tends to zero with τ, so a single positive τ₀ exists; for every
`0<1-t<τ₀`, the whole closed spatial ball lies in `q<Q_res`, the first
potential cutoff is on its unit plateau, `radialSquare<1/32`, and `|z|<1/8`.
These are the exterior sublevel, cutoff, time-activation, and spatial-plateau
conditions needed to apply the checked transfer theorem.

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
germ argument. The zeroth-stage decomposition does require checking the
initialization terms: it is
`TailGaugePotential.finalPotential + initialPotential`. In this case the
initial copy potential and initial mean stream/direct fields use the same
inner-radius ingredients, and `ActualCandidateAssembly.initialPotential_exterior`
and `initialDirect_exterior` give zero outside the active annulus. Thus the
initial terms are not a separate obstruction to equality inside the proposed
hole. What remains unverified is the complete quantitative tube instantiation
and its composition through the selected sums and outer localizations.

### Source-level transfer map

The intended aggregate implication now has concrete source pieces. Write
`L=leftRadius` and `r` for transverse physical radius. The chart's active
annulus coordinate is `r²/(2q)`, while `activeLeft=L²/2`. From
`c₀<=L/(4*sqrt(2))` and `r<c₀ sqrt(q)`,

    r²/(2q) < c₀²/2 <= L²/64 < L²/2 = activeLeft.

So the tube is outside `ActualPolarCoverage.active` whenever it is
preterminal and `q<Q_res`. The named exterior lemmas kill the initial
potential/direct fields and signed/mean fields; the particular annulus lemmas
kill particular stages. Therefore the zeroth potential equals its base
potential on the tube, and every positive potential and direct stage has a
zero germ there. Since `q>0`, local finiteness reduces each selected cutoff
sum to a finite local prefix; the zeroth cutoff condition retains only the
base term and its spatial derivatives. Curl gives the base velocity, and the
existing periodic spatial and late-time local-agreement lemmas preserve it.
This makes the source-level transfer plausible without a uniform
stage-dependent germ radius.

The aggregate field-equality step is now formalized and compiled in
`verification/SupportHoleAssembly.lean` against the pinned source. Its theorem
works on the actual open exterior and keeps the zeroth-cutoff plateau and
outer-localization assumptions explicit. The moving-tube inequalities have
not yet been encoded and connected to those hypotheses. Thus the field
transfer is checked conditionally, while the proposed complete cusp tube
remains a hand-derived geometric consequence rather than a Lean theorem.

The extension now also contains
`selected_inner_exterior_velocity_germ_of_radial_hole`: given a point in the
preterminal region with `q<Q_res` and physical radius satisfying
`r²/(2q)<activeLeft`, it derives that the point is outside the actual active
annulus and applies the checked field-transfer theorem. The corollary keeps
the zeroth-cutoff, spatial-plateau and late-time hypotheses explicit. It does
not establish that every point in the proposed moving ball meets those
premises; the whole-ball estimates remain to be formalized.

The remaining gap is specifically quantitative moving-tube geometry and its
connection to the hypotheses of the checked exterior theorem. The pinned
source has generic lemmas for local finite-prefix equality of the cutoff
potential sum on `q>0`, spatial derivatives of that sum, and local agreement
through periodic spatial localization and time activation. The extension
composes the actual selected stages and direct-stage sum with those results.
The center-plane germ theorem alone is not a tube theorem. The selected
constants remain existential, so no numerical tube radius or executable
numerical certificate is claimed.

The pinned source tarball is archived at
`work/openai-f9e8bc5b38b6e212696e8a30e3e91517af887bbd.tar.gz` with SHA-256
`9832374e0926a8a9dfb19699e50bf8ddb957fb9e961e7cc85b8fb689eda2b1b7`. Lean
4.34.0-rc2 and pinned mathlib commit
`85e3a25e006c35636f0e53b0e9296caca2685bc0` were available through a verified
source archive and populated Lean cache. The five imported upstream modules
built successfully (3,679 jobs), and
`verification/SupportHoleAssembly.lean` compiled in that pinned environment.
The extension checks the conditional exterior field transfer, not the
quantitative tube geometry or any physical conclusion.

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
`evidence/tests/support-hole-tube-geometry.json`. Those symbolic checks do not verify the whole-tube inequalities or their
instantiation into the checked field-transfer theorem.

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

## 2026-09-30: axial eta-margin lemma

The extension now proves `coordinateEta_lipschitz_z` from the source's exact
`coordinateEta_hasDerivAt_z` formula and the lower bound
`scalarSlope = 1-a*eta^2 >= 1-a`. At fixed positive `tau`, this yields

    |eta(tau,z)-eta(tau,z')| <= |z-z'| / ((1-a)*tau^((1-a)/2)).

`coordinateEta_axis_center` derives the exact normalized center directly from
the source forward map, and `coordinateEta_margin_of_axial_radius` combines the
two results. Its hypothesis is an axial distance bound scaled by
`(1-2h)*tau^((1-2h)/2)`; its conclusion is the requested `|eta| <= |eta0|+delta`.
This is only a one-dimensional, fixed-time lemma. It remains to prove the
radius bound for every point in the full Cartesian cusp ball, include any
time-dependent center displacement, establish the transverse q/radius
sublevel, and place the entire ball in each cutoff and localization plateau.
Consequently the all-tube assembled-field transfer remains conditional.

The follow-up lemma `coordinateEta_margin_of_sqrt_axial_radius` proves that,
for `0<tau<=1`, an axial distance at most `c*sqrt(tau)` gives the margin
`|eta| <= |eta0| + c/(1-2h)`. The scaling follows from
`D=(1-2h)/2`, `D+h=1/2`, and `tau^h<=1`. It does not establish that a full
three-dimensional Euclidean ball meets the axial-distance premise.

### 2026-09-30: Euclidean-ball to eta-margin theorem

`coordinateEta_margin_of_euclidean_ball` now derives the axial-distance
hypothesis from a genuine Euclidean norm bound around the source trajectory's
axis center, using the coordinate projection bound in `EuclideanSpace`. Thus,
for every fixed `0<tau<=1`, every point in the full spatial ball of radius
`c*sqrt(tau)` has `|eta| <= |eta0| + c/(1-2h)`. This closes the ball-to-axial
step without a simulation or a continuum linearization assumption.

The theorem compiles against the pinned OpenAI source and Lean cache; its
axioms are only `propext`, `Classical.choice`, and `Quot.sound`. Reproducible
command and source/log hashes are recorded in
`evidence/openai-lean-2026-09-30-spatial-ball-clean/manifest.json`. It does not
yet establish transverse-radius, exterior-sublevel, cutoff, localization, or
time-window conditions for the assembled-field theorem. Therefore it is not
the promised whole cusp-tube field-equality result, and it adds no particle or
molecular conclusion.
