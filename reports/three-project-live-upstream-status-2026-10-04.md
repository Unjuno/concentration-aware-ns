# Three-project upstream status refresh

Checked the live GitHub API on 2026-10-04 at 05:43 UTC. OpenAI's
`NavierStokesAndEuler` still points to main commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; repository issue tracking is
disabled, and the pull-request listing endpoint returns 404. NVIDIA
PhysicsNeMo remains at `b45a5c8`; Issue #2007 and unmerged PR #2008 remain the
existing channel for the reproduced odd-width spectrum defect. SU2 remains at
`bc154666`; Issues #2353 and #2932 remain open for time-source semantics and
maximum-residual location reporting. The raw metadata and selected object
states, including repository license metadata, are preserved in
[`three-project-live-status-2026-10-04T0543Z.json`](../evidence/upstream-refresh/three-project-live-status-2026-10-04T0543Z.json).

This refresh found no state change that justifies a duplicate issue or PR. The
metadata check supplements the prior source-level audits; it is not itself
evidence that a numerical defect exists or has been fixed.
