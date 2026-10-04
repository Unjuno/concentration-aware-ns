# Independent replay of the Foundation 13 AMR mean-quality matrix

The four AMR runs in
`evidence/of13-amr-mean-quality-v1/` were reanalyzed from their published raw
release archives. The source tree was reconstructed from frozen harness commit
`3566f89058071910a41bb68010eb258c7bbc3d74`, rather than current HEAD, because
the current `tools/openfoam_case.py` has since changed. Raw archive assets were
downloaded from release `of13-amr-mean-quality-v1-3566f89`; each GitHub asset
digest matched its recorded SHA-256. The pinned analyzer verified each
archive-level hash and every archived member, checked the recorded source and
protocol identities, and replayed all three captured stages for each case.

Each regenerated analysis exactly matches its previously saved same-host
macOS analysis object. Running the frozen matrix aggregator also exactly
reproduced `evidence/of13-amr-mean-quality-v1/matrix.json`:

- all four standard acceptance gates pass;
- the n16 capture-disabled U/p control is byte-identical;
- both fixed-dt fine cases have adequate independent gradient/curl reference
  operators at every stage;
- the postSolve mean-quality gate fails for n32 and n64, so the matrix verdict
  is `REPRODUCED_SPECIFIED_MEAN_GATE_DISCREPANCY`.

This is a verified, preregistered mean-error discrepancy for the specified N=3
AMR experiment. It is not evidence of a Foundation implementation-contract
violation: at n64 the mean gradient and curl limits pass, the measured errors
improve from n32 to n64, and the analytic P0 decomposition shows exact
parent-value injection exchanges representation error for cell-mean mismatch
without a corresponding jump in total continuum velocity error. The separate
N=4 AMR peak/spectrum gate remains `UNCERTAIN`, and source equivalence of the
whole packaged binary is not established.

Receipt: `evidence/tests/openfoam-amr-mean-quality-replay-2026-10-04-b996015.json`.
Cross-platform floating differences and the strict regenerated-input byte
identity failure remain explicitly preserved in each case's existing replay
records; this replay does not erase or relabel them. No new upstream defect
report is warranted by the result.
