# Supported impact and outstanding evidence

This report bounds impact by the reproduced case, source version and theorem
hypotheses. It is not an inventory of every industrial consequence. No result
below establishes physical danger, molecular alignment or changing viscosity.

| Finding | Demonstrated scope | Concrete improvement supported | What must precede expansion |
|---|---|---|---|
| SU2 BDF2 source-time lag | v8.5.0 uniform time-dependent MMS; six archived runs, converged inner residuals, exact discrete recurrences | Add a regression test that checks temporal order for the time-dependent source path; review source-time evaluation in that path | Independently test other source paths, restarts, first-step history and time schemes before recommending a general code change |
| Aggregate versus local diagnostics | The frozen localized benchmark matrices; eleven UNCERTAIN acceptance reports | Report aggregate errors alongside local derivative and spectrum observations, with diagnostic controls | Establish continuous-field bounds, temporal/asymptotic convergence and preregistered thresholds before declaring standard-PASS/local-FAIL |
| OpenFOAM derivative-observation error | Foundation 13 n32 case and same-grid exact-field FD2 control | Differentiate the known reference using the same postprocessor; separate its error from the computed-field discrepancy | Control sampling and derivative error for the computed field; the reference-control error is not a universal error bound |
| OpenFOAM AMR history | Archived dynamic and fixed-refined controls | Retain both histories and inspect initialization/remapping contributions | Isolate a contract violation before attributing the difference to an implementation defect |
| PhysicsNeMo validation | v2.2.1 explicit time-derivative API checks and five fixed-budget training cases | Publish independent manufactured-solution residual and derivative checks alongside training loss | Fresh preregistration, seed/optimizer assessment and continuum extrema control; newer-version runtime validation is separate |
| Axis material deformation | Selected terminal root under the recorded assembly/schedule hypotheses; checked components and classical flow argument; power-law envelope analysis gives a conditional certified-radius exponent | Use anisotropic contraction/extension, volume preservation and the quadratic local remainder to assess which continuum claims follow | Actual tube/Hessian endpoint envelopes and constants, plus end-to-end formalization, are still needed to certify any particular finite packet; see `docs/axis-packet-bound.md` |
| Strict negative viscous-force/inertia limit | Pressure-qualified witness and stated root hypotheses | Retain the precise pressure condition in every sign claim | Link the pressure bound to `actualProfile`; qualified existence alone does not supply this |
| Subcritical force-space density (Cao–Chi–Nie, arXiv:2609.10262v4) | Article claims breakdown-producing smooth forces are dense in relative `L¹_t Hˢ_x` for `s<1/2` on `T³` and `R³`, and in `L²_t Hˢ_x` for `s<-1/2` on `R³`; proof assumes the OpenAI compact blowup seed | Keep the manufactured forcing byte-identical across resolutions; report its resolved spectrum and any force-representation error separately from solution error | Independently check the downstream proof closure and establish relevance to a fixed force/solver before changing gates; force-space density is not probability, molecular alignment, or a solver defect |
| Gaussian tangent-map comparison model | Under global affine application of the audited local derivative, fixed-radius infinite-axis-tube probability tends to one, while fixed finite-cylinder probability is asymptotic to `sqrt(2/pi)*L*Q^C` and tends to zero; peak density and entropy stay constant | Report the observation geometry explicitly; distinguish transverse localization from 3D localization | The actual nonlinear-flow theorem does not extend its tangent map over an unbounded Gaussian; effective finite-packet bounds and a particle/kinetic model are needed for that extension; see `docs/particle-position-probability.md` |

## Reporting disposition

The SU2 time-path finding has been sent to the existing
[discussion](https://github.com/su2code/SU2/discussions/2890#discussioncomment-18613462).
The diagnostic shift is an intervention showing causation within the tested
recurrence; it is not a reviewed production patch. This project has not
demonstrated an implementation defect in OpenFOAM or PhysicsNeMo. Their
published benchmark and methodology findings remain useful without inventing
defect issues. The exact decisions and contribution routes are in
[upstream disposition](upstream-disposition.md).

## Mathematical and physical boundaries

The smooth manufactured benchmark tests approximation to a known solution.
It is not a numerical reproduction of the OpenAI singular construction.
The [forcing audit](forcing-scope-audit.md) records their different assumptions.
The later energy-defect paper concerns another target and does not transfer
its hypotheses to these runs; see [the research refresh](research-refresh-2026-09-27.md).
The force-density follow-up varies the external force in a specified weak
function-space topology. Its scaling thresholds motivate documenting forcing
resolution and cross-mesh input identity, while leaving the current fixed-force
acceptance gates and solver verdicts unchanged; see the
[2026-09-28 source refresh](../docs/openai-refresh-2026-09-28.md).

The [flow-derivative argument](../docs/axis-flow-derivative.md) describes
infinitesimal continuum separations, with a non-effective local finite-packet
remainder for each fixed T<1. Axial uncertainty can grow while transverse
uncertainty shrinks. A continuum fluid element is not a molecule, and
volume-preserving deformation is not particle shrinkage. Claims about light,
phase transitions or constitutive viscosity require separate physical models
and evidence, absent here.

## Remaining project obligations

The completed experiments and publication decisions do not close every
analytic obligation. The actual-profile pressure premise, effective
finite-neighborhood control and end-to-end formalization remain open. The
original NS independent-kernel result verifies its stated target only;
Euler verification and finite-stage extraction have not been performed.
These gaps are kept in [the completion audit](../docs/completion-audit.md),
which still records the overall goal as incomplete.
