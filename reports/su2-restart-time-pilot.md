# SU2 restart pilot: fields agree, history times differ

The fixed protocol extends the all-face Dirichlet boundary pilot to four BDF2
steps (dt=0.1). For each existing image, a continuous run is compared with a
restart at iteration 2 using both archived states 0 and 1. All four solver
invocations exit zero. Raw inputs, histories, fields, logs and image IDs are
archived in `evidence/su2-restart-time-pilot-v1/`.

At saved indices 2 and 3 (target times 0.3 and 0.4), pressure and all velocity
components match between same-variant continuous and restarted runs within
1.964e-15. This meets the frozen 1e-7 tolerance. All saved inner residuals
meet the log10 threshold -10. Both imported restart states match the prefix
archive byte-for-byte.

However, the history time comparison fails:

| Variant | Time_Iter | Continuous Cur_Time | Restarted Cur_Time |
|---|---:|---:|---:|
| Original | 2 | 0.2 | 0.1 |
| Original | 3 | 0.3 | 0.2 |
| Global time shift | 2 | 0.2 | 0.1 |
| Global time shift | 3 | 0.3 | 0.2 |

The restart history is named `history_00002.csv`, which the replay reads
explicitly. The checker preserves separate field and time decisions:
`field_comparison_pass=true`, overall `success=false`. This is an observed
history-label discrepancy with field continuation preserved in this pilot.
It is not evidence that the physical solve restarts at the wrong time, nor
proof of a general output defect. Source attribution, intended label semantics,
other restart indices and existing upstream reports remain to be reviewed.

Reproduce with the existing two images:

```sh
python3 -m tools.run_su2_restart_time_pilot
python3 -m tools.check_su2_restart_time_pilot
```

The runner refuses an existing output directory. The second command replays
committed archives and intentionally exits 1 while the time comparison fails;
`replay-review.json` records both outcomes. Do not add it to a success-only
common replay without preserving that distinction. No additional upstream
message has yet been submitted. This does not establish temporal order,
cross-version restart correctness, or a general timing fix.

## Source attribution of the observed label difference

The v8.5.0 `COutput.cpp` and `COutput.hpp` were independently fetched at the
runtime pin and match the local files byte-for-byte. Their hashes and excerpts
are in `output-clock-source.json`. History fields initialize to zero
(`COutput.hpp:130,144`). `COutput::LoadCommonHistoryData` (`COutput.cpp:2282`)
adds one TIME_STEP to CUR_TIME whenever the stored TIME_ITER differs from the
current iteration, then updates TIME_ITER. It does not read driver PhysicalTime
in that update. The field description calls CUR_TIME the current physical time.

For a fresh history object with fixed dt, first iteration 0 leaves its clock
at zero; first iteration R>0 advances it only to dt. Subsequent iteration changes
add one dt. Consequently the simple accumulator model predicts index-time
offset (1-R)*dt after a restart at R>0. For the exercised R=2 case, it predicts
-0.1. This model matches all 12 archived history rows in both variants exactly
using rational arithmetic:

```sh
python3 -m tools.check_su2_output_clock
```

The model result is in `output-clock-model.json`. Its success explains the
recorded time mismatch; it does not turn the failed continuity comparison into
a pass. Other restart indices and variable-dt output lifecycles have not been
executed. A general correction must define how to initialize absolute output
time, especially for variable steps, rather than blindly substituting iteration
number times the current dt. The source also has other CUR_TIME consumers;
this audit does not infer their runtime effects from the history discrepancy.


## Upstream disposition

Existing issue [#2353](https://github.com/su2code/SU2/issues/2353) already covers
target-time semantics and explicitly documents two-state BDF2 restart. Related
PR #2857 is closed and unmerged; its discussion raises moving-mesh restart and
discrete-adjoint compatibility concerns. Issue #1681 concerns zero-valued
explicit-scheme screen fields, a different reported setup. The search was
bounded and does not prove that no other duplicate exists.

The new same-variant field/history comparison was submitted as a
[supplement to #2353](https://github.com/su2code/SU2/issues/2353#issuecomment-5849620199),
with the fixed-version scope, raw data, failed time gate and compatibility
limits. Read-back matches the submitted text and is archived in
`upstream-comment-readback.json`. No new issue or general-fix PR was created.

## Independent prediction check at restart index 3

The subsequent protocol `su2-restart-time-pilot-r3.json` was frozen before its
four new solver invocations. It predicts a two-step output-clock offset for
R=3, imports saved states 1 and 2 from the existing same-image continuous
archive, and compares against a fresh five-step run. Both variants finish
successfully. Fields at indices 3 and 4 agree within 2.659e-15; all saved
inner residuals meet the same threshold. The expected time-label failure
persists: continuous times are 0.3,0.4 while resumed times are 0.1,0.2.
The exact accumulator model matches all 14 new history rows.

```sh
python3 -m tools.run_su2_restart_time_pilot --protocol protocols/su2-restart-time-pilot-r3.json
python3 -m tools.check_su2_restart_time_pilot --protocol protocols/su2-restart-time-pilot-r3.json
python3 -m tools.check_su2_output_clock --protocol protocols/su2-restart-time-pilot-r3.json
```

The field/time checker intentionally exits 1; the accumulator-model checker
exits 0. Both the original R=2 archive and new R=3 archive retain that same
distinction under the generalized replay. New evidence lives in
`evidence/su2-restart-time-pilot-r3/`. This tests the restart-index dependence
predicted before the run, while remaining a fixed-dt, static-mesh pilot. It
adds no variable-step or discrete-adjoint evidence. No additional upstream
comment was posted for this follow-up.
