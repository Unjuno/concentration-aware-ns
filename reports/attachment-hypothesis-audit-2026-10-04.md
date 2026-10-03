# Audit of the attached benchmark proposal (2026-10-04)

## Decision

The proposal is a useful hypothesis map, not evidence that any solver hides a
singularity or that a real fluid undergoes molecular ordering or a viscosity
transition. Existing benchmark evidence partly realizes its narrowest test:
OpenFOAM's frozen standard gate passes while its sampled local-quality gate
fails on the two coarsest meshes. The preregistered persistent discrepancy at
the two finer spatial levels is **not observed**. SU2 has no case that passes
the complete conventional accuracy/residual conjunction and fails the sampled
local gate. PhysicsNeMo remains **uncertain** because its local checks are
sampled, its seed effects matter, and no solver-specific acceptance threshold
was preregistered.

The distinction matters: the narrow coarse-grid counterexample supports
reporting local observables beside ordinary gates. It does not establish a
general acceptance defect, a persistent fine-grid failure, or a physical
singularity mechanism.

## H / T / D / C / U review

| Proposal item | Evidence-based status | What it supports |
|---|---|---|
| H: ordinary acceptance can miss local concentration | **Observed narrowly** for OpenFOAM Foundation 13: standard acceptance passes all six archived uniform cases, while sampled local quality fails at n=16 and n=32 and passes at n=64, n=128, and both finer temporal cases. The preregistered n=64/n=128 persistent-blind-spot criterion is `NOT_OBSERVED`. | Keep aggregate and local gates separate; do not label a general solver defect. The local metric is sampled and is not a certified continuous maximum. |
| H: the same blind spot appears in SU2 | **Not observed** in the five-archive v8.5.0 review. n=16 passes inner residual but fails velocity and energy accuracy; n=64 passes aggregate accuracy but misses the all-step inner-residual threshold on 2, 3, or 7 steps. No frozen case passes the complete standard conjunction while failing local sampled accuracy. | Residual, aggregate accuracy, and local derivatives need separate reporting. Current data do not justify a cross-solver defect claim. |
| H: average TKE can hide local PhysicsNeMo error | **Unresolved.** Five seeds per case show mixed spatial contrasts and sampled velocity versus derivative metrics can disagree, but continuous extrema are uncertified and no PhysicsNeMo-specific threshold was preregistered. | The proposed diagnostic set is sensible research instrumentation. The current archives cannot establish a formal pass/fail blind spot. |
| OpenFOAM `maxCells` / `maxRefinement` saturation is an upstream bug | **Not established.** One pinned Foundation 13 case reproduces whole-level refinement overshoot of `maxCells=5000` (4,096 initial cells; 1,792 selected; 16,640 resulting cells). The inspected selection path implements an approximate cap; this is not a reproduced contract violation. AMR quality attribution remains `UNCERTAIN`. | Record budget limits and realized mesh sizes; report no duplicate issue from this observation. |
| `residualControl` is a local-error certificate | **Rejected as an equivalence.** Residual convergence and solution/local-QoI accuracy are distinct measurements. The benchmark correctly computes them separately. | A residual pass alone must not be presented as an accuracy certificate. |
| Smooth manufactured solution first, singular construction later | **Supported as a verification design choice.** The manufactured solution has an independent analytic reference and source; it isolates numerical verification from the proposed singular construction. | Keep the staged boundary: smooth MMS results do not validate an OpenAI construction or physical extrapolation. |
| PINN theory or 3D control theory proves an engineering hazard | **Unsupported transfer.** The cited mathematics has explicit regularity, smallness, and local-stability hypotheses. No named product or deployed controller has been linked to those assumptions here. | Preserve as a literature question; make no product-safety claim absent an implementation and reachability bridge. |
| Molecular alignment, phase transition, or viscosity collapse follows | **Unsupported.** The continuum CFD and PINN observables here do not resolve molecules or identify a constitutive law. | No physical inference follows from these benchmark errors. |

## Upstream disposition

No new solver issue is justified from this proposal audit. The OpenFOAM
`maxCells` behavior matches the documented approximate whole-level selection
path, and the local-quality attribution remains uncertain. SU2's relevant
source-time discussion, maximum-residual-location request, and time-dependent
boundary-condition issue already exist. PhysicsNeMo's derivative-boundary
concerns are already tracked and do not apply to this periodic/autodiff path;
its odd-width spectrum issue has its own issue and PR. Current contribution
policy and bounded overlap searches are recorded in the dated upstream audits.

This is a claim audit against the repository's archived evidence, not a fresh
exhaustive inventory of every upstream issue or current default-branch commit.
The last scoped three-project inventory is dated 2026-10-02; refresh live
metadata before any new external report.

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
