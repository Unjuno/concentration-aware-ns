# Restart clock offset changes MAX_TIME termination

On SU2 v8.5.0 (12eb826f049ef7f67df974dfcb44cf36ee07c0f8), the static
singlezone BDF2 R=2 restart runs one extra iteration before reaching MAX_TIME
compared with the continuous run. Changing only the COutput clock update removes
this difference. This reproduces an execution consequence beyond CSV labels.

The protocol was committed in a00faa8 before execution. Both modes reuse the
original R=2 case inputs and (for restart) saved states 0 and 1. Only MAX_TIME
and TIME_ITER are changed to 0.35 and 20; dt remains 0.1. The diagnostic image
sets CUR_TIME to index*dt without changing driver PhysicalTime, MMS source or
boundary evaluation. Four fresh runs use network-disabled containers.

| Image | Mode | Saved indices | Final history time |
|---|---|---|---:|
| Original | Continuous | 0–4 | 0.4 |
| Original | R=2 restart | 2–5 | 0.4 |
| Output-clock diagnostic | Continuous | 0–4 | 0.4 |
| Output-clock diagnostic | R=2 restart | 2–4 | 0.4 |

All four solver exit codes are zero. Every saved inner residual is below -10.
Every termination log identifies MAX_TIME, and none identifies the TIME_ITER
cap. At common saved indices, every pressure/velocity value matches exactly at
CSV precision between same-mode images (4,000 scalar comparisons). Thus the
intervention changes the stopping iteration without changing these shared states.
The original restart reaches the same *reported* time after one extra step;
reported time must not be mistaken for agreement of the simulation endpoint.

The direct source path is recorded in
`evidence/su2-output-clock-control-v1/stop-consumer-source.json`:
CSinglezoneDriver reads CUR_TIME, compares it to MAX_TIME and ORs the result
into StopCalc. The BDF2 delay helper's false return cannot suppress that direct
condition. This explains the observed first-threshold-crossing termination.

## Reproduction and evidence

With both recorded images available, run:

```sh
python3 -m tools.run_su2_max_time_control
```

The runner refuses existing experiment directories. Evidence in
`evidence/su2-max-time-clock-control-v1` contains all four raw archives and
`summary.json`. Each archive preserves configuration, mesh, saved states,
history, solver log, exit code, image identity, baseline/protocol hashes and
container command. The summary separately records prediction reproduction;
it does not certify the simulator's physical accuracy or a general repair.

This is a fixed-dt, static singlezone result. Moving meshes, multizone,
variable-step accumulation and adjoints are not tested. The diagnostic formula
is unsuitable as a general variable-step fix. Existing source/boundary timing
issues and the meaning of absolute endpoint labels remain separate. The stopping experiment was reported as a focused follow-up on existing
[SU2 #2353](https://github.com/su2code/SU2/issues/2353#issuecomment-5851174679).
The submitted body and API readback are preserved; the readback matches.
Before posting, raw archives were checked again for stopping indices, residuals,
exit/log conditions and byte-identical common-index restart files. This review
is recorded in `publication-review.json`; it does not validate a general repair.
