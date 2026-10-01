# Independent check of the finite-packet fixed-cone exponent (2026-10-01)

## Question

The packet note uses a conditional `Q^43` initial-radius law to keep a fixed
non-transverse infinitesimal direction inside a fixed cone around the axis.
This audit re-derives that angle condition from vector components and separates
it from a stronger relative-error condition against the contracting transverse
component.

## Derivation

Write `Q=(1-T)/(1-t0)`, `m=tan(theta*)`, and let an initial displacement have
length `delta` and angle `theta0<pi/2` to the unoriented axis. Choose its sign so
its initial axial component is positive. The linear image has axial and
transverse magnitudes

```
A = Q^(-C) delta cos(theta0),
B = Q^(C/2) delta sin(theta0),
B/A = Q^(3C/2) tan(theta0).
```

Let `Z` bound the nonlinear displacement from the linear image. If `Z<A`, the
actual axial component is at least `A-Z`, and its transverse component is at
most `B+Z`. Hence membership in the target cone follows from

```
(B+Z)/(A-Z) <= m.
```
This holds when `Z/A <= eta(Q)`, where

```
eta(Q) = (m - Q^(3C/2) tan(theta0))/(1+m).
```
For a fixed positive target angle, `eta(Q)` tends to `m/(1+m)>0`.

The classical comparison bound gives

```
Z <= Q^(-C) k delta^2 I / (1-k delta I),
Z/A <= k delta I / (cos(theta0)*(1-k delta I)).
```
Set `E(Q)=cos(theta0)*eta(Q)`. Then it suffices that

```
delta <= E(Q)/((1+E(Q))*k*I).
```
For sufficiently small `Q`, `E(Q)>=E0/2`, where
`E0=m*cos(theta0)/(1+m)`. Under `k<=k0*Q^(-kappa)` and
`I<=tau0/(C-1)*Q^(1-C)`, this gives a prefactor times
`Q^(C+kappa-1)`. The tube condition independently gives
`Q^(C+max(r,kappa-1))`; combining them leaves the same tube-dominated exponent.
For `r=1/2`, `kappa=40`, and the source bound `C<4`, `Q^43` remains a
conditional sufficient law.

This does not guarantee that the remainder is small relative to the shrinking
transverse linear component. Imposing that different criterion gives the
stronger power `Q^(kappa+5C/2-1)` because the amplified remainder must then be
compared to `Q^(C/2)*delta`. At the conservative `C=4`, `kappa=40` specialization
that power is `Q^49`. The distinction is now explicit in both symbolic records.

## Validation and scope

`tools/check_axis_packet_bound.py` checks the fixed-cone component inequality
and threshold identity symbolically. `tools/check_packet_radius_scaling.py`
records both asymptotic powers and the selected specialization.
`tests/test_packet_alignment_scaling.py` checks the identities and confirms
that `Q^43` and `Q^49` represent distinct requirements. The two tests pass;
both symbolic checkers pass. This audit verifies algebra only. It does not
verify the classical nonlinear comparison theorem, make the Lean-derived tube
or Hessian constants effective, certify any nonzero finite packet, or infer
molecular alignment, viscosity change, or a physical singularity.

The earlier `Q^43` fixed-cone conclusion is not withdrawn; this note fills in
its previously implicit geometric derivation and prevents it from being
misread as a transverse-relative-error bound.
