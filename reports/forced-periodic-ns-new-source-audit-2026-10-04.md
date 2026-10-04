# New exact periodic solution and concentration study — 2026-10-04

## Why this source matters

A new primary-source search found Thambynayagam, arXiv:2609.38210v1,
submitted 2026-09-24. It is directly relevant to the benchmark's intended
separation between global energy and local-gradient diagnostics. The paper
contains (i) a smooth, closed-form forced Navier–Stokes solution with exact
velocity, pressure, force and energy decay, and (ii) a separate, nonlinear
localized/unforced numerical study of vorticity growth under a zero-work
constraint. The paper itself states that its finite-resolution computations
show concentration over the examined cases, not singular behavior.

## Independent analytic replay

I transcribed the paper's three-dimensional seed field (5.1) and pressure
(5.4), derived the convective term and projected force as
U0 = (u0·grad)u0 + grad(p0) at unit density, then checked the identities
symbolically with SymPy 1.14.0:

- div(u0) = 0;
- Delta(u0) = -2 u0;
- div(U0) = 0;
- for u=e^(-2 nu t)u0, p=e^(-4 nu t)p0,
  f=e^(-4 nu t)U0, the three strong-form residual components vanish;
- both u0·(u0·grad)u0 and u0·grad(p0) are periodic divergences,
  proving their cell means vanish and therefore the applied force does zero
  net work.

The independent checker is
`tools/check_forced_periodic_ns_candidate.py`; its machine output is
`evidence/analytic-checks/forced-periodic-ns-candidate-2026-10-04.json`.
This is a symbolic replay of the closed-form base solution, not a discretized
solver validation.

## Critical separation of the paper's two results

Theorem 4.1's exact solution evolves by pure exponential decay, retaining its
finite Fourier support and fixed spatial profile. Its peak velocity gradient
and vorticity do not grow relative to the amplitude. It is therefore useful as
an exact periodic source/projection/pressure/energy-decay check, but by itself
does not exercise concentration.

The concentration experiment in Section 7 changes the force to leave a
projected nonlinear term active in a selected region. That is a different
time-evolving PDE calculation, performed with the authors' pseudo-spectral
solver. The paper reports that (a) a coarse-grid apparent vorticity saturation
is contradicted by refinement, (b) a spectral-tail cutoff of 1e-4 is not
sufficient alone—the 96^3 case stays below it while the 128^3 comparison
changes peak vorticity by about 20%, and (c) localized forcing is not shown to
systematically enhance peak concentration against the unforced run. At
Re=3000, the two runs cross while both are resolved, then the unforced run
becomes under-resolved; the final resolved peak ordering is therefore
undetermined. These are author-reported numerical findings, not yet
independently rerun here.

This paper is a particularly close conceptual precedent for our acceptance
question. It already makes direct grid comparison and spectral resolution
diagnostics part of the claim and warns against reading a single-grid peak.
Accordingly, it narrows novelty claims: this repository should be presented as
a cross-solver (OpenFOAM Foundation, SU2, PhysicsNeMo), mixed discretization,
predeclared acceptance-gate audit with AMR-cap limits and exact-reference
quality metrics—not as the first demonstration that local vorticity can be
missed by inadequate resolution.

## Usability and limits

The exact base field may be a valuable additional periodic solver-verification
case if the same equations and boundary conditions can be mapped consistently
to each target. Its few persistent modes make it primarily a code-path and
projection/forcing check; it is not a harder local-concentration stress test.
The localized Section 7 family is a possible later stress test, but its forcing
is only C1 under the raised-cosine cutoff described in (7.1), unless replaced
with a smooth bump and re-derived. Its 1e-4 spectral-tail criterion is explicitly
a working convention rather than a proved error bound.

The arXiv record shows a perpetual non-exclusive license to distribute the
article; this does not establish a license to reuse the ancillary scripts. No
paper or ancillary source code was copied. No solver issue follows from the
paper or this algebra check. The paper is a v1 preprint; neither its theorem
proof nor its numerical claims are represented as peer reviewed here.

## Pinned source

- Paper: [arXiv:2609.38210v1](https://arxiv.org/abs/2609.38210)
- PDF SHA-256: fbe0d2198b000e8632525a9d6fed5ae47ab9fc3099a990b1802a4de397f43c5d
- Relevant statements: equations (3.2), (4.1)–(4.3), (5.1)–(5.5), Sections
  7.1–7.3 and 8.
- Reproduction command:
  `uv run --no-project --with-requirements requirements-verification.txt python tools/check_forced_periodic_ns_candidate.py`
