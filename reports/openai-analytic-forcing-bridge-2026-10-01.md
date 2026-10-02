# Flat-but-active forcing: analytic-forcing regularity cross-checked against OpenAI

Status: a source-to-source assumption crosswalk and elementary conditional deduction. This is not an independent verification of either research paper's complete proof, the OpenAI construction, or a physical interpretation.

## Primary sources and version

The current arXiv version checked on 2026-10-01 is Constantin, Ignatova, and Vicol, *Regularity of asymptotically axisymmetric solutions to the 3D Navier-Stokes equations with analytic forcing*, v2, revised 2026-09-29: [versioned HTML](https://arxiv.org/html/2609.20803v2) and [version history](https://arxiv.org/abs/2609.20803). Its Appendix A records specific source statements from OpenAI's manuscript and derives the properties used by its theorems. The OpenAI primary source checked here is the [166-page Navier-Stokes manuscript](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf). The authors explicitly say they do not claim to have verified the correctness of the OpenAI construction (arXiv paper §1, lines 79-80 in the versioned HTML). Treat their source crosswalk accordingly.

## Two distinct implications

The paper's Theorem 1.1 assumes a suitable weak solution, a force bounded in spatial `C^2` up to the candidate terminal time, local-uniform spatial real analyticity on interior time cylinders, anisotropic Type-II bounds through second derivatives for the angular mean, and exact axisymmetry on a nonempty core at every preterminal time. Under these joint conditions it proves regularity at the candidate point. The paper's Appendix A.2/A.3 states that the OpenAI construction has the angular-mean bounds and collapsing exactly axisymmetric core; A.6 cites OpenAI Proposition 10.1 and Lemma 10.3 for smooth compactly supported fields and force. OpenAI Lemma 10.3 says the force extends as `C∞_c(R^3 × (0,∞))`, which in particular supplies a uniform spatial `C²` bound.

Consequently, **conditional on the OpenAI construction having the claimed singularity and on the Appendix A source crosswalk**, its force cannot satisfy the paper's local-uniform spatial analyticity hypothesis. Corollary 2.3 further deduces that the force is not identically zero on any space-time cylinder `B(R') × (-δ',0)` around the point. These are restrictions on the forcing required by that construction, not a contradiction: OpenAI only claims a smooth force, and explicitly builds it with smooth cutoffs.

The paper also gives a separate route in Remark 2.6. On a fixed open off-axis set `E`, the OpenAI field is pure swirl, so `u_r=u_z=0` there for a time interval. At the axis, the paper derives `u_z(0,-τ)=j₀ τ^{-A} ≠ 0` for sufficiently small `τ>0` from OpenAI's axis profile `U*(η)=4η+j₀` and similarity coordinates (`q=τ`, `η=0` on the axis). For any ball intersecting `E`, suppose the force had a common spatial-analyticity bound over a time interval ending at such a time. Interior spatial analyticity of the solution would make `u_z(·,t)` analytic on that ball. Since it vanishes on the nonempty open set `E` intersected with the ball, the identity theorem would force it to vanish on the whole connected ball, including the axis. Continuity to the endpoint contradicts the nonzero axial value. Therefore no such common analyticity bound exists on those ball-time intervals; in particular the force cannot vanish identically there, since zero is analytic. This argument uses the cited geometric and axis-value properties, but **does not use the blow-up claim, the Type-II bounds, or the shrinking-core analyticity theorem**.

The axis-value calculation can be checked from the primary manuscript's profile data: `U*(η)=4η+j₀` is specified in Appendix B; the axial similarity profile has `u_z=q^{-A}U` on the axis, with higher-order axial coefficients vanishing there; `η=zq^{-D}` and `A+D=1`. At `z=0`, `q=τ` and `η=0`, giving `u_z=j₀τ^{-A}`. Differentiating in `z` at the axis gives `∂z u_z=4τ^{-(A+D)}=4/τ`. The arXiv appendix provides the detailed source crosswalk at A.3; the underlying OpenAI manuscript gives the axis profile in Appendix B and the smooth compact-force construction in §10.

## Flat at the point, nonzero arbitrarily near it

OpenAI Lemma 10.2 states that as `t↑1`, every mixed derivative has a uniform
limit `∂x^α∂t^j f(x,t) → ∂x^α F_j(x)` and that `∂x^α F_j(0)=0` for every
spatial multi-index `α` and every `j≥0`. Lemma 10.3 constructs a `C∞`
extension through `t=1` matching those jets. Therefore every space-time
derivative of the extended force vanishes at `(x,t)=(0,1)`: its full Taylor
jet there is zero. Taylor's theorem then gives, for each finite order `m`,
`f(x,t)=o((|x|+|t-1|)^m)` as `(x,t)→(0,1)`. In particular, the supremum on
parabolic cylinders `B(r)×(1-r²,1)` is `o(r^m)` for every fixed `m`.

Combine that source statement with Corollary 2.3's conditional conclusion that
the force is not identically zero on any such neighborhood cylinder. Under the
OpenAI construction's claimed singularity and the preprint's stated source
crosswalk, the force is thus **flat at the singular point but nonzero somewhere
in every neighborhood cylinder**. The independent Remark 2.6 route yields
nonvanishing on ball-time slabs intersecting the pure-swirl set from its
geometric and axis-value properties, without using blow-up. Neither result
gives a lower bound on where the nonzero values occur or how large they are;
the flatness estimate specifically rules out inferring a polynomial lower
amplitude scale from these statements.

This distinction matters when interpreting finite-resolution forcing: a
finite-order local expansion at the singular point is identically zero even
though the conditional nonvanishing result precludes an actually zero force
on every full neighborhood. It does not by itself prove that a numerical
discretization misses the force; that would require quantitative constants,
support geometry at the chosen grid scale, and a frozen implementation.

## What follows, and what does not

The mathematically useful distinction is between smoothness, flatness at a
point, nonvanishing in every neighborhood, and spatial analyticity. The
construction's forcing is smooth and flat at the terminal singular point, yet
the stated source geometry rules out spatial analyticity on specific local
time slabs and, conditionally on the claimed singularity, rules out turning the
force off through a full neighborhood cylinder. This gives a concrete
forcing-regularity boundary for the claimed construction and a falsifiable
source audit.

It gives no positive lower bound on force amplitude, no lower bound on how often or how strongly it acts at any selected point, no actuator bandwidth or energy requirement, and no evidence that an ordinary physical flow realizes the construction. A smooth force can be nonzero somewhere in every neighborhood while vanishing to high order at the limiting point. It also does not imply molecular ordering, particle-position certainty, a change in constitutive viscosity, numerical solver failure, or a global regularity resolution. The result is an arXiv preprint, not an independent adjudication of the OpenAI proof.

## Audit record

The machine-readable crosswalk is [`evidence/openai-analytic-forcing-v2-audit.json`](../evidence/openai-analytic-forcing-v2-audit.json). Useful source locations are Theorem 1.1, Corollary 2.3, Remark 2.6, and Appendix A.2–A.6 in arXiv v2; and OpenAI Theorem 1.1, §§3.1 and 10, and Appendix B.1. No simulator run or upstream software report is warranted by this analytic constraint alone.
