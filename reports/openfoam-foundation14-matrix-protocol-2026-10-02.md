# Foundation 14 high-gradient matrix protocol

This is a frozen successor to the Foundation 13 high-gradient v2 study. It
uses the same manufactured velocity field, forcing, endpoint, spatial and
temporal matrix, and numerical acceptance thresholds. The only deliberate
change is the solver release: Foundation package `20260724` for Linux/arm64,
identified by the runtime image digest in
[`protocols/high-gradient-of14-v1.json`](../protocols/high-gradient-of14-v1.json).

The matrix has six rows. The already completed `n=64`, `dt=0.001` probe is
reused with its original archive hash; the remaining five rows are run in
series by `tools.run_openfoam_foundation14_matrix`. The runner records source,
protocol, Docker client/context, image ID, platform, case commands, inputs,
logs, diagnostics, and archive hashes. It refuses to overwrite run or evidence
directories and preserves a timed-out case's inputs and partial output. Large
gzip archives are split into independently hashed 80 MB pieces for hosting
limits and can be reconstructed byte for byte.

The comparison reports case-level standard acceptance and sampled local
quality separately. Agreement with Foundation 13 is descriptive, not a
correctness oracle; disagreement would require independent analysis of the
reference, discretization, runtime package, and exercised code path before any
software-defect claim. Center-sampled derivative peaks do not certify
continuous extrema. This matrix cannot establish a singularity, molecular
alignment, a phase transition, or a change in material viscosity.

The protocol and runner were committed before any new v14 matrix run. The
existing compatibility case predates this matrix, remains identified as such,
and is not represented as a prospective rerun.

The first n128 run was stopped after 13 of 50 time steps when comparison with
the preserved Foundation 13 n128 log showed that this grid can require roughly
93 minutes; the initial 40-minute timeout was therefore inadequate. Its inputs,
partial log, outputs, and nonzero exit record are preserved as an incomplete
attempt. The resume path reuses only cases that pass a strict completion check,
preserves incomplete attempts, and reruns an incomplete grid from clean inputs
under a four-hour per-case cap. This correction changes run control, not the
frozen numerical protocol or acceptance thresholds.

The first resume exposed a bug in the new completion check: it counted every
occurrence of `Time =` rather than only OpenFOAM's time-step header lines. It
therefore replayed the already complete n16 and n32 cases before rejecting the
reused n64 archive. Those original attempts remain preserved. The checker now
counts anchored `^Time =` lines and reclassifies preserved runs using the full
step, convergence, end-marker, exit-code, and endpoint-field checks. Their
diagnostic and input hashes will be compared against the replay before the
matrix result is interpreted.
