# SU2 localized-QoI and residual-location upstream audit

Checked: 2026-10-01 21:48 UTC. The current public release is SU2 8.5.0
(`Harrier`, released 2026-04-27); the default `master` SHA observed is
`bc15466602a687d6fb796d5df7a12ce3fde0949a` (2026-04-28). The benchmark itself
uses its separately frozen v8.5.0 checkout and arm64 image. GitHub reports
`NOASSERTION` for the repository license; the repository `COPYING` contains
LGPL-2.1 and `LICENSE.md` identifies SU2. The upstream tree has no root
`CONTRIBUTING.md`; `.github/pull_request_template.md` asks contributors to
target `develop`, add tests where necessary, and update documentation as needed.

## Existing upstream work relevant to the audit

- [Issue #2353](https://github.com/su2code/SU2/issues/2353) remains open and
  concerns the time at which implicit schemes evaluate time-varying boundary
  conditions and motion. This is related to, but distinct from, the benchmark's
  source-time and output-clock contracts.
- [Discussion #2890](https://github.com/su2code/SU2/discussions/2890), where the
  benchmark's source-time reproducer was reported, is closed but has no accepted
  answer (`isAnswered=false`). A maintainer reply remains visible. Closure is
  not evidence of an adopted fix. No duplicate report was made.
- [Issue #2932](https://github.com/su2code/SU2/issues/2932) requests an opt-in
  `MAX_RES_LOC` history group with the location of each variable's maximum
  residual. It is open, unassigned, and has no comments at this check. In the
  frozen SU2 source tree, `MAX_RES` exposes residual magnitudes, but no
  `MAX_RES_LOC`/`MAXLOC_*` output group exists. This is directly relevant to
  diagnosing where iterative residuals concentrate, but the request is already
  tracked upstream.

## Fresh archive review and interpretation

Re-ran `work/reference-check-env/bin/python -m tools.review_su2_standard`.
The command verified all five archive hashes against the run summary and
recomputed the velocity error, analytic mean-energy comparison, and whether
every physical update met the four frozen inner-residual thresholds. The
result exactly matches the tracked `evidence/tests/su2-standard-review.json`:

| Cases | Velocity and energy thresholds | All-step residual threshold |
|---|---|---|
| n=16, dt=.001 | Fail both | Pass |
| n=32, dt=.001 | Fail both | Fail (48/50 updates) |
| n=64, dt=.001/.0005/.00025 | Pass both | Fail (48/50, 97/100, 193/200) |

Thus no frozen case passes the full observed conjunction of aggregate accuracy
and all-step iterative residual checks. At n=32 the sampled gradient and
vorticity peak discrepancies exceed 11%, but the aggregate accuracy and
all-step residual conditions also fail, so this is not a standard-pass/local-
fail counterexample. At n=64, the aggregate field/energy metrics pass while a
small number of inner iterations do not meet the residual threshold; sampled
derivative discrepancies are below 5%, but their continuous extrema are not
certified. The fixed sequence's near-first-order time differences remain
descriptive and are not an error certificate.

The study therefore demonstrates why residual magnitudes, aggregate solution
error, and local derivative quality should be reported separately. It does not
show an SU2 defect or a reproduced acceptance blind spot. In addition, archived
history does not expose the per-step location of maximum residual; #2932 is an
existing potential remedy for that observability gap, not a new issue to file.
No upstream report was submitted in this audit. Detailed live state and
reproduction metadata are in
`evidence/upstream-refresh/su2-localized-residual-upstream-audit-2026-10-02.json`.
