# Clean tracked-export replay at `e039e4b`

`run.json` records a fixed-commit clean export from source commit
`e039e4b4098fedda2f53f76a71d3a447e384b5c1`. The export created a fresh Python
environment on macOS 27.0.1 arm64 with CPython 3.14.5 and installed the exact
versions in `requirements-verification-locked.txt`.

Reproduce from the repository root:

```sh
python3 -m tools.check_clean_export \
  --locked \
  --revision e039e4b4098fedda2f53f76a71d3a447e384b5c1 \
  --destination work/clean-export-2026-10-04-e039e4b
```

The fresh tracked archive hash is recorded in `run.json`. The report replay
completed all 47 steps, including 399 passing tests, one skip and 89 passing
subtests. Seven further analytic/review commands passed. It compared 328
tracked report and test-evidence files before and after replay; no file changed.
`SHA256SUMS` verifies every included log and manifest.

Two log copies contain host-specific checkout paths; those prefixes were
normalized to `<checkout>` or `<workdir>`. `run.json` preserves both the
original run-log hashes and the hashes of the included normalized copies.
The original result JSON and full tracked archive remain in the local ignored
`work/clean-export-2026-10-04-e039e4b/` directory; the source commit and archive
hash make them independently reconstructible.

This checks Python postprocessing and analytic replays on the recorded host. It
does not rerun OpenFOAM, SU2 or PhysicsNeMo, train networks, execute Lean, or
change any scientific acceptance verdict.
