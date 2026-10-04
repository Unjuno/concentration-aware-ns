# Withdrawn unforced-regularity claim and an external Lean kernel replay

**Checked:** 2026-10-04 02:22 UTC

**Status:** primary arXiv metadata and GitHub API checked; external proof-export result observed; no theorem or solver was independently reproved in this audit.

## A seemingly contradictory claim was withdrawn

Thomas Ruf's arXiv:2609.18808 v1 (submitted 2026-09-16, updated 2026-09-17) claimed global regularity for strong solutions of the homogeneous, unforced 3D Navier–Stokes equations for (H^1_\sigma(\mathbb R^3)) data, with broader uniqueness and smoothness consequences. As checked on 2026-10-04, the arXiv record marks the work withdrawn. Its comment states: “There is an error in equation (27) that renders the crucial inequality below equation (29) wrong.” The original v1 PDF remains retrievable at the versioned arXiv URL; its SHA256 is `a5fc896be86f14f144eae65edcde47ccbbac3c3b3b15eefad7114d412276ba41`.

This is an instructive false lead, not a counterexample or current proof of global regularity. I checked the versioned PDF and independently replayed the Hölder exponents in equation (27). Writing \(a=r/2-1\) and \(h=|u|^a|\partial_i u|\), the displayed split and Hölder exponents \(q=(2/\alpha)'\), \(p=2/\alpha\) give

\[
\left(\int |u|^{2a\alpha}|\partial_i u|^\alpha\,dx\right)^{1/\alpha}
\le \left(\int |u|^2\,dx\right)^{(2-\alpha)/(2\alpha)}\|h\|_2.
\]

The second factor is \(\|h^\alpha\|_{2/\alpha}^{1/\alpha}=\|h\|_2\). In the printed equation (27), it is instead raised to \(1/\alpha^2\); equation (29) carries that exponent into \(\|h\|_2^{1/\alpha^2+4/r}\). For \(r=2+2/\sqrt3\) and \(\alpha=3r/(3r-2)\), the printed exponent is about 1.89, while the direct Hölder calculation gives \(1+4/r\approx2.268>2\). Thus the stated subquadratic power used for the subsequent energy absorption does not follow from the displayed estimate. This agrees with the author's withdrawal comment. This is a narrow replay of the cited inequality chain, not an audit of every other step or a proposed repair; the withdrawal notice remains the reason the advertised conclusion is excluded from accepted evidence.

The equation class also differs from OpenAI's advertised Navier–Stokes theorem, which uses a constructed smooth body force. A result about the unforced equations would have been especially relevant to the classical problem, but its withdrawal cannot be used to infer anything about the forced construction. Neither paper describes molecule-resolved motion or a physical phase transition.

## What external Lean checking adds

The current Lean Kernel Arena “official” checker page records successful acceptance of the OpenAI NavierStokesAndEuler export: 129,842 declarations, 9.9 minutes, Lean 4.34.0-rc2. The linked source is commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, also the latest commit returned by GitHub on this date. This is useful additional evidence that an independently hosted export/kernel checker accepted the listed declarations at that source snapshot.

This check does not show that the paper's informal derivation is correct, that the formal statements match every intended physical interpretation, that a molecular model follows, or that the repo has advanced since that snapshot. The official GitHub API reports the repository was last pushed 2026-09-10 and has Issues, Discussions, and Pull Requests disabled. A third-party checker page and preprint record are not an upstream defect report or maintainer response.

## Effect on the active benchmark

No solver acceptance, concentration criterion, local-quality threshold, or OpenAI proof verdict changes. The finding strengthens the reason to separate paper claims, formal kernel acceptance, reproducible CFD behavior, and physical inference. The long SU2 matched-pair GitHub workflow is still a separate active numerical gate and has not been restarted.

## Sources

- Ruf, arXiv:2609.18808 record and withdrawal comment: <https://arxiv.org/abs/2609.18808>
- Ruf, original v1 PDF: <https://arxiv.org/pdf/2609.18808v1>
- OpenAI Lean repository: <https://github.com/openai/NavierStokesAndEuler>
- Lean Kernel Arena checker results: <https://arena.lean-lang.org/checker/official/>
- Captured metadata and hashes: [`withdrawn-ruf-paper-and-lean-arena-2026-10-04.json`](../evidence/upstream-refresh/withdrawn-ruf-paper-and-lean-arena-2026-10-04.json)
