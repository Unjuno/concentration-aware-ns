# High-gradient OpenFOAM v2 run status

Run started 2026-09-28 against the frozen protocol
`protocols/high-gradient-of13-v2.json` using source commit
`0e0288f98209f856931352ebfa5dad0f1aad0014` and container image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`
(`linux/arm64`). The exact commands, generated case inputs, raw logs, endpoint
fields and per-case diagnostics are archived under
`evidence/of13-high-gradient-v2/`. Archive hashes and the run-environment
manifest are in its `manifest.json`.

## Completed cases at the snapshot

| Grid / time step | Standard acceptance | Local quality | Main observed errors |
|---|---|---|---|
| n=16, dt=0.001 | PASS | FAIL | velocity L2 8.88%; gradient peak 37.0%; vorticity peak 33.5% |
| n=32, dt=0.001 | PASS | FAIL | gradient peak 10.3%; vorticity peak 9.18% |
| n=64, dt=0.001 | PASS | PASS | velocity L2 0.478%; gradient peak 2.64%; vorticity peak 2.35% |

All three cases reached the requested end time and recorded 50 PIMPLE-converged
steps. The n=16 and n=32 derivative discrepancies are classified as
underresolution: before execution, the reference-only periodic FD2 audit
predicted that those grids exceed the 5% derivative thresholds. The n=64
case, which clears that stencil-floor condition, passes every preregistered
local-quality threshold. These coarse-grid failures do not reproduce an
acceptance blind spot or establish a software defect.

## Incomplete cases and interpretation

At the manifest snapshot, n=128/dt=0.001 had entered its first physical step
and completed velocity and pressure solves in the first PIMPLE iteration, but
had not emitted a convergence record or another time-step record. Its
`log.foamRun` then remained unchanged for more than 25 minutes. The host
`docker run` client remained live, while separate Docker `top`, `stats` and
`inspect` requests did not return during the observation window. This is an
execution/runtime stall with no terminal container state: no exit code, solver
verdict, or OOM result is inferred. The active runner and incomplete case were
left intact; OrbStack and unrelated containers were not restarted or stopped.

The two n=64 smaller-time-step cases had not started. Consequently the full
spatial/time matrix is incomplete, and the persistent-blind-spot gate remains
`UNCERTAIN`. In particular, n=128 must finish and the dt triple must run before
the frozen hypothesis rule can be applied. The unarchived n=128 partial tree
remains under ignored `work/of13-high-gradient-v2/n128-dt0.001`; the evidence
manifest records its observed step count and log hash. The reusable
`tools/archive_high_gradient_openfoam.py` archives only cases whose runner exit,
step count, convergence count, `End` marker and endpoint fields all pass its
completion checks; it verifies archive contents against source files before
reporting them.

## Later live-run observation (2026-09-28 01:48 UTC)

The same original runner and Docker client PIDs remained live; no replacement
container was started. The n=128 case had reached `Time = 0.009s`, with five
outer correctors recorded for completed steps through 0.008s. The step ending
at 0.009s was still inside its PIMPLE loop at the latest log read. The previous
logged state reported cumulative `ExecutionTime = 498.94 s` and `ClockTime =
2309 s`; these are solver run counters, not a measured per-step duration. At a
later same-process observation the case reached `Time = 0.030s`, with five
outer correctors recorded through 0.029s and the next step underway. The host
runner and docker client were still live. No exit code,
completed-case archive, or quality verdict is available. The two smaller-dt
cases remain unstarted and the matrix remains INCOMPLETE/UNCERTAIN. Preserve
the partial tree and process for later observation; don't infer a solver defect
from runtime cost.

## Analytic reference follow-up

Separately, the exact high-gradient MMS identities were extended to report the
Frobenius-gradient norm and vorticity at a selected analytic point, explicitly
as lower bounds on their continuous maxima rather than asserting global
maximality. A short derivation and both replay commands are in
`docs/high-gradient-analytic-checks.md`. The symbolic identities pass, and an
independently coded Fourier evaluator agrees with direct SymPy differentiation
for velocity, full gradient, vorticity and forcing at the recorded points.
These are continuum formula checks, not solver integration or a numerical
acceptance verdict.

The older `evidence/of13-amr-v1/` sweep is not a substitute for this protocol's
AMR requirement: it used the Gaussian profile and was already classified
UNCERTAIN because source sensing, remapping and gradient reconstruction were
not separated. A dedicated high-gradient AMR runner exists at
`tools/run_high_gradient_amr.py`, but its three cell-budget cases have not run.
Run that frozen v2 sweep only after the current serial uniform-mesh runner
releases the OpenFOAM container; then compare against the v2 uniform n=64
control and preserve budget/level histories. Nonuniform-mesh spectrum remains
unavailable until a reconstruction is validated.

The spectral reference for this MMS is also now derived directly from its
finite complex Fourier coefficients and checked against resolved cell-centered
FFT samples. An initial factor-of-two coefficient error was detected by this
independent comparison and corrected; the corrected spectral tests pass. See
`docs/high-gradient-spectrum.md` and
`evidence/tests/high-gradient-spectrum.json`. This strengthens the analytic
reference only, not the in-progress OpenFOAM verdict.

The high-gradient AMR case generator now has three focused unit checks for
sensor initialization/update, dynamic-refinement limits and the minimum
refinement interval. They pass as input-generation checks only; compiled
source-hook integration and runtime mesh adaptation remain untested.

The AMR runner has since been aligned with the uniform-grid runner's engine
provenance: it honors `CANS_DOCKER_CLI` and `CANS_DOCKER_CONTEXT`, passes the
selected context on engine commands, and records the resolved CLI hash/version,
context, image ID/platform and protocol hash. `CANS_OF13_AMR_RUN_ROOT` now
provides a collision-free work-root override. The locked-dependency suite passes
85 tests, including the new AMR-root resolution test. This is runner-level
reproducibility evidence only; no v2 AMR case has run and the blocked-candidate
count remains unobserved.

## Container activity check

At a later observation the log remained at `Time = 0.041s` for roughly four
minutes, but the host runner and Docker client were still live. A bounded,
read-only `docker exec ... ps` succeeded and observed container PID 221
(`foamRun`) in runnable state, with 66% CPU and 12.9% memory reported by `ps`.
This is positive evidence of ongoing solver computation during the quiet log
interval, not an exit or runtime failure. No case verdict is available yet.


## Later completion and temporal-runner status (2026-09-28)

The n=128, dt=0.001 run subsequently completed at t=0.05 with zero runner exit,
50 time steps, 50 PIMPLE convergence records, final `End`, and endpoint U/p/C/phi
fields. Its diagnostics report standard acceptance PASS and local quality PASS.
The original case tree was archived and its members were checked against source
files; see `evidence/of13-high-gradient-v2/manifest.json` and
`evidence/of13-high-gradient-v2/README-n128-archive.md` (the 169 MiB tar is published as a checksummed, split Zstandard package because GitHub rejects a single file above 100 MiB).

The same serial runner then automatically began n=64, dt=0.0005. The partial
case has 36 `Time =` records through t=0.018, of which 35 have five-iteration
PIMPLE convergence records; the final record is an incomplete step.
`log.foamRun` last changed at 11:51:31 JST and has no final `End`; `exit.json`
and diagnostics are absent. The host runner was stopped after no solver process
was observable and the Docker client/control commands remained blocked. Docker
container removal could not be verified, so this case is INCOMPLETE with no
quality verdict. Its inputs, command and raw logs are preserved. The smaller-dt
case and all dedicated high-gradient AMR budgets remain unrun. Do not interpret
this runtime stall as an OpenFOAM solver defect or a numerical result.

## Evidence reconciliation (2026-10-03)

A later review found the retained partial-run README had overstated that the
container was absent and that Docker `inspect` returned `no such object`. The
contemporaneous runner report above is authoritative on this point: Docker
control/API requests were blocked and container removal/liveness could not be
verified. A later host process check found neither recorded PID 37980 nor
91031, but that does not resolve the historical or container state. The raw
partial logs and their hashes remain unchanged. The status JSON timestamp
`2026-10-01T22:19:05Z` is October 2 in JST, consistent with the directory
label.

## Docker observability follow-up (2026-09-28)

Read-only host checks found the original `docker run` client (PID 91031) still
waiting, but no host `foamRun` process. The case log remains unchanged at
11:51:31 JST and ends in PIMPLE iteration 5; there is no `exit.json`. OrbStack
reports `Running`. The selected Docker context is `orbstack` and points to
`/Users/taka/.orbstack/run/docker.sock`, but `orbctl doctor` reports that the
PATH-selected CLI is the Nix Docker binary rather than OrbStack's wrapper.
Several earlier `docker ps`/`inspect` requests are also still waiting. This
documents a CLI PATH inconsistency alongside an unresponsive API path; it does
not establish which caused the stall or whether the container remains alive.
No process was signalled and OrbStack was not restarted.

At 13:14 JST the same client had waited 90m44s. An explicit read-only request
through OrbStack's own CLI (`/Users/taka/.orbstack/bin/docker --context
orbstack image inspect concentration-aware-ns:of13`) timed out after 8 seconds.
A direct HTTP `GET /_ping` over the configured Unix socket returned zero bytes
and timed out after 5 seconds. `orbctl status` still said `Running`. These
checks rule out the Nix CLI path as a sufficient explanation for the API
failure, but they do not reveal the Docker engine's internal state or container
liveness. No host `foamRun` process was observable; the container process state
remains unknown.

The runner now accepts an absolute `CANS_DOCKER_CLI` override, resolves and
records the Docker context (or accepts `CANS_DOCKER_CONTEXT`), and pins that
context on every engine command. `CANS_OF13_RUN_ROOT` selects a fresh run
directory; `CANS_OF13_EVIDENCE_ROOT` selects a separate publication directory,
and archival refuses to overwrite a nonempty custom evidence directory. The next
run's environment manifest records the invoked CLI path, resolved executable,
executable SHA-256, version and context. For this host the intended explicit selectors are
`CANS_DOCKER_CLI=/Users/taka/.orbstack/bin/docker` and
`CANS_DOCKER_CONTEXT=orbstack`. A later attempt should set unique
`CANS_OF13_RUN_ROOT` and `CANS_OF13_EVIDENCE_ROOT` paths so the partial run and
published archives remain intact. The existing frozen run manifest describes
the earlier run and is not retroactively rewritten. Seven unit tests cover CLI,
context and collision-safe output path selection; the full repository suite passes 82 tests. Before any
continuation, the Docker API and this named container still need an authoritative
state check. Keep the partial case and use a fresh, collision-free run directory
if a rerun becomes safe; do not infer completion from the client timeout.

## Offline forcing-body compilation (2026-09-28)

The generated `codedFvModel` body now compiles against the repository's minimal
Foam-like C++ mock using Nix Clang 21.1.8. At 48 seeded points, time 0.037 and
N=4, its force agrees with the independent analytic evaluator to maximum
absolute error `1.3877787807814457e-17` (threshold `1e-10`). The exact compiler
path and executable SHA-256, generated `fvModels` source SHA-256 and result are
in `evidence/tests/high-gradient-cpp-mock.json`. The mock initially failed
because its vector type omitted addition/subtraction operators used by the
generated expression; adding those operators fixed the harness, after which
compilation and numerical comparison passed. This is a mock-harness correction,
not evidence of an OpenFOAM defect. The check does not include Foundation
headers, validate the live solver's source sign convention, or run a solver.
Reproduce with:

```sh
CXX=/nix/store/l32bv33wqwkj2l1y8dp5x6h9r3q9im77-clang-wrapper-21.1.8/bin/clang++ \
  uv run --with-requirements requirements-verification-locked.txt -- \
  python -m tools.check_high_gradient_cpp_mock
```

The compiler selection is now explicit and hashed in the output. Two additional
compiler-resolution tests bring the focused environment tests to nine and the
full Python suite to 85 passing tests. The API-stalled solver matrix and AMR
results remain unchanged.

## OrbStack API recheck after runner cleanup

At 2026-09-28 04:57 UTC, OrbStack still reported `Running`, while its doctor
reported that the PATH-selected Docker CLI resolves to the Nix package rather
than OrbStack's wrapper. Stale read-only `docker ps/inspect` clients were
terminated; a fresh `~/.orbstack/bin/docker --context orbstack ps` still timed
out after eight seconds, and `lsof` showed 58 file-descriptor rows for the
Docker socket. This makes the PATH mismatch insufficient to explain the
current failure, although the underlying engine cause remains unknown.

OrbStack's `vmgr.log` was last modified at 11:45 JST, before the target case's
last solver log update at 11:51 JST. Its recent history also contains a kernel
`fork rejected by pids controller` event for an unrelated container. This is a
possible shared-VM resource-pressure clue, not a causal diagnosis for this case;
the log had no later engine error that identifies the stalled request.

The preserved `n64-dt0.0005` case log is unchanged at 36 time records and 35
completed PIMPLE convergence records; it has no terminal `End` marker or
`exit.json`. The foreground `docker run` client is still present without CPU
activity. Container state therefore remains **unknown**, not confirmed stopped;
no solver restart or OrbStack restart was attempted. Hash and command details
are in `evidence/environment/orbstack-docker-hang-recheck-2026-09-28.json`.
