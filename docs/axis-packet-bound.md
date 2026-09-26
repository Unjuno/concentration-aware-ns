# Finite-packet bound using the exact axis propagator

This classical estimate refines the generic exp(L*Delta) estimate in
[the flow-derivative proof](axis-flow-derivative.md). It uses the exact linear
stretching rate instead of the full velocity-gradient norm, which also counts
rotation. It is conditional on a smooth tube and a certified Hessian bound;
neither numerical value has yet been extracted for the actual construction.

## Propagator and cancellation

Assume C>0 and t0<=s<=t<=T<1. Let F be the checked variational solution.
Its propagator P(t,s)=F(t)*F(s)^(-1) has singular values

    ((1-t)/(1-s))^(C/2), twice, and ((1-s)/(1-t))^C.

Thus its Euclidean operator norm is exactly

    ||P(t,s)|| = a(t)/a(s),     a(t)=((1-t0)/(1-t))^C.

The arbitrary transverse rotation cancels from this norm. Equivalently,
v dot Gv = g*(v3^2-(v1^2+v2^2)/2) <= g*|v|^2, with g=C/(1-t).
No bound on omega enters these linear estimates. The nonlinear Hessian bound
below can still depend on the swirl profile; this is not complete independence
from rotation in the actual fluid.

## Nonlinear comparison

On the closed tube of radius rho around X over [t0,T], let M>=0 bound
the second spatial derivative operator norm and put k=M/2. Let Y start
at X(t0)+h, delta=|h|, and e=Y-X. Until the first exit from this tube,
Taylor's formula gives e'=Ge+R with |R|<=k*|e|^2. Variation of constants
and the propagator norm yield, for w(t)=|e(t)|/a(t),

    w(t) <= delta + k*integral[t0,t] a(s)*w(s)^2 ds.

Define I(t)=integral[t0,t] a(s) ds. Scalar comparison gives

    w(t) <= b(t)=delta/(1-k*delta*I(t))

while the denominator is positive. For completeness, if delta>0 set
v(t)=delta+k*integral a*w^2. Then w<=v and v'<=k*a*v^2;
integrating (1/v)'>=-k*a proves the bound. For delta=0, local ODE
uniqueness gives e=0. The case k=0 is also included.

Since a and I are nondecreasing, the sufficient condition

    delta < rho / (a(T)+k*rho*I(T))

ensures both denominator positivity and |e(t)|<rho on the entire interval.
A first exit is impossible, and compact-tube continuation supplies Y through
T. Failure of this sufficient inequality does not prove exit or instability.

For the linearization error z=e-F(t)h, variation of constants gives

    |z(t)| <= a(t)*k*integral[t0,t] a(s)*b(s)^2 ds
            = a(t)*(b(t)-delta)
            = a(t)*k*delta^2*I(t)/(1-k*delta*I(t)).

Here b'=k*a*b^2 and b(t0)=delta. This replaces an exponential bound involving
the full off-axis gradient norm by a power-law propagator and a nonlinear
denominator. It is a quadratic remainder for fixed T and sufficiently small
delta. It requires no bound on the first derivative throughout the tube for
the error estimate, although smoothness is still used for local existence.

## Explicit time integral and relative-error meaning

With Q=(1-t)/(1-t0) and tau0=1-t0,

    I(t)=tau0*(1-Q^(1-C))/(1-C),   C != 1;
    I(t)=-tau0*log(Q),             C = 1.

Both are nonnegative for 0<Q<=1 and have derivative a(t). The normalized
error bound |z|/(a*delta) is k*delta*I/(1-k*delta*I). This is relative to
the **largest possible linear amplification**, not to |Fh| for every h.

In particular a transverse displacement has |Fh|=r*delta, r=Q^(C/2).
To guarantee |z|<=epsilon*|Fh| for all such h using this norm bound, it
suffices (when k*I>0) to require additionally

    delta <= epsilon*r / (k*I*(a+epsilon*r)).

Ignoring this distinction can make a good absolute error bound appear to
certify a contracting direction that it does not resolve. This is directly
relevant to the proposed alignment inference.

## Verification and remaining inputs

`python -m tools.check_axis_packet_bound` in the pinned verification environment
checks nine exact identities, including both integral branches, rotation
cancellation and the nonlinear denominator. Exact rational controls show one
radius satisfying the tube criterion and another that cannot be certified by
it; they are illustrative constants, not parameters of the OpenAI field.

The scalar comparison and continuation proofs above are classical, not
Lean-formalized. The actual tube radius rho and Hessian bound M remain
non-effective. No fixed-size packet is certified through t=1, and no molecular
or constitutive-viscosity law is inferred. The source pressure-witness gap
remains separate from this deformation estimate.

[The constant-dependency audit](packet-constant-dependencies.md) now identifies
the compact derivative bound and finite-stage cutoff route in the source.
Uniform full-spacetime derivative bounds transfer through base-field germs,
and sufficiently high cutoff stages have zero jets above an explicit index
condition J*qmin>1. Neither result supplies numerical rho or M yet.

[The actual-root exponent enclosure](axis-stretch-range.md) now proves
7999999/2000000 <= C < 4 without a pressure premise. Its upper bound gives
explicit conservative replacements a<=Q^(-4) and
I<=(1-t0)*(Q^(-3)-1)/3 in the packet-radius and remainder formulas. This
removes the need to evaluate C; numerical rho and M are still missing.
