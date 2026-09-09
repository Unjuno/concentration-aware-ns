# Acceptance gate v2

This is report triage. Hash checks bind a review to file bytes; they cannot decide
whether the review, mathematics or experiment is correct. Human/source review of
the evidence remains necessary. Synthetic unit fixtures are not real reviews.

Reports require schema_version=2. All keys in tools.acceptance_gate.REQUIRED must
be true in evidence, and each must map in artifacts to a relative path and SHA256
for the reviewed evidence. The CLI resolves paths relative to the report folder,
or an explicitly supplied --artifact-root. Missing, changed or escaping paths
leave the result uncertain. A review file may cover multiple requirements, but
must actually substantiate each one; identical references do not create evidence.
The standard acceptance decision also needs a reviewed artifact.

Each metric has name, error_lower, error_upper and tolerance. The bounds refer to
the same defined nonnegative error and include the review's uncertainty budget.
Null error_upper denotes an unavailable upper bound, not zero uncertainty.

- A lower bound strictly above tolerance proves failure of that metric.
- An upper bound at or below tolerance permits passing that metric.
- An interval crossing the threshold, or a non-failing lower bound without an
  upper bound, is uncertain.
- Invalid/inverted intervals, missing mandatory gradient/vorticity metrics and
  duplicate metric names never yield a local quality verdict.

One proved metric failure suffices for overall local FAIL after evidence checks;
all required metrics must pass for local PASS. REPRODUCED additionally requires
standard PASS. It means the reviewed acceptance/local-accuracy discrepancy was
observed in the stated scope, not that an upstream software defect was proved.

CLI exit 0 requires both standard and local PASS. Any established FAIL returns 1;
otherwise exit 2 denotes uncertainty. This fixes the earlier CLI behavior where
local PASS alone could return success despite uncertain standard acceptance.
Legacy flag-only reports are now uncertain. No existing solver case has been
upgraded to full acceptance by this change.
