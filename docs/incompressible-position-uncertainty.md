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
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`). Applying the volume argument to
that field additionally presumes its classical flow map exists as a smooth
diffeomorphism on the interval under consideration. No endpoint flow map at
`t=1` is asserted. The result does not cover a point-mass initial law, an
unbounded initial density, stochastic molecular motion, finite-particle
collisions, or a constitutive-viscosity response.

Reproduce the abstract measure inequality with
`sh runtime/lean-verification/check_volume_preserving_position_bound.sh` in the
prepared pinned Lean environment. The extension reports only `propext`,
`Classical.choice`, and `Quot.sound`. The classical Jacobian/change-of-variables
step and the application-specific global flow-map hypotheses remain separate
from that formalized measure lemma.
