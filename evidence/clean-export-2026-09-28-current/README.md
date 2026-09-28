# Current tracked-only locked replay

Reproduction command (run at repository root with the stated commit checked out):

```sh
python3 -m tools.check_clean_export --locked --destination work/clean-export-2026-09-28-current-replay
```

The run used commit `0a950128f0d49701d6323b8ccd58f71b7e20e715`, Python 3.14.5 on macOS 26.6.2 arm64, and the package set in `summary.json`. The venv install, 25-step report replay, SU2 standard review, and four symbolic checks all exited zero. The strict byte comparison exited nonzero because one of 111 compared files differs only in the NumPy version string (`2.5.3` tracked versus `2.5.2` regenerated); after removing that field, both JSON objects compare equal. This is not recorded as clean-export success. The saved logs are unmodified outputs from the six checks; absolute local paths are omitted from the summary.
