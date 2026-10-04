# Matched full-horizon SU2 CFL pair — run 37180101797

The paired result archive is the GitHub Actions artifact named in
`run-metadata.json`. It contains a fresh CFL=10 baseline and CFL=100 control
at n=32, dt=0.001, t=0.05, run sequentially with one measured linux/arm64
image. The report keeps inner residual convergence separate from solution
quality and does not make a source-defect or physical claim.

`pair-review.json` is the hosted review. `independent-review.json` was
regenerated locally from the downloaded `baseline/results` and
`control/results` with the repository's locked Python dependencies:

```sh
uv run --python 3.14 --with-requirements requirements-verification-locked.txt \
  python -m tools.review_su2_full_horizon_cfl_pair \
  --baseline-root evidence/su2-full-horizon-cfl-pair-37180101797/baseline/results \
  --control-root evidence/su2-full-horizon-cfl-pair-37180101797/control/results \
  --protocol protocols/su2-n32-full-horizon-cfl-control-v1.json \
  --output NEW_REVIEW_JSON
```

The frozen historical baseline is separately checked by
`local-historical-baseline-replay.json`. The hosted raw artifact expires
2027-01-02; its ID, byte size, and ZIP digest are recorded in
`run-metadata.json`. The 725 MB baseline artifact holding the saved image tar
is a separate Actions artifact, also identified there; the pair artifact
preserves the image audits, receipts, and all raw case results but does not
contain the full image tar.
