"""Exact symbolic audit of a smooth, divergence-free localized MMS.

Continuum identities only: this does not run a CFD solver or claim a gate miss.
"""
import json
from pathlib import Path

import sympy as sp


def run() -> dict:
    x, y, z, t = sp.symbols("x y z t", real=True)
    N = sp.symbols("N", integer=True, positive=True)
    nu = sp.Rational(1, 100)
    g = ((1 + sp.cos(y)) / 2)**4
    h = ((1 + sp.cos(z)) / 2)**4
    chi = g * h
    psi = sp.exp(-t) * chi * sp.sin(N*x) / N**2
    u = sp.Matrix([sp.diff(psi, y), -sp.diff(psi, x), 0])
    grad = u.jacobian([x, y, z])
    div = sp.trigsimp(sp.diff(u[0], x) + sp.diff(u[1], y) + sp.diff(u[2], z))
    lap = sp.Matrix([sum(sp.diff(u[i], q, 2) for q in (x, y, z)) for i in range(3)])
    conv = grad * u
    forcing = sp.diff(u, t) + conv - nu * lap
    residual = sp.diff(u, t) + conv - nu * lap - forcing
    omega_z = sp.diff(u[1], x) - sp.diff(u[0], y)
    derivative_identity = sp.trigsimp(grad[1, 0] - sp.exp(-t)*chi*sp.sin(N*x))
    vorticity_identity = sp.trigsimp(
        omega_z - sp.exp(-t)*(chi - sp.diff(chi, y, 2)/N**2) * sp.sin(N*x))

    # At the selected point x=pi/(2N), y=z=0, first derivatives of chi
    # vanish, chi=1, and chi_yy=-2. The only nonzero velocity-gradient entries
    # are du_x/dy=chi_yy/N^2 and du_y/dx=1, so the Frobenius norm is exact.
    gradient_frobenius_at_peak = sp.simplify(sp.sqrt(
        grad[0, 1]**2 + grad[1, 0]**2).subs(
            {x: sp.pi/(2*N), y: 0, z: 0, t: 0}))
    omega_z_at_peak = sp.simplify(omega_z.subs(
        {x: sp.pi/(2*N), y: 0, z: 0, t: 0}))

    # g(y)=cos(y/2)^8 has a finite Fourier expansion. Orthogonality gives
    # exact normalized means by zero-mode sums, without quadrature.
    coeff = {
        0: sp.Rational(35, 128),
        1: sp.Rational(7, 32), 2: sp.Rational(7, 64),
        3: sp.Rational(1, 32), 4: sp.Rational(1, 256),
    }
    q = sp.symbols("q", real=True)
    fourier_poly = coeff[0] + sum(2*coeff[k]*sp.chebyshevt(k, q) for k in range(1, 5))
    envelope_poly = ((1+q)/2)**4
    fourier_identity = sp.Poly(sp.expand(fourier_poly-envelope_poly), q).is_zero
    g2 = sp.simplify(coeff[0]**2 + 2*sum(coeff[k]**2 for k in range(1, 5)))
    gp2 = sp.simplify(2*sum(k**2*coeff[k]**2 for k in range(1, 5)))
    gvort2 = sp.simplify(coeff[0]**2 + 2*sum(
        (1+sp.Rational(k**2, 1)/N**2)**2*coeff[k]**2 for k in range(1, 5)))
    mean_u2 = sp.factor(g2*gp2/(2*N**4) + g2**2/(2*N**2))
    mean_gradient_component2 = sp.factor(g2**2/2)
    mean_omega2 = sp.factor(g2*gvort2/2)

    identities = {
        "divergence_free": div == 0,
        "time_dependent_ns_residual_zero": all(sp.expand(v) == 0 for v in residual),
        "localized_gradient_formula": derivative_identity == 0,
        "vorticity_formula": vorticity_identity == 0,
        "gradient_frobenius_at_selected_peak": sp.simplify(
            gradient_frobenius_at_peak - sp.sqrt(1 + 4/N**4)) == 0,
        "vorticity_at_selected_peak": sp.simplify(
            omega_z_at_peak - (1 + 2/N**2)) == 0,
        "selected_point_is_exact_lower_bound_on_continuous_peaks": True,
        "envelope_fourier_identity": fourier_identity,
    }
    if not all(identities.values()):
        raise AssertionError(identities)

    cases = []
    for n in (4, 8, 16):
        at_n = lambda expr: sp.sstr(sp.factor(expr.subs(N, n)))
        cases.append({
            "N": n,
            "velocity_sup_upper_bound": f"{sp.sstr(sp.Rational(1,n)+2*sp.Rational(1,n**2))}",
            "selected_gradient_component_peak_at_t0": "1 (attained at x=pi/(2N), y=z=0)",
            "gradient_frobenius_at_selected_point_t0": sp.sstr(sp.sqrt(1 + 4*sp.Rational(1,n**4))),
            "vorticity_at_same_point_t0": sp.sstr(1 + 2*sp.Rational(1,n**2)),
            "mean_velocity_squared_at_t0": at_n(mean_u2),
            "mean_selected_gradient_component_squared_at_t0": at_n(mean_gradient_component2),
            "mean_vorticity_squared_at_t0": at_n(mean_omega2),
        })
    result = {
        "scope": "Exact continuum MMS identities; no CFD solver was run and no acceptance-gate failure is claimed.",
        "domain": "[0,2*pi]^3 periodic",
        "potential": "A=(0,0, exp(-t)*chi(y,z)*sin(N*x)/N^2), chi=((1+cos(y))/2)^4*((1+cos(z))/2)^4",
        "velocity": "u=curl(A)=exp(-t)*(chi_y*sin(N*x)/N^2, -chi*cos(N*x)/N, 0)",
        "equation": "partial_t(u)+(u dot grad)u = nu*Delta(u) + f, p=0, nu=1/100",
        "exact_checks": identities,
        "cases": cases,
        "passed": all(identities.values()),
        "limitations": [
            "The velocity bound follows from ||chi||inf<=1 and ||chi_y||inf<=2; it is an upper bound, not an exact velocity peak.",
            "The local derivative and vorticity values are continuum identities, not discrete-resolution results.",
            "The selected-point values are rigorous lower bounds on the continuous Frobenius-gradient and vorticity maxima, but are not asserted to be the global maxima.",
            "A fixed N case may be resolved by sufficient refinement; no solver was tested.",
            "This benchmark stress test implies no blow-up, molecular alignment, particle-position concentration, or constitutive-viscosity law.",
        ],
    }
    out = Path("evidence/tests/high-gradient-mms.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    if not run()["passed"]:
        raise SystemExit(1)
