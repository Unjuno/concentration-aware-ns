# OpenFOAM high-gradient temporal addendum — 2026-09-30

## Case and provenance

The frozen v2 protocol's `n=64, dt=0.0005, end=0.05` row was rerun in a new
work directory after the original attempt stopped at 36 observed steps / 35
converged steps. The earlier partial log remains preserved under
`work/of13-high-gradient-v2/n64-dt0.0005/`; the new raw case is under
`work/of13-high-gradient-v2-temporal-20260930-dt0005/n64-dt0.0005/`.
The protocol JSON remains byte-for-byte frozen as the pre-run snapshot, so its
historical `status` field still says execution had not begun; current execution
state is in the manifests cited below.

- Protocol SHA256: `838ac4d91d8a816f96cebf02d780a9ec7df265ae3b45748d2a2c795c6d80d93d`.
- Run source commit: `721b7cda5c58dd095d16792a459d69ef1aebce6c`.
- Container image: `sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`, linux/arm64.
- Parent manifest SHA256: `9dc26bad1e249669fa18a3a430712edf8df83445238c1cb846fb4b262debb89c`.
- Archive SHA256: `93a72add2e0f13352bf07e9a050c237756e02aa117d8bbed9f1d50f038afc0b5`.

## Completion and measured quality

The raw solver exited zero, recorded all 100 expected time steps and 100 PIMPLE convergence records, ended with `End`, and wrote endpoint `U`, `p`, `C`, and `phi`. The fixed acceptance gate reports standard acceptance PASS and local quality PASS:

| Quantity | Observed relative error | Threshold |
|---|---:|---:|
| Velocity L2 | 0.4784% | 2% |
| Sampled kinetic energy | 0.02165% | 2% |
| Cell-sampled FD2 gradient peak | 2.6417% | 5% |
| Cell-sampled FD2 vorticity peak | 2.3500% | 5% |
| Shell spectrum | 0.02165% | 5% |

The continuous full-gradient maximum is not certified; the derivative metrics are grid-sampled. This result is one temporal-resolution row, not a temporal convergence conclusion and not an OpenFOAM defect finding.

## Gate correction

The first run of the new orchestration script returned a false incomplete result after the solver had completed. The script counted the substring `Time = `, which also occurs in `ExecutionTime =` and `ClockTime =`. The raw solver output was retained. An independent validation tool now reuses the repository archiver's line-anchored time-step check, confirms the full completion contract, computes diagnostics, creates the archive and verifies every archived regular file and symbolic link. A unit-test fixture now includes `ExecutionTime`/`ClockTime` lines so this parser error cannot recur. The validator output is preserved in `evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005-manifest.json`.

## Quarter-step completion and temporal comparison

The `n=64, dt=0.00025` rerun completed all 200 of 200 steps with 200 PIMPLE
convergence records, endpoint U/p/C/phi, `End`, zero runner exit and both
standard acceptance and local-quality PASS. Its archive hash is
`705be3ab67347eedeb4dad548d4caa3a796b13ea7cd8cca1a70125f7452825c6` and log
hash is `2776137a1b38d01ac854fc7153426131374268cf770d750be844c2fcc525f4f7`.

The fixed n=64 three-step comparison is recorded in
`evidence/tests/high-gradient-of13-v2-temporal-comparison-2026-09-30.json`.
All three archives and completion records were checked, cell centers match
exactly, and non-time input hashes match. The normalized adjacent endpoint
differences are 1.3374e-5 and 9.4658e-6. The descriptive endpoint order is
0.499; exact-velocity errors are 0.4781%, 0.4784%, and 0.4790%, so their
two-point observed orders are slightly negative. These finite-resolution
quantities are not a temporal error certificate.

The additive cross-run index records all six spatial/temporal rows complete.
The frozen high-gradient matrix's specific standard-PASS/local-FAIL concern is
NOT_OBSERVED: n=64 and n=128 both pass both gates. This says nothing universal
about OpenFOAM or about physical blow-up. The prior five-of-six index is
preserved in `manifest-five-of-six-2026-09-30.json`; the original base manifest
is unchanged. Dedicated AMR runs remain unexecuted.
