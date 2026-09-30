# Primary-source audit

Updated 2026-09-30. Source observations, reproduced behaviors and unresolved
quality claims are distinguished below. This remains an interim audit.

## OpenFOAM Foundation 13

Inspected commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`.
License: GPL-3.0-or-later per source headers. Do not mix OpenCFD APIs into this
Foundation adapter.

- [Residual implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/cfdTools/general/solutionControl/convergenceControl/singleRegionConvergenceControl/singleRegionConvergenceControl.C): compares configured fields' initial residuals with absolute thresholds.
- [AMR implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C): candidate selection and consistency refinement must both be considered in interpreting maxCells.
- [AMR cell-budget source audit](../reports/openfoam-amr-source-budget-audit-2026-09-28.md): pinned source behavior, cap-5000 allowance arithmetic, and why budget-blocked candidates remain unobserved.
- [Source hook](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvModels/general/codedFvModel/codedFvModel.H): coded fvModel is an integration candidate; forcing sign and units need execution tests.
- [Reporting instructions](https://github.com/OpenFOAM/OpenFOAM-13): README directs bug reports to bugs.openfoam.org.

## SU2

Pinned v8.5.0: `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`;
LICENSE.md and adapter headers reviewed: LGPL-2.1-or-later.

- [Configuration](https://github.com/su2code/SU2/blob/v8.5.0/config_template.cfg): includes MMS_INC_NS and USER_DEFINED_SOLUTION. BODY_FORCE_VECTOR alone is constant and insufficient for the proposed varying force.
- [Convergence documentation](https://su2code.github.io/docs_v7/Solver-Setup/): residual and coefficient stopping criteria; verify against selected version.

## NVIDIA PhysicsNeMo

Pinned v2.2.1: `1b961314e42a0625502ba1592d25f706f1e02a24`;
LICENSE.txt reviewed: Apache-2.0. Native CPU residual evaluation and training
executed; exact dependency freeze is in runtime/physicsnemo.

- [Archived symbolic repository](https://github.com/NVIDIA/physicsnemo-sym): upstreamed into NVIDIA/physicsnemo; API changes include inline PDE definitions. Old repository uses Apache-2.0.
- [Historical Taylor–Green example](https://docs.nvidia.com/physicsnemo/25.08/physicsnemo-sym/user_guide/intermediate/moving_time_window.html): Re=500, spectral reference, average TKE evaluation. This is historical example evidence, not proof of current code behavior.

## Candidate register

| ID | Candidate | Classification now | Next evidence |
|---|---|---|---|
| OF-01 | residual convergence with inaccurate local gradients | high-gradient v2 uniform matrix complete; n16/n32 local failures exceed the exact-reference FD2 resolution floor, while n64/n128 at dt=.001 and n64 at dt=.0005/.00025 are standard/local PASS | temporal trend is descriptive; AMR-path attribution remains open |
| OF-02 | AMR accuracy under finite budgets | completed budget and static refined-mesh controls; attribution unresolved | isolate initialization/remapping/flux effects |
| OF-03 | strict interpretation of maxCells | source loop and cap100000 log agree: allowance 11,908, whole level group 12,416, transient 103,552, then 256 split points unrefined to 101,760 | approximate-cap behavior explained for this event; exact unselected candidate count unavailable; no defect issue warranted |
| OF-04 | high-gradient AMR accuracy under frozen budgets | Three v2 budgets and fixed-final-mesh controls complete. Endpoint and logged time-step continuity residuals are tiny despite 37–40% AMR velocity error | continue with momentum/field-transfer history controls; do not attribute to a specific map or projection component; blocked candidates remain unobserved |
| SU-01 | conventional convergence with inaccurate local QoI | localized grid/time sweep complete; no standard-PASS/local-FAIL counterexample established, residual gate limits conclusions | investigate nonuniform/AMR and additional solver paths only under a distinct preregistered contract |
| SU-02 | MMS old-time forcing | reproduced with analytic control and intervention; contract question | upstream Q&A 2890 |
| ML-01 | aggregate and peak accuracy disagreement | five-case sampling matrix complete; all gate outcomes uncertain | bound continuum peaks and assess optimization/seed effects |
| ML-02 | automatic time derivative assumption | x/y/z-only autodiff, explicit t input; documented API behavior | no defect report warranted |
| REF-01 | derivative/sampling artifacts mimic solver error | reproduced FD2 versus analytic/autograd differences | continuous-extremum uncertainty |
| REF-02 | forcing formula error | symbolic/C++/autograd checks passed in stated scopes | preserve per-solver time/assembly distinctions |

### Alignment and viscosity hypothesis

An exact affine incompressible solution shows that directional material-line
alignment does not logically entail a change in the constitutive viscosity:
the solution aligns directions while keeping arbitrary constant `nu`, with
zero viscous force. It is an unbounded-domain counterexample to that inference,
not evidence about the selected OpenAI field or molecular scales. See
[`docs/affine-alignment-viscosity-counterexample.md`](affine-alignment-viscosity-counterexample.md).

### OpenFOAM temporal addendum update (2026-09-30)

The single n64/dt=.0005 rerun passed standard acceptance and all sampled local
quality thresholds; the original run was partial and is retained separately.
The quarter-step temporal case remains unstarted. The original v2 manifest is
unchanged; `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`
is the current cross-run status index. There is no defect or end-to-end matrix
conclusion from this single PASS.

SU2 time-contract reproducer submitted as [Q&A 2890](https://github.com/su2code/SU2/discussions/2890).
No new duplicate OpenFOAM or PhysicsNeMo issue was filed: the sampled accuracy
limitations do not establish a violated implementation contract, and the
odd-width spectrum defect is already tracked in PhysicsNeMo issue #2007 / PR
#2008. Its September 30 current-main recheck is recorded below.

### SU2 adapter clarification

Resolved v8.5.0 to `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`.
LICENSE.md and CUserDefinedSolution.cpp identify LGPL-2.1-or-later.
CUserDefinedSolution's constructor and methods intentionally abort until the user
implements them. Selecting USER_DEFINED_SOLUTION in a config alone does not
provide our MMS; an adapter patch and build are necessary. This is documented
extension scaffolding, not a newly discovered bug.
Source: https://github.com/su2code/SU2/blob/12eb826f049ef7f67df974dfcb44cf36ee07c0f8/Common/src/toolboxes/MMS/CUserDefinedSolution.cpp

### Current PhysicsNeMo API evidence

v2.2.1 resolves to `1b961314e42a0625502ba1592d25f706f1e02a24`.
The current ldc_pinns example (Apache-2.0 header) defines its PDE inline and uses
PhysicsInformer with autodiff. It is steady 2D, so cannot itself stand in for the
required transient 3D forced MMS. The adapter must explicitly add the third
coordinate, time derivative, forcing and periodic conditions.
Source: https://github.com/NVIDIA/physicsnemo/blob/1b961314e42a0625502ba1592d25f706f1e02a24/examples/cfd/ldc_pinns/train.py


### PhysicsNeMo reporting policy and interim decision

The pinned CONTRIBUTING.md permits issues for discussion, asks for tests and a
linked issue for code contributions, and describes fork-based PRs and sign-off.
The one-project-repository constraint is preserved; no additional fork is created.
A search for PhysicsInformer time-derivative issues found no match, but the source
explicitly warns that nonspatial derivatives are caller-supplied. We implemented
that contract and verified residuals. This does not warrant a defect report.
Training inaccuracies alone likewise do not show a framework bug. The completed matrix and reporting decision are recorded in
reports/upstream-disposition.md; no demonstrated framework defect was found.

Source: https://github.com/NVIDIA/physicsnemo/blob/1b961314e42a0625502ba1592d25f706f1e02a24/CONTRIBUTING.md

### Current repository and PhysicsNeMo follow-up (2026-09-28)

The Foundation 13 repository still resolves to the audited source commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90`; its current public open issue list
contains no issue matching this benchmark's high-gradient MMS or coded forcing.
SU2 v8.5.0 remains the experimental target, while the moving `master` branch
has advanced to `bc15466602a687d6fb796d5df7a12ce3fde0949a`; the existing Q&A
and pinned-version results are not silently re-labeled as main-branch tests.

PhysicsNeMo's latest release is v2.2.2 (`072465a1a56817f180f64dee8a4069a1612b2d9e`,
Apache-2.0); current main is `426f7552da4b4fa675e404e8a4f437e27681b668`.
An independent CPU reproducer confirmed open Issue #2007 on both snapshots:
the 33x33, wavenumber-5 spectrum differs by axis and fails transpose symmetry.
The correction is already proposed in [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008),
which is open and behind current main. We ran its modified function on the
reported odd/even shapes and verified the symmetry correction, but did not run
the full PhysicsNeMo suite. Since the concentration-aware benchmark uses even
uniform grids, this issue does not alter its current spectra; no duplicate
issue or code change is justified. Reproduction, source hashes, environment and
scope are recorded in
`evidence/upstream-refresh/physicsnemo-power-spectrum-odd-width-2026-09-28.json`.

The focused CPU reproducer is now checked in as
`tools/reproduce_physicsnemo_issue_2007.py`. With the unmodified source already
under `work/physicsnemo-source` and the recorded `work/physicsnemo-env`, run
`work/physicsnemo-env/bin/python -m tools.reproduce_physicsnemo_issue_2007`.
It emits `evidence/upstream-refresh/physicsnemo-issue-2007-reproduction.json`,
including the source-file SHA256, Torch version, even/odd axis-wave controls,
and deterministic transpose-symmetry checks. The reproduced file hash is
`13e7847c62b9285daafdf88307bd548e0f18e1f5d4fa0bf33f3552303deb8552`, which
matches the recorded v2.2.2 and current-main target file. This improves
reproduction of the existing issue; it is not a full upstream suite run and
does not justify a duplicate report.

The same tool also tested the exact PR #2008 head
`7407608723062dc11ba5332e9ff3774f42bb02d9` with `--expect-fixed`. The odd/even
axis-wave and transpose controls pass on that version; its source hash and
results are preserved in
`evidence/upstream-refresh/physicsnemo-pr2008-fix-validation.json`. This
confirms the existing patch resolves this focused counterexample, while leaving
full-suite and merge/review status unresolved.

To regenerate the focused fix-validation artifact, fetch only the target file
from the pinned PR head and run the same tool:

```sh
gh api 'repos/NVIDIA/physicsnemo/contents/physicsnemo/metrics/general/power_spectrum.py?ref=7407608723062dc11ba5332e9ff3774f42bb02d9' --jq .content \
  | python3 -c 'import base64,sys;sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))' \
  > /tmp/physicsnemo-pr2008-power_spectrum.py
work/physicsnemo-env/bin/python -m tools.reproduce_physicsnemo_issue_2007 \
  --source-file /tmp/physicsnemo-pr2008-power_spectrum.py --expect-fixed \
  --source-reference 'NVIDIA/physicsnemo PR #2008 head 7407608723062dc11ba5332e9ff3774f42bb02d9' \
  --output evidence/upstream-refresh/physicsnemo-pr2008-fix-validation.json
```

The related periodic-gradient concern is also already tracked: PhysicsInformer
Issue #2001 identifies the caller-facing periodic assumption, while #1852 and
open draft PR #1853 concern a lower-level nonperiodic mode. Our current MMS is
periodic, so these reports do not identify a defect in the present benchmark.
No additional boundary issue was filed.

Current target/default-branch heads and the focused SU2 duplicate searches are
summarized in `evidence/upstream-refresh/current-project-inventory-2026-09-28.json`.
That inventory is intentionally scoped; it does not claim that all open issues
in these large repositories were individually reviewed.

### Current PhysicsNeMo recheck (2026-09-30)

PhysicsNeMo `main` advanced to `eb8f95897eed9887295cb8110ba1017d2d670b58`.
We reran the focused odd-width reproducer against that exact current source:
Issue #2007 still reproduces on 33x33, while the exact existing PR #2008 head
passes the odd/even controls. The PR is still open and behind main, with review
required. No full upstream suite was run and no duplicate issue was filed; see
`reports/physicsnemo-refresh-2026-09-30.md` and the new structured artifacts.
This defect remains outside our even-grid benchmark cases.
