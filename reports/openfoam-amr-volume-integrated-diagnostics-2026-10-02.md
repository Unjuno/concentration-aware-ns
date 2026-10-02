# Cell-integrated AMR gradient and vorticity diagnostics

## Result

### Separate maximum-refinement endpoint

I also analyzed the independently archived cap100000 run at `t=0.05`. Its
saved mesh reaches refinement level 2 (2,176 level-0, 3,328 level-1, and
96,256 level-2 cells). Treating the saved OpenFOAM `grad(U)` tensor as
cellwise constant and integrating on the same `pi/4`-margin support gives
130.3984% gradient and 208.8220% curl relative L2 error. Order-6 and order-8
quadrature ratios differ by only `4.44e-16`.

This is a separate endpoint diagnostic, not another point in the n=16/32/64
first-map trend: it has a different adaptation history and final time. The
quadrature only establishes stable integration of the selected stored tensor
representation. It does not validate the tensor's construction, represent a
continuous velocity field, or establish a solver defect. There was no
preregistered AMR quality threshold, so quality remains `UNCERTAIN`. The
reproducer is `tools/analyze_amr_cap100000_integrated.py`; its input hash,
mesh counts, method, and result are recorded in
`evidence/tests/amr-cap100000-integrated-endpoint-2026-10-02.json`.

I recomputed the archived n=16, n=32, and n=64 first-map gradient fields on
the same physical interior and integrated the squared error of the
cellwise-constant finite-volume Gauss gradient over each cell. This removes
the earlier diagnostic's cell-center sampling of the analytic derivative.
The archived field is still represented by a piecewise-constant gradient; the
calculation does not reconstruct a continuous OpenFOAM velocity field.

| n | preMap Gauss gradient / curl | mapped Gauss gradient / curl | mapped least-squares gradient / curl |
|---:|---:|---:|---:|
| 16 | 56.1359% / 59.3938% | 54.2540% / 59.7202% | 54.3082% / 59.8115% |
| 32 | 28.0990% / 29.5427% | 27.8614% / 31.2579% | 27.9295% / 31.3311% |
| 64 | 13.9804% / 14.6428% | 14.0147% / 15.8499% | 14.0719% / 15.9026% |

These volume-integrated values materially change how the earlier center-sample
comparison should be read. At n=64, center-sampled gradient error was 1.8830%
preMap and 12.1431% mapped; the cell-integrated piecewise-constant diagnostic
is about 13.98% and 14.01%. The mapped cell-center metric therefore understated
the within-cell variation of the exact derivative for this P0 reconstruction.
Mapping and piecewise-constant parent injection did not create a clear
additional n=64 gradient penalty in this integrated metric, although the
vorticity value increases from 14.64% to 15.85%. This is a property of the
specified reconstruction and data, not a solver-defect finding.

As an operator-sensitivity check, a second derivative estimate was formed by
an unweighted one-ring least-squares fit of each mapped cell's neighboring
cell-center velocity differences against periodic minimum-image center
displacements. Its n=64 integrated gradient/curl errors are 14.0719%/15.9026%,
only 0.0572/0.0527 percentage points above the finite-volume Gauss result.
Across all mapped resolutions, the largest corresponding Gauss-versus-LS
differences are 0.0681 percentage points for gradient and 0.0913 points for
curl. All normal matrices were full-rank; their maximum condition number was
5.0. This makes the observed integrated scale insensitive to these two
cellwise-constant derivative estimators for these archives. Least-squares is
an independent post-processing alternative, not the solver's declared
gradient scheme and not a fitted polynomial over each cell interior.

Across n=16, 32, and 64, adjacent-grid descriptive error slopes range from
0.961 to 1.007 for gradient and 0.934 to 1.013 for vorticity. They are
consistent with first-order convergence of a cellwise-constant derivative
reconstruction in these three single-run, fixed-time samples. They do not
establish asymptotic order, an AMR guarantee, or a predeclared AMR acceptance
result; no AMR quality threshold was preregistered.

## Method and checks

The region retains cell centers more than `pi/4` from every periodic boundary,
which is the same physical support at all three resolutions and contains
42.1875% of the domain volume. Archived cell volumes and centers are checked
against the expected axis-aligned cubic base and half-base refinement levels.
For every retained cell, tensor-product Gauss-Legendre quadrature integrates
the analytic MMS gradient and vorticity against the constant discrete
gradient/curl over the cell. Order 6 and order 8 results agree within
`1.20e-13` in absolute relative-L2 ratio across all cases and stages for both
operators. Unit tests also check tensor quadrature exactness through degree
11, cell-geometry validation, an order 8 versus 10 local MMS integral, exact
recovery of an affine vector field by the least-squares operator, and rejection
of a rank-deficient stencil.

The reproducible analyzer is `tools/compare_amr_resolution_volume_integrated.py`;
the face-neighbor least-squares operator is in
`tools/analyze_amr_gauss_gradient.py`.
It verifies all three archived input hashes and reconstructs the split n=64
archive before analysis. Machine-readable metrics, protocol and archive hashes,
and quadrature-sensitivity values are in
`evidence/of13-amr-volume-integrated-comparison-2026-10-02.json`; its six-point
and eight-point full replay is included in `tools/replay_published_reports.py`.

This diagnostic integrates the exact derivative over cells for a specified
piecewise-constant gradient representation. It is not interval arithmetic,
does not integrate an independently reconstructed continuous OpenFOAM field,
and does not resolve whether another gradient reconstruction is more
appropriate for a given solver output. The AMR quality verdict therefore
remains `UNCERTAIN`; no upstream report or physical inference is supported.
