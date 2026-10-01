# Axis-tube concentration versus bounded-position probability

## Exact result in the linearized Gaussian model

Along the selected axis trajectory, the linearized volume-preserving map has
singular values

\[
Q^{C/2},\quad Q^{C/2},\quad Q^{-C},\qquad
Q=\frac{1-t}{1-t_0}\downarrow0,\quad C>0.
\]

Apply this map to an initially isotropic Gaussian displacement
\(X_0\sim N(0,\sigma^2 I)\). The covariance at time \(t\) is

\[
\operatorname{Cov}(X_t)
=\operatorname{diag}(\sigma^2Q^C,\sigma^2Q^C,
                      \sigma^2Q^{-2C}).
\]

The transverse radius \(r_\perp=\sqrt{X_1^2+X_2^2}\) has a Rayleigh
distribution. For any fixed radius \(R>0\),

\[
\mathbb P(r_\perp<R)
=1-\exp\!\left(-\frac{R^2}{2\sigma^2Q^C}\right)
\longrightarrow1.
\]

So this model does produce concentration toward the **infinite axis as a
geometric set**. But the independent axial coordinate has standard deviation
\(\sigma Q^{-C}\), which diverges. For a finite cylinder with the same fixed
transverse radius and fixed axial half-length \(L>0\), independence gives

\[
\mathbb P(r_\perp<R,\ |X_3|<L)
=\left[1-\exp\!\left(-\frac{R^2}{2\sigma^2Q^C}\right)\right]
  \operatorname{erf}\!\left(\frac{LQ^C}{\sqrt2\sigma}\right)
\sim \sqrt{\frac2\pi}\frac{L}{\sigma}Q^C
\longrightarrow0.
\]

Any fixed ball is contained in a finite axial slab, so its probability also
tends to zero. Indeed, for a ball of radius \(R\), the axial marginal alone
gives

\[
\mathbb P(|X_t|<R)
\le \mathbb P(|X_3|<R)
\le \sqrt{\frac2\pi}\frac{R}{\sigma}Q^C.
\]

This reconciles two statements that can sound contradictory: the transverse
distance to the axis tends to zero in probability, while the ensemble has no
increasing certainty about a bounded three-dimensional position. Its axial
spread grows as the transverse spread shrinks. The full covariance determinant
and Gaussian peak density remain constant.

## Scope

This is an exact probability calculation for a Gaussian pushed through the
linearized variational map, not a finite-packet theorem for the nonlinear
Navier–Stokes field. The Gaussian has unbounded support; the calculation does
not assert that the true flow is linear on that support. It adds no molecular
positions, collisions, orientation distribution, constitutive law,
phase-transition, or viscosity result. The underlying field's flow map is
itself conditional on classical smooth existence on each preterminal interval.

The calculation is reproduced by
python -m tools.check_alignment_uncertainty; exact symbolic identities and
the source hash are stored in evidence/tests/alignment-uncertainty.json.
The separate volume-preserving density bound in
incompressible-position-uncertainty.md applies to arbitrary absolutely
continuous passive-tracer laws under its stated hypotheses. Neither statement
establishes that the pinned OpenAI candidate satisfies the full
Navier–Stokes candidate theorem.

This separation is also consistent with the announcement's stated model
boundary: it describes Navier–Stokes as a continuum model and says particle
tracking would be needed beyond its breakdown; it supplies no particle
ensemble law or molecular arrangement. See the
[OpenAI announcement](https://openai.com/index/navier-stokes-solution/).
