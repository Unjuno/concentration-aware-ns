"""Check that translational hydrodynamic moments do not identify rod order."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    theta, alpha = sp.symbols("theta alpha", real=True)
    p = (1 + alpha * sp.cos(2 * theta)) / sp.pi
    normalization = sp.integrate(p, (theta, 0, sp.pi))
    nematic_order = sp.integrate(sp.cos(2 * theta) * p, (theta, 0, sp.pi))
    transverse_order = sp.integrate(sp.sin(2 * theta) * p, (theta, 0, sp.pi))

    controls = {
        "orientation_density_normalizes": sp.simplify(normalization - 1) == 0,
        "nematic_order_is_alpha_over_two": sp.simplify(nematic_order - alpha / 2) == 0,
        "transverse_order_is_zero": sp.simplify(transverse_order) == 0,
        "isotropic_case_has_zero_order": sp.simplify(nematic_order.subs(alpha, 0)) == 0,
    }
    out = {
        "scope": "Exact angular moments for a constructed orientation distribution; translational moments are invariant because the angular factor integrates to one. Not a kinetic solution or molecular dynamics result.",
        "sympy": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "conditions": ["theta in [0, pi)", "abs(alpha) < 1", "orientation-independent translational distribution f(x,v)"],
        "orientation_interval": "[0, pi)",
        "density": "(1 + alpha*cos(2*theta))/pi",
        "normalization": str(normalization),
        "nematic_order": str(sp.simplify(nematic_order)),
        "transverse_order": str(sp.simplify(transverse_order)),
        "positivity_condition": "abs(alpha) < 1",
        "same_translational_moments": ["mass density", "mean velocity", "translational temperature", "translational kinetic-stress tensor"],
        "controls": controls,
        "success": all(controls.values()),
    }
    Path("evidence/tests/molecular-state-nonidentifiability-2026-10-02.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )
    print(json.dumps(out, indent=2))
    return 0 if out["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
