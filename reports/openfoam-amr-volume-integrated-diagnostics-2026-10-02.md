# Cell-integrated AMR gradient and vorticity diagnostics

## Result

I recomputed the archived n=16, n=32, and n=64 first-map gradient fields on
the same physical interior and integrated the squared error of the
cellwise-constant finite-volume Gauss gradient over each cell. This removes
the earlier diagnostic's cell-center sampling of the analytic derivative.
The archived field is still represented by a piecewise-constant gradient; the
calculation does not reconstruct a continuous OpenFOAM velocity field.

| n | Stage | Gradient relative L2 | Vorticity relative L2 |
|---:|---|---:|---:|
| 16 | preMap → mapped | 56.1359% → 54.2540% | 59.3938% → 59.7202% |
| 32 | preMap → mapped | 28.0990% → 27.8614% | 29.5427% → 31.2579% |
| 64 | preMap → mapped | 13.9804% → 14.0147% | 14.6428% → 15.8499% |

These volume-integrated values materially change how the earlier center-sample
comparison should be read. At n=64, center-sampled gradient error was 1.8830%
preMap and 12.1431% mapped; the cell-integrated piecewise-constant diagnostic
is about 13.98% and 14.01%. The mapped cell-center metric therefore understated
the within-cell variation of the exact derivative for this P0 reconstruction.
Mapping and piecewise-constant parent injection did not create a clear
additional n=64 gradient penalty in this integrated metric, although the
vorticity value increases from 14.64% to 15.85%. This is a property of the
specified reconstruction and data, not a solver-defect finding.

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
`1.20e-13` in absolute relative-L2 ratio across all cases and stages. Unit
tests also check tensor quadrature exactness through degree 11, cell-geometry
validation, and an order 8 versus 10 local MMS integral.

The reproducible analyzer is `tools/compare_amr_resolution_volume_integrated.py`.
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
