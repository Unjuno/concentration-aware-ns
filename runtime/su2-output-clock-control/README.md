# Fixed-step output-clock causal control

This diagnostic image derives from the original uniform MMS image. It changes
only the assignment to CUR_TIME in COutput::LoadCommonHistoryData from an
increment to curTimeIter*TIME_STEP. Driver PhysicalTime, MMS source evaluation,
boundary evaluation and output file numbering are unchanged in source.

It is intended only for the existing static-mesh, constant-dt direct BDF2
pilots. It is not a proposed general fix: multiplication by current dt does
not reconstruct variable-step elapsed time, and other output-clock consumers
may affect stopping behavior. No moving-mesh or adjoint applicability is asserted.

```sh
docker build --network=none -t concentration-aware-ns:su2-output-clock-control runtime/su2-output-clock-control
```

The planned comparison retains original old-time source and boundary behavior.
If history continuity improves while same-index fields remain unchanged, it
supports attribution to the output accumulator. Build success alone is not
that experimental result.
