# OpenFOAM Foundation 13 manufactured-force sign audit

Audit date: 2026-09-28. Source pin:
`18870c24d21c6b982e2cdec27b2f59738cca5f90`.

## Result

The generated high-gradient `codedFvModel` body uses
`eqn.source()[celli] -= volumes[celli]*forcing`. At the pinned source, this
injects the intended positive physical forcing on the right-hand side of the
`incompressibleFluid` momentum equation. The existing mock diagnostic
`-eqn.source()/V` consequently recovers `forcing` with the correct sign. This
resolves the source-level sign question raised by the mock's limited scope; it
does not certify a live solver run.

## Source chain

The `incompressibleFluid::momentumPredictor` assembles the momentum terms with
`fvModels().source(U)` on the right of `==`. `fvModel::source` builds a fresh
matrix and invokes `addSup`; `codedFvModel::addSupType` forwards that same
equation to the generated model. In `fvMatrix`, `A == B` is implemented as
`A - B`, and matrix subtraction subtracts the stored source arrays. Thus a
coded source array `-V*f` becomes `+V*f` in the assembled right-hand-side
source when the model matrix is subtracted from the left-hand side.

The transient Euler matrix provides a direct sign check: its diagonal is
`V/dt` and its old-time source is `V*U_old/dt`. With only this transient term
and the coded forcing, the assembled equation therefore gives
`U_new = U_old + dt*f`, the expected explicit forcing direction. The actual
solver also contains convection, stress, pressure correction, relaxation and
constraints, so this scalar reduction checks only the sign convention.
`fvMatrix::solve` copies its stored `source_` into the source argument passed to
the LDU solver, completing the source-to-right-hand-side path.

The source hash manifest, exact file paths, line ranges and stable GitHub links
are in `evidence/upstream-refresh/openfoam-force-sign-audit-2026-09-28.json`.

## Limits

This is a static audit of Foundation 13 at the stated commit. It does not show
that the OpenFOAM case builds, that the generated code compiles in the pinned
container, that pressure correction preserves the manufactured solution, or
that any mesh/time-step reaches the requested end time. Docker execution was
not performed as part of this source refresh. No solver defect or physical
singularity is inferred.
