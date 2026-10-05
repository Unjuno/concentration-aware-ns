# SU2 shared high-gradient run 37230949147 — n16 replay

This directory preserves the completed n16 case from GitHub Actions run
37230949147 and its build log/image ID, protocol, source patch, original case
archive, full exported case files, run summary, and independent archive replay
receipt. The machine receipt is `verification.json`.

The fresh archive replay passes, while the study stays **INCOMPLETE**: only
one of five cases was available in this artifact when it was reviewed. That
n16 run exited zero and completed 50 updates, but `standard_acceptance=FAIL`
and sampled local quality also fails. Velocity and energy relative errors are
0.618% and 0.661%; sampled gradient and vorticity peak errors are 36.095% and
34.034%; spectrum L1 error is 0.664%.

The case was compared with n16 from run 37190363204. All ten archive member
paths match. Seven payload members are byte-identical; the only differing
members are metadata: the separately built Docker image ID in `parameters`
and `diagnostics`, and the ephemeral runner bind-mount path in `command`.
After normalizing those run-specific values, the full diagnostics and command
match. Thus this verifies repeatability for this one n16 case across two image
builds, not the complete matrix, continuum extrema, or an upstream defect.

Replay with the locked Python dependencies from the repository root:

```sh
uv run --no-project --with-requirements requirements-verification-locked.txt --python 3.12 python -m tools.replay_su2_high_gradient_study --root evidence/su2-shared-high-gradient-v1-run-37230949147 --output /tmp/su2-n16-replay.json
```

The original GitHub Actions artifact ID, ZIP digest, expiry and exact file
hashes are recorded in `verification.json`. The raw solver archive is stored
here so the case does not depend on Actions artifact retention.
