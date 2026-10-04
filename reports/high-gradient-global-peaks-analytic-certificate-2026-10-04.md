# Exact global local-observable peaks for the shared high-gradient MMS

## Result

For the frozen Fourier-envelope manufactured field at `N=4`, the exact
continuous-domain maxima at time `t` are

```text
max |grad u|_F = (sqrt(65)/8) exp(-t)
max |curl u|   = (9/8) exp(-t)
```

Both are attained at `x=pi/(2N)`, `y=z=0`. This closes a reference-field
uncertainty: earlier local-peak receipts used the value at this point only as
a lower bound and explicitly left the global continuum peak unproved. The
result applies to the exact analytic reference only; it says nothing about a
solver's interpolated or within-cell field.

## Derivation and certificate

Write `s=sin(y/2)^2` and `r=sin(z/2)^2`, so `s,r in [0,1]`, and
`g(s)=(1-s)^4`, `chi=g(s)g(r)`. The chain rule gives the exact identities

```text
(d/dy g)^2 = 16 s (1-s)^7
d²g/dy²   = 2 (1-s)^3 (8s-1).
```

Set `chi_y`, `chi_z`, `chi_yy`, and `chi_yz` for the corresponding spatial
derivatives. The velocity-gradient Frobenius norm and vorticity norm split
their independent `x` dependence:

```text
|grad u|_F² = exp(-2t) [A(s,r) sin²(Nx) + B(s,r) cos²(Nx)]
|curl u|²   = exp(-2t) [C(s,r) sin²(Nx) + D(s,r) cos²(Nx)]

A = chi² + (chi_yy² + chi_yz²)/N⁴
B = (2 chi_y² + chi_z²)/N²
C = (chi - chi_yy/N²)² + chi_yz²/N⁴
D = chi_z²/N².
```

At `N=4`, each of the four target gaps `65/64-A`, `65/64-B`, `81/64-C`,
and `81/64-D` is a bivariate polynomial of degree at most `(8,8)`. The
checker expands each in the tensor Bernstein basis on `[0,1]²`. Every exact
rational coefficient is nonnegative. Since these basis functions are
nonnegative and sum to one, all four gaps are nonnegative throughout the
square. At `(s,r)=(0,0)`, `A=65/64` and `C=81/64`; choosing `Nx=pi/2` attains
both maxima, proving the bounds sharp.

The machine-readable certificate stores all 324 rational Bernstein
coefficients, the two derivative identities, and provenance. Reproduce it
with:

```sh
work/reference-check-env/bin/python -m tools.check_high_gradient_global_peaks
work/reference-check-env/bin/python -m unittest tests.test_high_gradient_global_peaks -v
```

The checker used Python 3.14.5 and SymPy 1.14.0. A deterministic 200,000-point
sample through the independent NumPy field evaluator stayed below both exact
maxima and the analytic attainment point reproduced them in floating point;
these are sanity checks, not the proof. The proof is the exact polynomial
identity plus the nonnegative Bernstein coefficients.

## Effect on existing gates

Existing solver gates remain unchanged. They compare the solver's sampled
derivative peak to the exact reference sampled on the same mesh, which is the
appropriate denominator for the current finite-grid diagnostic. The new
global peak supplies a separate continuum target, so a future report can
distinguish reference-grid peak undersampling from solver error without
silently changing preregistered thresholds or historical verdicts. No
continuous maximum of a numerical solver field is certified here.

Receipt: [`high-gradient-global-peaks.json`](../evidence/tests/high-gradient-global-peaks.json).
