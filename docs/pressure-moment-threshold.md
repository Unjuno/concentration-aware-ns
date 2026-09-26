# Pressure-moment route to the root sign

Scope: source pin `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`.
This is an exact algebraic reduction, not a proof of the remaining bound for
`FinalSlowBase.actualProfile`. The root identity is now also checked in Lean;
the subsequent inequalities retain the scope stated below.

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

## Why the cone inequality alone does not select the axial sign

At the same source pin, `ActivationContinuation.lean:23-30` defines

```
S = a*(1+(b/a)^2)
P = p+q*b/a
J = q-p*b/a
Relaxed = (a>0) and (P>2) and (S<coneBound(P,J)).
```

Here P denotes the projected stress coordinate, not the pressure datum.
`ConeAlgebra.lean:17` defines
`coneBound(P,J)=P+J^2/4-|J|*sqrt((P-2)/2+J^2/16)`.
Under `(b,q) -> (-b,-q)`, S and P stay fixed, J changes sign, and coneBound
stays fixed. The extra true-cone inequality S>2 also stays fixed. For example,
(a,b,p,q)=(1,2,2,4) and (1,-2,2,-4) both give S=5, P=10, J=0 and bound=10.
Thus those coordinate inequalities alone cannot determine the sign of b.

This loss of sign information also appears explicitly in
`NaturalEntrance.ns_separated` (line 779): its hypothesis separates |Z| from
zero, and its conclusion bounds |ns| away from zero. The subsequent cone-size
estimate uses a squared second coordinate. It supplies no Z>0 conclusion.

`python -m tools.check_cone_sign_symmetry` checks four exact identities and
both rational coordinate examples; results are in
`evidence/tests/cone-sign-symmetry.json`. This excludes the shortcut of inferring
an axial sign from the bare cone inequalities. It does **not** construct two
complete profiles, establish symmetry of the full PDE assembly, or show that
all retained conditions together fail to determine the sign. Additional
pressure/jet relations could break this coordinate symmetry. The unresolved
step must use such relations or the pressure-qualified witness, rather than
cone membership alone.


## Formal root identity

`ConcentrationAware.root_pressure_moment_identity` proves the displayed identity
against the upstream `NaturalAxisData.Z` definition. It assumes the root
equation, nonzero A and d, and the two pressure-moment formulas. The algebra
is therefore formally connected to the correct source definition. Instantiating
those formulas with the outgoing integrals and establishing their quantitative
lower bound are separate obligations. Both source-pin extension runs pass
145 axiom reports using only propext, Classical.choice and Quot.sound; the
five verifier fault tests pass. This extension was not checked by nanoda.


## Actual outgoing integral instantiation

`outgoing_root_pressure_moment_identity` now replaces the two abstract pressure
jet hypotheses with the actual outgoing integrals. It uses `axisDatum_eq`,
`SchedulePressure.axisPressure_eq`, and `PressureDatum.deriv_pressure` under
the schedule's proved admissibility. The statement holds for any outgoing
profile with the specified root and nonzero A,d, including the outgoing
profile contained in the selected `ProfileData`. It does not change that
selected witness. Both source-pin checks pass 146 axiom reports with only
the allowed standard axioms; all five verifier fault tests pass.

This supersedes the earlier unperformed integral-instantiation obligation.
The quantitative lower bound on the resulting moments remains unproved.
Neither this identity nor the existing cone inequalities establish Z>0 for
the actual profile without that additional step.
