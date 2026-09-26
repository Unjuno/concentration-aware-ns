# Pressure-moment route to the root sign

Scope: source pin `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.
This is an exact algebraic reduction, not a proof of the remaining bound for
`FinalSlowBase.actualProfile` and not a new Lean theorem.

The outgoing pressure is not an arbitrary negative jet. In
`NavierStokes/SchedulePressure.lean`, `axisPressure_eq` identifies it with
`PressureDatum.pressure`; `admissible` establishes nonnegative integrable
clock weight g and a shape exponent a between zero and one.
`PressureDatum.deriv_pressure` (line 334) gives its derivative. Write

```
K(y,eta) = (1+eta^2)^(-2*a(y))
M0 = integral g(y)*K(y,eta) dy
M1 = integral g(y)*a(y)*K(y,eta) dy
P = -M0/2
Pprime = 2*eta*M1/(1+eta^2)
```

Thus 0 <= M1 <= M0. With A=1/2+h, D=1/2-h, d=1-eta^2,
and the root equation U=-D*eta/d, the exact numerator becomes

```
T = D/(2*d) * (1+2*D*eta^2/d)
Z = -2*A*eta * (M0 + d*M1/(A*(1+eta^2)) - T).
```

For A>0 and -1<eta<0, positivity of Z is equivalent to the weighted moment
exceeding T. This includes the derivative contribution with its correct sign.
A sufficient condition is M0>T. A necessary condition is
M0*(1+d/(A*(1+eta^2)))>T, because M1<=M0. Neither condition is asserted for
the selected actual profile.

There is also a source-based sufficient amplitude criterion. Let b denote
`outgoing.data.core.P`, to distinguish the positive schedule amplitude from
negative pressure P. `SchedulePressure.axisPressure_lower_bound` (line 180)
implies M0 >= 5*b^2/(1+eta^2)^2. Therefore

```
b^2 > T*(1+eta^2)^2/5
```

suffices for Z>0. This is a pointwise sufficient condition, not a replacement
proof of global `PressureData`. The earlier amplitude assumption b>=2 is
stronger than needed locally, but no lower bound meeting this new criterion
has yet been derived for the arbitrary selected `ProfileData` witness.
Positivity b>0 alone does not supply a quantitative lower bound.

Reproduce the exact algebra with:

```sh
work/reference-check-env/bin/python -m tools.check_pressure_moment_threshold
```

The SymPy check verifies the root identity and amplitude-threshold conversion.
Two exact rational moment controls give opposite signs while retaining the
pressure/derivative relationship. They are not shown to be realizable by the
complete outgoing, nominal and modulation construction, so they are not
upstream counterexamples. Results are recorded in
`evidence/tests/pressure-moment-threshold.json`.

Next obligation: derive a quantitative moment or amplitude bound from retained
nominal/certificate data, or carry the pressure-qualified existential witness
through the complete assembly. The present reduction narrows that obligation;
it does not identify a new material-viscosity law.

## Retained-condition audit

The selected `ProfileData` contains a `NominalProfile.Witness`. Its
`outgoing_specification` field (NominalProfile.lean:2481) carries the full
`OutgoingProfile.Specification`, not just smoothness. That record
(OutgoingProfile.lean:557) includes pressure identities and ideal-prefix
formulas, but no explicit lower bound on core amplitude b. The construction
`exists_profile_for_data` (line 594) takes any b>0, with parameter-dependent
smallness thresholds. This prevents treating that construction theorem as a
uniform numerical amplitude bound. It does not exhibit an arbitrary small-b
complete `ProfileData`, because nominal and cone conditions still have to hold.

The retained `NominalConeAssembly.Certificate` (line 1362) has relaxed-cone,
initial true-cone and outgoing true-cone conditions. `IsTrue` (line 31) means
`IsRelaxed` plus a shear-size inequality. In turn, `IsRelaxed`
(ActivationContinuation.lean:147) is stated in shear and stress coordinates;
it is not literally the moment threshold above. These field inequalities
might imply a useful bound, but an axis-limit/coordinate argument is required.
Neither positivity of a stress coordinate nor a cone certificate can be
silently relabeled as Z>0.

The nested `NaturalEntrance.EntranceProfile` (line 1096) retains source,
slope and cone-margin inequalities. Its existence theorem (line 1109) uses
a cutoff condition involving |Z|, not a direct Z>0 premise. Again, this is
an audit of explicit hypotheses, not a proof that their consequences cannot
supply the desired bound.

The inspected source hashes and declaration locations are saved in
`evidence/upstream-refresh/pressure-retained-conditions.json`. No upstream
bug or counterexample follows from this audit. The next concrete proof route
is to express the retained cone inequalities in the actual natural-axis jets
and determine whether they constrain the weighted moment above.
