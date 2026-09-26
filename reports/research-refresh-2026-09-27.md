# Research refresh: 2026-09-27 (JST)

## Newly identified follow-up

[Petrillo and Glimm, arXiv:2609.23868v1, September 20](https://arxiv.org/html/2609.23868v1)
formulate a positive energy-defect target for unforced periodic Navier–Stokes
at fixed positive viscosity. Their target implies blowup; the converse is
not established. They distinguish a flux lower bound over finitely many
resolved scales from a uniform bound at arbitrarily fine scales. The paper
does not construct a solution realizing its target. Its formal library uses
abstract functions and sequences; connection to formal Navier–Stokes solution
objects remains outside that library. These are useful limits on inference,
not a new proof of unforced blowup or changing material viscosity.

## Pinned source inspection

Inspected [commit fe8b8217b2e342fb5fc0dc8514e651b5df12d930](https://github.com/researchathomology/NS_ENERGY_DEFECT_REDUCTION/tree/fe8b8217b2e342fb5fc0dc8514e651b5df12d930).
Selected source files, Apache license, notice, toolchain and dependency manifest
are archived under `evidence/upstream-refresh/positive-defect-2026-09-27/`.
`source-audit.json` records hashes and observation time. This is source
inspection, **not a local Lean build or independent-kernel verification**.

Concrete declaration boundaries in `EnergyDefect/EnergyDefect.lean`:

| Declaration | Input that must still be established for a physical/PDE application |
|---|---|
| `flux_tendsto_defect` | Shell balance identity and three convergence hypotheses |
| `averaged_tail_floor_le_defect` | Convergence to the defect and a lower bound for every sufficiently large index |
| `defect_gives_averaged_tail_floor` | An already positive limiting defect, above the proposed lower bound |

`ValidatedProof.lean` likewise takes the computed lower bound, analytic upper
bound and enclosure assumptions as inputs to `validated_epoch_ends_inside`.
None of these inspected declarations supplies a particular Navier–Stokes
trajectory satisfying the inputs.

The pinned README reports that the regenerated 17-module package has not been
rebuilt as a whole, while describing successful older builds. This is an
unresolved build-evidence item, **not an observed compilation failure**. Do not
promote the older build to validation of this pin, or file an upstream defect
on that basis. No upstream issue was submitted for this inspection.

## Consequences for our work

Our finite-resolution acceptance gates remain accuracy diagnostics. A measured
flux plateau, energy-budget residual or localized gradient cannot on its own
certify a continuum singularity. For a forced periodic smooth solution, an
energy-budget diagnostic must include external work:

`E(t0) - E(t1) + integral <f,u> - nu * integral ||grad u||^2`.

That residual should vanish for the exact smooth solution. A nonzero numerical
value first requires checking quadrature, spatial/time errors and forcing
alignment. A nonperiodic domain additionally requires the appropriate boundary
fluxes. This is our diagnostic implication, not a claim that the new paper
proves our benchmark correct.

The user's concentration → alignment → viscosity hypothesis therefore retains
separate obligations: identify deformation with the flow derivative, quantify
directional contraction/extension, and supply a constitutive or microscopic
model before claiming material viscosity changes. Energy loss beyond a fixed
viscosity budget is not a derivation of a smaller viscosity coefficient.

## Refresh checks and remaining work

- GitHub API still reports OpenAI `main` at
  `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, matching our previously checked pin.
- [Cao–Chi–Nie arXiv:2609.10262](https://arxiv.org/abs/2609.10262) still lists
  September 22 v4; its page says the change was abstract metadata, with the
  manuscript unchanged. Search snippets containing an older title are stale.
- No extension theorem changed in this refresh. The existing 123-report
  Lean checks are historical results for the unchanged extension. Variational
  uniqueness and identification with a nonlinear flow derivative remain open.
- This search is bounded literature surveillance, not an exhaustive claim
  that every new result has been found.

## Subsequent analytic work: variational uniqueness

The subsequent extension adds `axisDeformation_inverse`; both source pins
pass 124 axiom reports with only the allowed standard axioms. The earlier
123-report statement above describes the literature-refresh revision.
[The new note](../docs/axis-variational-uniqueness.md) gives a classical
uniqueness proof using the conserved vector J*y, with eight independent
symbolic identities and three rejected sign/rate perturbations. Full
uniqueness is not yet Lean-formalized; identification with a nonlinear flow
derivative and finite-packet bounds remain outstanding.

## Subsequent connection to the nonlinear material flow

Both pins now pass 125 axiom reports, including
`actual_candidate_axis_contDiffAt`: eventual spacetime smoothness of the actual
assembled field at the axis. [The flow-derivative argument](../docs/axis-flow-derivative.md)
joins the source hypotheses on one terminal interval, constructs a compact
smooth tube for each T<1, and derives a quadratic displacement remainder.
It identifies the explicit deformation with the nonlinear flow derivative
at the classical analytic level. That argument is not yet end-to-end
Lean-formalized. The tube radius and derivative bounds are non-effective;
uniform fixed-packet control through t=1 and the actual-profile pressure
witness are still open.

## Propagator-based finite-packet estimate

The [packet-bound note](../docs/axis-packet-bound.md) refines the generic
Gronwall estimate using the exact operator norm of F(t)F(s)^(-1). Rotation
drops out of the linear amplification. A scalar nonlinear comparison supplies
an explicit sufficient packet radius and remainder conditional on the tube
radius and Hessian bound. Nine symbolic residuals vanish and three algebraic
controls pass; this is not a new Lean run or PDE simulation. The actual tube
and Hessian constants remain non-effective, and a separate stronger condition
is needed to resolve relative error in contracting transverse directions.

## Source dependencies for packet constants

[The source audit](../docs/packet-constant-dependencies.md) identifies compact
jet bounds and the finite cutoff-stage route. Two new extension lemmas transfer
uniform derivative bounds from the selected base through neighborhood equality
on a compact set, and prove all scalar cutoff-stage jets vanish for j>=J when
J*qmin>1 and q>=qmin>0. The latter uses only strict increase of the natural
cutoff schedule. This is progress toward finite-stage extraction, not extraction
of executable coefficient data or a numerical Hessian bound. The actual profile,
schedule and compact maxima remain existential in the inspected source.
Both source-pin runs now pass 127 extension axiom reports; the five gate-fault
tests pass. No solver or training rerun is part of this change.

## Exact finite-sum replacement

Four subsequent extension lemmas now establish equality of the scalar slow sum
with its finite cutoff prefix under J*q>1, neighborhood equality, all-order
jet equality, and neighborhood equality after physical-chart composition and
the restored q-power. The cutoff prefix retains the original cutoffs; it is
not the uncut asymptotic prefix. These identities advance finite extraction
without claiming executable coefficients or a certified numerical Hessian.
Both pins pass 131 extension axiom reports with only the allowed standard
axioms. The five verification-gate fault tests also pass.

## Actual-root stretching exponent enclosure

The extension now proves 7999999/2000000 <= C < 4 for an existing root of
the actual nominal witness, using its SmallParameters and the proved root
interval. [The enclosure note](../docs/axis-stretch-range.md) gives the exact
algebra and conservative packet formulas obtained by replacing the unknown C
with its upper bound 4. No PressureData hypothesis or numerical flow is used.
The actual tube radius and Hessian bound remain uncomputed; full coefficient
extraction has not been achieved.
Both source-pin checks pass 134 axiom reports; the five verifier fault tests
pass. The numerical benchmark verdicts are unchanged.

## Variational equation connected to the actual Jacobian

`selected_root_axis_jacobian` substitutes C/(1-t) into the complete selected
matrix. `actual_root_axis_jacobian` transfers the same identified matrix to
the assembled field. `actual_root_deformation_hasDerivAt` then verifies the
explicit deformation equation with the actual spatial Frechet derivative on
its right-hand side, eventually on the terminal axis. This closes a formal
coefficient/ODE connection; the compact-interval extraction, full variational
uniqueness and nonlinear-flow identification remain classical arguments.
An earlier normalization time outside the terminal interval does not give an
initial-value solution for the actual field before that interval.
Both source pins pass 137 axiom reports with only the permitted standard
axioms. All five verification-gate fault tests pass. No numerical solver run
or molecular interpretation is part of this verification.
