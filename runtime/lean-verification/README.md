# Independent proof-check environment — preparation in progress

The pinned project's ComparatorChallenges/README.md calls for mathlib cache,
Comparator, landrun, lean4export and nanoda_bin. No successful proof build or
independent check is claimed yet. Preparation is isolated under work/lean-verification.

Source: openai/NavierStokesAndEuler at 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538.
Source tar SHA256: e44f67a2bc3c133c14856d73b697f77344b030e3fae2f798254b64dcefbbb772.
Lean: v4.34.0-rc2 Linux aarch64, asset URL/digest in evidence/lean-verification.

The dependency fetcher reads the pinned upstream lake-manifest.json and fetches
all eleven exact revisions as source archives, preserving per-archive hashes.
It creates no Git repositories. Dependencies' own licenses remain applicable.
Lake integration for archive-only packages must be verified before use; this
fetch step does not establish that Lake will build without requesting Git metadata.

`unpack.py` verifies the fixed archive digest before extraction and refuses an
existing destination. Python 3.14 supports the toolchain's Zstandard archive.
Source changes, if any are needed only for package path configuration, must be
recorded separately from the original theorem source. Do not alter proof statements
to obtain a successful check. A Lean build, cache reuse and independent kernel
validation are distinct forms of evidence and must be reported separately.
