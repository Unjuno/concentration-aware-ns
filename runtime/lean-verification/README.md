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

## Verified archive integration

`use_archive_paths.py` rewrites only the project lake manifest and two direct
requirements in lakefile.toml, preserving upstream backups. Run it after fetching
and unpacking. `check_sources.py` compares every archived Lean source byte with
the extracted copy; evidence/lean-verification/source-byte-check.json records
counts and list hashes. This checks source identity, not theorem validity.

The pinned Lean binary and `lake env lean --version` execute successfully in
the existing SU2 Linux container image. The cache executable also builds.
The initial downstream `lake exe cache get` exits because mathlib compares Git
manifest entries with our path entries. No revision discrepancy is established
by this diagnostic. The dependencies were fetched at their original pins.

Run the built cache from mathlib's own directory under the project's Lake
environment, preserving mathlib's original manifest and cache hash inputs:

```sh
docker run --rm --name cans-lean-cache \
  -e XDG_CACHE_HOME=/verify/cache -e LEAN_NUM_THREADS=2 \
  --entrypoint /bin/bash \
  -v "$PWD/work/lean-verification:/verify" -w /verify/source \
  concentration-aware-ns:su2 \
  -c 'export PATH=/verify/toolchain/bin:$PATH; lake env bash -c "cd /verify/packages/mathlib && .lake/build/bin/cache get"'
```

Upstream Cache/Requests.lean runs the downstream manifest comparison only outside
the mathlib root; Cache/IO.lean identifies that root by its Mathlib directory.
This invocation requires no changes to the cache implementation or Lean sources.
Retrieval and decompression of all 8,747 files completed with exit code zero;
cache-result.json records the log hash. Project type checking and independent
Comparator/kernel checking remain separate outstanding steps. An origin warning is expected for
source archives; the tool reports its official mathlib4 fallback explicitly.

The first project proof build targets `+NavierStokes.ComparatorSolution`, which
imports both R3 and periodic theorem adapters and prints their axioms. It runs
under the same Docker invocation above with `--cpus=2 --memory=10g`, container
name `cans-lean-ns-build`, and final command
`lake build +NavierStokes.ComparatorSolution`. Its log is retained separately
as navier-stokes-build.log. A started build is not a successful check.
