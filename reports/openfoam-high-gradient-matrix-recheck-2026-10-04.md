# OpenFOAM Foundation 13 high-gradient matrix replay

The six-case index in
`evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json` was replayed
from the published case archives with
`tools.verify_openfoam_high_gradient_matrix`. The verifier checked the current
index, frozen protocol and original base-manifest hashes; reconstructed the
split n=128 package; verified all six archive and source-log digests; checked
endpoint fields and case metadata; and recomputed the standard stopping and
sampled local-quality gates from each archived log, configuration and
diagnostics.

The replay passed for all six cases. Every case passes standard acceptance.
The n=16 and n=32, dt=0.001 cases fail the frozen local-quality gate; n=64 and
n=128 at dt=0.001 and n=64 at dt=0.0005 and dt=0.00025 pass it. Accordingly,
the frozen fine-grid concentration rule is `NOT_OBSERVED`: both n=64 and n=128
pass the standard and local sampled gates. The two temporal addendum cases each
contain 100 and 200 converged time steps, respectively; the historical
36-record partial `dt=0.0005` attempt remains preserved and is explicitly
superseded by the completed addendum run.

The replay receipt is
`evidence/tests/openfoam-high-gradient-matrix-2026-10-04-b996015.json`.
It binds the result to index SHA-256
`8f6004aeedcc821da319fe1d7af646138b17c5bf7f948c08548c2c6ae7fbaee8`, frozen
protocol SHA-256 `838ac4d91d8a816f96cebf02d780a9ec7df265ae3b45748d2a2c795c6d80d93d`,
and base-manifest SHA-256
`9dc26bad1e249669fa18a3a430712edf8df83445238c1cb846fb4b262debb89c`.

This is a replay of archived solver outputs and declared gates, not a fresh
solver run, an independent source-to-binary proof, or a continuous-domain error
certificate. The separate AMR/remap pilot remains quality `UNCERTAIN`; no
AMR conclusion follows from this six-case uniform-grid replay.
