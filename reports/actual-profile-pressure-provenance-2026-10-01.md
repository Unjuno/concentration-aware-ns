# Actual-profile pressure-threshold provenance audit

Date: 2026-10-01  
Upstream source: `openai/NavierStokesAndEuler` at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`  
Benchmark status: analytic extension audit; no CFD run or physical interpretation.

## Question

The pressure-moment derivation gives a sufficient local sign condition when the selected outgoing amplitude satisfies `b >= 9/40`. Does the pinned construction prove this for `FinalSlowBase.actualProfile`?

## Lean result

`verification/ActualProfilePressureProvenance.lean` was compiled in the isolated checker using the pinned source volume. It establishes:

1. There exists a `FinalSlowBase.ProfileData` assembled from `PreparedOutgoing.exists_prepared`, `NominalConeAssembly.exists_certificate`, and `ModulatedProfileAssembly.exists_of_certificate` whose outgoing core amplitude is at least 2.
2. For `FinalSlowBase.actualProfile`, the currently available conclusion is `core.P > 0`, obtained from `actualProfile.outgoing.data.core.P_pos`.

Both declarations report only `propext`, `Classical.choice`, and `Quot.sound`. The exact checker output is in `evidence/lean-verification/actual-profile-pressure-provenance-2026-10-01.log`; the replay command is `runtime/lean-verification/check_actual_profile_pressure_provenance.sh`.

## Interpretation and limits

The first existential result does not transfer its amplitude inequality to the separate `Classical.choice` used for `actualProfile`. This is a witness-provenance gap in the extension. It is not evidence that `actualProfile` violates `b >= 2` or `b >= 9/40`; no counterexample or impossibility theorem was constructed. The threshold condition remains unproved for the selected profile. A possible proof route is to retain `PreparedProfile.amplitude_lower` through the certificate/profile records and define the final selection from the enriched record, or derive the weaker moment bound from the conditions already retained.

This result concerns a proof obligation in the benchmark's analysis extension. It is not an OpenAI repository defect, an upstream theorem refutation, a CFD failure, or evidence for molecular alignment or a viscosity transition. The pinned source-dataflow record is `evidence/upstream-refresh/pressure-witness-dataflow-2026-09-28.json`; the exact pressure threshold and earlier limitations are in `docs/pressure-moment-threshold.md`.

## Upstream disposition

The OpenAI repository has Issues and Discussions disabled in the October 1 inventory. No upstream report was submitted. Even if a channel existed, the current result concerns how our extension carries a witness, not a demonstrated error in upstream source or theorem.

## Related run-state correction

The current OpenFOAM six-case matrix remains complete according to `evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json`. The historic n64, `dt=0.0005` partial attempt is superseded by its archived 100/100-step completed rerun. No matrix verdict changes.
