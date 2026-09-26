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

## Extension dependency delta

`python -m tools.audit_lean_dependency_delta` traverses the old pinned local
NavierStokes imports and intersects them with the saved comparison inventory.
It finds 506 modules with no missing local files, including 10 changed modules.
Only NaturalProfile changes among the extension's ten direct imports, but the
transitive changes also include NaturalAxisCoefficients, NaturalCore,
NaturalEntrance, NominalProfile, ReferenceBounds, LeadingStressWeights and three
activation modules. See `evidence/upstream-refresh/extension-dependency-impact.json`.

Direct inspection of NaturalProfile's diff shows six theorem signatures changing
from NaturalAxisData.SmallParameters to NaturalAxisRange.Parameters, including
axial_equation_reconstruct and exists_profileFamily. This identifies a parameter
interface change to check, not a demonstrated failure of our extension. New
modules imported by the updated versions and external dependencies are outside
this old-closure scan. A fresh build remains necessary before claiming updated
source compatibility; the old pinned proof environment is unchanged.

## New parameter range checked against old dependencies

The new NaturalAxisRange module broadens h≤1/1000 and j≤1/1000 to h≤1/100
and j≤1/20. Its ofSmall theorem and CoeOut instance explicitly retain old small
parameters. We compiled the entire downloaded module with the old pinned Lean
and NaturalAxisData dependencies, appending an ofSmall axiom report. The process
exited 0 and the report contains only propext, Classical.choice and Quot.sound.
Source/check/log hashes and the exact appended suffix are in
`evidence/upstream-refresh/range-check.json`; output is in `range-check.log`.

This establishes that this range adapter checks in that recorded mixed-source
context. It does not certify the whole new revision, its new dependency closure,
or our extension against it. The source is retrieved from the manifest URL;
append check_suffix and run `lake env lean` with the existing checker environment
as in runtime/lean-verification/check_axis_sign.sh. Existing selected small
parameters need not be enlarged to use the new interface. PressureData is not
supplied by this parameter conversion; the pressure-threshold gap is unchanged.

The bounded range check now has an executable replay:
`python3 -m tools.verify_upstream_range`. It checks the reviewed source hash,
constructs and hashes the appended axiom-report file, runs the network-isolated
checker, and requires successful exit, the expected axiom report, no sorryAx,
and unchanged inputs. A real replay succeeded; command, runner hash and result
are in `evidence/upstream-refresh/range-replay.json`. This command uses the
previously provisioned checker volume; it is not a clean-room new-pin build.

## Updated assembly build started

The full pinned updated archive has been acquired and hashed in
`evidence/upstream-refresh/source-acquisition.json`. Comparison with the original
old archive confirms identical lean-toolchain, lakefile.toml and lake-manifest.json
bytes. The previously configured old checkout had local-path changes, which are
recorded separately rather than mistaken for upstream changes.

A fresh source/build area in Docker volume cans-lean-updated now builds
NavierStokes.ActualCandidateAssembly. Only Lake manifest/config paths were changed
to /verify/packages; a file-by-file comparison confirms theorem sources are
unchanged. Old toolchain/dependency artifacts are mounted read-only from
cans-lean-verification. Inputs and limits are recorded in updated-build-inputs.json;
the reusable execution command is runtime/lean-verification/check_updated_assembly.sh.
The ongoing process log must not be treated as a successful result. Completion,
extension compatibility, and independent comparator checking are separate steps.

## New quantitative pressure-root lemma

AxisRootPressureBounds.ideal_prefix_root_pressure_lower supplies a root with
Z > j B²/20, retaining the pressure-prefix amplitude in the bound. It still
requires B≥2, admissibility and the ideal-prefix identities. Thus its descriptive
reference to the actual integral pressure does not assert that the arbitrary
FinalSlowBase.actualProfile retains B≥2.

We checked both new modules by concatenating NaturalAxisRange and
AxisRootPressureBounds (removing only the second module's import of the first)
against the old pinned dependency environment. Lean exited 0; the printed axiom
report for ideal_prefix_root_pressure_lower contains only propext, Classical.choice
and Quot.sound. Exact composition and source/check/log hashes are saved in
`evidence/upstream-refresh/range-pressure-check.json`. This gives a usable
quantitative lemma for pressure-qualified profiles, not an unconditional theorem
about our actual candidate. The separate updated assembly build remains ongoing.


## Separate extension compatibility runner

`python3 -m tools.verify_updated_axis_sign` now uses the prepared updated source
volume with both source and dependency volumes mounted read-only. It reuses the
existing axiom/exit-code/source-integrity gate, but writes only to
`evidence/upstream-refresh/updated-axis-force-sign.{json,log}`. The original pinned
proof evidence is preserved. Five existing gate fault-injection tests pass after
the output-path refactor. The updated extension run has not yet been executed;
it depends on successful completion of the assembly build.

SU2 discussion refresh encountered a live GraphQL TLS handshake timeout. The
web fallback showed unanswered/zero comments, but its crawl was reported as last
week, so it does not establish the current absence of replies. The distinction
is recorded in `evidence/upstream-refresh/su2-discussion-refresh.json`.


## Live SU2 response and BDF2 follow-up

A successful live retry supersedes the stale cached zero-comment result.
`evidence/upstream-refresh/su2-discussion-live-retry.json` records the September 13
response. Its proposed BDF2 check was performed with the existing pinned runtime:
six runs confirm the exact lagged/source-target recurrences, including startup,
and all residual thresholds pass. See `reports/su2-bdf2-source-time.md`.
The result was submitted as a reply in the existing discussion, not a duplicate
issue or a claim that the broad PhysicalTime edit is ready to merge.


## PhysicsNeMo compatibility removal

The September 22 commit 426f7552 removes the opt-in pre-v2.0 compatibility layer
and the PHYSICSNEMO_ENABLE_COMPAT hook for the v2.3 development tree. The migration
guide enumerates replacement imports. Static comparison of all direct
physicsnemo imports in our tools against both removed alias maps finds no match.
The current FullyConnected, PhysicsInformer and PDE imports do not depend
directly on those aliases. Evidence is saved in physicsnemo-compatibility-removal.json
and physicsnemo-direct-import-audit.json under evidence/upstream-refresh.
This is only an impact review of that commit, not a transitive-import or runtime
compatibility test of v2.3. The original pinned v2.2.1 experiment is unchanged.


## Updated build and extension completed

The previously running build finished with exit code 0: all 3679 jobs for
NavierStokes.ActualCandidateAssembly completed. The post-build comparison finds
all 2669 source/config files unchanged, with the same manifest hash as the
pre-completion check. The extension was then run against the updated project
artifacts: exit code 0, all 104 axiom reports present, only allowed axioms, and
no sorryAx. AxisForceSign.lean is byte-identical to the extension previously
checked against the original pin; no compatibility edits were required.

`evidence/upstream-refresh/updated-verification-summary.json` binds the new
results and logs by hash. Old-pin proof evidence remains separate. These results
supersede the historical started/not-yet-executed statuses above. They establish
targeted Lean build and extension compatibility, not independent nanoda or
comparator verification of the new pin. The actualProfile pressure premise,
molecular interpretation and physical constitutive-viscosity claim remain open.


## Updated independent comparator run started

After the successful assembly and extension checks, the same tested Comparator
and nanoda binaries are now running the updated source's public NavierStokes
challenge. The challenge statement and JSON are byte-identical to the original
pin. `updated-comparator-inputs.json` records live binary hashes and challenge
hashes; `runtime/lean-verification/run_updated_comparator.sh` records the command.
Only the updated project's .lake subtree is writable. The old dependency/checker
volume and updated theorem sources remain read-only, with networking disabled.
This run is not yet complete. Its results must remain separate from the already
successful original-pin independent check and from our extension's Lean check.


## Updated independent verification completed

The same comparator invocation completed with exit code 0. After the 9371-job
solution build and export, nanoda accepted the solution, Lean's default kernel
accepted it, and Comparator reported final success. Both public challenge
theorems (R3 and periodic) list only propext, Classical.choice and Quot.sound.
The unchanged challenge statement is checked against the updated source pin
f9e8bc5b38b6e212696e8a30e3e91517af887bbd.

`evidence/upstream-refresh/updated-comparator-result.json` records the terminal
result and log/input hashes. The full log is archived alongside it. This
supersedes the started status above. It is independent kernel acceptance for
these two formal theorems, not independent verification of our extension or
evidence for the proposed molecular/viscosity interpretation.


The extension subsequently gained two stretch-coefficient lemmas: its exact
root identity and positivity. Both original and updated source pins now pass
all 106 axiom reports with the same extension bytes, only permitted axioms and
no sorryAx. The current summary hashes refer to this replay. The earlier
104-report compatibility run remains available at commit cae2ac5. Full matrix
deformation and molecular interpretations remain outside these two lemmas.


The next extension replay adds the selected-base axial derivative connection
C/(1-t). Both pins pass all 107 required axiom reports. This connects the
coefficient calculation to the previously proved stream derivative, while
leaving the full Jacobian/matrix-ODE transfer explicit as unfinished work.


Both source pins now pass 109 extension axiom reports after adding the
selected-base velocity-component derivative and its transfer to the actual
activated periodic field. The actual axial entry equals C/(q*(1-eta²))
eventually as q tends to zero from above, under explicit root and schedule
hypotheses. No PressureData assumption is used for this axial stretching result.
The full Jacobian and matrix deformation remain separate unfinished steps.


The general axisymmetric Cartesian Jacobian at the axis is now checked as
well: a transverse block [-b,-f;f,-b] and axial entry partialZ(u), with no
axis singularity. Both pins pass 110 extension axiom reports. This establishes
the matrix shape under slice differentiability; it does not by itself establish
contraction or identify the full actual-field matrix coefficients.
