# Analytic self-audit — 2026-09-09

The claims below are derived independently of accepting a solver's numerical
output. Computations test implementation behavior; they do not establish the
mathematical assumptions or the validity of a physical model.

## Uniform SU2 control: what follows, and what does not

Assume the nondimensional incompressible equations

    ∂t u + (u·∇)u = -∇p + νΔu + f,    ∇·u = 0.

For u=(1+t²,0,0), p=0 and f=(2t,0,0), all spatial derivatives vanish.
The continuous equation reduces exactly to du_x/dt=2t with u_x(0)=1.
At t_k=k h the exact value is 1+k²h².

If a completed update uses (U_k-U_(k-1))/h=2(k-1)h, summing the arithmetic
series gives U_k=1+h²k(k-1), with error -k h²=-t_k h.
If it uses (U_k-U_(k-1))/h=2kh, the result is U_k=1+h²k(k+1), with error
+k h²=+t_k h. Both are first-order consistent as h tends to zero. Therefore:

- Agreement with the first recurrence demonstrates old-time forcing in this
  configuration; it does not demonstrate divergence or loss of first-order
  consistency.
- Changing the source time and obtaining the second recurrence is a causal
  intervention on this source-time behavior, not a proof of a general fix.
- Neither recurrence is the exact continuous solution at finite h. Calling the
  second result "exact" would be incorrect.
- If history labels the output (k-1)h, comparison with u((k-1)h) instead of u(kh)
  changes the apparent error. Output labels alone cannot define the physical
  time of an already completed update.
- A backward-Euler residual for the state does not logically force every source
  to be implicit. An intentionally explicit source would also explain this
  recurrence. Whether SU2's MMS interface promises the updated time is a contract
  question that should be made explicit in any upstream report.

The actual pinned source initializes U at t=0, advances a dual-time residual
between U^n and U^(n+1), and passes TimeIter*h to GetMMSSourceTerm. The control
results corroborate this chain with errors below 2.7e-11 and converged residuals.
This is stronger than output inspection alone, but is limited to single-zone,
constant time step, first-order integration, no restart, and the custom MMS.
It does not establish effects on production cases that do not use this interface.

Current classification: reproduced source-time behavior and potential MMS time
contract mismatch. A blanket claim of a defective time integrator is unsupported.

## Localized calibration: smoothness and the peak comparison

Let ψ=exp(-t + Σ_j(cos(x_j-π)-1)/σ²), a=(1,2,3), u=∇ψ×a with fixed σ>0.
All factors are smooth and periodic, ∇·u=∇·curl(ψa)=0, and p=0 with
f=∂t u+(u·∇)u-νΔu makes the continuum equation an identity. On a compact
periodic spatial domain every derivative is finite at every finite time. This
calibration cannot itself establish blow-up.

At x=(π,π,π), ∇ψ=0 and Hess ψ=-(exp(-t)/σ²)I. Hence
||∇u||_F=√28 exp(-t)/σ² and ||curl u||=√56 exp(-t)/σ² there. These are lower
bounds on global maxima, not necessarily their exact values. If a reported
nonnegative peak m is below a known lower bound L for the true peak M, then
1-m/M ≥ 1-m/L. This justifies a one-sided underestimation bound; it cannot certify
accuracy when m≥L.

The observed FD2 peak is a property of the numerical field plus our sampling and
postprocessing. Even an exact sampled velocity has finite-difference error.
Consequently the 32³ aggregate/local discrepancy supports a diagnostic coverage
example, not a solver defect or real-world danger. The incomplete acceptance gate
must not be upgraded merely because the example is persuasive.

## Separation from the OpenAI construction

The smooth forced calibration and the uniform time control are not numerical
realizations of the pinned OpenAI construction. Its theorem predicates, proof
closure, construction, scaling and finite truncations require their own audit.
No result here establishes or refutes that theorem. A continuum singularity also
does not imply molecular alignment without an additional microscopic model and
a defined alignment observable.

## Continuum energy independent of grid sampling

For the localized calibration let β=1/σ², z=exp(-2β)I₀(2β) and
v=exp(-2β)[I₀(2β)-I₂(2β)]/2, where I_j is the modified Bessel function.
Separation of the three periodic integrals and oddness of the mixed sine terms
give mean |u|²=28 β² exp(-2t) v z². The Bessel recurrence
I₀(2β)-I₂(2β)=I₁(2β)/β therefore gives

    mean kinetic energy = 7 β exp(-2t) [exp(-2β)I₁(2β)] [exp(-2β)I₀(2β)]².

This is the spatial mean of |u|²/2 over the 2π-period cube, not the total integral.
The factor 28 comes from |a|²=14 and the cross-product identity, after isotropic
integration. tools/reference_energy.py evaluates the scaled Bessel factors to
avoid overflow. Independent scalar quadrature checks the separated integrals;
ordinary floating-point agreement is not an interval-certified error bound.
