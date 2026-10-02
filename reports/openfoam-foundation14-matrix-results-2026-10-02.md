# Foundation 14 high-gradient matrix results

## Outcome

The Foundation 14 package `20260724` (`linux/arm64`, image
`sha256:13a8802edab29a093c62ab90f063b823536e18985d52c91ab58212a4ac31447d`)
completed the frozen six-row successor matrix at `t=0.05`. It reuses the
previously completed Foundation 14 `n=64`, `dt=0.001` compatibility probe;
the other five rows were run under the frozen protocol. All six rows pass the
standard solver gate. Local sampled-quality results are identical to the
Foundation 13 matrix: n16 and n32 fail local quality, while n64 and n128 pass
at `dt=0.001` and both n64 time-step refinements pass.

| Grid and time step | Standard | Local quality | Velocity L2 error | Gradient peak error | Vorticity peak error |
|---|---:|---:|---:|---:|---:|
| n16, 0.001 | PASS | FAIL | 8.876% | 37.025% | 33.534% |
| n32, 0.001 | PASS | FAIL | 1.876% | 10.281% | 9.180% |
| n64, 0.001 | PASS | PASS | 0.478% | 2.640% | 2.349% |
| n128, 0.001 | PASS | PASS | 0.121% | 0.663% | 0.589% |
| n64, 0.0005 | PASS | PASS | 0.478% | 2.642% | 2.350% |
| n64, 0.00025 | PASS | PASS | 0.479% | 2.642% | 2.351% |

All five stored diagnostic scalars (velocity, sampled energy, gradient peak,
vorticity peak, and shell-spectrum error) are bit-for-bit equal to the
corresponding Foundation 13 values for all six rows. The final fields `U`, `p`,
`C`, and `phi` are also byte-identical after replacing only the OpenFOAM
version-banner token with a common marker. This was checked from the archived
outputs, including the reconstructed Foundation 13 Zstandard package for
n128. The immutable result and hashes are in
[`openfoam-foundation14-matrix-verification-2026-10-02.json`](../evidence/tests/openfoam-foundation14-matrix-verification-2026-10-02.json).

## Recovery and artifact verification

The first n128 attempt was stopped at 13 of 50 steps (12 converged steps,
exit 143) after a prior Foundation 13 run showed that a 40-minute cap could
truncate this case. That partial attempt remains under the ignored run
directory and is recorded in the matrix manifest. The completed retry ran
under the four-hour cap. During recovery, a faulty substring count caused
completed n16/n32 runs to be repeated. The originals are preserved, and the
replay comparison confirms identical input hashes, all four endpoint fields,
and scalar diagnostics; run logs differ in host/time and execution-time
metadata. The later line-anchored checker recounts the partial n128 log
correctly.

The final evidence package also includes compact archives of the interrupted
n128 attempt's inputs, command, exit record, and raw logs, plus full archived
copies of the preserved n16/n32 runs. The partial package deliberately omits
intermediate time directories and their large flow fields; it is sufficient to
replay the attempt's setup and inspect why it was classified incomplete.

`python -m tools.verify_openfoam_foundation14_matrix` verifies each archived
file against its run directory, reconstructs and checks all three n128 archive
parts, checks the reused compatibility archive, confirms the exact six-case
matrix, compares the stored scalar diagnostics, and compares endpoint field
hashes between Foundation 13 and 14. It reports `PASS`. The runner and verifier
are committed in the task branch; the frozen protocol hash is
`4b561ce371d988c043882bac547d7682756c27e635176c4cec9a9a2242d1a5ee`.

## Interpretation

This exact match is useful compatibility and repeatability evidence for this
manufactured solution, static mesh, `incompressibleFluid` path, arm64 package,
and six parameter combinations. It does not establish version-wide
equivalence, independently validate the shared reference/postprocessing,
certify continuous extrema, or establish a software defect. Foundation 13 and
14 could share a numerical or benchmark limitation. The n16/n32 derivative
failures remain consistent with the independently measured centered-difference
resolution floor; the adequate-grid matrix has no standard-PASS/local-FAIL
counterexample. No upstream issue or PR is warranted by this matrix.

The experiment is not a numerical reproduction of OpenAI's singular solution.
It does not test particle trajectories, molecular alignment, a phase
transition, or a changing constitutive viscosity. Those claims need separate
analytic and kinetic evidence; matching solver outputs cannot supply that
bridge.

## Run provenance

The frozen protocol and first runner were committed at `24e91762b6f763d7a48e41da95c74c88c8f6227c` before the first run. The first n16/n32 results and the
incomplete n128 attempt came from that run. The resume implementation at
`e2da2c28` repeated n16/n32; the corrected resume implementation at
`4f175202` ran the successful n128 retry and the two temporal refinements. The
final manifest/archive verification replay used `7e588cbd` and performed no
new solver calculations. The reused n64 compatibility row retains its original
source record and archive hash.
