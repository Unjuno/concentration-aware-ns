A follow-up control shows that the restart clock difference also changes **MAX_TIME termination**, beyond the history labels.

Using the same pinned v8.5.0 static singlezone BDF2 case above, I changed only MAX_TIME to 0.35 and TIME_ITER to 20 (dt remains 0.1), so the iteration cap does not bind. The protocol and expected stopping indices were committed before the four runs.

| Build | Continuous final Time_Iter | R=2 restart final Time_Iter |
|---|---:|---:|
| Original MMS build | 4 | 5 |
| Output-clock-only diagnostic | 4 | 4 |

The diagnostic changes only the COutput CUR_TIME update to `curTimeIter*TIME_STEP`; driver PhysicalTime and MMS source/boundary evaluation are unchanged. All four logs terminate for MAX_TIME, not TIME_ITER, and every saved inner residual is below -10. At common indices, the same-mode original/diagnostic restart CSV files are byte-identical. The original restarted run therefore advances one extra step while reaching the same reported Cur_Time=0.4.

The direct consumer is [CSinglezoneDriver.cpp, lines 267–306](https://github.com/su2code/SU2/blob/12eb826f049ef7f67df974dfcb44cf36ee07c0f8/SU2_CFD/src/drivers/CSinglezoneDriver.cpp#L267-L306): it reads CUR_TIME, compares it with MAX_TIME, and ORs that result into StopCalc. This also means a false result from the BDF2 time-convergence delay helper cannot override that direct condition.

[Report and reproduction command](https://github.com/Unjuno/concentration-aware-ns/blob/3673d70/reports/su2-max-time-clock-control.md) · [Four raw archives, logs, configurations and image identities](https://github.com/Unjuno/concentration-aware-ns/tree/3673d70/evidence/su2-max-time-clock-control-v1).

This is a fixed-dt diagnostic, **not a proposed production patch**: index*current-dt is inappropriate for variable steps. A focused regression comparing continuous/restarted stopping indices, with MAX_TIME binding and TIME_ITER deliberately loose, would help protect a repair. Absolute target-time conventions, moving meshes, multizone and adjoints still need separate treatment. No new master runtime claim or restart-file renumbering is intended.
