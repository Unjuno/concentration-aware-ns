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
