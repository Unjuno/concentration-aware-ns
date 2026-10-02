# What incompressibility says about particle-position certainty

## Result

For a classical flow map `X_t` generated on a time interval by a smooth,
divergence-free velocity on three-dimensional space, the Jacobian satisfies

```
 d/dt det(DX_t) = (div u)(t, X_t) det(DX_t) = 0,
 det(DX_t) = 1.
```

Thus each such `X_t` preserves volume. If the initial passive-tracer position
law has a density bounded by `K` with respect to volume, then for every
measurable target set `B_t`, even one whose center moves with time,

```
 P(X_t(X_0) in B_t)
   = P(X_0 in X_t^{-1}(B_t))
   <= K * volume(X_t^{-1}(B_t))
   = K * volume(B_t).
```

The inequality is formalized in
[`VolumePreservingPositionBound.lean`](../verification/VolumePreservingPositionBound.lean)
as `VolumePreservingPosition.transported_mass_bound`. It assumes the initial
measure domination and volume preservation explicitly. The Lean proof does
not derive a flow map from the OpenAI velocity field.

For a uniform initial law on a finite-volume set `A`, take `K=1/volume(A)`.
In three dimensions, if `A` is a ball of radius `a` and the target is any ball
of radius `R`, the volume ratio is `R^3/a^3`. Therefore, for every `R<a`,

```
 P(position at time t lies within R of any chosen center) <= (R/a)^3 < 1,
```

uniformly for all times on which the smooth incompressible flow map exists.
Such an ensemble cannot become arbitrarily certain inside a fixed ball whose
volume is smaller than its initial support volume. This conclusion is
stronger than the isotropic-Gaussian countercheck in
[`openai-core-material-trajectory.md`](openai-core-material-trajectory.md#exact-positional-probability-check-in-the-linearized-gaussian-model),
but it remains a statement about absolutely continuous passive-tracer
ensembles, not single particles or molecules.

## Relation to alignment

The axial variational map previously audited has singular values
`Q^(C/2), Q^(C/2), Q^(-C)` and determinant one. Its infinitesimal directions
can align with the axis while an absolutely continuous packet preserves its
volume. The estimate above explains why directional alignment alone cannot
imply concentration of particle centers into a smaller fixed spatial region.
It does not say that the probability of every fixed ball is constant: the
bound is informative only when `K*volume(B_t)<1`, and a larger ball may contain
most or all of the transported ensemble.

The pinned OpenAI source declares smoothness and zero spatial divergence of
`FinalSlowBase.velocity` for each `t<1` in
`work/openai-f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/FinalSlowBase.lean`
(`velocity_smooth` and `divergence_zero`, source commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`). However,
`NavierStokes/ProblemStatement.lean` defines `candidateStatement` and notes
that it is not proved in that declaration module. This is not the status of the
whole pinned repository: `NavierStokes/ActualCandidateAssembly.lean` proves
`selected_candidate : ProblemStatement.candidateStatement`, and
`NavierStokes/R3/Theorem.lean` proves the whole-space breakdown statement.
Both targets build from a clean checkout at commit
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; see
[`openai-public-proof-audit-2026-10-02.json`](../evidence/lean-verification/openai-public-proof-audit-2026-10-02.json).
This correction establishes the repository's formal claim as Lean code, not
independent mathematical validity of every analytic argument or a molecular
model. The measure result below remains a kinematic consequence for any smooth
divergence-free field whose classical flow map exists. The application-specific
flow-map existence argument is supplied in the section below, using periodicity
and compactness for each fixed preterminal interval.
No endpoint flow map at `t=1` is asserted. The result does not cover a
point-mass initial law, an unbounded initial density, stochastic molecular
motion, finite-particle collisions, or a constitutive-viscosity response.

Reproduce the abstract measure inequality with
`sh runtime/lean-verification/check_volume_preserving_position_bound.sh` in the
prepared pinned Lean environment. The extension reports only `propext`,
`Classical.choice`, and `Quot.sound`. The classical Jacobian/change-of-variables
argument is not part of that formalized measure lemma; its candidate-specific
preterminal use is given classically above.

## Application to the pinned periodic candidate before its endpoint

The flow-map condition is available on every compact subinterval strictly
before `t=1`, conditional on the pinned candidate theorem. Its
`CandidateProperties` supplies a smooth velocity on `Ico 0 1 × Space`, unit
spatial periodicity, and zero divergence at every interior time. Fix
`0 < t0 < T < 1`. Periodicity lets the velocity descend to a smooth
time-dependent vector field on the compact flat torus `T^3`; smoothness on
`[t0,T] × T^3` gives bounded spatial derivative. Standard ODE existence and
uniqueness on a compact manifold therefore gives a flow of diffeomorphisms
throughout `[t0,T]`. Its derivative `J` obeys

```
J' = (D u)(t, X(t)) J,
(det J)' = (div u)(t, X(t)) det J = 0,
det J(t0) = 1.
```

Thus the flow preserves torus volume on every such interval. The source theorem
is a Lean-checked repository claim at the pinned commit, but this classical
ODE/change-of-variables bridge is not itself formalized in Lean here. The
deduction is conditional on the mathematical validity of that candidate
construction; it does not independently validate its proof.

Consequently, at any fixed `T<1`, an ensemble of passive tracers whose law at
`t0` has density at most `K` relative to torus volume satisfies
`P(X(T) ∈ B_T) ≤ K vol(B_T)` for every measurable, even moving, target set.
For a geodesic ball of radius `R<1/2` in the unit flat torus,
`vol(B_T)=4πR^3/3`, so if `K 4πR^3/3 < 1`, the ensemble cannot have probability
one inside that ball at that time. This is a finite-time, continuum passive-
tracer statement. It gives no bound uniform in the singular limit if the
initial density bound `K` or target radius changes with time; it says nothing
about a point-mass tracer, Brownian/molecular dynamics, or particle orientation.

This sharpens the application scope of the abstract measure lemma; it still
does not turn directional alignment of infinitesimal material vectors into
position certainty or a constitutive law.

## Occupancy bound for the shrinking Eulerian core

The [OpenAI paper's Section 2.1](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)
defines its core by fixed similarity-coordinate bounds `0≤X≤X_c`,
`|η|≤η_c<1`, with `τ=1-t=q(1-η²)`, `r²=2Xq`, and
`z=q^Dη`, `D=1/2-h`, `0<h<1/100`. These coordinates imply
`q≤τ/(1-η_c²)`. Therefore the core lies inside a cylinder with

```
r² ≤ 2 X_c τ/(1-η_c²),
|z| ≤ η_c (τ/(1-η_c²))^(1/2-h).
```

The cylinder's volume, and hence the core's volume, is bounded by

```
vol(C_τ) ≤ 4π X_c η_c (1-η_c²)^(-(3/2-h)) τ^(3/2-h).
```

If passive-tracer positions at a fixed preterminal time have density bounded
by `K`, volume preservation gives
`P(X_t(X_0)∈C_τ)≤K vol(C_τ)=O(τ^(3/2-h))→0`. The exponent is between 1.49
and 1.5. Thus this construction's shrinking Eulerian core does not become
occupied by an increasing fraction of any fixed bounded-density tracer
ensemble. This is compatible with the separate alignment of infinitesimal
material directions: core occupancy and tangent-direction alignment are
different events. It does not rule out an individual trajectory following the
axis, and says nothing about point masses, inertial or finite-size particles,
molecules, or constitutive viscosity. The algebra and exponent range are
checked in `tools/check_shrinking_core_mass_bound.py` and
`evidence/tests/shrinking-core-mass-bound.json`; the volume-preserving measure
lemma is Lean-checked, while its classical flow-map application remains under
the conditions stated above.
