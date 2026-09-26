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
