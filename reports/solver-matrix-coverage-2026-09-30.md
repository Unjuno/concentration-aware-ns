# Cross-solver matrix coverage and verdicts

This inventory distinguishes completed runs from acceptance and hypothesis
verdicts. Hash checks and diagnostic replays establish artifact consistency;
they do not independently validate a solver or turn finite samples into
continuous error bounds.

The historical base OpenFOAM run manifest still labels the two later temporal
rows incomplete. The `manifest-current-2026-09-30.json` cross-run index plus
the per-row temporal manifests and raw archive checksums supersede that status
for matrix coverage, without rewriting the original frozen base record.

| Target and pinned scope | Spatial matrix | Time-related matrix | Matrix result and limits |
|---|---|---|---|
| OpenFOAM Foundation 13 package in arm64 image `sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b`, GPL-3.0-or-later source headers. Harness commits: `0e0288f98209f856931352ebfa5dad0f1aad0014` (uniform) and `265611cd160a7e139b6950c918e6dc1d90056d97` (AMR) | Uniform `n=16,32,64,128`, all at `dt=0.001` | At `n=64`, `dt=0.001,0.0005,0.00025`; common endpoint `t=0.05` | Six uniform cases complete. Standard and local gates pass at n=64 and 128; n=16 and 32 pass standard but fail local quality. The predeclared persistent-blind-spot criterion is `NOT_OBSERVED`, not “all resolutions accurate.” The temporal triplet passes both gates but exact velocity error stays nearly flat, so asymptotic time convergence is not certified. Foundation binary/source equivalence was not independently established. |
| SU2 v8.5.0, source `12eb826f049ef7f67df974dfcb44cf36ee07c0f8`, LGPL-2.1-or-later; arm64 image | `n=16,32,64`, all at `dt=0.001` | At `n=64`, `dt=0.001,0.0005,0.00025`; endpoint `t=0.05` | Five cases complete and diagnostics replay exactly from raw archives. No case satisfies the observed conjunction of velocity, energy and all-step residual checks: n=16/32 exceed aggregate thresholds and n=32/64 have steps that miss the frozen inner-residual threshold. The temporal field-difference order is about 0.999, but 2–7 steps per run miss residual thresholds; no temporal error certificate or local-quality PASS is assigned. |
| NVIDIA PhysicsNeMo v2.2.1, source `1b961314e42a0625502ba1592d25f706f1e02a24`, Apache-2.0; CPU float64, Torch 2.11.0 | `n=16,32,64` collocation densities | `time_nodes=5,9,17` at `n=64`; these are collocation nodes, **not time steps** | Original five seed-709 runs plus 20 preregistered runs across four additional seeds complete; five seeds per case, all with 5,000 optimizer steps. Per-case variability and paired contrasts are archived in `evidence/physicsnemo-seed-control-v1/analysis.json`. Spatial contrasts have mixed signs; temporal-node contrasts lower sampled velocity error in all five seeds, but magnitudes are small and descriptive. All acceptance verdicts remain `UNCERTAIN`: no PhysicsNeMo-specific threshold was preregistered, continuous extrema are not bounded, the architecture does not enforce incompressibility exactly, and this fixed budget does not establish optimizer convergence. AMR is not applicable to this fixed-architecture PINN study. |

## OpenFOAM AMR upper-state evidence

The AMR integration pilot used the n=16 case, `maxRefinement=2`, and nominal
cell budgets 4,096, 5,000 and 100,000. All three runs completed 50 converged
steps. The 4,096 budget permitted no refinement. The 5,000 case ended with
16,640 cells (level 1); the 100,000 case ended with 101,760 cells (level 2),
so the configured cap is not a strict final-cell upper bound in these batch
adaptation outcomes. Blocked-candidate counts were not observed. This matches
an approximate budget/synchronization behavior in the inspected AMR source
path; it is not evidence of an unexpected implementation defect.

The adaptive final fields have relative volume-velocity errors of 37.0% and
40.1% for the two refined cases, while fixed-final-mesh analytic-initialization
controls report 1.88% and 0.483% on the same respective meshes. This points to
an adaptive-history contribution, but the control does not isolate every
interpolation, flux-correction, projection or sensor-update effect. AMR local
quality remains `UNCERTAIN`; spectra on these nonuniform meshes are unavailable
because no reconstruction was validated. All five adaptive/remap raw archives
are now retained with byte and per-entry tree hashes; see
`evidence/tests/openfoam-amr-archive-integrity-2026-09-30.json`.

## Upstream disposition

- **OpenFOAM:** no new issue filed. The localized MMS results do not isolate an
  implementation defect, and the AMR upper-budget behavior agrees with the
  documented source path. The public repository directs bug reports to its
  separate tracker; see `reports/openfoam-amr-source-budget-audit-2026-09-28.md`
  and `reports/upstream-disposition.md`.
- **SU2:** no duplicate report filed. The nonautonomous BDF source-time
  observation is already discussed in [SU2 discussion #2890](https://github.com/su2code/SU2/discussions/2890),
  with maintainer response and scoped follow-up. The benchmark's broad local
  quality verdict remains uncertain.
- **PhysicsNeMo:** no duplicate issue filed. Odd-width power-spectrum behavior
  is already tracked in [issue #2007](https://github.com/NVIDIA/physicsnemo/issues/2007)
  and [PR #2008](https://github.com/NVIDIA/physicsnemo/pull/2008). Focused
  current-main reproduction confirms the tracked bug; it does not affect the
  benchmark's even-grid runs.

Re-run the targeted evidence checks from the repository root:

```sh
work/reference-check-env/bin/python -m tools.audit_high_gradient_time_sequence
work/reference-check-env/bin/python -m tools.replay_su2_diagnostics
work/reference-check-env/bin/python -m tools.compare_su2_time
work/reference-check-env/bin/python -m tools.review_su2_standard
work/reference-check-env/bin/python -m tools.verify_openfoam_amr_archives
work/reference-check-env/bin/python -m tools.audit_physicsnemo_local_fields
```

These commands replay records and postprocessing; they do not rerun all three
solver/training matrices. The per-target raw inputs, environments, gates and
runtime limitations remain in their linked protocol and evidence directories.
The current OpenFOAM cross-run manifest also binds the recorded arm64 image ID,
Foundation DEB, Dockerfile, build log, and installed-package inventory by hash.
The base image and DEB are pinned, but Ubuntu apt dependencies were not
snapshot-pinned and source-to-binary equivalence was not established. See the
[runtime reproduction guide](../runtime/openfoam13/README.md); replaying the
published archives does not require a solver rebuild.

## Fresh archive/postprocessing replay on 2026-10-01

Using `work/reference-check-env/bin/python`, the four original OpenFOAM
fixed-step archives again matched their frozen 50-step schedules and manifest
hashes. The five SU2 diagnostics again matched exactly when recomputed from the
saved fields and histories; the observed temporal order remained `0.99916`,
with no temporal error certificate because inner residual checks fail on some
steps. All five AMR/remap archives again passed byte and per-entry tree-hash
verification. The five PhysicsNeMo archive/checkpoint/evaluation links matched;
sampled derivative peak-magnitude errors remained `0.91–0.97%`, while the
maximum sampled derivative-field differences normalized by an exact sampled
peak were `1.20–1.26%`. These checks establish artifact and current
postprocessing consistency only. They do not rerun either solver, establish
source-to-binary equivalence, certify continuous extrema, or validate a
physical interpretation. The replay commands are listed above; the detailed
outputs remain in the existing JSON evidence records.

### OpenFOAM fixed-time-step matrix replay on 2026-10-01

The current cross-run manifest was re-read after an earlier status note relied
on the historical partial attempt. Its six completed cases were rechecked by
combining `tools.audit_high_gradient_time_sequence` (the four spatial rows,
including reconstruction and hash validation of the split n=128 archive) and
`tools.compare_high_gradient_temporal` (the n=64 temporal triplet, including
archive-to-source tree checks, exit records, complete PIMPLE counts, endpoint
fields, matching cell centers, and frozen non-time input hashes). All six
archives match their manifest digests. The two temporal addendum cases are
complete at 100/100 and 200/200 converged steps; the earlier 35/36 partial
attempt is preserved as a historical artifact and is not the source of those
rows. Their exact-velocity errors are 0.00478066, 0.00478409, and 0.00479049,
and the observed adjacent-field-difference order is about 0.499. Every temporal
row passes the configured standard and local gates, but the three-point trend
still gives no asymptotic temporal error certificate. This is a fresh replay of
archived evidence, not a solver rerun or a change to the matrix's
`NOT_OBSERVED` defect criterion.

### Short first-refinement AMR probe on 2026-10-01

A preregistered n=16, three-step probe compared the adaptive case
(`maxRefinement=2`, `maxCells=5000`, `refineInterval=2`) with an otherwise
matching uniform control. Both completed all three steps with converged PIMPLE
records. The AMR case stayed at 4,096 cells through t=0.002, then refined 1,792
cells to 16,640 before solving the t=0.003 step. The relative
volume-weighted velocity L2 errors at t=0.002 and 0.003 were 5.875% and 39.948%
for AMR, versus 5.875% and 6.161% for the uniform control. The frozen
difference-in-differences is +0.33786. The sampled maximum-gradient relative
error decreased after refinement, from 36.62% to 9.17%; this cell-center
maximum is not a continuous bound.

The cell-centre diagnostic difference is large and reproducible, but by itself
does not show that the represented velocity field worsened. A subsequent
quadrature audit below finds that the norm changes substantially with the mesh.
The
t=0.003 state already includes one solved post-remap step, so the experiment
does not identify whether interpolation, flux correction, pressure projection,
sensor updates, or subsequent evolution produced the change. It is not an
instantaneous remap measurement, a quality-threshold verdict, evidence of a
general OpenFOAM defect, or a physical singularity/particle claim. The frozen
protocol, inputs, solver and postprocessing logs, checkpoints, two raw tarballs,
and analysis are under `protocols/high-gradient-of13-amr-first-refinement-v1.json`,
`work/of13-amr-first-refinement-v1/`, and
`evidence/of13-amr-first-refinement-v1/`. Both tarball SHA-256 values were
recomputed and all members read successfully. Initial preflight failures with
no solver launch were retained under the `*-preflight-failure-*` paths.

### Analytical audit of the AMR error contrast

The first-refinement result above initially looked like a sharp error increase,
but the original metric evaluates the exact field only at cell centres and
weights those samples by cell volume. Its quadrature changes when the mesh
refines. On the identical n=16 velocity field at t=0.002, the reported norm is
5.875%; integrating either a piecewise-constant or a cellwise gradient-linear
reconstruction over each cube gives 47.684% or 58.005%, respectively. Orders
4 and 8 tensor-product Gauss-Legendre rules agree to better than 5e-8 for these
reconstructions.

As a transfer counterfactual, each of the 4,096 old cell values was assigned
to the new child cells by Cartesian containment. This produces exactly the
observed topology (2,304 unchanged parents and 1,792 parents represented by
eight children each). The integrated piecewise-constant error against the
t=0.002 exact field is 47.684% on both the old and subdivided partitions,
showing that mere subdivision does not change that volume integral. Yet
evaluating those unchanged parent values at the newly added fine-cell centres
against the exact field at t=0.003 yields 41.816%, versus 5.875% for the
old-grid centre samples. This metric change alone exceeds the apparent +33.786
percentage-point difference-in-differences, before accounting for the actual
post-refinement solver step, and arises from resolution-dependent sampling of
intra-cell variation.

Under the integrated piecewise-constant reconstruction, the t=0.002 to 0.003
difference-in-differences is -1.638 percentage points; under the integrated
gradient-linear reconstruction `U + grad(U)·(x-C)`, it is -7.060 points. Both
contrast signs reverse relative to the original centre-sample value. The
actual post-step AMR field has integrated errors 46.076% (piecewise constant)
and 50.975% (gradient-linear); these are interpretation-dependent reconstructed
norms, not a unique FV “true error”. These results show that the original
positive centre-sample contrast is not by itself evidence of AMR-induced
degradation: it is strongly confounded by mesh-dependent sampling. They do not
validate AMR accuracy or isolate the post-remap solver step.

The analytical exact cell-average reference adds a different, DOF-level view.
Under that measure, relative errors for AMR are 13.783% at t=0.002 and 40.559%
at t=0.003; the uniform control is 13.783% and 13.915%. The frozen
difference-in-differences becomes +26.643 percentage points. The parent-value
transfer counterfactual on the refined mesh is already 42.484% against exact
t=0.002 cell averages, and 42.511% against t=0.003 averages; the actual solved
t=0.003 AMR state is somewhat closer at 40.559%. This metric resolves
fine-cell-average variation that the coarse-grid DOFs do not represent. It is
consistent with the source-level parent-to-child field map, which preserves
the mapped cell value/integral while not reconstructing new subcell variation.
This is not a contradiction of the P0 integrated continuous-field result: the
two quantities answer different questions. Since the installed field's exact
average-versus-point-value semantics are not established and the checkpoint
includes flux correction plus one solve step, the DOF-level increase is a
diagnostic of prolongation/resolution mismatch, not an implementation-defect
verdict. This is why the AMR quality finding remains `UNCERTAIN`; the original
centre-sample contrast alone is insufficient. The per-case and transfer
counterfactual cell-average values are recorded in the same JSON audit.

This correction is scoped to the cross-topology n=16 AMR velocity-error
contrast. It does not rewrite the six uniform-grid run-completion or configured
PIMPLE gates. Those per-case local metrics compare computed and analytic fields
on the same cell-centre stencil, but any interpretation as a continuous-domain
norm or peak remains limited by that grid's sampling. In particular, the
matrix's fine-grid `NOT_OBSERVED` rule is a frozen discrete benchmark result,
not a proof about continuous extrema.

### Orthogonal decomposition of the AMR P0 error

For the explicitly selected piecewise-constant reconstruction, let `P_h u`
be the exact cell-average projection of the MMS and `U_h` the stored value
held constant within each cell. L2 orthogonality gives
`||U_h-u||^2 = ||U_h-P_hu||^2 + ||P_hu-u||^2`. The first term is a
cell-DOF mismatch; the second is the unresolved within-cell variation of the
analytic field. The exact continuum mean-square norm was independently
evaluated by Parseval from the reference Fourier coefficients, while exact
cell averages use the closed-form sinc formula already crosschecked against
10-point tensor Gauss integration. The resulting total agrees with the
independent order-8 cellwise Gauss integral within 1.6e-15.

At t=0.003, the AMR P0 total relative L2 error is 46.0763%, split into a
39.3816% cell-DOF mismatch and a 23.9190% projection floor; these are
orthogonal components, not quantities to add linearly. The DOF term accounts
for 73.05% of squared total error. The uniform n=16 control has a 47.7139%
total, 12.3494% DOF mismatch and 46.0881% projection floor; its DOF term is
only 6.70% of squared total error. AMR captures 94.28% of exact kinetic energy
in its cell-average projection versus 78.76% for uniform n=16, substantially
lowering the unresolved floor, while the solved AMR cell values are farther
from their exact local averages. The net P0 error improves by only 1.638
percentage points. At t=0.002, AMR has not refined and exactly matches the
uniform control in all three components.

This decomposition explains why the large 40.559% AMR error normalized by the
fine-grid cell-average vector can coexist with a slightly lower P0 integrated
error: refinement lowers the projection floor but the post-step values have a
larger mismatch to the exact means. It is conditional on the named P0
reconstruction and does not prove OpenFOAM's stored U is a cell average,
identify which AMR operation caused the mismatch, or establish an
implementation defect. Reproduce with
`python -m tools.audit_amr_projection_decomposition`; exact values and the
orthogonality check are in
`evidence/tests/amr-p0-projection-decomposition.json`. The script reads the
tracked AMR and uniform raw archives directly, checks mesh geometry and
archive/member hashes, and does not depend on extracted work directories or
run a solver.

### Where the AMR projection error and MMS gradient energy lie

The same analytic Fourier construction gives the exact cell mean of the
squared Frobenius norm of the velocity gradient, not just mean velocity energy.
Grouping exact cell
integrals by the archived `cellLevel` at t=0.003 shows:

| AMR level | Volume fraction | Exact kinetic-energy fraction | Exact gradient-energy fraction | Projection-floor fraction | DOF-mismatch fraction |
|---:|---:|---:|---:|---:|---:|
| 0 | 56.25% | 0.000621% | 0.001930% | 0.005303% | 0.009229% |
| 1 | 43.75% | 99.999379% | 99.998070% | 99.994697% | 99.990771% |

Thus almost all of this manufactured field's kinetic energy and squared
gradient lie in the refined cells, which occupy 43.75% of the domain. The
remaining projection floor and cell-DOF mismatch are also located almost
entirely there. This is consistent with the mesh being spatially matched to
the localized envelope, but the frozen sensor itself uses that known analytic
envelope; it is not a blind test of whether AMR can discover an unknown
concentration. It identifies where the explicit P0 representation error
occurs, not a physical phase transition, a singularity, or an implementation
defect. Exact cell integrals close to the global Parseval norms within the
recorded floating-point checks. The cellLevel hash and per-level contributions
are included in the same JSON evidence.

The public Foundation 13 source at tag `20260624` resolves to commit
[`18870c24d21c6b982e2cdec27b2f59738cca5f90`](https://github.com/OpenFOAM/OpenFOAM-13/tree/18870c24d21c6b982e2cdec27b2f59738cca5f90).
Its `fvMesh::topoChange` maps volume fields through `fvMeshMapper`; the
`cellMapper` uses parent-cell addressing and normalized old-volume weights for
cells created from cells. The incompressible solver then rebuilds face flux
from mapped `Uf` and runs `correctPhi` when topology changed, before the
ordinary pressure-velocity step. Thus the counterfactual parent-value mapping
matches the source-level refinement mapping for a child with one parent, while
the saved t=0.003 field additionally includes flux correction and one solved
step. Source-to-binary equivalence with the packaged DEB remains unestablished.
Relevant pinned source: [`fvMesh::mapFields`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/finiteVolume/fvMesh/fvMesh.C#L1156-L1197),
[`cellMapper`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/OpenFOAM/meshes/polyMesh/polyTopoChangeMap/cellMapper/cellMapper.C#L77-L148),
and [`motionCorrector`](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/applications/modules/incompressibleFluid/moveMesh.C#L42-L72).
Reproduce the retrospective calculation with
`work/reference-check-env/bin/python -m tools.audit_amr_cell_center_quadrature`;
its method, checkpoint metrics, counterfactual mapping counts and scope limits
are saved in `evidence/of13-amr-first-refinement-v1/cell-center-quadrature-audit.json`.

### Uniform-grid velocity L2 reconstruction audit

The same question was checked on all four completed OpenFOAM spatial cases at
`dt=0.001`, `t=0.05`. Cell-centre relative L2 errors for n=16/32/64/128 are
8.876%, 1.876%, 0.478%, and 0.121%. Integrating the piecewise-constant stored
cell values gives 48.112%, 24.170%, 12.105%, and 6.054%. A cellwise linear
reconstruction `U + grad_h(U)·(x-C)`, using the periodic Gauss gradient, gives
22.637%, 4.970%, 1.193%, and 0.296%. Tensor-product Gauss orders were compared
per resolution; the linear reconstruction values agree within 6e-12 absolute
at n=16/32, 7.5e-7 at n=64, and 4.9e-8 at n=128. At n=16, the reconstructed gradient agrees with
the saved OpenFOAM `grad(U)` field to 3.1e-15 after tensor-index normalization.
Raw field hashes and the complete table are in
`evidence/of13-high-gradient-v2/uniform-cell-center-quadrature-audit.json`.

An additional reconstruction-independent comparison uses the exact volume
average of the analytic velocity in each cell as the reference DOF. These
closed-form averages follow from separability. For
`g(q)=(1+cos q)^4/16`,
`g(q)=[35+56 cos(q)+28 cos(2q)+8 cos(3q)+cos(4q)]/128`; each Fourier mode's
cell average is multiplied by `sinc(m h/2)`. Thus the exact averages of
`u_x=e^-t g'(y)g(z) sin(Nx)/N^2` and
`u_y=-e^-t g(y)g(z) cos(Nx)/N` factor into three analytic one-dimensional
averages. Relative discrete errors against these exact cell-average vectors
are **15.558%, 3.581%, 0.894%, 0.225%** for n=16/32/64/128. The formula agrees
with independent 10-point tensor Gauss integration at five n=16 cells to
`1.8e-16` maximum absolute difference. This is a natural comparison if the
finite-volume unknown is interpreted as a cell average, but this audit does
not establish that the packaged solver's field is an exact average rather
than a cell-centred representative. It is an additional DOF-level diagnostic,
not a new preregistered gate. It places n=64/128 below the 2% velocity
threshold, while n=32 exceeds it; the full combined gate is not recomputed.

This changes the velocity-only 2% threshold result for n=32: the frozen
cell-centre norm passes narrowly, while the cellwise linear reconstruction
fails. The n=16 velocity metric fails either way; n=64 and n=128 remain below
2% under both cell-centre and linear-reconstruction norms. The complete
per-case local gate is still FAIL at n=16/32 and PASS at n=64/128 in the frozen
manifest, but this audit does not recompute gradient, vorticity, or spectrum
criteria using a reconstructed field. Therefore it neither changes the
matrix's discrete fine-grid `NOT_OBSERVED` classification nor establishes a
continuous-domain quality certification. The P0/P1 spread is itself evidence
that the reconstruction convention must be named when interpreting an FV
velocity error; these are reconstructed-field diagnostics, not replacements
for the preregistered cell-centre result.

Reproduce with
`work/reference-check-env/bin/python -m tools.audit_uniform_cell_center_quadrature`.
It reads the four archived extracted final fields, checks mesh ordering and
solver completion, records each field/input/log hash, and performs no solver
execution. The n=128 source archive integrity remains covered by the fixed-time
matrix replay described above.

### AMR sensor-to-level audit

The archived `refineSensor` at t=0.003 was independently evaluated against the
frozen prescribed formula `g(y)g(z)`, where
`g(q)=(1+cos(q))^4/16`. Across all 16,640 cells, the maximum absolute sensor
residual is 3.33e-15 (RMS 3.14e-16), confirming that the stored sensor is the
analytic envelope sampled at the archived cell centers. Level 1 covers 43.75%
of domain volume; it contains every cell with sensor >=0.01, while 72.32% of its
volume lies above that threshold. The rest is consistent with threshold-edge
and buffer-layer effects; the frozen refiner uses a buffer layer, so exact
sensor-threshold equivalence is not expected. At thresholds 0.1 and 0.5, all
selected volume is level 1, but those thresholds cover 38.39% and 11.61% of
level-1 volume respectively. Level 0 has sensor <=0.000893 in this checkpoint.

This is a consistency check of an intentionally informed AMR setup: the
source hook writes the same known manufactured envelope used by the reference.
The level/sensor correlation is therefore built into the experiment. It does
not show that the solver discovered a hidden concentration, that physical
particles aligned, or that a phase transition occurred. The complete field
parsing, protocol/archive hash checks and threshold table are reproducible via
`work/reference-check-env/bin/python -m tools.audit_amr_sensor_mapping`; output
is saved in `evidence/of13-amr-first-refinement-v1/sensor-mapping-audit.json`.
