# OpenFOAM AMR nested cell-average error decomposition — 2026-10-03

## Question and result

The n=16, 32, 64, and 128 same-run first-refinement audits all find that the
mapped cell-centered velocity is exactly the piecewise-constant injection of
the pre-map parent values (reported weighted relative L2 difference 0 in each
analysis). Their separate exact-cell-average diagnostic shows a predictable
resolution effect: refining a smooth reference reveals subcell variation that
the parent values cannot encode. The relative L2 magnitude of this refinement
variation is 40.573%, 20.800%, 10.465%, and 5.240%, respectively. Doubling n
halves the quantity, with observed pairwise orders 0.964, 0.991, and 0.998.

This is an algebraic explanation of the cell-average DOF comparison for these
four events, not a quality pass, continuous-field error estimate, or defect
finding. In particular, OpenFOAM's stored `volVectorField` value is not assumed
to be an exact finite-volume average.

## Exact identity

Let a parent cell P be partitioned into child cells K, and let u be any
square-integrable vector field. Write `u_P` and `u_K` for its exact volume
averages, and `a_P` for an arbitrary value injected from the parent into every
child. Since `u_P` is the volume-weighted mean of the child averages,

    sum_K |K| (u_K - u_P) = 0.

Expanding the square and using this zero-mean identity gives

    sum_K |K| |a_P - u_K|^2
      = |P| |a_P - u_P|^2 + sum_K |K| |u_K - u_P|^2.

The cross term vanishes exactly. Summing over parents gives the global identity
for nested partitions. Its first term is inherited parent-DOF error; its
second term is exact subcell-average variation revealed by refinement. The
identity is purely geometric and does not depend on the Navier–Stokes equations
or on a particular AMR implementation.

## Recorded resolution sequence

Errors are relative L2 magnitudes against the exact velocity cell averages;
the two decomposition components are square roots of the normalized squared
terms. `Map difference` is the audit's weighted relative L2 comparison of
mapped values with same-run parent injection.

| Base n | Pre-map cells | Mapped cells | Parent DOF error | Subcell-average variation | Mapped DOF error | Map difference |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 4,096 | 16,640 | 12.598% | 40.573% | 42.484% | 0 |
| 32 | 32,768 | 118,784 | 3.418% | 20.800% | 21.079% | 0 |
| 64 | 262,144 | 901,888 | 0.875% | 10.465% | 10.502% | 0 |
| 128 | 2,097,152 | 6,949,888 | 0.220% | 5.240% | 5.245% | 0 |

For n=128 the normalized squared terms are 4.8511e-6 inherited parent error
and 2.7462e-3 subcell-average variation; the total is 2.7511e-3, with
cross-term 2.23e-19 and identity residual -2.23e-19. The coarser three runs
show the same structure. The n=32 half-time-step repeat reproduces the same
refinement-variation term (0.0432641 squared-relative), as expected because
the compared refinement geometry and exact reference are unchanged; it is not
an independent spatial resolution.

The approximate first-order scaling is consistent with the generic local
Poincare estimate for cell averages of a smooth field,
`||u - average_K u||_L2 <= C h_K ||grad u||_L2`, when the refined regions and
shape regularity remain comparable. It is not a convergence proof here:
the sensor-defined refined regions vary with n, only four exploratory events
are available, and there is no preregistered AMR accuracy threshold.

## Evidence and replay scope

The source analyses and archives are:

- n=16: `evidence/of13-amr-same-run-map-v4-run3/analysis.json`, archive SHA256
  `178d764fd5a4d519d3cc1ea2692d8fde9c2318a4e85910cfb36854e9b95869ed`.
- n=32: `evidence/of13-amr-same-run-map-v5-n32/analysis.json`, archive SHA256
  `e4a0ec53e9a70f876d9b60a553375097c45854cfa59ed7b9e7dab88ed171c8f1`.
- n=64: `evidence/of13-amr-same-run-map-v7-n64/analysis.json`, archive SHA256
  `a9933f34d824cdd40adf10052fc121f62041bbf943a69b24102e3c141a26c6b5`.
- n=128: `evidence/of13-amr-same-run-map-v8-n128/analysis.json`, archive SHA256
  `d3fbd66c19f2a5274f364d062ee579248656b24a76efdf603898e62cebcb0100`.

The exact-average formula is checked against independent tensor Gauss
quadrature with maximum absolute discrepancy 1.80e-16 in
`evidence/of13-high-gradient-v2/uniform-cell-center-quadrature-audit.json`.
The n=128 compact package has a separate member-integrity record matching
the as-run preMap and mapped cell snapshots and mapped-face snapshot; that
integrity check does not recompute the numerical diagnostics. The per-run
analyses contain the pointwise/cell-average decomposition residuals and source
provenance.

The cross-run arithmetic can be regenerated from these analysis JSON files
without solver execution using `PYTHONPATH=. uv run --with-requirements
requirements-verification-locked.txt python -m
tools.audit_amr_nested_cell_average_error`. Its output is
`evidence/tests/openfoam-amr-nested-cell-average-audit-2026-10-03.json`; the
tool validates cell counts, exact parent-injection status, decomposition
residuals and records input hashes before calculating pairwise orders. It
does not recompute the archived field diagnostics or solver runs.

A live read-only replay on 2026-10-03 returned an object exactly equal to that
saved audit. The n=128 package recheck also matched all 15 local chunk hashes,
the assembled Zstandard hash, the recorded instrumentation-library hash, and
the names/sizes/digests of all 15 assets on the GitHub Release. The prior
archive-member verification still records the three as-run snapshots matching
the captured manifest. This strengthens the integrity/replay chain only; it is
not a new OpenFOAM execution or accuracy certification. Details are in
`evidence/tests/openfoam-amr-nested-cell-average-live-recheck-2026-10-03.json`.

To reproduce the numerical analyses, acquire each run's complete raw archive
according to its local manifest and use the run's pinned protocol with
`tools.analyze_amr_same_run_map`. For the n=128 review package, reconstruct the
Zstandard chunks in `evidence/of13-amr-same-run-map-v8-n128/` before archive
inspection. A replay of the decomposition arithmetic alone does not validate
the CFD solver or the field-capture instrumentation.

## Interpretation boundary

The data rules out a remap-value change relative to same-run parent injection
for these four captured first events. It also shows that most of the n=16 and
n=32 child-cell-average discrepancy, and an increasing fraction at every
resolution, is the exact reference's subcell variation rather than inherited
parent DOF error. This narrows the candidate explanation for the DOF metric;
it does not validate the AMR solution as a finite-volume approximation,
identify flux/pressure/time-integration effects, or establish behavior for
other meshes and fields. The AMR quality verdict stays `UNCERTAIN`; no upstream
defect or physical inference follows.

### Live release asset integrity recheck — 2026-10-05

The local 15-part package, reassembled `.zst` file, and instrumented library
were hashed again. Every part's byte count and SHA-256 matches the parts
manifest; the reassembled archive hash is
`68f635f06c1a00bca533e30556deeba472dd25fa91c24b1cc8ab563607a51da9`. A fresh
GitHub Release API read returned the same 15 uploaded asset names, sizes, and
SHA-256 digests. The library hash still matches the run manifest. The
machine-readable receipt is
`evidence/tests/openfoam-amr-n128-release-live-recheck-2026-10-05.json`.
This confirms current artifact distribution integrity only; it does not rerun
OpenFOAM, recompute AMR errors, establish cell-average storage semantics, or
change the AMR quality verdict from `UNCERTAIN`.
