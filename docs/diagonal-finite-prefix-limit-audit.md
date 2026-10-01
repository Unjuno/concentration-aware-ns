# Fixed-prefix limits and the need for uniform tails

The pinned source and our Lean extension establish several useful facts about
every fixed finite prefix: each retained cutoff stage can vanish at the axis as
the chart variable tends to zero, and sufficiently late stages are exactly zero
on a compact set where a positive chart lower bound is known. Neither fact by
itself gives a uniform limit for a sum whose active stage count grows while the
chart lower bound shrinks. This note gives a smooth counterexample to that
inference pattern, then compares it with the stronger bounds actually present
in the pinned source. It is not a model or counterexample to the OpenAI field.

## A smooth diagonal counterexample

Let `chi` be a nonnegative smooth cutoff with `chi(s)=1` for `s<=1`, a smooth
transition on `(1,2)`, and `chi(s)=0` for `s>=2`. For `q>0`, define

```text
f_j(q) = q chi(j q),       a(j)=j,
S(q)   = sum_{j>=1} f_j(q).
```

The schedule `a(j)` diverges. For each fixed `q>0`, the sum is finite because
terms vanish when `j q>=2`. For every fixed stage `j`, however, `j q<=1`
eventually as `q->0`, so `f_j(q)=q->0`. The same is true for every fixed
finite prefix.

Now take the diagonal sequence `q_n=1/n`. For every `1<=j<=n`,
`chi(j/n)=1`, and therefore

```text
S(1/n) >= sum_{j=1}^n 1/n = 1.
```

At most `2n` stages are nonzero and each is at most `1/n`, so also
`S(1/n)<=2`. Thus every fixed finite prefix tends to zero while the full,
smooth, finitely supported stage sum does not tend to zero along this sequence.
This exact lower bound does not depend on a floating-point calculation.

The example isolates the missing quantifier exchange:

```text
for each fixed J:       sum_{j<=J} f_j(q) -> 0
does not imply:         sum_{j>=1} f_j(q) -> 0,
```

when the number of active stages grows as `q->0`. A construction-specific
uniform tail estimate, a summable majorant independent of `q`, or another
uniform-in-stage argument is needed. A cutoff index bound alone only says the
sum is finite at each positive `q`; it does not control the magnitude of the
growing prefix.

## What the pinned construction supplies

The pinned OpenAI source does provide a stronger analytic estimate. Its
`AdmissibleScales` record stores, for each stage `j`, derivative order `m`,
and `0<q<=1`, the ordinary bound

```text
||D^m slowStage_j(q,w)|| <= 2^(-j) q^(h*j-m)
```

on the compact inner-coordinate set. `ordinary_tail_bound` sums these stage
bounds and proves for `m<=J+3`

```text
||D^m(slowSum-cutPrefix_J)(q,w)||
    <= 2^(-J) q^(h*(J+1)-m).
```

`exists_ordinary_uncut_tail` further chooses a fixed prefix and a positive
terminal neighborhood for any finite list of requested jet orders. The local
Lean extension uses this chain in `axial_derivative_tail_tends_zero`, whose
axiom report is included in
`evidence/lean-verification/axis-force-sign.json`. Thus the generic example
above does **not** expose a missing analytic tail theorem for that proved
observable. The source already has a non-effective construction-specific
uniform bound, and the radial-derivative limit has been formally checked under
its hypotheses.

What remains unavailable is an effective numerical extraction: the compact
derivative constants used to choose `AdmissibleScales`, the selected integer
schedule, and the resulting prefix/threshold are existential and are not
turned into computable coefficient enclosures or a reproducible finite
approximation of the selected field. The generic counterexample explains why
the existence-level uniform-tail theorem matters; it must not be used to
claim that the theorem is absent.

## Reproduction and scope

`tools/check_diagonal_finite_prefix.py` evaluates the smooth cutoff example at
`q=1/n`, records fixed-stage values and sum bounds, and writes
`evidence/tests/diagonal-finite-prefix.json`. Run:

```sh
python -m tools.check_diagonal_finite_prefix
python -m unittest tests.test_diagonal_finite_prefix -v
```

This is a generic counterexample to a proof pattern, not a counterexample to
the OpenAI construction and not evidence of a solver defect. The exact
construction-specific analytic tail estimate is already present as described
above. The still-open task is to make its existential constants, scales and
coefficients effective enough for an executable finite-stage approximation
and numerical error certificate. The benchmark remains open.
