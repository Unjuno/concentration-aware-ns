# Foundation 13 prospective AMR mean-quality v1

Frozen execution commit: `3566f89058071910a41bb68010eb258c7bbc3d74`.
Hosted run: [37124421538](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37124421538).
Protocol: [`of13-amr-mean-quality-v1`](../../protocols/of13-amr-mean-quality-v1.json).
Read `matrix.json` and the separate standard/local/reference gates in every
case's `analysis.json`; workflow success is not numerical quality PASS.

The original raw tarballs are release assets listed with bytes and SHA256 in
`raw-assets.json`. Download each case's named asset from
[the canonical release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89)
to that case directory as `raw.tar.gz`; verify its SHA256 before replay.
Nothing from the older user-owned n128 archives is changed.

From the frozen code plus the published supplemental replay tools and locked
verification environment:

```sh
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.analyze_amr_mean_quality --evidence-root evidence/of13-amr-mean-quality-v1/n16-dt0.001
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.replay_amr_mean_archive --evidence-root evidence/of13-amr-mean-quality-v1/n16-dt0.001 \
  --output work/n16-replay.json
```

Strict regenerated input byte identity fails between Linux/macOS for the
initial U values. See the preserved failure and per-case comparisons. To run
separate machine-scale numerical compatibility, explicitly add
`--allow-input-ulp-drift`; its result retains strict byte identity FAIL.
Source/harness hashes must still match the frozen manifest. No CFD is rerun.
The compiled module binary is hash-recorded but not included in the raw archive;
this replay is not a compiled-binary rebuild or full-runtime source proof.

Optional archived-map diagnostic:

```sh
python -m tools.audit_amr_mean_transfer --evidence-root evidence/of13-amr-mean-quality-v1/n16-dt0.001 \
  --output work/n16-transfer.json
```

Use `tools.summarize_amr_mean_quality` on all four `analysis.json` files.
Missing/mixed results or missing/failed controls must remain UNCERTAIN.
These mean gates leave continuous peaks, AMR spectra and physical conclusions open.

The raw module sources retain their upstream copyright/GPL headers.
[`OpenFOAM-13-COPYING`](OpenFOAM-13-COPYING) accompanies those sources and is
also available with the raw release; see `third-party-source-notice.json`.
