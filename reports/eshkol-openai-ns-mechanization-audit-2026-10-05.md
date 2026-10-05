# Audit of the Eshkol Navier–Stokes mechanization — 2026-10-05

## Finding

A recent public project contains a useful independent mechanization of selected
leading-order algebra from OpenAI's 2026 forced Navier–Stokes construction
([paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)). At
the pinned Eshkol commit `c10c146e32c21a46552779fdeedd215e03d3d209`, the
first-principles example derives the scale exponents from five stated balance
relations using exact rational elimination. An independent Fraction check of
those displayed relations gives

```text
ell_r ~ tau^(1/2), ell_z ~ tau^(1/2-h),
u_theta,u_z ~ tau^(-1/2-h), u_r ~ tau^(-1/2),
core-energy exponent = 1/2 - 3h.
```

The listed positivity conditions intersect at `0 < h < 1/6`; the paper's
`0 < h < 1/100` interval lies strictly inside. This algebra supports the
scaling bookkeeping, including the warning that radial and axial Reynolds
scales behave differently. It does not independently validate the OpenAI
blow-up construction or imply that viscosity disappears: the scaling example
itself retains radial diffusion at leading order.

## What is checked and what remains open

The Eshkol source describes nine programs. Its most relevant examples use
exact scalar rational arithmetic for a finite exponent solve, truncated
profile-coefficient systems, and selected stress-cone calculations. The
source also clearly marks several boundaries: the profile operator is reduced
to `eta=0` with profiles independent of `eta`; the return to the physical
residual uses floating-point evaluation at `z=0` and stated tolerances; one
order-by-order residual example is explicitly a scalar model rather than the
paper's elliptic system; and the pulse checks do not implement the complete
infinite correction hierarchy.

The project documentation says its nine examples are exercised in JIT and AOT
CTest runs. The pinned CMake source indeed generates JIT and AOT CTest entries
for every criterion. The full-suite runner also calls
`scripts/run_examples_tests.sh`, which iterates over all `examples/*.esk`,
including the three programs omitted from the guide; the workflow assigns that
runner to the lite lanes. Thus source wiring suggests the examples are
exercised, but their result was not independently reproduced here. The
upstream CI run (`37247264764`, head `c10c146e32`) was still in progress at
00:48 UTC, with Linux ARM64/x64 and macOS ARM64 lite lanes active. A later
GitHub API status request returned HTTP 403 for rate limiting, so no completion
result is claimed.
No local Eshkol binary was built: the system compiler stopped at the Xcode
license gate, and a Nix Clang retry configured the compiler but could not find
the Apple ImageIO SDK framework. These are environment limits, not mathematical
failures.

Eshkol is a C++ implementation of a custom LISP-like language, not Lean or a
proof assistant that exports independently checkable proof objects. Its
documentation explicitly says the family uses no rigorous interval bounds
and that its verdicts depend on trusting the compiler. The exact rational
subcalculations can be valuable independent consistency checks, but they do
not certify inequalities over continuous regions unless a separate proof is
provided. The project itself does not claim to reproduce the full argument.

## Provenance and reporting decision

The source repository is [`tsotchke/eshkol`](https://github.com/tsotchke/eshkol),
licensed MIT, at a commit whose GitHub signature reports verified. The commit
adds CUDA build fixes; the audited example sources are pinned and hashed in
[`eshkol-ns-mechanization-2026-10-05.json`](../evidence/upstream-refresh/eshkol-ns-mechanization-2026-10-05.json).
The referenced OpenAI repository remains at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`,
Apache-2.0, with GitHub Issues and Discussions disabled.

The Eshkol snapshot also contains a reproducible documentation discrepancy:
`docs/NAVIER_STOKES_EXAMPLES.md` says nine programs and 18 JIT/AOT tests, while
`CMakeLists.txt` registers 14 `ns_*` criteria (28 generated CTest entries)
over 12 distinct source files. The guide omits
`mathematics_navier_stokes_mean_corrections.esk`,
`mathematics_navier_stokes_residual_ladder.esk`, and
`mathematics_navier_stokes_localization.esk`. Both counts were taken from the
same pinned tree, and all 12 referenced files exist. The Python evidence-ledger
self-check passes its 84-row consistency test, but compares the ledger with
the design pipeline table and does not check this user guide. This is a
documentation synchronization issue, not a mathematical or compiler defect.

The project's contribution guide asks reporters to check existing Issues
before opening one. The authenticated issue-list request returned HTTP 403
for API rate limiting, so duplicate status could not be confirmed; no issue
was submitted. The prepared candidate is **“Synchronize the Navier–Stokes
examples guide with the current CTest matrix.”** It would cite the
`ESHKOL_NS_EXAMPLES` list and the three omitted programs, and request updating
the guide or adding a small consistency check. Recheck the issue list when API
access is available before posting.

This is a useful addition to the analytical cross-check map, not evidence for
molecular alignment, particle-position certainty, a viscosity transition,
physical blow-up, or a failure in OpenFOAM, SU2, or PhysicsNeMo.
