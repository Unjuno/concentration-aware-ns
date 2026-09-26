# Extracting the constants needed for a packet certificate

The [packet estimate](axis-packet-bound.md) requires a spacetime tube where
the actual assembled field equals its smooth base, a tube radius rho, and a
uniform spatial Hessian bound M. This audit identifies which source results
supply existence and which data still lack numerical certificates.

Source inspection uses OpenAI commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; the added extension lemmas are
also checked against the original pin. No coefficient values or ODE trajectory
were sampled to infer the bounds.

Both source-pin runs pass 127 extension axiom reports, using only the allowed
standard axioms. The five verification-gate fault tests also pass. These are
checks of the stated lemmas and acceptance path, not numerical extraction.

## A uniform derivative bound can be transferred

`SlowBorelBase.compact_jet_bound` gives, for a smooth function on an open
domain and any compact subset K, a uniform bound for each prescribed
iterated derivative order. `FinalSlowBase.velocity_smooth` supplies smoothness
on `BaseResidual.past`, the open spacetime domain t<1.

The extension `compact_jet_bound_from_selected_base_germs` now joins those
facts to neighborhood equality: if the assembled velocity agrees locally
with that selected base at every point of compact K contained in t<1, then

    exists M >= 1, for every w in K: ||D^m u(w)|| <= M.

This is a uniform bound over K, not separate unrelated constants at its
points. Its hypothesis is neighborhood equality throughout K. Equality on
the axis alone would not supply a bound on a tube. The classical open-union
and compact-tube construction in the flow note supplies such a K existentially.

At m=2 the formal statement concerns the full spacetime derivative. Restrict
each argument to a spatial vector through the linear embedding v -> (0,v).
This embedding has norm one for the source product norm, so the same bound
controls the spatial Hessian. This restriction argument is classical here;
the new Lean lemma does not separately formalize that last composition.

## Finite-stage cutoff with a known chart lower bound

There is also a useful finite reduction. Suppose q_chart>=qmin>0 throughout
a proposed compact tube, and the natural-valued cutoff schedule a is strictly
increasing. Then a(j)>=j. Choose a natural J with J*qmin>1. For every j>=J,

    a(j)*q_chart >= j*qmin >= J*qmin > 1.

`SlowBorelBase.powerStage_jet_zero` then makes every derivative order of
that cutoff stage zero. The new extension lemma
`cutoff_stage_jets_zero_above_index` checks this implication for arbitrary
scalar coefficients, exponents and derivative orders.

Classically, on the open region q_chart>1/J the positive-stage sum therefore
reduces to the finitely many indices below J, plus the separately retained
leading profile. The extension checks the individual vanishing jets; the
complete finite-sum replacement and its chart composition are not new Lean
theorems in this change. A valid qmin must bound the chart coordinate on the
**whole tube**. Substituting its value only on the axis would leave a gap.

This reduction avoids estimating an infinite tail on a compact interval away
from t=1. It does not make the remaining coefficient functions or cutoff
scales numerically available by itself.

## Why this is not yet a numerical packet certificate

| Input | Inspected source evidence | Missing numerical content |
|---|---|---|
| Profile and modulation | `FinalSlowBase.actualProfile` uses `Classical.choice profileData_nonempty` | An executable representative or certified enclosures for the selected coefficient functions |
| Base cutoff scales | `EntranceAlignedBase.scales` uses `Classical.choose exists_admissibleScales`; `FinalSlowBase.scales_spec` retains admissibility | Values or upper/lower interval certificates for the finite active scales |
| Template derivative bound | `SlowBorelBase.exists_template_jet_bound` takes a compact continuous-derivative bound | A computed enclosure for that compact maximum |
| Physical tube | Terminal base-germ transfer and compactness give a neighborhood | Explicit radius and chart-coordinate lower bound valid throughout it |
| Finite-prefix Hessian | Finitely many smooth terms and chart derivatives | Certified derivative enclosures after composition and multiplication |

The existing `exists_cartesian_profile_tail` theorem is another possible
route, but its J, delta and C are existential and depend on admissible scales
and compact chart-derivative bounds. It is not an already available numerical
Hessian constant. Likewise the stress-weighted estimates cannot be substituted
for a velocity Hessian estimate without proving the relevant derivative link.

These are limits of the extracted evidence, not a theorem that numerical
realization is impossible. A future certificate can provide rho, qmin, the
finite active data and derivative enclosures, then use the explicit packet
inequality. At present only the existence/transfer and stage-vanishing steps
are formalized. No particular finite packet is certified, and no pressure
condition or material-viscosity conclusion follows from these bounds.

## Source anchors

- [Compact derivative bounds and cutoff jets](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/SlowBorelBase.lean)
- [Chosen scales](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/EntranceAlignedBase.lean)
- [Actual profile and smooth base velocity](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/FinalSlowBase.lean)
