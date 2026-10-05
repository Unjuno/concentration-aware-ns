# Fixed-commit clean export: b0e590e

The tracked-only archive for `b0e590e3c1b9b19044748fac7ad06109785f6fe5` passed all 46 report/evidence replay steps and six follow-up checks in a fresh locked CPython 3.14.5 environment on macOS 27.0.1 arm64. All 234 compared tracked report/test-evidence files stayed byte-identical. The fresh test stage reports 233 passed, one skipped and five subtests passed; its log is preserved as `replay-tests.log`.

This verifies same-host Python postprocessing/evidence reproducibility only. No solver, Lean proof or physical verdict was rerun or upgraded. The manifest preserves raw and saved wrapper/test-log hashes; absolute local paths are replaced with `<REPO>` and `<CLEAN_EXPORT_ROOT>`. All 46 internal raw replay log hashes were also checked against the fresh replay summary before this record was saved. Later evidence/documentation commits are separate from this tested source commit.
