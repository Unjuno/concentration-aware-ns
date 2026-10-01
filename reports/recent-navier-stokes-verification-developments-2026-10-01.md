# Recent Navier–Stokes verification developments (2026-10-01)

## A nearby method worth auditing

An arXiv preprint submitted 14 September 2026 claims computer-assisted global
regularity for specified continuous families of 3D periodic Navier–Stokes
initial data. It is not a theorem for arbitrary initial data and does not
contradict a finite-time blowup result for a different, forced problem. Its
method combines finite Fourier comparison paths, a common a-posteriori error
bound, and exact-rational checks of finite inequalities; it also claims a
uniform extension over a coefficient interval and infinitely many smooth
perturbation modes. The paper says it uses separate primary and independent
implementations and deliberate negative controls.

The potentially useful connection to this repository is methodological:
replace a sampled or globally coarse bound with a finite approximation plus a
rigorous enclosure of the whole untested set, then independently reconstruct
the finite checks. For our continuous peak question, this suggests testing
local/adaptive interval enclosures around candidate extrema and explicitly
covering the remaining domain. The preprint concerns global regularity of
solutions, however, while our current audit concerns a pointwise derivative
error in a manufactured benchmark; its result does not transfer directly.

The evidence is preliminary. The arXiv record lists a single-author v1
preprint, not a peer-reviewed publication. It says a permanent reproducibility
repository/DOI will be created before journal submission; the current arXiv
record does not link that package. Therefore its detailed calculations and
code have not been independently reproduced here. Treat the conclusions as
the author's claims pending artifact availability and independent audit.

## Relation to the OpenAI announcement and the user's hypothesis

OpenAI's public description frames its result as a singularity for a smooth,
externally forced 3D incompressible continuum flow, with finite energy. The
repository describes the Lean files as formalizations accompanying its
Navier–Stokes and Euler papers. Neither the announcement nor this newly found
preprint supplies evidence that molecular positions become ordered, that a
continuum singularity predicts particle trajectories, or that viscosity
collapses in a material above a speed threshold. Those would need a separate
model connecting continuum fields to kinetic/statistical mechanics and
experimental observables; they remain hypotheses, not consequences of these
PDE results.

## Sources checked

- OpenAI announcement: <https://openai.com/index/navier-stokes-solution/>
- OpenAI Lean repository: <https://github.com/openai/NavierStokesAndEuler>
- Preprint record: <https://arxiv.org/abs/2609.16157>
- Full preprint: <https://arxiv.org/html/2609.16157v1>

## Upstream feedback route

GitHub repository metadata was checked on 2026-10-01: the OpenAI repository
has GitHub Issues disabled and Discussions disabled, and GitHub reports no
open issues. There is therefore no issue/discussion channel in that repository
for a reproducible finding. This benchmark's own pull request remains on its
separate repository; no message was sent to OpenAI maintainers.
The raw metadata and decision are preserved in
`evidence/upstream-refresh/openai-navierstokes-feedback-surface-2026-10-01.json`.

## Newly posted profile-construction exposition (checked 2026-10-01)

A second, narrower source appeared in the latest search: Lei and Ren,
[Part I: Construction of Self-Similar Solutions with Admissible Stress and Flat
Remainder](https://arxiv.org/abs/2609.35406), submitted September 28 and revised
September 29 (v2). The abstract says it presents a readable account of the
profile-construction part, yielding a divergence-form residual plus a remainder
flat to infinite order on fixed similarity sectors. It explicitly says the
oscillatory-pulse residual cancellation is deferred to a companion Part II; the
comments call this an expository article that will not be submitted to a journal.

This is useful as a new explanatory source for the inner profile, but its own
scope and stated relationship to the OpenAI manuscript mean it is not an
independent verification of the entire force-correction/blow-up construction,
and it does not peer-review or certify the OpenAI proof. We have checked only
the arXiv metadata and abstract in this refresh, not the body derivations. No
benchmark theorem, solver verdict, or molecule/viscosity hypothesis changes.
Metadata notes are saved in
`evidence/upstream-refresh/lei-ren-profile-part1-2026-10-01.json`.

## Post-announcement analytical developments (checked 2026-10-01)

Two newer analysis preprints sharpen the mathematical picture, but neither is
an independent verification of the complete OpenAI construction. Cao, Chi,
and Nie's [*Density of Forces Producing Navier--Stokes Blowup*]
(https://arxiv.org/abs/2609.10262), v4 (22 September), takes the compact,
smoothly forced blow-up solution as an input and proves a density result for
forces in a specified relative `L^1_t H^s_x` topology when `s < 1/2`.
This is a consequence conditional on that starting construction; it is not a
second derivation of the construction itself.

Constantin, Ignatova, and Vicol's [*Regularity of asymptotically axisymmetric
solutions to the 3D Navier--Stokes equations with analytic forcing*]
(https://arxiv.org/abs/2609.20803), v2 (29 September), proves regularity at a
putative singular point under joint assumptions including real-analytic
forcing, anisotropic Type-II bounds for the angular mean, and an exactly
axisymmetric shrinking core. Their source comparison says the OpenAI
construction has the latter geometric properties and a smooth, bounded-`C²`
force. Conditional on the comparison and the claimed singular construction,
the force cannot be real-analytic in the stated local-uniform sense. This is
not a contradiction: smoothness does not imply analyticity, and the OpenAI
manuscript claims a `C∞` force. The paper also derives nonvanishing-on-every-
neighborhood consequences from stated profile geometry; these give no
quantitative lower bound on forcing amplitude.

The OpenAI announcement itself describes Navier--Stokes as a continuum model
and says that a singularity would mark breakdown of that model, after which
individual-particle tracking would be needed to continue modeling. This
motivates a precise open modeling question—what kinetic or particle system,
limit, and observables could continue a given continuum solution—but supplies
no such bridge. In particular, the shrinking vortex core and fine oscillatory
pulses in the continuum construction do not establish molecular ordering,
deterministic molecular positions, optical-fluid behavior, a phase transition,
or a speed-triggered viscosity collapse. Those remain separate hypotheses
requiring a defined microscopic model and independently testable predictions.

The scope above was checked against the arXiv version records/abstracts and
relevant stated theorem assumptions, plus the OpenAI announcement and paper.
It is a literature and assumption audit, not a line-by-line independent proof
review. These results motivate no new CFD solver defect report or simulation
run by themselves.

## SU2 Discussion #2890 follow-up (checked 2026-10-01)

The discussion now includes a second-order dual-time control. The pinned
v8.5.0 run reports observed endpoint orders `0.87905, 0.94267` for the
original old-time source evaluation and `1.99408, 1.99998` for a diagnostic
time-shift intervention, with all configured residual thresholds passing.
The post explicitly limits this to a causal reproducer, not a general fix or
a fresh current-master executable. The maintainer reply cautions that the
physical-time variable also feeds verification errors and time-dependent
boundary states, and recommends separating stored-state and target/solution
time semantics before changing it globally. This is a concrete temporal
verification/documentation candidate; multizone, restart, moving-grid, and
broader time-scheme behavior remain open.

The live GitHub GraphQL record checked at 2026-10-01 14:24 UTC now shows the
discussion closed on 30 September but `isAnswered=false`. Its visible content
still contains the maintainer's time-level analysis and the BDF2 follow-up; no
code change or general fix is recorded there. SU2 `master` remains at the
previously checked source commit. The thread status therefore changes the
follow-up channel, not the technical conclusion.
