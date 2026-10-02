# Finite mesh observations do not identify a continuum flow

Date: 2026-10-03. This is a conditional analytic corollary, not a new CFD
experiment and not an independent verification of the OpenAI construction.

## Claim and scope

Assume the localized forced blow-up packet and the torus gluing theorem used in
Cao, Chi and Nie, *Density of Forces Producing Navier–Stokes Blowup*,
arXiv:2609.10262v4, Theorem 3.6. Let a reference forced solution be smooth
through a chosen time `T+delta`. Fix a finite collection of finite meshes of
`T^3`. Each mesh is a finite partition into cells whose skeleton (the union of
cell boundaries) is closed and has empty interior; ordinary finite polyhedral
AMR meshes satisfy this condition. Also fix a finite set of spatial
point-observation locations.

Then the localized insertion can be placed so that, for all `t<T`, all of the
following remain identical between the reference and inserted solutions:

- velocity cell averages on every cell of every fixed mesh;
- force cell averages on every such cell;
- velocity values and derivatives on mesh faces (the perturbation vanishes in
a neighborhood of every face);
- velocity and force values at the fixed finite point-observation locations.

The inserted continuum solution nevertheless has unbounded velocity as
`t` approaches `T`, as asserted by the assumed packet/gluing theorem. Thus no
finite observation set of these forms, by itself, identifies the continuum
solution class. The conclusion is existential and depends on the finite
observation family chosen in advance.

## Proof of the observation statement

For ordinary finite polyhedral meshes, each skeleton is closed with empty
interior. A finite union of such polyhedral skeletons and finitely many points
still has empty interior, so its complement contains a ball `B` whose closure
lies inside one cell of every mesh and avoids all sample points. More
abstractly, the claim assumes that this particular finite union of skeletons
has empty interior; closedness alone would not suffice. Apply the localized
torus gluing theorem with support inside `B`. Write the velocity, pressure and
force differences as `delta u`, `delta p`, and `delta g`. For each `t<T`,
`delta u` is smooth, divergence-free, and compactly supported in `B`; likewise
`delta g` is supported in `B`.

Using the Euclidean coordinates of the chart containing `B`, for each component
`j` the vector field `x_j delta u` is compactly supported inside `B`, and
incompressibility gives

    div(x_j delta u) = delta u_j + x_j div(delta u) = delta u_j.

Its integral over the containing cell is therefore zero by the divergence
theorem. For force averages, subtract the momentum equations and integrate over
a cell `C`:

    integral_C delta g = d/dt integral_C delta u
      + integral_boundary_C (u⊗u - v⊗v + delta p I - nu grad(delta u)) n.

The first term is zero because the cell integral of `delta u` vanishes for
every `t<T`. All boundary flux differences vanish because the perturbations
are supported strictly inside `B`; a spatially constant pressure gauge also
contributes zero since the integral of the outward normal on a closed cell
boundary is zero. Thus the cell integral of `delta g` is zero. Every other
cell has zero perturbation. The point and face statements follow directly
from the support choice.

The finite-uniform-grid result is explicit in v4, Section 4.6, Theorem 4.7,
on `R^3`. The torus finite-AMR and finite point/face-observation statement
above is a separate proof adaptation from the periodic gluing theorem (v4,
Theorem 3.6). It is not stated verbatim in the article. The geometric step
uses only that the finite union of skeletons and probes leaves an open ball;
the conservation step is the cell integration shown above.

## What this does and does not imply for this benchmark

The result limits *universal identification from finite observations*. It
does not contradict convergence under refinement for one fixed smooth
solution, and it does not say that the hidden inserted field is a solution for
the reference force: the force is changed, though the stated cell-average
observations of that force are preserved. A solver given an exact analytic
formula for the force, a known fixed manufactured solution, derivative-sensitive
information, or an unbounded/dense observation family is outside this
indistinguishability statement.

Therefore the benchmark's spatial and temporal convergence claims must remain
conditional on its fixed manufactured solution, forcing representation,
reconstruction operators and frozen observables. Passing those gates cannot be
promoted to a detector guarantee for every nearby smooth forced flow. Conversely,
this information limit is not evidence of an OpenFOAM, SU2 or PhysicsNeMo bug,
and supplies no upstream issue. It does not imply particle alignment, a
molecular position law, a phase transition or a viscosity change.

## Source

Cao, Chi and Nie, [Density of Forces Producing Navier–Stokes Blowup,
arXiv:2609.10262v4](https://arxiv.org/html/2609.10262v4), Theorems 3.6 and 4.7
(revision dated 2026-09-22). The finite-grid theorem is in Section 4.6 of v4
and applies on `R^3`; the torus/AMR statement above is our separate adaptation.
The paper's results are preprint claims conditional on the cited OpenAI packet;
this note does not certify their proof or premise.

## Related literature update (checked 2026-10-03)

Lei and Ren, [Finite-Time Blowup for Navier-Stokes with Smooth Forcing, Part I:
Construction of Self-Similar Solutions with Admissible Stress and Flat Remainder,
arXiv:2609.35406v2](https://arxiv.org/abs/2609.35406), submitted 2026-09-28
and revised 2026-09-29, describe their work as an expository reconstruction of
the profile-construction part of OpenAI's manuscript. Their abstract says the
residual cancellation by oscillatory pulses is reserved for a companion Part II.
This is useful additional exposition, not an independent verification of the
full construction or of its singularity theorem; no claim about the status or
contents of the planned companion is made here.
