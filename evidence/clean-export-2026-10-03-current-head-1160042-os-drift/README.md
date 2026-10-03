# Current-head clean-export comparison: OS metadata drift

Fixed commit `1160042e53d2db0a372f6a7a60bec9570784bd06` was exported from tracked Git content into a fresh locked CPython 3.14.5 environment on macOS 27.0.1 arm64. Dependency installation, all 43 report-replay steps, and all six follow-up checks exited zero. The final comparison found seven changed files, so this is not a clean-export PASS.

Field-level comparison against the fixed commit found only two changed values in source evidence: `platform` changed from macOS 26.6.2 to macOS 27.0.1. Five SU2 report hashes changed because they hash those two evidence files. Numeric fields, verdicts, and other evidence fields matched. This records runtime provenance drift after an OS update; it does not indicate solver behavior or scientific-result change.

The sanitized result and replay/check logs are preserved here; the local absolute path in `install.log` is replaced with `<CLEAN_EXPORT_ROOT>`, and its saved digest reflects that sanitized file. The original unmodified attempt remains under the local ignored `work/clean-export-2026-10-03-current-head-1160042-retry1/` directory.
