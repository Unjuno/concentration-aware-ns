# Follow-up literature: forcing structure and finite-grid observability

Date checked: 2026-10-03. This is a source audit of recent preprints, not an
independent verification of their theorems or of the OpenAI construction.

## Results found

Constantin, Ignatova and Vicol, arXiv:2609.20803v2 (revised 2026-09-29), prove a
conditional regularity theorem for suitable weak 3D forced Navier–Stokes
solutions. Their hypotheses combine (a) a force uniformly bounded in spatial
`C^2` up to the proposed singular time and spatially real-analytic on compact
preterminal time cylinders, (b) stated anisotropic Type-II bounds on the
angular mean of the velocity and its derivatives, and (c) exact axisymmetry on
a positive-radius core at each preterminal time. Under all these hypotheses,
the point is regular. Their appendix says the OpenAI construction satisfies
(b) and (c), while its force is smooth and uniformly `C^2` but not spatially
analytic near the proposed point; this is consistent with, and does not
contradict, their theorem. They explicitly state that they do not independently
verify the OpenAI construction and derive the needed properties from that
manuscript. We therefore record this as a conditional structural result, not
as validation of either proof. The assumptions and conclusion are in the
[primary arXiv text](https://arxiv.org/html/2609.20803v2), Theorem 1.1 and
Appendix A.6.

Cao, Chi and Nie, arXiv:2609.10262v4 (revised 2026-09-22), study density of
smooth forces producing classical breakdown. On the torus, for fixed viscosity
and terminal time, their Theorem 3.1 states density in relative
`L^1_t H^s_x` for every fixed admissible smooth initial velocity when `s < 1/2`;
for zero initial velocity it gives an if-and-only-if threshold, with
non-density for `s >= 1/2`. Their whole-space theorem gives the corresponding
threshold `1/2` for `L^1_t H^s_x` and `-1/2` for `L^2_t H^s_x`. Their method
inserts a rescaled singular packet while changing the force. This is density
in specified function-space topologies, not a probability, prevalence, or
engineering-realizability statement. The [primary arXiv text](https://arxiv.org/html/2609.10262v4)
states the torus result in Theorem 3.1 and the whole-space result in Theorem
4.1.

The same paper's Theorem 4.7 is directly relevant to how finite-grid evidence
should be worded: for any fixed finite family of complete uniform Cartesian
grids, it constructs a comparison whose velocity and force cell averages
match on every cell at every preterminal time, even though the glued solution
has unbounded terminal velocity. The construction's perturbation depends on
the chosen finite grid family and develops larger amplitudes and derivatives
as its support shrinks. The authors explicitly limit the conclusion to the
information in those prescribed averages, not convergence under refinement
for one fixed smooth problem. It therefore motivates documenting the
benchmark's observables and exact-solution scope, but it does not invalidate
our fixed manufactured-solution consistency/convergence studies and does not
show that any solver has a defect.

## Consequences for this benchmark

- Keep continuum claims separate from finite-grid acceptance. Report exact
  reference agreement and resolution trends only for the frozen manufactured
  solution, discretization, and observables; do not infer that finite grids
  settle behavior of every nearby smooth forced flow.
- Keep forcing regularity visible in the case manifest. An analytic
  manufactured force exercises a different regularity class from the smooth,
  nonanalytic force described in the OpenAI construction. This is a scope
  distinction, not evidence that the current case is invalid.
- The density result does not imply that singular behavior is typical or that
  a physically admissible force can realize it at bounded amplitude, bandwidth,
  or derivative norms. The analytic-forcing theorem also has several
  simultaneous structural hypotheses; it is not a generic prohibition on
  smooth forcing.
- These papers provide no reproduced OpenFOAM, SU2, or PhysicsNeMo defect and
  do not justify an upstream issue. No report was filed. They also do not
  support particle alignment, a viscosity-law change, or material hazard.

## Status and source limits

Both works were consulted as arXiv preprints; no peer-review status is asserted
here. The results build on the OpenAI construction as a mathematical input, and
this audit has not replayed their proofs or checked the linked Lean project.
Their source statements are nevertheless useful for delimiting what numerical
and physical conclusions this benchmark can responsibly draw.
