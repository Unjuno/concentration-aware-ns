# OpenFOAM Foundation 13 single-case repeat

This archive repeats the frozen `n=64, dt=0.0005, end=0.05` row in a new run
root. Run provenance is in `run-environment.json`; the complete case tarball,
completion manifest and comparison report are beside this file. The run used
source commit `0dc1e99b06ef1632e9199891c8382a21ee2a267b`, protocol SHA256
`838ac4d91d8a816f96cebf02d780a9ec7df265ae3b45748d2a2c795c6d80d93d`, and the
recorded Foundation 13 linux/arm64 image ID.

The solver completed 100/100 steps and 100/100 PIMPLE convergence records.
Against the earlier archived run, all four endpoint fields are byte-identical
and all five listed error metrics match exactly. The raw archives differ in
runtime metadata and log hashes; see `comparison.json` for the exact member
comparison. This is one-case numerical reproducibility evidence. It does not
establish a general solver property or any physical interpretation.

The comparator also checks the evidence chain before comparing results: it
rehashes every archived input, independently parses the 100 raw time labels and
PIMPLE convergence records, requires zero runner exit and terminal `End`, and
cross-checks the raw log and endpoint hashes against diagnostics and manifests.
It rejects any raw archive difference outside the five runtime-metadata/log
members listed in `comparison.json`. Four adversarial fixtures cover a coherently
rewritten time label, an unexpected archive difference, and a tampered manifest
verdict, in addition to the clean repeat. These are checks of this comparator's
acceptance logic, not further solver runs.

The comparison can be replayed from the repository root with the locked
verification environment:

```sh
work/reference-check-env/bin/python -m tools.compare_openfoam_repeat \
  --baseline-manifest evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005-manifest.json \
  --baseline-archive evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005.tar.gz \
  --repeat-manifest evidence/of13-high-gradient-repeat-2026-10-01/manifest.json \
  --repeat-archive evidence/of13-high-gradient-repeat-2026-10-01/n64-dt0.0005.tar.gz \
  --output evidence/of13-high-gradient-repeat-2026-10-01/comparison.json
```

To execute the case again, use a clean checkout of the recorded runner commit,
the recorded image and a fresh work root:

```sh
work/reference-check-env/bin/python -m tools.run_high_gradient_temporal_case \
  --dt 0.0005 --run-root work/of13-high-gradient-repeat-new
```
