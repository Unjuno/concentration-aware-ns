# Tracked-only replay including restart findings

Fixed commit: `3678eb8`. Fresh same-host Python environment, with no borrowed
work files. All 18 replay steps and five additional analytic/standard-review
checks exit zero; the replay includes 50 tests and 93 gate artifact checks.
The restart wrapper reproduces the documented scientific FAIL rather than
relabelling it as a pass.

Overall strict byte-equality result remains **FAIL**: six of 75 compared report
and test files differ. Inspection finds NumPy 2.5.2 -> 2.5.3 metadata and its
propagated hashes only. The related diagnostic replay JSON, outside that
75-file comparison, was also inspected and differs only in the same metadata.
All inspected numeric values and verdicts are unchanged. This is not a claim
of byte identity for every generated file.

`result.json` retains commands, environment, archive identity and log hashes;
`inspected-differences.json` records exact JSON leaf changes. Regenerated files
and the complete report replay logs are preserved. The large export and venv
remain untracked under work/clean-export-2026-09-27-restart.

No solver build, training, Lean or independent kernel execution occurred in
this check. Reproduce with:

```sh
python3 -m tools.check_clean_export --revision 3678eb8 --destination work/clean-export-restart-reproduction
```
