# PhysicsNeMo full-domain gradient-error interval cover — 2026-10-01

## Result

An adaptive interval cover was run on the frozen `n64-nt17` PhysicsNeMo model.
The periodic domain is covered by `[-16/5,16/5]^3`, which contains a full
fundamental cube because `pi < 22/7 < 16/5`; the model and reference field are
2π-periodic in each spatial coordinate. Starting from a 4×4×4 uniform cover,
the algorithm bisected boxes with the largest current outward-rounded upper
bound until it had 8,192 leaves.

The sampled candidate at `(3.079742548222244, 2.9815677777975633,
3.276092089071606)` gives a pointwise interval lower bound of `0.25092778047`
for the continuous Frobenius norm of the spatial gradient error. The maximum
upper bound across the cover is `7.27395329144`, a ratio of about 28.99. The
requested 10% enclosure gap was not reached. Increasing the leaves from 2,048
to 8,192 lowered the earlier direct-interval upper bound from `11.3883` to
`7.2740`, but the result remains far too broad to certify a useful peak value.

This result improves on the old sampled-only picture by placing a finite
interval upper bound over the full periodic domain, but it does not certify
the global maximum tightly, establish a PhysicsNeMo defect, or change the
quality gate. The PhysicsNeMo quality verdict remains `UNCERTAIN`: no
preregistered acceptance threshold exists, and the interval backend has not
been checked as a formal proof kernel.

## Method and reproduction

The script reconstructs the frozen network from the archived checkpoint and
encloses the analytic Jacobian error with Arb interval arithmetic. Box upper
bounds use outward-rounded Frobenius norms of the nine component intervals;
the lower bound is evaluated at one recorded point. The partition is refined
by replacing a parent with two children sharing the same binary-float midpoint.
The run used Python 3.14, python-flint 0.9.0 and PyTorch 2.11.0. Archive,
checkpoint, candidate metadata and tool hashes are recorded in
`evidence/tests/physicsnemo-gradient-global-cover-2026-10-01.json`.
The recorded execution hash identifies the exact untracked script used for
the run; a later lazy-import-only edit made the helper tests usable without
PyTorch in generic CI, and both hashes plus the base commit are preserved.

Reproduce from the repository root:

```sh
work/physicsnemo-env/bin/python tools/physicsnemo_gradient_global_cover.py
```

The local helper comparison found that quadratic Taylor enclosures were much
tighter than direct interval extensions on small boxes around the candidate,
but much worse on broad boxes. With the 8,192-leaf adaptive run, no leaf
reached the configured 0.1 width threshold, so all 16,320 box evaluations
used the direct interval method. A useful next certificate therefore needs a
better global enclosure strategy or a materially larger computation budget;
the current output records the failed tightening attempt rather than claiming
the mixed strategy helped.
