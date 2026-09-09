# Analytic transfer from the candidate to a numerical experiment

Source pin: [openai/NavierStokesAndEuler, 8937a8f](https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538).
This note checks elementary consequences conditionally on the stated candidate
properties. It does not certify the construction or its Lean proof closure.

## What the source statement actually quantifies

[ProblemStatement.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/ProblemStatement.lean#L94)
defines unbounded speed by: for every positive threshold M and every positive
neighborhood size δ, some t in (0,1), with t>1-δ, and some spatial x satisfy
||u(t,x)||>M. This is not a statement that every particle, every point or every
velocity component diverges. It does not prescribe molecular orientation.

The candidate is smooth before time 1, with a smooth, spatially periodic forcing
on the full future domain, vanishing after some common finite time. Its residual
uses viscosity one. [The selected witness](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/ActualCandidateAssembly.lean#L1120)
quantifies over a common integer schedule and sums for potentials, direct fields
and pressure. The selected candidate is obtained from that witness. Reading this
existence interface does not supply numerical constants or an executable tail bound.

## Viscosity and period scaling, derived directly

Suppose u(s,y), p(s,y), f(s,y) satisfy the unit-viscosity equation on a unit-period
cube. For ν>0 and target period L>0, put s=νt/L² and y=x/L, and define

    U(t,x) = (ν/L) u(s,y)
    P(t,x) = (ν²/L²) p(s,y)
    F(t,x) = (ν²/L³) f(s,y).

The chain rule makes ∂t U, (U·∇)U, νΔU and ∇P all equal to ν²/L³ times their
unit-scale counterparts. Divergence remains zero. Thus this is an equation-level
mapping, not a simulation observation. L=1 gives the source bridge's ν² f(νt,x).

Consequences for a numerical or physical transfer:

- The candidate time 1 maps to T=L²/ν. Changing ν changes both time and forcing;
  the existence claim does not use one fixed external force for every viscosity.
- Velocity gradients scale by ν/L². A time derivative of order k and spatial
  derivative of order m of F scales by ν^(k+2)/L^(2k+m+3).
- The squared velocity integral over one periodic cell scales by ν²L. The unit
  cell and our calibration's 2π-period cell cannot be interchanged silently.
- Smoothness only gives finite derivative bounds on each compact domain. It
  supplies no application-specific amplitude or bandwidth bound unless the
  constants are extracted and compared with that application.

## Finite energy does not control pointwise speed

For a smooth periodic solution before T, integration by parts gives

    (1/2) d||U||²_L2/dt + ν||∇U||²_L2 = <F,U>.

Cauchy–Schwarz implies ||U(t)||_L2 ≤ ||U(0)||_L2 + ∫₀ᵗ ||F(s)||_L2 ds
(the zero-norm case can be handled by regularization). Smooth periodic forcing
on a compact time interval makes this bound finite. This does not bound the
L∞ norm in three dimensions. Consequently bounded energy and pointwise
concentration are not contradictory, but this inequality alone proves neither
that concentration occurs nor that a solver misses it.

## What a finite-stage experiment still needs

Fix t_max<T first. For a finite approximation U_N,P_N define its own exact
manufactured residual F_N=∂t U_N+(U_N·∇)U_N-νΔU_N+∇P_N. Let w=U-U_N and
q=P-P_N. Then, identically,

    F-F_N = ∂t w - νΔw + (U_N·∇)w + (w·∇)U_N + (w·∇)w + ∇q.

A small velocity tail alone does not control this residual: bounds on its time
derivative, two spatial derivatives, pressure gradient and nonlinear products
are also needed. A solver run using F_N tests a finite manufactured problem;
it is not automatically a faithful approximation of a run driven by F.

Before calling a numerical case an extracted OpenAI candidate, require:

1. Concrete schedule and finite-stage formulas, with source-to-formula mapping.
2. Quantitative tails for every derivative used, on [0,t_max] and one spatial cell.
3. Divergence, pressure, force and unit/period conventions verified independently.
4. A separation of truncation, discretization, iteration and floating-point errors.
5. A statement that finite samples and finite stages cannot establish the
   universal threshold quantifier in the blow-up predicate.

Current status: statement and elementary scaling inspected; constructive
schedule extraction, tail bounds and independent proof verification remain open.
The existing localized MMS remains a separate calibration, not this extraction.
