# Research refresh: new exposition of the OpenAI Navier–Stokes profile construction

Date checked: 2026-10-03

## New source

Zhen Lei and Xiao Ren, *Finite-Time Blowup for Navier–Stokes with Smooth
Forcing, Part I: Construction of Self-Similar Solutions with Admissible Stress
and Flat Remainder*, arXiv:2609.35406, v2 dated 2026-09-29:
<https://arxiv.org/abs/2609.35406>

The authors describe this as an explanatory reconstruction of the profile-
construction part of OpenAI's manuscript, intended to help the community
understand it and not intended for journal submission. Its abstract says that
the constructed profiles are smooth and axisymmetric; substitution into
Navier–Stokes yields a divergence-form residual plus a remainder flat in
`1-t` on fixed similarity sectors; and the associated stress and radial shear
satisfy an admissible cone condition. It explicitly says that the stress need
not be small. It introduces a linear model for the inner core and defers
oscillatory-pulse cancellation of the residual to a planned Part II.

## Relevance to this repository

This is a useful independent explanatory source for the *profile-construction
stage*, but the abstract does not report particle tracking, molecular
alignment, a measured viscosity transition, or a validation of a numerical
solver. “Stress need not be small” refers to the mathematical stress constraint
in the construction; it is not a claim that physical viscous effects vanish.
The pulse correction is a residual-cancellation step, not evidence of
particle-scale ordering.

The result therefore does not support the proposed inference

> singular or unbounded continuum quantity ⇒ molecular particles align ⇒
> viscosity loses effect.

That inference would require a specified kinetic or molecular model, a
continuum-to-particle limit, and observables that connect the model to
alignment and constitutive stress. None is supplied by this explanatory
profile paper. It does, however, reinforce a useful audit distinction for our
benchmark: verify separately the leading profile, admissible-stress condition,
residual correction, and final PDE solution. A small residual or a cone
inequality alone cannot stand in for the full construction.

## Status and limits

This source is an explanatory preprint by the authors, not an independent
numerical replication or a separate proof audit. Its own abstract says Part II
will handle oscillatory-pulse cancellation; this refresh does not establish
that Part II has appeared or assess that step. No OpenAI issue or discussion
was opened from this finding, and no defect in the upstream proof is inferred.

The current repo's recorded `actualProfile` pressure-provenance gap remains a
separate extension-level proof obligation. The new exposition neither closes
it nor contradicts it. Likewise, the local OpenFOAM benchmark continues to
test numerical indicators and does not test the analytic theorem.

## Related development: force-space density

A separate paper by Shaozhen Cao, Zhuoni Chi, and Ping Nie, *Density of Forces
Producing Navier–Stokes Blowup* (arXiv:2609.10262, v4 dated 2026-09-22), uses
OpenAI's compact forced solution as a building block. It reports a sharp
threshold for density of smooth blowup-producing forces in relative
`L¹_t Hˢ_x`: for fixed viscosity and zero initial velocity, density holds
exactly for `s < 1/2` on both the three-torus and whole space. Its abstract
also says the local insertion can preserve any given smooth initial velocity,
by cutting off a vector potential so the background is zero near the rescaled
packet and the two velocity fields have no nonlinear cross-interaction. The
authors point to a separate Lean 4 formalization project.

This develops consequences of the forced construction in a different
direction: it studies how densely the forcing can be perturbed in specified
function-space topologies. It does not claim density for fixed force, does
not classify singular initial data for one prescribed force, and says nothing
about molecular alignment or a viscosity law. For experimental interpretation
it underlines that the singular packet is inserted through a localized,
carefully altered external force; observed concentration cannot be attributed
to spontaneous particle ordering without a separate model and evidence.

Source: <https://arxiv.org/abs/2609.10262>

## Formalization repository checkpoint

The paper links to `mathzhuonichi/blowup_density`. Its README claims 27 mapped
article entries are closed in Lean and explicitly says claims outside that
mapped scope are excluded. GitHub Actions run `35692963936` completed
successfully on commit
`af963994418ae32ff16e00a942bf532410928b09` on 2026-09-22. The run includes a
Lean contracts build, an architecture check, compilation of changed modules
outside the registered build closure, and rejection/refactoring checks. This
is meaningful reproducibility evidence for that repository's own formalized
scope; it does not establish that every statement in the paper has been mapped,
that the underlying OpenAI building block has been independently re-proved, or
that a particle-scale model follows.

At the 2026-10-03 GitHub API check, the repository's `main` still pointed to
that commit, Issues were enabled with no open issues, Discussions were
disabled, and GitHub returned no declared license (`license: null`; the root
listing has no `LICENSE` file). Accordingly, this benchmark does not reuse or
vendor its code. No report was sent: there is no demonstrated defect, and this
auxiliary formalization is outside the three prioritized solver repositories.
The read-only snapshot is
`evidence/upstream-refresh/blowup-density-2026-10-03.json`.
