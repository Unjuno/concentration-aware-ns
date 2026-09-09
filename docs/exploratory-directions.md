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

The suggestion that continuum concentration entails particle alignment remains
unverified. Specify position versus velocity alignment, a molecular model, and
a limiting relation before testing it. Linearity and geometric alignment are
different properties. No present benchmark result establishes this implication.
