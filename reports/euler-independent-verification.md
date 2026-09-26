# Euler independent verification — accepted at the pinned revision

Source pin: `openai/NavierStokesAndEuler` at
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.

On 2026-09-27 the separate Euler Comparator run was started with nanoda enabled,
using `runtime/lean-verification/run_updated_euler_comparator.sh`. The source
and dependency volumes are read-only except the updated checkout's `.lake`
build tree; the container has no network, two CPUs and an 8 GB memory limit.
The entry-point hashes were read from the live container and matched the local
pinned source. Checker fingerprints and the exact challenge configuration are
in `evidence/upstream-refresh/updated-euler-comparator-inputs.json`.

A subsequent live-container audit checked all 2,669 regular files from the
pinned source archive. Every file matched, allowing only the two previously
recorded local dependency configuration overrides (`lakefile.toml` and
`lake-manifest.json`). There were no missing or mismatched files. The archive
hash, overrides, observation time and scope are recorded in
`evidence/upstream-refresh/euler-live-source-integrity.json`. Generated build
files are excluded; this is source identity evidence, not kernel acceptance.

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

The separate Euler run completed on 2026-09-27 JST (2026-09-26
18:26:28 UTC), with exit code 0 after 10,591 build jobs. Both configured
theorems reported only `propext`, `Classical.choice` and `Quot.sound`.
The full log records `nanoda kernel accepts the solution`,
`Lean default kernel accepts the solution`, and the final line
`Your solution is okay!`. The recorded-result audit passed all nine checks.

Evidence: [full log](../evidence/upstream-refresh/updated-euler-comparator.log),
[execution result](../evidence/upstream-refresh/updated-euler-comparator-result.json),
and [consistency audit](../evidence/upstream-refresh/updated-euler-comparator-audit.json).
This is independent kernel acceptance of the configured Euler challenge at the
pinned revision. It does not verify our extension, resolve the actual-profile
pressure premise, or establish molecular/constitutive consequences. Human
review of definitions and physical interpretation remains a separate task.

## Recorded-result audit

To reproduce the completed recorded-result audit, run:

```sh
python3 -m tools.audit_comparator_result \
  --result evidence/upstream-refresh/updated-euler-comparator-result.json \
  --inputs evidence/upstream-refresh/updated-euler-comparator-inputs.json \
  --output evidence/upstream-refresh/updated-euler-comparator-audit.json
```

The auditor checks exit status, log hash, source pin, both named axiom reports,
configured permitted axioms, nanoda enablement and acceptance, Lean acceptance,
and the final Comparator success line. Nine unit tests exercise missing
acceptance lines, forbidden axioms, altered logs, wrong pins, invalid targets,
failed exit status and trailing failure text. Results are recorded in
`evidence/upstream-refresh/comparator-audit-tests.log`. A separate smoke check
accepted the previously completed Navier–Stokes run using its recorded
configuration. Neither that smoke check nor these synthetic tests establish
Euler acceptance. The auditor verifies recorded evidence consistency; it is
not a cryptographic attestation that arbitrary supplied logs are genuine.
