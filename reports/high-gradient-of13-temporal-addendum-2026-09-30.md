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

## Independent repeat of the half-step row (2026-10-01)

To distinguish archived post-processing replay from solver execution, the
`n=64, dt=0.0005` row was executed again in a new work root using the same
Foundation 13 image ID and frozen protocol. The new run source commit is
`0dc1e99b06ef1632e9199891c8382a21ee2a267b`; its Docker CLI, context, image,
protocol and input hashes are recorded under
`evidence/of13-high-gradient-repeat-2026-10-01/`. The new run completed 100/100
steps, recorded 100/100 PIMPLE convergence messages, ended with `End`, and
passed the same standard and local gates.

An independent archive comparator checked 40 files in each tarball. Thirty-five
were byte-identical. The only five raw differences are `command.json`,
`diagnostics.json`, `log.blockMesh`, `log.centres`, and `log.foamRun`: after
normalizing the case mount path, runtime date/time/host/PID, cumulative
ExecutionTime/ClockTime and the diagnostics pointer to the raw solver-log hash,
the commands, logs and diagnostics match. In particular endpoint `U`, `p`,
`C`, and `phi` are byte-identical, as are velocity, energy, spectrum, sampled
gradient-peak and sampled-vorticity-peak errors. The repeat archive and source
log hashes differ because these runs have different execution metadata. The
comparison is reproducible with `tools.compare_openfoam_repeat`; its success is
evidence for one fixed case on one image, not a guarantee for all OpenFOAM
executions, a physical validation, or a mathematical conclusion.

The additive cross-run index records all six spatial/temporal rows complete.
The frozen high-gradient matrix's specific standard-PASS/local-FAIL concern is
NOT_OBSERVED: n=64 and n=128 both pass both gates. This says nothing universal
about OpenFOAM or about physical blow-up. The prior five-of-six index is
preserved in `manifest-five-of-six-2026-09-30.json`; the original base manifest
is unchanged.

## Dedicated AMR and fixed-final-mesh controls

All three frozen high-gradient AMR budgets completed in
`work/of13-high-gradient-amr-v2-20260930/`. Compact tracked summaries are
`evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json` and
`evidence/of13-high-gradient-remap-control-v2-manifest-2026-09-30.json`;
event-level selections and associated input hashes are summarized in
`evidence/of13-high-gradient-amr-event-audit-2026-09-30.json`;
complete raw solver trees remain under ignored `work/` paths. cap4096 stayed at
4096 level-0 cells because the budget disallowed refinement. cap5000 produced
16,640 cells (2,304 level 0 and 14,336 level 1); cap100000 produced 101,760
cells (2,176 level 0, 3,328 level 1, 96,256 level 2). The 5000 and 100000
budgets therefore overshot by factors 3.328 and 1.0176. Exact identities/counts
of sensor candidates excluded by the budget remain UNOBSERVED. For cap100000,
the source-level event replay explains the sequence: from 16,640 cells the
nominal allowance is 11,908 candidates, but source appends whole refinement
levels before checking that allowance; 12,416 level-group candidates therefore
produce 103,552 cells. The subsequent 256 split points are unrefined, leaving
101,760 cells. The pinned source and event arithmetic are documented in
`reports/openfoam-amr-source-budget-audit-2026-09-28.md`. This observed case is
consistent with approximate maxCells semantics and does not establish a defect.

On those exact final meshes, fixed-mesh runs initialized from the analytic
high-gradient field reduced the volume-weighted velocity error from 37.01% to
1.878% (cap5000 mesh) and from 40.11% to 0.483% (cap100000 mesh). The AMR-path
errors thus do not follow from the final cell locations alone. Adaptation
history, field remapping, flux correction, sensor updates and pressure
projection remain possible contributors; these controls do not isolate them
all. The per-case quality verdict remains UNCERTAIN, and no OpenFOAM defect
report is justified without a more specific reproducible component-level
violation. Raw logs and fields are retained locally for continued audit.

### Endpoint and time-history continuity diagnostic

As a post-processing-only discriminator, Foundation 13 `foamPostProcess
-func "div(phi)" -latestTime` was applied to both AMR cases and the two
same-mesh fixed controls. The volume-weighted endpoint RMS `div(phi)` divided
by `Urms/(2*pi)` is `1.27e-11` and `8.78e-12` for the AMR cases, versus
`6.20e-14` and `2.68e-14` for the fixed controls. The original solver logs also
contain 496–566 continuity records per case; maximum `sum local` is
`2.33e-15` to `2.96e-15`, with maximum absolute global imbalance below
`5.7e-22`. Thus the large AMR velocity errors are not accompanied by a large
endpoint discrete mass-flux divergence or by large reported time-step
continuity errors. This narrows the mechanism search toward momentum/field
transfer, flux mapping not captured by these aggregate continuity metrics, or
other AMR history effects; it does not rule out transient local errors or
identify any one cause. The post-processing-only artifact is
`evidence/of13-high-gradient-amr-flux-balance-2026-09-30.json` and can be
regenerated with `uv run --with-requirements requirements-verification.txt
python -m tools.analyze_amr_flux_balance` after the raw `work/` trees are
available.
