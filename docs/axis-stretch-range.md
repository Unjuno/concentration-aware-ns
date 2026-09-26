# A numerical enclosure for the actual axis stretching exponent

The parameter choices need not be evaluated to bound the stretching exponent.
For the actual selected profile, the extension now establishes existence of
the distinguished root together with

    3.9999995 <= C < 4.

The lower endpoint is the exact rational 7999999/2000000, not a rounded
floating-point estimate. No simulation or PressureData hypothesis is used.
This does not determine the exact root, rotation rate, coefficient sequence,
or spatial Hessian bound.

Both source pins pass 134 extension axiom reports with only the permitted
standard axioms. Five verification-gate fault tests pass. These checks include
the exact enclosure and actual-root existence, not a numerical trajectory.

## Source conditions and algebra

`CorrectionInitialization.ActualPrimary.nominal.axis.small` supplies
0<h<=1/1000 and 0<j<=1/1000. These are the actual nominal witness's
`NaturalAxisData.SmallParameters`, not the broader range used by some newer
upstream results. `NaturalAxisData.exists_unique_root` places the root at
-j/4<eta<-j/5, hence -1/4000<eta<0.

Put e=eta^2, A=1/2+h, D=1/2-h, L=1-2*h*e. The previously identified
axial rate is C/(1-t), with

    C = [4*(1-e)^2 + 2*A*D*e] / L.

Here 0<e<=1/16000000, A*D>=0 and 0<L<=1. The numerator is at least
4-8*e, so C>=4-8/16000000=7999999/2000000. For the upper bound,

    4-C = e*(15/2-8*h+2*h^2-4*e)/L > 0.

All signs follow from the stated small-parameter box. The Lean declarations
are `materialStretchCoefficient_enclosure`, `natural_root_stretch_enclosure`
and `exists_actual_root_with_stretch_enclosure`. The last one connects the
bound to a root of the actual nominal witness, rather than leaving root
existence or a freely chosen parameter box as an extra premise.

## Consequences for the already derived deformation

For t0<t<1 write Q=(1-t)/(1-t0), so 0<Q<1, and C0=7999999/2000000.
The classical flow-derivative identification gives the following enclosures:

    Q^2 < transverse factor Q^(C/2) <= Q^(C0/2),
    Q^(-C0) <= axial factor Q^(-C) < Q^(-4),
    Q^6 < directional ratio factor Q^(3*C/2) <= Q^(3*C0/2).

The inequalities reverse in the exponent because Q<1. The directional ratio
only describes initial separations with a nonzero axial component. These
consequences use the classical connection to the flow and monotonicity of
real powers; they are not separate new Lean declarations in this change.

For the [packet comparison](axis-packet-bound.md), C>1 now follows without
extracting any chosen profile. Its linear amplification a and integral I obey

    a(t) <= A4(t) = Q^(-4),
    I(t) <= I4(t) = (1-t0)*(Q^(-3)-1)/3.

This supplies a conservative sufficient packet-radius condition with no
unknown C:

    delta < rho / (A4(T) + (M/2)*rho*I4(T)).

Both substitutions enlarge the denominator, so the condition implies the
previous sufficient condition. The same monotonic substitutions give

    nonlinear remainder <= A4*(M/2)*delta^2*I4 /
                           (1-(M/2)*delta*I4)

when that denominator is positive and the tube condition holds. The constants
rho and M are still needed on the whole tube; they have not been numerically
certified. In particular this is not a guarantee for a fixed finite packet
as t approaches 1.

## Interpretation

This is quantitative information about one continuum construction: strong
axial stretching coexists with transverse contraction and volume preservation.
It does not supply a molecular alignment model, phase transition, particle
shrinkage or a material viscosity law. The pressure-qualified force-ratio sign
claim remains a separate unresolved instantiation for `actualProfile`.
