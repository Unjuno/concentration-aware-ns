# Identified OpenAI source — preliminary statement audit

The user identified OpenAI's repository as the source. Located and read on
2026-09-09, pinned revision:
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

- Repository: https://github.com/openai/NavierStokesAndEuler
- Official announcement: https://openai.com/index/navier-stokes-solution/
- Statement: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/ComparatorSolution.lean
- Metadata: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/formalization.yaml

## What was actually inspected

README, formalization.yaml, top-level Navier–Stokes Comparator theorem statements,
and Comparator checking instructions. Metadata declares Apache-2.0 and labels
review as self-assessed. We have not built Lean, checked the dependency closure,
run Comparator, or independently verified the mathematics.

The exposed NS statements quantify over every positive viscosity and assert
existence of initial data and forcing meeting named decay/periodicity conditions,
with no global solution meeting the corresponding existence/smoothness predicate.
The actual predicates and constructive witness chain need further inspection.
Do not infer their complete analytic content from their names alone.

The README distinguishes forced NS on R3/the torus from unforced Euler. The
announcement describes a concentrated vortex with finite energy. Those are source
claims, not yet reproduced results of this benchmark.

## Effect on benchmark scope

1. The original discovery is now identified; it is no longer an unidentified
   attribution. Mathematical and numerical verification remain separate tasks.
2. The current periodic manufactured solution is a calibration reference, not
   this blowup construction or a numerical reproduction of its theorem.
3. First inspect force regularity/decay, scale schedules, finite-time localization
   and the explicit witness. Extract only finite smooth pre-singular segments
   whose formulas and truncation error can be verified.
4. Map applicability separately for forced incompressible NS, unforced Euler,
   unforced viscous NS, compressible models, turbulence closures and controllers.
   No blanket downstream vulnerability claim follows from the theorem statement.
5. Mathematical smoothness of a forcing does not establish implementation within
   actuator amplitude, bandwidth or spatial-resolution constraints.
6. Follow source license terms before redistributing code. Source inspection used
   GitHub API; no second project repository was created or cloned.
