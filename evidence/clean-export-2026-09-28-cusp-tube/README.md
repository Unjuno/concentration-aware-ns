# Fresh locked clean-export verification

Reproduce from repository commit `03ce175fcf26d17869de330720f2dfe8a49c4481`:

```sh
python3 -m tools.check_clean_export --locked --destination work/clean-export-2026-09-28-cusp-tube
```

The runner exported only tracked files into a new directory, created a fresh environment, installed the locked postprocessing dependencies, replayed 26 published report/check steps, and compared reports plus test evidence. All six runner checks exited zero; all 26 replay steps and 85 unittest cases passed; the 113 compared files had zero changes. This validates Python postprocessing and archived reports only. It does not build/run CFD solvers, train PhysicsNeMo, execute Lean, or upgrade any scientific verdict.

`summary.json` records the fixed commit, source archive hash, dependency set, check hashes and exact comparison result. `report-replay/` holds all child outputs; its summary normalizes interpreter paths while retaining the SHA-256 of the raw generated summary. Runner logs with local absolute paths were not copied.
