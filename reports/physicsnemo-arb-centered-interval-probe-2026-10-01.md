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

## Adaptive local cover cost

A deterministic worst-upper-first axis-bisection routine now records every
terminal cell, its coordinate box, and its centered Arb Frobenius upper bound.
For an explicitly exploratory target of `0.26` (not preregistered and not an
acceptance threshold), the half-width `0.01` parent reaches the target with 77
interval evaluations and 39 leaves; half-width `0.025` takes 1,085 evaluations
and 543 leaves. Half-width `0.05` stops at the 2,049-evaluation budget with
1,025 leaves and maximum terminal upper `0.27613`. Autograd checks at every
terminal leaf center were within the enclosures at the stated `1e-8` floating
comparison tolerance. The exact partition and bounds are serialized in the
JSON evidence file, so the candidate-local cover is reproducible. These runs
cover only the listed local parent boxes around one sampled point. In
particular, the `0.26` comparator is not a quality gate, and neither successful
local cover establishes a full-domain maximum or changes the `UNCERTAIN`
quality status.

The adaptive algorithm's unit tests verify complete volume preservation under
bisection and explicit evaluation-budget stopping. Run them with
`python -m unittest tests.test_arb_local_branch_cover -v`.

## Full-periodic-domain enclosure probe

Wide input balls exposed an interval-wrapping weakness in the elementary range
calls: on a ball spanning `[-1, 1]`, the library's direct `tanh` ball can be
wider than the mathematical range. The evaluator now intersects Arb's `sin`,
`cos`, and `tanh` balls with their analytic range `[-1, 1]`; this is a valid
range tightening and has a regression test. The rerun preserves all hashes and
recomputes the earlier local sweeps with the tightened evaluator.

The audit additionally tiles an outward-rounded superset of `[-pi, pi]^3`
using 2, 4, and 8 cells on each axis. Shared binary-float faces produce a
complete partition; the outer endpoint `3.141592653589794` exceeds mathematical
pi. All 584 cell-center autograd checks were within their respective component
intervals to `1e-8`. However, the maximum cell Frobenius upper bounds are
`242,057`, `70,089`, and `12,251`, while maximum center samples are only
`0.0148`, `0.0553`, and `0.146`. The box enclosures remain far too wide to
certify a useful continuous peak at these resolutions. A finite whole-domain
upper bound is now produced by this explicit tiling, but it is not a practical
quality certificate, and the sampled center checks are only diagnostics. No
PhysicsNeMo threshold is preregistered; quality remains `UNCERTAIN`. The
periodic-domain sweep and exact numerical output are in the JSON evidence.

## Derivative-range intersection and full-domain adaptive cost

The network jet now also intersects `tanh'` with `[0,1]` and `tanh''` with
`[-0.8,0.8]`, using the analytic global derivative bounds. This further lowers
the 8-per-axis uniform full-domain maximum from `12,251` to `275.01` (for 512
cells), with center-sample maximum `0.14597`. A worst-upper-first adaptive
partition of the whole outward-rounded periodic cube spends 2,049 evaluations
and leaves 1,025 cells; its maximum upper is `167.31`, still above the
illustrative `0.26` comparator. On the single sampled-candidate neighborhood,
the updated local adaptive results are 63 evaluations / 39 leaves at half-width
`0.01` (max `0.25961`), 1,023 / 511 at `0.025` (max `0.25980`), and a budget
stop at `0.05` (2,049 / 1,025, max `0.27268`). None is a preregistered quality
gate. These values replace the earlier interval results in this JSON, which
was regenerated from the same archived checkpoint.

A second analytic candidate was tested on all 25 frozen checkpoints: a vector
Hessian operator-norm recurrence using exact rational Frobenius upper bounds
for weight matrices and `|tanh''|<=4/5`. It is valid but markedly looser than
the existing componentwise recurrence: the illustrative best-case uniform-grid
floor increases from 9,465–13,743 to 287,269–328,448 nodes per axis (roughly
24–31 times as many). The new route is retained as a documented comparison,
not selected for certification. Eight fixed-point automatic-differentiation
checks per archive stayed under both network envelopes; these remain sanity
checks, not global validation. The updated 25-case record is in
`../evidence/tests/physicsnemo-global-hessian-coverage.json`.

## Monotone endpoint range for tanh

For a real input interval, monotonicity gives `tanh([a,b]) =
[tanh(a),tanh(b)]`. The network evaluator now encloses the ball's lower and
upper endpoints separately and takes their Arb hull, intersected with
`[-1,1]`. A regression test checks the broad `[-1,1]` interval against several
point evaluations and confirms the result is narrower than `0.77` in absolute
value. This avoids the direct broad-ball Taylor enclosure (about `[-5.63,5.63]`
for input `[-1,1]`).

The frozen audit was rerun after this change. On 512 uniform whole-domain
cells, the maximum centered Frobenius upper is `235.32` (cell-center sample
maximum `0.14597`). Whole-domain adaptive bisection reaches `151.40` after
2,049 evaluations / 1,025 leaves and does not meet the exploratory `0.26`
comparator. Candidate-local adaptive boxes meet it at half-width `0.01` with
63 evaluations / 32 leaves and at `0.025` with 1,021 / 511; half-width `0.05`
stops at the budget with upper `0.27174`. These results supersede the interval
sweep numbers above and in Revision 71; they remain exploratory and do not
change the `UNCERTAIN` quality status.

## Quadratic Taylor enclosure with a third-derivative remainder

For each Jacobian-error component `G_ij`, the added local enclosure uses

```text
G_ij(c+d) = G_ij(c) + sum_k D_k G_ij(c) d_k
           + 1/2 sum_{k,l} D_l D_k G_ij(B) d_k d_l.
```

It bounds the linear term with the point Hessian at the box center and the
remainder with Arb third-derivative intervals over the whole box. The MLP third
jet follows the third-order chain rule for tanh layers; the manufactured-field
term uses fourth derivatives of its scalar potential. Autograd checks all
spatial third derivatives of a synthetic frozen-shape MLP, and independent
finite differences check selected manufactured-field third derivatives. A
27-point direct-Arb sample grid is contained by the Taylor enclosure in the
synthetic small-box test.

On the frozen candidate, Taylor lowers the Frobenius upper from `0.3240` to
`0.2618` at half-width `0.01`, and from `0.7580` to `0.3684` at `0.025`.
At half-width `0.05` it lowers `2.3397` to `1.4313`. But on equal full-domain
tiles the Taylor upper is much worse: at 8 cells per axis it is `4,173`, versus
`235.3` for centered mean-value; the 2- and 4-per-axis Taylor bounds are
roughly 135x and 50x larger than the corresponding centered bounds. A hybrid
full-domain adaptive cover choosing the smaller of both estimates reaches
`469.90` after 513 box evaluations / 257 leaves, exactly the same terminal
maximum as the standard centered method with the same box count; the standard
run took about 10.6 seconds and the hybrid computes both enclosures per box.
Thus Taylor is useful for small local boxes, not broad global cells; it did not
improve this budget-matched global partition. All comparisons are on one
frozen model, exploratory, and do not set a quality threshold or change
`UNCERTAIN`.

## Local method crossover versus global cell scale

A radius sweep around the same saved candidate locates the method crossover
between half-width `0.05` and `0.075`: at `0.05`, the quadratic Taylor upper is
0.612 times the centered mean-value upper; at `0.075` it is 1.031 times as
large, and at `0.1` it is 1.62 times as large. This crossover is specific to
this candidate and cube geometry. The current 2,049-evaluation whole-domain
adaptive cover has terminal widths `0.785` on every axis (half-width about
`0.393`), so none of those global terminal cells reaches the observed local
crossover scale. This explains why the tested global hybrid did not improve
the budget-matched result. The sweep is preserved under
`local_method_crossover_sweep` in the JSON and must not be generalized to other
points or treated as a threshold.

## Uniform 16-per-axis full-domain cover

Added a standalone reproduction script for a 16-by-16-by-16 cover of the
outward-rounded periodic cube. For the same frozen `n64-nt17` checkpoint used
above, all 4,096 cells receive centered Arb enclosures at 30 decimal digits.
The maximum cell Frobenius upper falls from `235.32` at 8 divisions per axis
to `52.13` at 16 divisions, with 67.2 seconds wall time on this recorded
machine. The maximum autograd error sample over the 4,096 cell centers is
`0.22006`; every center sample fell inside its component enclosure within the
`1e-8` float comparison tolerance. The upper is still about 237 times the
center-sample peak and does not certify a useful peak to the benchmark's
unregistered PhysicsNeMo threshold. The output is
[`../evidence/tests/physicsnemo-centered-domain-cover-n16.json`](../evidence/tests/physicsnemo-centered-domain-cover-n16.json); rerun with:

```sh
PYTHONPATH=.:work/physicsnemo-source \
  work/physicsnemo-env/bin/python tools/audit_physicsnemo_centered_domain_cover.py \
  --divisions 16 --dps 30
```

The saved checkpoint/archive hashes match the earlier Arb audit. This cover is
finite and whole-domain under the Arb contract, but neither its center checks
nor this implementation independently prove the interval library's guarantees.

The 16^3 audit now also decomposes the worst cell. It is the diagonal box
`[2.3562, 2.7489]^3`, centered at `(2.5525, 2.5525, 2.5525)`. The center
Jacobian Frobenius upper is only `0.0508`; the centered upper is dominated by
Hessian variation, with per-coordinate variation Frobenius bounds `16.69`,
`18.16`, and `17.38`. The quadratic Taylor upper on this same coarse box is
`293.83`, versus `52.13` for the centered form. This localizes the current
bottleneck to broad-box second-derivative enclosure and confirms that the
higher-order remainder is unsuitable at this cell scale. The decomposition is
included as `worst_cell_decomposition` in the n16 JSON.

## Refinement cost for the worst global-cover cell

The worst cell from the 16^3 uniform cover was refined independently with the
same centered Arb evaluator and deterministic worst-upper-first bisection.
The reproducible script and hash-linked output are
`tools/audit_physicsnemo_hotcell_refinement.py` and
`evidence/tests/physicsnemo-hotcell-refinement-2026-10-01.json`. At budgets
129, 513, and 2,049 evaluations, the maximum terminal uppers are 2.0987,
0.93861, and 0.36148. An exploratory target of 0.26 is reached at 3,923
evaluations and 1,962 leaves, with maximum upper 0.259992. The leaf volumes
sum exactly to the parent cell volume in the recorded binary-float check.

This is a cost measurement for one cell only. It does not refine the other
4,095 cells, establish the full-domain maximum, or make 0.26 a preregistered
quality threshold. It shows that subdivision reduces the large cell bound at
a substantial local evaluation cost; the global budget needed cannot be
inferred by multiplying this single-cell result.
