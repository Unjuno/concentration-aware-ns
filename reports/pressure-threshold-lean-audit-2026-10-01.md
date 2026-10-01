# Lean audit of the uniform pressure-amplitude threshold

Date: 2026-10-01  
Upstream pin: `openai/NavierStokesAndEuler@f9e8bc5b38b6e212696e8a30e3e91517af887bbd`  
Checker: recorded `concentration-aware-ns:checker` image and read-only `cans-lean-verification` volume; network disabled.

## Result

The uniform small-parameter estimate is now machine-checked. Under
`0 <= h <= 1/1000`, `eta^2 <= 1/4000000`, and `9/40 <= b`, the exact threshold
expression is strictly below `5*b^2/(1+eta^2)^2`. The outgoing schedule uses
`shape eta = 1/(1+eta^2)`, while the actual outgoing pressure-integral lower
bound provides the corresponding prefix mass. Consequently the extension proves
`Z > 0` at the unique root for any outgoing profile whose axis parameters lie
in the prescribed small range and whose amplitude is at least `9/40`.

A stronger existential combination is also checked: the prepared outgoing
construction supplies amplitude `P >= 2`; the nominal and modulation assemblies
produce complete `FinalSlowBase.ProfileData`; and the axis theorem supplies a
root in `(-j/4,-j/5)`. Thus at least one complete profile-data/root pair has
`Z > 0`. The theorem is named
`ConcentrationAware.exists_profile_data_with_positive_root_pressure`.

All three new declarations report only `propext`, `Classical.choice`, and
`Quot.sound`. The complete extension output is
`evidence/lean-verification/axis-force-sign-pressure-uniform-2026-10-01.log`.

## Scope boundary

This closes the classical small-parameter inequality and proves the local sign
condition for an existential complete profile-data witness. It does not show
that the separate `FinalSlowBase.actualProfile := Classical.choice
profileData_nonempty` has amplitude at least `9/40`; the current selected-profile
theorem only provides positivity. It therefore does not establish a local sign
for that selected profile, nor does it independently discharge the strict
negative force-ratio result for it. The profile-data existence statement is not
a molecular model and yields no particle alignment or constitutive-viscosity
conclusion.

The exact prior witness/selection distinction is recorded in
`reports/actual-profile-pressure-provenance-2026-10-01.md`. The analytical
threshold and source integral identification are in
`docs/pressure-moment-threshold.md`.
