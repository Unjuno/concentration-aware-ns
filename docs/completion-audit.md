# Completion audit — interim, 2026-09-27

### Completion audit refresh — 2026-10-03 compatible-interface clean export

The tracked-only export of fixed commit
`b0e590e3c1b9b19044748fac7ad06109785f6fe5` passes all 46 report/evidence
replay steps, six follow-up checks and strict comparison of 234 unchanged
tracked report/test-evidence files in a fresh locked CPython 3.14.5 environment
on macOS 27.0.1 arm64. The fresh suite reports 233 passed, one skipped and
five subtests passed. Saved wrapper/test-log hashes and all 46 internal raw
replay log hashes match. The result and sanitized logs are in
[`clean-export-2026-10-03-success-b0e590e/`](../evidence/clean-export-2026-10-03-success-b0e590e/README.md).
Subsequent evidence/documentation commits are separate from this tested source
commit; hosted Python CI is recorded as its own PR check. No CFD solver or
Lean proof was rerun, and no scientific verdict is upgraded.

The PR description's earlier blanket OPEN candidate-statement claim is also
corrected to the October 2 source audit below: proposition definitions and
their proving modules are separate. The candidate and whole-space theorem
declarations compile at the pin, while our extension's actual-profile pressure
condition and independent mathematical/physical interpretation remain open.

### Completion audit refresh — 2026-10-03 compatible interface control

The new analytical trace-compatibility lemma narrows the independent-tensor
stress control: for continuous velocity with a common differentiable tangential
trace and divergence-free one-sided gradients, the interface jump of the
normal-contracted explicit transpose correction is zero. A compatible planar
Couette weak solution instead exercises the implicit diffusion coefficient.
The exact orthogonal FV resistance analysis and independent stiffness-matrix
tests show first-order arithmetic-interface flux error and exact harmonic
half-cell resistance for this aligned case. Seven further pinned-source files,
ten exact controls and five tests are recorded in
[`incompressible-interface-stress-compatibility-2026-10-03.md`](../reports/incompressible-interface-stress-compatibility-2026-10-03.md).
No packaged solver, VoF model, pressure coupling or upstream case was executed.
The fresh locked export at `a444a5f` passed 45 steps, six follow-up checks and
232 unchanged files, but predates this compatibility addition. The new full
replay passes all 46 steps, including 233 tests, one skip and five subtests;
its saved log and checker/source-manifest hashes match. A new tracked-only
export remains to be verified. No broad verdict is upgraded.

### Completion audit refresh — 2026-10-03 source-linked stress correction controls

The new pinned-source trace establishes the generic covariance model for the
explicit correction with common uncorrected linear weights. Captured source
identities match the local tree; binary equivalence remains unverified.
Mixed-weight/corrected and noncommuting neighbour-map controls make the
missing premises explicit. Exact conservative assembly shows that a synthetic
planar face mismatch can cancel globally while its local residual-density
norms grow under refinement. The prescribed product-constant tensor control
is not a compatible manufactured incompressible flow and does not compare
the complete stress or solution. Ten exact algebra controls and five targeted
tests pass. Full published-report replay passes all 45 steps, including 228
tests, one skip and five subtests. Fresh tracked-only export and hosted checks
remain separate validation stages.
The details and source links are in
[`openfoam-stress-operator-source-link-2026-10-03.md`](../reports/openfoam-stress-operator-source-link-2026-10-03.md).
No CFD, AMR-quality, upstream-defect or particle-scale verdict is upgraded.

### Completion audit refresh — 2026-10-03 clean export at viscosity-jump audit head

Exported fixed commit `0526de204d4cab95a432db254c148bdb1773c0bc` from tracked
Git content into a fresh locked CPython 3.14.5 environment on macOS 27.0.1
arm64. All 44 report/evidence replay steps and six follow-up checks exited
zero; all 230 compared tracked files remained byte-identical. The sanitized
manifest and logs are preserved at
[`clean-export-2026-10-03-success-0526de2/`](../evidence/clean-export-2026-10-03-success-0526de2/README.md).
Hosted Python CI passed for branch head
`e5d78a4b1c9bcd129b75578bf0e443c843c6866e` in run `37110793834`. This verifies
the tracked Python postprocessing/evidence path for the recorded host and
commit; it does not rerun OpenFOAM, SU2, PhysicsNeMo, or Lean and does not
upgrade any scientific verdict.

### Completion audit refresh — 2026-10-03 stress-interpolation checker replay

Added the symbolic face-interpolation identity as a report-replay step and ran
the complete replay from the locked verification environment. All 44 steps
exited zero, including 223 tests, one skip and five subtests. The replay also
refreshed existing report/test metadata for the current macOS 27.0.1 host. This
is an exact generic algebra control, not an OpenFOAM operator reproduction or
a run of the issue #2 case. A tracked-only clean export and CI at the next
commit are still required. The finding remains a distinct, unconfirmed
interface-discretization question; benchmark and physical verdicts are
unchanged.

### Completion audit refresh — 2026-10-03 cross-project issue and viscosity-jump analysis

Read-only live checks confirm the OpenAI source pin is unchanged, SU2 target-time
PR #2857 is closed unmerged while its issue/discussion records remain available,
and PhysicsNeMo main advanced without changing the affected odd-width spectrum
file. The Foundation 13 GitHub tracker contains an existing open issue #2 with
a two-phase, high-viscosity-contrast stress-flux reproducer. Do not merge that
with the smooth single-phase MMS or the proposed physical-viscosity hypothesis.
The current source/disposition snapshot is
[`live-upstream-recheck-2026-10-03-0824Z.md`](../reports/live-upstream-recheck-2026-10-03-0824Z.md).

For the generic model of two factors interpolated with the same linear face
weights, the exact checker proves
`I_w(aG)-I_w(a)I_w(G)=w(1-w)(a_P-a_N)(G_P-G_N)`. It is quadratic in cell
spacing for smooth affine data and can remain finite across unresolved jumps.
This gives a discrete numerical confounder for interface-viscosity cases, not
a verdict on the full OpenFOAM operator, the attached issue case, the current
benchmark, or physical viscosity. No duplicate upstream report was made. The
derivation, exact scope and limits are recorded in
[`openfoam-stress-interpolation-covariance-2026-10-03.md`](../reports/openfoam-stress-interpolation-covariance-2026-10-03.md)
and its replayable symbolic result.

### Completion audit refresh — 2026-10-03 clean export at current head

Fixed commit `48579a4e70176c1166f33a75b2ef803b2714e30a` was exported from
tracked Git content and replayed with locked dependencies in a fresh
CPython 3.14.5 environment on macOS 27.0.1 arm64. All 43 report/evidence
replay steps and six follow-up checks exited zero; all 227 compared tracked
files remained byte-identical. GitHub Actions passed for the same commit.
The result and sanitized logs are preserved at
[`clean-export-2026-10-03-success-48579a4/`](../evidence/clean-export-2026-10-03-success-48579a4/README.md).
This verifies the tracked Python postprocessing/evidence path for this
fixed commit and host; no CFD solver, training run, or Lean proof was rerun,
and no scientific or benchmark-quality verdict is upgraded.

### Completion audit refresh — 2026-10-03 OS provenance drift

A fresh locked export of fixed head `1160042e53d2db0a372f6a7a60bec9570784bd06`
completed all 43 report replay steps and six follow-up checks. Strict byte
comparison found seven files changed: two test-evidence files differed only
in the recorded platform string after the host upgraded from macOS 26.6.2 to
27.0.1, and five SU2 report hashes changed because the regenerated diagnostic
replay records that host metadata. No numerical fields or verdicts changed.
The attempt is preserved at
[`clean-export-2026-10-03-current-head-1160042-os-drift/`](../evidence/clean-export-2026-10-03-current-head-1160042-os-drift/README.md).
Refreshed those runtime-provenance records and dependent report hashes for
the current host. A new fixed-commit clean export is still required; this
metadata refresh is not solver validation or a scientific-verdict change.

### Completion audit refresh — 2026-10-03 clean-export metadata comparison

The corrected exporter at `a6e2ce5` completed the 42-step report replay and
all six follow-up checks. Its final tracked-only comparison still returned
`success: false` because exactly two generated test-evidence JSON files changed
only in runtime metadata: a host-specific interpreter path and Python/platform
metadata from 3.14.5 versus the evidence's 3.12.10. The separate replay steps
all returned zero; this is not a successful clean-export verification because
the unchanged-artifact gate is part of that claim. Preserved the run at
[`clean-export-2026-10-03-metadata-diff/`](../evidence/clean-export-2026-10-03-metadata-diff/README.md).
Removed the absolute interpreter path from the force-scaling evidence and now
record only the implementation name. A fresh export under the recorded Python
3.12.10 is required to establish exact reproducibility.

### Completion audit refresh — 2026-10-03 clean-export runner diagnosis

The first new tracked-only export at commit
`2d3983d1a563a2aae368348618a69cca46e2e8b6` failed at report-replay step 1:
the venv install passed, but a nested test subprocess resolved the host
`python` and reported `No module named pytest`. The replay runner intentionally
uses PATH lookup for child commands; `tools/check_clean_export.py` had not put
its fresh venv on that PATH. This is our clean-export environment-propagation
defect, not a solver finding or scientific verdict. Preserved the sanitized
failure record and raw log hashes in
[`clean-export-2026-10-03-path-failure/`](../evidence/clean-export-2026-10-03-path-failure/README.md).
Added a regression test that failed before the fix and passed after it; the
full current-checkout suite passed 222 tests, one skipped, five subtests. The
exporter now places the venv scripts directory first for all post-install
subprocesses. A fresh locked tracked-only export from the corrected commit is
still required; the previous failure must not be represented as a successful
replay.

### Completion audit refresh — 2026-10-03 full-sphere rotational diffusion

Extended the conditional Jeffery director analysis from its local tangent
plane to a probability density on `S^2`, using the standard rigid-spheroid
orientation law and rotational Smoluchowski diffusion. This is a prescribed
finite-director model, not a particle-scale transfer theorem for the OpenAI
field. In logarithmic time `s=log(tau0/tau)` and strain
`gamma=C/(2*tau)`, the checker verifies
`partial_s rho=-div_S(b rho)+D0*tau0^(1-delta)*exp((delta-1)s)*Delta_S rho`,
`b=(3*kappa*C/2)*(p_z*e_z-p_z^2*p)`, and
`div_S b=(3*kappa*C/2)*(1-3*p_z^2)`. At `delta=1`, the unique stationary
density is proportional to `exp(chi*p_z^2)`, with a finite, explicit
two-pole-cone probability. At `delta>1`, an energy estimate using the
sphere's mean-zero Poincare gap yields `Y' <= -lambda*d(s)*Y+K/d(s)`, hence
convergence to isotropy for normalized `L2` initial densities. This corrects
the interpretation of the earlier tangent-plane variance divergence: it
signals loss of the local approximation, not unbounded orientation variance.
For `delta<1`, finite integrated diffusivity makes the sample path an
asymptotic pseudotrajectory of the deterministic Jeffery flow. The strict
Lyapunov function narrows its limit set to the equator or one pole, but does
not exclude convergence to the unstable equator; almost-sure alignment is
still unproved. This uses the Benaïm–Hirsch asymptotic-pseudotrajectory and
strict-Lyapunov framework after checking the finite-quadratic-variation
condition for this SDE. Exact symbolic identities passed with SymPy 1.14.0;
the focused rotational-diffusion tests passed 3/3. The complete Python 3.14.5
report replay passed 42/42 and the full suite reported 220 passed, one skipped,
five subtests. All replay log hashes match the summary. See
[`full-sphere-rotational-diffusion.md`](full-sphere-rotational-diffusion.md),
[`spherical-orientation-diffusion-2026-10-03.json`](../evidence/tests/spherical-orientation-diffusion-2026-10-03.json),
and [`report-replay/summary.json`](../evidence/report-replay/summary.json).
Primary framework sources are Jeffery (1922),
[DOI 10.1098/rspa.1922.0078](https://doi.org/10.1098/rspa.1922.0078), and
Hinch–Leal (1972), [DOI 10.1017/S002211207200271X](https://doi.org/10.1017/S002211207200271X);
the singular-time limit and energy estimate here are our own conditional
derivations, not claims from those sources. The APT/strict-Lyapunov framework
follows Benaïm and Hirsch (1996),
[DOI 10.1007/BF02218617](https://doi.org/10.1007/BF02218617), and Benaïm
(1999), [paper](https://www.numdam.org/item/SPS_1999__33__1_0.pdf); the
SDE-specific finite-noise estimate is checked here. Benaïm's Theorem 9.1
(1999, §9, pp. 49–50) is for discrete Robbins–Monro processes and does not
directly establish equator-avoidance for this continuous-time SDE. No molecular diffusion law,
particle-position determinism, phase transition, viscosity change, or solver
acceptance result follows. No upstream report was warranted.

### Completion audit refresh — 2026-10-03 scalar equatorial reduction

Projected the sphere Itô equation onto `x=p_z` to obtain
`dx=[(a-2d(s))*x-a*x^3]ds+sqrt(2*d(s)*(1-x^2))*dW_s`, with the poles
absorbing. A SymPy checker verifies the spherical Laplacian drift correction,
noise variance, and decomposition identities. The linearization around the
equator has a nondegenerate Gaussian integrating-factor amplitude, but its
no-atom conclusion is not transferred to the nonlinear state-dependent SDE.
The exact checker passes 13 identities; focused tests pass 4/4; the complete
locked replay passes 42/42 and all log hashes match. The suite reports 221
passed, one skipped, five subtests. The same four focused tests and 13 exact
identities pass under Python 3.12.10; the command and hashes are in
[`spherical-orientation-diffusion-py312-2026-10-03.json`](../evidence/tests/spherical-orientation-diffusion-py312-2026-10-03.json).
This is not a full-suite or hosted-CI result. This remains an ideal orientation model;
almost-sure alignment and all molecular/viscosity implications remain open.
See [`full-sphere-rotational-diffusion.md`](full-sphere-rotational-diffusion.md)
and [`spherical-orientation-diffusion-2026-10-03.json`](../evidence/tests/spherical-orientation-diffusion-2026-10-03.json).

### Correction — 2026-10-03 pole behavior and subcritical equator argument

The prior paragraph incorrectly called `x=+/-1` absorbing; the exact scalar
Itô drift is `-2*d(s)` at `+1` and `+2*d(s)` at `-1`, pointing inward when
`d(s)>0`. Also derived the exact additive-noise coordinate
`theta=asin(x)`. Its drift derivative is `a*cos(2*theta)-d(s)/cos(theta)^2`,
which is uniformly positive in a fixed equatorial band at sufficiently late
deterministic times for `delta<1`. For each fixed future Brownian path, at
most one state at that time can converge to the equator; finite-time
ellipticity gives a nonatomic state law independent of future increments, so
equator convergence has probability zero. Together with the prior APT and
strict-Lyapunov classification, this conditionally gives a single-pole limit
for the ideal director. The argument uses standard endpoint nonattainment
and elliptic-smoothing facts; the symbolic checker verifies only algebra.
Four focused tests pass and the checker reports 16 exact identities. The
machine record is
[`spherical-orientation-diffusion-equator-avoidance-2026-10-03.json`](../evidence/tests/spherical-orientation-diffusion-equator-avoidance-2026-10-03.json).
This correction supersedes the preceding absorbing-pole and equator-gap
statements. It establishes no molecular or OpenAI-flow consequence.

### Completion audit refresh — 2026-10-03 analytic provenance recheck

Re-fetched `openai/NavierStokesAndEuler` main and confirmed commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, Apache-2.0 metadata, and disabled
GitHub issues. Re-read the exact source path from
`PreparedOutgoing.PreparedProfile.amplitude_lower`, through nominal and
modulated assembly, to `FinalSlowBase.ProfileData` and its
`actualProfile := Classical.choice profileData_nonempty`. The strong outgoing
amplitude bound is retained on the prepared record and used to establish
downstream existential assemblies, but `ProfileData` does not carry it; the
actual selection therefore has only the source's ordinary profile-data
guarantees in this extension. Re-ran
`runtime/lean-verification/check_actual_profile_pressure_provenance.sh` in its
pinned checker environment. Its three theorem axiom reports are limited to
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. The selected
profile's threshold remains unproved; no counterexample or theorem failure
was found. This is a verification-provenance gap, not a demonstrated defect
in the upstream result. No simulation was run and no upstream post was made;
the issue tracker is disabled and the finding concerns our extension. Exact
source, script and output hashes are in
[`evidence/lean-verification/actual-profile-pressure-recheck-2026-10-03.json`](../evidence/lean-verification/actual-profile-pressure-recheck-2026-10-03.json).

At the same observation, PR #4 remained open at `b11c1450fd75474f9f5821b745ae630975164706`; its GitHub Actions `tests` check was still queued. No claim of hosted CI completion follows from the local Lean check.

### Completion audit refresh — 2026-10-02

The current-main PhysicsNeMo boundary-source follow-up confirms the low-level
finite-difference and spectral docstrings explicitly require periodic data,
which narrows the wording of existing issue #2001. The consumer-facing
`GradientsFiniteDifference`/`PhysicsInformer` docs still omit that precondition,
their tests crop the outer two cells, and no boundary-mode option is exposed.
An exact source-formula ramp check reproduces the expected periodic-wrap edge
derivative; PyTorch was unavailable, so no runtime reproduction is claimed.
Existing #2001/#1852/PR #1853 already cover the matter; no duplicate issue was
filed. The audited benchmark uses periodic autodiff and is unaffected. See the
[source-level qualification](../reports/physicsnemo-upstream-derivative-audit-2026-10-02.md#2026-10-02-source-level-qualification)
and [pinned evidence](../evidence/upstream-refresh/physicsnemo-boundary-source-check-2026-10-02.json).

The latest tracked head before this record, `5cb3d65c2b4c065df1cc21ed4ec68dde3b603d7b`,
was exported from Git's tracked tree with a fresh locked Python 3.14.5
environment. All 37 published report-replay steps and six additional checks
passed; all 189 compared report/test-evidence files were unchanged. The full
suite from the clean export reported 201 passed, 1 skipped, and 5 subtests
passed, with a separate full-suite rerun also passing. The sanitized record,
raw/published log hashes, archive and runner hashes, commands, and package
versions are in
[`evidence/clean-export-2026-10-02-current-head-5cb3d65/`](../evidence/clean-export-2026-10-02-current-head-5cb3d65/README.md).
A Python 3.12 first attempt produced seven environment-metadata/hash
differences; matching the recorded Python 3.14.5 environment eliminated all
of them. This is publication/replay validation, not a solver rerun or a
scientific verdict upgrade.

The separate Foundation 13 `n=64`, `dt=0.0005` rerun has 36 converged steps
through `t=0.018`; a later `t=0.0185` time label has no completed convergence
record. It has no `exit.json` or endpoint archive. Current Docker inspection
finds no container object, and no host solver process is present. Its sanitized
inputs, original input hashes and raw logs are preserved in
[`incomplete-rerun-2026-10-02/`](../evidence/of13-high-gradient-v2/incomplete-rerun-2026-10-02/README.md).
This repeat remains excluded from the completed matrix and all verdicts; the
same n=64/dt=.0005 matrix row had separately completed 100/100 steps and
passed both gates on September 30. The repeat is not a missing matrix row.

The OpenFOAM Foundation's current release is v14, with a September 30 source
update; the benchmark's complete six-case matrix remains pinned to v13. The one
v14 compatibility case matches v13 at n=64/dt=.001 after version-banner
normalization, but no v14 matrix or AMR run was performed. Foundation's current
GitHub issue/PR inventory contains no matching report; its separate Mantis
all-issues page redirects to login, so tracker-wide duplicate clearance is
still incomplete. See the
[current Foundation audit](../reports/openfoam-foundation-current-upstream-audit-2026-10-02.md).

The frozen OpenFOAM v2 six-case replay passes archive, protocol, endpoint,
standard-acceptance, and sampled-local-quality checks. Standard acceptance
passes all six cases; sampled local quality fails n=16 and n=32 and passes
n=64/n=128 and both n=64 temporal cases. Thus a standard-PASS/local-FAIL
disagreement is observed on the two coarse grids. The preregistered matrix
criterion specifically requires that disagreement on both adequately resolved
grids, n=64 and n=128; because both pass the local gate, that persistent
fine-grid criterion is `NOT_OBSERVED`. This does not erase the coarse-grid
disagreement. Replay uses stored archives and logs; it is not a new solver run
or a continuous-field certificate.
An October 2 repeat of n=64, dt=0.0005 reached 36/100 steps before its runner
stopped producing output. Preserve that attempt as incomplete and exclude its
partial data. The same protocol row had already completed 100/100 steps on
September 30, passed both gates, and is included in the six-case matrix; see
`evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005-manifest.json`.
The incomplete repeat does not create an additional missing matrix condition
or alter its verdict.

The SU2 v8.5.0 five-archive review likewise found no standard-PASS/local-FAIL
case: n=16 passes the all-step residual gate but fails accuracy; n=64 time
cases pass aggregate accuracy but miss 2, 3, and 7 residual steps. Related
time-boundary behavior is already tracked in issue #2353, and residual
location visibility in issue #2932. Discussion #2890 is closed without an
accepted answer, and the benchmark report is already posted there. No
duplicate upstream report was filed. See the
[current SU2 audit](../reports/su2-localized-residual-upstream-audit-2026-10-02.md).

The PhysicsNeMo path uses autodiff on a periodic domain, so the current
nonperiodic derivative-boundary issue/PR is not applicable to this benchmark.
The five-seed and local-peak evidence remains descriptive: sampled maxima do
not certify the full-domain continuous maximum, seed sensitivity remains, and
no preregistered acceptance threshold exists. No duplicate issue was filed.
See the
[current PhysicsNeMo audit](../reports/physicsnemo-upstream-derivative-audit-2026-10-02.md).

The current public head `28d417e` was exported from tracked Git data into a
fresh locked environment. All 37 replay steps and six additional checks
passed; all 182 compared report/test-evidence files remained unchanged, and
the suite reported 200 passed, one skipped, and five subtests passed. The
sanitized run record is in
[`evidence/clean-export-2026-10-02-current-head-28d417e/`](../evidence/clean-export-2026-10-02-current-head-28d417e/README.md).
This validates same-host postprocessing of tracked evidence, not solver
rebuilds or runs, PhysicsNeMo training, Lean execution, or scientific verdicts.

### Current tracked-only export — commit `2fb0681`, 2026-10-02

The latest branch head `2fb068172a25d980f9eb52b5a519e8666e35fe79` was
exported from tracked Git data into a fresh directory and locked Python 3.14.5
environment. The 37-step report replay and six additional checks passed; all
188 report/test-evidence files were byte-identical. The full suite then ran
from the exported source: 201 passed, one skipped, and five subtests passed.
Sanitized results and logs are in
[`evidence/clean-export-2026-10-02-current-head-2fb0681/`](../evidence/clean-export-2026-10-02-current-head-2fb0681/README.md).
This verifies tracked postprocessing and archived-data replay only; it does
not rebuild or rerun solvers, retrain PhysicsNeMo, execute Lean, or upgrade any
scientific verdict.

The project remains **incomplete**. Higher-resolution AMR quality,
continuous-field derivative certification, the unresolved actual-profile
pressure premise, end-to-end executable extraction, and live OpenFOAM tracker
coverage remain open. The user's molecular-alignment, phase-transition, and
constitutive-viscosity interpretations are not established by these results.

### Current tracked-only replay — 2026-10-02, commit 28aa3c2

Exported the exact tracked tree at `28aa3c2de78264d243598aaf9064918f7e3a8d1b`
into a fresh directory and locked Python 3.14.5 environment. All 38 published
report-replay steps and seven additional postprocessing checks exited zero;
196 tracked report/test-evidence files remained byte-identical. Sanitized
commands, package inventory, archive digest, and logs are published in
[`evidence/clean-export-2026-10-02-current-head-28aa3c2/`](../evidence/clean-export-2026-10-02-current-head-28aa3c2/README.md).
This validates Python replay of archived evidence on the recorded host. It
does not run the full pytest suite, rebuild or rerun a solver, retrain
PhysicsNeMo, execute Lean, certify continuous field errors, or upgrade a
scientific verdict. The separate Foundation issue-tracker search was bounded
and partly blocked by HTTP fetch restrictions; it found no matching AMR
quality report but does not close the live-tracker coverage gap.

### OpenFOAM AMR addendum — 2026-10-01

### Current tracked-only export — 2026-10-02

Source commit `84a3cc6e4bffad458466441201e3b45bcdd77fc6`, immediately before
publication of its evidence bundle, was exported from tracked Git data into a
fresh directory and locked virtual environment. The publication commit adds
documentation and the sanitized run record only. All 37 report-replay steps and six
additional checks passed, with 178 tracked report/test-evidence files unchanged.
The full suite from that exported tree reported 200 passed, one skipped, and
five subtests passed. Sanitized logs, hashes, package versions, and reproduction
commands are in
[`evidence/clean-export-2026-10-02-tracer-head/`](../evidence/clean-export-2026-10-02-tracer-head/README.md).
This checks same-host postprocessing and stored evidence only; it does not
rebuild or rerun solvers, retrain PhysicsNeMo, execute Lean, or change scientific
verdicts.

The first clean export at commit `46691344` exposed a real harness defect:
`openfoam_temporal_triplet` depended on ignored `work/` data despite its public
case archives being tracked. The temporal comparer now extracts those frozen
archives safely, checks their digests and source-log hashes, and reconstructs
the verdict from public manifests. At commit `e5f4aab6`, the fixed-head
tracked-only replay passed all 36 steps and six added checks, with 170 tracked
report/test-evidence files unchanged; pytest reported 187 passed, one skipped,
and five subtests passed. The pre-fix failure and post-fix replay logs are
preserved in `evidence/clean-export-2026-10-02-archive-replay/`. This closes a
reproducibility gap in the audit harness only; it does not change any solver or
physical verdict. Absolute local workspace and temporary paths in the published
log bundle are replaced with placeholders, with hashes recomputed over the
published copies.

The archived AMR stage audit's parent-value comparison is now reproducible
from frozen tarballs and synthetic geometry tests. It matches the mapped
field to weighted relative L2 `1.79e-16`, but uses a prior-run parent state;
the single common-input difference is the output write interval, so direct
same-run mapping attribution remains open. A separately built library from
the pinned Foundation 13 commit reproduces `maxCells=5000` overshoot in the
n=16 case (4,096 to 16,640 cells; 1,792 selected), with the override library
load path confirmed and clean solver exit. This confirms the already recorded
approximate-cap, whole-level selection behavior; it is not a new defect report
or solution-quality verdict. The earlier live inventory disposition remains
authoritative: no duplicate OpenFOAM issue is warranted. See
`reports/openfoam-amr-stage-snapshot-v3-2026-10-01.md` and the primary source
audit `reports/openfoam-amr-source-budget-audit-2026-09-28.md`.

The v4 same-run map capture closes the cross-run parent-field limitation for
this n=16 event. Cell-centered mapped `U` exactly equals independent injection
from the captured pre-map parent field, with `6.53e-15` maximum relative
parent-volume closure error. The corresponding exact-MMS child-center error is
41.7955%; this remains a point-sample metric rather than a finite-volume
cell-average certificate. The solver completed normally and the archive is
hash-checked; its manifest was recovered after a post-run runner metadata
exception and that recovery is recorded. No upstream issue follows from this
expected mapping behavior. Replay with
`python3 -m tools.analyze_amr_same_run_map`; evidence and protocol are in
`evidence/of13-amr-same-run-map-v4-run3/` and
`protocols/high-gradient-of13-amr-same-run-map-v4.json`.

Applying the independently Gauss-checked analytic MMS cell-average formula to
the same-run pair gives 13.7834% relative L2 for the coarse preMap DOFs and
42.4839% for the mapped child DOFs. Their normalized squared-error identity
separates inherited coarse DOF error (`0.015871`) from newly resolved exact
parent-to-child average variation (`0.164617`), with cross term near zero.
This is a DOF-level alternate comparison; it does not prove the stored evolved
`U` is defined as an exact cell average and is not a continuous reconstruction
norm. AMR quality and convergence remain UNCERTAIN pending higher-resolution
cases.

The cell-average evaluator is now isolated at
`tools/high_gradient_cell_average.py`; it no longer imports the archive-bound
uniform-grid audit module. Independent tensor Gauss checks on multiple widths,
including centers near periodic boundaries, pass, and replay of the published
AMR archive preserves its prior values. See `tests/test_high_gradient_cell_average.py`
and commit `696c0b9`. This reduces analytical-audit coupling but does not close
the missing higher-resolution AMR comparison.

The n=32 same-run first-refinement replication now confirms the independent
selection predictor (12,288 candidates), exact parent-value injection, and a
reduction in both coarse and mapped child DOF discrepancies relative to n=16.
This remains exploratory two-resolution evidence; the AMR quality status stays
UNCERTAIN. The solver run completed normally; the current 36.5 MB archive
contains the same-run cell pair and mapped face snapshot for the gradient
audit. Later-stage fields and faces remain in ignored local raw data and the
manifest/log. For this earlier n=32 run, a runner source-overlay hash was not
captured at launch and remains a reproducibility limitation. The later n=128
run has a separate verified harness-provenance addendum below. See
[`n=32 AMR report`](../reports/openfoam-amr-resolution-replication-2026-10-01.md).

The common-support n=16/n=32/n=64 derivative comparison now integrates the
analytic gradient and vorticity error throughout each cell for the
piecewise-constant finite-volume Gauss reconstruction. At n=64 this gives
13.9804% preMap and 14.0147% mapped gradient relative L2, compared with 1.8830%
and 12.1431% from cell-center samples. Order-6/order-8 tensor quadrature
agrees within 1.20e-13 in the relative-L2 ratios. The integrated diagnostic
captures within-cell variation omitted by center sampling, but does not bound
a continuous OpenFOAM reconstruction; AMR quality remains `UNCERTAIN` because
no threshold was preregistered. See the
[`cell-integrated AMR report`](../reports/openfoam-amr-volume-integrated-diagnostics-2026-10-02.md)
and `evidence/of13-amr-volume-integrated-comparison-2026-10-02.json`.
The mapped result is insensitive to a second one-ring least-squares derivative
estimate: at n=64 it gives 14.0719% gradient and 15.9026% curl error, compared
with 14.0147% and 15.8499% for the face-Gauss operator. This is an
operator-sensitivity check, not an independent solver gradient or an AMR
quality acceptance result. An independent replay of this full cell-integrated
analysis matched the tracked JSON byte-for-byte and passed its five targeted
tests; its interpreter, input evidence hash, analyzer/operator hashes, and
scope are recorded in
`evidence/tests/amr-volume-integrated-rerun-2026-10-02.json`.

The project is **not complete**. This audit preserves the original three-target
scope and the user's analytic-priority requirement. Published artifacts and
measured behavior take precedence over prior progress summaries.

The table was refreshed on October 3; dated entries below retain historical
run scopes. The [impact-scope report](../reports/impact-scope.md) now maps each
finding to a supported improvement and the evidence required to extend it.

| Requirement | Inspected evidence | Current conclusion |
|---|---|---|
| One project repository | Current git remote, public Unjuno/concentration-aware-ns | Satisfied; upstream sources held as archives, no extra project fork |
| Source/version/license audit | docs/audit.md, runtime recipes, pinned source files | Three targets identified; runtime dependencies have stated reproducibility limits |
| Analytic reference and force | reference.py, symbolic, C++, autograd and energy/Fourier checks | Verified in stated scopes; no physical blow-up inference |
| Alignment versus positional certainty | [Exact linearized Gaussian calculation](../docs/openai-core-material-trajectory.md#exact-positional-probability-check-in-the-linearized-gaussian-model); [volume-preserving measure bound](../docs/incompressible-position-uncertainty.md); Lean artifact `evidence/lean-verification/volume-preserving-position-bound.json`; [shrinking-core algebra check](../evidence/tests/shrinking-core-mass-bound.json) | Directional alignment can coexist with no concentration of an absolutely continuous passive-tracer law into a smaller fixed ball: under a smooth volume-preserving flow, probability is at most the initial density bound times target volume. Applying this to the pinned paper's shrinking Eulerian core yields an explicit occupancy upper bound of order `(1-t)^(3/2-h)`, which tends to zero for bounded initial densities. The measure inequality is Lean-checked; a global classical flow map is an explicit hypothesis. The pinned OpenAI repository formally proves its candidate statement and whole-space theorem in separate modules (clean build and axiom audit: `evidence/lean-verification/openai-public-proof-audit-2026-10-02.json`). This does not independently validate the construction's mathematics or create a molecular/stochastic-particle result. |
| OpenFOAM 3-space/multiple-time comparison | Five archives in evidence/of13-study-v1 | Runs complete; three tighter-iteration controls add 350 converged steps without changing endpoints materially or the observed order 0.493. Asymptotic temporal convergence remains unproved. |
| High-gradient OpenFOAM v2 space/time matrix | `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`; `evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-02-followup.json`; fresh archive and temporal replay [`openfoam-six-case-and-temporal-replay-2026-10-03.json`](../evidence/tests/openfoam-six-case-and-temporal-replay-2026-10-03.json); [derivative reconstruction sensitivity](../reports/openfoam-gradient-reconstruction-sensitivity-2026-10-01.md); [Arb trigonometric supremum bound](../reports/openfoam-trigonometric-supremum-bound-v3.md) | All six archived cases replay successfully. Standard acceptance passes all six; sampled local quality fails n16/n32 and passes n64/n128 and both n64 temporal cases. The coarse-grid standard-PASS/local-FAIL disagreement is observed; the preregistered persistent discrepancy at both adequately resolved n64/n128 grids is NOT_OBSERVED. The n64 three-step velocity error stays near 0.478–0.479%; temporal convergence is not certified. An Arb coefficient-sum bound certifies only the named trigonometric interpolant, not the OpenFOAM finite-volume field or unrounded solver state. An October 2 partial repeat (36/100 steps) is preserved and explicitly linked to the already completed 100-step matrix row; it is excluded from verdicts. |
| OpenFOAM solver rerun reproducibility | [Single-case repeat archive, provenance and comparator](../evidence/of13-high-gradient-repeat-2026-10-01/README.md) | A fresh n=64, dt=.0005 run on the recorded image completed 100/100 steps. All four endpoint fields and five diagnostics reproduce byte-for-byte/exactly against the earlier archive. Comparator provenance checks and four hostile fixtures pass; only five declared raw archive members may differ. This is one-case reproducibility, not a general guarantee or physical validation. |
| AMR constraints and controls | AMR, event, fixed-mesh, and `div(phi)` manifests; [n16/n32/n64 common-support first-map replication](../reports/openfoam-amr-common-support-resolution-2026-10-02.md); [four-resolution nested cell-average decomposition](../reports/openfoam-amr-nested-cell-average-error-2026-10-03.md); [cell-integrated derivative comparison](../reports/openfoam-amr-volume-integrated-diagnostics-2026-10-02.md); [live n=128 package recheck](../evidence/tests/openfoam-amr-nested-cell-average-live-recheck-2026-10-03.json) | Three budgets and two fixed-mesh controls complete. Whole-level selection explains the observed approximate-cap overshoot. Fixed-mesh errors fall to 1.88%/0.483% from AMR-path 37.0%/40.1%. A third same-run map event at n64 matches the independent 901,888-cell prediction exactly. On the common interior, cell-center derivative errors rise after mapping; volume integration of the cellwise-constant Gauss gradient instead gives about 14.0% at n64 both preMap and mapped, exposing the within-cell variation missed by center sampling. Across the n=16/32/64/128 immediate first-map events, the exact-average DOF identity separates inherited parent error from subcell-reference variation; all four stored mapped fields equal parent-value injection, with the variation term decreasing at approximately first order. The n=128 package and live release hashes replay, but this is artifact integrity, not a solver rerun. The separate cap100000 t=0.05 maximum-refinement endpoint gives 130.40% gradient and 208.82% curl error for saved cellwise-constant `grad(U)`, but it has a different run history and is not a convergence point. This is an operator-specific diagnostic, not a continuous field certificate or defect finding. No AMR quality threshold was preregistered; quality remains UNCERTAIN. |
| SU2 3-space/multiple-time comparison | All five archives; archive-review.json, diagnostic-replay.json, su2-time-comparison.json; [Oct 2 upstream and localized-residual audit](../reports/su2-localized-residual-upstream-audit-2026-10-02.md) | Matrix and standard replay complete. No standard-PASS/local-FAIL conjunction: n16 passes residual but fails accuracy; n64 time cases pass aggregate accuracy but miss 2/3/7 residual steps. Continuous derivative extrema remain uncertified. Related upstream records #2353 and #2932 already cover adjacent issues; no duplicate report filed. |
| PhysicsNeMo 3-space/multiple-time sampling | Original five archives plus 20 preregistered added-seed archives; [paired-seed analysis](../reports/physicsnemo-seed-control-v1.md); [local interval-maximum audit](../reports/physicsnemo-local-peak-refinement-2026-10-01.md); [Oct 2 upstream derivative audit](../reports/physicsnemo-upstream-derivative-audit-2026-10-02.md) | Five seeds per case complete. Spatial paired contrasts have mixed signs. Sampled velocity and gradient/vorticity metrics disagree; the full-domain continuous maximum remains uncertified. Material seed sensitivity remains and no preregistered acceptance threshold exists, so acceptance stays UNCERTAIN. Current derivative-boundary issue/PR concerns nonperiodic paths; this benchmark uses autodiff on a periodic domain, so no duplicate issue was filed. |
| Local derivatives and spectra | Native/autograd/FD2/spectral comparisons, analytic spectrum | Diagnostics exist; sampled maxima are not certified continuous maxima |
| Evidence-linked acceptance gate | v2 checker; evidence/tests/gate-artifact-audit.json; internal timestamp-sequence audit; `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json` | Eleven reports (OpenFOAM n32, PhysicsNeMo five, SU2 five); all 93 artifact links match. Verdicts remain UNCERTAIN with gaps explicit. The run-level parser's duplicate/skipped-time false-pass was found synthetically and corrected. The current six-case OpenFOAM uniform matrix is complete; its four original fixed-step archives pass the sequence check, and the two later temporal addenda independently validate 100/100 and 200/200 completed steps. |
| Genuine upstream reporting | [Three-project live disposition, 2026-10-02](../reports/upstream-status-2026-10-02.md); SU2 Q&A 2890 and issue #2353; PhysicsNeMo issue #2007 follow-up comment | Rechecked live target heads and issue states. PhysicsNeMo's known odd-width defect reproduces on current main and was added to its existing issue; SU2's discussion is closed without a chosen answer and adjacent issues remain open; OpenFOAM's GitHub list does not match the exploratory AMR result, while its separate issue tracker was not exhaustively searched. OpenAI's Lean repository has no issue/discussion channel. No duplicate or speculative issue filed. |
| Other target report/no-report decisions | Interim audit and contribution policies | Explicit no-defect-report decisions for OpenFOAM and PhysicsNeMo are recorded in reports/upstream-disposition.md; the SU2 BDF2 finding is scoped separately |
| OpenAI construction audit and transfer | Independent NS kernel logs for both pins; current source-bound extension checks; docs/axis-flow-derivative.md; docs/packet-constant-dependencies.md; conditional Jeffery bridge in docs/fiber-vortex-literature-audit.md | Full axis Jacobian, explicit variational solution, inverse identity and eventual axis smoothness are Lean-checked. The cusp-ball theorem supplies a field-equality radius proportional to `sqrt(1-t)` and transfers the base endpoint Hessian exponent `kappa=40` to the full spacetime jet on that ball. `SpatialHessianTransfer.lean` composes the local `ContDiffAt` spatial restriction with the selected-field estimate and is Lean-checked with an axiom audit. The classical nonlinear packet comparison remains outside Lean, so `Cstretch+39` is a conditional, non-effective shrinking-packet allowance; `Cstretch<4` gives a more conservative conditional `Q^43` sufficient packet-radius power under the same envelopes. Neither gives a fixed-packet certificate. Nonlinear-flow identification remains classical; there is no end-to-end Lean flow theorem. The Jeffery director follows an integrated-strain law: pointwise-unbounded but integrable strain does not force alignment, while the idealized `1/(1-t)` rate is nonintegrable and predicts alignment only with an added finite-object spatial-uniformity assumption. The strict negative force-ratio limit still requires the unresolved actual-profile pressure premise. The pinned Euler challenge has passed recorded independent checks; no molecular or constitutive consequence is established. Executable finite-stage extraction remains unperformed. |
| Analytic forcing and unforced-defect literature refresh | [arXiv:2609.20803v2](https://arxiv.org/abs/2609.20803v2); [arXiv:2609.23868v1](https://arxiv.org/abs/2609.23868v1); versioned record [`analytic-literature-2026-10-03.json`](../evidence/upstream-refresh/analytic-literature-2026-10-03.json) | A conditional regularity theorem excludes spatially analytic forcing when combined with the OpenAI construction's cited anisotropic/core-symmetry properties and bounded-C2 force; its corollary also excludes a force vanishing throughout any backward cylinder ending at a singular point. The paper does not independently verify that construction, and this is no pointwise lower bound. A separate paper studies an unforced positive-defect target and explicitly limits what finite Galerkin computations certify. Neither changes solver verdicts or supports molecular/constitutive conclusions. |
| User-proposed Burgers feedback and particle interpretation | `reports/recent-developments-and-hypothesis-audit-2026-09-28.md`; `tools/check_burgers_feedback_mapping.py`; [accumulated-strain discriminator](../evidence/tests/alignment-integrability-threshold.json) | Under imposed linear strain, the Gaussian-vorticity width equation yields the diffusion-versus-strain threshold. The extra `a=kappa W_peak` closure is not derived from Navier–Stokes; its parameterization matches the known singular Burgers-vortex family, which has spatially growing linear strain. The new exact Jeffery calculation shows an unbounded rate `gamma~(1-t)^(-alpha)` need not align a director when `0<alpha<1`; the OpenAI-style `alpha=1` only predicts alignment in the spatially uniform ideal finite-object model. The OpenAI-core comparison still tests pointwise vorticity on one selected trajectory, not global peak vorticity. Molecular orientation, phase transition, and constitutive-viscosity changes remain unsupported. |
| OpenFOAM n=64 endpoint pressure reconstruction | v3 frozen protocol, three Docker archives, and independent archive replay | All three dt cases exit 0; U/p/phi are byte-identical to same-dt baselines, and endpoint velocity algebra replays at 2.12e-16–2.15e-16 relative L2. Narrow endpoint gate passes; trajectory cause, molecular alignment, phase change, and material-viscosity claims remain unsupported. |
| Reproducible public deliverables | Runtime instructions, scripts, archived raw results; [fresh export record](../evidence/clean-export-2026-10-01-alignment-uncertainty/README.md) | The tracked-only clean export at `6e16c65` passed 26 replay steps and seven additional checks in a fresh locked venv; all 153 report/test-evidence files were byte-identical. Full pytest reported 151 passed, one skipped, and five subtests passed. Solver rebuild/reproduction remains separate. |

The latest fixed-revision clean-export summary and command logs are public in
[`evidence/clean-export-2026-09-30-current/`](../evidence/clean-export-2026-09-30-current/README.md).
This strengthens reproduction of tracked Python evidence only; it does not
reproduce a solver, training run or Lean build.

The 2026-10-02 focused three-project inventory has its own tracked-only replay
at [`evidence/clean-export-2026-10-02-upstream-refresh/`](../evidence/clean-export-2026-10-02-upstream-refresh/README.md): 36 report-replay steps and six additional checks passed, 171 tracked report/evidence files remained byte-identical, and the full tests from the fresh exported source reported 187 passed, 1 skipped, and 5 subtests passed. This verifies the published postprocessing/evidence path on the recorded host, not solver rebuilds or runs.

The 2026-10-02 JST focused upstream refresh is recorded in
[`three-project-inventory-2026-10-02.json`](../evidence/upstream-refresh/three-project-inventory-2026-10-02.json)
and [`upstream-disposition.md`](../reports/upstream-disposition.md). It found
no new reportable issue; OpenFOAM's separate tracker was only searchable, not
directly accessible, so its coverage remains explicitly incomplete.

The archived Foundation 13 `volVectorField U` values are discrete DOFs; they do
not define a unique within-cell continuous field. Even if one assumes exact
cell averages, smooth divergence-free perturbations supported inside cells
can leave all DOFs unchanged; an explicit sequence even tends to zero in
uniform velocity norm while its continuous gradient grows without bound. See
[finite-volume derivative identifiability](../reports/openfoam-fv-continuous-derivative-identifiability.md).
This information limit is not evidence of an OpenFOAM defect or molecular
alignment. Issue #5 remains open for any claim about the actual finite-volume
field.
The curl/divergence identity and high-frequency gradient term now have a
SymPy replay and regression test (`tools/check_fv_derivative_nullspace.py`,
`tests/test_fv_derivative_nullspace.py`); the sequence makes its velocity
perturbation vanish uniformly while its continuous gradient grows. This is
conditional analysis of the observation class, not a same-forcing solution.

### Analytic result refreshed 2026-09-30

The OpenAI extension was re-run in the pinned Lean checker environment from the
current `verification/AxisForceSign.lean`; its 21,306-byte output is byte-equal
to `evidence/lean-verification/axis-force-sign.log`, and the source hash matches
`axis-force-sign.json`. It reports only `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorryAx`. The checked chain includes the selected
candidate's full axial Laplacian limit, material acceleration, and their ratio.
For a root in the prescribed interval, `actual_ratio_negative_of_local_Z`
proves a strictly negative, nonzero limit under the local pressure-moment
condition `Z>0`; `outgoing_root_Z_positive_iff_moment_threshold` gives its exact
moment inequality. This sharpens the sufficient premise from global
`PressureData`. Neither premise has been shown for the arbitrary
`FinalSlowBase.actualProfile` choice, so the conclusion remains conditional at
that selection boundary. It concerns viscous force divided by material
acceleration on one trajectory, not a constitutive-viscosity law or molecular
alignment. The `AxisForceSign.lean` ratio and moment-threshold proof closure
has now passed an independent nanoda check (85,455 declarations, zero
typechecker errors); its hash manifest and rerun script are in
`evidence/lean-verification/axis-force-nanoda-2026-09-30.json` and
`runtime/lean-verification/check_axis_force_nanoda.sh`. The separate
`SupportHoleAssembly.lean` cusp-ball and Hessian-transfer extensions have
pinned Lean elaboration and axiom-audit records, including the ten-declaration
v6 run cited below, and have now passed an independent nanoda check of 85,487
declarations with zero typechecker errors. Nanoda reported one pretty-printer
error (`Unable to print axioms`); the separate Lean audit printed the allowed
axioms for all ten target declarations. The run manifest and rerun script are
`evidence/lean-verification/support-hole-nanoda-2026-10-01.json` and
`runtime/lean-verification/check_support_hole_nanoda.sh`. Conditional
parameter assumptions remain. The local `ContDiffAt` restriction inequality
and its composition with the selected-field cusp-ball Hessian theorem are now
compiled and axiom-audited in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`.
The classical nonlinear packet comparison remains outside Lean. The
AxisForceSign, SupportHoleAssembly, and spatial-Hessian transfer checks are
distinct proof closures.

An UNCERTAIN result is legitimate evidence of a limitation, but it is not a
substitute for an unperformed required run or a missing final report. The archive
inventory verifies readability and identity only. A recorded zero exit code does
not prove accuracy, convergence or the correctness of the underlying review.

Current report and exact-algebra replay covers eighteen steps, including all five SU2 archive
reviews, diagnostic replays, spectral derivatives, direct temporal differences
and gate generation, including the separate BDF2 control, root-pressure identities,
pressure-moment threshold, cone sign symmetry and archived Dirichlet boundary-time
pilot. The current 50 tests and 93 matching artifact links
verify their stated implementation and provenance scopes, not continuum accuracy.
PhysicsNeMo's missing preregistered threshold remains a limitation that cannot
be repaired retrospectively.

Remaining completion work:

1. Comparative audit now exists at reports/comparative-audit.md. Retain its
   bounded conclusions: no certified standard-PASS/local-FAIL case is established.
2. SU2 observed aggregate checks are now included in each case report with a
   hashed review artifact and archive-identity check. All five observed
   conjunctions fail. Their post-hoc definition remains distinct from a
   preregistered acceptance gate; continuous-peak and inner-iteration uncertainty
   remain. OpenFOAM and PhysicsNeMo standard-acceptance limitations remain recorded.
3. Independently review the new source-to-trajectory implication chain; symbolic
   identities do not cover theorem hypotheses. New Lean proofs now establish the chart derivative chain through the natural
   profile, including a root with eventual negative derivative, the selected base-field vector material trajectory, and its axis Laplacian identity. An independent symbolic Eulerian material-acceleration calculation agrees with the trajectory formula. Current Lean proofs establish the physical Laplacian/material-acceleration limit and strict negative sign under explicit root and PressureData assumptions. Unconditional instantiation for actualProfile remains unproved. Do not describe original kernel acceptance
   as verification of our new result.
4. Tracked-only export and fresh-venv postprocessing succeeded (see
   evidence/fresh-environment-check.json). SU2 discussion now has a September 13 response; the September 26 BDF2 follow-up reproduces the suggested order-reduction control and is posted with raw evidence. No general-fix endorsement is inferred. Full solver builds were not
   repeated by this postprocessing check.
5. Audit the requested impact analysis against what the evidence supports.
   No finite benchmark can establish all industrial or molecular consequences;
   reports/impact-scope.md now bounds findings by solver versions, cases and
   construction hypotheses. Effective finite-packet bounds and the actual-profile
   pressure premise remain unresolved; publication of the scope report does not
   discharge them.

September 27 reconciliation and replay: all thirteen archived-input replay
steps completed with exit code zero, including 36 tests and 93 matching artifact
links. Comparison values and localized verdicts did not change. Both existing
125-declaration Lean results still match the current extension source and log
hashes; no new Lean execution is claimed by this reconciliation. The comparative
report now includes the six BDF2 controls and distinguishes checked deformation
components from the classical nonlinear-flow argument. No new solver runs,
training runs, upstream messages or theorem changes occurred in this audit.

This remains an interim audit, not a declaration that all goal requirements
have been completed.

### Quantitative copy-support hole, 2026-09-28

The updated OpenAI source's `SupportData.sum_support` now feeds a new Lean
extension, `verification/SupportHole.lean`. The theorem
`copy_sum_zero_below_physical_hole` proves that a supported copy-family sum
vanishes whenever its physical transverse radius is below
`a*sqrt(physicalQ/2)`. The proof uses the dyadic active-band comparison and
the annulus-to-physical-radius identity, and compiled with the pinned checker
environment. This is a generic primitive-family result. It does not yet show
that all actual candidate stages, direct curls, and the full cutoff series
share one coefficient on a complete tube. The packet-radius transfer and
completion verdict therefore remain unresolved; see
`docs/packet-constant-dependencies.md`.

### Conditional cusp-tube chart estimate and source-bound correction

The similarity equation `tau=q-z^2 q^(2h)` yields the normalized coordinate
`F(eta)=eta*(1-eta^2)^(-D)`, `D=1/2-h`. Its derivative factors as
`(1-eta^2)^(-D-1)*(1-2*h*eta^2)`, bounded below by `1-2h>0` on `|eta|<1`.
This gives a uniform inverse bound: an axial displacement of at most
`c*sqrt(tau)` around the selected axis curve changes eta by at most
`c*tau^h/(1-2h)`. Conditional on a common primitive inner-support coefficient
`c0`, choose c smaller than both `c0` and the chart-margin allowance. For
sufficiently small tau, the full spatial ball of radius `c*sqrt(tau)` remains
inside the physical sublevel and spatial/time localization plateaus, and lies
inside the proposed support hole. The exact algebraic identities are checked
in `evidence/tests/support-hole-tube-geometry.json`; derivation and explicit
smallness conditions are in `docs/support-hole-tube-geometry.md`. The
conditional existential cusp-ball interval and actual selected-field local-
germ equality now pass the pinned Lean check and axiom audit in
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/`. It remains a shrinking-
ball continuum result with conditional parameters; it is not a finite-size
packet theorem or numerical packet certificate.

This audit also corrects a source-description error in an earlier note:
OpenAI's `SublevelShrinkingSupport` is an outer support bound (nonzero values
have radius at most the stated shrinking outer radius). It does not establish
an inner hole. The candidate hole depends on separate lower annulus bounds;
selected-stage transfer, cutoff sums, curl, and final-field equality remain
unproved.

Correction to analytic evidence: the force-ratio geometric factor d=1-eta²
was inverted in earlier revisions. Current symbolic and Lean sign checks
use -nu*d*Z/(L*A*U). The historical fresh-environment check-3.log records
the superseded formula and is retained as a run record, not evidence for
the corrected coefficient. The current axis-force symbolic JSON and Lean
verification JSON contain the corrected run. Strict negativity survives;
physical-force identification is checked conditionally; unconditional pressure instantiation remains incomplete. See the pressure-hypothesis retention audit in docs/openai-core-material-trajectory.md.

Verification-gate fault injection (2026-09-26):
`python3 -m unittest discover -s tests -p test_axis_verifier.py -v` passes five
checks. The recorded successful axiom output is accepted; a failed subprocess,
a missing required axiom report, a forbidden sorryAx, and source mutation during
the mocked run are rejected with CLI exit code 1. Fixtures and outputs live in
temporary directories, so this check does not overwrite published proof evidence.
These tests exercise the Python acceptance/exit-code path, not Lean itself, and
do not discharge the actual-profile pressure condition. No new Lean replay is
claimed from this test run.


Current-checkout report replay (2026-09-26): all twelve steps completed with
exit code 0, including 36 tests and all 88 artifact byte-identity checks.
Only the test log and its recorded hash changed during regeneration; generated
comparison values and gate reports were unchanged. The run is recorded in
`evidence/report-replay/summary.json`. It is a replay of archived-input
postprocessing, not a fresh solver, training, or Lean run. Historical fresh-venv
records retain their own earlier scope and are not relabeled as this run.


SU2 aggregate-review integration (2026-09-26): the report builder now carries
velocity, energy and all-step residual observations from
`evidence/tests/su2-standard-review.json`, hashes that artifact and checks that
each reviewed archive matches the case archive. It no longer incorrectly says
that energy review is absent from the report. This addition does not change the
conservative gate flags or promote post-hoc observed FAIL to a preregistered
standard-acceptance decision. The raw review can be regenerated separately with
`python -m tools.review_su2_standard` in the verification dependency environment.

The integration replay passed all twelve steps and 36 tests; all 93 artifact
links match (five additional SU2 aggregate-review links). All eleven gate
verdict files are unchanged.


The forcing-scope comparison is now explicit in
`reports/forcing-scope-audit.md`: the implemented manufactured force is analytic
for fixed positive sigma, while the construction and later regularity/density
results have different forcing quantifiers and hypotheses. This addresses part
of the impact audit without extending any numerical verdict to singularities.
Full follow-up-paper proof review and updated-source compatibility remain open.


BDF2 follow-up replay integration (2026-09-26): the common replay now has thirteen
steps, including raw-archive BDF2 recurrence and endpoint-error verification.
All thirteen completed successfully, with 36 tests and 93 gate artifact links.
The six BDF2 control runs are separate from the eleven localized acceptance
reports; their successful residual and recurrence checks do not change those
UNCERTAIN verdicts. The updated OpenAI assembly build and unchanged extension check have now completed successfully; see evidence/upstream-refresh/updated-verification-summary.json. New-pin independent Comparator/nanoda verification subsequently completed successfully for the R3 and periodic challenge; evidence/upstream-refresh/updated-comparator-result.json records it. Neither check discharges the pressure premise.


Clean-export refresh (2026-09-27, commit `60302db`): thirteen replay steps and
five additional checks exited zero in a fresh same-host environment. Strict
byte equality failed in six of 66 compared files. All inspected differences
were NumPy version metadata and propagated hashes; numeric results/verdicts
were unchanged. See `evidence/clean-export-2026-09-27/README.md` for the exact
scope, preserved failure, differences and logs. This adds reproducibility
evidence without discharging the open physical, analytic or formal premises.


Integrated pressure-analysis replay (2026-09-27): all sixteen steps exited zero,
including 45 tests and 93 matching artifact links. The three added algebra
checks reproduced their existing JSON exactly; existing comparison values and
gate reports were unchanged. The current replay requires
`requirements-verification.txt` for SymPy and SciPy. Logs and hashes are in
`evidence/report-replay/summary.json`. This is not a new clean-export, solver,
training or Lean run, and it does not resolve the actual-profile pressure gap.


Boundary-pilot replay integration: all seventeen steps completed with exit code
zero, including the raw two-variant/two-step boundary checker, 45 tests and
93 matching gate artifact links. This checker independently selects nodes by
mesh numbering and reads residuals and time labels from the archives. It adds
no temporal-order or restart claim. The existing localized gate verdicts remain
UNCERTAIN. Separately, the current 149-report Lean extension now derives actual
physical-ratio negativity from local Z>0, without global PressureData; the
actual outgoing weighted-moment threshold is equivalent to that local sign
condition. Its satisfaction for the selected profile remains unproved.


Restart-finding replay integration: the current eighteen-step replay completes
with 50 tests and 93 matching gate artifact links. Its restart step reruns the
raw checkers and accepts only the specific field-agreement/history-mismatch
result for both R=2 and R=3. Scientific history-time continuity remains FAIL;
reproduction success does not relabel it. Five fault tests reject wrong exit
codes, missing rows, wrong times and nonfinite/large field differences.
No new solver or Lean run is part of this integration.


Locked-dependency replay: at commit `5b8e305`, a fresh tracked-only export
passes eighteen replay steps and five additional checks; all 75 compared
report/test files match byte-for-byte. Evidence is in
`evidence/clean-export-2026-09-27-locked/`. This closes the observed dependency
version drift for that explicit same-host configuration. Supported-range
NumPy 2.5.3 failures remain preserved, and no cross-platform, solver-build,
training or Lean reproducibility conclusion is added.


## Current next-action audit after startup controls

The completed work narrows rather than closes the remaining numerical question.
The three tight-iteration runs and archive-only replay rule out a material
endpoint response to those specific tolerance changes. Constructor probes
establish the initial discrete face-flux mismatch. Two completed early-time
runs and an unfitted leading Poisson model support a startup pressure/velocity
response, but do not establish its causal role in later-time order reduction.
Spatial operator checks show this initialization correction shrinks with mesh
refinement; none of these results proves a physical singularity.

Required next evidence, in dependency order:

1. Resolve the actual state of the pending dt=0.00025 startup request. Its host
   process remains live and a Docker daemon ping timed out; no replacement run
   is justified solely from that observation. Preserve the two completed cases.
2. Complete the three-case common-endpoint startup comparison. The published
   comparator requires all cases; partial pressure/velocity evidence is labeled
   separately and cannot be promoted to a three-level result.
3. Execute the frozen initial-divergence intervention once Docker is responsive.
   All three prepared input manifests pass, and only initial U differs. A
   successful prediction would identify the initial impulse's dependency on
   initial discrete divergence, not certify the original MMS acceptance gate.
4. Only then select an experiment to test whether that startup mechanism affects
   the t=0.05 temporal result. Avoid treating a changed initial-value problem
   as a repair of the original benchmark or assuming its result in advance.

At the historical update, the common replay had 25 passing steps and 59 tests.
It includes a fresh six-archive OpenFOAM comparison reconstruction, the SU2
output-clock replay, exact uniform-prefix threshold algebra, and the localized
high-gradient MMS plus its independent symbolic-versus-NumPy derivative
comparison. It excludes solver runs for that new MMS case.
The analytic actualProfile moment/amplitude obligation and non-effective
packet constants remain unresolved. Whole-goal completion is not established.

### Startup intervention completion update

The original pending baseline completed without a task-issued runtime restart;
all three baseline and all three solenoidal control cases are now complete.
`reports/openfoam-solenoidal-startup-control.md` records the observed suppression
of the leading startup pressure impulse and its limits. Steps 1–3 in the
next-action list above are now satisfied. Step 4 (late-time causal attribution)
and the independent analytic obligations remain open. The new control archive
reader passes on the real six-archive comparison; this does not change any
original acceptance gate or claim whole-goal completion.

### Replay integration on 2026-09-28 JST

The common replay now includes the completed archive-only solenoidal startup
comparison: 22/22 steps pass using
`work/clean-export-2026-09-27-locked/venv/bin/python -m tools.replay_published_reports`.
The original system-Python attempt failed at step 15 because SymPy was absent;
its summary and error log remain in
`evidence/report-replay-missing-sympy-2026-09-28/`. This is an environment failure,
not a numerical finding. The successful run uses the existing locked-dependency
venv against the current checkout; it is not a new clean-export or solver replay.
The startup diagnostic JSON was regenerated without a tracked difference.
At this historical replay checkpoint the late-time v2 intervention was still
running; it completed afterward, as recorded in the following section.

### Late-time intervention result

All three v2 late-time controls are complete and the six-archive comparator
passes. Projecting initial U changes observed temporal order from 0.49291429
to 0.49948838; the late-time anomaly persists despite the early impulse
suppression. The planned initialization-sensitivity experiment is complete,
but it does not resolve the original temporal acceptance gap. See
`reports/openfoam-solenoidal-late-control.md`. Whole-goal completion remains
unproven, including the independent analytic obligations.

The common replay has been extended with the archive-only n=16 pressure
reconstruction pilot. In the locked-dependency environment, 23/23 replay steps
pass. The pilot proves byte-identical endpoint fields under diagnostic
instrumentation and verifies the final-call pressure/velocity algebra at
roundoff. It does not yet attribute the n=64 temporal discrepancy; an instrumented
three-dt run is now complete for its endpoint-only gate; see the update below.

### n=64 pressure endpoint reconstruction, 2026-09-28

The frozen v3 three-dt OpenFOAM 13 diagnostic matrix completed and its retained
archives independently replay. Each run exited zero and has same-dt byte identity
for endpoint U/p/phi. This closes that experiment's endpoint gate only; it does
not identify the temporal-order mechanism or support molecular/constitutive
claims. The locked environment completed all 23 configured report-replay steps. The
whole project remains incomplete under the unresolved analytic and solver gates
listed above. See `reports/openfoam-pressure-reconstruction.md` and
`evidence/of13-pressure-reconstruction-n64-v3/`.

### Directional-alignment audit, 2026-09-28

The selected continuum deformation now has an explicit angle formula for
infinitesimal separations and a conditional finite-packet angle bound with its
exceptional transverse subspace stated. The finite-packet bound still needs
effective tube-radius and Hessian constants and does not model molecules. Exact
linearized squared-ratio algebra passes the pinned Lean runner; the nonlinear
finite-packet estimate remains classical and conditional. The separate SymPy
identity checks are in `evidence/tests/axis-directional-alignment.json`. See
`docs/axis-directional-alignment.md` and
`evidence/lean-verification/axis-force-sign.json`.

The finite-packet note now converts a target angle into explicit angle-error
and tube-exit bounds on the initial radius. The formula is symbolically checked,
but selected-profile values for `rho(T)` and `M(T)` are still missing, so no
numerical packet is certified.

### Post-announcement density-paper intake, 2026-09-28

The current arXiv v4 of 2609.10262 and its linked formalization project were
inspected. The article claims force-space density thresholds from a compact
OpenAI forced-blowup input; its Lean repository maps 27 article results and the
latest recorded GitHub Actions run passed the architecture and Lean-contract
jobs. Our local external-source checks are static only; a local Lean build was
not run because the pinned Lean toolchain is unavailable in this environment.
The downstream formalization therefore does not independently verify the
OpenAI seed. “Dense” here refers to specified forcing norm topologies, not
probability or molecular alignment. The result supports keeping forcing input
identity and spectrum auditable across solver resolutions, but does not alter
the frozen benchmark gates, solver verdicts, or upstream-reporting decisions.
The version-history correction, dependency boundary and evidence record are
in `docs/openai-refresh-2026-09-28.md` and
`evidence/upstream-refresh/force-density-2026-09-28.json`. Whole-goal
completion remains unproven.

### Independent recent-work scan, 2026-09-28

The 20 September *Positive Defect Problem* preprint was reviewed alongside the
OpenAI source refresh. It provides a distinct, machine-checked reduction from
positive energy defect to an averaged fine-shell energy-flux floor, but says a
finite Galerkin computation cannot certify that uniform condition. No existing
MMS run tests this target, and the paper supplies no microscopic alignment
bridge. The finding is recorded as a research direction only; gates and
verdicts are unchanged. See the added subsection in
`docs/openai-refresh-2026-09-28.md`.

### Direction probability versus spatial concentration, 2026-09-28

The audited local deformation gives a conditional closed-form probability that
an isotropically sampled infinitesimal separation lies within a chosen angle of
the axis. Its limit is one as the singular time is approached. The same map has
unit determinant, so an initially isotropic Gaussian retains its peak density
and differential entropy while becoming transversely narrower and axially
wider. The symbolic identities pass in the reference-check environment. This
sharpens the user's direction-alignment idea while rejecting the inference that
it establishes concentrated absolute positions or molecular predictability.
Finite-packet and kinetic-model premises remain open; the acceptance gates and
solver verdicts are unchanged. See `docs/particle-position-probability.md`.

In the global affine tangent-map toy calculation, observation regions separate:
mass in any fixed-radius infinite axis tube tends to one, while mass in a fixed
finite cylinder is asymptotic to `sqrt(2/pi)*L*Q^C` and tends to zero. This
illustrates how transverse localization can coexist with increasing axial
uncertainty, unchanged peak density and constant differential entropy. The
actual nonlinear-flow theorem does not establish the affine map on an
unbounded Gaussian cloud. Symbolic limit checks pass after substituting
`z=Q^C`, which avoids a symbolic-exponent limitation in the CAS. No microscopic
or finite-packet claim is added.

### Conditional finite-packet radius scaling, 2026-09-28

The classical tube and angle-error sufficient conditions were combined under
explicit endpoint envelopes `rho(Q)=rho0*Q^r` and `k(Q)<=k0*Q^-kappa`.
Splitting `kappa-r-1` by sign gives a joint sufficient initial-radius power
`Q^(C+max(r,kappa-1))`; for `C>1`, this tends to zero. The new SymPy check
verifies the integral bound and piecewise exponent identities. Neither the
endpoint envelopes nor their constants are established for the selected
profile, and the result is not a fixed-packet counterexample. See
`docs/axis-packet-bound.md` and `evidence/tests/packet-radius-scaling.json`.

### Current archived-report replay and selected-profile gap, 2026-09-28

The locked-dependency replay was rerun against the current checkout:
`work/clean-export-2026-09-27-locked/venv/bin/python -m
tools.replay_published_reports`. All 23 configured steps exited successfully;
the acceptance-audit suite ran 54 tests and the artifact audit matched all 93
links. This is archived-input report and exact-algebra replay only. It does not
include new solver, training, or Lean execution and does not alter any scientific
verdict.

The source audit reconfirmed a material instantiation gap. In the pinned OpenAI
source, `FinalSlowBase.actualProfile` is `Classical.choice profileData_nonempty`;
the `ProfileData` record retains nominal, cone and modulation witnesses but no
explicit amplitude lower bound or `PressureData` field. Our Lean extension
constructs a separate pressure-qualified `ProfileData` from
`PreparedOutgoing.exists_prepared`, but explicitly does not identify it with the
upstream choice. Thus existence of a pressure-qualified profile does not yet
establish the negative force-ratio result for the selected profile. This is not
an upstream counterexample or evidence that no implication follows from the
retained fields; deriving that implication or changing the selected construction
remains open. The replay and source cross-reference are recorded in
`evidence/report-replay/summary.json`, `evidence/report-replay/tests.log`,
`docs/pressure-moment-threshold.md`, and `verification/AxisForceSign.lean`.

### Localized high-gradient manufactured solution, 2026-09-28

Added a second analytic periodic transient MMS candidate with vector potential
`A=(0,0,exp(-t) chi(y,z) sin(Nx)/N^2)`, where
`chi=((1+cos y)/2)^4 ((1+cos z)/2)^4`. Exact symbolic checks verify
divergence-free velocity, the time-dependent forced Navier–Stokes identity, its
selected derivative and vorticity formulas, and the envelope's finite Fourier
expansion. Orthogonality gives exact t=0 volume means for `N=4,8,16`. The
velocity supremum is bounded above by `exp(-t)*(1/N+2/N^2)`, while
`partial_x u_y` attains `exp(-t)` at the localized envelope center; this
analytically separates small velocity amplitude from an order-one local
derivative.

This case is now in `docs/protocol.md`, `tools/check_high_gradient_mms.py`,
`tests/test_high_gradient_mms.py` and `evidence/tests/high-gradient-mms.json`.
The locked report replay then had 25 successful steps and 59 tests. A second
implementation evaluates fields from hand-coded Fourier derivative formulas;
direct SymPy differentiation agrees for velocity, gradient, vorticity and
forcing at 65 seeded points for each `N`, with maximum component error below
`2.3e-16`. OpenFOAM's case generator now emits the matching time-dependent
`codedFvModel`, and a unit test reads back the generated cell initialization.
The original Foundation 13 matrix and quality thresholds are preserved in
`protocols/high-gradient-of13-v1.json`; before any solver run, the FD2
reference-only floor audit showed that n=16 and n=32 exceed the 5% gradient and
vorticity thresholds even for exact sampled data. The additive successor
`protocols/high-gradient-of13-v2.json` adds n=128, giving two spatial levels
(n=64,128) below both derivative floors; the reproducible audit is
`evidence/tests/high-gradient-fd2-resolution-floor.json`. A mock-mesh C++ compiler check is
available at `tools/check_high_gradient_openfoam_force.py`. It has not run:
the selected OrbStack Docker context did not answer `docker info` within 3 s,
recorded at `evidence/environment/openfoam-docker-preflight-2026-09-28.json`.
No daemon restart was attempted because running OrbStack processes were
present. A local minimal-type C++ mock checker is also prepared, but host
`/usr/bin/c++` is gated by the unaccepted Xcode license; no license state was
changed. Its preflight is in
`evidence/environment/high-gradient-compile-preflight-2026-09-28.json`.
Consequently no solver result or C++ compile result is claimed, and there is no
evidence that a solver misses the peak. The spatial/time matrix, AMR run,
threshold results and cross-solver comparisons remain open.

The high-gradient AMR path now uses the analytic `chi(y,z)` envelope as its
refinement sensor. `tools/openfoam_amr_case.py`, `tools/analyze_amr.py` and
`tools/run_high_gradient_amr.py` support the frozen 4096/5000/100000 cell
budgets and compare nonuniform fields to the exact time-dependent reference.
The six-case v2 uniform matrix also has a provenance-recording runner in
`tools/run_high_gradient_openfoam.py`; both runners check the immutable image
and require a clean committed source tree before creating a work tree. Case
generation, sensor wiring and the current test suite pass, but neither high-gradient
matrix has been run. The blocked-candidate count is explicitly `UNOBSERVED`
unless runtime evidence exposes it. Spectrum remains unavailable on the
nonuniform mesh without a validated reconstruction.
An offline analyzer control now verifies that the sampled central-FD2 component
peak differs from its exact cell-sample derivative peak by the predicted
`sin(N*dx)/(N*dx)` factor; the continuous full-gradient peak remains uncertified
and the result stays `UNCERTAIN`.

The uniform runner was invoked once after preparation; its bounded eight-second
Docker image-inspect preflight timed out and created no case tree. The exact
result is in `evidence/environment/openfoam-high-gradient-run-preflight-2026-09-28.json`.

The post-announcement mathematical and physical literature scan, including the
OpenAI source refresh and explicit molecular-bridge audit, is summarized in
`reports/recent-developments-and-hypothesis-audit-2026-09-28.md`. That note also
corrects the live SU2 Q&A status: a maintainer replied on September 13 and the
author added the BDF2 control on September 26; GitHub has not marked an accepted
answer.

### High-gradient acceptance gate integration, 2026-09-28

The uniform analyzer now computes relative velocity, energy, FD2 gradient,
vorticity and sampled shell-spectrum errors, and the runner writes separate
standard-acceptance and local-quality verdicts. Standard acceptance requires
the requested endpoint, expected number of time steps, one PIMPLE convergence
record per step within the configured outer-corrector limit, and an `fvSolution`
whose outer-corrector count and absolute `p`/`U` residual controls match the
frozen protocol. This parser was tested against the preserved Foundation 13 n64
run archive as well as synthetic pass/fail/truncated/misconfigured logs. The matrix-level blind-spot verdict requires both
n=64 and n=128 to pass standard acceptance and fail local quality; these are
the two levels whose exact-reference FD2 floors clear the preregistered gradient
and vorticity thresholds. Missing evidence stays UNCERTAIN. All 68 tests and
the 25-step archived report replay passed. This is gate implementation evidence
only; the high-gradient OpenFOAM matrix and AMR sweep had not run at this
historical update.

### High-gradient OpenFOAM execution update, 2026-09-28

The original six-case uniform runner completed and archived the n=128,
dt=0.001 case at t=.05 with exit code 0, 50/50 PIMPLE-converged steps and an
`End` marker. Its standard acceptance and local-quality gates both PASS. The
coarse n=16 and n=32 cases remain standard PASS/local FAIL but are below the
preregistered exact-reference FD2 resolution floors; n=64 and n=128 at dt=.001
are standard PASS/local PASS. These observations do not reproduce a persistent
acceptance blind spot.

The runner then started n=64, dt=.0005 and stopped logging at t=.018. The
preserved log has 36 time records, 35 completed convergence records, and no
terminal marker or exit record. At the last live audit there was no observable
`foamRun` process, while the Docker client and Docker/OrbStack inventory/stop
requests remained unresponsive. The container's terminal state is unknown; its
partial inputs and logs remain preserved. The final dt=.00025 case and all
three high-gradient AMR budgets remain unrun. Accordingly, v2 remains
INCOMPLETE/UNCERTAIN, with no solver-defect or physical-singularity inference.
The completed n=128 archive is published as two checksummed Zstandard parts
under GitHub's per-file limit, with reconstruction instructions in
`evidence/of13-high-gradient-v2/README-n128-archive.md`.

### Current locked replay refresh, 2026-09-28

The locked same-host environment replayed all 25 configured report steps with
zero failures. Its unittest discovery ran 73 tests, and the artifact audit
matched all 93 links. The separate current verification environment passed 75
pytest tests and five subtests. The refreshed high-gradient MMS replay log
now includes selected-point Frobenius-gradient lower bounds; its independent
reference-comparison replay log records NumPy 2.5.2 from the locked environment. This replay
updates archived analytic/report artifacts only; it does not rerun any solver,
continue the stalled Docker case, or upgrade a scientific verdict.

A fresh tracked-only replay of commit `0a950128f0d49701d6323b8ccd58f71b7e20e715`
on 2026-09-28 also completed all 25 report steps, SU2 standard review, and four
symbolic axis checks with exit code zero. The strict 111-file byte comparison
returned nonzero for one field only: the tracked high-gradient reference JSON
records NumPy 2.5.3, while the locked environment regenerates it with NumPy
2.5.2. Removing that version string makes the JSON objects identical. This is
a preserved metadata-only reproducibility mismatch, not a numerical discrepancy
or a clean-export PASS; details and sanitized command outcomes are in
`evidence/clean-export-2026-09-28-current/`.

The locked metadata baseline was then regenerated under NumPy 2.5.2 and the
new support-hole geometry check was added to report replay. A fresh export of
commit `03ce175fcf26d17869de330720f2dfe8a49c4481` now passes: 26 replay steps,
85 unit tests, 113 compared report/test files, and zero changed files. This is
Python postprocessing/replay evidence only, not a solver, training or Lean
reproduction. Sanitized logs and hashes are preserved at
`evidence/clean-export-2026-09-28-cusp-tube/`.

### Analytic axis-margin continuation, 2026-09-30

`verification/SupportHoleAssembly.lean` now has three additional chart results:
`coordinateEta_lipschitz_z`, `coordinateEta_axis_center`, and
`coordinateEta_margin_of_axial_radius`. They compiled in the pinned upstream
Lean environment. The last theorem is conditional on an explicit scaled axial
radius bound and controls eta by `|eta0|+delta`; it does not prove that the
bound holds on the requested full space-time tube. The tube-to-sublevel,
transverse geometry, time-varying center and all-plateau obligations remain.
No new solver experiment or upstream finding is claimed. The pinned upstream
full `lake build` completed successfully with 11,424 jobs. Its replay log,
extension compile output, and `#print axioms` output for the three new lemmas
are preserved under `evidence/openai-lean-2026-09-30/`. The added lemmas depend
only on `[propext, Classical.choice, Quot.sound]`. The full build separately
warns that two Euler and two Navier--Stokes ComparatorChallenges declarations
use `sorry`; the exposed Navier--Stokes theorem declarations report only those
three standard Lean axioms. This does not imply independent review of the
source argument. The symbolic tube-geometry checker also passes under the
locked verification requirements with SymPy 1.14.0; its output explicitly
limits itself to exact identities and does not prove the full tube inclusion.
The formalization is in stacked PR
https://github.com/Unjuno/concentration-aware-ns/pull/2, based on the current
OpenFOAM runner PR branch because the support-hole extension is introduced
there. Its Python verification CI passed (run 36688606215). This is a
contribution to the benchmark repository; no defect issue was submitted to
OpenAI or a solver project because this work establishes a conditional
mathematical lemma rather than a reproducible upstream implementation defect.

### Conditional existential cusp-ball transfer, 2026-09-30

The later extension check supersedes the earlier statement above that the
whole-ball inclusion remained unformalized. The fresh pinned run
`evidence/openai-lean-2026-09-30-cusp-ball-germ-v5/manifest.json` compiles and
audits eight declarations, including `selected_axis_center_small_eventually`,
`selected_velocity_germ_on_cusp_tube`, and `exists_admissible_cusp_radius`, with only
`[propext, Classical.choice, Quot.sound]`. Under fixed strict eta-margin and
active-annulus interior assumptions, it proves existence of `tau0>0` and
local-germ equality throughout every Euclidean ball of radius `c*sqrt(tau)`
for all `0<tau<tau0`; an admissible positive radius and margin exist for every
fixed `eta∈(-1,1)`. The interval is existential and parameter-dependent;
this is not a finite-size packet result, a molecular inference, or a solver
validation. The refreshed audit and derivation are in
`reports/openai-support-hole-assembly-audit.md` and
`docs/support-hole-tube-geometry.md`.

### Full spatial-ball eta margin, 2026-09-30

`coordinateEta_margin_of_euclidean_ball` in
`verification/SupportHoleAssembly.lean` now derives the one-dimensional axial
distance premise from a Euclidean norm bound centered on the actual axis-center
formula. It proves the similarity-coordinate margin for every point in a fixed
time slice of the full spatial ball. Its companion
`transverse_radius_le_of_euclidean_ball` bounds the physical transverse radius
by `sqrt(2)*c*sqrt(tau)`. The pinned Lean compile and axiom audit passed; see
`evidence/openai-lean-2026-09-30-spatial-ball-transverse/manifest.json`. These
discharge the ball-to-eta and transverse-radius steps. Exterior-domain, cutoff
and localization conditions and the full moving-tube transfer remain open.
No particle-position or molecular conclusion follows.

At the September 28 source-run snapshot, four of six cases were complete and
`n64-dt0.0005` was partial. That attempt is retained in place. The newer
September 30 cross-run status index below supersedes its completion count;
previous host PID observations are stale and are not treated as current
container state.

## 2026-09-30 initial temporal addendum snapshot — superseded

The original September 28 v2 manifest remains unchanged as a source-run
snapshot. The separate `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`
joined the four original complete cases with the independently archived
`n=64, dt=0.0005` case. At that snapshot, the quarter-step row and AMR cases
were still unrun. A later same-day addendum completed the `dt=0.00025` row and
the separate three-budget AMR/remap controls. The authoritative current index
is `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`; the
current cross-solver scope and remaining limitations are in
`reports/solver-matrix-coverage-2026-09-30.md`. The original partial attempt
and this earlier status record are preserved as historical evidence.

## 2026-10-01 current analytic and upstream-scope addendum

The pinned Lean extension now proves a selected-field equality ball of radius
`c*sqrt(1-t)` and transfers the actual-base full-spacetime Hessian rate
`C2*q^(-40)` throughout that ball on an existential terminal interval. The
October 1's `verification/SpatialHessianTransfer.lean` now composes that
full-spacetime estimate with a fixed-time spatial restriction and provides
`C2*q^(-40)` for the spatial Hessian on the same ball. The helper and composed
theorem passed Lean elaboration and axiom audit; details are in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`. The
classical nonlinear packet estimate remains separate, so `Cstretch+39` and
its conservative `Q^43` specialization are analysis-level conditional
shrinking-packet allowances with non-effective constants, not a fixed-size
packet theorem. The earlier full-spacetime theorem's ten-declaration axiom
audit remains in
`evidence/openai-lean-2026-09-30-cusp-hessian-v6/`.

The October 1 GitHub issue/PR inventory is recorded in
`reports/upstream-status-2026-10-01.md`. PhysicsNeMo issue #2001 already covers
periodic-only grid-gradient behavior on non-periodic domains; this benchmark
uses a periodic domain and autograd. Issue #2007's odd-width spectral behavior
does not touch its even-width outputs. A successful MLP import smoke on the
pinned environment does not replace the separate #1990 reproducer. No new
upstream report is warranted by the present evidence.

## 2026-10-01 follow-up literature: analytic forcing

Constantin, Ignatova and Vicol's [arXiv:2609.20803](https://arxiv.org/abs/2609.20803)
proves regularity near the proposed singular point under its stated anisotropic
Type-II bounds, exact axisymmetry in a collapsing core, and spatially analytic
forcing assumptions. Version 2's Appendix A crosswalks the Type-II, core,
force-regularity and pure-swirl/axis-value properties to the OpenAI manuscript
and explicitly disclaims verification of the construction's correctness. Our
separate note checks the implication chain and identity-theorem deduction
against both primary texts. Conditional on the cited properties and claimed
singularity, analytic forcing is excluded and the force is not identically
zero on neighborhood cylinders; the independent pure-swirl route excludes
common spatial analyticity on specified slabs without the blow-up hypothesis.
Neither route bounds force amplitude or establishes physical actuation,
particle alignment, viscosity change, or a solver defect. See
`reports/openai-analytic-forcing-bridge-2026-10-01.md` and
`evidence/openai-analytic-forcing-v2-audit.json`. OpenAI Lemma 10.2's zero
endpoint jets plus its smooth extension make the force flat at the point;
combined with conditional nonvanishing on every surrounding cylinder, this is
a flat-at-the-point but locally active force. It still supplies no positive
amplitude lower bound.

## 2026-10-01 independent archive replay

The targeted replay suite was rerun from `work/reference-check-env`. OpenFOAM's
four original time-series archives match the frozen schedules; SU2's five
diagnostic records replay exactly, with temporal order `0.99916` still
uncertified due to per-step residual misses; all five AMR/remap archives pass
hash/tree verification; and PhysicsNeMo's five saved checkpoint/evaluation
pairs match their run archives. PhysicsNeMo derivative comparisons remain
sample-only, not continuous-extremum bounds. No solver was rerun. The full
results and scope limits are recorded in
`reports/solver-matrix-coverage-2026-09-30.md`.

## PhysicsNeMo continuous-peak certificate feasibility

The new exact-rational global Hessian cover audit processes all 25 frozen
checkpoints and saves per-case weight/archive hashes and bounds in
`evidence/tests/physicsnemo-global-hessian-coverage.json`. Under a hypothetical
5% comparator, even a perfect-sample uniform-grid Lipschitz cover would need
at least 9,465–13,743 nodes per axis under this envelope, so it is not a practical
continuous-error certificate. Eight-point autograd checks sanity-check the
network envelope but do not certify it; the analytic inequalities provide the
bound. The illustrative threshold is not PhysicsNeMo-preregistered and no
acceptance status changes. Review found and corrected an input feature-order
error in the first envelope; its old bounds are withdrawn. The checker now
validates the frozen source expression and the regression suite covers the
actual grouped sine/cosine mapping. A corrected optimistic floor uses an upper
bound on the reference peak and lower bound on pi; local interval subdivision
remains untested.

## External verification-method update

An arXiv preprint submitted 2026-09-14 claims all-time smoothness for named
families of periodic initial data using finite Fourier comparison paths and
exact-arithmetic a-posteriori enclosures. It is a bounded-family result, not
global regularity for all data and not a direct counterexample to the distinct
forced blowup claim. The preprint says a reproducibility archive will be
created before journal submission; no such package is linked from its current
arXiv record, so we have not independently checked its proof or code. The
proof architecture may inform local/adaptive whole-domain coverage for our
continuous-peak question, but the theorem itself does not transfer to our
manufactured case. See
`reports/recent-navier-stokes-verification-developments-2026-10-01.md`.
The OpenAI source repository also has both Issues and Discussions disabled,
so the planned upstream issue round has no GitHub issue/discussion route there.

## 2026-10-01 actual-profile pressure provenance

The new isolated Lean extension `verification/ActualProfilePressureProvenance.lean`
proves both (a) existence of a complete `ProfileData` arising from the prepared
outgoing construction with core amplitude `P >= 2`, and (b) only `P > 0` for
the separately selected `FinalSlowBase.actualProfile`. Both proofs use only
`propext`, `Classical.choice`, and `Quot.sound`; the pinned checker log is
`evidence/lean-verification/actual-profile-pressure-provenance-2026-10-01.log`.
This is not a counterexample: it does not show that the selected amplitude is
small, only that the existential construction bound is not currently carried
through the record used by the classical selection. Consequently the
`b >= 9/40` local pressure-sign premise remains unproved for `actualProfile`.
The source-backed dataflow and limits are described in
`docs/pressure-moment-threshold.md`. No OpenAI upstream report is warranted:
the evidence identifies a missing transfer theorem/data field in our extension,
not a defect or false claim in their repository.

### 2026-10-02 retained-preparation inequality follow-up

A further audit traced the retained `AxisPreparation.entrances` field. It
contains universally quantified `NaturalEntrance.EntranceProfile` records,
including `source_lower`, `slope_positive`, and `cone_margin` inequalities.
These are a concrete possible route to derive the missing lower bound, but the
final selected records still carry neither the consumed `2 <= core.P` proof
nor a `PreparedProfile`; no theorem deriving that bound from the retained
entrance inequalities was found. This is a bounded source search, not a proof
that such a derivation is impossible. Thus the pressure premise remains
conditional, and no upstream defect or physical consequence is established.
Exact pinned hashes and field-level analysis are in
`reports/actual-profile-pressure-provenance-2026-10-01.md`.

The analytic form of the retained cone test is `q + n^2/q > 9/4` in regular
source-integral coordinates, while `PressureData` states smoothness, a
negative pressure bound, and a derivative sign without naming the ideal-prefix
amplitude. The fields are still coupled through the scaled-solution and
pressure-integral identities, so this is not an impossibility result; it
identifies the missing quantitative bridge. The proof agenda and exact scope
are in the dated provenance report.

A concrete analytic countermodel closes the narrower converse from generic
pressure hypotheses: for any `0 < B < 2`, retain the ideal prefix
`g(y)=B^2 exp(y/5)` on `y<=0`, add nonnegative exponent-zero schedule mass `2`
on `[1,2]`, and use exponent one on the prefix. The resulting pressure is
`-1-(5/2)B^2(1+eta^2)^(-2)`, meeting both `PressureData` sign conditions despite
`B<2`. This proves only that generic admissibility plus `PressureData` cannot
recover the prefix threshold; the construction does not satisfy the selected
schedule/entrance fields and is not a counterexample to `actualProfile`.
The exact SymPy replay and isolated regression test are
`tools/check_pressure_data_amplitude_countermodel.py`,
`evidence/tests/pressure-data-amplitude-countermodel-2026-10-02.json`, and
`tests/test_pressure_data_amplitude_countermodel.py`; the check is included in
`tools/replay_published_reports.py`. Interpretation limits are in the dated
provenance report.

The pinned selected schedule also has a zero-exponent tail after
`flattenEnd`; its pressure-integral contribution is independent of `eta`.
The tail weight remains coupled to `TailData`, so this does not instantiate
the abstract countermodel. It identifies a focused next proof target: bound
the tail mass relative to `core.P^2`, or establish the root-pressure condition
directly from the retained schedule. The eta-independence identity is
Lean-checked with an explicit axiom audit; source hashes, replay command, and
scope are in `evidence/lean-verification/selected-schedule-tail-pressure-2026-10-02.json`.

### 2026-10-02 source-schema follow-up

Rehashed `PreparedOutgoing.lean`, `NominalConeAssembly.lean` and
`FinalSlowBase.lean` in the isolated pinned source; all three match the
2026-09-28 dataflow inventory exactly. The constructor path confirms that
`PreparedProfile.amplitude_lower` is projected away before
`FinalSlowBase.ProfileData` is formed. Its retained `AxisPreparation` includes
analytic inputs and an all-sufficiently-large-scale entrance-existence
property, so deriving the amplitude/moment threshold from every retained field
remains a possible but unproved route. The alternate pressure-qualified
selection still does not identify with `actualProfile`. No counterexample or
new conclusion about the fixed candidate was obtained, and no upstream defect
or physical consequence is inferred. Details and hashes are in
`reports/actual-profile-pressure-provenance-2026-10-01.md`.

The concurrent OpenFOAM run-status correction was checked against
`evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`: the six-case
uniform-grid matrix is complete. Its historical n64/dt=0.0005 partial attempt
was superseded by the separately archived 100/100-step run. It is not evidence
against or in favor of the completed matrix result.

## 2026-10-01 uniform pressure-threshold Lean closure

`AxisForceSign.lean` now machine-checks the rational small-parameter estimate
`b >= 9/40` sufficient for the outgoing root's `Z > 0` condition. It connects
that estimate to the constructed outgoing pressure integrals and proves that at
least one complete `FinalSlowBase.ProfileData` and its natural-axis root have
`Z > 0`. The three added theorem axiom reports contain only `propext`,
`Classical.choice`, and `Quot.sound`; the full output and source hashes are in
`evidence/lean-verification/pressure-threshold-uniform-2026-10-01.json`.
This is existential. The selected `actualProfile` amplitude premise remains
open, so the actual-profile local sign and strict negative-ratio conclusions
remain conditional. No molecular or constitutive claim follows. Details are in
`reports/pressure-threshold-lean-audit-2026-10-01.md`.

## 2026-10-01 literature-source update

The arXiv metadata for Lei–Ren Part I (arXiv:2609.35406, v2) describes an
exposition of the OpenAI profile construction and explicitly defers oscillatory
pulse residual correction to a companion Part II; its comments say it will not
be submitted to a journal. We checked only metadata/abstract. It is a helpful
new explanatory source, not independent verification of the entire construction
or peer review. No benchmark or physical-hypothesis verdict changes. See
`reports/recent-navier-stokes-verification-developments-2026-10-01.md` and
`evidence/upstream-refresh/lei-ren-profile-part1-2026-10-01.json`.

## 2026-10-02 physical follow-up reread

Duraiswami's arXiv:2609.17642 was reread through its reduced profile method,
admissibility-cone discussion, and physical-cutoff estimates. It reports that
the tested smooth reduced profiles fail the cone, while explicitly leaving out
the full construction's pulse annulus and higher-order terms; this is not a
counterexample to that full mechanism. Its illustrative water and air estimates
place cavitation/compressibility before molecular scales, and its tracer-motion
discussion distinguishes profile collapse from material-line winding. These are
model-dependent order-of-magnitude estimates, not measurements or a complete
forced-flow simulation. They do not negate the separate infinitesimal
tangent-direction alignment calculation and do not establish molecular order
or a viscosity transition. See
`reports/recent-navier-stokes-verification-developments-2026-10-01.md` and
`evidence/upstream-refresh/duraiswami-physical-followup-2026-10-02.json`.

## 2026-10-01 linearized-flow volume check

The Lean extension now proves the scale-volume factor of the selected
rotation/stretch variational map is one and separately checks preservation of
the isotropic Gaussian covariance eigenvalue product. Both new declarations use
only the three permitted standard axioms. This formalizes the linearized
volume-preservation step behind the existing Gaussian argument; it does not
formalize its probability tail bound or extend it to nonlinear finite packets or
molecules. Evidence is in `evidence/lean-verification/axis-volume-covariance-2026-10-01.json`
and interpretation limits in `reports/linearized-flow-volume-audit-2026-10-01.md`.

## 2026-10-01 pressure-qualified alternative profile selection

`verification/QualifiedProfilePressure.lean` constructs a new complete
`FinalSlowBase.ProfileData` selection through the prepared outgoing amplitude
bound, nominal cone certificate and modulation witness. It proves `P >= 2`
for that selected record and `Z > 0` at its natural-axis root. The isolated
checker exits 0; the new declarations use only `propext`, `Classical.choice`,
and `Quot.sound`. This is an alternate selection and does not prove the sign
for the upstream fixed `FinalSlowBase.actualProfile`; it also yields no
molecular, phase-transition, viscosity-law, blow-up, or solver-defect result.
No upstream report is justified. Details and replay evidence are in
`reports/qualified-profile-pressure-selection-2026-10-01.md` and
`evidence/lean-verification/qualified-profile-pressure-2026-10-01.log`.

The same extension now also proves a finite limit for `nu * spatialLaplacian /
materialAcceleration` along the selected slow-base material curve and a strictly
negative value at its pressure-qualified root (`slow_base_viscous_acceleration_ratio_limit`,
`exists_qualified_slow_base_negative_ratio`). A third theorem,
`exists_qualified_slow_base_ratio_magnitude_limit`, proves that the magnitude of the
magnitude of this ratio tends to a strictly positive constant. The isolated
replay exits 0 and these declarations have no `sorryAx`. Thus this ratio does
not tend to zero for the selected field. The result is still only about the
alternate slow-base selection: it is not transferred to
`FinalSlowBase.actualProfile` or the completed periodic field and does not imply
molecular ordering, a phase transition, constitutive viscosity loss, blow-up,
or an upstream solver defect. No upstream report is warranted.
The source equation also includes pressure and forcing in the momentum balance;
the slow-base ratio is not a viscosity-share measure and the arbitrary `nu`
multiplier does not rebuild a solution at another viscosity. A live upstream
metadata recheck still matches the pinned source and is recorded in
`evidence/upstream-refresh/openai-live-recheck-2026-10-01T0808Z.json`.

## 2026-10-01 integrated published-evidence replay

`tools/replay_published_reports.py` now directly rechecks the OpenFOAM uniform
fixed-step schedules, its n=64 three-dt comparison, all five AMR/remap archive
trees, OpenFOAM stencil/Arb derivative checks, the SU2 localized source-lag
audit, the SU2 standard review, and the PhysicsNeMo sampled-derivative links.
The full one-command replay completed 34/34 steps. Its test step reports 165
passed, 1 skipped and 5 subtests passed. The generated summary keeps exact local
argv plus a portable `python3` replay command for every step; output and hashes
are in `evidence/report-replay/summary.json`. These checks do not rerun the
solvers or train PhysicsNeMo. The Arb step bounds only the named trigonometric
reconstruction, not the OpenFOAM finite-volume field; no solver-quality verdict
was promoted.

### 2026-10-01 odd-grid and alias-boundary adversarial checks

The interpolation helper's FFT-bin map previously assigned the highest
positive mode on odd grids to an out-of-range negative frequency. The archived
audit cases are all even-sized, so this did not change their coefficient
bounds; odd/even bin tests now cover the mapping. The analytic reference mode
is also checked to be strictly below Nyquist before interpreting sampled
values as an unaliased reference. Five focused Arb tests and the full suite
pass (167 passed, 1 skipped, 5 subtests passed); the n=16/32/64 archived bound
values are unchanged. This expands helper robustness, not the solver-field
certificate or physical interpretation.

### 2026-10-01 linearized axis-tube probability refinement

The exact Gaussian pushforward under the selected axis variational map now
also distinguishes set-relative concentration from bounded-position certainty.
For transverse variance sigma^2 Q^C, mass within any fixed-radius tube around
the infinite axis tends to one. The axial standard deviation grows as
sigma Q^-C; for a fixed finite cylinder of radius R and half-length L, the
probability is asymptotic to sqrt(2/pi)(L/sigma)Q^C and tends to zero. SymPy
1.14.0 verifies the closed forms and limits. The statement remains conditional
on the linearized Gaussian model and does not establish a nonlinear
finite-packet flow, molecule arrangement, phase transition, viscosity change,
or solver defect. See
docs/linearized-axis-tube-concentration.md and
evidence/tests/alignment-uncertainty.json.

### 2026-10-01 analytical and AMR mapping replay refresh

The one-command published-evidence replay now includes the axis-tube
probability checker and the archived same-run AMR parent-injection analysis.
The current replay completed 36/36 steps; its full test step reports 171
passed, 1 skipped, and 5 subtests passed. The axis-tube checker records the
exact finite-cylinder formula and its Q^C asymptotic coefficient. The AMR
checker verifies the v4 archive hash and same-run preMap/mapped comparison.
These are an analytical model check and a single-event mapping-mechanism
diagnostic, not a new broad solver-quality verdict or an upstream defect
finding. No new issue or PR was submitted for either result.

The n=32 AMR same-run experiment was replicated at `dt=0.0005`, preserving the
first-map time with `refineInterval=4`. The selected count and mapped topology
match the n=32 `dt=.001` case; the DOF metrics change only slightly. This is a
fixed-first-map-time exploratory control with a changed pre-map step count and
adaptation interval, not a temporal order study. AMR quality remains
UNCERTAIN; see the dated AMR-resolution report.

The v4/v5/v6 same-run AMR snapshots now have an interior Gauss-gradient/curl
replay. With a shared physical boundary mask, gradient and vorticity pointwise
errors increase immediately after mapping at both n=16 and n=32. Same-parent
child faces carry exactly the injected constant parent `Uf`, consistent with
no newly resolved subcell slope. This diagnoses a representation limitation
for these events, not an implementation defect; the reconstructed gradient is
not asserted to be the solver's stored `grad(U)`. The n=32 archives include
only mapped face data required for replay; later face stages stay excluded.

### 2026-10-01 independent six-case OpenFOAM matrix archive replay

Added `tools/verify_openfoam_high_gradient_matrix.py` to verify the current
cross-run index against the protocol, original manifest, six archive hashes,
archived logs/configuration/endpoint fields/diagnostics, and recomputed gates.
It reconstructs the n=128 archive from its published chunks and checks both
the chunked Zstandard stream and reconstructed gzip hash. All six rows replay;
all pass standard acceptance, local quality fails at n=16/32 and passes at
n=64/128 and the two smaller n=64 time steps. The preregistered fine-grid
blind-spot verdict recomputes to `NOT_OBSERVED`. The audit and test are in
`reports/openfoam-six-case-matrix-independent-replay-2026-10-01.md`,
`evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-01.json`, and
`tests/test_openfoam_high_gradient_matrix_replay.py`. This verifies stored
evidence and the gate logic, not source/binary equivalence or continuous field
accuracy; separate AMR quality remains uncertain.

### 2026-10-01 live upstream status delta

The latest PhysicsNeMo `main` maintenance commit leaves the audited
`power_spectrum.py` Git blob unchanged; the odd-width behavior remains tracked
in issue #2007/PR #2008 and does not affect the benchmark's even-width cases.
SU2 Discussion #2890 has been closed but remains formally unanswered and
contains no fix record. The OpenAI Lean repository still has no issue or
discussion channel. The bounded live inventory is preserved in
`evidence/upstream-refresh/live-status-2026-10-01T1424Z.json`; no duplicate
upstream report is warranted by the new status alone.

The 2026-10-02 actual-profile provenance change at `e24c2b6` was exported
from tracked Git data into a fresh locked environment. All 36 report-replay
steps and six additional checks passed, with 176 tracked report/evidence files
unchanged; the full suite reported 199 passed, one skipped, and five subtests
passed. Sanitized logs and post-sanitization hashes are preserved in
[`clean-export-2026-10-02-actual-profile-audit/`](../evidence/clean-export-2026-10-02-actual-profile-audit/README.md).
This is Python postprocessing and evidence replay only. It does not execute
Lean or solver runs and does not discharge the actual-profile pressure premise
or change any scientific verdict.

### 2026-10-02 n=128 same-run AMR extension and harness provenance

The Foundation 13 n=128 first-map run completed at 6,949,888 cells. Its mapped
velocity exactly matches parent-value injection; the reported coarse/mapped
cell-DOF errors against analytic cell averages are 0.2206%/5.2451%. The within-
run two-base-cell-width interior Gauss-gradient error changes 0.6084% to 5.2472%,
but its boundary mask differs from the common-physical-mask cross-resolution
table and is reported separately. AMR quality remains UNCERTAIN; no blow-up,
particle-ordering, viscosity-change, or solver-defect inference follows. The
full run archive is preserved locally and a 15-part compact review archive is
published at [GitHub Release `of13-amr-same-run-map-v8-n128`](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-same-run-map-v8-n128);
the server-reported sizes and SHA-256 digests match all entries in the parts
manifest, and the package reconstructs locally with its recorded SHA-256. A
replay audit confirms the runner and
its three helper files match commit `e92a77e`; the startup worktree status
recorded by the runner contains only the untracked protocol. See
`reports/openfoam-amr-resolution-replication-2026-10-01.md` and
`evidence/of13-amr-same-run-map-v8-n128/harness-provenance-a1.json`.

### 2026-10-03 follow-up literature: forcing structure and finite-grid observability

Two recent arXiv preprints add useful scope constraints. Constantin, Ignatova
and Vicol's conditional theorem gives regularity under simultaneous analytic
forcing, uniform preterminal spatial `C^2`, anisotropic angular-mean bounds and
exact axisymmetry on a shrinking core; their appendix states the OpenAI
construction has the latter two properties but a smooth nonanalytic force.
Cao, Chi and Nie give force-density thresholds in specified Sobolev topologies
and a whole-space construction with identical velocity/force averages over any
fixed finite family of uniform grids despite terminal blow-up. They explicitly
do not claim failure of refinement convergence for one fixed smooth problem.
These are preprint claims we have not independently verified. They sharpen
scope and reporting limits but establish no defect in OpenFOAM, SU2 or
PhysicsNeMo, and no physical/molecular interpretation. Full source audit:
`reports/navier-stokes-followup-literature-2026-10-03.md`.

The localized force rescaling has also been differentiated explicitly:
`L^q_t Ḣ^s_x` scales as `ε^(2/q-3/2-s)`, while its pointwise amplitude,
spatial-gradient and time-derivative scales grow as `ε^-3`, `ε^-4` and
`ε^-5`. A new exact SymPy replay covers these exponents. This narrows the
engineering interpretation of force-space density but does not establish a
regularity theorem under bounded actuator constraints or independently verify
the OpenAI building block; see
`evidence/tests/force-concentration-scaling-2026-10-03.json`.

### 2026-10-03 live upstream status recheck

The GitHub API recheck confirms PhysicsNeMo issue #2007 remains open and the
related fix PR #2008 remains unmerged; the affected source blob is unchanged
at the current main SHA. SU2 v8.5.0 still resolves to the audited commit, and
discussion #2890 remains closed without a marked answer; its BDF2 follow-up is
already recorded there. OpenAI's Lean repository remains Apache-2.0 with
issues disabled and no issue entries. No duplicate or unsupported report was
filed. The response snapshot and exact details are in
`evidence/upstream-refresh/upstream-status-2026-10-03.json` and
`reports/upstream-status-2026-10-03.md`.

### 2026-10-03 correction to the retained-entrance limit audit

The coefficient witnesses in the all-scale entrance property converge to
their common reference pair at rate `O(1/Λ)`, so witness incoherence alone
does not prevent a limit argument. At `chi=0`, the reference radial profile
has zero derivative at the entrance section, making `p1` tend to zero; the
stored cone margin uses `p1 + p2²/p1`, singular in this limit, and `p2` also
depends on a shrinking angular amplitude. The joint asymptotic rate needed to
recover the pressure moment is not established. The corrected source-level
analysis is in
[`reports/actual-profile-pressure-provenance-2026-10-01.md`](../reports/actual-profile-pressure-provenance-2026-10-01.md).
No selected-profile pressure sign, solver verdict, or physical conclusion is
changed, and this correction has not been Lean-replayed.

The entrance cone has the equivalent form `q²+p2²>(9/4)q` for `q=p1>0`.
After scaling by `Λ`, any finite limits of `Λq` and `Λp2²` would obey
`R²≥(9/4)Q`; the current source audit has not derived these limits or linked
them to `Z`. Thus the reformulation sharpens the proof obligation but does not
close the actual-profile pressure gate.

The source's `reference_u_derivative` already identifies the reference shear
with `Z/L`, and `ns_error` provides its `O(1/Λ)` actual-profile error. The
remaining difficulty is the degenerate `Z=0` case: exact rescaling gives
`p2²=(2/Λ)ns²/(a²φ²)`, but no rootwise lower bound on amplitude `a` is present.
The coupled first-order fixed-point and amplitude asymptotics needed for this
case remain unproved; see the updated provenance report.

The selected normalization `C0` comes from an `eventually_atTop` threshold
for prefix-budget and separation constraints. No explicit upper bound in
terms of the scale is exposed, while the angular amplitude divides by `C0`.
The source trace therefore leaves the scale-uniform root-amplitude comparison
unverified; it does not establish that the selected threshold is large or
invalidate the pressure claim.

An isolated Lean theorem now proves there is no positive amplitude floor
uniformly over all admissible `C` above any fixed finite threshold. This
validates only the limitation of the existential/all-larger-`C` interface;
it does not characterize the one `C` selected in `actualProfile`. The exact
statement, axiom list and replay log are in
`evidence/lean-verification/actual-profile-amplitude-normalization-2026-10-03.json`.


## PhysicsNeMo live status refresh, 2026-10-03

GitHub still reports `power_spectrum.py` at blob `fb3e8cda`; Issue #2007 is
open and fix PR #2008 remains open/review-required. Against current `main`
`83d6a337`, the PR branch is two commits ahead and twelve behind, so it has
diverged from its merge base. The periodic-gradient behavior remains covered
by Issue #2001 and lower-level Issue #1852 / draft PR #1853; #1852 is stale but
open. No duplicate report was filed. Exact live metadata is in
`evidence/upstream-refresh/physicsnemo-current-status-2026-10-03T-live.json`;
see `reports/physicsnemo-live-status-2026-10-03.md`. The full local benchmark
suite passed 212 tests, one skip, and five subtests. This is not PhysicsNeMo's
own test suite, so target-runtime/full-upstream validation remains separate.

## Full local verification replay, 2026-10-03

Re-ran the complete benchmark-repository test suite on commit
`b6dde6fa5b1014f5149a4ed6ca8e8d119df3b2a3` with the locked verification
requirements. Result: 212 passed, one skipped, five subtests passed. The
exact command, macOS/arm64/Python/uv versions, lockfile digest, raw output and
log digest are recorded in `evidence/tests/full-suite-2026-10-03-b6dde6f.json`
and `.log`. This verifies the benchmark repository at that commit only; it is
not a full test suite for any of the three upstream solver projects. The PR
workflow for this same commit remains queued at the latest observation.


### Python 3.12 CI-version local compatibility check — 2026-10-03

On macOS arm64, the full benchmark suite under Python 3.12.10 passed 212 tests,
skipped one, and passed five subtests. Environment, dependency versions,
requirements digest, command, log and hash are in
`evidence/tests/full-suite-2026-10-03-py31210.json` and `.log`. This aligns the
interpreter minor version with CI but is not evidence that the hosted Ubuntu
job ran; its latest state must be checked independently.


### Nullspace algebra and deterministic archive replay refresh — 2026-10-03

The published replay now includes the symbolic cell-local divergence-free
null-sequence check and passed all 39 steps under Python 3.14.5. The full
benchmark test suite reported 213 passed, one skipped, and five subtests
passed. Every step's stored log digest matches its summary entry. Successful
zstd output no longer injects random temporary paths into the AMR replay log;
its numerical output is unchanged. This verifies the local symbolic identity
and replay machinery only. It does not prove the finite-AMR extension, the
OpenAI packet, or any solver hypothesis.

### n=128 compact Gauss replay and streaming input — 2026-10-03

Reconstructed the public n=128 review archive and reran the Gauss postprocessor.
The mapped-stage diagnostics and same-parent-face audit exactly match the
full-run record. The compact archive omits `preMap_faces.csv`, so the preMap
replay uses the centered-periodic-difference fallback instead of the full
archive's captured-face Gauss sum; the small metric difference and exact
methods are recorded in
`evidence/of13-amr-same-run-map-v8-n128/compact-gauss-replay-verification.json`.
The CSV loader now parses bounded 8,192-row chunks, and its regression plus the
full suite pass under Python 3.14.5 and 3.12.10 (214 passed, one skipped, five
subtests). Logs and environment records are in
`evidence/tests/gauss-streaming-full-suite-2026-10-03.json/.log` and
`evidence/tests/gauss-streaming-ci-python-full-suite-2026-10-03.json/.log`.
The local Python 3.12 run is not the hosted Ubuntu job; Actions for PR #4 at
`d93502c` remained queued at the latest live query. None of these postprocessing
checks validate OpenFOAM itself or imply a physical effect.

After adding the accumulated-strain Jeffery analysis, the full suite was
re-run on commit `5a2b5e2a2c9a42b68c5416acecbe42611de285c2` under Python
3.12.10: 217 passed, one skipped, five subtests passed. The new analysis's
two focused tests and exact checker also pass on that interpreter. The local
run record is `evidence/tests/full-suite-2026-10-03-py31210-after-alignment.json`
and `.log`; GitHub Actions for the same head remained queued at the latest
check, so the hosted Ubuntu job is unverified.
