# Rejected historical-baseline continuation

Workflow [37179161618](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37179161618)
successfully replayed the archived baseline, prepared the frozen inputs, and
built/probed the ARM64 successor image. It stopped at the exact image-identity
gate before the CFL=100 solver step. The uploaded raw artifact is
[11294596244](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37179161618/artifacts/11294596244),
SHA-256 `bbc9629df3c801b9baf0de65c068037ce2d37e1a051db81abd22849d2fc383ca`;
the downloaded contents and a structured comparison are stored alongside this
file. The runner's raw Docker build log is preserved byte-for-byte as
`image/build.log.gz`; its decompressed SHA-256 is
`dc5aedd6bc519dd2dbd1b149afcceb2f6dbbc5b39d92de6bef39a489ed83dd0f`.
The workflow-prepared input files were independently byte-compared with the
frozen historical inputs; all six files match and their hashes are recorded in
`image-identity-comparison.json`. The original mesh/config/parameter files are
retained under `evidence/su2-full-horizon-run-37160281461/inputs/`, so duplicate
3.8 MiB mesh copies are not committed here.

The historical image was `sha256:4fbff71542a3fce61a65ad27edd8c1f5364b76f1a629395e75b00f8788ed3d92`.
The rebuild was `sha256:3cddca9f4a9f63a8ca11da813fa8d20817dc12a7d28efc2fbed119c164a314d6`.
The measured SU2 executable, patched source, installed package-version list,
compiler, upstream source revision, and recipe hashes matched. The Docker
image IDs and root filesystem layer lists did not; image configuration did
match. The frozen continuation required exact image identity, so rejecting
this control was the correct outcome. It is a provenance stop, not a solver
failure and not an accuracy result.

The previous seven-row CFL=100 partial remains a separate incomplete record.
Protocol v4 starts both CFL values afresh on one newly built image, saves that
image as an Actions artifact, and loads the exact image archive in a second
runner before executing CFL=100. This prevents rebuilding between matched
cases. See `protocols/su2-n32-full-horizon-cfl-matched-rebuild-v4.json`.
