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

## Status note (2026-10-02)

The immutable original `evidence/of13-high-gradient-v2/manifest.json` is a
historical base-run record and still shows only four completed rows. Do not use
that file alone as the current matrix status. The dated cross-run index
`evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json` joins the two
later temporal addendum rows; each has a complete archive, endpoint fields,
100/100 or 200/200 converged steps, and a separately recorded archive hash.
The six-case replay output above verifies those exact hashes and recomputes all
gates. Thus the frozen six-case matrix is complete and its persistent-blind-
spot verdict is `NOT_OBSERVED`. This status reconciliation does not upgrade the
temporal triplet to an asymptotic convergence certificate and does not change
the separate AMR attribution verdict from `UNCERTAIN`.

## Current-state recheck (2026-10-03)

Replayed the same verifier against the present tracked archives on 2026-10-03.
It returned `PASS`, verified all six archive hashes and endpoint fields, and
recomputed the same gate pattern and `NOT_OBSERVED` matrix classification.
The new dated output is
`evidence/tests/openfoam-high-gradient-matrix-replay-2026-10-03.json`
(SHA-256 `4e1158322e59b254adc5981842d02f4c55a074ec5647dd709e179b006318e772`).
The September 28/October 2 partial n=64, `dt=0.0005` work directory remains a
historical incomplete rerun; its separately archived 100/100-step matrix row
is still the accepted evidence. The recheck does not add a new solver run,
source-to-binary equivalence proof, or physical conclusion.
