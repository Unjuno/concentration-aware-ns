# OpenAI proof follow-up refresh — 2026-10-04

The latest targeted search of the public arXiv record still finds Lei and
Ren's [Part I, arXiv:2609.35406v2](https://arxiv.org/abs/2609.35406v2) as the
public explanatory companion. Its abstract explicitly limits that manuscript
to the profile construction and says cancellation of the divergence-form
residual by oscillatory pulses will be treated in a companion Part II. The
search did not locate a separate Part II record. This bounded negative search
does not establish that no draft exists elsewhere, and it does not show that
OpenAI's own proof omits the step. It means our independent public-paper audit
still cannot replay the final pulse-cancellation stage from Lei–Ren Part I.

This refresh adds no mathematical finding and no upstream defect. OpenAI's
own Lean repository remains pinned separately by its live `main` source
identity, and its GitHub repository currently disables Issues and restricts
new pull requests. The right next analytic audit, if Part II appears, is to
rederive the residual-to-pulse matching and uniform remainder estimates,
checking the function spaces and all scales independently; the current Part I
compatibility and displayed-scale replays do not discharge that task.

## Search record

On 2026-10-04, searched the exact proposed Part II title and the distinctive
phrase “Residual Correction via Oscillatory Pulses” on arXiv-indexed results,
then opened the primary Part I abstract. This is a bounded title/phrase
search, not an exhaustive crawl. Its result supports “not located,” not “does
not exist.”

### Official API recheck — 2026-10-04 05:48 UTC

Queried arXiv's Atom API directly with an exact `ti:` Part II title search and
an exact-phrase `all:` search. The title query returned `totalResults=0`; the
phrase query returned one result only, Part I v2 (`2609.35406v2`). Raw Atom
responses, captured timestamps, and SHA-256 hashes are preserved at
`evidence/upstream-refresh/lei-ren-part-ii-exact-title-2026-10-04T0548Z.atom.xml`
and `evidence/upstream-refresh/lei-ren-part-ii-phrase-2026-10-04T0548Z.atom.xml`.
This strengthens the current public-catalog check but still cannot rule out an
unsubmitted draft, a changed title, or a manuscript outside arXiv.
