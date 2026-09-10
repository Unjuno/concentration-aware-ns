# Local deformation extracted from the pinned natural core

Pin: 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538. This is a direct calculus
consequence of the natural-core definitions and IsNaturalSolution assumptions,
not a new Lean theorem or an extracted trajectory of the final assembled field.
The user's specific hypothesis is concentration -> filament deformation ->
alignment/predictability -> reduced relative viscous influence. We examine the
actual core rather than substitute the generic Burgers-vortex example.

## Source mapping

All links refer to that pin in openai/NavierStokesAndEuler:

- [NaturalAxisData.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/NaturalAxisData.lean): A=1/2+h, D=1/2-h, axis profile U(j,eta)=4eta+j.
- [SimilarityCoordinates.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/SimilarityCoordinates.lean): tau=q-z²q^(2h), eta=z/q^D.
- [NaturalProfile.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/NaturalProfile.lean): IsNaturalSolution.average_axis fixes V(0,eta)=4eta+j on an open interval containing zero.
- [NaturalCore.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/NaturalCore.lean): H=q^(-A)V(s/q,eta), K=-q^(-h) integral_0^(s/q) f(X,eta)dX, s=(x²+y²)/2.
- [AxisymmetricFields.lean](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/AxisymmetricFields.lean): u_x=-x H_z/2+y K_s, u_y=-y H_z/2-x K_s, u_z=H+s H_s.

## Instantaneous strain at the origin

Fix t<1 and put tau=1-t. At s=z=0, q=tau, q_z=0 and eta_z=tau^(-D).
Consequently H_z=4 tau^(-A-D)=4/tau. Also
K_s=-tau^(-h-1) f(0,0). Writing Omega=tau^(-h-1) f(0,0), direct
Cartesian differentiation gives

    grad u(t,0) = [ -2/tau   -Omega   0
                     Omega  -2/tau   0
                       0        0   4/tau ].

A separate symbolic curl/Jacobian calculation using the sufficient profile Taylor
jets agrees; see evidence/tests/openai-core-strain-symbolic.json. This does not
verify the full candidate or its trajectories.

Its symmetric part is diag(-2,-2,4)/tau. The two transverse directions contract
instantaneously, while the axial direction stretches; the skew part rotates
transverse displacements. The trace is zero, as required by incompressibility.
For an infinitesimal separation present at this point at this instant,

    (1/2) d|delta x|²/dt = [-2(delta x²+delta y²)+4 delta z²]/tau.

This supports a local filament-deformation mechanism within the core. It does
not show shrinking molecular sizes, phase transition, decreased viscosity, or
concentration of the full three-dimensional position probability distribution.

Crucially u(t,0)=j tau^(-A)e_z with j>0, so the fixed origin is not a material
trajectory. Integrating the eigenvalues above at the fixed origin does not give
the deformation of an actual particle packet. That requires X'=u(t,X), followed
by F'=grad u(t,X)F. Rotations and moving strain directions must be retained.

## What the shrinking core width says about viscosity

At z=0, a fixed positive similarity radius X=s/q gives r²=2X tau. This is a
profile contour scale, not a proven material-particle radius. Comparing the
axial strain scale a=4/tau with the dimensional diffusion scale nu/r² gives

    a r²/nu = 8X/nu.

Thus this particular scale comparison is constant as t approaches 1 at fixed X
and fixed nu (the native core equation uses nu=1). Accelerating strain and a
shrinking contour alone do not demonstrate asymptotically vanishing relative
viscosity in this core. This is not an exact ratio of PDE terms: actual radial
and axial derivatives, profile coefficients, cancellations and forcing remain
to be evaluated. Changing nu using the full solution scaling must also rescale
time and forcing, rather than insert nu into the same fixed core unchanged.

## Remaining transfer checks

1. Establish which first and second spatial jets of the final assembled candidate
   coincide with this core, and in which time-dependent neighborhood. Agreement
   of velocity values on the axis alone is insufficient for derivative equality.
2. Derive or bound genuine material trajectories and their deformation matrices
   while they remain in that neighborhood.
3. Compare actual viscous, advective and forcing terms, with explicit treatment
   of zeros in denominators; a heuristic rate ratio is not that calculation.
4. Define the alignment and uncertainty observables before claiming improved
   predictability or inferring a microscopic transport coefficient.

An actual core material trajectory and its infinitesimal deformation are now
derived in [the trajectory note](openai-core-material-trajectory.md). Transfer to
the final assembled field remains open.
