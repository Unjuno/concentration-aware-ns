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
