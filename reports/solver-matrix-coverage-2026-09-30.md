# Cross-solver matrix coverage and verdicts

This inventory distinguishes completed runs from acceptance and hypothesis
verdicts. Hash checks and diagnostic replays establish artifact consistency;
they do not independently validate a solver or turn finite samples into
continuous error bounds.

The historical base OpenFOAM run manifest still labels the two later temporal
rows incomplete. The `manifest-current-2026-09-30.json` cross-run index plus
the per-row temporal manifests and raw archive checksums supersede that status
for matrix coverage, without rewriting the original frozen base record.

| Target and pinned scope | Spatial matrix | Time-related matrix | Matrix result and limits |
|---|---|---|---|
| OpenFOAM Foundation 13 package in arm64 image `sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`, GPL-3.0-or-later source headers. Harness commits: `0e0288f98209f856931352ebfa5dad0f1aad0014` (uniform) and `265611cd160a7e139b6950c918e6dc1d90056d97` (AMR) | Uniform `n=16,32,64,128`, all at `dt=0.001` | At `n=64`, `dt=0.001,0.0005,0.00025`; common endpoint `t=0.05` | Six uniform cases complete. Standard and local gates pass at n=64 and 128; n=16 and 32 pass standard but fail local quality. The predeclared persistent-blind-spot criterion is `NOT_OBSERVED`, not “all resolutions accurate.” The temporal triplet passes both gates but exact velocity error stays nearly flat, so asymptotic time convergence is not certified. Foundation binary/source equivalence was not independently established. |
| SU2 v8.5.0, source `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`, LGPL-2.1-or-later; arm64 image | `n=16,32,64`, all at `dt=0.001` | At `n=64`, `dt=0.001,0.0005,0.00025`; endpoint `t=0.05` | Five cases complete and diagnostics replay exactly from raw archives. No case satisfies the observed conjunction of velocity, energy and all-step residual checks: n=16/32 exceed aggregate thresholds and n=32/64 have steps that miss the frozen inner-residual threshold. The temporal field-difference order is about 0.999, but 2–7 steps per run miss residual thresholds; no temporal error certificate or local-quality PASS is assigned. |
| NVIDIA PhysicsNeMo v2.2.1, source `1b961314e42a0625502ba1592d25f706f1e02a24`, Apache-2.0; CPU float64, Torch 2.11.0 | `n=16,32,64` collocation densities | `time_nodes=5,9,17` at `n=64`; these are collocation nodes, **not time steps** | Original five seed-709 runs plus 20 preregistered runs across four additional seeds complete; five seeds per case, all with 5,000 optimizer steps. Per-case variability and paired contrasts are archived in `evidence/physicsnemo-seed-control-v1/analysis.json`. Spatial contrasts have mixed signs; temporal-node contrasts lower sampled velocity error in all five seeds, but magnitudes are small and descriptive. All acceptance verdicts remain `UNCERTAIN`: no PhysicsNeMo-specific threshold was preregistered, continuous extrema are not bounded, the architecture does not enforce incompressibility exactly, and this fixed budget does not establish optimizer convergence. AMR is not applicable to this fixed-architecture PINN study. |

## OpenFOAM AMR upper-state evidence

The AMR integration pilot used the n=16 case, `maxRefinement=2`, and nominal
cell budgets 4,096, 5,000 and 100,000. All three runs completed 50 converged
steps. The 4,096 budget permitted no refinement. The 5,000 case ended with
16,640 cells (level 1); the 100,000 case ended with 101,760 cells (level 2),
so the configured cap is not a strict final-cell upper bound in these batch
adaptation outcomes. Blocked-candidate counts were not observed. This matches
an approximate budget/synchronization behavior in the inspected AMR source
path; it is not evidence of an unexpected implementation defect.

The adaptive final fields have relative volume-velocity errors of 37.0% and
40.1% for the two refined cases, while fixed-final-mesh analytic-initialization
controls report 1.88% and 0.483% on the same respective meshes. This points to
an adaptive-history contribution, but the control does not isolate every
interpolation, flux-correction, projection or sensor-update effect. AMR local
quality remains `UNCERTAIN`; spectra on these nonuniform meshes are unavailable
because no reconstruction was validated. All five adaptive/remap raw archives
are now retained with byte and per-entry tree hashes; see
`evidence/tests/openfoam-amr-archive-integrity-2026-09-30.json`.

## Upstream disposition

- **OpenFOAM:** no new issue filed. The localized MMS results do not isolate an
  implementation defect, and the AMR upper-budget behavior agrees with the
  documented source path. The public repository directs bug reports to its
  separate tracker; see `reports/openfoam-amr-source-budget-audit-2026-09-28.md`
  and `reports/upstream-disposition.md`.
- **SU2:** no duplicate report filed. The nonautonomous BDF source-time
  observation is already discussed in [SU2 discussion #2890](https://github.com/su2code/SU2/discussions/2890),
  with maintainer response and scoped follow-up. The benchmark's broad local
  quality verdict remains uncertain.
- **PhysicsNeMo:** no duplicate issue filed. Odd-width power-spectrum behavior
  is already tracked in [issue #2007](https://github.com/NVIDIA/physicsnemo/issues/2007)
  and [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008). Focused
  current-main reproduction confirms the tracked bug; it does not affect the
  benchmark's even-grid runs.

Re-run the targeted evidence checks from the repository root:

```sh
work/reference-check-env/bin/python -m tools.audit_high_gradient_time_sequence
work/reference-check-env/bin/python -m tools.replay_su2_diagnostics
work/reference-check-env/bin/python -m tools.compare_su2_time
work/reference-check-env/bin/python -m tools.review_su2_standard
work/reference-check-env/bin/python -m tools.verify_openfoam_amr_archives
work/reference-check-env/bin/python -m tools.audit_physicsnemo_local_fields
```

These commands replay records and postprocessing; they do not rerun all three
solver/training matrices. The per-target raw inputs, environments, gates and
runtime limitations remain in their linked protocol and evidence directories.
The current OpenFOAM cross-run manifest also binds the recorded arm64 image ID,
Foundation DEB, Dockerfile, build log, and installed-package inventory by hash.
The base image and DEB are pinned, but Ubuntu apt dependencies were not
snapshot-pinned and source-to-binary equivalence was not established. See the
[runtime reproduction guide](../runtime/openfoam13/README.md); replaying the
published archives does not require a solver rebuild.

## Fresh archive/postprocessing replay on 2026-10-01

Using `work/reference-check-env/bin/python`, the four original OpenFOAM
fixed-step archives again matched their frozen 50-step schedules and manifest
hashes. The five SU2 diagnostics again matched exactly when recomputed from the
saved fields and histories; the observed temporal order remained `0.99916`,
with no temporal error certificate because inner residual checks fail on some
steps. All five AMR/remap archives again passed byte and per-entry tree-hash
verification. The five PhysicsNeMo archive/checkpoint/evaluation links matched;
sampled derivative peak-magnitude errors remained `0.91–0.97%`, while the
maximum sampled derivative-field differences normalized by an exact sampled
peak were `1.20–1.26%`. These checks establish artifact and current
postprocessing consistency only. They do not rerun either solver, establish
source-to-binary equivalence, certify continuous extrema, or validate a
physical interpretation. The replay commands are listed above; the detailed
outputs remain in the existing JSON evidence records.

### OpenFOAM fixed-time-step matrix replay on 2026-10-01

The current cross-run manifest was re-read after an earlier status note relied
on the historical partial attempt. Its six completed cases were rechecked by
combining `tools.audit_high_gradient_time_sequence` (the four spatial rows,
including reconstruction and hash validation of the split n=128 archive) and
`tools.compare_high_gradient_temporal` (the n=64 temporal triplet, including
archive-to-source tree checks, exit records, complete PIMPLE counts, endpoint
fields, matching cell centers, and frozen non-time input hashes). All six
archives match their manifest digests. The two temporal addendum cases are
complete at 100/100 and 200/200 converged steps; the earlier 35/36 partial
attempt is preserved as a historical artifact and is not the source of those
rows. Their exact-velocity errors are 0.00478066, 0.00478409, and 0.00479049,
and the observed adjacent-field-difference order is about 0.499. Every temporal
row passes the configured standard and local gates, but the three-point trend
still gives no asymptotic temporal error certificate. This is a fresh replay of
archived evidence, not a solver rerun or a change to the matrix's
`NOT_OBSERVED` defect criterion.
