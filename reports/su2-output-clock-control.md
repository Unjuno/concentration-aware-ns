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
