# OpenAI Lean audit retry: nanoda module discovery

## Result

The 180-minute retry of the pinned OpenAI formalization audit did not produce a
new completed independent-check result. GitHub Actions run
[37240186684](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37240186684)
ended in failure after 1 hour 59 minutes. The visible job annotations report
`nanoda check failed` and `Could not detect module name from lakefile.toml or
lakefile.lean`. The Euler axiom-audit step is not verified by this run.

This is an assurance-pipeline failure, not a Lean compilation diagnosis or a
counterexample to any OpenAI theorem. The run's step logs are not available in
the public page, so this record does not infer whether the preceding Lake build
completed. Earlier pinned clean-build and axiom-audit evidence remains a
separate result.

## Exact compatibility cause

At OpenAI source commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, the project lakefile has a
top-level `name = "NavierStokesAndEuler"` and declares its Lean modules in
three `[[lean_lib]]` tables: `NavierStokes`, `Euler`, and
`ComparatorChallenges`. Its SHA-256 is
`97b2804da5b9a2cd0aaf44ce42b7c39e9947beff9d2ac01a11e0d3d867af1c09`.

The audit workflow pins `leanprover/lean-action` to
`f061402b660e0c34644504b324e830f2991d4865`. At that commit,
`scripts/run_nanoda.sh` looks only for a legacy `[package]` table, then for a
`package` declaration in `lakefile.lean`; it does not inspect top-level TOML
`name` or `[[lean_lib]]`. I downloaded both files from their immutable commit
URLs, confirmed their SHA-256 values, and ran the exact detector extraction
against the pinned OpenAI lakefile. It returned an empty module name although
the three `lean_lib` module names are present.

## Upstream disposition

The same gap is already addressed by the open
[lean-action PR #187](https://github.com/leanprover/lean-action/pull/187),
which proposes detecting the first `[[lean_lib]]` name and adds a TOML fixture.
That PR reports that its full nanoda success path is separately blocked by a
nanoda export-format problem. The OpenAI run is a useful real-project case for
the module-detection change; it does not diagnose or resolve that separate
export-format issue. A concise reproduction was added to the existing PR, so
no duplicate issue was filed. The comment is
[here](https://github.com/leanprover/lean-action/pull/187#issuecomment-5986827987).

The machine-readable source hashes, hosted run status, exact detector result,
and bounded interpretation are in
[`evidence/upstream-refresh/lean-action-nanoda-toml-repro-2026-10-05.json`](../evidence/upstream-refresh/lean-action-nanoda-toml-repro-2026-10-05.json).
