# Foundation 13 forced-periodic control repeat across runtime images

The six-case forced-periodic smooth-solution matrix was rerun by hosted
Foundation 13 workflow run
[37196452449](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37196452449)
from source commit `1b40ece31627cde6cba6da7e7ba8bb5706dddc2d`. The run completed
all 6 cases at the prescribed end time with exit code 0 and exact requested
step counts. The newly built ARM64 image ID was
`sha256:667bd7977fab8f295c7423272cb588ba59372128b48a559ddcb24ae1b3be8c66`.

The raw Actions artifact was downloaded and independently replayed with
`tools.verify_forced_periodic_openfoam_run`. All six case archive hashes,
input/output field digests, recorded diagnostics and logged time grids passed.
The existing Foundation 13 standard stopping check, applied retrospectively,
passes all six rows. The protocol did not freeze a local-quality threshold for
this calibration field, so every local-quality label remains `UNCERTAIN`; the
temporal-order assessment remains `UNCERTAIN` because total error is not
separated from the spatial error floor.

The previously verified run 37174784940 used source commit
`1cacf3c282a2c6ea5a81354865bba1ab0e932427` and image
`sha256:383b0f958aa9867af6e2db9ec7681141393c9d213cd821c1f68a33f4353f0baf`.
An exact comparison of the six replayed metrics for all six cases gives a
maximum absolute difference of zero, and the spatial velocity and pressure
observed orders also match exactly. All six raw archive SHA-256 values differ
between runs. This is numerical-diagnostic reproducibility across two recorded
runtime builds, not byte-identical archives or proof of continuous solver
extrema.

The spatial result remains: velocity relative L2 errors are 2.706e-3,
6.980e-4 and 1.733e-4 for n=16/32/64, with observed orders 1.955 and 2.010;
gauge-free pressure errors are 1.168e-1, 3.232e-2 and 7.060e-3, with observed
orders 1.853 and 2.195. At n=32, the three time-step cases complete at 25/50/100
steps, but their temporal-order conclusion remains `UNCERTAIN`.

A third hosted run, [37197955693](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37197955693),
was executed at PR source `739a4bf76cc39b4af3ea8e31b46bdf41cb56120f` on image
`sha256:39e4a262019bd81627d9b1e3357ea13f4b4ba2606974b543b6752383f026cb8a`.
Its six archives and diagnostics independently replay, and all six metrics for
every case exactly match both prior runs. The three builds used three distinct
image IDs; every per-case archive digest differs across runs. The new receipt,
both pairwise comparisons, build provenance and replayable raw case bundle are
under [`evidence/of13-forced-periodic-control-hosted-739a4bf`](../evidence/of13-forced-periodic-control-hosted-739a4bf/verification.json)
and in [the third-run release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-forced-periodic-control-rerun-739a4bf),
whose remote asset digest matches the local package SHA-256.

The permanent replay receipts, both run manifests/provenance and build
inventory are under
[`evidence/of13-forced-periodic-control-hosted-1b40ece`](../evidence/of13-forced-periodic-control-hosted-1b40ece/verification.json).
The full six-archive bundle is published as
[release asset `of13-forced-periodic-control-rerun-1b40ece.tar.gz`](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-forced-periodic-control-rerun-1b40ece);
its SHA-256 is in `run-metadata.json` and `release-asset.sha256`.

This remains a smooth periodic control. It does not test the localized
high-gradient profile or AMR, and it does not support molecular, singularity,
constitutive-transition, or engineering conclusions.

A fourth hosted run, [37199509312](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37199509312), from PR source `0622352cba68c9c1814d249154de94cdd6d40372` completed all six cases on image `sha256:eddcfa196d21d4b027370be0449399c853787462e50c857b02bd95497ac9f193`. I downloaded its 39,827,681-byte Actions artifact and independently replayed each archive, field/input digest, scalar diagnostic, step count, exit receipt, and retrospective Foundation stopping check. All six scalar diagnostics for every case exactly match the prior three-run matrix (maximum absolute difference 0); all archive SHA-256 values differ. The fourth receipt and provenance are preserved in [`evidence/of13-forced-periodic-control-hosted-0622352`](../evidence/of13-forced-periodic-control-hosted-0622352/verification.json). This is repeatability of these diagnostics across four recorded image builds. The spatial sample errors and continuum extrema remain subject to the limits above, local quality remains `UNCERTAIN`, and the completed time-step sweep still does not isolate temporal truncation error from the spatial error floor.

A fifth verified matrix is [workflow run 37200525739](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37200525739), from commit `d138edc23c33d5f2a5dc540f10afda15f10955ac`, on image `sha256:40ab4665a484a38f4d6e0c34162d44afffbd4a9a4b0c9d69bf08b7051a7b06c2`. The downloaded 39,823,522-byte archive passed the same independent six-case replay, including input/field hashes and the retrospective standard stopping check. All six scalar diagnostics per case exactly match the four earlier matrices; all archive SHA-256 digests differ. The fifth run's provenance, raw manifests, and comparison receipt are under [`evidence/of13-forced-periodic-control-hosted-d138edc`](../evidence/of13-forced-periodic-control-hosted-d138edc/verification.json). This extends diagnostic reproducibility to five recorded builds; it does not change the `UNCERTAIN` quality and temporal-order dispositions or provide evidence about the high-gradient or molecular hypotheses.

A sixth hosted run, [37201155941](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37201155941), completed the same six cases from source `661a3969e2466bb2473bb52ee32dbd1269813aca` on image `sha256:62ae72eae52c3cc43db4165e61f907c8c63575ac6c745f2af757a4698833b0b8`. I downloaded its 39,820,267-byte Actions artifact, checked the ZIP, and independently replayed all six case archives. Every input/output digest, diagnostic, time-grid count, exit status, and retrospective standard stopping check passed. Comparing its replay with run 37200525739 gives exact equality for all 36 scalar diagnostic values (maximum absolute difference zero); each case archive digest and the image ID differs. The artifact ZIP SHA-256 is `d87aadd9380ed347b0617c67f49351f1209489d7511927f0c3b266ef986b6e1c`. The manifest, replay, comparison, build log, image inspection and package inventory are preserved in [`evidence/of13-forced-periodic-control-hosted-661a396`](../evidence/of13-forced-periodic-control-hosted-661a396/verification.json); the raw ZIP is a workflow artifact and expires 2027-01-02.

The six-run record confirms repeatability of this smooth calibration matrix across recorded builds. The hosted Linux verification job for the same source also passed 439 tests, three skips and 89 subtests, and its published cellPoint replay kept all analytic JSONs byte-identical. One n64 native floating-secants diagnostic differs by roughly 1e-16 from its earlier macOS value; selected candidates, cell membership, explicit interpolation and validity checks agree. This small cross-platform diagnostic difference remains visible in the saved receipt. None of these checks resolves the localized high-gradient result, continuous solver-field extrema, local-quality gates, or the temporal-order uncertainty.
