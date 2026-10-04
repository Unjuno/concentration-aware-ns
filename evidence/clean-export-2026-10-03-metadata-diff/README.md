# Clean-export metadata comparison — 2026-10-03

The corrected exporter at commit `a6e2ce5f13d53478f1e22bd4333435f3e6df488a`
ran the locked dependency install, all 42 report-replay steps, and all six
post-replay checks successfully. The final clean-export result was nevertheless
`success: false`: two generated evidence JSON files differed only in
environment metadata.

- The force-scaling record stored an absolute virtual-environment interpreter
  path, which necessarily changed in a fresh export.
- The spherical-orientation record was originally generated with Python
  3.12.10, while this export used Python 3.14.5; the recorded platform string
  also differed.

No analytical identity or scientific result differed. This is a provenance /
artifact-portability issue, not a solver defect. The force-scaling record has
since been changed to store the portable interpreter implementation rather
than an absolute path. The next clean export is being run from Python 3.12.10,
matching the pinned evidence-generation interpreter. Detailed command exit
codes and raw log hashes are in `result.json`; precise field-level differences
are in `metadata-diff.txt`.
