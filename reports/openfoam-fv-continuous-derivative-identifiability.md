# What archived finite-volume velocity values identify

## Scope

The high-gradient benchmark archives OpenFOAM Foundation 13 `volVectorField U`
values and compares diagnostics derived from them. In the pinned source,
`volVectorField` is a typedef of `VolField<vector>`
(`work/openfoam13-source-20260624/src/finiteVolume/fields/volFields/volFieldsFwd.H`,
commit `18870c24d21c6b982e2cdec27b2f59738cca5f90`). These are discrete field
degrees of freedom. The type and serialized values do not, by themselves,
select a unique continuous velocity between cells. In particular, this report
does not assume that `U` stores exact cell averages.

## Exact observation ambiguity, even under a cell-average interpretation

There is a stronger limit than finite point sampling. Suppose, solely for this
argument, that every archived value were an exact cell average on a finite
mesh. Choose a smooth vector potential compactly supported in a ball strictly
inside one cell, and let `w` be its curl. Choose the potential so that the
curl is nonzero. Then `w` is smooth, divergence-free, zero near every cell
face, and has zero integral over every cell (each component is a derivative
of a compactly supported function). Consequently adding `A*w` for any real
amplitude `A` preserves every cell average and all face values, while its
continuous gradient maximum grows like `|A|`.

Thus even exact finite-volume averages, without additional regularity or a
specified within-cell reconstruction, do not give a finite universal upper
bound on the continuous gradient maximum. This is an information limit; it is
not evidence that the solver produced the hidden field, that the field solves
the benchmark PDE with the same forcing, or that a physical fluid contains
aligned particles. The existing periodic nullspace example in
`reports/sampling-observation-limit.md` separately demonstrates the same
sampling issue for nodal, cell-center, and cell-average observations on a
specified family of uniform grids.

## What the current benchmark can support

- The archived `U` values and mesh are identifiable and replayable discrete
  outputs.
- A finite-difference diagnostic, the named trigonometric interpolant, or a
  declared finite-volume reconstruction is a separate derived object. Its
  conclusions apply to that operator/reconstruction and its stated error
  bound.
- A continuous derivative bound for the unknown solver field requires extra
  assumptions or evidence, such as a validated reconstruction, a regularity
  estimate, or a bound on unresolved modes. It cannot be inferred from the
  stored DOFs alone.
- None of these diagnostics tracks molecular positions. Navier–Stokes fields
  here are continuum-model outputs; particle alignment and a velocity-driven
  change in material viscosity require a separately defined microscopic model
  and independent evidence.

The current trigonometric certificate remains valid for its explicitly named
interpolant. It does not certify the unknown within-cell OpenFOAM field. Frozen
solver verdicts are unchanged, and the continuous finite-volume-field question
remains open under issue #5.
