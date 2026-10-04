# Three-project scope refresh — 2026-10-04

> Correction (2026-10-04): the original localized source-lag receipt used an unrelated high-gradient reference family. Its numerical force mismatch is inapplicable to SU2 study-v1. Original archives and other SU2 diagnostics are unchanged. See `reports/su2-source-lag-reference-correction-2026-10-04.md` and additive v2 evidence.


The current OpenFOAM particle work is source-linked conditional algebra, not
an executed particle cloud or a replacement for the frozen field benchmark.
The source-linked body-force counterexample prevents transferring the
zero-force contraction to arbitrary force. Neither that result nor the
empirical threshold jump establishes a solver defect, molecular alignment,
viscosity reduction or a physical phase transition. No upstream post is made.
The new particle branch/body-force CI steps are prepared locally; hosted
execution has not happened. Existing run 37157306920 at a611973 remains queued.

For SU2, reanalysis on c772574 verifies all three saved archive digests before
computing the old-time versus target-time manufactured-force mismatch.
Results exactly equal the previous receipt; successive dt-halving orders are
1.0003607125390805 and 1.000180344999887. This is sampled analytic forcing
mismatch, not the measured PDE endpoint-error contribution. Failed inner
solves, spatial error and nonlinear response remain separate. The successful
one-step CFL=100 control does not resolve full-horizon convergence. PR #2857
is closed and unmerged at the fresh REST observation; no new issue is posted.

PhysicsNeMo issue #2007 is open and PR #2008 is open/unmerged, with head
7407608723062dc11ba5332e9ff3774f42bb02d9. The reported merge_commit_sha is a
GitHub prospective merge value and is not evidence of integration. The known
spectrum discrepancy remains assigned to those existing records. Their
status does not certify the full framework or the benchmark's continuous
peaks. No duplicate issue or request to maintainers is sent.

Fresh no-cache metadata, hashes, timestamps and SU2 replay output are in
`evidence/three-project-refresh-2026-10-04-drag`. This refresh revalidates the
listed metadata and source-lag calculation only; it does not refresh every
upstream source/issue or run any new solver. The broader objective remains
active, including global reconstruction bounds, unresolved proof identities,
full consumer trajectories, project-specific continuous quality requirements
and justified public integration.

## Live tracker and source refresh, 2026-10-04 01:29 UTC

A read-only GitHub API refresh confirms OpenFOAM Foundation 13 `master` remains
at `18870c24d21c6b982e2cdec27b2f59738cca5f90`; its repository license field
is `NOASSERTION`, while the previously inspected source headers identify
GPL-3.0-or-later. Adjacent Issue #2 remains open and concerns a two-phase
version difference, not the reproduced AMR case. The Foundation README's
separate bug-tracker requirement still bounds this GitHub-only duplicate check.

SU2 `master` remains at `bc15466602a687d6fb796d5df7a12ce3fde0949a`; its
repository license field is `NOASSERTION`. Issues #2353 and #2932 remain open,
and PR #2857 remains closed/unmerged. GraphQL confirms Discussion #2890 is
unanswered and has one top-level comment by `sbryngelson` plus one nested reply
by `Unjuno` (posted September 26 and updated September 30); no later reply or
accepted answer is present. The BDF2 report is our reply to the existing
thread, not maintainer acceptance of a general fix.

PhysicsNeMo `main` remains at `b45a5c810c741e6b41f8515be24c51121f8fc21f`;
the API declares Apache-2.0 and the audited `power_spectrum.py` blob remains
`fb3e8cda3bc7916b8e56833dda240cb74463fabb`. Issue #2007 and PR #2008 remain
open, with the PR unmerged. The existing records cover the known odd-width
behavior; no duplicate issue was filed. The complete targeted API/GraphQL
responses, query scope and normalized hashes are in
[`three-project-live-status-2026-10-04T0129Z.json`](../evidence/upstream-refresh/three-project-live-status-2026-10-04T0129Z.json).
This is a focused tracker refresh, not a full source or issue-history audit.

## Live API refresh — 2026-10-04 21:08 UTC

A new no-cache REST/GraphQL snapshot is preserved at
[`three-project-live-status-2026-10-04T2107Z.json`](../evidence/upstream-refresh/three-project-live-status-2026-10-04T2107Z.json).
The OpenFOAM Foundation 13/14, SU2, PhysicsNeMo and OpenAI formalization
default-branch SHAs match the October 4 inventory. OpenFOAM-13 issue #2 remains
open and unrelated to the uniform MMS finding. SU2 issues #2353/#2932 remain
open; PR #2857 remains closed; discussion #2890 remains unanswered with the
same September 13 maintainer reply. PhysicsNeMo #2007 and PR #2008 remain open;
the PR is still `behind` base. The OpenAI Lean repository remains unchanged
with issues disabled. This supports no new upstream report or duplicate. The
snapshot also records the live SU2 matrix and Lean-audit workflow states; both
were still in progress at capture time. This is a focused tracker refresh, not
a re-audit of all upstream source or issue history.
