# What incompressibility does and does not imply for tracer certainty

This note gives a general continuum result relevant to the proposed inference
from local stretching/alignment to increasingly certain particle positions.
It concerns passive point tracers in a prescribed smooth incompressible
velocity field. It is not a molecular model and does not cover inertial,
Brownian, interacting, compressible, or finite-size particles.

Let `u(t,x)` be sufficiently smooth that its flow map `X(t,a)` exists as a
diffeomorphism on the time interval in question:

    dX/dt = u(t, X),       X(0,a)=a.

The deformation matrix `F=D_a X` obeys `dF/dt=(D_x u)(t,X) F`. Jacobi's
determinant identity gives

    d/dt det(F) = (div u)(t,X) det(F).

Since `det(F(0))=1`, incompressibility `div u=0` implies `det(F)=1` for all
times. If initial tracer locations have probability density `rho_0`, the
change-of-variables formula therefore gives

    rho_t(x) = rho_0(X(t,.)^(-1)(x)) / |det D_a X| = rho_0(X^(-1)(x)).

Consequently every essential-value distribution of the density is preserved.
In particular, `||rho_t||_p=||rho_0||_p` for every `1<=p<=infinity` (when
defined), so its peak density does not grow. If differential entropy exists,
`h(rho_t)=h(rho_0)` as well. These are general consequences of smooth
volume-preserving transport, not special to the OpenAI construction.

This does **not** say that every positional event has constant probability.
The covariance can become highly anisotropic, and probability in a chosen
tube or observation window can increase or decrease. The local derivative can
also align infinitesimal separation directions. Those are distinct
observables. The exact affine-Gaussian example and its geometry-dependent tube
versus finite-cylinder probabilities are recorded in
[`particle-position-probability.md`](particle-position-probability.md).

For one known initial point, a unique flow map gives a deterministic tracer
trajectory while the smooth-flow assumptions hold. For an uncertain initial
position, later uncertainty is the pushforward of the initial distribution;
the PDE does not specify that prior distribution. A local flow derivative
describes only infinitesimal separations, not a finite cloud unless a separate
nonlinear remainder estimate keeps that cloud in the validity region.

Finally, the constant-viscosity incompressible Navier–Stokes model uses
`tau = 2*mu*D(u)` with prescribed material viscosity `mu` (and
`nu=mu/rho_material` for constant mass density). The equations contain no
rule that lowers `mu` when speed or alignment crosses a threshold. Such a
claim requires a different constitutive law and a material-scale model or
measurement. A continuum velocity-gradient theorem alone does not supply
that bridge.

## Scope boundary

The determinant and density transport identities hold only while the flow is
a smooth diffeomorphism. They do not prove that a singular flow has a unique
continuation through its singular time. They also do not rule out clustering
for inertial or compressible particles, where the particle velocity field can
have nonzero divergence, or for interacting stochastic models. Those
mechanisms require separate equations and separately validated parameters.

The general 3-by-3 determinant differentiation and a diagonal affine-Gaussian
control are checked by `python -m tools.check_incompressible_tracer_density`;
the JSON record is
`evidence/tests/incompressible-tracer-density-invariant.json`. The script
checks symbolic algebra only and does not numerically solve a flow.
