# Navier–Stokes blow-up follow-up scan (2026-10-02)

## Scope and cutoff

This is a targeted literature and upstream-repository scan after OpenAI's
2026-09-08 announcement, not a proof review. Sources were checked on
2026-10-02. The arXiv papers below are preprints; their claims are reported as
claims, not as peer-reviewed consensus. The OpenAI Lean repository currently
shows two commits, dated 2026-09-08 and 2026-09-10; the latter is
`f9e8bc5b38b6`. Its README describes forced incompressible Navier–Stokes
alternatives on both R3 and the periodic torus, and an unforced Euler result.
The repository page does not expose a normal Issues tracker, so this scan does
not interpret an unavailable issue endpoint as evidence that no concerns exist.

## Developments relevant to this benchmark

1. **A structural regularity constraint (Constantin–Ignatova–Vicol,
arXiv:2609.20803, v2 dated 2026-09-29).** The authors assume an analytic body
force and two structural properties attributed to the OpenAI construction:
anisotropic Type-II bounds for the angular mean and exact axisymmetry in the
collapsing core. Under those hypotheses they prove regularity at the proposed
singular point. Their stated consequence is that a construction with those
properties and force bounded in C2 up to blow-up cannot have force identically
zero near the singular point and cannot have force real-analytic in space,
locally uniformly in time. This is a substantive necessary-structure result,
not a direct contradiction: the OpenAI announcement describes a smooth force,
not an analytic one. It motivates checking the actual force's regularity,
spatial analyticity, and behavior near the core before any numerical proxy is
interpreted as physically realizable.

2. **An accessible profile-construction exposition (Lei–Ren,
arXiv:2609.35406, v2 dated 2026-09-29).** Part I rewrites the self-similar
profile construction and states that substitution leaves a divergence-form
stress plus a remainder flat to infinite order on fixed similarity sectors.
It is an exposition of the OpenAI manuscript, not an independent full proof
check; it explicitly leaves residual correction by oscillatory pulses to a
companion Part II. This reinforces that the forcing/stress balance and the
full residual correction are central audit objects. It does not establish
that a conventional CFD trajectory resolves or validates the continuum proof.

3. **A numerical similarity-profile study (Duraiswami, arXiv:2609.17642,
2026-09-15).** This study recasts a related swirl profile in the announced
similarity variables and reports symbolic/manufactured/exact-solution checks
and parameter sweeps. Its abstract also reports unresolved resolution
stability for the Dirichlet axis problem, non-symmetric core flow needed for
moment constraints, nonconvergent spectra in some strong-swirl cases, and
physical limits (cavitation in water or shocks in air) occurring first. The
author explicitly says the study does not show reachability in flows one can
compute or build. This is a useful independent numerical-methods lead, but it
is one preprint's exploratory result, not independent certification of the
OpenAI theorem or an engineering hazard finding.

4. **A separate neural-forcing preprint (Li, arXiv:2609.23934,
2026-09-20).** Its abstract proposes neural forcing discovery plus independent
fixed-force replay and a continuum certification argument. Because this is a
single recent preprint and its own abstract makes a strong proof claim, treat
it as a candidate for a separate mathematical audit, not as corroboration
until hypotheses, theorem dependencies, code/data, and independent checking
are examined.

The OpenAI announcement itself explicitly describes Navier–Stokes as a
continuum model and says that if the continuum model breaks down, a different
microscopic model would be needed to continue. That statement does not imply
molecular alignment, a particle-position distribution, or a drop in
constitutive viscosity. The PDE blow-up claim supplies no molecule-resolved
trajectory or constitutive law. Any such bridge would require a specified
kinetic/molecular model, a scale map, and independent evidence.

## Consequence for the repository's next experiments

The current benchmark is still the right narrow question: can standard
numerical acceptance pass while a predeclared local quantity remains
resolution-sensitive? The n16/n32/n64 AMR replay is exploratory and has no
preregistered quality threshold, so it remains UNCERTAIN and does not show an
upstream defect. A follow-up inspired by the new literature should first be a
separate, reproducible **forcing audit**: extract the published forcing and
self-similar scales; check divergence, smoothness class, C2 bounds, local
analyticity/non-vanishing conditions, and the exact validity region; then
compare sampled CFD diagnostics only where the target continuum fields and
forcing are fully specified. Do not convert a numerical residual, failed
axis discretization, or preprint abstract into a claim against OpenAI or a
solver vendor.

## Sources

- OpenAI announcement, 2026-09-08: <https://openai.com/index/navier-stokes-solution/>
- OpenAI Lean repository: <https://github.com/openai/NavierStokesAndEuler>
- Constantin, Ignatova & Vicol, arXiv:2609.20803: <https://arxiv.org/abs/2609.20803>
- Lei & Ren, arXiv:2609.35406: <https://arxiv.org/abs/2609.35406>
- Duraiswami, arXiv:2609.17642: <https://arxiv.org/abs/2609.17642>
- Li, arXiv:2609.23934: <https://arxiv.org/abs/2609.23934>
