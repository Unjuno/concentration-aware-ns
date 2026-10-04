# Guarded fresh-export replay of the P0 spectrum audit

The exported source at `e6e3480cfce44c3eceda561363501b50972258a6` reruns all
four raw archives and twelve states. The analysis JSON and all twelve band
arrays are byte-identical to the published artifacts. See `manifest.json`.
The source has no .git directory; a Python audit hook rejects subprocess,
system/exec/spawn, network connect and Git-path open events during analysis.
Every loaded tools module must originate in the export. The raw tarballs are
external original inputs, each checked against its frozen hash and members.
This is not a general syscall sandbox for native library internals.

The initial wrong-CWD repeat and wrong relative-path wrapper launch are
recorded and excluded from the accepted independence check. Only the final
separately created, correctly launched guarded replay is accepted.

To reproduce: export the named Git commit to a new source directory, install
its locked dependencies, keep the provided `isolate_replay.py` beside that
source directory named `source`, and run from inside `source`:

```sh
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python ../isolate_replay.py --raw-map /absolute/path/to/raw-map.json \
  --output /absolute/path/to/new-results
```

The wrapper asserts its actual working directory, records module origins and
forbids Python-level external process/network/Git-file access. The source
export archive and input map remain locally preserved; raw inputs are public
release assets. No CFD, proof or older 47-step report replay is rerun here.
