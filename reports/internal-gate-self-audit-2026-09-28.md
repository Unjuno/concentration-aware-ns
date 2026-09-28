# Internal acceptance-gate self-audit: fixed-step time sequence

## Finding

The OpenFOAM standard-acceptance parser previously required the expected number
of `Time = ...` records, a final time equal to the protocol endpoint, an `End`
marker, per-step PIMPLE convergence messages, and matching residual controls.
It did not check the intermediate time labels. A synthetic log with 50 records,
49 repetitions of `Time = 0.001` and a final `Time = 0.05`, each paired with a
convergence record, was therefore classified `PASS` for `delta_t=0.001` and
`end_time=0.05`.

This is a reproducible false-pass in our **evaluation harness** for malformed
or corrupted logs. It is not evidence of an OpenFOAM defect, and no actual
solver result is reclassified by the synthetic counterexample.

## Correction and evidence

The checker now compares each logged time against `i*delta_t` for all expected
steps, with tolerance `1e-9*max(1,|end_time|)`. It reports whether the sequence
matches and the zero-based mismatching record indices. A completed run with an
incorrect sequence receives standard-gate `FAIL`; a truncated or unparseable
run remains `UNCERTAIN`.

Regression tests cover the malformed duplicate/skipped-time log, a normal
synthetic schedule, the archived OpenFOAM study-v1 run, and the archived
high-gradient v2 `n64, dt=0.001` run. This corrects the local acceptance
instrument only. It does not change solver inputs, local-quality thresholds,
matrix status, or upstream issue dispositions.

Validation after the correction: `python -m pytest -q tests` reports 77 passed
and 5 subtests passed; `python -m unittest discover -s tests` reports 75
passed. The archive audit reports PASS and zero time-sequence mismatches for
all four complete v2 archives.

## Classification and disposition

- Category: evaluation-procedure / benchmark-tooling defect in our own checker.
- Actual solver impact: none established. The new audit tool checked all four
  currently archived complete v2 cases (n=16,32,64,128 at dt=0.001); each has
  50/50 expected timestamps, matching fixed-step order, and standard PASS.
  Their local-quality verdicts and the incomplete matrix verdict are unchanged.
- Upstream report: not filed. The issue is in this repository's parser, not in
  OpenFOAM, SU2, or PhysicsNeMo.
- Scientific interpretation: no inference about a solver defect, singularity,
  physical hazard, particle alignment, or constitutive viscosity.

Reproduce the archive/hash/log audit with `python3 -m
tools.audit_high_gradient_time_sequence`. Reconstructing the split n=128 case
requires the `zstd` command-line utility. The result is stored at
`evidence/tests/high-gradient-time-sequence.json`.
