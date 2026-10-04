# Part I compatibility assumption cross-check — 2026-10-04

## Question

A machine-generated secondary reading described the profile construction in
Lei and Ren, arXiv:2609.35406v2, as conditional on simultaneous compatibility
conditions that were not discharged by the paper. I treated that as a lead and
checked the primary PDF, rather than accepting the summary.

## What the primary source states

The versioned Part I PDF (SHA-256 recorded in the accompanying evidence)
distinguishes an assembly theorem for arbitrary compatible pieces from a
separate theorem that constructs compatible pieces. Assumption 12.1 lists the
joint data required by the assembly step. Section 12.1 says those conditions
are evaluated from the specified profiles and that Section 12.5 proves them
for the paper's concrete construction.

Theorem 12.4 states existence of compatible data. Its prescribed dependency
order is to fix the dimensionless outer data and axis shift first, choose the
core scale `Lambda` next, then increase `C_*` while tying
`R_ref = 110 (C_* P_*)^10` to it. The proof supplies finitely many lower bounds
for `C_*`, uses decay in `C_*` to close the five moment tolerance, and checks
all four clauses of Assumption 12.1 for the same data. It says the waiting
length and restored axis pressure remain common across this family.

Therefore the narrower statement “no single parameter may be increased while
all dependent quantities are frozen” must not be turned into “compatibility is
left as an unresolved assumption.” The paper explicitly claims a simultaneous
choice theorem and gives a dependency-aware construction order. The machine
summary's conditional wording is incomplete on this point.

## Scope and remaining audit

This is a source-reading correction, not an independent proof of Theorem 12.4
or of the preceding outer/core estimates. I have not reconstructed every
constant, checked every inequality from its lemmas, or audited the lower-order
induction. Part I also says that cancellation of the divergence-form residual
by oscillatory pulses is deferred to Part II; the Part II manuscript remains
unlocated in the bounded arXiv/index checks recorded separately. Thus this
cross-check strengthens the claim that Part I attempts to discharge its own
compatibility condition, while leaving the full forced-blowup construction
unverified here. It exposes no solver software defect and warrants no
upstream solver issue.

## Reproduction record

The pinned PDF is available at
https://arxiv.org/pdf/2609.35406v2. Its downloaded SHA-256, relevant section
references, and finding boundaries are in
[`evidence/upstream-refresh/lei-ren-part1-simultaneous-compatibility-audit-2026-10-04.json`](../evidence/upstream-refresh/lei-ren-part1-simultaneous-compatibility-audit-2026-10-04.json).
