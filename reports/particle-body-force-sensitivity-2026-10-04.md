# Body-force limitation of particle sensitivity

The pinned Foundation 13 solidParticle update includes a body-force term:
Up_new=(Up+dt*(Dc*Uc+(1-rhoc/rhop)*g))/(1+dt*Dc). Tracking precedes
this update, so the following holds at fixed dt, old velocity, properties and
geometry; it is not a bound for the tracked trajectory.

On one positive scalar high-Re branch, with Up=0, set r=Uc, x=dt*Dc,
b=dt*(1-rhoc/rhop)*g. Then F=(x*r+b)/(1+x), and

    dF/dr = x/(1+x)+(r-b)*x'(r)/(1+x)^2.

Independent SymPy differentiation has zero residual. At nu=d=dt=r=1,
rhoc/rhop=1/2 and decoded binary64 p=.687, k=.15, x=9*(1+k), x'=9*k*p.
Arb128 encloses the zero-force derivative near **0.9190937142191775**,
below one. For opposing g=-40, b=-20, it encloses the derivative near
**1.0630825360476626**, strictly above one. Both are inside the smooth Re=1
branch, far from the Re=.01 threshold. This supplies a local mathematical
counterexample to extending the body-force-free contraction to arbitrary
constant body force. It does not contradict the earlier stated conditions.
For this r=1 family the exact amplification condition is b<1-(1+x)/x'.

The interval auditor, source/consumer hashes and symbolic receipt are in
`evidence/particle-body-force-sensitivity-v1`. Numerical source is 902b47e;
`python -m tools.audit_particle_body_force_sensitivity --output NEW_DIRECTORY
--source-commit 902b47e058bb824a382523d05c5796f0a9b76769` recomputes it.
A second same-host run reproduces the JSON exactly; this is neither a guarded
source export nor cross-host reproduction. No native cloud execution or
observed instability is claimed. The parameter example is synthetic; no
benchmark particle-state relevance, timestep suitability or actual encounter
has been established. No physical transition, viscosity law or global error
bound follows. No upstream issue is justified by this conditional algebra.

The pending a611973 Python run 37157306920 remains queued on fresh inspection.
The new audit and CI integration are local commits held until that exact-head
job terminates, avoiding cancellation. Full goal remains active.
