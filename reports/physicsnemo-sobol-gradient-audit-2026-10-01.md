# Independent PhysicsNeMo gradient-error point search — 2026-10-01

The frozen `n64-nt17` checkpoint was evaluated at 1,048,576 scrambled Sobol
points over `[0,2π)^3` using PyTorch autograd and the independent analytic
reference Jacobian in `tools.reference`. The seed is 20261001; the run used
PyTorch 2.11.0 and batches of 512. The largest sampled Frobenius gradient error
was `0.2523457378401675` at
`(3.0490564258730486, 2.993409257476551, 3.23764079755766)`. An Arb point
enclosure gives a lower bound `0.25234573784017766` at that location.

The earlier 262,144-point lattice maximum was `0.2509277804721862`. The new
sample is larger by `0.00141795737`, about 0.56%, and lies in the same local
region. This is evidence that the earlier lattice understated its own sampled
peak slightly. It does not show that the Sobol maximum is the continuous
maximum, or that there is a solver/software defect. It also does not resolve
the prior full-domain interval enclosure, whose upper bound remains about
7.274. The quality verdict stays `UNCERTAIN` because there is no preregistered
continuous PhysicsNeMo acceptance threshold.

The raw checkpoint and evaluation archive hashes, all top sampled points,
pointwise Arb lower bound, seed and script hash are in
`evidence/tests/physicsnemo-sobol-gradient-audit-2026-10-01.json`.

Reproduce from the repository root, with the pinned PhysicsNeMo source and
runtime environment present:

```sh
PYTHONPATH=.:work/physicsnemo-source \
  work/physicsnemo-env/bin/python tools/audit_physicsnemo_sobol_gradient.py
```
