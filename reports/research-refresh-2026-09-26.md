# Research refresh — 2026-09-26

This is a primary-source literature and repository refresh, not independent
verification of the new papers. The existing benchmark and Lean results retain
their original pins. Search snippets were checked against current landing pages;
one search result described an older, subsequently withdrawn paper.

## Directly relevant follow-up work

- Constantin, Ignatova and Vicol, September 17:
  [Regularity of asymptotically axisymmetric solutions](https://arxiv.org/html/2609.20803v1).
  Theorem 1.1 assumes a suitable weak solution, uniform spatial C2 forcing bounds,
  spatially analytic forcing locally uniformly on compact time intervals,
  anisotropic Type II derivative bounds on the angular mean, and exact axisymmetry
  in a shrinking core. It concludes regularity. This is a restriction on this
  mechanism under extra hypotheses, not a refutation of a merely smooth-forced
  construction. Our next comparison must explicitly distinguish smooth from
  analytic forcing and verify every hypothesis before applying the result.

- Duraiswami, September 15:
  [Self-similar swirl between contracting porous walls](https://arxiv.org/html/2609.17642v1).
  Section 2 retains radial viscosity in the leading balance while axial viscosity
  is smaller by q^(2h). This agrees in scaling with our derivative calculation,
  but does not verify our particular pressure sign or actualProfile corollary.
  Its numerical boundary-value problem is not the entire OpenAI construction.
  Treat its physical reachability discussion as the author's analysis, not an
  independently established molecular or phase-transition result. Compare the
  operators in equations (3)–(4) before considering reproduction of its code.

- Cao, Chi and Nie, current September 22 version:
  [Density of Forces Producing Navier–Stokes Blowup](https://arxiv.org/abs/2609.10262v4).
  The abstract claims density of breakdown-producing smooth forces in relative
  L1-time Hs-space topology exactly for s<1/2, on the torus and whole space.
  It varies the force while preserving initial velocity. This is relevant to
  the topology of error measurements, but does not establish failure of our
  fixed-force manufactured benchmark or a particular solver. The listing links
  a Lean project, which we have not checked. Version 3 combines earlier work;
  version 4 changes abstract metadata without changing the manuscript.
  [2609.10269](https://arxiv.org/abs/2609.10269) is withdrawn; do not use its old
  search snippet as a current independent result.

- [Clay's September 11 statement](https://www.claymath.org/news/navier-stokes-announcement/)
  acknowledges the apparent resolution and describes a deliberately unhurried
  evaluation process. This statement is not a prize award or our verification.

## Repository changes and action

GitHub main is now f9e8bc5b38b6e212696e8a30e3e91517af887bbd, dated September 10,
one commit after our 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538 pin. The compare
API returns 188 changed-file entries, including the PaperResults import and
additional bound/theorem modules. See `evidence/upstream-refresh/openai-2026-09-26.json`.
This is substantial enough to require a separate compatibility/build audit;
the prior successful kernel run must not be relabeled as verification of main.

Targeted inspection of the new FinalSlowBase.ProfileData and actualProfile still
shows the same choice pattern without a stored pressure amplitude lower bound.
This does not settle whether new modules provide another route to our local
pressure threshold. Inspect those dependencies before repeating the old proof
search. The current three solver heads are inventoried separately; their change
impact has not yet been reviewed and no existing numerical verdict is upgraded.

Next priorities: audit the new source pin against our extension; compare the
radial/axial viscous operators with Duraiswami; read the density theorem's exact
norms and hypotheses; then map these results to the benchmark's measurement
limitations. No new upstream defect report is justified by this refresh alone.

## Independent operator comparison

`python -m tools.check_similarity_operators` in the verification environment now
checks Duraiswami's equations (1), (3) and the scalar radial operator of (4b)
against implicit differentiation of physical coordinates. Inverting the
(t,z,r²) Jacobian independently reproduces both time and axial chain rules.
A second axial derivative scales as q^(b-2D), while the radial scalar Laplacian
is 2 q^(b-1) (f_X+X f_XX). Their power difference is 2h. SymPy 1.14.0 checks
all identities exactly; evidence is in `evidence/tests/similarity-operators.json`.

This confirms the coordinate/operator comparison, not the paper's numerical
branches or physical predictions. The radial coefficient can still vanish,
and controlling profile derivatives remains necessary. In particular this does
not discharge the pressure threshold for our actualProfile. The distinction
between declining axial viscosity and declining total viscous force is retained.
