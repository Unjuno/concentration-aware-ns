# Part I scale-inequality replay — 2026-10-04

## Scope

I independently expanded the three explicit sufficient lower bounds for
`C_*` in Lei–Ren, arXiv:2609.35406v2, Theorem 12.4, against the two radius
inequalities in (12.6). This checks the algebraic implication in the displayed
proof only; it is not an independent proof of Lemma 9.1, Lemma 10.2, or the
existence theorem.

## Replay

The paper fixes `P_* > 0`, chooses `Lambda` before this final increase, and
states finite bounds `A(C_*) <= A` and `K(C_*) <= K C_*`, where the constants
are independent of the subsequently increased `C_*`. It sets
`R_ref = 110 (C_* P_*)^10` and lists the target inequalities

```
R_ref >= 110 exp(400 A + 10) (1 + A)^10,
exp(-8) R_ref >= 110 (1 + K)^2 / P_*^2.
```

For the first, the sufficient condition
`C_* >= P_*^{-1} exp(40 A + 1) (1 + A)` gives

```
(C_* P_*)^10 >= exp(400 A + 10) (1 + A)^10,
```

by raising nonnegative sides to the tenth power. Multiplication by 110 gives
the first target inequality.

For the second, the paper's condition
`C_*^8 >= exp(8) (1 + K)^2 P_*^{-12}`, together with `C_* >= 1`, implies
`C_*^10 >= C_*^8 >= exp(8) (1 + K)^2 P_*^{-12}`. Since `P_* > 0`, multiplying
by `exp(-8) 110 P_*^10` gives exactly
`exp(-8) R_ref >= 110 (1 + K)^2 / P_*^2`.

The other listed threshold `C_* >= exp(4 A)` is itself the first condition in
(12.6), and the proof imposes the remaining fixed or eventually satisfied
thresholds separately. Each lower bound is finite under the theorem's fixed
data, so taking their maximum is algebraically consistent. This supports the
paper's stated simultaneous-parameter argument at this displayed step.

## Boundary

No supporting estimate was independently established here. In particular,
this replay does not verify the definitions of `A` and `K`, the core/outer
construction, the moment estimates, the lower-order induction, or Part II's
residual cancellation. It identifies no solver defect and makes no claim
about molecular alignment or physical particle locations.

## Source

Primary source: [arXiv:2609.35406v2](https://arxiv.org/abs/2609.35406v2),
Theorem 12.4, equations (12.6), (10.21)–(10.22). The pinned PDF SHA-256 is
`8396b998dcf737cd6a7c12ff1019c6b2fd308a7e6f0907c0c6647a9b2ec64e8d`.
