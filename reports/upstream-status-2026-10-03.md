# Live upstream status recheck — 2026-10-03

The GitHub API was queried on 2026-10-03 for the current issue, discussion,
PR, source pin and repository state. The structured responses and relevant
public comments are preserved in
`evidence/upstream-refresh/upstream-status-2026-10-03.json`.

## NVIDIA PhysicsNeMo

`NVIDIA/physicsnemo` remains Apache-2.0 with issues enabled. `main` is
`83d6a337eecfc70e215ed1978af8dba9a38580fb`; the affected
`physicsnemo/metrics/general/power_spectrum.py` blob remains
`fb3e8cda3bc7916b8e56833dda240cb74463fabb`, matching the source hash in the
prior reproduction. Issue [#2007](https://github.com/NVIDIA/physicsnemo/issues/2007)
is open with the odd-width half-cell centering diagnosis and two comments.
Fix PR [#2008](https://github.com/NVIDIA/physicsnemo/pull/2008) is open and
unmerged, based on `ff5d19d`, while `main` has advanced to `83d6a337`. This is
already tracked upstream and the benchmark currently uses even widths, so no
duplicate report was filed. The existing issue and PR are the appropriate
URLs for future follow-up.

## SU2

The audited release tag `v8.5.0` still resolves to
`12eb826f049ef7f67df974dfcb44cf36ee07c0f8`. Discussion [#2890](https://github.com/su2code/SU2/discussions/2890)
is closed, has two comments and no marked answer. Its maintainer comment agrees
with the source-time diagnosis at the cited master revision; the follow-up
records a BDF2 control on the pinned release with first-order observed behavior
in the original setup and near-second-order behavior under the existing time
shift intervention. This is a useful reproducible discussion, not a maintainer
commitment to a general fix. No duplicate issue or further comment was added.

## OpenAI source repository

`openai/NavierStokesAndEuler` remains Apache-2.0 at main
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; the repository reports
`has_issues=false`, and the all-state issue query returned no entries. The
actual-profile pressure condition in our extension remains a proof-provenance
gap, not a reproduced defect in the upstream theorem. No issue was filed.

## Disposition

This recheck changes no solver verdict and reveals no new actionable upstream
finding. OpenFOAM's AMR observations still lack a reproduced contract
violation; its separate Foundation tracker audit and limitations remain in
`reports/upstream-disposition.md` and the dated tracker record. The three
solver outcomes and all remaining proof/quality uncertainty stay bounded by
the pins and cases in the existing reports.
