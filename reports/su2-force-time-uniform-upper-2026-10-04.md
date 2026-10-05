# Continuous-domain SU2 MMS force time-displacement upper bound

For the executed exponential-envelope reference, set beta=1/sigma^2,
a=(1,2,3), psi_0=exp(sum(cos(d_i)-1)*beta). Then |psi_0|<=1 and
|q_i|,|r_i|,|s_i|<=beta, where q,r,s are the first three log-envelope
coordinate derivatives. Write u(t)=exp(-t)*u0 and
f(t)=exp(-t)*L+exp(-2t)*Q, L=-u0-nu*lap(u0), Q=grad(u0)*u0.

The Euclidean/Frobenius triangle and cross-product inequalities give, for
all points on the periodic domain,

    |u0| <= sqrt(42)*beta
    ||grad(u0)||F <= sqrt(14)*(3*beta^2+sqrt(3)*beta)
    |lap(u0)| <= sqrt(42)*(3*beta^3+5*beta^2+beta)
    |L| <= B_L = sqrt(42)*(beta+nu*(3*beta^3+5*beta^2+beta))
    |Q| <= B_Q = 14*sqrt(3)*beta*(3*beta^2+sqrt(3)*beta).

Here the Hessian is psi_0*(q q^T+diag(r)), whose Frobenius norm is bounded
by |q|^2+|r|. The Laplacian gradient is
psi_0*(q*sum(q_i^2+r_i)+2*q*r+s); its three terms yield the stated bound.
Therefore, for 0<h<=t,

    sup_x |f(x,t-h)-f(x,t)| <= (exp(h)-1)*exp(-t)*B_L
                              +(exp(2*h)-1)*exp(-2*t)*B_Q
                           <= h*(exp(h-t)*B_L+2*exp(2*h-2*t)*B_Q).

The last step uses exp(v)-1=integral_0^v exp(s) ds <= v*exp(v).
This establishes an absolute O(h) continuous-domain bound for fixed t and a
bounded positive h range. It is not a relative error or solution-error bound.

The three archive digests and sigma/nu parameters are rechecked. Arb128
outward endpoints enclose each bound expression. Use the upper rational
endpoints for an upper-bound certificate; the lower endpoints are NOT lower
bounds on the actual supremum. For dt=.001,.0005,.00025 the upper endpoints
are approximately 9.69284,4.84400,2.42140. Corrected sampled maxima are only
.085052,.042505,.021247, respectively, and lie below these bounds. The
triangle estimate is consequently loose and cannot decide an acceptance gate.

Numerical source e9cdce37 and evidence are in
`evidence/su2-force-time-uniform-upper-v1`; run
`python -m tools.bound_su2_force_time_displacement --output NEW_DIRECTORY
--source-commit e9cdce37cc06cb62bc030ec692decaf0b71b10fe`.
The domain derivation is independent of mesh resolution and point sampling.
Intervals describe the real reference with decoded archived parameters;
floating evaluator rounding, source callback rounding, discrete solver
response and convergence failures are not covered. No native solver is run,
no original threshold changes and no new upstream issue is justified.
The full goal remains active; hosted correction CI is still queued.
