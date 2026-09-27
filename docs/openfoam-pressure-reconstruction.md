# Actual pressure-correction reconstruction

The source copied read-only from a retained container matches the previously
recorded correctPressure.C hash exactly:
`1e6b6d38e1f2730368b5de45a4fc76017b06284748349149da41c90c6d84efb2`.
It defines rAU from the momentum matrix diagonal, constructs HbyA, adds a
time-derivative flux correction, optionally changes rAtU and HbyA in the
consistent branch, solves pressure, and corrects phi. It then invokes pressure
relaxation before assigning U=HbyA-rAtU*grad(p), followed by boundary and
constraint operations. A relaxation call does not itself prove pressure was
changed in these cases: no explicit relaxation factors are set in the saved
fvSolution. Branch activation must be observed, not inferred from source alone.

The endpoint dt*grad(p) proxy omits the matrix diagonal and HbyA. Its failure is
therefore not evidence of an incorrect sign in the source. The next diagnostic
must record operands at the actual assignment and distinguish subsequent
constraint effects. `protocols/of13-pressure-reconstruction-v1.json` fixes the
record points and algebraic checks before any instrumented build/run.

First validate instrumentation on a separate n16 pilot by exact comparison of
endpoint U,p,phi with an uninstrumented run under identical inputs. Preserve the
installed library; use a separately identified diagnostic library and verify
what was loaded. Until this pilot passes, do not interpret diagnostic output
or launch the expensive three-case reconstruction. Final-call algebra cannot
by itself explain error accumulated over the trajectory. No instrumented solver
has been built or executed as part of this source review.
