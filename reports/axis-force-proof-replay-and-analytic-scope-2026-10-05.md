# Axis-force proof replay and analytic scope

**Checked:** 2026-10-05

## Exact algebra replay

Using the repository's pinned SymPy 1.14.0 reference environment,
`tools.check_axis_force`, `tools.check_pressure_moment_threshold`,
`tools.check_jeffery_axisymmetric_bridge`,
`tools.check_alignment_integrability_threshold`, and
`tools.check_alignment_uncertainty` all completed successfully. These replay
identities in their stated models; they do not prove the upstream construction
or transfer a finite-particle model to it.

The exact axial viscous-force/material-acceleration ratio remains
`-nu*Z*d/(L*A*U)` under the stated axis-root and coefficient definitions.
Strict negativity follows when `Z>0`; the exact weighted pressure-moment
threshold is checked. The source does not yet establish that threshold for
`FinalSlowBase.actualProfile`. The symbolic checker also includes cases of
opposite `Z` signs, but these are algebraic controls, not realized complete
profiles. Thus the conditional force-ratio calculation cannot support a
general claim that viscosity becomes ineffective.

For an ideal Jeffery director in spatially uniform axisymmetric strain,
alignment is controlled by accumulated strain. A rate that diverges like
`(1-t)^(-alpha)` is integrable for `0<alpha<1` and does not force complete
alignment. The selected continuum axis rate has the nonintegrable exponent
`alpha=1`, so the ideal finite-rod model predicts alignment only after adding
the assumptions that the rod samples spatially uniform strain, follows the
specified axisymmetric field, and obeys Jeffery dynamics. The source-bound
continuum derivative does not establish these finite-size premises. The
separate incompressible position bound further keeps absolutely continuous
tracer mass from concentrating in the shrinking core at fixed bounded initial
density; that is compatible with tangent-direction alignment.

## Current Lean source and preserved log

Current `verification/AxisForceSign.lean` has SHA-256
`a61600fcc260fb75c00323bb53c94d96effa24b2c4e82c66355c352fe7eb0dce`. The
preserved 2026-10-01 log
`evidence/lean-verification/axis-volume-covariance-2026-10-01.log` has SHA-256
`0cea167d85234dcb648b3bb8071af0cf6d2ce84b2f30bf0752e88c81572a4b04`; its
manifest records the same source hash. A new offline auditor verifies that
all 156 source `#print axioms` declarations have corresponding reports, all
reported axioms are among `propext`, `Classical.choice`, and `Quot.sound`, and
the saved log contains no `sorryAx` or Lean error. Its result is
`evidence/lean-verification/axis-sign-source-replay-2026-10-05.json`.

The Oct 1 manifest does not record the Lean process exit status. This proves
source-bound, complete axiom output, but not a clean-exit full-file run. The
new native attempt below likewise emitted all reports but exited abnormally.
The older
aggregate `axis-force-sign.json` records source hash
`fe989c3a279d7515b2584e82ada2632930a80299f98f502f68720ff45e2fb793`, which
belongs to a preceding source snapshot, so it must not be cited as proof for
the current bytes. The newer Oct 1 receipt is the matching saved full-file
output, with execution status unknown.

A new exact rerun attempt on Oct 5 stopped before Lean started: Docker returned
exit 125 because its content store could not read checker-image blob
`0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de`
(`operation not supported`). The attempt and full daemon output are preserved
in `evidence/lean-verification/axis-force-sign-rerun-2026-10-05.json` and
`.log`. This is an environment/image-storage failure, not a Lean counterexample.

As a fallback, the same source was run natively with the prepared local Lean
4.34.0-rc2 environment. It emitted all 156 axiom reports, and those reports
exactly match the Oct 1 source-matched log, but Python recorded return code
`-5` (`SIGTRAP`). No Lean `error:` or `sorryAx` appears, and output reaches
the final declaration, yet the abnormal process exit prevents calling this a
clean run. The native command output and execution receipt are preserved in
`evidence/lean-verification/axis-force-sign-native-rerun-2026-10-05.log` and
`.json`; the offline audit is
`evidence/lean-verification/axis-force-sign-native-log-audit-2026-10-05.json`.

## Reproduction and limits

Run the pure recorded-log check with:

```sh
python3 -m tools.audit_axis_force_log \
  --source verification/AxisForceSign.lean \
  --log evidence/lean-verification/axis-volume-covariance-2026-10-01.log \
  --manifest evidence/lean-verification/axis-volume-covariance-2026-10-01.json \
  --output evidence/lean-verification/axis-sign-source-replay-2026-10-05.json
```

Its unit tests are `tests/test_audit_axis_force_log.py`. The output verifies
stored-log consistency and exposes a recorded exit code when one is available;
it does not execute Lean, validate the source
mathematically, prove `Z>0` for the selected profile, or model molecules,
finite rods, or constitutive viscosity. Current-source execution remains
unverified at clean-exit status: Docker needs a repairable pinned checker image
or the native runtime needs to return cleanly.
