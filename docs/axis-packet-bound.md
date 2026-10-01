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

## Power-law envelopes toward the endpoint

The sufficient initial radius can be generalized without pretending the
unknown tube and Hessian constants are uniform. Let `Q=(1-T)/(1-t0) -> 0`,
assume `C>1`, and suppose for each terminal interval `[t0,T]` an available tube
has radius `rho(Q)=rho0*Q^r`, while its half-Hessian bound satisfies
`k(Q)<=k0*Q^(-kappa)`, with fixed positive `rho0,k0` and exponents `r,kappa>=0`.
These are hypotheses about endpoint-dependent bounds, not established facts
for the selected profile.

The exact integral obeys

```
I(Q) = tau0*(Q^(1-C)-1)/(C-1)
     <= tau0/(C-1)*Q^(1-C).
```

Writing `d=kappa-r-1`, the tube denominator is bounded by

```
Q^(-C) + B*Q^(-C-d),      B=k0*rho0*tau0/(C-1).
```

If `d>=0`, the second power dominates and the tube condition is ensured by an
initial radius no larger than a constant times `Q^(C+kappa-1)`. If `d<=0`,
the first power dominates, giving a tube radius allowance of order `Q^(C+r)`.
The angle-error condition from the previous section requires order
`Q^(C+kappa-1)` for a fixed non-transverse initial direction and fixed positive
target angle: its linear margin tends to
`tan(theta_target)*cos(theta0)/(1+tan(theta_target)) > 0`. In the `d<=0` case,
`C+r >= C+kappa-1`, so the tube condition is at least as restrictive. Combined,
a sufficient power is therefore

```
delta(Q) = O(Q^(C + max(r,kappa-1))).
```

Here the angle condition means remaining inside a **fixed cone about the axis**;
it does not mean that the nonlinear error is small relative to the shrinking
transverse linear component. The distinction matters. Write
`m=tan(theta_target)`, `c=cos(theta0)>0`, and
`s=sin(theta0)`. For an initial displacement of length `delta`, the linear
image has axial magnitude `A=Q^(-C)*delta*c` and transverse magnitude
`B=Q^(C/2)*delta*s`. If the nonlinear remainder has norm at most `Z`, then
the perturbed direction is in the target cone whenever

```
(B+Z)/(A-Z) <= m,       with Z < A.
```

The classical remainder estimate gives
`Z <= Q^(-C)*k*delta^2*I/(1-k*delta*I)`. Thus

```
Z/A <= k*delta*I / (c*(1-k*delta*I)),
B/A = Q^(3C/2)*tan(theta0).
```

It suffices that the first ratio is at most
`eta(Q)=(m-Q^(3C/2)*tan(theta0))/(1+m)`, which is positive for sufficiently
small `Q`. Equivalently, with
`E(Q)=c*eta(Q)`, it suffices that
`delta <= E(Q)/((1+E(Q))*k*I)`. Since `E(Q)` tends to
`E0=m*c/(1+m)>0`, eventually `E(Q)>=E0/2`; using the stated upper bounds for
`k` and `I` yields the angle radius prefactor in the next paragraph. By
contrast, requiring `Z` to be at most a fixed fraction of the *transverse*
linear magnitude is a stronger, different criterion and has a different power
of `Q`. The checker records both quantities so they are not conflated.

For explicit constants, put
`B=k0*rho0*tau0/(C-1)` and
`p=C+max(r,kappa-1)`. Since each denominator term is at most its dominant
power for `0<Q<=1`, the tube allowance is at least
`rho0/(1+B)*Q^p`; choosing a smaller prefactor makes the strict tube
inequality hold. For the angle condition, put
`E0=tan(theta_target)*cos(theta0)/(1+tan(theta_target))>0`. Eventually
`E(Q)>=E0/2`, while `E(Q)<=E0`, so
`E(Q)/(1+E(Q)) >= E0/(2*(1+E0))`. Thus the angle-error condition is ensured by
`delta <= E0*(C-1)/(2*(1+E0)*k0*tau0) * Q^(C+kappa-1)`. As `p>=C+kappa-1`,
choosing a sufficiently small common constant in front of `Q^p` satisfies
both bounds. The case `k(Q)=0` has no nonlinear remainder and omits the angle
division by `k`.

For bounded Hessian (`kappa=0`) and a tube radius bounded below (`r=0`), this
reduces to `O(Q^C)`, agreeing with the fixed-constant special case. Since
`C>1`, the sufficient radius still tends to zero under all `r,kappa>=0`.
This proves only that this particular estimate certifies shrinking initial
packets under the stated envelopes. It does not show that an actual packet of
fixed size loses alignment, nor that the selected solution has any such
power-law tube/Hessian bounds. The piecewise exponent and integral are checked
symbolically by `python -m tools.check_packet_radius_scaling`; evidence is in
`evidence/tests/packet-radius-scaling.json`.

The source-rate audit in [packet-constant-dependencies.md](packet-constant-dependencies.md)
now Lean-checks a shrinking equality ball with radius proportional to
`sqrt(1-t)` and transfers the base's full-spacetime Hessian rate `kappa=40`
onto that ball. The new composition in
`verification/SpatialHessianTransfer.lean` transfers the same bound to the
fixed-time spatial Hessian. Combining that result with the classical nonlinear
comparison gives candidate exponents `r=1/2` and
`Cstretch+39`, enclosed in `[42.9999995,43)`. A simpler conservative power
follows by using the source enclosure `Cstretch<4`: for
`rho(Q)=rho0*Q^(1/2)` and `k(Q)<=k0*Q^(-40)`, we have
`a(T)<=Q^(-4)` and `I(T)<=(tau0/3)*Q^(-3)`. The tube criterion then allows
`delta < rho0/(1+B)*Q^43`, where `B=k0*rho0*tau0/3`. For any fixed initial
angle below pi/2 and positive target angle, the angle-error criterion also
allows a constant times `Q^43` once its linear margin is positive. With
`E0=tan(theta_target)*cos(theta0)/(1+tan(theta_target))`, choose

```
K < min(rho0/(1+B), 3*E0/(2*(1+E0)*k0*tau0)).
```

Then the combined sufficient law is `delta<=K*Q^43` for sufficiently small
Q. The exact exponent specialization is checked in
`evidence/tests/packet-radius-scaling.json`.

This remains a conditional shrinking-packet allowance: the Lean spatial
Hessian transfer is recorded in
`evidence/lean-verification/spatial-hessian-transfer-2026-10-01.json`, while
the nonlinear comparison is classical and K is non-effective. It is neither a
numeric packet certificate nor evidence that fixed-size packets lose
alignment.

## Verification and remaining inputs

`python -m tools.check_axis_packet_bound` in the pinned verification environment
checks nine exact identities, including both integral branches, rotation
cancellation and the nonlinear denominator. Exact rational controls show one
radius satisfying the tube criterion and another that cannot be certified by
it; they are illustrative constants, not parameters of the OpenAI field.

The rational controls include an explicit logical-boundary audit: one example
is certified inside its tube (`4/99 < 1/10`), while another comparison upper
exceeds the tube (`4/19 > 1/10`). The second case means only that this
sufficient estimate cannot certify containment. It is deliberately not
classified as an actual exit, finite-packet misalignment, molecular change,
or constitutive-viscosity change; those claims require separate evidence.

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
