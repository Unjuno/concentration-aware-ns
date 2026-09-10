# A material trajectory and deformation in the natural core

Source pin and core assumptions are those of openai-core-deformation.md.
This is a hand-derived consequence of that core, not a verified transfer to the
final assembled candidate. No numerical integration is used.

Let A=1/2+h, D=1/2-h, U(eta)=4eta+j, d=1-eta² and L=1-2h eta².
NaturalAxisData.exists_unique_root gives a root eta_* in (-j/4,-j/5) of

    D eta_* + (1-eta_*²) U(eta_*) = 0

under its SmallParameters assumptions (0<h,j<=1/1000). In particular d_*>0
and L_*>0. Put tau=1-t and define the physical axial curve

    q(t)=tau/d_*,   z(t)=eta_* q(t)^D,   X(t)=(0,0,z(t)).

The similarity identity tau=q-z²q^(2h) holds because 2D+2h=1. Thus eta is
exactly eta_* along the curve. Since A+D=1,

    z'(t)=-(D eta_*/d_*) q^(-A)=U(eta_*) q^(-A).

The last equality is the root equation. The transverse velocities are zero on
the axis, and the axial velocity has exactly this value. Hence X'=u_core(t,X)
for t<1 while the natural-core domain assumptions hold. The curve approaches
the origin from negative z, with increasing positive axial speed. This is a
material trajectory, unlike the fixed origin used in the previous calculation.

## Deformation along that trajectory

On the axis H=q^(-A)(4eta+j). Implicit differentiation yields
q_z=2eta q^A/L and eta_z=d/(q^D L). Therefore

    H_z=q^(-1)[4d-2A eta U(eta)]/L.

At eta=eta_*, the root equation reduces this to H_z=C/tau, with

    C=[4d_*²+2AD eta_*²]/L_* > 0.

The Cartesian Jacobian along the curve is

    G(t)=[ -C/(2tau)   -Omega(t)     0
            Omega(t)  -C/(2tau)     0
                  0           0    C/tau ],
    Omega(t)=q(t)^(-h-1) f(0,eta_*).

The diagonal and rotation generators commute. For a fixed initial t0<1,
let tau0=1-t0. The deformation matrix F'=G F, F(t0)=I, has singular values

    sigma_perp=(tau/tau0)^(C/2)   (twice),
    sigma_axial=(tau/tau0)^(-C).

It includes a transverse rotation with angle integral_(t0)^t Omega(s) ds.
The determinant is exactly one. For infinitesimal initial displacements with
nonzero axial component, the transverse-to-axial ratio decreases proportionally
to (tau/tau0)^(3C/2). This is directional alignment of infinitesimal material
separations in this core. It is not molecular orientation or finite-particle
packing, and does not establish a phase transition.

A small initial isotropic covariance, propagated by the linearized map F, has
two decreasing eigenvalues and one increasing eigenvalue; its determinant stays
constant. Thus directional alignment does not itself imply improved full-position
certainty. Finite neighborhoods may leave the core; the linearization is not a
uniform approximation for a fixed-size packet up to t=1.

## Transfer to the actual assembled field remains open

GermCandidateAssembly.potentialSum_eq_base_germ establishes neighborhood equality
of the potential sum to a base potential on the cutoff plateau, under the stated
zero-germ and local-finiteness hypotheses. MixedAxisPreservation also contains
mixedDiagonal_eq_cutBase_germ and directDiagonal_zero_germ. These are stronger
than mere axis value equality, but their target base is not automatically the
NaturalCore field used above.

FinalSlowBase.velocity uses a modulated coefficient family and a Borel-type
assembly. Its origin value is shown to retain j tau^(-A)e_z. To transfer this
trajectory and its Jacobian, verify the axis profile for nonzero eta, the
necessary derivatives, cutoff hypotheses along X(t), and the final periodic
assembly. Matching a value at the origin alone cannot establish these facts.

Source identifiers newly inspected: NaturalAxisData.exists_unique_root,
GermCandidateAssembly.potentialSum_eq_base_germ and origin_eventually_base,
MixedAxisPreservation.mixedDiagonal_eq_cutBase_germ,
FinalSlowBase.velocity and leading_origin. All refer to the existing fixed pin.

## Transfer advanced to FinalSlowBase (source-derived, not new Lean verification)

A further read of the actual coefficient assembly supplies more than the origin
value: EntranceAlignedBase.modulated_leading_axis states axial_0(0,eta)=4eta+j
for every eta in [-1,1], and modulated_positive_axis makes axial_n(0,eta)=0
for all n>0 there. FinalSlowBase.coefficients uses this family.

SlowBorelBase.streamFactor is q^(-A) times the slow sum of radial averages of
these axial coefficients. ProfileHistories.average_at_axis returns the coefficient
value at X=0. BaseResidual.slowSum_eq_leading_of_positive_zero removes all positive
terms exactly, for any cutoff schedule. Together, these identities give

    H_base(t,0,z)=q^(-A)(4eta+j)   for |eta|<1, t<1.

AxisymmetricFields.velocity_on_axis then gives the same axial particle ODE as
above. Smoothness allows differentiating this identity with respect to z along
the axis. The two transverse diagonal Jacobian entries are -H_z/2 and the axial
one is H_z. Thus the trajectory and the three deformation singular values carry
over to this smooth axisymmetric FinalSlowBase. Its transverse rotation may
differ; do not transfer the natural-core formula for Omega without checking the
swirl coefficients. Rotation does not alter the singular values in this axis
Jacobian structure.

This is a deductive extension of the inspected definitions and theorem statements,
not a newly compiled Lean proof. It does not yet complete transfer through every
actual mixed correction, cutoff, activation, periodicization, and chosen witness.
In particular, the neighborhood and cutoff conditions along the moving trajectory
must be checked in the actual assembled candidate, not just at the fixed origin.

## Terminal cutoff conditions along the moving trajectory

The cutoff check can be made quantitative in symbolic parameters. Along X(t),
q=tau/d_* and X(t) stays on the spatial axis. For the support domain
MixedAxisPreservation.localDomain(h,qbig), membership reduces to

    0 < tau < d_* qbig.

For the zeroth cutoff plateau, |scales(0) q|<1/2 reduces, if scales(0) is
nonzero, to tau<d_*/(2|scales(0)|). If scales(0)=0 it holds automatically.
TimeLocalization.activatedVelocity_eventuallyEq_late applies for t>3/4,
i.e. tau<1/4. All three restrictions therefore hold on a nonempty terminal
interval whenever qbig>0 and the schedule's first value is finite. They are
conditions along this actual moving trajectory, not only at the origin.

MixedAxisPreservation.mixedDiagonal_axis_jets explicitly transfers derivatives
of every order on its plateau, provided its PotentialStage and AngularSupport
hypotheses are instantiated. The actual candidate uses the initialized
GermCandidateAssembly interface, so that instantiation must still be reconciled
with its initial contribution and selected witness. Periodic spatial localization
and the final chosen-field identity also remain to be checked. We do not yet
claim the complete final-candidate trajectory theorem.
