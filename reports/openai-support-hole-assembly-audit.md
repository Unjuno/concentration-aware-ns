# Source audit: inner-hole transfer toward the selected OpenAI field

Audit date: 2026-09-28. Source: `openai/NavierStokesAndEuler` commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. This is an analytical source audit plus a separately compiled Lean extension.
It is not a numerical simulation result or a physical/molecular conclusion.

## Result

The selected construction exposes a source-level route from the common
primitive support hole to equality of the final activated periodic velocity
with its smooth base on a sufficiently thin terminal cusp tube. The initial
copy and mean terms are covered by the same hole; they are not an independent
obstruction. Existing source lemmas cover local finiteness of the selected
potential sum, curl/local derivative transfer, and outer spatial/time
localization. The aggregate velocity transfer is now checked in a local Lean
extension: `verification/SupportHoleAssembly.lean` proves eventual equality
of the final activated periodic candidate and its smooth base on the actual
open exterior, then derives an existential terminal interval on which this
equality holds throughout each shrinking Euclidean cusp ball. Conditions on
the axis parameter, radius coefficient, eta margin, and annulus interior stay
explicit; `tau0` is existential, not numerically estimated.

## Inner-hole to active-annulus exterior

Let `L=PrimaryTargetBounds.leftRadius`, let `q` be the similarity chart
coordinate, and let `r` be the physical transverse radius. The source defines
the active annulus by

    r²/(2q) ∈ [activeLeft, activeRight],   activeLeft=L²/2.

The common primitive coefficient is

    c0 = min(L/(4*sqrt(2)), patch.a/4) > 0.

If `r<c0*sqrt(q)`, then

    r²/(2q) < c0²/2 <= L²/64 < L²/2 = activeLeft,

so the point lies outside the closed active annulus. The inequality is strict,
so it remains true on a neighborhood of any point satisfying the tube bound.
The Lean extension now converts this physical-radius inequality to the actual
open exterior membership and then to final-field equality, provided `q<Q_res`
and the stated cutoff/localization/time plateaus hold.

Outside this active annulus and within the actual exterior sublevel
`q<Q_res`, where `Q_res=ChartScales.Q(residualBand B N0)`, the selected-source
audit identifies these zero results. The source has `qbig=2*Q_res`; the looser
`q<qbig` condition alone is insufficient for the checked exterior theorem:

- `initialPotential_exterior` kills the initial copy plus initial stream mean;
- `initialDirect_exterior` kills the initial angular mean;
- positive particular, signed, and mean stages have zero values/germs;
- pressure exterior statements exist too, though pressure is not needed for
  the velocity equality discussed here.

Thus stage zero is the gauge-fixed base potential on this region, while all
positive potential and direct stages vanish locally.

## Whole-tube geometry and cutoff conditions

For `tau=1-t`, the chart relation gives `tau=q*(1-eta²)`. Around the selected
axis curve parameterized by `eta0`, set `d=1-eta0²`,
`delta=(1-|eta0|)/2`, and `s0=1-(|eta0|+delta)²`. The chart then gives
`tau<=q<=tau/s0` throughout a sufficiently narrow tube. A radius
`c*sqrt(tau)` obeys `r<=c*sqrt(tau)<c0*sqrt(q)` whenever `c<c0`.

The chart upper-bound step is now Lean-checked as
`physicalQ_le_of_eta_margin`: a uniform normalized-coordinate margin
`|eta|<=beta<1` implies `q<=tau/(1-beta^2)`. The remaining geometry proof
must derive that margin uniformly on every point of the moving ball.

The geometry note derives the remaining whole-ball conditions. In particular,
`tau<s0*Q_res` places the tube in the exterior sublevel required by the
checked theorem;
`tau<s0/(2*max(1,(a(0):ℝ)))` ensures `a(0)*q<1/2`, so the zeroth cutoff is identically one;
`tau<1/4` activates the late-time field; and smallness conditions on `c*sqrt(tau)`
and the center's axial coordinate place the tube inside the spatial
localization plateau. Since all constants are positive and `a(0)` is finite,
these conditions hold for some existential `tau0>0`. They do not produce a
numerical value of `tau0` or `c`.

## Assembly route and checked exterior theorem

At each point of the actual open exterior, the selected construction has
exterior identities for stage zero, all positive potential stages and all
direct stages. The extension `verification/SupportHoleAssembly.lean` composes
these with cutoff local finiteness, zeroth-cutoff plateau, spatial curl,
`finalPotential_sameCurl`, periodic spatial localization and late-time
activation. Its theorem gives eventual equality of the final activated
velocity and the selected smooth-base velocity on that open exterior, under
explicit hypotheses. It compiled with the pinned Lean and dependency versions.

The extension now proves `selected_velocity_germ_on_cusp_tube`: for fixed
`eta`, `c>0`, and `beta<1` satisfying the explicit eta-margin and strict
active-annulus interior conditions, there is an existential `tau0>0` such that
for every `0<tau<tau0` and every point in the Euclidean ball of radius
`c*sqrt(tau)` around the selected axis center, the actual activated field has
the selected smooth-base velocity germ. The proof derives the center bound by
continuity at `tau=0` and combines the finitely many geometric, cutoff, and
localization thresholds. A separate checked lemma proves that admissible
positive `c` and `beta` exist for every fixed `eta∈(-1,1)`. The pinned Lean run
and axiom audit are recorded in
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/manifest.json`.

This is a continuum local-germ equality on a shrinking ball, under stated
conditional parameters. It is not an endpoint value, a finite-size packet
estimate, or a statement about particle alignment, molecular determinism,
phase transition, or viscosity.

The follow-on Lean audit proves that the entire moving ball eventually enters
any prescribed endpoint neighborhood, then transfers the upstream actual-base
rate to obtain an existential full-spacetime second-jet bound
`C*q^(-40)` throughout that ball. The new v6 manifest records this exact scope
and the permitted axiom set. The local `ContDiffAt` spatial-jet restriction is
now composed with the selected-field cusp-ball Hessian result in
`verification/SpatialHessianTransfer.lean`; both declarations' Lean elaboration
and axiom results are recorded in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`. The
nonlinear packet comparison remains outside Lean, so `Cstretch+39` is still a
conditional shrinking-packet inference, not a Lean packet theorem or numerical
certificate.

## Evidence boundary and next action

The algebraic chart identities were rechecked by
`work/reference-check-env/bin/python -m tools.check_support_hole_tube_geometry`;
the output is `evidence/tests/support-hole-tube-geometry.json`. The mean-value,
ball inclusion, all-plateau, and assembled-field implications are now covered
by the pinned Lean extension. The symbolic checker remains an independent
algebraic cross-check only. Full pinned proof and source-archive details are in
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/` and `GOAL.md`.

## Independent proof-term check — 2026-10-01

The v6 cusp-ball/Hessian extension was exported with the pinned lean4export
tool and checked by nanoda in the digest-pinned checker image, with networking
disabled and the unprivileged user. Nanoda checked 85,487 declarations with
zero typechecker errors. It reported one pretty-printer error,
`Unable to print axioms`; separately, the Lean run printed and checked the
permitted axiom list for each of the ten selected declarations. The exact
source/image hashes, declaration list, output hashes, logs, and reproduction
script are indexed in
`evidence/lean-verification/support-hole-nanoda-2026-10-01.json` and
`runtime/lean-verification/check_support_hole_nanoda.sh`. The 906 MiB exported
NDJSON is retained locally under `work/` and identified by hash rather than
committed. This adds independent proof-term checking, not independent
validation of OpenAI's mathematical construction or a finite-packet,
molecular, or constitutive conclusion.

No implication is drawn here about molecular ordering, absolute-position
certainty, finite-size packets at the singular endpoint, a phase transition,
or reduced viscosity. The audited continuum deformation remains
volume-preserving and anisotropic.

## Pinned source file hashes

Hashes below were calculated from the archived commit tree:

| File | SHA-256 |
|---|---|
| `NavierStokes/ActualPolarCoverage.lean` | `5a200c8e0c23011bb09ff0bc33b90753abacd4b02e34f927a48bfb8a954a83e7` |
| `NavierStokes/ActualCandidateAssembly.lean` | `bba2f74a938039caec486ca6a35576efd21e6fe35c1ba695e4d21609d89b8a94` |
| `NavierStokes/ActualMeanExterior.lean` | `f9c1d7e1fd4e659185f580112b45941c72c09c54cc92210a07d23764b9ef77ea` |
| `NavierStokes/ActualCurrentWaveSupport.lean` | `bfe9d89941842402ffd89e18eee0074f0e66e24ddc0bc3c5dd8e984576827bfb` |
| `NavierStokes/ActualMeanStageData.lean` | `7195488e5bed2a1261067ff7e997c7b1ce230747b235b9178c53da3a7184b471` |
| `NavierStokes/SolenoidalDiagonal.lean` | `548b6292d7e41f434ec996ee2d6ee683c526339422da18ff9ee96a93486329c7` |
| `NavierStokes/SpatialLocalization.lean` | `62afe29ed1dffe71e178784b76b5ea4cc965b1d2ca854602d982210e2de94785` |
| `NavierStokes/TimeLocalization.lean` | `295de27f11ba189b9bd1263dc6571f7410947b3e6de1106d55f05440fdb79a70` |
