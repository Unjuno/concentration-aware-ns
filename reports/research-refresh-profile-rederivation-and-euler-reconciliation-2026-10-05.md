# Profile-construction rederivation and Euler audit reconciliation

**Checked:** 2026-10-05

## A readable reconstruction of the profile stage

Lei and Ren's arXiv:2609.35406, submitted 2026-09-28, presents a detailed,
readable reconstruction of the leading profile-construction portion of
OpenAI's forced Navier–Stokes manuscript. It describes smooth axisymmetric
profiles, a divergence-form stress plus a remainder flat to infinite order on
fixed similarity sectors, an admissible stress/shear cone, and a linear model
for the inner core. Its abstract explicitly says that cancellation of the
residual by oscillatory pulses is deferred to a companion Part II.

This is useful explanatory and cross-reference material for auditing the
construction, and a source of intermediate identities to compare against the
pinned Lean development. The authors present it as an accessible version of
the profile stage; it is not an independent end-to-end proof of the completed
Navier–Stokes theorem. In particular, the stated residual and deferred
cancellation step prevent treating this installment as a new numerical or
physical validation. It contains no molecule-resolved model or evidence for
alignment, deterministic particle positions, or a constitutive-viscosity
transition.

## Reconcile the failed integrated Lean retry with prior Euler evidence

The 2026-10-05 integrated `lean-action` retry failed while discovering the
TOML project module for Nanoda. The run's Euler axiom-audit step therefore did
not execute. This is the status of that workflow run, not the status of all
Euler evidence.

The separate pinned Euler Comparator run completed on 2026-09-26 UTC at the
same OpenAI source commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. A fresh
replay of the repository's nine-check recorded-result auditor passes: exit
status, log hash, source pin, Nanoda configuration and acceptance, both target
axiom reports, Lean acceptance, and final Comparator success. The configured
targets are `Euler.euler_breakdown_R3` and
`Euler.exists_compact_smooth_euler_singularity`; each reports only
`propext`, `Classical.choice`, and `Quot.sound`. The audit itself checks the
consistency of the preserved log/configuration; it does not rerun Lean or
Nanoda, authenticate the original container, or independently validate the
mathematics. The report at
[`euler-independent-verification.md`](euler-independent-verification.md)
records the original run and its acceptance boundary.

Accordingly, the Euler challenge has prior recorded independent-kernel
acceptance at the pinned revision, while the 2026-10-05 integrated retry is
incomplete and its own Euler step remains unverified. Neither result implies
the forced Navier–Stokes theorem's physical applicability or a molecular or
constitutive consequence.

## Sources and evidence

- Lei and Ren, [arXiv:2609.35406](https://arxiv.org/abs/2609.35406).
- OpenAI, [pinned formalization repository](https://github.com/openai/NavierStokesAndEuler/tree/f9e8bc5b38b6e212696e8a30e3e91517af887bbd).
- Prior Euler run log, inputs and result: `evidence/upstream-refresh/updated-euler-comparator.log`, `updated-euler-comparator-inputs.json`, and `updated-euler-comparator-result.json`.
- Fresh recorded-result audit: `evidence/upstream-refresh/euler-comparator-reconciliation-2026-10-05.json`.
- Integrated retry failure: [`lean-action-nanoda-toml-detection-2026-10-05.md`](lean-action-nanoda-toml-detection-2026-10-05.md).
