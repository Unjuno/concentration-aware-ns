# PhysicsNeMo local peak refinement (2026-10-01)

## Result

Starting from the top 16 points of the independent 1,048,576-point scrambled
Sobol scan, bounded PyTorch L-BFGS refinement found a candidate at
`(3.027973887483007, 3.0013446094963365, 3.259521137998328)` with gradient-error
Frobenius value `0.2534082916967482`. Its final objective gradient norm is
`8.42e-8`. This is a numerical candidate, not a proof of a local maximum.

An Arb point enclosure gives a pointwise lower bound of `0.253408291696744` at
the candidate. For the box with half-width `1e-4` in each coordinate, direct
interval arithmetic gives an upper bound `0.25773554`, while the quadratic
Taylor enclosure gives `0.25344430`. At wider boxes, direct interval dependency
inflation is substantial; the Taylor upper grows more slowly (e.g. `0.25419206`
at half-width `0.002`). These enclosures cover only boxes centered at this
candidate.

## Interpretation and limits

The refined candidate is about 0.42% above the prior Sobol sampled maximum
`0.25234574`, in the same spatial neighborhood. This is further evidence that
the old lattice understates the largest observed point value. It does not
locate or certify the continuous-domain maximum, establish a solver defect, or
support a physical particle-alignment or viscosity claim. The full-domain
interval cover remains too coarse, and no preregistered quality threshold is
available; verdict remains **UNCERTAIN**.

The optimizer is PyTorch L-BFGS with a logistic map into the explicit box
`[2.4,3.7] x [2.4,3.7] x [2.8,3.8]`. “Success” records only that the final
floating-point gradient norm met the selected tolerance. Arb bounds inherit
the limitations of the underlying Arb Python library and are not an
independent formal verification of that library.

## Reproduction

From the repository root:

```sh
PYTHONPATH=.:work/physicsnemo-source work/physicsnemo-env/bin/python tools/refine_physicsnemo_gradient_peak.py
```

The script verifies that the checkpoint hash in the Sobol record matches the
frozen archived study input. The complete per-start outputs, input hashes,
precision, and tool hash are in
`evidence/tests/physicsnemo-local-peak-refinement-2026-10-01.json`.
