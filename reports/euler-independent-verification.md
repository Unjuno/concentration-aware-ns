# Euler independent verification — in progress

Source pin: `openai/NavierStokesAndEuler` at
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.

On 2026-09-27 the separate Euler Comparator run was started with nanoda enabled,
using `runtime/lean-verification/run_updated_euler_comparator.sh`. The source
and dependency volumes are read-only except the updated checkout's `.lake`
build tree; the container has no network, two CPUs and an 8 GB memory limit.
The entry-point hashes were read from the live container and matched the local
pinned source. Checker fingerprints and the exact challenge configuration are
in `evidence/upstream-refresh/updated-euler-comparator-inputs.json`.

## What this challenge asks

`Euler.euler_breakdown_R3` asserts existence of rapidly decaying smooth,
divergence-free initial data without a global smooth unforced Euler solution
in the specified finite, uniformly bounded energy class.

`Euler.exists_compact_smooth_euler_singularity` additionally asks for nonzero
compactly supported initial data, a positive finite maximal lifespan at most
one, a solution in an all-order Sobolev class, bounded energy, existence on
closed intervals exactly below that lifespan, locally bounded C1 norms and
locally finite vorticity integrals, and endpoint divergence of the C1 upper
limit and full vorticity integral. The global nonexistence clause is retained
separately in the broader smooth energy class.

These are statements about **zero viscosity and zero external force**.
Consequently they do not establish a velocity-triggered drop of a material's
constitutive viscosity, molecular alignment, or a light-fluid model. They are
also separate from this project's conditional force-ratio consequence for the
forced Navier–Stokes construction.

## Acceptance boundary

The reference challenge file intentionally contains `sorry` placeholders;
building it is not evidence that either theorem is proved. The solution module
imports a separate development and prints the axioms of its two theorems.
Acceptance requires the Comparator's final success for the configured two
targets, the allowed axiom policy (`propext`, `Quot.sound`, `Classical.choice`),
and successful Lean/default-kernel and nanoda checks. Process completion and
full logs must be inspected before claiming acceptance.

At this report revision the solution dependency build is still running.
No Euler independent-verification PASS is claimed. The previously completed
Navier–Stokes Comparator run does not substitute for this run. A successful
kernel check would still leave human review of mathematical definitions and
physical interpretation as a separate task.
