# High-gradient AMR verdict and provenance audit — 2026-10-02

This audit separates the observed numerical result from the strength of the
prospective-registration claim. It does not modify the protocol, run archives,
or machine gate reports.

## What the result establishes

For the three archived AMR runs, the source-backed configured standard
acceptance decision is PASS. The separately computed volume-weighted,
cell-center velocity L2 errors are 8.876%, 32.070%, and 38.572%, each above
the 2% threshold. The bounds include only the stated `1e-12` numerical
roundoff allowance. Thus `local_quality=FAIL` is valid for this named discrete
metric and these archived cases. `hypothesis=REPRODUCED` denotes that
scoped acceptance/local-error discrepancy, not a general solver defect.

This does not establish comprehensive AMR quality. Energy, peak-gradient,
peak-vorticity, and shell-spectrum upper error bounds are unavailable; the
peak metrics also lack validated continuous-domain bounds. Overall AMR
quality therefore remains UNCERTAIN. The three cases share a coarse `n=16`
initial mesh and confound initialization, interpolation, sensor, and adaptation
schedule. No OpenFOAM upstream defect follows from these results.

## What the chronology establishes

The parent `protocols/high-gradient-of13-v1.json` (including the 2% velocity
threshold) and general `protocols/of13-amr-v1.json` (including base mesh,
budgets, interval, and maximum level) occur in repository history before this
AMR campaign. The high-gradient AMR protocol file is preserved and its SHA256
is recorded in the matrix manifest. The manifest records creation at
`2026-10-02T04:46:03.847446Z`; the high-gradient-specific AMR protocol first
appears in tracked Git history in commit `62c1b29` at
`2026-10-02T06:12:12Z` (times as recorded by Git and the manifest).

That ordering means tracked repository history alone cannot verify the report's
claim that the exact sensor/settings file was recorded before execution. The
file could have existed locally before it was committed, so this is a gap in
independent provenance, not evidence of post-hoc manipulation. Archived
`parameters.json`, generated inputs, logs, endpoint fields, and hashes still
make the executed configurations and metric calculation auditable. They do not
prove when the exact protocol was frozen.

Accordingly, preserve the machine result and classify the discrete velocity
threshold failure as reproduced for the archived runs. Keep overall AMR quality
UNCERTAIN, and mark prospective registration of the exact high-gradient AMR
sensor protocol unverified. Do not upgrade the claim to an upstream defect or
to a general acceptance blind spot.

## Next discriminating evidence

For a future campaign, commit the complete protocol and its hash in a manifest
before launching runs, emit that hash in each run's `parameters.json`, and
record start/end timestamps from the runner. To isolate the observed error,
compare a non-refined `n=16` run with cap-4096, measure conservation across the
first refinement event, and repeat the same adaptation schedule from a better
resolved base mesh. Keep these as new cases; do not overwrite the current
archives.
