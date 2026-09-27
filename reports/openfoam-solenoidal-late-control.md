# Late-time initialization intervention: execution pending

Protocol: `protocols/of13-solenoidal-late-control-v1.json`, frozen in commit
4d13fc0 before execution. The three n=64 cases use dt=0.001, 0.0005,
0.00025 and end at 0.05, with the same tighter iteration settings as the
completed original baseline. Input preparation independently checks centered
discrete divergence and confirms only `0/U` differs from baseline.

Execution uses `python3 -m tools.run_openfoam_solenoidal_control --protocol
protocols/of13-solenoidal-late-control-v1.json`. This command is already running;
do not launch it again to recover a polling timeout. Inspect the existing
process and archived exit records first.

Once complete, run `python3 -m tools.check_openfoam_solenoidal_late`.
The comparator reads six archives, verifies every expected time and outer
convergence, prepared input hashes, unchanged non-velocity inputs, and identical
cell centers. It reports same-dt endpoint field shifts and temporal difference
norm order, direction cosine and first-order defect separately for baseline
and control. It does not assign an original-MMS error score to the changed
initial-value problem. The missing-archive guard was exercised (exit 1, no
result written); the successful comparison path is not yet verified.

The early-time intervention supports sensitivity of the startup impulse to
initialization. This longer experiment tests whether the later temporal
comparison also changes. Even a change would not isolate every feature of the
projected initial velocity, certify an asymptotic limit, or establish an
upstream implementation defect. No numerical result is available yet.

## Recovery on 2026-09-28 JST

Docker became responsive, but the original session handle was missing and no
host runner or running Docker container remained. The first case had a solver
End log and endpoint fields, but no captured exit code; it is preserved as
`n64-dt0.001-unverified-exit.tar.gz`, not a validated completed run. The other
two cases were not executed by that runner. No task-issued daemon restart was
performed. See `evidence/of13-solenoidal-late-control-v1/recovery.json`.

A fresh attempt uses protocol `of13-solenoidal-late-control-v2`, the identical
solver inputs and exact image, and separate work/evidence paths. Its stopped
containers and cidfiles are retained to permit authoritative exit-status
recovery if the host runner disappears again. Preparation manifests were
revalidated before launch. The v2 runner is in progress; use
`python3 -m tools.check_openfoam_solenoidal_late --study of13-solenoidal-late-control-v2`
only after all three archives have completed. Do not mix unverified v1 output
into the complete v2 triple.

### First v2 case complete

The dt=0.001 retry completed with exit 0 and 50/50 converged steps. Retained
Docker state independently confirms exited/0 on the pinned image. Its endpoint
U and p bytes exactly match the preserved unverified-exit v1 fields; the v1
missing exit status remains missing. Archive and container evidence are in
`evidence/of13-solenoidal-late-control-v2/first-case-review.json` and `runs.json`.
The dt=0.0005 case has started. No three-case temporal conclusion is available.
