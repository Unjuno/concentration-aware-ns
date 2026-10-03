# AMR derivative error: representation floor and cell-mean mismatch

## Result

The archived first-refinement events contain two opposing changes that the
total integrated derivative error alone obscures. Refinement reduces the best
possible error of a cellwise-constant derivative representation. At the same
instant, the reconstructed derivative departs further from the exact
child-cell mean. At n=64, the gradient representation floor falls from
13.8870% to 7.0390%, while the mean mismatch rises from 1.6132% to 12.1187%.
Their combined relative L2 error is 13.9804% before mapping and 14.0147%
afterward. Similar totals therefore do not mean that their components stayed
similar.

This is a retrospective decomposition of specified reconstructed tensors,
not an AMR quality verdict, a defect finding, or a new solver execution.

## Exact identity and analytic integration

On each retained cube K let D(x) be the exact MMS velocity gradient, let D_K
be its exact volume mean, and let G_K be any constant reconstructed tensor.
The zero-mean property `integral_K (D-D_K) = 0` gives

    integral_K |G_K-D|_F^2
      = |K| |G_K-D_K|_F^2 + integral_K |D-D_K|_F^2.

Summing over the selected cubes separates the mean mismatch from the
unresolved within-cell variation. The second term is a lower bound for every
cellwise-constant tensor on this partition and is attained by `G_K=D_K`.
The same identity holds for curl. Taking curl from a component-first tensor
is a linear contraction, so the mean exact curl is the contraction of D_K.
Neither identity requires G_K to be the derivative of a continuous velocity
field.

The known reference uses `g(q)=((1+cos(q))/2)^4`, frequency N=4 and amplitude
`exp(-0.002)`. The average of each Fourier mode on a cube interval is its
center phase multiplied by `sinc(k*h/2)`. Products of finite Fourier sums
give exact formulas for the means of `|grad(u)|_F^2` and `|curl(u)|^2`; the curl
energy includes the `g*g''` cross term. The formulas are evaluated in floating
point, rather than with interval arithmetic. The resulting total error is
checked against the independently computed tensor Gauss-Legendre integrals
saved on October 2.

## Recomputed three-resolution data

All rows use the same physical cube region `[pi/4,7*pi/4]^3`, 42.1875% of the
periodic domain. Geometry checks confirm that the retained whole cubes lie
inside this region and have the expected cubic refinement widths. Values are
relative L2 percentages, normalized by the integrated exact derivative norm
on this region. Components combine through the sum of their **squares**.

| Base n | Stage | Gradient floor | Gradient mean mismatch | Gradient total | Curl floor | Curl mean mismatch | Curl total |
|---:|---|---:|---:|---:|---:|---:|---:|
| 16 | preMap | 52.1177% | 20.8564% | 56.1359% | 54.1326% | 24.4392% | 59.3938% |
| 16 | mapped | 27.4741% | 46.7833% | 54.2540% | 28.6636% | 52.3918% | 59.7202% |
| 32 | preMap | 27.4187% | 6.1459% | 28.0990% | 28.6273% | 7.2975% | 29.5427% |
| 32 | mapped | 13.9737% | 24.1038% | 27.8614% | 14.5740% | 27.6524% | 31.2579% |
| 64 | preMap | 13.8870% | 1.6132% | 13.9804% | 14.5184% | 1.9052% | 14.6428% |
| 64 | mapped | 7.0390% | 12.1187% | 14.0147% | 7.3317% | 14.0522% | 15.8499% |

Before mapping, the representation floor supplies 86.20%, 95.22% and 98.67%
of the squared gradient error at n=16/32/64. After mapping it supplies only
25.64%, 25.15% and 25.23%. For curl the corresponding fractions are
83.07/93.90/98.31% before and 23.04/21.74/21.40% after. The archived mapped
velocity fields equal parent-value injection in the earlier same-run audit;
the derivative mean mismatch reported here additionally depends on the
selected reconstruction and the inherited velocity error. It is not a
measurement of mapping truncation error alone.

The mapped one-ring least-squares alternative shares the same mathematical
floor and gives gradient mean mismatches of 46.8460%, 24.1825% and 12.1849%.
Its curl mean mismatches are 52.4958%, 27.7351% and 14.1116%. The difference
between the two selected operators is small relative to the mismatch in these
archives; that does not validate every possible reconstruction.

## Verification and replay

The new analyzer verifies each raw archive hash against both its run manifest
and the saved quadrature artifact. It reads the captured cell and internal
face data, reconstructs the uniform preMap centered/Gauss derivative and the
mapped face-based Gauss and least-squares derivatives, then evaluates the
closed-form moments on the retained cubes. All 18 comparisons (gradient and
curl for nine stage/operator rows) agree with saved order-8 quadrature within
`8.33e-16` in absolute relative-L2 ratio. This checks archived numerical
postprocessing, not the solver or its instrumentation.

Tests compare the Fourier moments against independent real-space
differentiation of `((1+cos(q))/2)^4` followed by order-12 tensor quadrature
at frequencies 1, 4 and 7. Further controls check exact projection attaining
the floor, a perturbation with known mismatch energy, nested-cube moment
conservation, and rejection of invalid geometry/nonfinite tensors. Test and
clean-export results are recorded separately from the scientific quantities.

```sh
uv run --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_amr_derivative_projection
```

Machine-readable results and all source/protocol/archive hashes are in
[`openfoam-amr-derivative-projection-2026-10-03.json`](../evidence/tests/openfoam-amr-derivative-projection-2026-10-03.json).
The n=64 archive is reconstructed from its published split parts when absent;
n=16 and n=32 archives are tracked. The n=16 original run did not serialize its
protocol hash; a current replay hash cannot repair that historical limitation.
Existing archived evidence is preserved. The n=128 operator and the separate
cap100000 endpoint are outside this three-resolution decomposition.

## Consequence for the remaining goal

At source commit `5bc0691a60d2282aef6828f5da6d5f2a803673e9`, hosted Python CI
passes 264 tests, one skip and 70 subtests. The fresh locked CPython 3.14.5
export passes all 47 report-replay steps, six follow-up checks and strict
comparison of 237 unchanged files. The earlier CPython 3.12 export executed
all computations but failed strict artifact identity in nine files due to
environment metadata and cascading hashes; its failure/differences remain
preserved. The new decomposition JSON is byte-identical in both exports.
Records are in [`validation`](../evidence/amr-derivative-projection-validation-2026-10-03/README.md),
[`3.14 export`](../evidence/clean-export-2026-10-03-amr-5bc0691-py314/README.md)
and [`3.12 strict failure`](../evidence/clean-export-2026-10-03-amr-5bc0691-py312/README.md).
Later documentation/evidence commits are outside this fixed-commit test scope.

A future AMR quality gate must name its representation, norm, support, time
and reference-resolution floor before execution. For example, no constant
gradient tensor on the archived n=64 mapped partition can attain an integrated
relative L2 error below its 7.0390% floor. This is a bound for that
representation, not a new 5% acceptance rule: the existing uniform protocol's
5% **peak** gradient error is a different quantity and cannot be reused as an
integrated-L2 threshold.

The new split gives a concrete observable for transfer/accuracy studies,
while preserving the historical AMR quality verdict `UNCERTAIN`. New
prospective runs must also distinguish instantaneous transfer from subsequent
flux/pressure/time evolution. No violated upstream contract is demonstrated,
so no new upstream issue is submitted from this audit. No molecular alignment,
viscosity change, phase transition or singularity follows from these errors.
