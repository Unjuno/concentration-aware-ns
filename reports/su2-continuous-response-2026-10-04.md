# Conditional continuous response to force time displacement

This is an analytic comparison of two continuous strong solutions, not a
SU2 endpoint-error estimate. Assume periodic incompressible smooth solutions
u,v on [0,T], identical viscosity and initial velocity, with u driven by the
executed MMS force f(t) and v by its analytic extension f(t-h). Extending f to
negative startup times is an explicit hypothetical choice, not the recorded
solver callback schedule.

For w=v-u the difference equation contains v dot grad(w) and w dot grad(u).
Incompressibility and periodicity cancel transport and pressure in the energy
identity. With volume-normalized L2 norm E and viscosity dissipation dropped,

    dE/dt <= ||grad(u)||_operator,infinity * E + ||delta f||_L2.

The reference Hessian satisfies operator norm <= exp(-S)*(2*beta*S+beta),
where S>=0. Cross multiplication by a=(1,2,3) has norm sqrt(14).
The maximum of exp(-S)*(2*S+1) is 2*exp(-1/2), at S=1/2. Thus on t>=0
K0=2*sqrt(14)*beta*exp(-1/2) bounds the velocity-gradient operator norm.
The envelope-aware constants give a time-uniform force bound
F0=(exp(h)-1)*B_L+(exp(2*h)-1)*B_Q. Gronwall with E(0)=0 yields

    E(T) <= F0*(exp(K0*T)-1)/K0.

The normalized norm avoids an extra domain-volume factor. The same inequality
can be justified at E=0 by regularizing the energy norm before taking its limit.
Arb128 upper endpoints at T=.05 for h=.001,.0005,.00025 are recorded under
`evidence/su2-continuous-response-v1`, numerical source dc34d0f. They are
absolute bounds for the hypothetical strong-solution comparison. They do not
prove that v exists on the interval, quantify discrete solver error or assign
its observed error to forcing lag. Unconverged inner solves, time-discrete
assembly, startup timing, spatial error and floating rounding remain absent.
No original acceptance verdict changes and no upstream issue follows.
The full goal remains active; hosted publication CI is still queued.

Additive v2 recomputes the two force constants from archived parameters before
using them. Exact rational comparisons reject a stored interval that fails to
enclose the fresh expression. The response uses freshly recomputed upper
endpoints instead of trusting stored ones. Three focused tests pass, including
zeroed linear/quadratic constant rejections. All three response records remain
identical to v1; evidence is `evidence/su2-continuous-response-v2`, source
0777d12. This does not establish the hypothetical strong solution or a discrete
solver-error connection. Hosted correction run remains queued.

Additive v3 removes fixed-lag restriction for the comparison model. Let
0<=tau(t)<=h be measurable and drive v with f(t-tau(t)). At each time,
exp(tau)-1<=exp(h)-1 and exp(2*tau)-1<=exp(2*h)-1, so the same F0 and
energy estimate hold. Ideal sample-and-hold uses tau(t)=t-floor(t/h)*h;
on the first interval its force is f(0), requiring no negative-time extension.
Assume spatial smoothness, absolutely continuous L2 energy and the energy
identity almost everywhere, which accommodates forcing jumps. Existence and
these regularity conditions are still assumptions, not proved conclusions.
All three interval response records are unchanged. Twenty-seven exact rational
schedule controls cover startup, interiors and boundaries for the three time
steps. These ideal controls do not verify SU2's floating clock or BDF assembly.
V3 binds the frozen study protocol hash; evidence is
`evidence/su2-continuous-response-v3`, numerical source 852d6ea. A prospective
matched discrete stability/residual study remains necessary before assigning
observed SU2 error to this continuous comparison.
