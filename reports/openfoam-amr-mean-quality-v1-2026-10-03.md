# Prospective Foundation 13 AMR mean-quality study

The N=3 successor executes separately specified mean-quality gates on native
Foundation 13 fields. It does not reuse the earlier N=4 peak/spectrum threshold.
The run is frozen at `3566f89058071910a41bb68010eb258c7bbc3d74`;
[hosted run 37124421538](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37124421538)
uses four independent ARM64 VMs. The numerical and reproduction outcomes below
are distinct from workflow success and from an upstream implementation defect.

## Frozen experiment

The smooth periodic MMS uses frequency N=3, viscosity 0.01 and end time 0.05.
Base grids are 16/32/64 with dt=0.001, plus n32 with dt=0.0005. All first maps
occur at t=0.002, maxRefinement=1; specified budgets are 5000/120000/920000.
The case matrix and thresholds were committed before any N=3 solver run,
but informed by the earlier N=4 diagnostics; no blinded design is claimed.
See [`protocol`](../protocols/of13-amr-mean-quality-v1.json).

The new accuracy targets are 2% for exact cube-mean velocity mismatch and 5%
for exact cube-mean gradient/curl mismatch. Errors are volume weighted and
normalized by the integrated continuum reference norm. These are engineering
accuracy targets for a defined synthetic case, without application-specific
certification. P0 representation floors and total errors are reported separately.
Native Gauss gradients are transposed to component-first indexing on export.
A separate real-space analytic field, independent of the forcing's Fourier
implementation, passes through the same native gradient operator on every mesh.
Reference-operator failure blocks the fine-case reproduction judgment.

Snapshots capture preMap/mapped at t=0.002 and postSolve at t=0.05. The n16
run also executes the same compiled module/inputs with callbacks disabled.
Its final U/p files must match exactly. No capture-disabled fine-grid
counterpart was run; this empirical noninterference check covers n16. All eight original module file hashes
and 167 stock library payloads match the pinned official Foundation package.
The archived positive dynamic-loader initialization confirms use of the
instrumented module. Uniform preMap native tensors are independently checked
against periodic centered/Gauss reconstruction. This establishes the recorded
measurement controls, without full-runtime source/compiler equivalence.

## Outcomes

| Case | Final cells | Standard | Velocity mean, 2% | Gradient mean, 5% | Curl mean, 5% | Composite mean gate |
|---|---:|---|---:|---:|---:|---|
| n16-dt0.001 | 16640 | PASS | 28.4503% | 28.3092% | 26.4502% | FAIL |
| n32-dt0.001 | 116992 | PASS | 13.8446% | 14.0465% | 11.7136% | FAIL |
| n32-dt0.0005 | 116992 | PASS | 13.6743% | 13.8612% | 11.7121% | FAIL |
| n64-dt0.001 | 887552 | PASS | 3.9248% | 4.0255% | 3.2919% | FAIL |

All four hosted executions and analyses complete. The n16 disabled-capture
control matches final U/p bytes exactly. Both n32/n64 native reference
derivative controls pass at all three stages. The composite rule reproduces
a **specified final velocity-mean threshold discrepancy** at n32/n64.
At n64, final gradient/curl mean gates PASS; they are not common fine-grid
failures. All reported errors improve markedly from n32 to n64; no failure
of asymptotic convergence is established. The n32 preMap velocity mean already
exceeds 2% (2.1481%), while n64 preMap passes all mean gates (velocity 0.5465%).
No complete AMR-disabled N=3 counterpart was run, so the late-time comparison
does not isolate AMR as the only cause. This is a bounded exp(-t)-decaying MMS.
The broader OpenAI candidate and particle/viscosity model transfer remain separate.


The matrix rule requires all four complete same-source/protocol cases,
verified n16 capture control, standard PASS in every case and reference
operator PASS at every stage of both fine fixed-dt cases. Only then can two
postSolve mean-quality failures reproduce a specified discrepancy. Missing,
mixed or inadequate-reference evidence gives UNCERTAIN. A reproduced
engineering-threshold discrepancy is not evidence of nonconvergence or a
solver contract violation.

## What the map changed

Across all four independently checked archives, the captured mapped U/p are exactly the parent values,
component by component. The velocity integrals are preserved within floating
roundoff. Refinement increases the available cell count without introducing
new velocity information at that instant.

There is a precise distinction between changed cell-mean mismatch and changed
continuum error. Let P0/P1 be a nested parent/child cube partition, let v be the
parent-constant captured velocity, and let u be the smooth exact reference.
The orthogonal projection identity for each partition is

$$\|v-u\|_{L^2}^2=M_i+F_i,\qquad
M_i=\sum_{K\in P_i}|K|\,|v_K-\bar u_K|^2,\qquad
F_i=\sum_{K\in P_i}\int_K|u-\bar u_K|^2.$$

Exact parent-value injection leaves v unchanged as a P0 function. Therefore

$$M_1-M_0=F_0-F_1,\qquad M_1+F_1=M_0+F_0.$$

The lower representation floor becomes higher mean mismatch; the continuum
velocity error does not jump merely because the same function was subdivided.
For n32/dt=.001, the relative squared total stays 0.036321852492838, with an
exchange-identity residual 3.33e-16. Mean mismatch changes 2.1481% to 16.5053%,
while the velocity representation floor changes 18.9369% to 9.5285%.
Calling this increase newly created continuum velocity error would be wrong.
The native derivative tensor can itself change when its stencil and mesh
change; the velocity repartition identity does not assert tensor invariance.

The n32 half-step control reduces final velocity/gradient mean errors modestly
(13.8446% to 13.6743%, 14.0465% to 13.8612%) while curl error stays near 11.71%.
This supports a limited comparison at fixed refinement scheduling and physical
map time. It does not isolate every spatial/temporal contribution or establish
an asymptotic convergence order.

## Independent replay and limitations

Every archived regular member is checksum verified. The supplemental replayer
regenerates inputs, checks archived final fields against the captured postSolve
values, verifies the positive loader initialization and repeats all 167 stock
payload comparisons. Hosted and macOS categorical analysis results agree;
floating differences are retained in per-case comparison records.

Strict cross-platform regenerated input byte identity fails: the archived
Linux initial U and macOS-generated U differ at roundoff. The first n16
comparison has maximum absolute difference 1.38778e-17 and relative L2
difference 2.48960e-17. The original strict failure is preserved. An explicit
optional compatibility mode compares only the initial vector values within
32 machine epsilons times their maximum magnitude, retains identical nonvalue
structure and every other input file, and continues to label byte identity
FAIL. It never changes the solver quality thresholds. Archive byte integrity
and n16 main/control byte identity are separate, successful checks.

The gradients are the declared piecewise constant native Gauss tensors;
sampled peaks remain diagnostics, numerical continuous extrema are uncertified
and validated AMR spectrum reconstruction remains open. This study does not
close the original N=4 AMR peak/spectrum gate, SU2 quality, PhysicsNeMo
continuous-field certification, or the OpenAI proof/physical-model bridge.
It demonstrates neither molecular alignment, a phase transition nor a change
in constitutive viscosity. Viscosity is held constant in these inputs.

No new upstream defect report is warranted from these mean thresholds alone.
The raw data, source/input identities and replay instructions belong to the
same canonical repository. The overall goal remains active.
