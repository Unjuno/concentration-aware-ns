# Foundation 13 exact-control cross-image replay — 2026-10-05

## Result

The current PR head `82c9ae9eb3f4ccd1189891b36015d5cbf93c1b7c` completed the
six-case smooth forced-periodic calibration matrix in hosted Foundation 13.
All six archives independently replayed, all six retrospective standard
stopping checks pass, and all 36 replayed scalar diagnostics match the prior
complete run exactly even though the source commit, image ID, and raw archive
hashes differ. The comparison receipt records those distinctions explicitly.

This is evidence of reproducibility for the fixed smooth calibration case. It
does not exercise localized concentration, prove continuum extrema, or support
particle, molecular, constitutive, or engineering claims. Temporal convergence
order remains `UNCERTAIN`: the total-error changes do not isolate temporal
error from the fixed-grid spatial floor.

## Provenance and replay

- GitHub Actions run: [37244697803](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37244697803)
- Source commit: `82c9ae9eb3f4ccd1189891b36015d5cbf93c1b7c`
- Frozen protocol SHA-256: `6e7f52520159c1c65dd3e1e4a48152876c2807d45ce89f29030c7a8022206e78`
- OpenFOAM image: `sha256:95c675f5673951d4e639fe69a7a05f587775edd5ca3d828f554406ccbba7e9ef` (`linux/arm64`)
- Artifact ID: `11318029983`; GitHub-reported and locally recomputed ZIP SHA-256 both equal `23f509b33ddd2d4c099b96b1facb9020adef455ad6920e1934f7d5c305612136`.
- `tools.verify_forced_periodic_openfoam_run` replayed all six archived runs. Spatial velocity orders were `1.9546194257342775` and `2.009709031502043`; gauge-free pressure orders were `1.853310827109758` and `2.1946908835496957`.
- `tools.compare_forced_periodic_control_runs` compared the replay receipt with the earlier run from source commit `1cacf3c282a2c6ea5a81354865bba1ab0e932427` and image `sha256:383b0f958aa9867af6e2db9ec7681141393c9d213cd821c1f68a33f4353f0baf`. Protocols and all replayed scalar metrics match; raw archive hashes and image IDs differ.

The new run manifest's in-run diagnostic decimals differ in a few final floating
digits from the archive-recomputed values. The comparison uses the independent
archive-replay receipts, and that scope is kept explicit rather than
overwriting either record. The complete new run archive, manifest, protocol,
independent replay, comparison, and artifact digest receipt are retained in
[`evidence/of13-forced-periodic-control-hosted-82c9ae9/`](../evidence/of13-forced-periodic-control-hosted-82c9ae9/).

## Same-head verification workflow

Python verification run [37244697840](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37244697840)
also succeeded on the same PR head. Its artifact is retained in
[`evidence/pr4-ci-verification-37244697840/`](../evidence/pr4-ci-verification-37244697840/).
The hosted verification replayed the published Foundation 13 cell-point
samples and analytic enclosures. The exact rational scalar implications
verified and the analytic JSON records were byte-identical. For n=64, a few
finite floating secant diagnostics differed at roughly `2e-17`; the checker
preserved these differences while confirming matching native selection and
analytic enclosures. This is a finite query replay, not a proof of global
continuity or correctness for every floating search input. The same workflow
recomputed the forced-periodic candidate's symbolic residual identities as
exact zero.

At the time of this report, PR #4 is open with all required checks complete and
GitHub reports `CLEAN`. The still-running shared SU2 matrix and pinned OpenAI
Lean build are separate gates; neither is counted as complete here.

## Disposition

This repeat strengthens the exact-control path and archive pipeline, not the
benchmark's primary local-concentration hypothesis. No new upstream software
defect is indicated and no external issue was filed.
