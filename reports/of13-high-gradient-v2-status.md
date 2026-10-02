# OpenFOAM Foundation 13 high-gradient v2 status — 2026-10-02

## Scope and evidence

This is a smooth, forced, periodic manufactured solution (MMS), not an
executable extraction of the OpenAI blow-up witness. The frozen spatial/time
protocol is [`protocols/high-gradient-of13-v1.json`](../protocols/high-gradient-of13-v1.json).
The run environment records source commit
`0e0288f98209f856931352ebfa5dad0f1aad0014`, OpenFOAM Foundation 13 image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`, and
the protocol hash. The full per-case hashes, sanitized review archives,
completion states and later rerun/AMR protocol hash are in
[`evidence/of13-high-gradient-v2/matrix-manifest.json`](../evidence/of13-high-gradient-v2/matrix-manifest.json).

A source-level sign audit reads `momentumPredictor.C` and `fvMatrix.C` from that
exact image. It verifies that `A == fvModels().source(U)` is assembled as `A-B`,
that matrix subtraction subtracts the model matrix's internal source, and that
the generated coded model's `-V*f` therefore contributes `+V*f` to the assembled
momentum RHS. Source hashes and the bounded conclusion are in
[`evidence/tests/high-gradient-openfoam-sign-audit.json`](../evidence/tests/high-gradient-openfoam-sign-audit.json).
This checks the files shipped in the image; source-to-binary identity remains
unverified.

## Uniform-grid result

The `n=16, 32, 64` spatial cases at `dt=0.001`, `nu=0.01`, and `T=0.05`
completed with exit code 0, terminal `End` in the solver log and expected
endpoint output. `n=128` is an additional completed spatial case. Re-running
the postprocessor against all four archived work directories reproduced the
stored core metrics.

The peak columns below compare the computed periodic-FD2 peak with the analytic
reference peak sampled at cell centers, so they combine solution and
postprocessing differences. The FD2-operator columns compare computed FD2 peaks
with FD2 applied to the sampled analytic field.

| n | velocity relative L2 | energy relative | gradient peak difference | gradient FD2 operator difference | vorticity peak difference | vorticity FD2 operator difference |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 8.87583% | 0.61945% | 37.02461% | 2.42366% | 33.53426% | 0.19702% |
| 32 | 1.87602% | 0.04842% | 10.28069% | 0.46427% | 9.17986% | 0.07815% |
| 64 | 0.47807% | 0.02419% | 2.64037% | 0.11873% | 2.34876% | 0.01682% |
| 128 | 0.12096% | 0.01035% | 0.66306% | 0.02840% | 0.58899% | 0.00564% |

These decreases are consistent with improving resolution for this MMS. They do
not establish a software defect, an acceptance blind spot, or a singularity.
Continuous-domain peak certification is not provided.

## Temporal matrix

The original `n64-dt0.0005` attempt remains preserved as incomplete. Fresh
parameter-identical reruns at `dt=0.0005` and `dt=0.00025` completed with exit
code 0 and endpoint output; neither overwrote the original history. At fixed
`n=64`, relative endpoint field differences normalized by the finest run are
`1.3374e-5` between `dt=0.001` and `0.0005`, and `9.4658e-6` between `0.0005`
and `0.00025`, giving a diagnostic observed difference order of `0.499`. The
velocity errors are `0.47807%`, `0.47841%` and `0.47905%`. These small
inter-run differences are not a temporal error bound or proof of asymptotic
convergence; spatial and iteration effects may dominate. Reproduction data are
in [`evidence/tests/of13-high-gradient-time-comparison.json`](../evidence/tests/of13-high-gradient-time-comparison.json).

## AMR matrix

The corrected sensor was run at three requested cell caps. All cases reached
`T=0.05`, but the `cap5000` case ended with 5,440 cells, exceeding its cap by
440. Volume-weighted velocity errors are 8.876%, 32.070% and 38.572% for caps
4,096, 5,000 and 100,000. The uniform `n=64` control error is 0.478%. The
refined levels carry most of the squared error: level 1 holds 92.10% of the
error at cap 5,000; level 2 holds 77.89% at cap 100,000. These are adverse
observations for this `n=16` base-mesh setup; they do not isolate a solver defect
or its mechanism. Full analysis is in
[`reports/of13-high-gradient-amr-v1.md`](of13-high-gradient-amr-v1.md), with
per-level recomputation and hashes in
[`evidence/tests/of13-high-gradient-amr-error-strata.json`](../evidence/tests/of13-high-gradient-amr-error-strata.json).
Nonuniform shell spectra are unavailable without a validated reconstruction.

## Completion state and interpretation

- The original `n64-dt0.0005` attempt stopped at `t=0.0185` (36 of 100 steps),
  without `End`, `exit.json` or final-time output. It remains preserved as an
  incomplete attempt and is not evidence of solver failure.
- Parameter-identical reruns complete both fine temporal cases; all three
  preregistered AMR cases also complete. They are separately archived.
- At 2026-10-02 05:39 UTC, Docker context `orbstack` responded normally. No
  `cans-hg` container appeared in `docker ps -a`, and inspection of the five
  named temporal/AMR containers returned “No such container”. No active host
  `foamRun` process was observed. This resolves the earlier container-state
  uncertainty for the named runs.

The required spatial, temporal and AMR runs are present. Source-backed checking
of the configured outer-corrector criteria and frozen completion requirements
gives standard acceptance PASS for all nine complete cases. The AMR velocity
metric independently fails its preregistered 2% threshold in all three cases;
the acceptance/local-error discrepancy is therefore reproduced for this tested
matrix. See the per-case gate reports and
[`reports/of13-high-gradient-amr-v1.md`](of13-high-gradient-amr-v1.md). This is
not an upstream software-defect finding: AMR begins from a coarse `n=16` mesh,
causal factors remain confounded, raw debug residual histories were not enabled,
and source-to-binary identity is unverified. The remaining peak/spectrum metrics
and the v1 peak-metric semantics are unresolved, so campaign-wide quality is not
a PASS. The frozen AMR protocol remains unchanged; its post-run interpretation
is recorded separately in the AMR report and gate outputs. Do not use these results to infer molecular alignment, particle-position
probabilities, material-viscosity change, phase transition, engineering risk or
blow-up.
