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
