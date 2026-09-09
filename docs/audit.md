# Primary-source audit

Inspected 2026-09-09. These are source observations, not reproduced failures.

## OpenFOAM Foundation 13

Inspected commit: `18870c24d21c6b982e2cdec27b2f59738cca5f90`.
License: GPL-3.0-or-later per source headers. Do not mix OpenCFD APIs into this
Foundation adapter.

- [Residual implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/cfdTools/general/solutionControl/convergenceControl/singleRegionConvergenceControl/singleRegionConvergenceControl.C): compares configured fields' initial residuals with absolute thresholds.
- [AMR implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C): candidate selection and consistency refinement must both be considered in interpreting maxCells.
- [Source hook](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/fvModels/general/codedFvModel/codedFvModel.H): coded fvModel is an integration candidate; forcing sign and units need execution tests.
- [Reporting instructions](https://github.com/OpenFOAM/OpenFOAM-13): README directs bug reports to bugs.openfoam.org.

## SU2

Candidate release: v8.5.0, resolved through GitHub releases API. Immutable commit
pin and license text review remain TODO.

- [Configuration](https://github.com/su2code/SU2/blob/v8.5.0/config_template.cfg): includes MMS_INC_NS and USER_DEFINED_SOLUTION. BODY_FORCE_VECTOR alone is constant and insufficient for the proposed varying force.
- [Convergence documentation](https://su2code.github.io/docs_v7/Solver-Setup/): residual and coefficient stopping criteria; verify against selected version.

## NVIDIA PhysicsNeMo

Candidate release: v2.2.1, resolved through GitHub releases API. Immutable commit
pin and current license/dependency review remain TODO.

- [Archived symbolic repository](https://github.com/NVIDIA/physicsnemo-sym): upstreamed into NVIDIA/physicsnemo; API changes include inline PDE definitions. Old repository uses Apache-2.0.
- [Historical Taylor–Green example](https://docs.nvidia.com/physicsnemo/25.08/physicsnemo-sym/user_guide/intermediate/moving_time_window.html): Re=500, spectral reference, average TKE evaluation. This is historical example evidence, not proof of current code behavior.

## Candidate register

| ID | Candidate | Classification now | Next evidence |
|---|---|---|---|
| OF-01 | residual acceptance with inaccurate local gradients | hypothesis / evaluation gap | forced solution runs and grid study |
| OF-02 | AMR constraints leave local concentration unresolved | hypothesis / configuration limitation | candidate counts, budget sweep, uniform control |
| OF-03 | interpreting maxCells as a strict stopping-count equality | audit instrumentation risk | actual refinement/consistency trace |
| SU-01 | conventional convergence with inaccurate local QoI | hypothesis | independent same-problem runs |
| ML-01 | average energy agrees while peaks do not | hypothesis / evaluation gap | current framework training and held-out peak checks |
| REF-01 | derivative/sampling artifacts mimic solver error | confounder | independent derivatives and extrema |
| REF-02 | source units/sign errors mimic solver error | confounder | analytic residual and simple forcing test |

No upstream submission yet: no solver reproducer or completed duplicate search.

### SU2 adapter clarification

Resolved v8.5.0 to `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`.
LICENSE.md and CUserDefinedSolution.cpp identify LGPL-2.1-or-later.
CUserDefinedSolution's constructor and methods intentionally abort until the user
implements them. Selecting USER_DEFINED_SOLUTION in a config alone does not
provide our MMS; an adapter patch and build are necessary. This is documented
extension scaffolding, not a newly discovered bug.
Source: https://github.com/su2code/SU2/blob/12eb826f049ef7f67df974dfcb44cf36ee07c0f8/Common/src/toolboxes/MMS/CUserDefinedSolution.cpp
