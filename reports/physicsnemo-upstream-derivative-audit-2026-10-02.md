# PhysicsNeMo upstream derivative-path audit

Checked: 2026-10-01 21:43 UTC  
Repository: `NVIDIA/physicsnemo`  
Benchmark pin: `1b961314e42a0625502ba1592d25f706f1e02a24` (v2.2.1 line)  
Live main observed: `83d6a337eecfc70e215ed1978af8dba9a38580fb`  
License: Apache-2.0.

## Existing boundary-gradient reports

Three live upstream records cover the grid-gradient boundary concern:

- Issue [#2001](https://github.com/NVIDIA/physicsnemo/issues/2001) reports that `GradientsFiniteDifference`, `GradientsSpectral`, and `PhysicsInformer` expose periodic-wrap derivatives without clearly warning non-periodic users. It is open, unassigned, and has no labels as of this check.
- Issue [#1852](https://github.com/NVIDIA/physicsnemo/issues/1852) requests an opt-in one-sided non-periodic mode for lower-level uniform/rectilinear grid derivatives. It is open and marked stale/needs-triage.
- Draft PR [#1853](https://github.com/NVIDIA/physicsnemo/pull/1853) implements a non-periodic grid-gradient mode and remains open/draft; it is not merged.

The project `CONTRIBUTING.md` invites contributors to start with an issue to
discuss a proposal, in part because similar work may already be underway.
Accordingly, no duplicate issue or PR was filed. The live issue bodies,
contribution guidance, repository metadata and observed main SHA are summarized
in `evidence/upstream-refresh/physicsnemo-derivative-boundary-audit-2026-10-02.json`.

## Applicability to this benchmark

The audited benchmark does **not** call the grid finite-difference or spectral
gradient backends for its PINN training residual or local derivative
measurements. The frozen training script constructs `PhysicsInformer` with
`grad_method='autodiff'`; local velocity-gradient metrics use PyTorch autograd.
The case is periodic on `[0, 2π)^3`. The historical pin is PhysicsNeMo v2.2.1,
commit `1b961314…`; the live main observed above is a later source state and is
not substituted for the historical run environment.

Thus issue #2001 is relevant as framework guidance for non-periodic users, but
it does not explain or invalidate this benchmark's periodic autograd results.
No defect is reproduced on our chosen path and no new upstream report is
warranted. The separate PhysicsNeMo quality verdict remains `UNCERTAIN` because
continuous peak errors are not globally certified and the local threshold was
not preregistered for this solver. This audit does not imply blow-up or a
physical/material consequence.
