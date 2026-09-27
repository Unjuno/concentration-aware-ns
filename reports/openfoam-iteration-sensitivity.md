# OpenFOAM temporal comparison is insensitive to the tested iteration tolerances

All three preregistered n=64 controls completed at t=0.05. Linear tolerances
were tightened from 1e-10 to 1e-12, outer tolerances from 1e-8 to 1e-10, and
the outer-corrector cap increased from 12 to 40. Initial conditions, forcing,
mesh, Euler scheme and output precision were retained from byte-verified
baseline inputs. All 350 physical steps report outer convergence.

| dt | Steps | Relative endpoint velocity shift from original |
|---:|---:|---:|
| 0.001 | 50 | 6.55046e-15 |
| 0.0005 | 100 | 6.77897e-15 |
| 0.00025 | 200 | 4.82925e-15 |

The timestep-difference order changes from 0.492914290106 to 0.492914289889.
The difference-vector cosine remains 0.8830965338, and the relative first-order
vector defect remains 0.713912132. Changes in iterative settings therefore do
not explain or remove the non-asymptotic behavior in this tested comparison.
This is not proof of zero iteration error under every setting, nor evidence
that the Euler implementation is faulty. Initial discrete flux compatibility,
pressure/flux coupling and the asymptotic timestep range remain candidates.

The first case's outer-iteration total increases from 300 to 349, confirming
that stricter settings led to additional work despite the almost identical
endpoint. The solver convergence criterion itself is not a continuum accuracy
certificate. Overall quality remains UNCERTAIN; no acceptance gate is relaxed.

## Reproduction

With baseline cases restored under work/of13-study-v1 and the recorded runtime
image available, run in an unused work/evidence namespace:

```sh
python3 -m tools.run_openfoam_iteration_sensitivity
python3 -m tools.compare_openfoam_iteration_sensitivity
```

The runner refuses existing output roots. Each archive in
`evidence/of13-iteration-sensitivity-v1` preserves copied inputs, altered solver
dictionary, input/protocol hashes, image identity, commands, logs and endpoint
fields. `summary.json` records exits/convergence counts/archive hashes;
`comparison.json` records field hashes and comparative metrics. Cell-center
correspondence, finite fields, terminal logs, step counts and endpoint time were
checked before comparison. The temporal comparator's four focused tests pass.

The constructor-only startup probe is documented separately in
`docs/openfoam-startup-flux.md`; it establishes a discrete initialization
observation but has not established causation for this temporal-order result.
No OpenFOAM upstream defect report is justified by these controls alone.

Fresh-directory archived-input replay now reconstructs this comparison from
six published archives (three original, three tighter-iteration cases), with
no reliance on the retained work directories. The regenerated comparison JSON
matches the published result exactly. `archive-replay.json` records archive
hashes and scope. Run `python3 -m tools.replay_openfoam_iteration_archives`.
This reuses the published comparison routine; it is not an independent numerical
algorithm or a new solver execution.

The common report replay now includes this reconstruction, the SU2 output-clock
archived control and the uniform pressure-prefix threshold. All 21 steps pass,
including 54 unit tests. Pending startup/intervention runs are excluded from
that success claim, and scientific UNCERTAIN verdicts remain unchanged.
