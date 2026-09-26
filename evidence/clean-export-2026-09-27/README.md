# Fixed-commit clean-export replay, 2026-09-27

Tested commit: `60302db8e779b387304ff4f5d925bb6566f0b3bc`.

The tracked-only archive was extracted without the working `work/` directory,
and a fresh virtual environment was created on the recorded host/interpreter.
Dependency installation, thirteen replay steps and five additional checks all
exited zero. The replay includes 36 tests and 93 artifact-link checks.

The strict byte-equality gate **FAILED**: six of 66 compared report/test files
changed. `result.json` intentionally retains `success: false`. Inspection of
all JSON differences found only NumPy version metadata (2.5.2 to 2.5.3) and
propagated evidence hashes. The diagnostic replay outside the 66-file comparison
also changed only that version field. Numeric values and scientific verdicts
in these compared files are identical. This is not a claim that every generated
file is byte-identical or that every possible environment is supported.

`differences.json` records every changed JSON leaf in those seven inspected
files; `regenerated/` preserves their new contents. Original logs are copied
unchanged and their hashes were checked against `result.json`. Absolute paths
in the logs describe the original run.

Reproduce from the repository (choose an unused destination):

```sh
python3 -m tools.check_clean_export --revision 60302db8e779b387304ff4f5d925bb6566f0b3bc --destination work/clean-export-reproduction
```

Dependencies are installed from the revision's requirements; NumPy is not
exactly locked, so environment metadata can legitimately differ. This is
same-host postprocessing verification, not a new solver, training, or Lean run.
The eleven localized acceptance verdicts remain UNCERTAIN.
