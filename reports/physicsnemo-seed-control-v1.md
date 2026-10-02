# PhysicsNeMo paired-seed control — descriptive, uncertain

The frozen control adds four seeds to the existing seed 709 across five fixed-budget cases (five seeds per case, 25 runs total). The 20 added runs completed with exit code 0. Values below describe this configuration only; they do not establish optimization convergence, continuous extrema, or a universal trend.

| Collocation case | Seeds | Velocity relative L2 mean ± sample SD [range] | Sampled gradient peak error mean ± SD |
|---|---:|---:|---:|
| n16-nt5 | 5 | 0.018655 ± 0.003911 [0.014785, 0.024820] | 0.007376 ± 0.001758 |
| n32-nt5 | 5 | 0.018855 ± 0.003936 [0.014698, 0.024996] | 0.007692 ± 0.002068 |
| n64-nt5 | 5 | 0.018943 ± 0.004140 [0.014790, 0.025697] | 0.007772 ± 0.002071 |
| n64-nt9 | 5 | 0.018206 ± 0.003393 [0.014494, 0.023656] | 0.007614 ± 0.001991 |
| n64-nt17 | 5 | 0.017718 ± 0.003016 [0.014212, 0.022481] | 0.007637 ± 0.002013 |

Paired velocity-error changes are new condition minus old condition:

| Contrast | Paired seeds | Mean delta | SD | lower / same / higher |
|---|---:|---:|---:|---:|
| n16 → n32 (nt=5) | 5 | +0.000199 | 0.000629 | 2 / 0 / 3 |
| n32 → n64 (nt=5) | 5 | +0.000089 | 0.000453 | 2 / 0 / 3 |
| nt5 → nt9 (n=64) | 5 | -0.000737 | 0.000880 | 4 / 0 / 1 |
| nt9 → nt17 (n=64) | 5 | -0.000488 | 0.000419 | 5 / 0 / 0 |

The paired derivative-peak metrics do not follow the velocity metric uniformly. From nt=9 to nt=17, sampled velocity relative L2 decreases for 5 of 5 seeds (mean delta -0.000488), while sampled gradient-peak error changes are higher for 3 and lower for 2 seeds (mean +0.000022); sampled vorticity-peak error is higher for 3 and lower for 2 (mean +0.000022). From n=16 to n=32, sampled gradient- and vorticity-peak errors increase for 4 of five seeds and decrease for 1. These are paired comparisons on a shared fixed validation design, not evidence of a continuous extremum or a causal effect of node count; magnitudes are small and no acceptance threshold was preregistered.


Seed 8191 produced a visibly higher velocity error in all five conditions than the first three new seeds; this demonstrates material seed sensitivity in this small sample. The paired contrasts remain descriptive and share the same fixed validation design. Training loss and runtime are retained per-run in the JSON artifact.

All quality/gate conclusions remain `UNCERTAIN`. The sampled gradient/vorticity metrics are finite-point checks, not certified maxima. No molecular interpretation, phase transition, or physical instability follows from these PINN errors.

Machine-readable means, medians, sample standard deviations, ranges, exact paired deltas for velocity/gradient/vorticity, run records, and limitations are in `evidence/physicsnemo-seed-control-v1/analysis.json`. The frozen report is regenerated from the archived run manifest; all 20 added archive hashes are verified before regeneration.
