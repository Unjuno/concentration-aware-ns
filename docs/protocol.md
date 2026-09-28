# Verification protocol — draft, not yet frozen for execution

## Reference construction

Use the periodic cube [0, 2*pi)^3 with constant density 1 and viscosity nu>0.
For width sigma>0, let

    psi(x,t) = A(t) exp(sum_i(cos(x_i-c_i(t))-1)/sigma^2)
    a = (1,2,3)
    u = curl(psi a) = grad(psi) cross a
    p = 0
    f = partial_t u + (u dot grad)u + grad p - nu laplacian(u)

This defines a smooth periodic divergence-free field. It is a manufactured
forced solution, not unforced turbulence or a singular solution. Fix sigma for
each refinement sequence. Use constant A and c for the steady case; prescribe
smooth nonconstant A or c for the time-dependent case. Freeze numerical values
before any production run, including time horizon and a pressure gauge.

Independently differentiate the analytic construction, then verify against a
separate differentiation implementation. Check divergence, forcing sign, volume
weighting, density conventions, initialization and periodic boundaries. Forcing
must be based on the reference field, not the computed field. Validate a
nontrivial transient case so exact initialization cannot mask time-integration
errors. A second reference/derivative implementation is still TODO.

An additional analytic stress-test candidate isolates small velocity amplitude
from large local derivatives. On the same periodic cube, set

    chi(y,z)=((1+cos(y))/2)^4 ((1+cos(z))/2)^4
    psi_N=exp(-t) chi sin(N x)/N^2,  u_N=curl((0,0,psi_N))
    f_N=partial_t u_N+(u_N dot grad)u_N - nu Delta(u_N),  p=0.

For positive integer N this is smooth, periodic and divergence-free. The
analytic bound `||u_N||_infinity <= exp(-t)*(1/N + 2/N^2)` tends to zero, while
`partial_x (u_N)_y = exp(-t) chi sin(N x)` attains magnitude `exp(-t)` at
`(x,y,z)=(pi/(2N),0,0)`. Thus value/energy agreement alone cannot imply
gradient accuracy. This is a verification stress case, not a singularity model.
The symbolic checker derives the exact forcing identity, divergence, vorticity,
selected peak and Fourier-orthogonality volume means for finite `N=4,8,16`:
`tools/check_high_gradient_mms.py`. It has not yet been run through OpenFOAM,
SU2 or PhysicsNeMo, and no solver gate failure or acceptance threshold is
claimed. The original unrun OpenFOAM matrix is preserved in
`protocols/high-gradient-of13-v1.json`. The active six-case successor and its
reference-only derivative-resolution audit are in
`protocols/high-gradient-of13-v2.json` and
`evidence/tests/high-gradient-fd2-resolution-floor.json`, separately from the
existing Gaussian concentration case.
An independent numerical formula comparison is also provided:
`tools/high_gradient_reference.py` evaluates derivatives from the finite
Fourier coefficients, while `tools/check_high_gradient_reference.py` constructs
the potential and differentiates it directly with SymPy. Their u, gradient,
vorticity and forcing values agree to below `1e-10` at 65 seeded points for
each N. This checks the two formula evaluators, not OpenFOAM's equation sign or
its C++ source assembly.

## Experimental matrix

- At least three successively finer spatial grids at fixed sigma and sufficiently
  small dt. Starting candidate: 32^3, 64^3, 128^3; revise before freezing if needed.
- At least three dt values at fixed fine mesh and common physical output times.
  Separate temporal and spatial error; do not refine both together and call it
  independent convergence. Check CFL/stability feasibility before freezing dt.
- Repeat at narrower sigma only as distinct sequences, not mesh refinement.
- Compare limited-AMR cases with sufficiently resolved uniform-grid controls.
- For ML, distinguish training samples, evaluation grids and time windows;
  record multiple seeds, optimizer budget and independent held-out coordinates.
  Do not reinterpret an evaluation-grid sweep as a training convergence study.

## Quantities and interpretation

Record volume-weighted velocity L2 error, energy, max Frobenius norm of grad(u),
max magnitude of curl(u), periodic peak location/set distance, shell energy
spectrum and local-region error. Treat equivalent multiple peaks as a set.
Evaluate analytic values both at solver sample sites and against independently
resolved continuous extrema to separate sampling and derivative error.
AMR/nonuniform samples require a documented spectral reconstruction; otherwise
mark the spectrum unavailable rather than applying a uniform-grid FFT directly.

Keep ordinary solver convergence separate from time-horizon completion. For
transients, an inner-loop convergence flag does not mean the physical solution
has reached the requested evaluation time. Record the exact criterion and fields.

AMR state must include requested refinement, actual cell counts/levels, blocked
candidates where observable, protection/consistency constraints and budget.
Budget equality alone does not establish saturation or inaccurate results.

## Decision contract

Before production, freeze absolute/relative tolerances, error normalization,
near-zero handling, evaluation times, metrics, seeds and required evidence.
Current code uses supplied per-metric tolerances; **no tolerances are frozen yet**.

Report independent fields:

- standard_acceptance: PASS / FAIL / UNCERTAIN
- local_quality: PASS / FAIL / UNCERTAIN
- hypothesis: REPRODUCED / NOT_OBSERVED / UNCERTAIN

REPRODUCED requires verified standard acceptance and local failure with adequate
independent reference and resolution evidence. NOT_OBSERVED is limited to the
tested matrix. A resolved finer grid does not erase a coarse-grid discrepancy;
classify that discrepancy as underresolution unless stronger evidence supports
another cause. A software defect needs a violated contract, not just a failed
accuracy threshold. Uncertainty and unperformed runs never become PASS.

## Per-run evidence

Source commit, patch, solver version, build/container digest, platform, input
hashes, commands, exit status, raw logs, physical end time, sampling geometry,
metric definitions, reference checks, resolution matrix and uncertainty budget.
The v2 JSON checker binds required review flags to hashed evidence files and
uses error intervals, including one-sided bounds. Human/source review is still
required to establish the validity of those artifacts and bounds. See
docs/acceptance-gate-v2.md; a matching hash is not scientific certification.

## Optional independent formula checks

Install requirements-verification.txt in an isolated environment and run
`python3 -m tools.check_reference_symbolic`. This differentiates the potential
symbolically rather than reusing the hand-derived derivatives.
`python3 -m tools.check_openfoam_force` compiles the generated codeAddSup body
against actual OpenFOAM vector types, with a mock mesh/equation and varying cell
volumes. It checks formula/assembly equivalence. A pinned-source audit now
traces the Foundation 13 `codedFvModel` callback through
`fvModels().source(U)`, the
`incompressibleFluid` momentum equation, matrix subtraction and Euler `ddt`
assembly. It confirms that `source[cell] -= V*f` contributes the intended
positive `+f` on the physical right-hand side, and that the mock's
`-eqn.source()/V` extraction has the right sign. This is a static source-level
result, not a live solver run; runtime integration, pressure coupling and the
numerical time-discretization remain unverified. See
`reports/openfoam-source-sign-audit-2026-09-28.md` and its pinned evidence JSON.
Run the compile check when the n16 study case and OpenFOAM container are usable.

The exact Hessian at the concentration center also supplies one-sided analytic
lower bounds on continuous gradient and vorticity maxima; see tools/peak_bounds.py.
These can establish underestimation by a reported sampled FD2 peak, but cannot
establish a quality PASS or separate solution error from postprocessing error.
