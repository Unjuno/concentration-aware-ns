# SU2 shared-MMS run audit and parallel successor

## Preserved run and replay result

GitHub Actions run [37190363204](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37190363204)
used source commit `0dece1c93181f6ee66630873bede46c16dfe29a7`, the frozen
protocol SHA-256
`dacd7638a306a810c986ce8d5922f16e55a76698b67d97f7ff892b7f6c9b60aa`, and
image ID `sha256:88796454471f478a15081123bca0e7e092249eceb2ce2aeacd60397d4dcc3847`.
The job ended at its configured 360-minute limit. Its 8,932,993-byte hosted
artifact (ID `11306796849`, ZIP digest
`3398d5a4dcc8d1772c8fdbb6a5c39b5232539941e382520190ddf12bb49a2dda`) is
preserved under
[`evidence/su2-shared-high-gradient-v1-run-37190363204/`](../evidence/su2-shared-high-gradient-v1-run-37190363204/).

The original five-case protocol remains unchanged. Only `n16-dt0.001` produced
a completed archive; `n32-dt0.001` has a partial log and initial field, while
the other three cases have no artifacts. The n16 archive hash is
`2441111ed75fc86ba1c914e9a32669893dff8c4e5ba9b700709bbbd60a220f2f`.
Independent replay matched its stored hashes and recomputed diagnostics at
the fixed replay tolerance. It recorded 50 output rows but only 49 rows met
the four-residual standard gate; the initial pressure residual was `-9.000986`
against the configured `-10` threshold. Its sampled gradient and vorticity
peak errors were 36.09% and 34.03%, while velocity, energy, and spectrum
errors were below their limits. This is one coarse case with failed standard
and local gates; it cannot establish an acceptance blind spot or an upstream
defect. Full case coverage and the replay receipt are recorded in
[`evidence/tests/su2-shared-high-gradient-replay-37190363204.json`](../evidence/tests/su2-shared-high-gradient-replay-37190363204.json).

## Execution-path correction

The original runner serialized all five solver runs inside one 360-minute
job, which made full coverage infeasible at the observed runtimes. The
successor workflow now builds the pinned solver image once, transfers that
image to one worker per frozen case, and verifies that every worker loaded the
same image ID. A final collector merges the per-case archives, and the
existing independent replay verifier checks each available archive.
Coverage status is now computed from the exact expected case set; per-case
standard acceptance remains a separate result. A full five-case matrix can
therefore be execution-complete even when a solver case fails its stopping
gate, while any missing, duplicate, or mismatched case keeps coverage
`INCOMPLETE`.

The new worker selection and collector pass focused unit tests, including
complete coverage with a failed standard gate, missing-case handling,
duplicate protection, and same-image enforcement. The preserved n16 artifact
also passed through the new collector and replay path without changing its
`INCOMPLETE` classification. The parallel workflow itself has not yet run;
no solver result is inferred from this orchestration change.

## Remaining SU2 evidence

Run the frozen five cases through the shared-image matrix workflow. Replay the
published aggregate artifact, then apply the interpretation rules in
`reports/su2-shared-high-gradient-interpretation-2026-10-04.md`. An n64-only
quality discrepancy remains `UNCERTAIN` for a persistent acceptance blind
spot; that rule requires a second adequately resolved spatial level such as
n128. Refresh overlapping SU2 issues and discussions only if a reproduced,
actionable finding meets that rule.
