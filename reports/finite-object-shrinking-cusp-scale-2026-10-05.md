# Finite-object size versus the certified cusp tube

**Checked:** 2026-10-05  
**Classification:** analytic consequence of a pinned proof extension; not a
physical-particle result.

## Derivation

The source-bound Lean extension `selected_cusp_ball_actual_hessian_rate`
transfers the selected field's local germ and a spatial Hessian estimate onto
an entire Euclidean ball of radius `c*sqrt(tau)` around the selected axis
center, for each fixed admissible construction parameter and some `c>0`.
Its terminal interval, radius coefficient, and derivative constant are
existential. The exact Lean receipt, source hashes, and permitted axioms are in
[`evidence/openai-lean-2026-09-30-cusp-hessian-v6/manifest.json`](../evidence/openai-lean-2026-09-30-cusp-hessian-v6/manifest.json).

Set `tau=1-t`, choose a fixed reference `tau_s>0`, and write
`Q=tau/tau_s`. A finite body of circumscribed radius `a>0` centered at the
selected trajectory is contained in this certified ball only if

```text
a <= c*sqrt(tau)
  = c*sqrt(tau_s)*sqrt(Q).
```

Equivalently, whole-body containment requires
`Q >= (a/(c*sqrt(tau_s)))^2`. The ratio of body radius to certified radius is
`a/(c*sqrt(tau_s))*Q^(-1/2)`, which diverges for every fixed `a>0`. Therefore
the existing certificate does not give a spatially uniform local-field
neighborhood for any fixed nonzero body size all the way to `Q=0`. A joint
limit can remain inside this ball only if `a(Q)=O(Q^(1/2))`; to make the ratio
vanish, it requires `a(Q)=o(Q^(1/2))`.

This establishes nonuniformity of the available pointwise-to-finite-size
transfer. It does **not** establish that the actual field ceases to be uniform
outside this ball, that a finite fiber becomes misaligned, or that physical
molecules order. The ball is a certified lower neighborhood for the local
germ, not a maximal regularity radius. The conclusion is that the already
formalized infinitesimal tangent-map alignment cannot by itself establish
finite-particle alignment near the endpoint. That transfer needs a
uniform-in-size spatial estimate and a particle model on its scale.

## Reproduction and evidence boundary

The cited receipt binds the Lean-checked neighborhood to OpenAI source commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, Lean `4.34.0-rc2`, and a source
hash for `verification/SupportHoleAssembly.lean`. It records only
`propext`, `Classical.choice`, and `Quot.sound` for the audited extension. The
algebra above is the direct substitution `tau=tau_s*Q` and squaring of
nonnegative quantities; it introduces no fitted parameter or numerical
simulation.

The coefficient `c` and `tau_s` cannot be turned into a particle-size cutoff
from this evidence, because they are not effectively extracted. The inequality
is a scope boundary on the proof, not a measured cutoff for any material. No
solver gate or upstream issue status changes.
