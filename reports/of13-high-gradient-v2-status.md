# OpenFOAM Foundation 13 high-gradient v2 status — 2026-10-02

## Scope and evidence

This is a smooth, forced, periodic manufactured solution (MMS), not an
executable extraction of the OpenAI blow-up witness. The frozen protocol is
[`protocols/high-gradient-of13-v1.json`](../protocols/high-gradient-of13-v1.json).
The run environment records source commit
`0e0288f98209f856931352ebfa5dad0f1aad0014`, OpenFOAM Foundation 13 image
`sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`, and
the protocol hash. The full per-case file hashes, sanitized review archives and
completion states are in
[`evidence/of13-high-gradient-v2/matrix-manifest.json`](../evidence/of13-high-gradient-v2/matrix-manifest.json).

## Uniform-grid result

The `n=16, 32, 64` spatial cases at `dt=0.001`, `nu=0.01`, and `T=0.05`
completed with exit code 0, a terminal `End` in the solver log, and the expected
terminal output. `n=128` is an additional completed spatial case. Re-running
the present postprocessor against all four archived work directories reproduced
the stored core metrics.

The first two peak columns below compare the computed periodic-FD2 peak with
the analytic reference peak sampled at cell centers. They combine solution and
postprocessing differences. The FD2-operator columns compare the computed FD2
peak with FD2 applied to the sampled analytic field; they isolate the
postprocessing contribution on those sample sites.

| n | velocity relative L2 | energy relative | gradient peak difference | gradient FD2 operator difference | vorticity peak difference | vorticity FD2 operator difference |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 8.87583% | 0.61945% | 37.02461% | 2.42366% | 33.53426% | 0.19702% |
| 32 | 1.87602% | 0.04842% | 10.28069% | 0.46427% | 9.17986% | 0.07815% |
| 64 | 0.47807% | 0.02419% | 2.64037% | 0.11873% | 2.34876% | 0.01682% |
| 128 | 0.12096% | 0.01035% | 0.66306% | 0.02840% | 0.58899% | 0.00564% |

The decreasing errors are consistent with improving resolution for this MMS.
They do not establish a software defect, a residual/local-quality acceptance
blind spot, or a singularity. The peak metrics are still diagnostics rather
than a protocol-complete quality verdict, and continuous-domain peak
certification is not provided.

## Incomplete cases and verdict

- `n64-dt0.0005` stopped at `t=0.0185` (36 of 100 requested steps). Its log has
  no terminal `End`, it has no `exit.json`, and no final-time output. It remains
  `INCOMPLETE`; it is not evidence of a solver failure.
- `n64-dt0.00025` was not started.
- The frozen protocol requires an AMR comparison; no AMR solver run is present.
- A host process-list scan on 2026-10-02 found no `foamRun` process. The
  Docker/OrbStack container state is `UNVERIFIED`; earlier stop/inspect requests
  had hung, so absence of a host process is not represented as confirmed
  container removal.

Campaign status is `INCOMPLETE`, and numerical quality remains `UNCERTAIN`.
The high-gradient analytic identities and independent SymPy/NumPy formula
comparison pass, but no independent OpenFOAM source-equation sign audit or
completed temporal/AMR matrix is available. Do not use this campaign to infer
molecular alignment, particle-position probabilities, material-viscosity
change, phase transition, engineering risk, or blow-up.
