# Exact finite-grid observation limit

The conservative peak gates require more than finite samples. A simple exact
control explains why, without relying on singularities or simulation.
On the periodic cube take m=128, p=0 and

    u = (0, sin(m*x)/m, 0),
    f = (0, nu*m*sin(m*x), 0).

This stationary velocity is smooth, divergence free and has zero advective
term. Since Delta u=-m²u, it solves the forced Navier–Stokes equation exactly.
For every uniform grid with n=16,32,64, its nodal velocity values, cell-center
velocity values and cell averages vanish. Nevertheless, its continuous maximum
velocity-gradient Frobenius norm and vorticity magnitude are both 1. Its mean
kinetic energy is 1/65536. Differencing or Fourier-differentiating only those
zero velocity observations cannot recover that derivative maximum.

The general family m=2*lcm(n1,...,nk) works for any specified finite set of
uniform grid sizes. An arbitrary amplitude factor scales the derivative while
keeping all those velocity observations zero. Therefore these observations
alone provide no universal upper bound on continuous derivative maxima.
This is the familiar sampling ambiguity, not a new blow-up result.

`python -m tools.check_sampling_nullspace` verifies the divergence, advection,
steady PDE balance, every sample and cell integral, and energy by exact SymPy
arithmetic. Evidence: `evidence/tests/sampling-nullspace.json`.

This auxiliary solution uses different forcing and initial data from the main
manufactured benchmark. It does not show failure of OpenFOAM, SU2 or PhysicsNeMo,
does not show that a configured solver would return zero, and does not establish
a standard-PASS/local-FAIL case under the benchmark protocol. In particular,
analytic derivative observations would distinguish this field from zero.

A useful certification must therefore add assumptions or evidence such as a
bounded unresolved spectral tail, derivative bounds, or a specified numerical
reconstruction with an error estimate. An analytic reference field alone does
not provide those bounds for the computed field. The existing UNCERTAIN peak
verdicts are retained; this control explains their missing-information boundary.
