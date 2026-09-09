# OpenAI Navier–Stokes independent verification

The pinned NavierStokes challenge completed with exit code 0. Comparator reports
`nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`,
and `Your solution is okay!`. The final success follows the configured comparison.

Target commit: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
Targets are `NavierStokes.Comparator.navier_stokes_breakdown_R3` and
`NavierStokes.Comparator.navier_stokes_breakdown_periodic`.
Permitted axioms are `propext`, `Quot.sound`, and `Classical.choice`.
The challenge configuration enables nanoda. Both theorem dependency displays
contain only those three axioms.

The complete terminal log and its SHA-256 are preserved in
`evidence/lean-verification/comparator-ns-result.json` and the referenced log.
The executed runner is `runtime/lean-verification/run_comparator_volume.sh`.
It uses the previously recorded pinned toolchain and checker binaries, a native
Docker volume, non-root execution, read-only sources, network isolation and the
recorded Unix-socket seccomp wrapper. Earlier resource and ownership failures
remain archived; this successful run supersedes their execution status, not their
historical evidence.

This verifies acceptance of these formal targets under the recorded checker
configuration. It does not establish that molecular alignment follows, validate
physical continuum assumptions, or constitute an independent check of the Euler
challenge. The benchmark's SU2 resolution/time-step matrix remains incomplete.
