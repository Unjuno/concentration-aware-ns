# Three-project scope refresh — 2026-10-04

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
