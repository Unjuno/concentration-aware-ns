# Exploratory directions under the expanded objective

The user authorizes following additional potentially important findings while
retaining the original three-project benchmark. Novelty is unverified until
checked against prior work; candidate ideas are not discoveries by designation.

## Certifying reconstructed-field peaks

The exact reference peaks in reference-global-peaks.md suggest an extension:
certify the continuous peak of a specified numerical reconstruction, then compare
it with the exact reference. This targets the current sampling uncertainty.

For tensor fields A and B on the same domain with finite sup norms,

    |sup_x ||A(x)|| - sup_x ||B(x)||| <= sup_x ||A(x)-B(x)||.

Proof: the triangle inequality gives ||A(x)|| <= ||B(x)|| + ||A-B||_infinity;
take the supremum and repeat with A and B exchanged. This is an elementary bound,
not a new mathematical result. A small peak discrepancy provides no converse
bound on the field error.

For a differentiable reconstructed tensor A and a sample set of covering radius
rho, if ||A(x)-A(y)|| <= L distance(x,y), then its continuous norm peak P obeys

    max_samples ||A|| <= P <= max_samples ||A|| + L rho.

Apply the Lipschitz bound to a nearest sample and take the supremum. A certified
implementation additionally requires valid domain coverage, a rigorously bounded
L and outward-rounded arithmetic. For Fourier reconstructions, coefficient sums
can bound derivatives, but floating-point FFT coefficients alone do not certify
the original solver field. Reconstruction error remains a separate question.

Next bounded investigation: derive usable coefficient bounds for the existing
periodic spectral reconstruction and assess whether interval widths can resolve
the preregistered tolerances. Do not substitute these bounds for the unfinished
SU2 matrix or automatically upgrade current gates.

## Molecular alignment hypothesis

For isotropically distributed infinitesimal continuum directions, the selected
local flow derivative does yield a model-dependent angular-event probability
that tends to one near the singular time; see
[`particle-position-probability.md`](particle-position-probability.md). Its
determinant-one map preserves a centered Gaussian's peak density and entropy,
so directional alignment does not imply spatial concentration. The extension
to finite particles or molecules remains unverified. It needs a microscopic
model, an observable, and an effective bridge to the continuum flow.

## Small-amplitude, large-gradient perturbations

The independent porous-wall study describes a high-frequency radial
oscillation in the OpenAI construction that changes a shear quantity by order
one while changing the profile and moments by order `1/N`. This suggests a
useful analytic stress test for concentration-aware verification: low-order
averages or field-amplitude agreement need not control local derivatives. The
paper's reduced numerical problem is not evidence that the OpenAI proof is
wrong; its precise comparison must be audited against the original hypotheses
before using it to make any such claim.

The scale separation itself has an elementary model. With logarithmic
coordinate `s=log X`, a compactly supported smooth envelope `chi(s)` that is
identically one on a nonempty interval, and
`r_N(s)=N^(-1) chi(s) sin(Ns)`,

    ||r_N||_infinity <= ||chi||_infinity/N,
    d r_N/ds = chi(s) cos(Ns) + N^(-1) chi'(s) sin(Ns).

Thus the perturbation vanishes uniformly while its first derivative does not
converge uniformly to zero. Its second derivative includes a term of size
`N*chi(s) sin(Ns)`. This does not show that any solver's residual or ordinary
QoI passes while its gradient fails; it only proves why that implication needs
an independent derivative estimate. A future MMS case can use a *fixed*
finite `N` family with analytic forcing and compare value, gradient and Hessian
errors across grids, then separately test whether a preregistered coarse gate
misses those errors. Do not infer a singular limit by sending `N` to infinity.
