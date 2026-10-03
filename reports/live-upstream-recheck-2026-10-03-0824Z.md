# Cross-project live recheck — 2026-10-03 08:24 UTC

Read-only GitHub/API review of the pinned mathematical source and three solver
targets. Exact head hashes, version tags, license-file blobs, issue/PR states,
and dispositions are preserved in
[`live-upstream-recheck-2026-10-03T082416Z.json`](../evidence/upstream-refresh/live-upstream-recheck-2026-10-03T082416Z.json).

OpenAI's main remains the audited `f9e8bc5`; the Apache-2.0 repository has
Issues and Discussions disabled. The actual-profile pressure obligation
remains a local extension gap, so there is no upstream finding to post.

OpenFOAM Foundation 13 remains the benchmark target. Its GitHub repository's
version-13 tag and current master head are recorded separately; GitHub's
license API reports `NOASSERTION`, while `COPYING` declares GPL-3.0-or-later.
The current GitHub tracker has four open issues. Issue [#2](https://github.com/OpenFOAM/OpenFOAM-13/issues/2)
is the relevant adjacent report: an attached two-phase squeeze-flow example
reports a change in stress-flux behavior at viscosity/gradient jumps. The
linked [source change](https://github.com/OpenFOAM/OpenFOAM-13/commit/6592798ca0704aa6eaaaaf74ea3cc6a9553317dc)
states its goal as consistency among surface-stress, momentum-matrix and
force/shear consumers. This case is outside our smooth single-phase,
constant-viscosity MMS; it was not rerun, and no duplicate was filed. The
separate Foundation Mantis tracker was not exhaustively searchable.

SU2 remains pinned to v8.5.0. Discussion [#2890](https://github.com/su2code/SU2/discussions/2890)
is closed without an accepted answer; issue [#2353](https://github.com/su2code/SU2/issues/2353)
remains open and carries the time-level observations. The broad target-time
PR [#2857](https://github.com/su2code/SU2/pull/2857) is now closed unmerged,
so there is no merged general fix to treat as current behavior. Issue
[#2932](https://github.com/su2code/SU2/issues/2932) separately tracks
maximum-residual-location output. These existing records make a duplicate
post inappropriate.

PhysicsNeMo main advanced to `b45a5c8` after the October 2 snapshot, while
the affected odd-width `power_spectrum.py` blob remains unchanged. Issue
[#2007](https://github.com/NVIDIA/physicsnemo/issues/2007) remains open and
PR [#2008](https://github.com/NVIDIA/physicsnemo/pull/2008) remains open and
review-required; current main is fourteen commits ahead of its head and the
PR has two unique commits. Its contribution guide asks contributors to begin
with an issue/discussion and coordinate with maintainers. The benchmark uses
even widths, so this known issue has no demonstrated effect on current
results. No duplicate was filed.

The new analytic note
[`openfoam-stress-interpolation-covariance-2026-10-03.md`](openfoam-stress-interpolation-covariance-2026-10-03.md)
derives a generic interpolation identity relevant to Issue #2. It provides a
discrete numerical confounder for viscosity-jump calculations, not evidence
that physical viscosity collapses or that molecules align.
