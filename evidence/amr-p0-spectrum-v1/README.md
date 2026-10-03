# AMR P0 spectrum archived-input audit

[`analysis.json`](analysis.json) records 12 verified states, the complete
outside-cube spectral mass, direct-integral and archived-spatial checks, and
four bit-identical preMap/mapped band arrays. PASS concerns the declared
analytic representation and verification controls. It is not a new solver
accuracy gate, continuous-gradient certificate or overall completion.

Each `*-band.npz` contains integer wavevectors and complex velocity/reference
coefficients. Load with `numpy.load(path, allow_pickle=False)`. Member hashes
are recorded in analysis.json. Shells above index 7 are incomplete cube cuts.
No source data or result from the prior mean study is overwritten.

Raw archives are the four original assets in
[the canonical release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89).
Download them to owned locations and verify hashes against
[`raw-assets.json`](../of13-amr-mean-quality-v1/raw-assets.json).
Create a JSON map of all four case IDs to their local raw tarball paths, e.g.:

```json
{
  "n16-dt0.001": "work/raw/n16/raw.tar.gz",
  "n32-dt0.001": "work/raw/n32/raw.tar.gz",
  "n64-dt0.001": "work/raw/n64/raw.tar.gz",
  "n32-dt0.0005": "work/raw/n32-halfstep/raw.tar.gz"
}
```

From the published code and its locked verification dependencies:

```sh
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_amr_p0_spectrum --raw-map work/raw-map.json \
  --output work/amr-p0-spectrum-replay-new
```

The output directory must be new. No Docker, CFD run or Git object lookup is
required. Protocol and harness hashes must match the frozen input manifests.
This uses analytic cube integration, a lossless voxel repetition and the
corrected FFT; it does not interpolate a smooth field. See the
[`report`](../../reports/openfoam-amr-p0-spectrum-2026-10-03.md) for formulas
and the distinction between P0 spectral mass and ordinary continuum derivatives.
