# Archived public diagnostic artifacts

Source: [`CokieMiner/nsblowup`](https://github.com/CokieMiner/nsblowup), commit `658812f7b02ea00065c54818e699105914507f9c` (Apache-2.0). GitHub's `artifacts-v1` release tag resolved to this commit during capture (2026-10-05). Files below were downloaded from that release and SHA-256 checked against the asset digests returned by the GitHub Releases API.

| File | SHA-256 | GitHub asset SHA-256 |
|---|---|---|
| `reference_report.txt` | `0c110670f5c29676410eb2c66d2709a5b1cbf65c4a5ad0d7c916f2d5223eec68` | `0c110670f5c29676410eb2c66d2709a5b1cbf65c4a5ad0d7c916f2d5223eec68` |
| `verify_report.txt` | `3b8b9bc26ffc1ec23022f759df78ee283d59eded05933b6467e3a4b6ca69c35c` | `3b8b9bc26ffc1ec23022f759df78ee283d59eded05933b6467e3a4b6ca69c35c` |
| `wave_calibration.json` | `98be599b6f9ad1b46c36280b54a4ff3a1b73e869bcf817101c3c7e38fbd524da` | `98be599b6f9ad1b46c36280b54a4ff3a1b73e869bcf817101c3c7e38fbd524da` |

These are the publisher's artifacts, not independently generated simulation outputs. The calibration records four zero wave coefficients, equal residual energy before/after, and zero relative reduction. The reference report independently included in the same release labels the carrier cases unresolved and says the fit does not test the paper's cancellation mechanism at this resolution. The separate verify report is an MMS implementation check for its stated 32³ tests only.
