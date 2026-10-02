# Adversarial audit of the particle-alignment inference — 2026-10-02

This is an analytical audit of the continuum-flow interpretation. It uses the
repository's recorded OpenAI source pin and formal artifacts; it does not use
CFD output to infer a mathematical or physical result.

## Precisely what the tangent map says

On the selected terminal axis trajectory, the audited deformation has singular
values `Q^(C/2), Q^(C/2), Q^(-C)` and determinant one, with
`Q=(1-t)/(1-t0)` and `C>=7999999/2000000>1`. For an infinitesimal displacement
`h=(h_perp,h_z)` with `h_z != 0`,

```
|Fh_perp|/|Fh_z| = Q^(3C/2) * |h_perp|/|h_z| -> 0.
```

So the direction of every such infinitesimal separation approaches the axis.
The exactly transverse plane is exceptional. The two transverse contractions
are balanced by axial expansion: `det(F)=1`. This proves neither collapse of a
material volume to a line nor concentration of absolute positions.

The phrase “probability of alignment” needs an added probability space. Under
uniform initial unoriented directions, `c=|h_z|/|h|` is uniform on `[0,1]`.
For a fixed cone half-angle `theta*` and `m=tan(theta*)`, the exact linear-map
probability outside the cone is

```
Q^(3C/2) / sqrt(m^2 + Q^(3C))
  ~ Q^(3C/2)/m.
```

For an arbitrary fixed direction law it is enough that the law give zero mass
to the transverse plane for the limiting aligned fraction to be one; this
qualitative assumption supplies no universal convergence rate. With a
quantified anti-concentration bound `lambda{c<epsilon}<=L*epsilon^beta`, the
recorded conditional finite-packet argument gives a cone-failure bound of
`L*Q^beta` for sufficiently small `Q`.

## Finite displacements and the key scale distinction

The smooth selected field has a Lean-checked equality ball of radius
`rho(Q)=rho0*Q^(1/2)` and spatial Hessian bound `M(Q)/2<=k0*Q^(-40)` on a
parameter-dependent terminal interval. The constants, starting time and
cutoff are existential, not numerically extracted. A classical Taylor and
variation-of-constants comparison, conditional on those envelopes, gives a
sufficient initial radius `delta<=K*Q^43` for a fixed non-transverse direction
to stay inside any fixed positive-angle axis cone. `K` depends on unknown tube
and Hessian constants. The comparison is not itself formalized end to end in
Lean.

The distributional extension uses the smaller initial radius `delta0*Q^44`.
For laws with no transverse atom, it proves conditional endpoint direction
alignment in probability. But it does not establish fixed-size-packet
alignment. Indeed, the same bound gives absolute endpoint displacement at
most `O(Q^40)` while, on a set of directions whose probability tends to one,

```
|Y(T)-X(T)| / initial_radius >= (1/2)*Q^(1/2-C) -> infinity.
```

These statements are compatible because the initial radius already shrinks
like `Q^44`. Absolute closeness to the reference trajectory is not contraction
relative to the initial packet size, and a direction law for tangent vectors
is not a probability law supplied by the Navier–Stokes construction.

## Independent checks and remaining boundary

The source-mapped deformation and exponent enclosure are recorded in
`verification/AxisForceSign.lean`, `verification/SpatialHessianTransfer.lean`,
`evidence/lean-verification/axis-force-sign.json`, and
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`. The
symbolic scaling check was freshly run with the pinned verification
environment: `tools.check_packet_radius_scaling` returned success for the
`Q^43` sufficient radius, the conditional `Q^44` direction-law extension,
the anti-concentration rate, and the tangent-map probability. Seven focused
tests covering the packet, tracer probability, and shrinking-core statements
passed. These checks verify algebra and stated implications under assumptions;
they do not verify the upstream proof independently, extract the unknown
constants, or simulate finite particles.

The admissible conclusion is therefore limited to infinitesimal continuum
directions and a conditional family of shrinking continuum tracer packets.
The current evidence gives no fixed-size finite-particle result, no molecular
orientation law, no particle-center certainty, and no phase-transition or
viscosity constitutive law. Those require a finite-size model, its forcing and
boundary regime, material parameters, and an independently validated bridge
from the continuum field. The separate smooth manufactured-solution CFD
benchmark cannot fill that gap or validate the singular construction.
