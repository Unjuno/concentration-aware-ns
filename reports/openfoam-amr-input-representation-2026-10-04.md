# OpenFOAM AMR input representation audit — 2026-10-04

The four archived mean-quality cases start from analytic velocity evaluated at
cell centres, not exact cell averages. Their forcing recipe also evaluates the
analytic force at the centre and multiplies it by cell volume. This resolves an
input-interpretation question; it does not establish an upstream defect.

## Archived initialization

| Case | Relative L2 difference from independent point reference | Relative L2 difference from exact cube mean |
| --- | ---: | ---: |
| n16, dt=0.001 | 1.97412e-15 | 7.765609% |
| n32, dt=0.001 | 2.12439e-15 | 1.878300% |
| n64, dt=0.001 | 2.40708e-15 | 0.465768% |
| n32, dt=0.0005 | 2.12439e-15 | 1.878300% |

The independent point reference uses the binomial Fourier coefficients of the
manufactured solution (162 modes), rather than the initialization routine.
The exact cube-mean reference integrates the same analytic velocity over the
uniform initial cells. The 2e-12 tolerance is solely a recipe comparison, not a
new quality threshold. These floating diagnostics are not interval certificates.
Archive hashes, every archived member hash, all twenty original source identities,
the original input protocol and uniform cell ordering are checked before analysis.
The centres come from the original uniform preMap snapshot; values come from 0/U.

## Source and contract interpretation

The frozen local recipe `tools/run_amr_mean_quality.py:42` calls the AMR generator
without replacing its velocity initialization. `tools/openfoam_case.py:53`
constructs centre points and evaluates the analytic field; its forcing code uses
`mesh().C()` and subtracts volume times the centre-evaluated force. The archived
fvModels text independently confirms both centre and volume anchors. AMR sensor
configuration does not convert these inputs into integrated exact means.

Upstream is pinned at OpenFOAM-13 commit
`18870c24d21c6b982e2cdec27b2f59738cca5f90`. Six local source files were compared
byte-for-byte with Git blobs at that pin; URLs and SHA256 hashes are in
[analysis.json](../evidence/amr-input-representation-v1/analysis.json).
The volFields declaration supplies cell-associated storage. Euler time assembly
volume-weights the field and old-time field; volume weighting alone does not
define an exact continuous reconstruction. Gauss gradient assembly interpolates
face values, sums face-area contributions and divides by volume. Linear
interpolation and its weights use owner/neighbour values and mesh geometry.
The momentum predictor connects the registered source assembly.

The primary [finite-volume explanation](https://doc.cfd.direct/notes/cfd-general-principles/the-finite-volume-concept)
describes conservation through control-volume fluxes; it does not supply a
continuous reconstruction for this certificate. The
[mesh explanation](https://doc.cfd.direct/notes/cfd-general-principles/finite-volume-mesh)
associates discrete fields with cells and faces and uses centroids in calculations.
The [gradient documentation](https://doc.cfd.direct/notes/cfd-general-principles/gradient-discretisation)
describes discrete Gauss and least-squares operators. These documents were read
on 2026-10-04. In the inspected files and documents, an exact-native-average H1
reconstruction guarantee was not established. This is a scoped conclusion, not
an exhaustive claim about all OpenFOAM models or every interpretation of volFields.
The inspected upstream code carries GNU GPL version 3 or later notices; no
upstream code was modified or copied into this evidence package.

## Consequence for previous bounds

The [Arb nominal-mean certificate](openfoam-amr-arb-mean-certificate-2026-10-04.md)
remains valid under its explicit exact-decoded-mean and canonical-partition
conditions. Those conditions cannot automatically become a solver contract.
A comparison against exact analytic cell means remains a defined engineering
target, but differs from testing the actual centre-value initialization recipe.
The captured native Gauss gradient and a derivative of a continuous reconstructed
field also remain distinct quantities.

Centre quadrature is an approximation, not by itself an implementation bug.
The initial 0.465768% mean gap at n64 cannot be subtracted from the final 3.9248%
mean error; nor can the n32 initial gap explain its final 13.8446% error without
controlled evolution experiments. Existing thresholds and verdicts are unchanged.
No new upstream issue is warranted by this finding alone. No conclusion about
singularities, molecular alignment, phase transitions or viscosity follows.

## Reproduction and verification

Numerical source: `e49f169fe86c4d433730df6d5011e79e8b8a42eb`.
The original CFD source remains `3566f89058071910a41bb68010eb258c7bbc3d74`.
Download the four raw archives from the
[original release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89)
and create a JSON map from the four protocol case IDs to their local archive paths.
Use a read-only upstream checkout at the pin above, with the six specified files
matching it. From the benchmark checkout run:

```bash
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_amr_input_representation \
  --raw-map /absolute/path/raw-map.json --upstream /absolute/path/OpenFOAM-13 \
  --output /absolute/path/new-audit-output \
  --source-commit e49f169fe86c4d433730df6d5011e79e8b8a42eb
```

The complete locked local suite passed: **297 passed, 1 skipped, 83 subtests
passed**. Two new controls distinguish point from mean recipes and check the
smooth reference's resolution-dependent point/mean gap. Compile checks and
`git diff --check` passed. Logs and source hashes are preserved in
[the evidence package](../evidence/amr-input-representation-v1/README.md).
No new CFD run, clean-export replay or whole-history revalidation was performed
for this audit. The source check intentionally invokes read-only Git.

Next work must either establish a suitable reconstruction contract, use a
point-interpolating regularity bound with explicit assumptions, or run prospective
paired point-versus-mean initialization and forcing controls. None is yet done.
Original AMR quality, other solver targets, analytic interpretation and the full
goal remain open.
