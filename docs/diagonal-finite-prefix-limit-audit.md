# Why fixed-prefix limits do not control the growing stage sum

The pinned source and our Lean extension establish several useful facts about
every fixed finite prefix: each retained cutoff stage can vanish at the axis as
the chart variable tends to zero, and sufficiently late stages are exactly zero
on a compact set where a positive chart lower bound is known. Neither fact by
itself gives a uniform limit for a sum whose active stage count grows while the
chart lower bound shrinks. This note gives a smooth counterexample to that
inference pattern. It is not a model or counterexample to the OpenAI field.

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

## Reproduction and scope

`tools/check_diagonal_finite_prefix.py` evaluates the smooth cutoff example at
`q=1/n`, records fixed-stage values and sum bounds, and writes
`evidence/tests/diagonal-finite-prefix.json`. Run:

```sh
python -m tools.check_diagonal_finite_prefix
python -m unittest tests.test_diagonal_finite_prefix -v
```

This is a generic counterexample to a proof pattern, not a counterexample to
the OpenAI construction and not evidence of a solver defect. It clarifies why
the existing finite-prefix identities do not yet extract an executable
finite-stage approximation or a numerical tail bound for the selected
candidate. The benchmark and the source-specific extraction obligation remain
open.
