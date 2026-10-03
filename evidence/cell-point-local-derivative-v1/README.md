# Captured local affine derivative witness

Numerical source `dc61811614770da398324339665a48a4d4ffb098`; native capture
source `4999a4db38d0ac41a5f253a6665f6701d64f561c`.

`analysis.json` contains one nondegenerate tet's decoded nodes, nodal values,
exact rational Arb96 endpoints and gradient/curl error bounds at its interior
centroid. The field is the idealized real-arithmetic affine piece defined by
cellPoint's explicit barycentric overload. Global geometry/continuity and the
floating position-query branch remain separate.

The complete locked suite passes 318 tests, 1 skip, 83 subtests. A Git-directory-
free selected export reproduces analysis JSON byte-for-byte with Python audit-hook
checks for process/socket and Git opens. External capture files are hash-checked
input; dependencies use the same host's locked environment. No new CFD or whole-
history replay is claimed. See [report](../../reports/cell-point-local-derivative-2026-10-04.md).
