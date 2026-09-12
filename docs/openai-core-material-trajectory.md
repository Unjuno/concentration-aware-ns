# A material trajectory and deformation in the selected construction

Current result (source-derived; not a new Lean theorem): along the selected
terminal axial trajectory, infinitesimal material separations align while the
axial viscous-force/material-acceleration ratio tends to a strictly negative,
nonzero constant. The derivative-level slow-sum remainder estimate completes
the argument in the final sections. Earlier headings saying a transfer
"remains open" record intermediate history and are superseded by those sections.

Reproducible algebra check: with SymPy 1.14.0 installed, run
`python -m tools.check_axis_force`. It checks the Cartesian Laplacian factor,
the natural axial equation's sign, and the axial derivative exponent. Output:
`evidence/tests/openai-axis-force-symbolic.json`. These checks do not verify
all theorem hypotheses or the source-transfer chain.


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

## Derivative remainder vanishes for the selected schedule

FinalSlowBase.scales_admissible gives AdmissibleScales for the actual seven-
component coefficientBundle on innerBox 0 (boxRadius W upper). Component 5
is the axial coefficient itself. Projecting to this component (a continuous
linear map of norm at most one) retains the admissible derivative bounds.
The fixed point w_*=(0,eta_*) belongs to this box: |eta_*|<1 and the box
radius bounds the positive activeRight radius.

Apply SlowBorelBase.exists_ordinary_uncut_tail with M=1, Jmin=1, P=2h
to the projected axial coefficient family. It supplies a finite J>=1 and
delta>0 such that the full first derivative of slowSum-uncutPrefix is bounded
by 2^(-J) q^(2h) at (q,w_*) for 0<q<delta. Evaluate that derivative on the
unit X direction. The finite uncut prefix has derivative

    partial_X a_0(w_*) + sum_(j=1)^J q^(2hj) partial_X a_j(w_*).

Each coefficient here is a fixed finite real number. For 0<q<=1, every
q^(2hj)<=q^(2h). Thus the finite prefix difference and the bounded tail
both are O(q^(2h)), establishing

    B(q,eta_*) = -Z_*/(2L_*) + O(q^(2h)).

This uses a derivative bound for the entire remaining sum, not an exchange
of a limit with infinitely many terms. No explicit numerical remainder
constant or usable finite-time crossover is obtained from the existential
schedule theorem.

Combining with q=tau/d_* and the earlier H_zz estimate gives, for the selected
completed periodic witness on its terminal material trajectory, at native nu=1,

    (Laplacian u)_z / (D_t u)_z
        = -Z_*/(L_* A U_* d_*) + O(tau^(2h)).

The limit is strictly negative and nonzero. The previously established local
spacetime equality to FinalSlowBase transfers the required velocity derivatives
to the selected witness. Consequently directional alignment does not imply
vanishing relative axial viscous force in this particular construction.
This result is specific to the selected trajectory and witness; it is not a
universal molecular model, a phase-transition statement, or a solution for
viscosity as a material property. Pressure and forcing have not been separately
quantified. The whole new consequence remains hand-derived from the pinned
source; no additional Lean theorem has been compiled.

## Machine-checked scalar part

`verification/AxisForceSign.lean` now proves both negativity of the actual
scalar expression and existence of a root with that property, from
SmallParameters, PressureData and positive viscosity. Positivity of the actual
L, A, U and d factors is derived internally. Lean reports only propext,
Classical.choice and Quot.sound for both theorems.

Replay with `sh runtime/lean-verification/check_axis_sign.sh` after provisioning
the pinned checker image and cans-lean-verification volume using the existing
verification setup. The runner mounts both original sources and extensions
read-only and disables networking. This is a Lean kernel check, not a second
nanoda validation. It does not yet formalize the field-derivative identity,
trajectory transfer or asymptotic remainder argument. The complete force-limit
conclusion above therefore remains hand-derived.

The additional theorem `natural_axis_radial_identity_from_solution` now derives
`2 L partialY u = -Z` directly from IsNaturalSolution, domain membership and
an interior eta. It derives the axial-value and eta-derivative identities from
the solution's local axis equalities, rather than assuming their numerical
values separately. The pinned Lean kernel accepts it with the same three
reported axioms. This checks the natural-profile PDE-to-radial-derivative step;
the completed-field transfer and asymptotic limit remain outside this theorem.

`natural_radial_derivative_negative_at_root` additionally combines the natural
PDE identity with the root/pressure sign theorem, deriving partialY u(0,eta)<0.
It assumes IsNaturalSolution, membership of the axis point in its domain,
interiority in the eta window, SmallParameters, the root equation/interval,
and PressureData. This is a statement about the actual natural profile
derivative, not merely an independently named scalar. It still does not
formalize its transfer through the complete assembly or the force-ratio limit.

The quantitative companion theorem `natural_radial_derivative_quantitative`
proves `2 L partialY u < -j/5` under those same natural-solution and root
hypotheses. Since the actual L is positive, this is the previously derived
strict bound `partialY u < -j/(10 L)`. It supplies a margin from zero for the
leading term. Turning that margin into an explicit finite-q guarantee for the
completed field still requires a quantitative remainder constant and cutoff
scale; an existential asymptotic estimate does not provide a numerical time.

`selected_axial_component_derivative_tail` now instantiates the first-derivative
remainder bound on FinalSlowBase.coefficients and FinalSlowBase.scales, using
their actual smoothness and admissibility theorems. It applies on the selected
innerBox, assuming positive F.data.h and the source's certificate/witness
objects. Thus admissibility is no longer supplied as a separate unconnected
hypothesis. The next formal step remains evaluating the derivative on the X
direction and proving convergence of the finite positive-order prefix.

`finite_prefix_derivative_tends_leading` combines the finite weighted-sum
derivative rule and positive-power limit. For a fixed finite prefix with
derivatives at X=0, its X derivative converges to the leading derivative as
q tends to zero. This is now one Lean theorem rather than two disconnected
facts. Identifying this generic prefix with SlowBorelBase.uncutPrefix and
combining its limit with the selected tail estimate remain formalization steps.

`chart_radial_derivative_eq_fderiv` checks the chain-rule identity between
the ordinary derivative of X -> g(q,X,eta) and the Frechet derivative of g
applied to (0,1,0), under DifferentiableAt. This supplies the coordinate
interpretation needed for the tail estimate. The remaining formal bridge
identifies the order-one iterated derivative with that Frechet derivative
and combines the tail and prefix limits for the selected smooth slow sum.


## Ordinary radial derivative of the actual slow-sum tail

`axial_radial_tail_tends_zero` in `verification/AxisForceSign.lean` now
connects the first-jet remainder estimate to the ordinary X derivative of
`slowSum - uncutPrefix` for axial bundle component 5 at `(q,(0,eta))`.
For positive h, smooth coefficients, admissible scales and `(0,eta)` in
the controlled inner set, it proves that there exists J >= 1 for which
this derivative tends to zero as q approaches zero from above.
Smoothness is derived from the source definitions and admissibility;
ordinary differentiability of the remainder is not an extra assumption.
The pinned Lean check passes without sorryAx. This does not yet formally
combine the prefix and tail limits or transfer the result through the
assembled physical field to the full viscous-force ratio.


## Full slow-sum radial derivative limit

`axial_radial_derivative_tends_leading` now combines the finite-prefix
limit and the ordinary radial derivative tail limit. Under positive h,
smooth coefficients, admissible scales and `(0,eta)` in the controlled
inner set, the X derivative of the full axial component-5 slow sum at
`(q,(0,eta))` tends to the X derivative of its zeroth coefficient as
q approaches zero from above. Coefficient differentiability is derived
from smoothness. The proof uses a finite prefix plus a controlled
remainder; it does not assume interchange of an infinite sum and limit.
The pinned Lean check passes without sorryAx. The remaining formal gap
is transfer through the selected assembled physical field and combination
with the physical Laplacian and material-acceleration identities.


## Selected FinalSlowBase instance

`selected_axial_radial_derivative_tends_leading` instantiates the full
slow-sum derivative limit with `FinalSlowBase.coefficients` and
`FinalSlowBase.scales`. It derives smoothness and admissibility from the
source theorems. For every eta in [-1,1], it also proves membership of
`(0,eta)` in the controlled inner box using positivity of the active
right radius. Thus no independent admissibility or box-membership
assumptions are left in this selected-instance theorem. The remaining
hypotheses are the source certificate, modulation witness and positive h.
The pinned Lean check passes without sorryAx. Identifying the leading
coefficient derivative with the natural solution derivative still needs
a formal one-sided-to-ordinary derivative argument: the source's
`EntranceAlignedBase.modulated_zero_fields` supplies equality on X >= 0,
which is not a two-sided neighborhood of X = 0. The physical-field and
force-ratio transfers remain unformalized.


## One-sided agreement and the leading derivative

`deriv_eq_of_nonnegative_agreement` proves equality of ordinary derivatives
at zero for two differentiable scalar functions that agree on X >= 0,
using uniqueness of the derivative within the closed right half-line.
`selected_leading_derivative_eq_modulated` applies it to the actual
component-5 zeroth coefficient and `v.profiles.U`, using
`EntranceAlignedBase.modulated_zero_fields`. The coefficient's
smoothness is derived from the source. This theorem currently retains
an explicit differentiability hypothesis for the modulated U slice;
deriving it from the profile's open-domain smoothness is still needed.
Both statements pass the pinned Lean check without sorryAx. Neither
statement yet identifies the modulated derivative with the natural
solution or proves the full physical force-ratio limit.


## Modulated-profile limit without an extra differentiability assumption

The explicit differentiability hypothesis described in the preceding section
has now been removed from `selected_leading_derivative_eq_modulated`.
`LoopData.parameters_contains` and `domain_nonnegative` place the axis point
inside the profile's open domain; `v.profiles.U_smooth` then supplies ordinary
slice differentiability by composition with X -> (X,eta).
`selected_axial_radial_derivative_tends_modulated` combines this identity
with the selected slow-sum limit. Its conclusion is the ordinary derivative
of the actual modulated U profile, without an extra smoothness hypothesis.
All printed statements pass the pinned Lean check without sorryAx.
Transfer from the modulated profile to the natural solution and then to
the assembled physical-field force ratio remains to be formalized.


## Removal of the finite modulation at the axis

`modulated_axis_derivative_eq_original` uses `Witness.fields_outside`
and positivity of the modulation's left endpoint to prove two-sided
neighborhood equality of the modulated and original U slices at X = 0.
Unlike coefficient-extension equality, this step requires no half-line
argument: the source theorem holds throughout that neighborhood.
`selected_axial_radial_derivative_tends_original` therefore identifies
the selected slow-sum derivative limit with the derivative of
`W.profiles.U` at `(0,eta)`. Both pass the pinned Lean check without
sorryAx. The next formal identification is between this original nominal
profile and the natural solution; the physical-field force-ratio limit
is still not an end-to-end formal theorem.


## Natural-profile derivative identification

`original_axis_derivative_eq_natural` uses `Controls.natural_prefix`
to identify the original nominal U derivative with
`W.axis.natural.profile.family.U` at X = 0. This requires the source
prefix condition `1 <= W.axis.scale`; it is explicit in the theorem.
The equality holds in a two-sided neighborhood below 4/scale, and the
positive scale supplies that neighborhood. No coordinate rescaling is
inserted in this equality.
`selected_axial_radial_derivative_tends_natural` composes the entire
selected-coefficient, modulation and nominal-profile chain to identify
the slow-sum derivative limit with this natural-profile derivative.
Both statements pass the pinned Lean check without sorryAx. Discharging
the scale condition for the final selected witness, applying the natural
PDE sign identity, and transferring to the physical force ratio remain
formalization work.


## Scale restriction removed from the natural derivative limit

The previous section's additional `1 <= W.axis.scale` hypothesis is no
longer needed. The full-prefix theorem used it to fit 4/scale below Xi,
but equality near X = 0 only requires the intersection X < 4/scale and
X < Xi. Both endpoints are strictly positive in the source.
`original_axis_derivative_eq_natural` now composes
`physical_before_Xi` with `seed_initial` on that neighborhood, using
only the witness's existing separation and positive-scale properties.
`selected_axial_radial_derivative_tends_natural` consequently also has
no extra scale lower bound. The updated pinned Lean check passes without
sorryAx. Natural PDE sign and physical force-ratio connections remain.


## Eventual sign of the selected axial radial derivative

`selected_natural_derivative_negative` applies the natural PDE sign lemma
to the actual family stored in W.axis.natural.profile.
`selected_axial_radial_derivative_eventually_negative` combines that
negative limit with the selected slow-sum convergence theorem: for all
sufficiently small positive q, the component-5 X derivative is negative.
The statements retain explicit axis-domain membership, window membership,
root interval/equation, and PressureData hypotheses. These hypotheses
have not yet been discharged here for a final selected root. Both pass
the pinned Lean check without sorryAx. This is a chart-component sign,
not yet a sign theorem for the physical Laplacian or the full force ratio.


## Root existence and domain hypotheses discharged

`exists_selected_root_with_negative_radial_derivative` obtains a root
in (-j/4,-j/5) from the source root-existence theorem and derives its
membership in [-1,1], the natural analytic window and the axis domain.
`OutgoingProfile.natural_axis_pressureData` supplies PressureData from
the explicit remaining bound `2 <= F.data.core.P`. The conclusion is
existence of a root at which the selected component-5 radial derivative
is negative for all sufficiently small positive q. The pinned Lean
check passes without sorryAx. This removes the separately assumed root,
pressure datum and domain conditions; it does not yet discharge the P
bound for the final witness or prove the physical force-ratio limit.


## Prepared outgoing amplitude bound

`prepared_root_with_negative_radial_derivative` specializes the root/sign
result to `PreparedOutgoing.PreparedProfile`, using its stored
`amplitude_lower` proof of P >= 2. No separate pressure-amplitude
hypothesis is required for this statement. A nominal witness for this
prepared profile, its cone certificate and modulation witness remain
inputs; this does not itself construct or identify the final periodic
witness. The pinned Lean check passes without sorryAx. Full physical
Laplacian and material-acceleration transfer is still unformalized.


## Cartesian Laplacian bridge

`physical_axial_laplacian_on_axis` specializes the source Cartesian
`spatialLaplacian_velocity` theorem at (0,0,z), under its SliceC2
hypotheses. It proves that the axial component equals 2 U_s + U_zz,
where U here denotes the axial velocity profile and s=(x²+y²)/2.
The pinned Lean check passes without sorryAx. This U must not be
confused with the stream potential H: U=H+s H_s is the additional
identity needed to obtain the previously symbolic 4 H_s + H_zz formula.
Instantiation with the actual slow-base physical profiles and transfer
through the final assembled field remain open formalization steps.


## Stream-to-velocity radial derivative factor

`stream_axial_radial_derivative_on_axis` proves
partialS (H + s partialS H) = 2 partialS H at s = 0, assuming
ordinary differentiability of H and partialS H at the axis point.
It uses the full Frechet product rule and the actual source partialS
definition. The pinned Lean check passes without sorryAx. Combined
algebraically with the preceding Cartesian formula, the radial part
is therefore 4 partialS H. The axial second-derivative identity and
instantiation of all smoothness hypotheses for the constructed field
are still required before claiming the full physical identity formally.


## Axial second derivative bridge

`axial_slice_derivative_eq_partialZ` identifies the source partialZ
with an ordinary axial slice derivative at differentiable points.
`axial_second_derivative_eq_slice` repeats this identification, requiring
slice-wide differentiability and differentiability of partialZ at the
point. `stream_axial_second_derivative_on_axis` then proves U_zz=H_zz
for U=H+s H_s at s=0, since the two axial slices agree identically.
The pinned Lean check passes without sorryAx. These explicit smoothness
hypotheses still need to be supplied for the actual physical profiles;
the statements do not yet establish the final assembled-field limit.


## Combined physical stream Laplacian identity

`physical_stream_laplacian_on_axis` now combines the Cartesian Laplacian
and both stream-to-velocity derivative identities into
(Delta u)_z = 4 H_s + H_zz on the axis for the regular axisymmetric
velocity with axial component H+s H_s. Axial slice differentiability of
that component is derived from SliceC2, not separately assumed.
The remaining smoothness assumptions on H and its derivatives are explicit.
The pinned Lean check passes without sorryAx. Instantiating those
hypotheses with the constructed stream and identifying the resulting
physical derivative with the selected slow-sum limit are still required.


## Laplacian bridge with source SliceC2 assumptions

`physical_stream_laplacian_of_sliceC2` derives all derivative-existence
conditions in the combined identity from SliceC2 of B, F, H and
U=H+s H_s at the fixed time. It uses the source's pointwise Frechet
second-derivative regularity, not an assumed smooth extension across
the singular time. The pinned Lean check passes without sorryAx.
The actual constructed profiles still need to be shown to satisfy
these SliceC2 hypotheses; the force-ratio limit remains unformalized.


## Actual selected stream regularity

`selected_stream_sliceC2` supplies SliceC2 for the actual
`streamFactor (FinalSlowBase.scales ...) ... (FinalSlowBase.coefficients ...)`
at every physical time t < 1. It derives h < 1/2 from the stored small
parameter bound, strict monotonicity from scale admissibility, and
coefficient smoothness from the FinalSlowBase theorem. No added
regularity assumption is used. The pinned Lean check passes without
sorryAx. The swirl-derived transverse profiles and axial velocity
H+s H_s still require their corresponding regularity and velocity
identification before the physical Laplacian theorem can be applied
to the actual base velocity.


## Actual stream-derived axial velocity regularity

`selected_stream_axial_velocity_sliceC2` proves SliceC2 of
H+s partialS H for the actual selected stream at every t<1.
The source's infinite-order pointwise smoothness supplies the derivative
regularity needed for partialS H to be C2; the multiplication and addition
then give C2 of the axial profile. No extra axial-velocity regularity
hypothesis is assumed. The pinned Lean check passes without sorryAx.
The transverse-profile regularity, identification with baseVelocity,
and final physical force-ratio transfer remain to be formalized.


## Selected transverse profiles and Laplacian instance

`selected_transverse_profiles_sliceC2` derives SliceC2 of H_z/2 and
-K_s from the actual selected stream H and swirl potential K.
`selected_profile_velocity_laplacian_on_axis` combines all selected
regularity results and proves the axial Laplacian formula for the
component-built velocity at every t<1. No additional regularity
hypotheses remain. Both pass the pinned Lean check without sorryAx.
The component-built velocity must still be identified with the curl-defined
`SlowBorelBase.baseVelocity`, then transferred through the final assembly
and related to the material acceleration and derivative limit.


## Curl and component velocity agreement

`curl_velocity_eq_profile_velocity` proves equality of the source
curl-defined velocity H,K and the component velocity with profiles
B=H_z/2, F=-K_s, U=H+s H_s at differentiable points. All three
Cartesian components, including transverse signs, are checked by the
pinned Lean run without sorryAx. This pointwise lemma still needs to
be instantiated across a fixed-time spatial slice for the selected
baseVelocity before transferring its spatial Laplacian.


## Actual baseVelocity Laplacian

`selected_base_velocity_slice_eq` proves equality of the entire spatial
velocity slice for t<1, using the selected stream and swirl regularity.
`selected_base_velocity_laplacian_on_axis` rewrites the spatial derivative
and Laplacian through that function equality and obtains
(Delta baseVelocity)_z = 4 H_s + H_zz at (0,0,z).
No added smoothness hypotheses are present. Both pass the pinned Lean
check without sorryAx. This establishes the formula for the actual
base velocity, not yet for the final periodic assembled candidate.
The physical H_s/slow-sum relation, H_zz asymptotics and material
acceleration comparison remain formalization work.


## Selected physical radial derivative formula

`selected_stream_radial_derivative_physical` instantiates the source
`partialS_physicalProfile` theorem for the actual selected stream.
It identifies H_s with the physical profile of exponent -A-1 built
from partialX of bundle component 0. The pinned Lean check passes
without sorryAx. Component 0 is the radial average, whereas the
existing negative derivative limit concerns raw axial component 5.
The averaging derivative identity linking these components, including
its factor 1/2 on the axis, remains a necessary formal bridge.


## Radial differentiation under the averaging integral

`radial_derivative_compact_integral` proves interchange of radialPartial
and integration over [0,1] under the source compact-parameter smoothness
hypotheses. It evaluates the integrated Frechet derivative in direction
(1,0), complementing the source's parameterPartial theorem in direction
(0,1). The pinned Lean check passes without sorryAx. Applying this to
F(tX,eta) and evaluating the integral of t at X=0 remains the next step;
the averaging factor 1/2 is not yet formally established here.


## Averaging factor at the axis proved

`average_radial_derivative_at_axis` proves radialPartial (average F)
(0,eta) = (1/2) radialPartial F (0,eta) for a smooth field on the
source radial domain containing the axis point. It combines the compact
integral derivative theorem, the Frechet chain rule for (rX,eta), and
the integral of r over [0,1]. The pinned Lean check passes without
sorryAx. Applying this identity to the selected coefficient bundle and
its slow sum remains the next connection to the physical H_s limit.


## Selected coefficient bundle averaging identity

`bundle_average_derivative_at_axis` identifies bundle components 0 and 5
as functions before differentiating, and applies the average theorem on
the global radial domain. `selected_bundle_average_derivative_at_axis`
instantiates it with FinalSlowBase coefficients for every order j and eta.
It proves partialX(component 0 j)(0,eta) = (1/2) partialX(component 5 j)(0,eta).
Both pass the pinned Lean check without sorryAx. Transferring this
coefficient identity through the locally finite slow sum, and connecting
the resulting physical derivative to its asymptotic limit, remain pending.


## Averaging identity through the slow sum

`slowSum_axis_proportional` transfers a coefficient-wise proportionality
at the axis through the actual slow sum for q>0 and strictly monotone
scales. It uses the source's common finite-at-scale representation.
`averaged_derivative_slowSum_at_axis` applies it to the radial derivatives
of bundle components 0 and 5, retaining the exact factor 1/2.
Both pass the pinned Lean check without sorryAx. The next bridge is to
identify the sum of component-5 derivatives with the ordinary derivative
whose asymptotic limit has already been proved, then include the physical
q^(-A-1) factor in H_s.


## Averaged derivative sum limit

`selected_averaged_derivative_sum_tends_natural` identifies the sum of
component-5 derivatives with the ordinary X derivative of its slow sum
using `hasDerivAt_slowSum_X`. It combines the selected derivative limit
and the averaging identity to prove that the component-0 derivative
sum tends to one half of the natural-profile radial derivative as q
approaches zero from above. The pinned Lean check passes without sorryAx.
The physical multiplier q^(-A-1) and evaluation along the material
trajectory remain to be connected before this gives an H_s asymptotic.


## Normalized physical radial derivative

`selected_stream_normalized_radial_derivative` proves the exact identity
q^(A+1) H_s(p) = slowSum of component-0 radial derivatives at the
physicalChart of p, for p.time<1. Positivity of q comes from the source
coordinate theorem and justifies cancellation of the real powers.
The pinned Lean check passes without sorryAx. To apply the previously
proved limit, the physicalChart of the proposed material trajectory
still needs to be identified as (q,(0,eta_star)) with q approaching zero
from above. This identity alone does not prove that trajectory property.


## Candidate trajectory scale limit

`trajectory_scale_tends_zero_right` proves that tau/(1-eta²) tends to
zero from above as tau tends to zero from above for -1<eta<1.
The denominator's positivity and the one-sided target filter are
proved explicitly. The pinned Lean check passes without sorryAx.
This does not identify that expression with the source coordinateQ
or prove the candidate curve is a material trajectory. Those coordinate
and differential-equation identities remain necessary before applying
this limit to the physical stream derivative.


## Candidate inverse coordinate identification

`candidate_axis_forward_coordinate` proves the forward scalar equation
for tau=q(1-eta²), z=eta q^D. `candidate_axis_inverse_coordinate` uses
the source positive-solution uniqueness theorem to show coordinateQ
returns exactly q for h in (0,1/2), q>0 and eta in (-1,1).
Both pass the pinned Lean check without sorryAx. Identification of the
remaining physicalChart coordinates and proof of the material-trajectory
ODE are still required; coordinate equality alone is not that ODE.


## Physical chart and normalized derivative limit on the candidate curve

`candidate_axis_physicalChart` proves that the full physical chart maps
(1-q(1-eta²),0,eta q^D) to (q,0,eta), including the time shift and
matching the two source conventions for D.
`candidate_normalized_stream_derivative_limit` then proves that
q^(A+1) H_s along this curve tends to half the natural-profile radial
derivative as q approaches zero from above. Both pass the pinned Lean
check without sorryAx. The curve has not yet been formally shown to
solve the material-trajectory ODE; the H_zz and acceleration comparison
and final assembled-field transfer also remain.


## Candidate curve physical-time derivative

`candidate_axis_curve_hasDerivAt` differentiates
z(t)=eta ((1-t)/(1-eta²))^D for t<1 and -1<eta<1.
It proves z'(t)=(-eta D/(1-eta²)) q^(-A), including the real-power
chain rule and D-1=-A. The pinned Lean check passes without sorryAx.
The root equation must still identify the prefactor with U(eta),
and the actual base-velocity value on the curve must be verified
before claiming the material-trajectory ODE formally.
