# Output-only clock intervention

The fixed-dt diagnostic changes only the CUR_TIME update in COutput, from
incrementing to `curTimeIter*TIME_STEP`. It derives from the original MMS image,
so driver PhysicalTime and source/boundary timing remain at their original
semantics. The build uses no network. Source fingerprints, parent image ID,
patch input hashes and build log are preserved in `evidence/su2-output-clock-control`.

The frozen protocol reuses the original R=2 pilot configurations, mesh and both
restart states, with fresh continuous and resumed executions. Both exit zero
and all saved inner residuals meet the -10 threshold. Results:

| Mode | History times | Maximum field difference from same-mode original |
|---|---|---:|
| Continuous | 0, 0.1, 0.2, 0.3 | 0 at saved CSV precision |
| Resumed | 0.2, 0.3 | 0 at saved CSV precision |

Thus the intervention removes the observed restart history offset while leaving
all saved pressure/velocity values unchanged in these runs. This provides a
causal control for the output accumulator explanation; the previous global
PhysicalTime intervention was not needed to change these labels.

Reproduce after building the diagnostic image:

```sh
docker build --network=none -t concentration-aware-ns:su2-output-clock-control runtime/su2-output-clock-control
python3 -m tools.run_su2_output_clock_control
```

The runner refuses an existing output root. Raw data and input identities are
in `evidence/su2-output-clock-control-v1`. The old failed pilot remains intact.
This is **not a proposed general fix**: multiplication by the current dt is
not cumulative time for variable steps. Moving meshes, discrete adjoints,
other CUR_TIME consumers and stop conditions require separate validation.
No claim is made that the original source/boundary time lag is repaired.

## Independent archived-data replay

`python3 -m tools.check_su2_output_clock_control` checks the saved archives
without running the solver or importing the execution runner. It parses CSV
numbers with Python Decimal instead of NumPy. The replay verifies archive and
baseline hashes, protocol/image metadata, identical configuration/mesh/imported
restart bytes, complete 125-node IDs and coordinates, finite entries, converged
residuals, and both original and intervened history clocks. All 3,000 saved
pressure/velocity values compare exactly at CSV precision. The machine-readable
result is `evidence/su2-output-clock-control-v1/independent-review.json`.
This validates the archived comparison, not the physical model, variable-step
behavior, or every possible consumer of the output clock.

## Direct stopping consumer found

A fresh byte-for-byte check against the pinned v8.5.0 source confirms that
`CSinglezoneDriver::Monitor` reads `CUR_TIME` (line 267), compares it with
`MAX_TIME` (line 296), and includes that condition directly in `StopCalc`
(line 306). `GetCauchyCorrectedTimeConvergence` also uses the same clock for
its BDF2 delay. Its false return cannot override the driver's independent
`FinalTimeReached` OR condition. Thus the source exposes a termination path,
not merely history display. These excerpts and pinned hashes are saved in
`stop-consumer-source.json` beside the raw experiment archives.

The existing field-invariance experiment does not test this path: its iteration
cap binds. Protocol `su2-max-time-clock-control-v1.json` freezes a follow-up
with MAX_TIME=0.35, dt=0.1 and TIME_ITER=20. It predicts an extra iteration
for the original R=2 restart. This remains a source-derived prediction pending
execution, not a reproduced stopping defect. The nonintegral threshold avoids
ambiguity from floating-point equality at an exact time-step boundary.
