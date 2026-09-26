# SU2 time-consumer scope audit

Pinned runtime source: v8.5.0, `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`.
The three inspected files were fetched again from that immutable GitHub revision
and matched the local source byte-for-byte. Hashes and excerpts are preserved
in `evidence/su2-study-v1/time-consumer-source-audit.json`.

| Location | Time use | Consequence for the proposed correction |
|---|---|---|
| `CSinglezoneDriver.cpp:120` | Sets physical time to TimeIter*dt during preprocessing; steady case sets zero | A global shift changes the value seen by all following consumers |
| `CIncEulerSolver.cpp:1861` | Reads physical time for the manufactured source path | The archived BDF2 control tests this source timing behavior |
| `CFVMFlowSolverBase.inl:559` | Reads the same time before GetLocalError against current solution values | Reported verification errors need an explicit association between stored solution and reference time |
| `CFVMFlowSolverBase.inl:1533` | Reads the same time before GetBCState and strong Dirichlet enforcement | A source-only timing correction would leave the boundary path requiring separate review |

This source evidence supports a time-level contract review. It does not prove
that every listed consumer is wrong: that depends on the solution state at the
call site. The uniform periodic BDF2 control does not exercise time-dependent
Dirichlet boundaries, output/restart conventions, or other drivers.

A regression supporting a general fix must distinguish:

1. Source evaluation at the target BDF state time, using the existing exact
   uniform recurrence control, including its repeated startup history.
2. A time-dependent Dirichlet MMS case, verifying boundary values at the same
   target time and separately checking temporal convergence.
3. Error reporting against a known saved-state timestamp, rather than merely
   accepting the displayed error norm.
4. A split/restart run versus an uninterrupted run at matching physical times,
   with explicit history-state timestamps. No restart result is asserted here.

The proposal is to name stored-state, target-state and output times explicitly
before choosing which consumers change. This report does not recommend the
global `(TimeIter+1)*dt` intervention as a complete fix. It also does not claim
all time consumers have been inventoried: these are the three files directly
identified by the reproducer and the upstream discussion.

The September 27 discussion refresh found no reply after our September 26
BDF2 follow-up. The existing response recommends this distinction:
[SU2 discussion response](https://github.com/su2code/SU2/discussions/2890#discussioncomment-18418174).
No additional upstream message was submitted, because this audit sharpens the
scope of the already posted finding without providing a new runtime defect.

A subsequent [two-step Dirichlet pilot](su2-boundary-time-pilot.md) now observes
the boundary time in both existing images and the unchanged history time labels.
The temporal-order and restart regressions listed above remain unperformed.

The [restart pilot](su2-restart-time-pilot.md) subsequently found matching
same-variant fields but a one-step discrepancy in restarted history labels.
The checker preserves that failure. The general restart contract and source
attribution remain under investigation.
