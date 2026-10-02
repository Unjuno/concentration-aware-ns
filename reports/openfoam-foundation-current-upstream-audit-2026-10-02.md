# OpenFOAM Foundation current-version and reporting-path audit — 2026-10-02

## Current upstream state

The Foundation's current release is v14, released on 14 July 2026; the official
site also lists v14 patch-release news dated 25 July. The current public
`OpenFOAM/OpenFOAM-14` `master` was at
`162fa7a2e51e9c9a86c3000efdd885907f7d1acc` on 30 September 2026. GitHub's
license API returns `NOASSERTION`; the pinned repository `COPYING` and
Foundation-authored `README.org` identify GPL version 3 or later.

The current v14 repository's only open issue observed through GitHub's issue
API is #3, a crash in the `circuitBoardCooling` tutorial. The two other open
records returned by that endpoint are pull requests about ParaView library
path quoting and VTK include directories. None concerns the benchmark's
static, single-phase `incompressibleFluid` path or AMR behavior.

The Foundation's contribution page says the effective development line is
`OpenFOAM-dev`, suggests starting with the issue tracker, and asks for
convenient reproducible cases, responsive follow-up, and tests. It requires a
Contributor Agreement for significant fixes or new developments, and links
separate code-quality and style guides.

The Foundation tracker is separate from GitHub and must not be confused with
the OpenCFD GitLab project. The all-issues URL redirected to its login page
(HTTP 302, then 200 for the login form) in this environment. Direct issue
pages likewise returned HTTP 403 to the browser fetcher. A targeted public-index
search did surface relevant historical records: #4178 (PIMPLE controls,
resolved), #3928 (dynamic-refinement history, resolved), #4378 (a June 2026
parallel zone-generation crash, resolved by a commit), and #4282 (a
propeller-disk model scope question, closed as a development request). These
records do not establish a present defect in this benchmark's fixed-mesh,
single-phase forced-flow path; #4378 concerns a different parallel zone-set
path, while #4282 explicitly concerned an unsupported model use. Because the
individual records and full listing could not be fetched directly, this is a
targeted indexed search, not an exhaustive live tracker review. The exact
search scope and records are captured in the machine-readable audit below.

## Benchmark coverage and disposition

The benchmark's full six-case matrix remains Foundation 13. A pinned Foundation
14 package (`20260724`) completed one `n=64`, `dt=0.001` compatibility probe.
Its endpoint fields, after normalizing only the OpenFOAM version banner, and
the five stored diagnostics exactly matched the corresponding Foundation 13
case. This is useful cross-version compatibility evidence for one static
execution path. It is not a v14 resolution/time-step matrix, an AMR audit, or a
continuous-extrema certificate. The relevant report and frozen comparison are
[`openfoam-foundation14-compatibility-probe-2026-10-02.md`](openfoam-foundation14-compatibility-probe-2026-10-02.md)
and [`v13-v14-comparison.json`](../evidence/of14-high-gradient-v1/v13-v14-comparison.json).

The Foundation 13 approximate `maxCells` behavior remains explained by the
pinned selection algorithm and has not been shown to violate its documented
contract. No new defect was reproduced, so no issue or patch was filed. The
conclusion is **no report warranted on present evidence**, with the explicit
limitation that Foundation's Mantis tracker listing could not be searched
without login. Do not describe this as an exhaustive tracker clearance or
promote the one-case v14 match into a version-wide solver conclusion.

The machine-readable API, source, release, tracker-access, and scope record is
[`openfoam-foundation-current-2026-10-02.json`](../evidence/upstream-refresh/openfoam-foundation-current-2026-10-02.json).
