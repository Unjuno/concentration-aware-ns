# Finite mesh observations do not identify a continuum flow

Date: 2026-10-03. This is a conditional analytic corollary, not a new CFD
experiment and not an independent verification of the OpenAI construction.

## Claim and scope

Assume the localized forced blow-up packet and the torus gluing theorem used in
Cao, Chi and Nie, *Density of Forces Producing Navier–Stokes Blowup*,
arXiv:2609.10262v4, Theorem 3.6. Let a reference forced solution be smooth
through a chosen time `T+delta`. Fix a finite collection of finite meshes of
`T^3`. Each mesh is a finite partition into cells with closed cell skeleton
(mesh faces) having empty interior; ordinary finite polyhedral AMR meshes
satisfy this condition. Also fix a finite set of spatial point-observation
locations.

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

The union of the finitely many mesh skeletons and sample points is closed with
empty interior. Its complement contains an open ball `B` whose closure lies
inside one cell of every mesh and avoids all sample points. Apply the localized
torus gluing theorem with support inside `B`. Write the velocity, pressure and
force differences as `delta u`, `delta p`, and `delta g`. For each `t<T`,
`delta u` is smooth, divergence-free, and compactly supported in `B`; likewise
`delta g` is supported in `B`.

For each component `j`,

    delta u_j = div(x_j delta u),

so its integral over the containing cell is zero by the divergence theorem.
Every other cell has zero perturbation. This proves equality of velocity cell
averages on each mesh. Integrating the difference of the momentum equations
over a cell gives the time derivative of this zero velocity integral plus
boundary fluxes from convection, pressure, and viscosity. The perturbations
vanish near the cell boundary; a spatially constant pressure-gauge difference
has zero net boundary integral. Consequently the force difference also has
zero integral in each cell. The point and face statements follow from the
support choice.

This extends the finite-uniform-grid observation argument in Theorem 4.7 from
whole-space Cartesian grids to any fixed finite family of finite meshes whose
skeletons leave an open cell interior. The torus version uses the article's
localized insertion theorem (Theorem 3.6); the finite-uniform-grid version is
stated in its Theorem 4.7. This extension is a proof adaptation recorded here,
not a theorem quoted verbatim from the article.

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
arXiv:2609.10262v4](https://arxiv.org/html/2609.10262v4), Theorem 3.6 and
Theorem 4.7 (revision dated 2026-09-22). The arXiv record states that v4
updated abstract metadata while leaving the v3 manuscript unchanged. The
paper's results are preprint claims conditional on the cited OpenAI packet;
this note does not certify their proof or premise.
