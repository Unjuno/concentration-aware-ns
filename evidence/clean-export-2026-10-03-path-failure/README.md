# Clean-export runner failure — 2026-10-03

The first tracked-only export of commit
`2d3983d1a563a2aae368348618a69cca46e2e8b6` created a fresh Python 3.14.5
environment and installed `requirements-verification-locked.txt` successfully,
then stopped at the first report-replay step. The nested pytest process resolved
the host `/run/current-system/sw/bin/python` from inherited `PATH`, rather than
the fresh venv, and exited with `No module named pytest`.

This is a reproducibility-runner environment propagation defect. It says
nothing about the archived solver results or scientific verdicts. The failed
destination remains preserved locally under ignored `work/`; its archive and
logs are represented here by hashes. The runner was corrected to prepend the
venv's platform-specific scripts directory to child `PATH`, and a regression
test was observed failing before that fix and passing after it. A fresh clean
export of the corrected committed runner is still required.

The event record contains the commit and archive identities, exact stage exit
codes, and raw hashes for the relevant logs. Paths have been reduced to
filenames and the host interpreter message.
