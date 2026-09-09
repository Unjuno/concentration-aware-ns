# Finite-horizon error from neglecting viscosity in the specified vortex

This elementary analytic comparison uses the same prescribed strain a(t) in
both models, initial squared width q0>0, nu>0, and t>=0. It does not compare
self-consistent feedback systems whose strain trajectories change with nu.
Let A(t)=integral_0^t a(s) ds. The exact width equation and inviscid approximation
are q'=4nu-aq and qi'=-a qi, respectively, with identical initial widths.
Integrating factors give

    qi = exp(-A) q0,
    q = exp(-A) [q0 + 4nu integral_0^t exp(A(s)) ds].

Define B=(4nu/q0) integral_0^t exp(A(s)) ds >= 0. Then q=qi(1+B).
Consequently the squared-width relative error, measured against the viscous
solution, and the center-vorticity relative error are exactly

    (q-qi)/q = B/(1+B),
    (Wi-W)/W = B,       W=Gamma/(pi q), Wi=Gamma/(pi qi).

For width ell=sqrt(q), the corresponding relative error is
1-1/sqrt(1+B). Thus different observables have different approximation errors.
For a chosen vorticity tolerance delta>=0, B<=delta is necessary and sufficient
in this specified ansatz. This includes accumulated history, unlike an
instantaneous strain-to-diffusion ratio.

For constant a>0, B=4nu(exp(at)-1)/(a q0). Vorticity error <=delta holds exactly
until t<=log(1+delta*a*q0/(4nu))/a. For a=0 the continuous limit is
B=4nu*t/q0. Even when the initial ratio a*q0/nu is large, neglecting viscosity
need not remain accurate over a long observation period.

This is a conditional continuum-model error identity, not an experimental
criterion, universal turbulence threshold, novel-theorem claim, or molecular
position reconstruction. For feedback a=kappa*W the two models generally have
different a(t); applying the same-strain formula to them would be invalid.
