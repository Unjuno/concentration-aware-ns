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
open exterior, under explicit exterior, cutoff, localization, and late-time
hypotheses. The whole moving cusp-tube inclusion and its quantitative `tau0`
conditions are still not formalized in Lean, so this is not yet an end-to-end
tube theorem.

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

The theorem does not yet show that a whole `c*sqrt(1-t)` tube satisfies those
exterior and plateau hypotheses. The chart/ball inequalities in the previous
section remain hand-derived; they need formalization and connection to the
actual exterior domain before claiming a cusp-tube equality.

## Evidence boundary and next action

The algebraic chart identities were rechecked by
`work/reference-check-env/bin/python -m tools.check_support_hole_tube_geometry`;
the output is `evidence/tests/support-hole-tube-geometry.json`. That checker
does not prove the mean-value inequality or the whole-tube inclusion. Source
archive and checksum details are recorded in
`docs/support-hole-tube-geometry.md` and `GOAL.md`.

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
