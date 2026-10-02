# Analytic pressure follow-up

This follow-up replays two existing evidence paths to test whether the latest
selected-schedule tail estimate closes the actual-profile pressure gap.

The locked SymPy 1.14.0 check reproduces the exact root identity

`Z = -2*A*eta*(M0 + d*M1/(A*(1+eta^2)) - T)`

and the sufficient amplitude-squared threshold. Its two rational moment
controls give opposite signs while respecting `M1=M0`; they are algebraic
controls, not examples realized by the pinned full profile construction. The
archived result remains `evidence/tests/pressure-moment-threshold.json`.

The independent nanoda check of the selected-schedule tail extension verifies
a conditional bound on the negative pressure contribution of the flattened,
zero-exponent tail. That bound is not a lower bound on the total positive
moment `M0`, nor does it establish a positive weighted root moment. In the
root identity, the full moments include the entire schedule; the tail has
zero `M1` but contributes positively to `M0` (equivalently, negatively to the
signed pressure). Therefore the `-P^2/100` tail-pressure bound does not close
the sign condition, and must not be read as a pressure-sign result.

The extension also proves the equivalent nonnegative-mass statement for the
existential rate-capped full `ProfileData`:

`integral_{flattenEnd}^∞ clockWeight(y) dy ≤ P^2/50`.

Here `P` in the Lean statement is `d.core.P`, the positive outgoing core
amplitude. It is not the signed pressure function `p(eta)`; the latter is
negative under the construction's pressure convention. The mass bound is
therefore relative to the squared core amplitude.

This upper bound uses the constructed witness's exact wait identity and lambda
cap. Independent nanoda checked 64,192 declarations with zero typechecker
errors, found the six selected declarations, and reported one pretty-printer
limitation (`Unable to print axioms`). The permitted source-side axioms remain
`propext`, `Classical.choice`, and `Quot.sound`. Run hashes and checker details
are in `evidence/lean-verification/selected-schedule-tail-mass-nanoda-2026-10-02.json`;
the raw 612 MiB export remains local under `work/` and is SHA-256 indexed.

The capped witness is existential and is not identified with
`FinalSlowBase.actualProfile`. The mass bound neither asserts concentration in
the tail nor supplies a lower bound on the pressure moment needed for the root
sign. It does not resolve the actual-profile provenance gap.

The fixed OpenFOAM archive verifier again passes integrity and gate replay for
all six frozen cases. Standard acceptance passes all six; sampled local
quality fails at n16 and n32 and passes for n64/n128 and both finer n64 time
steps. The preregistered blind-spot conjunction remains `NOT_OBSERVED`. This
is postprocessing replay, not an independent solver-source proof or physical
validation.

At the first report checkpoint, PR #4 was open and mergeable at
`7b5eda976733b6d34ed5061fda1b498ab8864e5a`, and run `36935724453` was queued.
The later tail-mass result is committed at `85b2a8456b5fe4934319a33c3c320c3dc8c50c23`;
the PR remains open/mergeable and Actions run `36936557714` was queued at the
latest check. A fresh GitHub API read on 2026-10-02 still reports upstream
`openai/NavierStokesAndEuler` at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`,
Apache-2.0, with Issues and Discussions disabled and zero issue records, so
there is no suitable upstream issue channel for this non-defect analytic
extension. The `actualProfile` pressure/moment bound remains open.
