# Audit of the attached benchmark proposal (2026-10-04)

## Decision

The proposal is a useful hypothesis map, not evidence that any solver hides a
singularity or that a real fluid undergoes molecular ordering or a viscosity
transition. Existing benchmark evidence partly realizes its narrowest test:
OpenFOAM's frozen standard gate passes while its sampled local-quality gate
fails on the two coarsest meshes. The preregistered persistent discrepancy at
the two finer spatial levels is **not observed**. SU2 has no case that passes
the complete conventional accuracy/residual conjunction and fails the sampled
local gate. PhysicsNeMo remains **uncertain** beyond its frozen sampled
comparison: v2 prospectively applied shared cross-target tolerances, but those
limits are not PhysicsNeMo-specific calibration, continuous-field bounds, or
an optimizer-convergence certificate.

The distinction matters: the narrow coarse-grid counterexample supports
reporting local observables beside ordinary gates. It does not establish a
general acceptance defect, a persistent fine-grid failure, or a physical
singularity mechanism.

## H / T / D / C / U review

| Proposal item | Evidence-based status | What it supports |
|---|---|---|
| H: ordinary acceptance can miss local concentration | **Observed narrowly** for OpenFOAM Foundation 13: standard acceptance passes all six archived uniform cases, while sampled local quality fails at n=16 and n=32 and passes at n=64, n=128, and both finer temporal cases. The preregistered n=64/n=128 persistent-blind-spot criterion is `NOT_OBSERVED`. | Keep aggregate and local gates separate; do not label a general solver defect. The local metric is sampled and is not a certified continuous maximum. |
| H: the same blind spot appears in SU2 | **Not observed** in the five-archive v8.5.0 review. n=16 passes inner residual but fails velocity and energy accuracy; n=64 passes aggregate accuracy but misses the all-step inner-residual threshold on 2, 3, or 7 steps. No frozen case passes the complete standard conjunction while failing local sampled accuracy. | Residual, aggregate accuracy, and local derivatives need separate reporting. Current data do not justify a cross-solver defect claim. |
| H: average TKE can hide local PhysicsNeMo error | **Not observed under the frozen sampled v2 policy; continuous-domain status remains unresolved.** A shared cross-target policy was frozen before independent evaluation: 19/25 models pass all six sampled metrics, six fail only velocity L2, and all 25 pass the sampled local metrics. | The v2 archive does not reproduce a sampled global-pass/local-fail blind spot. Its common engineering tolerances are not a PhysicsNeMo-specific calibration; finite-grid extrema, broader held-out regions, seed-population behavior, and optimizer convergence remain unestablished. |
| OpenFOAM `maxCells` / `maxRefinement` saturation is an upstream bug | **Not established.** One pinned Foundation 13 case reproduces whole-level refinement overshoot of `maxCells=5000` (4,096 initial cells; 1,792 selected; 16,640 resulting cells). The inspected selection path implements an approximate cap; this is not a reproduced contract violation. AMR quality attribution remains `UNCERTAIN`. | Record budget limits and realized mesh sizes; report no duplicate issue from this observation. |
| `residualControl` is a local-error certificate | **Rejected as an equivalence.** Residual convergence and solution/local-QoI accuracy are distinct measurements. The benchmark correctly computes them separately. | A residual pass alone must not be presented as an accuracy certificate. |
| Smooth manufactured solution first, singular construction later | **Supported as a verification design choice.** The manufactured solution has an independent analytic reference and source; it isolates numerical verification from the proposed singular construction. | Keep the staged boundary: smooth MMS results do not validate an OpenAI construction or physical extrapolation. |
| PINN theory or 3D control theory proves an engineering hazard | **Unsupported transfer.** The cited mathematics has explicit regularity, smallness, and local-stability hypotheses. No named product or deployed controller has been linked to those assumptions here. | Preserve as a literature question; make no product-safety claim absent an implementation and reachability bridge. |
| Molecular alignment, phase transition, or viscosity change follows from the blow-up theorem | **Not established as an implication.** Related shear-induced orientation and shear thinning are documented for specific liquid-crystalline/polymer materials, but those observations use material-specific microscopic or constitutive physics absent from this constant-viscosity continuum theorem. | Keep this as a separate testable material hypothesis. It requires a named material, local shear/strain history, an orientation observable and a constitutive link; generic inference from a diverging continuum velocity is unsupported. |

## Upstream disposition

No new solver issue is justified from this proposal audit. The OpenFOAM
`maxCells` behavior matches the documented approximate whole-level selection
path, and the local-quality attribution remains uncertain. SU2's relevant
source-time discussion, maximum-residual-location request, and time-dependent
boundary-condition issue already exist. PhysicsNeMo's derivative-boundary
concerns are already tracked and do not apply to this periodic/autodiff path;
its odd-width spectrum issue has its own issue and PR. Current contribution
policy and bounded overlap searches are recorded in the dated upstream audits.

This is a claim audit against the repository's archived evidence, not an
exhaustive inventory of every upstream issue. A scoped live metadata refresh
on 2026-10-04 found no new overlap or reportable benchmark finding: OpenFOAM
Foundation 13 and SU2 default-branch SHAs were unchanged; PhysicsNeMo's
default-branch SHA matched the already inspected 2026-10-02 state. The newly
opened PhysicsNeMo #2042 concerns nonuniform-bin Wasserstein CDF integration,
outside the audited periodic gradient/spectrum paths. SU2 #2353 and #2932,
PhysicsNeMo #2001 and #2007, and PRs #1853 and #2008 retain their recorded
states; discussion #2890 remains closed without an accepted answer. OpenAI's
reference repository still has issues and discussions disabled. No upstream
post was made. Exact metadata, license-file and contribution-template checks,
and the live SU2 run state are in
`evidence/upstream-refresh/live-status-2026-10-04T0646Z.json`.

A follow-up source review covers OpenAI's September 2026 theorem and a new
September 15 arXiv investigation of its leading-order physical bridge. That
preprint estimates cavitation/compressibility cutoffs before molecular scales,
but leaves the full finite-viscosity forced evolution and stress realization
open; it reports no molecular-alignment or viscosity-collapse result. See
`reports/openai-ns-blowup-physical-bridge-audit-2026-10-04.md` for the scoped
assessment and its limitations.

## Primary evidence in this repository

- `reports/openfoam-six-case-matrix-independent-replay-2026-10-01.md`
- `reports/openfoam-amr-stage-snapshot-v3-2026-10-01.md`
- `reports/su2-localized-residual-upstream-audit-2026-10-02.md`
- `reports/physicsnemo-seed-control-v1.md`
- `reports/physicsnemo-upstream-derivative-audit-2026-10-02.md`
- `reports/recent-developments-and-hypothesis-audit-2026-09-28.md`
- `reports/upstream-disposition.md`

## Live upstream metadata refresh

At 2026-10-03 23:55 UTC, the OpenFOAM Foundation 13 default branch still pointed
to `18870c24…`; its four open issues were unrelated to the exercised AMR path.
SU2 `master` remained `bc154666…`; issue #2353 and #2932 remained open, while
discussion #2890 remained closed without an accepted answer. PhysicsNeMo `main`
had advanced to `b45a5c81…`; issues #2001/#2007 remained open and PRs #1853/#2008
remained open (with #1853 still draft). These records preserve existing
overlap; they do not warrant a duplicate issue. The refresh is intentionally
metadata-scoped and is not a source audit of PhysicsNeMo's new commits. Exact
responses and the then-live SU2 job state are recorded in
`evidence/upstream-refresh/live-status-2026-10-03T2355Z.json`.

A second authenticated GitHub REST refresh at 2026-10-04 11:36 UTC records the
current default-branch commits and the relevant open/closed upstream records
in `evidence/upstream-refresh/live-status-2026-10-04T1137Z.json`. OpenFOAM
issue #2 already covers the two-phase viscosity-contrast topic. SU2 discussion
#2890 is closed while #2353 and #2932 remain open. PhysicsNeMo issues #2001 and
#2007 and PRs #1853/#2008 remain the relevant tracked reports; the new #2044
concerns a histogram CRPS dimension bug and is unrelated. The OpenAI formal repo
still disables Issues and Discussions. These checks reveal no new reproducible
software defect, so no duplicate upstream post was made.
