# Local affine incompressibility and impact boundaries — 2026-10-04

All four gradient-selected native cellPoint witnesses have interval-enclosed **nonzero divergence** in their decoded-node real-affine pieces. The interpolation derivative is constant on each piece. This concerns continuous point interpolation, not the finite-volume face-flux divergence or a failure of discrete mass conservation.

| Case | Signed affine divergence, approximately | Gradient-error lower bound from trace alone |
|---|---:|---:|
| n16, dt .001 | +0.8896697513 | 52.4054% |
| n32, dt .001 | -0.8194124394 | 48.2669% |
| n64, dt .001 | -0.4670880832 | 27.5135% |
| n32, dt .0005 | -0.8099874268 | 47.7117% |

Percent lower bounds round down from exact dyadic endpoints and normalize by the analytic reference-gradient peak upper bound. The divergence column is an approximate signed value; full rational enclosures are preserved. It is not normalized by reference divergence, which is zero. These trace-only bounds are weaker than the earlier full gradient-error bounds; they explain one unavoidable component rather than replacing them.

For a matrix G and any trace-free A, Cauchy–Schwarz gives

    ||G-A||_F >= |tr(G)|/sqrt(3).

Equivalently, the decomposition G=(tr(G)/3)I + (G-(tr(G)/3)I) is orthogonal in the Frobenius inner product. The reference manufactured solution is analytically divergence-free, so its gradient is trace-free at every point. The lower bound applies throughout the target idealized piece, including previously certified local balls. An affine field interpolating all four affinely independent vector nodes is unique; these recorded nodes therefore cannot simultaneously be interpolated by an affine field with zero divergence. This does not exclude nonlinear divergence-free interpolation through finitely many points, or a reconstruction that changes nodal values. No such correction is executed here.

If a point interpolant is used as an advection field, its divergence is the instantaneous logarithmic rate of the local flow-map volume Jacobian while trajectories remain in that smooth piece. Consequently volume preservation cannot be assumed from the discrete solver label alone. This is a conditional interpretation: this audit does not establish which OpenFOAM particle consumer uses this exact interpolant, integrate trajectories, or infer molecular alignment, particle shrinkage or a viscosity law.

## Project-specific disposition

- **OpenFOAM:** the captured local interpolation and its continuous derivative are verified. Classification: reconstruction limitation / evaluation-procedure gap. A cellPoint divergence-preservation contract has not been established; no source defect or new upstream issue follows. Next falsifier: identify actual interpolation contracts and a specific consumer, then compare its discrete flux constraint with its continuous reconstruction, without silently changing accepted inputs.
- **SU2:** the existing localized matrix has mixed inner-residual/accuracy verdicts. Its separately archived n32 CFL=100 first-step control converges, but does not establish full-horizon or n64 recovery. It uses a different representation and no captured cellPoint tetrahedra. These affine conclusions are not transferred to SU2. The existing source-time discussion remains the reporting route; a matched prospective convergence-control successor is still needed.
- **PhysicsNeMo:** archived sampled derivatives and the known spectrum issue/fix controls concern differentiable learned fields and different evaluation operators. No transfer of these tetrahedral trace bounds is established. Prospective acceptance limits and continuous/adaptive quality certification remain separate requirements; no duplicate spectrum issue is warranted.
- **OpenAI construction and physical hypotheses:** none of these approximation records identifies the continuum proof profile or supplies a molecular constitutive model. The prior proof-identity and physical-bridge obligations remain open.

Fresh default-branch reads of Foundation 13, SU2 and PhysicsNeMo match the previous audit pins (18870c24, bc154666 and b45a5c81). This does not claim that every issue/discussion or release has been re-audited. No external post is made on this finding because novelty plus a violated upstream contract has not been demonstrated.

Arb128 certificates at numerical source `b3ed2b7` and source/witness hashes are in `evidence/cell-point-affine-divergence-v1`. The complete four-case JSON reproduces byte for byte in a guarded same-host Git-directory-free selected export. Four controls cover isotropic strain, rigid rotation, sign invariance and degenerate geometry. No fresh-host exact equality is claimed for the raw signed-divergence enclosures.

Separately, hosted CI 37155563101 succeeds for publication 4d169bf4: all 371 tests, the three v2 analytic equality checks and the exact rational scalar checker pass. Its scalar JSON matches the local one byte for byte; executed merge and publication-head source/data closures agree. Those receipts are in `evidence/dyadic-scalar-hosted-v1`. This closes the previous scalar-hosted-check gap, not the broader goal.

The full local suite after adding divergence controls passes **375 tests, one skip, 89 subtests**. Current publication-head CI is separate from the earlier verified 371-test hosted run.
