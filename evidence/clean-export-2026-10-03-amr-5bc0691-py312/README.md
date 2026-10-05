# CPython 3.12 clean export: strict identity failed

Fixed commit `5bc0691a60d2282aef6828f5da6d5f2a803673e9` completed all 47 report/evidence replay steps and six follow-up checks in a fresh locked CPython 3.12.10 environment on macOS 27.0.1 arm64. Tests passed 264, with one skip and 70 subtests. The new AMR derivative-decomposition JSON is byte-identical to the tracked result.

The strict comparison failed: nine of 237 compared files changed interpreter/platform metadata or hashes referring to that metadata. The linked SU2 diagnostic-replay input was separately traced to the same metadata-only change. `identity-differences.json` records every differing JSON field and both file hashes; scientific values/verdicts in these differences did not change. This does not convert the strict identity failure into PASS or certify arbitrary cross-version reproduction.

The retry uses the same source commit and dependency lock with CPython 3.14.5 explicitly selected, matching the recorded baseline, in a fresh path. This attempt remains preserved. All wrapper and internal replay log hashes were checked before publication. Paths are sanitized; `result.json` retains separate raw and published log hashes. No solver, training, Lean proof or physical conclusion was rerun or upgraded.
