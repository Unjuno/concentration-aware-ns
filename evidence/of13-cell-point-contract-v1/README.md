# Scoped cellPoint source contract evidence

Numerical source `5207235c60417112cb35e620df8e9ecde37b8d75`.
Upstream `18870c24d21c6b982e2cdec27b2f59738cca5f90`.

`analysis.json` records eight pinned source hashes/URLs, exact symbolic affine
controls, 125 integer chord controls and four archive inventories. All original
raw/member hashes were verified. No polyMesh member exists in any of the four
archives; actual tetrahedral geometry is unverified. The source's degenerate
fallback prevents unconditional centre-interpolation inference.

`prospective-capture-requirements.json` is an unexecuted capture specification.
`audit.log`, `test-suite.log` and `validation.json` record execution and checks:
312 tests passed, 1 skipped, 83 subtests passed. The independent discontinuous
negative control demonstrates that point constraints alone do not imply the
continuous chord bound. No upstream C++/cellPoint evaluation, new CFD run,
clean-export replay or full upstream suite is claimed. See
[report](../../reports/openfoam-cell-point-contract-2026-10-04.md).
