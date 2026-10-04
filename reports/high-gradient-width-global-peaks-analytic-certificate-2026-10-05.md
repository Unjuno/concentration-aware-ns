# Exact continuum peaks for the frozen width-v1 MMS

## Result

For the frozen reference field

```text
h_m(q)=((1+cos(q))/2)^m,  N=4,  m in {1,2,4}
u=(chi_y sin(Nx)/N^2, -chi cos(Nx)/N, 0),  chi=h_m(y)h_m(z),
```

the exact continuum peaks at time `t` are

| `m` | `max |grad u|_F` | `max |curl u|` |
|---:|---:|---:|
| 1 | `sqrt(1025)/32 * exp(-t)` | `33/32 * exp(-t)` |
| 2 | `sqrt(257)/16 * exp(-t)` | `17/16 * exp(-t)` |
| 4 | `sqrt(65)/8 * exp(-t)` | `9/8 * exp(-t)` |

Each maximum is attained at `(x,y,z)=(pi/(2N),0,0)`. This closes the
continuous-reference-peak gap for all widths in the frozen OpenFOAM matrix.
It does not certify the solver field, its within-cell reconstruction, or the
sampled metrics used by the existing acceptance gates.

## Exact certificate

Let `s=sin(y/2)^2`, `r=sin(z/2)^2`. Then `s,r` range over `[0,1]` and
`h_m(y)=(1-s)^m`. For either coordinate, the exact chain rule is

```text
h'_m(q)^2 = (g'_m(s))^2 s(1-s)
h''_m(q) = g''_m(s)s(1-s) + g'_m(s)(1-2s)/2
g_m(s) = (1-s)^m
```

The squared gradient and vorticity each separate into a sine branch and a
cosine branch in `Nx`. The checker subtracts each branch from the claimed
squared peak and expands the difference in the tensor Bernstein basis on
`[0,1]^2`. All coefficients are exact nonnegative rationals. The certificate
bidegrees are `(2,2)`, `(4,4)`, `(8,8)` for `m=1,2,4`; in each sine branch
the minimum coefficient is zero, at the center attainment point. The cosine
branch minimum coefficients are strictly positive. These finite coefficient
checks prove the polynomial gaps are nonnegative on the entire square.

The complete coefficient tables and source/runtime hashes are in
[`high-gradient-width-global-peaks.json`](../evidence/tests/high-gradient-width-global-peaks.json).
Reproduce with:

```sh
work/reference-check-env/bin/python -m tools.check_high_gradient_width_peaks
work/reference-check-env/bin/python -m unittest tests.test_high_gradient_width_peaks -v
```

## Effect on the benchmark

This is a supplementary reference-side certificate. The frozen protocol's
same-grid FD2 denominators, resolution floor, solver thresholds, archived
cases, and `NOT_OBSERVED` width classifications remain unchanged. In
particular, a continuous analytic maximum does not replace the preregistered
grid-sampled comparison and is not evidence of molecular alignment, particle
position certainty, a phase transition, viscosity loss, or a physical
singularity.
