# SU2 n16 repeat across two image builds — 2026-10-05

## Result

The n16 case from hosted matrix run [37230949147](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37230949147) independently replays from its downloaded artifact. It reproduces the previously archived n16 case from run 37190363204 across two separately built Docker images. The case archive hashes differ, but all ten archive member paths are identical: seven members are byte-identical, and the only three changed members contain run metadata. The image ID is the only difference in `parameters.json` and `diagnostics.json`; the only command difference is the ephemeral runner bind-mount path. After normalizing those fields, the diagnostics and command compare equal.

Both cases used the same frozen protocol SHA-256
`dacd7638a306a810c986ce8d5922f16e55a76698b67d97f7ff892b7f6c9b60aa`, ran
50 updates to solution time 0.05, and report source/history time 0.049. The
five numerical quality errors match exactly: velocity L2 0.0061802, energy
0.0066102, sampled gradient peak 0.3609476, sampled vorticity peak 0.3403403,
and shell-spectrum L1 0.0066358. Both summaries say the solver exited zero,
but the standard acceptance and sampled local-quality verdicts are both
`FAIL`.

## Evidence and limits

The complete downloaded case export, compressed case archive, protocol, patch,
run summary, image ID, build log, and replay receipt are preserved in
[`evidence`](../evidence/su2-shared-high-gradient-v1-run-37230949147/README.md).
The independent replayer was run against that preserved directory with locked
Python 3.12 dependencies; its output is byte-identical to the saved replay
receipt, and all 17 recorded file hashes verify. The artifact's original
GitHub ZIP digest and expiration time are also recorded in
`verification.json`.

This repeat supports numerical reproducibility for this one n16 input across
two build artifacts. It does not complete the five-case matrix, establish
spatial or temporal convergence, show a standard-pass/local-fail blind spot,
validate the source-to-binary chain independently, certify continuous
extrema, or identify an SU2 defect. The remaining four cases in run 37230949147
and the Lean proof audit were still active when this report was prepared; they
must be polled before considering those gates complete.
