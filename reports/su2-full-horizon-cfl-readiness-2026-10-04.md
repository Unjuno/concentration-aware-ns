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
