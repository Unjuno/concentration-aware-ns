# OpenFOAM six-case matrix archive replay (2026-10-01)

The current cross-run index says all six frozen OpenFOAM Foundation 13 uniform
high-gradient cases are complete. This audit checks that claim against the
archived data rather than trusting the index alone.

`tools/verify_openfoam_high_gradient_matrix.py` verifies the current-index,
frozen-protocol, and original base-manifest hashes; checks every case archive
SHA-256; reconstructs the n=128 gzip tar from the two published Zstandard parts
and checks both package and reconstructed hashes; reads the archived solver
logs, `fvSolution`, endpoint fields, and diagnostics; recomputes standard
acceptance and local-quality gates; and recomputes the declared matrix
blind-spot verdict. The archived time histories have 50, 50, 50, 50, 100, and
200 steps respectively. All six pass standard acceptance. The local sampled
quality gate fails at n=16 and n=32 and passes at n=64, n=128, and both finer
time steps. The predeclared n=64/n=128 persistent-blind-spot criterion
recomputes to `NOT_OBSERVED`.

Replay command:

```sh
python3 -m tools.verify_openfoam_high_gradient_matrix \
  --output evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-01.json
```

The replay output is in
`evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-01.json`, and
`tests/test_openfoam_high_gradient_matrix_replay.py` exercises the complete
published archive chain. This proves consistency of the declared artifacts
and gates; it is not an independent source-to-binary audit, a continuous
derivative certificate for the finite-volume field, an asymptotic temporal
convergence result, or a physical claim. The separate AMR quality question
remains `UNCERTAIN`.
