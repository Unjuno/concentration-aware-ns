# Exact published-tag hosted verification

REST readback verifies both public release assets' sizes and GitHub SHA256
digests against the local full-suite log and verification receipt. The fixed
release tag remains aa3569176bad1ef7a26a9c12d3cfa4c133555cc6.

Python verification was dispatched once for this exact tag, as a distinct
source target from PR #4's pending fb35ac5 job. Registered run 37159301543
is queued and has the expected head SHA. No successful hosted result is
claimed, and no duplicate dispatch is needed. The existing PR job 37158068332
is retained. Request, acceptance timestamp, authoritative run metadata and
asset readback are in `evidence/su2-snapshot-hosted-dispatch-v1`.

The tag workflow executes the 386-test suite, published matrix/scalar
rechecks, conditional particle branches/body-force audit, C++ scalar
transcriptions and coarse/envelope SU2 force bounds. The continuous response
comparison is covered by focused constant validation but not an explicit
workflow CLI stage. A queued run is not evidence those steps have executed.
The broader global, physical, proof and solver-attribution requirements remain
open; the full goal remains active.
