# SU2 Dirichlet time observation pilot

The preregistered pilot uses v8.5.0's existing uniform transient MMS images,
u=(1+t²,0,0), p=0, f=(2t,0,0), a 4³-cell Cartesian mesh, BDF2, dt=0.1 and
two steps. All six faces use MARKER_CUSTOM, exercising GetBCState. The
original image and existing global-time-shift diagnostic both exit zero.
All four recorded inner residuals meet the predeclared log10 threshold -10
at both saved steps in both variants.

| Variant | Saved step | Boundary ux | Reported history time | Target time |
|---|---:|---:|---:|---:|
| Original | 1 | 1.00 | 0.0 | 0.1 |
| Original | 2 | 1.01 | 0.1 | 0.2 |
| Global shift | 1 | 1.01 | 0.0 | 0.1 |
| Global shift | 2 | 1.04 | 0.1 | 0.2 |

Each row covers all 98 boundary nodes. Original boundary values match the
old-time reference; shifted values match the target-time reference, exactly
at the saved CSV precision. Boundary errors against target time are 0.01 and
0.03 for the original, and zero for the intervention. The history clock remains
unchanged by the intervention. This is an observed distinction between history
labels and boundary evaluation times, not proof of incorrect output semantics.

The archived results were independently replayed using structured node IDs to
select boundary nodes, instead of the coordinate selection used by the runner.
Archive hashes and exit codes also matched. The small interior node set and
inner residual success do not certify overall discretization accuracy.

Reproduce the solver runs, with the two images built as described in
`runtime/su2-time-control/README.md`:

```sh
python3 -m tools.run_su2_boundary_time_pilot
# Replay committed archives without Docker:
python3 -m tools.check_su2_boundary_time_pilot
```

The runner refuses an existing output directory. Frozen protocol:
`protocols/su2-boundary-time-pilot-v1.json`. Raw inputs, mesh, image IDs,
commands, logs, histories, restart fields and diagnostics are archived in
`evidence/su2-boundary-time-pilot-v1/` with hashes in summary.json.

This pilot establishes the boundary-time observation for these two steps.
It does not isolate source versus boundary effects on interior errors, measure
temporal order, test restart, or validate a general correction. The global shift
changes both source and boundary timing; source-only and boundary-only
interventions would be needed for causal separation. No new upstream message
has been sent based on this pilot alone.
