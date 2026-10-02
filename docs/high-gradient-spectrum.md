# Exact Fourier spectrum of the high-gradient MMS

This reference is derived from the finite Fourier series, independently of a
sampled FFT. The periodic cube is `[0,2*pi)^3`, so wavevectors are integer
triples and the shell width used here is one.

Write

```text
g(y)=((1+cos(y))/2)^4 = sum_{m=-4}^4 c_m exp(i*m*y),
chi(y,z)=g(y)g(z),
psi=exp(-t) chi sin(N*x)/N^2,
u=(psi_y,-psi_x,0).
```

The real, symmetric coefficients are
`c_0=35/128`, `c_{±1}=7/32`, `c_{±2}=7/64`,
`c_{±3}=1/32`, and `c_{±4}=1/256`. For every pair `(m,n)`, the two
streamwise modes `k_x=±N` have a combined kinetic-energy contribution

```text
exp(-2t) c_m^2 c_n^2 (m^2/(4 N^4) + 1/(4 N^2)).
```

They belong to shell
`floor(sqrt(N^2+m^2+n^2)+1/2)`, matching the nearest-integer radial binning
in `tools.metrics.diagnostics`. Summing these finitely many terms gives the
exact continuum shell energy for this field. The total equals the volume-mean
kinetic energy by Parseval.

Reproduce the comparison with a resolved cell-centered FFT for `N=4,8,16`:

```sh
uv run --with pytest --with-requirements requirements-verification.txt -- python -m pytest -q tests/test_high_gradient_spectrum.py
```

The cross-check revealed and corrected an initial factor-of-two error in the
nonzero complex Fourier coefficients of `g`; the corrected coefficients agree
with both the existing symbolic cosine expansion and sampled FFT shell sums to
floating-point tolerance. This is a useful independent-reference failure caught
before publication. It does not validate a solver spectrum or a nonuniform AMR
reconstruction.
