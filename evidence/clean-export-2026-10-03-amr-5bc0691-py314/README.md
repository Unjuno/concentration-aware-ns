# CPython 3.14 fixed-commit clean export: strict identity passed

Fixed commit `5bc0691a60d2282aef6828f5da6d5f2a803673e9` passed all 47 report/evidence replay steps, six follow-up checks and strict byte comparison of 237 unchanged report/test-evidence files in a fresh locked CPython 3.14.5 environment on macOS 27.0.1 arm64. Tests passed 264, with one skip and 70 subtests.

The explicit interpreter matches the recorded baseline. The prior CPython 3.12 export passed all computations but failed strict artifact identity due to environment metadata and cascading hashes; its full result, field differences and logs remain in the neighboring `clean-export-2026-10-03-amr-5bc0691-py312` folder. No scientific values/verdicts in those differences changed. That failure has not been converted into a strict PASS.

All wrapper and 47 internal replay log hashes were verified before publication. `result.json` preserves separate raw and published hashes; local repository/export/uv prefixes are sanitized in logs. This verifies the named Python postprocessing export, not CFD, model training, Lean proofs or physical claims. Later publication commits are separate from the tested source commit.

Reproduction from a clone containing the commit, with the recorded interpreter available:

```sh
/path/to/python3.14 -m tools.check_clean_export \
  --revision 5bc0691a60d2282aef6828f5da6d5f2a803673e9 --locked \
  --destination work/clean-export-amr-new
```

The destination must not exist. The source archive and fresh environment remain under ignored `work/` locally; published logs and hashes do not include those large temporary files.
