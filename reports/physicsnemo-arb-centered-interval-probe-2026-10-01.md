# PhysicsNeMo Arb centered interval probe — 2026-10-01

## Method

The earlier local probe used `mpmath.iv`. Its own documentation describes the
interval support as experimental, warns that some functions may not support
intervals correctly, and notes that dependency can make bounds pessimistic.
That is a reason to treat the earlier result as exploratory, not as a package
failure. This follow-up uses python-flint 0.9.0's Arb real-ball arithmetic,
which represents real values by midpoint-radius balls and documents rigorous
error tracking for real operations and mathematical functions. The pinned
wheel installed successfully in the isolated Python 3.14 verification
environment. The package license metadata and its maintainers' component
license description are recorded in the README; the wheel is an optional
verification dependency and is not redistributed by this repository.

For the frozen endpoint ansatz,

```text
e = u_pred - u_ref = t*MLP + (1-exp(-t))*u0
G = D e
D_k G_ij = t*D²_kj MLP_i + (1-exp(-t))*D²_kj u0_i
```

On each box, the audit computes an Arb enclosure for the Jacobian at its center
and an Arb enclosure for the error Hessian over the full box. The mean-value
theorem then gives

```text
G_ij(box) subset G_ij(center) + sum_k D_k G_ij(box)*(box_k-center_k).
```

The radius implementation takes absolute upper bounds for each Hessian entry
and coordinate displacement, sums their products, and adds the resulting
symmetric radius to the center ball. The manufactured reference Hessian used
here comes from third derivatives of its scalar potential; a unit test checks
that result against independent finite differences of the repository's
`grad_u` implementation. Other tests verify the centered enclosure contains
direct Arb point evaluations on a 3x3x3 point set and that it narrows the direct
interval form for a synthetic network.

## Frozen-model result

The reproducible audit is
[`../evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json`](../evidence/tests/physicsnemo-arb-centered-interval-probe-2026-10-01.json).
It checks archive, checkpoint, and evaluation hashes for the `n64-nt17` run,
searches its 262,144 saved evaluation points for the largest sampled gradient
error, then evaluates that candidate and surrounding boxes. The best saved
point is `(3.079742548222244, 2.9815677777975633, 3.276092089071606)`; its
sampled gradient-error Frobenius norm is `0.2509277804721862`. At the
degenerate box, the Arb center-value result matches the independently
recomputed PyTorch-autograd error Jacobian to `2.17e-15` in the largest
component.

For a half-width `0.01` box around this sample, the direct Arb interval form
gives a Frobenius error upper bound of `0.94269`; the centered mean-value form
reduces it to `0.35744`. Subdividing that same local parent box into 8, 64, and
512 equal cells lowers the maximum centered cell upper bound to `0.27254`,
`0.25682`, and `0.25329`, respectively. Autograd values at the 27-point
neighborhood grids and at each subdivision-cell center fell within the
reported component intervals, within `1e-8` floating comparison tolerance.
These are diagnostic checks of the implementation; they do not prove the
enclosures independently.

At half-width `1e-4`, direct and centered Frobenius upper bounds are `0.25515`
and `0.25098`; at `1e-3` they are `0.29725` and `0.25201`. This illustrates
the advantage of the centered form on small boxes. The result is not uniform:
at half-width `0.025`, the centered bound (`11.18`) is slightly looser than the
direct bound (`11.02`), and at `0.05` the bounds are about `4.13e5` and
`5.90e3`, respectively. The local Hessian interval wraps badly on these larger
boxes. Subdivision is useful for the tested `0.01` parent, but the experiment
covers only that small neighborhood of one sampled peak candidate. It does not
cover the periodic domain or certify global continuous extrema. Arb/FLINT is
trusted according to the upstream library contract here, not proved in a
separate proof assistant. No PhysicsNeMo acceptance threshold was preregistered
and no quality verdict changes: it remains `UNCERTAIN`.

Run from the repository root with the pinned PhysicsNeMo source available:

```sh
PYTHONPATH=.:work/physicsnemo-source \
  work/physicsnemo-env/bin/python tools/audit_physicsnemo_arb_interval_probe.py
```

## Primary references

- [mpmath 1.3.0 contexts and interval arithmetic](https://mpmath.org/doc/current/contexts.html) documents the experimental status and dependency-related pessimism of `iv`.
- [python-flint 0.9.0 overview](https://python-flint.readthedocs.io/en/latest/) describes Arb ball arithmetic and rigorous error tracking.
- [python-flint `arb` reference](https://python-flint.readthedocs.io/en/stable/arb.html) documents midpoint-radius representation, precision, trig/exponential/hyperbolic functions, and outward absolute bounds.
- [python-flint on PyPI](https://pypi.org/project/python-flint/) records the 0.9.0 release, Python requirement, wheel availability, and license metadata.
