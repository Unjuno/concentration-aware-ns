# Primary-source audit

Updated 2026-10-02. Source observations, reproduced behaviors and unresolved
quality claims are distinguished below. This remains an interim audit.

## OpenFOAM Foundation 13

Inspected commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`.
License: GPL-3.0-or-later per source headers. Do not mix OpenCFD APIs into this
Foundation adapter.

- [Residual implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/cfdTools/general/solutionControl/convergenceControl/singleRegionConvergenceControl/singleRegionConvergenceControl.C): compares configured fields' initial residuals with absolute thresholds.
- [AMR implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C): candidate selection and consistency refinement must both be considered in interpreting maxCells.
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
| OF-01 | residual convergence with inaccurate local gradients | high-gradient matrix's configured standard gate passes all nine completed cases; AMR local velocity threshold fails all three; continuous peak and source-to-binary uncertainties remain | resolve diagnostic uncertainty and AMR causal factors before a defect claim |
| OF-02 | AMR accuracy under finite budgets | three caps completed; cap5000 exceeds requested cap by 440 cells, errors rise from 8.876% to 38.572%; coarse initialization/remap/flux attribution unresolved | isolate initialization/remapping/flux effects with matched controls |
| OF-03 | strict interpretation of maxCells | source describes approximate limit; no defect claim | report approximate semantics |
| SU-01 | conventional convergence with inaccurate local QoI | five-case matrix archived; temporal endpoint difference order 0.99916; case gates remain UNCERTAIN where every-step residual/quality criteria are unmet | strengthen converged time-step controls and continuous-peak bounds |
| SU-02 | MMS old-time forcing | pinned v8.5 behavior and first-order/BDF2 order reduction reproduced; maintainer agrees `t_n` source is not backward-Euler target-time evaluation and recommends explicit time levels | consider a narrow regression/example only after cross-consumer scope review; no global time shift |
| ML-01 | aggregate and peak accuracy disagreement | five-case sampling matrix complete; all gate outcomes uncertain | preregister thresholds in a future run, bound continuous peaks and assess optimization/seed effects |
| ML-02 | automatic time derivative assumption | x/y/z-only autodiff, explicit t input; documented API behavior | no defect report warranted |
| REF-01 | derivative/sampling artifacts mimic solver error | reproduced FD2 versus analytic/autograd differences | continuous-extremum uncertainty |
| REF-02 | forcing formula error | symbolic/C++/autograd checks passed in stated scopes | preserve per-solver time/assembly distinctions |

SU2 time-contract reproducer submitted as [Q&A 2890](https://github.com/su2code/SU2/discussions/2890).
OpenFOAM and PhysicsNeMo have no upstream defect report at this stage: observed
accuracy limitations do not yet establish a violated implementation contract.

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

## Live reporting-state verification — 2026-10-02

Read-only GitHub API checks confirm SU2 Discussion 2890 has two comments: the
September 13 maintainer analysis and our September 26 BDF2 control follow-up.
The maintainer identifies the lagged source-time behavior and recommends
separate stored-state and target-time semantics, while warning against treating
a global clock shift as a complete fix. SU2 issue 2353 remains open with eight
comments; its latest comment is our September 27 fixed-dt MAX_TIME restart-clock
control, with no later maintainer reply in that thread. These observations do
not broaden either finding beyond its pinned controls. OpenFOAM Foundation 13
and PhysicsNeMo v2.2.1 still have no demonstrated contract violation, so no
new upstream defect report is justified. Raw status fields and URLs are
recorded in
[`github-state-2026-10-02.json`](../evidence/upstream-review/github-state-2026-10-02.json).
