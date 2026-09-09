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
The current JSON checker checks required evidence flags and reported errors;
human/source review is required to establish those flags from real artifacts.
