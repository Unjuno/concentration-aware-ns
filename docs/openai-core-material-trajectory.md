# A material trajectory and deformation in the selected construction

Source pin and core assumptions are those of openai-core-deformation.md.
Current status: the source-derived neighborhood-equality chain to the selected
periodic candidate is completed in the final section below. The earlier sections
record intermediate scopes and the checks that were then outstanding. No new Lean
trajectory theorem has been compiled; this remains a hand-derived extension of
the pinned source. No numerical integration is used.

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

## Spatial localization and actual witness interface

SpatialLocalization.plateau is radialSquare(x)<1/32 and |z|<1/8. The trajectory
has zero radial coordinate, so it lies in that plateau whenever

    tau < d_* (1/(8|eta_*|))^(1/D).

The bound is positive because eta_*<0 and D>0. MixedPeriodicAssembly's
periodicVelocity_eventuallyEq states equality on a spacetime neighborhood to the
uncut mixed velocity at every plateau point. Thus spatial localization and
periodicization preserve all local derivatives there, not just the velocity
value. Together with the preceding time/cutoff bounds, this supplies a nonempty
terminal interval for all these geometric conditions.

ActualCandidateAssembly.Witness identifies its candidate velocity explicitly as
activatedVelocity(periodicVelocity(ASum,BSum)). Its witness theorem invokes
GermCandidateAssembly with initialPotential_axisZeroOn and
positivePotential_axisZeroOn. Consequently the remaining bookkeeping is the
initialized potential/direct sum's neighborhood equality to the FinalSlowBase
along this axis curve and its selected-schedule hypotheses. The outer
periodicization and time activation are now accounted for by named neighborhood
equalities and explicit trajectory bounds. This source audit has not compiled a
new theorem joining those facts into the final trajectory/deformation result.


## Completed source-level neighborhood chain for the selected periodic witness

The remaining initialized/direct-sum identities can be instantiated as follows.
Here a is any SelectedSchedule in ActualCandidateAssembly.Witness for the fixed
selected B and N0. Along the curve on the sufficiently late interval specified
above:

1. ActualCandidateAssembly.potentialStages is literally
   GermCandidateAssembly.potentialStages with initialPotential and
   positivePotential. Their AxisZeroOn hypotheses are supplied by the named
   initialPotential_axisZeroOn and positivePotential_axisZeroOn theorems.
2. MixedCandidateWitness.SelectedSchedule includes divergence of the real-valued
   schedule to infinity, and a(0)>=1. q is positive and continuous on t<1.
   Therefore GermCandidateAssembly.potentialSum_eq_base_germ applies at each
   axis point of the curve with q<qbig and a(0)q<1/2. It identifies ASum on a
   spacetime neighborhood with TailGaugePotential.finalPotential.
3. ActualCandidateAssembly.directStages is LocalAngularDiagonal.rawSeries of
   its actual directData. DirectAngularDiagonal.angularSum_axis_zero_germ,
   together with LocalAngularDiagonal.angularSum_eq_potentialSum, makes BSum
   zero on a spacetime neighborhood there. It uses the same schedule and
   positive continuous q, the open localSlowDomain, and zero radius.
4. Taking curls preserves neighborhood equality. TailGaugePotential's
   finalPotential_sameCurl identifies the base curl with FinalSlowBase.velocity
   for every t<1. Intersect with the open preterminal domain: the uncut actual
   mixed velocity is neighborhood-equal to FinalSlowBase along the curve.
5. MixedPeriodicAssembly.periodicVelocity_eventuallyEq preserves this equality
   in the spatial plateau. TimeLocalization.activatedVelocity_eventuallyEq_late
   preserves it for t>3/4. These are precisely the outer velocity operations
   in ActualCandidateAssembly.Witness.

Thus, as a source-derived mathematical consequence, the selected witness's
periodic candidate velocity agrees with FinalSlowBase on a spacetime neighborhood
of each sufficiently late point of the curve. All finite local derivatives
agree there. The trajectory is a material trajectory of that candidate on this
terminal interval, and its infinitesimal deformation has the singular values
derived above. The transverse rotation is that of FinalSlowBase, not assumed
equal to the original natural core's rotation.

An explicit sufficient upper bound on tau is the minimum of

    1/4, d_* qbig, d_*/(2 a(0)),
    d_* (1/(8|eta_*|))^(1/D).

Each quantity is positive; numerical values of the selected parameters have not
been extracted. This supplies an existence-level terminal interval, not a
numerically specified experiment. It applies to the explicitly constructed
periodic witness, not every solution or a claim of molecular alignment.

Validation distinction: the original configured NS target was independently
accepted by both kernels. The new trajectory/deformation consequence is a
hand-derived chain of inspected source identities with separate symbolic checks;
it has not itself been encoded and accepted by those kernels. Physical phase
transition, changing viscosity coefficients, finite-particle packing, and improved
three-dimensional position certainty remain unestablished.

## Viscous stress and local dissipation along this trajectory

For the derived strain S=diag(-C/2,-C/2,C)/tau, an incompressible Newtonian
fluid has viscous stress per unit density 2nu S. Contracting with grad u gives

    epsilon=2nu S:S=3nu C²/tau².

The skew rotation cancels exactly. At fixed positive nu this grows without bound
along the terminal trajectory, rather than tending to zero. The native selected
construction has nu=1; the formula with nu is a constitutive evaluation, not a
claim that the same unscaled solution works at every viscosity. The source's
viscosity rescaling also changes the field, time and forcing.

This distinguishes directional alignment from decreasing local viscous
conversion of kinetic energy. It does not compute nu*Laplacian(u), a second-
derivative quantity, nor its ratio to inertia, pressure or forcing. Large stress
or dissipation need not imply a large viscous force at the same point. A
pointwise divergence along one curve also does not establish divergent spatially
integrated dissipation. No temperature evolution or phase transition follows
without additional equations.

Reproduce the algebra with
`work/reference-check-env/bin/python -m tools.check_axis_dissipation` in the
recorded SymPy environment (or run that module with SymPy 1.14.0 installed).
Evidence: evidence/tests/openai-axis-dissipation.json.

## Axial viscous force: the missing radial derivative

The axisymmetric identity u_z=H+s H_s, s=(x²+y²)/2, gives exactly

    (Laplacian u)_z|axis = H_zz(t,0,z) + 4 H_s(t,0,z).

Indeed the coefficient of s in u_z is 2 H_s, and Laplacian_xy s=2.
Axis values of H determine H_zz but do not determine H_s. Consequently the
axis trajectory and strain alone cannot settle the viscous-force claim.

For the natural-core expression H=q^(-A)V(s/q,eta), the second term is
4 q^(-A-1) V_X(0,eta). Along the derived trajectory the material acceleration
is exactly A U_* d_*^A tau^(-A-1) in the axial direction. Thus this radial
viscous contribution has the same time exponent as material acceleration;
its coefficient must be determined before asserting relative suppression.
The axial H_zz contribution scales as q^(-A-2D), whose ratio to acceleration
scales as tau^(2h). This decay of one contribution does not prove decay of
the full Laplacian. These exponent statements concern the natural core;
transferring off-axis radial derivatives to FinalSlowBase requires its actual
modulated coefficients, not just the established common axis value.

This identifies a concrete remaining calculation: extract H_s for FinalSlowBase
on eta=eta_*, including the positive-order slow-sum terms, then compare the
complete axial Laplacian with acceleration, pressure gradient and forcing.
No conclusion about a viscosity drop is claimed here.

## Radial coefficient for the actual FinalSlowBase assembly

Write a_j(X,eta) for FinalSlowBase's modulated axial coefficient of order j,
chi for the scalar cutoff used by cutStage, and k_j for its selected integer
scale. These symbols avoid confusing the coefficient family with A=1/2+h.
ProfileHistories.average is exactly integral_0^1 a_j(v X,eta) dv. Smoothness
therefore gives partial_X average(a_j)(0,eta)=partial_X a_j(0,eta)/2.
PhysicalCoordinateBounds.qCoord depends only on time and z; consequently q
and eta are independent of physical s at fixed time,z, and X=s/q.
SlowBorelBase.slowSum retains the order-zero coefficient uncut and adds
cutoff-weighted positive orders with powers q^(2hj). Thus at the axis,

    B(q,eta) = partial_X a_0(0,eta)
               + sum_(j>=1) chi(k_j q) q^(2hj) partial_X a_j(0,eta),
    H_s = (1/2) q^(-A-1) B(q,eta),
    (Laplacian u)_z = H_zz + 2 q^(-A-1) B(q,eta).

At each fixed q>0 this cutoff sum is locally finite under the selected scale
hypotheses, so differentiation here is a finite local operation. It does not
justify taking q to zero term by term without the weighted derivative bounds.
The established identity a_j(0,eta)=0 for j>0 does NOT imply that its X
derivative is zero. This is precisely the information absent from axis values.

On eta=eta_* the material acceleration is A U_* d_*^A tau^(-A-1),
so the signed axial ratio of the radial viscous contribution to acceleration is

    2 nu B(q,eta_*) / (A U_* d_*),   q=tau/d_*.

The remaining axial H_zz contribution has a ratio proportional to tau^(2h),
as derived above. Therefore decay of the complete axial viscous-force ratio
requires control of B(q,eta_*); it cannot be inferred from alignment. Even
this axial comparison alone would not resolve pressure and forcing balance.
The construction's native nu is one. This is a source-derived formula, not
a computed coefficient value or a new Lean theorem. The next unresolved
step is to determine partial_X a_0 and bound the full positive-order remainder.

Inspected definitions: ProfileHistories.average; PhysicalCoordinateBounds.qCoord,
xCoord and etaCoord; SlowBorelBase.positiveCoefficient, slowStage, slowSum,
physicalProfile, bundleComponent and streamFactor. Source byte hashes are
recorded in evidence/openai-source/radial-coefficient-sources.json.

## Natural-core leading coefficient is strictly nonzero at the root

Evaluate IsNaturalSolution.axial_equation at X=0. NaturalAxisBridge defines
radialDifferential 1 U = X U_XX + U_X. Axis values and their eta derivatives
therefore give the exact identity

    2 L(eta) U_X(0,eta) = -Z(h,j,P0)(eta).

Here Z is exactly NaturalAxisData.Z, including the pressure value and derivative;
no pressure term was dropped. At the selected negative root, PressureData
(negative pressure <= -1 and eta P0' >= 0) implies
Z_* > j/5 by Z_at_root_lower / exists_root_with_positive_Z. Since L_*>0,

    U_X(0,eta_*) = -Z_*/(2 L_*) < -j/(10 L_*) < 0.

For the natural core V is the radial average of U, so B=U_X and the signed
radial viscous-force / material-acceleration ratio equals

    -nu Z_* / (L_* A U_* d_*),

which is strictly negative and independent of tau. U_*>0 follows from the
root equation and eta_*<0. The axial H_zz contribution has a ratio tending
to zero as tau^(2h). Thus the full axial viscous-force ratio for the natural
core tends to this nonzero negative constant: alignment on this trajectory
does not suppress the relative axial viscous force in that core.

Scope is essential: applying this conclusion to the completed candidate still
requires proving that its leading modulated profile has the same radial jet
near this axis and that the positive-order derivative remainder tends to zero.
The previous axis-value transfer alone cannot supply either fact. This is a
hand-derived consequence of inspected source equations, not a new Lean result.

## Leading radial jet survives the finite modulation

The leading coefficient transfer can be strengthened beyond axis values.
EntranceAlignedBase.modulated_zero_fields identifies a_0(X,eta) with
v.profiles.U(X,eta) for X>=0 and |eta|<=1. The actual finiteModification
certificate satisfies AssembledSlowBase.FiniteModification.fields: inside
X<=lo it identifies v.profiles.U with the nominal W.profiles.U.
More directly, EntranceAlignedBase.modified_ACT_fields identifies it with
(nominalACT W).U whenever 0<=X<cutoffInner and eta belongs to S.
S is open and contains [-1,1], and the cutoff radius is positive.

Fix eta=eta_* in (-1,1). These identities hold on a right interval in X
starting at zero, rather than merely at X=0. Both coefficient functions are
smooth at the axis, so their ordinary X derivatives equal the common right
derivative. Consequently

    partial_X a_0(0,eta_*) = partial_X (nominalACT W).U(0,eta_*).

Thus the finite modulation itself does not alter this leading radial jet.
This argument does not use a claim that the positive-order terms vanish with
their derivatives. It also does not silently equate the ACT normalization
with NaturalProfile's unscaled X: the remaining transfer step is to trace
ActivationContinuation's natural-collar identity and any coordinate/amplitude
scaling. A nonzero scale factor must be retained when transferring the
previous natural-core value -Z_*/(2L_*). The positive-order remainder bound
is still required for the final asymptotic force ratio.

## ACT-to-natural normalization check

StressActivation.FromReference.histories stores FromReference.U as its axial
field. Its definition returns N.refU on X<=N.endpoint; ReferencePath.refU
returns N.U on that same interval. ReferencePath.Input.ofNatural assigns
U:=F.U directly. Therefore this initial collar introduces no extra coordinate
or amplitude multiplier between the ACT axial field and the natural family's
physical U. The endpoint is positive, giving a right interval at the axis.

NaturalProfile.ProfileFamily.U already equals the affine-rescaled function
U_axis(eta)+(1/Lambda)*F.u(Lambda X,eta). Differentiation cancels the two
Lambda factors. This rescaling is already included in IsNaturalSolution;
applying it a second time would be an error. Together with the finite-modulation
jet identity above, the leading derivative is consequently

    partial_X a_0(0,eta_*) = -Z_*/(2 L_*) < 0.

The remaining issue for B(q,eta_*) is now the positive-order derivative
remainder only. Its vanishing requires a derivative-level asymptotic estimate
for the selected slow sum; local finiteness at each q>0 alone is insufficient.
This transfer remains a source-derived argument, not newly compiled Lean code.
