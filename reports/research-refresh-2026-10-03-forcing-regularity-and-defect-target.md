# Research refresh: forcing regularity and the unforced defect target

Checked 2026-10-03 JST against versioned arXiv records. This is an analytic
literature audit; it adds no solver run and makes no claim that an external
proof has been independently validated.

## Conditional regularity result for analytic forcing

Constantin, Ignatova, and Vicol, [arXiv:2609.20803v2](https://arxiv.org/abs/2609.20803v2), revised 2026-09-29, prove a local regularity theorem under a conjunction of hypotheses: a suitable weak solution smooth before the candidate singular time; a body force uniformly bounded in spatial C² up to that time and spatially real analytic locally uniformly on compact time intervals before it; the paper's anisotropic derivative bounds on the angular mean; and exact axisymmetry of the full velocity on some positive-radius ball at every pre-singular time. The radius may shrink with no positive lower bound. The theorem then implies regularity at the candidate point.

The pinned OpenAI repository was also rechecked through GitHub's API: its default branch remains at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, it declares Apache-2.0, and Issues and Discussions are disabled. This is a repository-status observation, not a peer review of the paper or proof.

The authors apply this conditional theorem to properties stated in the OpenAI construction. Under those properties and the force's bounded-C² premise, they conclude the force cannot be spatially analytic in the stated local-uniform sense near the candidate singular time. Their corollary also says the force cannot vanish identically on *any* backward space-time cylinder ending at that point. This means the scenario is not force-free throughout any whole neighborhood leading into the singular time; it does not imply a pointwise lower bound or that the force is nonzero at every time or location. Their paper explicitly says it does not verify correctness of the OpenAI construction; the properties used are taken from that manuscript and deduced as needed. The OpenAI construction's force is described as smooth and built from compactly supported cutoffs, which is compatible with smooth-but-nonanalytic forcing. This is a restriction on an analytic-forcing subclass, not a contradiction to the smooth-forcing construction.

For impact analysis, record this as a forcing-regularity boundary. It makes smooth and analytic external forcing materially different assumptions in this construction. It does not say that finite-time singularities occur in ordinary physical fluids, and it provides no molecular orientation, particle-position, phase-transition, or constitutive-viscosity result. Because the theorem is conditional on velocity properties and does not independently audit the OpenAI source proof, it is not an upstream defect report.

## Separate target for the unforced problem

Petrillo and Glimm, [arXiv:2609.23868v1](https://arxiv.org/abs/2609.23868), submitted 2026-09-20, formulate a positive energy-defect target for the *unforced*, fixed-viscosity periodic problem. They state that positive defect implies a negative answer to the relevant global-regularity alternative, while the converse is unknown, and reduce that target to an averaged fine-shell energy-flux floor. The paper distinguishes this from the smooth-forced OpenAI result and states that finite computation cannot certify the required Galerkin-uniform ceiling. Its 128³/256³ pseudo-spectral runs are exploratory diagnostics for their own unforced search, not verification or falsification of the OpenAI construction or this repository's benchmark.

This reinforces a methodological boundary already used here: finite grid studies can expose numerical behavior under recorded conditions, but cannot by themselves settle an infinite-dimensional regularity or blow-up theorem. It does not alter any solver gate or benchmark verdict.

Lei and Ren's profile reconstruction, [arXiv:2609.35406v2](https://arxiv.org/abs/2609.35406v2), remains Part I; its arXiv record says residual correction by oscillatory pulses is deferred to a companion Part II. A bounded search of current arXiv records did not locate that companion as of this check, so no claim is made about its release status elsewhere.

## Audit disposition

No simulation was used to assess these theorems. No upstream issue or discussion was opened: these papers expose no reproducible software defect in OpenFOAM, SU2, NVIDIA PhysicsNeMo, or the pinned OpenAI repository, and the relevant OpenAI repository has no enabled issue tracker. The versioned source records, claim boundaries, and refresh timestamp are captured in [`evidence/upstream-refresh/analytic-literature-2026-10-03.json`](../evidence/upstream-refresh/analytic-literature-2026-10-03.json). The construction's correctness, the `actualProfile` pressure premise, microscopic transfer, and the full solver/AMR program remain separate open work.
