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

## 2026-10-02 source-level qualification

I fetched the five implicated files from the exact observed live-main commit
`83d6a337eecfc70e215ed1978af8dba9a38580fb` and rechecked their hashes. Both
low-level implementations are explicit: `uniform_grid_gradient_torch` calls
its stencils periodic and uses `torch.roll`, while
`spectral_grid_gradient_torch` says it assumes periodic boundaries. Therefore
the issue body's broad implication that the periodic assumption is undocumented
throughout the implementation is too strong. The narrower public-interface
concern remains: `GradientsFiniteDifference` and `PhysicsInformer` do not state
that selecting these backends requires periodic data, and the wrapper offers no
boundary-mode option. The finite-difference and spectral tests compare only the
interior after removing two cells at each edge, so those tests do not establish
boundary correctness for non-periodic fields.

An exact source-formula check makes the limitation concrete without relying on
a simulation. For samples `f_i=i*dx`, the second-order periodic central
stencil gives derivative `(f_1-f_{N-1})/(2*dx)=(2-N)/2` at the first point,
although the interior derivative is `1`. This is expected for a periodic-wrap
stencil applied to a non-periodic ramp; it does not show that the implementation
violates its stated periodic contract. PyTorch is unavailable in this
environment, so this refresh did not execute the upstream tensor implementation.
Issues #2001 and #1852 and draft PR #1853 remain the appropriate existing
records; no duplicate report was filed.

The exact fetched-file hashes and formula calculation are recorded in
`evidence/upstream-refresh/physicsnemo-boundary-source-check-2026-10-02.json`.
