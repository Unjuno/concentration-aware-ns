# Full-horizon CFL control readiness

The original-image control is not executable on the observed runtime. Docker
context is orbstack and responds, but inspecting original image
sha256:c496fe61337ebef922bbd35d18f3a4d0f30c1524c0fc08fbcfff7b5c68d54643
returns a containerd content-store operation-not-supported error. The exact
command/response is preserved in the v1 preparation evidence. This is not an
observation timeout, a solver failure or evidence the image can be run.
No solver was started and no daemon repair/prune/restart was attempted.

The original v1 protocol and prepared inputs remain intact. A prospective v2
allows a separately identified rebuild from the pinned source/patch on a healthy
isolated runtime, with compiler/package/source/binary identities preserved.
Both CFL10 and CFL100 must then run freshly in that same image; archived old
baseline outputs cannot be paired with a new-image control. The old runtime's
transitive Ubuntu packages are not snapshot-pinned, so a rebuilt binary is not
assumed equivalent. Config/mesh identities and original quality gates remain.
The successor is a frozen execution plan, not a build or simulation result.

Exact public-tag hosted Python run 37159301543 remains queued. This runtime
failure does not block independent analytic/proof/other-project work, and the
full goal remains active. Neither the successful one-step control nor the
conditional continuous energy estimate resolves full-horizon inner convergence.

An original-image paired runner now preserves preflight failures and partial
outputs, verifies input identities before/after execution and requires 50
unique physical update IDs. Recorded CSV time/step values must match the frozen
old-time convention within an explicit absolute 1e-12 diagnostic tolerance;
this is not a proof of internal callback timing. Six focused tests pass on the
archived n32 history and five corruption controls. The actual preflight
runner rejects the unavailable original image with zero cases started.
Artifacts are under `evidence/su2-full-horizon-runner-preflight-v1`.
The runner does not yet implement the separately frozen rebuilt-image successor;
that healthy isolated execution lane still has to be established.

Successor support (source 8df1c63): `--successor-receipt FILE` explicitly
selects a new image while preserving the original prepared config/mesh checks.
The receipt must bind the frozen source, architecture and recipe hashes and
record binary, patched C++ source, package-list and compiler identities. An
actual image probe recomputes those fields before either solver starts; a
receipt alone is not accepted as runtime evidence. Both fresh runs use that
same new image, and their parameters record actual and predecessor IDs.
The original-only default still retains its image gate. Six history tests and
Python compilation pass, but the successor path has not executed on a healthy
runtime; no build, binary equivalence or solver result is claimed. A new
image build/receipt and healthy isolated capacity remain required.

Successor probe correction: the first receipt comparison iterated only over
reported fields, so an empty measured JSON could satisfy it vacuously. The
probe now requires exactly binary/source/package digests and compiler version,
valid nonempty values, digest syntax and equality. Six negative probe controls
plus one positive and the six history checks pass (13 focused tests). This
runner path was never used to claim a native successful run. Image/source
provenance beyond these actual-file measurements remains a build audit duty;
the unit fixtures do not substitute for a healthy-runtime probe or simulation.

An executable collector (`tools.collect_su2_successor_image`) now emits the
receipt from an explicitly selected immutable image ID, preserving inspect
and in-image probe stdout/stderr. It rejects mutable/malformed IDs before
Docker and emits no receipt after an unavailable image or failed/incomplete
probe. Three such input controls and Python compilation pass. Successful
image collection has not occurred; source provenance still needs the frozen
build log/checksummed inputs, and the collector explicitly does not prove it.
On a healthy isolated lane, build a separately named image from the pinned
recipe, collect its immutable ID, then use the emitted receipt for both fresh
paired cases. No shared daemon repair or original-image replacement is needed.

Actual successor build attempt: a read-only inventory showed Docker info/list
responding and no running containers. A distinct new tag and copied hash-checked
build context were used. Docker build exited 1 while resolving the fixed Ubuntu
base digest, with the same containerd operation-not-supported error. It never
reached source download/patch/compilation, emitted no image ID and started zero
solver cases. Logs/input hashes/status are preserved in
`evidence/su2-cfl-successor-build-failure-v1`. Runtime inventory success was
therefore insufficient evidence of content-store/build health. Do not repeat
this build on the same unchanged store; a healthy independent runtime is needed.
The fixed-tag hosted verification is still queued. No global goal completion
or native numerical conclusion follows from this environmental failure.

Hosted execution: run 37160281461 registered the expected frozen source
c9f0c43. Native ARM64 job 111312142060 started; setup, checkout, dependencies
and exact input preparation completed, and the frozen successor build is
in progress on an actual GitHub runner. No compiler/image/pair success is
inferred before its terminal outputs are inspected. No restart or duplicate
native dispatch is issued.

Terminal follow-up: the hosted job ended `cancelled` at 2026-10-04 04:00:12
UTC, at the configured 300-minute job limit. The frozen ARM64 image build and
actual-source probe completed, and both same-image cases started. The CFL=10
baseline reached all 50 updates and process exit 0, but only 48 steps met the
inner residual criterion. Its sampled velocity relative error is 2.277% against
the frozen 2% threshold; sampled gradient and vorticity errors are each about
11.24% against 5% thresholds. Its quality remains `UNCERTAIN` and acceptance
was not evaluated. The CFL=100 control has only initial/restart and partial
history/log files, with no completed diagnostics. Thus this is an incomplete
pair and says nothing about full-horizon CFL recovery. All downloaded runner,
image, baseline and partial-control evidence is preserved under
`evidence/su2-full-horizon-run-37160281461/`; the Actions record is
[37160281461](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37160281461).
A new run needs a better bounded execution strategy or split job budget; do
not relabel this cancellation as a numerical solver failure.

A separate reviewer (source a2336b9) recomputes diagnostics from raw completed
cases, validates the input/clock identities and rejects mixed image IDs. It
reports all-step residual convergence separately from original observed
velocity/energy/derivative thresholds. An incomplete-pair control is rejected
before field reads. This reviewer is prepared locally and is not an executed
native result or continuous peak certificate.

Continuation v3 (2026-10-04): the predecessor baseline archive was replayed
from its raw files before scheduling more solver work. The saved and recomputed
velocity, sampled-gradient and sampled-vorticity diagnostics agree within the
frozen replay tolerance; the baseline itself remains quality `UNCERTAIN` (48/50
inner-residual-converged steps, velocity error 2.277%, sampled gradient and
vorticity errors about 11.24%). The protocol binds the original artifact,
manifest, receipt, frozen input/quality protocols and build-recipe hashes.

To avoid exceeding the previous 300-minute job limit solely because the
baseline is already complete, continuation v3 runs only the missing CFL=100
case and uploads partial evidence on every exit path. It still rebuilds and
probes the ARM64 image, then requires exact equality of immutable image ID,
source, recipe, binary, patched source, installed package list and compiler
with the completed baseline receipt before starting SU2. This conservative
identity gate may stop a rebuild whose installed environment has drifted; a
build or probe stop is not a solver result. On success the split-root reviewer
replays both cases, checks the full physical update clock and process exit, and
reports residual convergence independently from all observed quality metrics.
The predecessor's seven-row CFL=100 partial remains intact and cannot count as
a completed pair. The continuation has not yet run; no solver result or
updated acceptance verdict is claimed here.

Continuation v3 execution and gate result: hosted run
[37179161618](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37179161618)
successfully prepared the inputs and replayed the historical baseline (50
updates, 48 residual-converged, quality `UNCERTAIN`). The ARM64 rebuild then
produced image ID
`sha256:3cddca9f4a9f63a8ca11da813fa8d20817dc12a7d28efc2fbed119c164a314d6`,
which differs from the historical
`sha256:4fbff71542a3fce61a65ad27edd8c1f5364b76f1a629395e75b00f8788ed3d92`.
Measured solver binary, patched source, package-version list, compiler, source
revision, build recipe and container config match, but rootfs layer digests do
not. The exact-image gate therefore rejected the continuation and skipped the
CFL=100 solver step. The 1.2 MB hosted artifact and a field-by-field comparison
are archived at
[`evidence/su2-full-horizon-control-continuation-37179161618/`](../evidence/su2-full-horizon-control-continuation-37179161618/).
This is a correct provenance rejection, not a numerical run or solver failure.

The v3 push-triggered workflow also exposed and fixed a missing parent-directory
creation before input preparation; the first attempt failed at that step and
never reached baseline replay or image build ([run
37179072835](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37179072835)).
To retain exact pairing without
relying on a non-reproducible Docker rebuild, frozen protocol v4 runs both fresh
cases in separate ARM64 jobs: the baseline job builds once and uploads a
`docker save` archive; the control job downloads and loads those same image
bytes, remeasures them, requires exact receipt equality, then runs CFL=100 and
recomputes the split-root pair review. Each job has a separate 360-minute limit.
This new two-case protocol has not yet run. Until both cases and the raw-output
review complete, the existing numerical conclusion remains unchanged.

Status update, 2026-10-04 05:45 UTC: hosted v4 run
[37180101797](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37180101797)
passed dependency installation, frozen input generation, replay of the old
50-update baseline, and the new image build/measurement. Its fresh CFL=10
baseline solver step is `in_progress`; the CFL=100 job is correctly waiting
for baseline completion and artifact upload. No fresh-case numerical result
is yet available, and the old quality verdict remains `UNCERTAIN`.

## Matched full-horizon CFL pair completed — 2026-10-04

Hosted run [37180101797](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37180101797) completed the freshly rebuilt, same-image ARM64 pair at n=32, dt=0.001, t=0.05. The baseline and control used the same immutable image ID `sha256:0efbefdedf95b5451e1a10e61b2f340382d71b3d1fea496adb7a5c14f0ecbcd7`; the workflow's image-match receipt requires image ID, source revision, architecture, build-input digest, SU2 binary, patched source, package inventory and compiler to agree. Both report 50 physical updates and exit code zero. Their recorded history CSVs pass the frozen time/update identity check.

I downloaded and ZIP-tested paired artifact 11303655387 (46,374,187 bytes; SHA-256 `e9d03067cfd251cd86055094ce5816912a5a07b3b3785da8d203516332a6b5e8`) and independently reran `tools.review_su2_full_horizon_cfl_pair` against both archived result directories. The historical baseline archive also independently replays. At CFL=10, 48/50 updates meet the inner log10 residual threshold `-10`; at CFL=100, all 50 do. But both cases fail all four frozen sampled-quality gates: velocity relative L2 is 2.277%, energy error 2.464%, gradient peak error 11.236%, and vorticity peak error 11.241%, against thresholds 2%, 2%, 5%, and 5%. The largest baseline/control absolute metric change is 5.85e-10. This pair indicates a difference in whether the per-step inner residual gate is met, not a material accuracy improvement; it does not identify a solver bug.

The complete paired raw outputs, histories, logs, immutable inputs, image-match receipts, local replay and checksums are preserved in [`evidence/su2-full-horizon-cfl-pair-37180101797`](../evidence/su2-full-horizon-cfl-pair-37180101797/README.md). The separately uploaded 725 MB baseline artifact contains the exact image tar used by the hosted continuation and expires on 2027-01-02; I retained its artifact ID and expiry, while the paired artifact retains the complete case outputs. The adjacent upstream issues [SU2 #2353](https://github.com/su2code/SU2/issues/2353) (time-dependent boundary/motion evaluation) and [#2932](https://github.com/su2code/SU2/issues/2932) (reporting residual maxima locations) do not describe this matched-pair observation. Because both quality results are unchanged and no source-level defect is demonstrated, this audit does not justify a new SU2 issue. No local-quality, continuous-extrema, or physical interpretation is upgraded.
