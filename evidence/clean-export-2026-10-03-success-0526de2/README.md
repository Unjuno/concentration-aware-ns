# Fixed-commit clean export: 0526de2

The tracked-only archive for commit `0526de204d4cab95a432db254c148bdb1773c0bc` was extracted to a fresh directory and checked in a new locked virtual environment with CPython 3.14.5 on macOS 27.0.1 arm64. All 44 published report/evidence replay steps and all six additional checks exited zero. The post-replay comparison covered 230 tracked files and found `changed_files: []`.

This establishes same-host, same-interpreter reproducibility of the tracked Python postprocessing and evidence path for this fixed commit. The checks do not rebuild or rerun OpenFOAM, SU2, or PhysicsNeMo; they do not run Lean or upgrade any solver, AMR-quality, theorem, or physical verdict.

`result.json` records the commit, archive and runner hashes, locked package set, comparison result, check commands, and raw plus sanitized log hashes. Local absolute paths are replaced with `<REPO>` and `<CLEAN_EXPORT_ROOT>` in the saved result and logs.
