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
