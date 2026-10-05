# Foundation 13 high-gradient width/time sweep

The frozen 15-case sweep completed successfully in [GitHub Actions run 37211431276](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37211431276), from source commit `999fe90ae0e8fef106fd9db521541f71a2dfca43`. It covered envelope powers `m=1,2,4`, uniform meshes `n=32,64,128`, and the two additional `n=64` time steps `dt=0.0005,0.00025`. All 1,350 expected steps reached `t=0.05`; every case exited zero and passed the configured PIMPLE stopping gate. The greatest observed outer-corrector count was five, below the frozen limit of twelve.

The measured gradient and vorticity peak errors show a clear coarse-grid effect. The two fine grids pass every local-quality metric for all three widths; the coarse `n=32` cases pass the solver stopping gate but fail local quality on gradient and vorticity peaks.

| Envelope power | `n=32` gradient / vorticity | `n=64` gradient / vorticity | `n=128` gradient / vorticity | Fine-grid classification |
|---:|---:|---:|---:|---|
| 1 | 10.17% / 9.64% | 2.60% / 2.46% | 0.65% / 0.62% | `NOT_OBSERVED` |
| 2 | 10.27% / 9.42% | 2.63% / 2.41% | 0.66% / 0.60% | `NOT_OBSERVED` |
| 4 | 10.28% / 9.18% | 2.64% / 2.35% | 0.66% / 0.59% | `NOT_OBSERVED` |

The allowed relative errors are 5% for gradient and vorticity peaks and 2% for velocity, energy, and shell spectrum. At `n=32`, velocity errors range from 1.30% to 1.88%, while energy and shell-spectrum errors stay below 0.07%; only the two peak metrics fail. The exact-field centered-FD2 reference floor at `n=32` is already about 9.9–10.0% for gradient and 9.3–9.7% for vorticity. This makes the coarse failures consistent with the known stencil-resolution floor. At `n=64`, velocity errors are 0.33–0.48%; at `n=128`, they are 0.08–0.12%. Energy and shell-spectrum errors on the fine grids remain near or below 0.025% and 0.011%, respectively.

The two extra `n=64` temporal cases for each width also pass all local-quality metrics. Their peak errors remain near the `dt=0.001` `n=64` values, so this matrix does not establish a temporal convergence order; the spatial error dominates the reported peaks here.

Before classifying a width, the frozen exact-field reference floor was recomputed. It passes the 5% gradient/vorticity thresholds at both classification grids: gradient/vorticity floors are 2.525–2.548% / 2.365–2.478% at `n=64`, and 0.635–0.641% / 0.595–0.623% at `n=128`. At every width, both `n=64` and `n=128` pass the standard stopping gate and all local-quality metrics, so the frozen rule returns `NOT_OBSERVED`. The coarse `n=32` failures are excluded from that persistent fine-grid classification because the exact-reference stencil floor is too high there.

I downloaded and replayed the hosted evidence. All 15 case archive hashes matched the run manifest; all 150 pre-run input hashes and 60 stored diagnostic-file hashes matched. Re-running `tools.analyze_openfoam.analyze` on each extracted case reproduced the saved diagnostics within relative tolerance `1e-12` and absolute tolerance `1e-14`. The reference-only FD2 audit and the width classifications also replayed. This verifies artifact integrity and the postprocessor result; it does not independently verify the OpenFOAM solver implementation. The machine-readable record is [the replay receipt](../evidence/tests/openfoam-high-gradient-width-hosted-37211431276.json).

GitHub retained the 1,288,865,979-byte artifact through 2027-01-02, with artifact SHA-256 `1f9b6113dde8427e8413ce149ff824d1c083add91dff7f7aa9ab3a1c9d61c277`. The downloaded raw cases and archives remain under the ignored `work/of13-high-gradient-width-hosted-37211431276/` directory; the committed receipt preserves hashes and the artifact reference without adding the multi-gigabyte solver fields to Git history.

This is a uniform-grid manufactured-solution benchmark with an analytic reference and prescribed forcing. `NOT_OBSERVED` means only that this finite set of fine-grid cases did not show standard acceptance hiding a local-quality failure. It does not prove that no other solver blind spot exists, and it does not test molecular ordering, deterministic particle positions, phase transitions, viscosity collapse, a real-fluid singularity, or Navier–Stokes blow-up. The solver can still share mistakes with its case construction or model assumptions. No confirmed software defect emerged from this run, so it gives no basis for an upstream issue or a claim about OpenAI's physical interpretation.
