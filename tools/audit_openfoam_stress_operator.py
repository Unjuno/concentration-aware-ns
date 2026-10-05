"""Check source-linked stress-flux models and conservative assembly controls.

The source manifest records a separate pinned-source byte comparison. The
default replay recomputes exact algebra; it does not execute OpenFOAM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = Path("evidence/upstream-refresh/openfoam-stress-operator-source-2026-10-03.json")
PIN = "18870c24d21c6b982e2cdec27b2f59738cca5f90"


def interpolation_defect(ap, an, gp, gn, wp, wa, wg, cp=0, ca=0, cg=0):
    """Product interpolation minus separately interpolated factors."""
    product = wp * ap * gp + (1 - wp) * an * gn + cp
    coefficient = wa * ap + (1 - wa) * an + ca
    gradient = wg * gp + (1 - wg) * gn + cg
    return sp.expand(product - coefficient * gradient)


def internal_face_balance(fluxes, owners, neighbours, volumes):
    """Fixed-mesh source convention: add to owner, subtract from neighbour."""
    if not (len(fluxes) == len(owners) == len(neighbours)):
        raise ValueError("face addressing and flux counts differ")
    sums = [sp.Integer(0) for _ in volumes]
    for flux, owner, neighbour in zip(fluxes, owners, neighbours):
        if not (0 <= owner < len(volumes) and 0 <= neighbour < len(volumes)) or owner == neighbour:
            raise ValueError("invalid internal-face addressing")
        sums[owner] += flux
        sums[neighbour] -= flux
    return [sp.simplify(total / volume) for total, volume in zip(sums, volumes)]


def verify_source_tree(manifest, source_root, role="current"):
    rows = [row for row in manifest["files"] if row["role"] == role]
    if not rows:
        raise ValueError("source manifest has no files for requested role")
    for row in rows:
        path = Path(source_root) / row["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            raise ValueError(f"source hash mismatch: {row['path']}")
    return len(rows)


def derive():
    ap, an, gp, gn = sp.symbols("a_P a_N G_P G_N", real=True)
    wp, wa, wg, w = sp.symbols("w_product w_coefficient w_gradient w", real=True)
    cp, ca, cg = sp.symbols("C_product C_coefficient C_gradient", real=True)
    da, dg = ap - an, gp - gn
    defect = interpolation_defect(ap, an, gp, gn, wp, wa, wg, cp, ca, cg)
    expected = ((wp - wg) * an * dg + (wp - wa) * gn * da
                + (wp - wa * wg) * da * dg + cp
                - ca * (gn + wg * dg) - cg * (an + wa * da) - ca * cg)
    checks = {"mixed_weight_and_correction_identity": sp.simplify(defect - expected) == 0}
    common = defect.subs({wp: w, wa: w, wg: w, cp: 0, ca: 0, cg: 0})
    covariance = w * (1 - w) * da * dg
    checks["uncorrected_common_weight_covariance"] = sp.simplify(common - covariance) == 0
    checks["constant_coefficient_zero_with_common_weights"] = sp.simplify(common.subs(ap, an)) == 0

    # The OpenFOAM vector & tensor contraction is linear in the tensor.
    surface = sp.Matrix(1, 3, sp.symbols("S_x S_y S_z", real=True))
    tensor_p = sp.Matrix(3, 3, sp.symbols("P_0:9", real=True))
    tensor_n = sp.Matrix(3, 3, sp.symbols("N_0:9", real=True))
    old_positive = surface * (w * ap * tensor_p + (1 - w) * an * tensor_n)
    new_positive = (w * ap + (1 - w) * an) * surface * (w * tensor_p + (1 - w) * tensor_n)
    tensor_covariance = w * (1 - w) * da * (surface * (tensor_p - tensor_n))
    checks["three_component_face_contraction"] = all(
        sp.simplify(x) == 0 for x in old_positive - new_positive - tensor_covariance)

    flux0, flux1 = sp.symbols("delta_F_0 delta_F_1", real=True)
    volumes = sp.symbols("V_0 V_1 V_2", positive=True)
    balance = internal_face_balance([flux0, flux1], [0, 1], [1, 2], volumes)
    signed_integral = sp.simplify(sum(v * d for v, d in zip(volumes, balance)))
    checks["internal_face_conservative_cancellation"] = signed_integral == 0

    r, traction = sp.symbols("r t", positive=True)
    constant_product = sp.factor(common.subs({ap: 1, an: r, gp: traction, gn: traction / r}))
    overshoot = 1 + w * (1 - w) * (r + 1 / r - 2)
    checks["constant_product_control"] = sp.simplify(constant_product - traction * (1 - overshoot)) == 0
    contrast100 = sp.simplify(overshoot.subs({r: 100, w: sp.Rational(1, 2)}))
    checks["constant_product_contrast_100_exact"] = contrast100 == sp.Rational(10201, 400)

    mismatched_constant = interpolation_defect(2, 2, 0, 1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(3, 4))
    checks["constant_coefficient_mixed_weight_counterexample"] = mismatched_constant == sp.Rational(1, 2)
    # A synthetic multi-donor map need not preserve products before the face blend.
    donor_defect = interpolation_defect(1, 3, 3, 1, sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
    checks["multi_donor_product_noncommutation_control"] = donor_defect == -1

    h, area = sp.symbols("h area", positive=True)
    c = sp.symbols("c", real=True)
    face_count, cell_volume, residual = area / h**2, h**3, c / h
    l1 = sp.simplify(2 * face_count * cell_volume * sp.Abs(residual))
    l2_squared = sp.simplify(2 * face_count * cell_volume * residual**2)
    weak_linear = sp.simplify(area * c * (-h / 2 - h / 2))
    checks["planar_layer_norm_scalings"] = (
        sp.simplify(l1 - 2 * area * sp.Abs(c)) == 0
        and sp.simplify(l2_squared - 2 * area * c**2 / h) == 0
        and sp.simplify(weak_linear + area * c * h) == 0)
    assert all(checks.values()), checks

    source_bytes = (ROOT / SOURCE_MANIFEST).read_bytes()
    manifest = json.loads(source_bytes)
    assert manifest["pinned_current_source_commit"] == PIN
    assert manifest["current_source_files_all_match_local"]
    return {
        "status": "PASS_SOURCE_LINKED_OPERATOR_MODEL_CONTROLS",
        "checker": "tools/audit_openfoam_stress_operator.py",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "symbolic_backend": f"SymPy {sp.__version__}",
        "source_manifest": str(SOURCE_MANIFEST),
        "source_manifest_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_commit": PIN,
        "implementation_change_parent": manifest["implementation_change_parent"],
        "checks": checks,
        "models": {
            "mixed_weight_correction_defect": str(expected),
            "new_minus_old_negative_stress_flux": "Sf & [I_product(a*G)-I_coefficient(a)*I_gradient(G)]",
            "common_uncorrected_weights": "w*(1-w)*(a_P-a_N)*(Sf & (G_P-G_N))",
            "three_cell_divergence": [str(x) for x in balance],
            "volume_weighted_signed_integral": str(signed_integral),
            "constant_product_separated_ratio": str(overshoot),
            "constant_product_ratio_w_half_r_100_exact": str(contrast100),
            "constant_coefficient_mixed_weight_defect": str(mismatched_constant),
            "synthetic_multi_donor_defect": str(donor_defect),
            "fixed_area_two_layer_jump_control": {
                "face_count": str(face_count), "cell_volume": str(cell_volume),
                "owner_neighbour_residual_density": [str(residual), str(-residual)],
                "volume_L1": str(l1), "volume_L2_squared": str(l2_squared),
                "Linf": str(sp.Abs(c) / h), "action_on_phi_x": str(weak_linear)},
        },
        "scope_limits": [
            "Default replay recomputes exact algebra only. Pinned-source acquisition and local-tree byte matches are separately recorded in the source manifest; --source-root rechecks its current-role file hashes.",
            "Source linkage is to the explicit transpose-gradient correction and a fixed, stationary mesh. The implicit Laplacian, boundary conditions, pressure solve and full solution are not compared.",
            "The simple covariance requires common uncorrected linear weights and coherent product endpoint values. Corrected, field-specific and multi-donor schemes require extra terms.",
            "The constant-product control uses prescribed independent coefficient/tensor data; it is not a manufactured incompressible velocity or a physical interface traction result.",
            "The planar-layer norm scalings describe a synthetic discrete correction mismatch. They establish neither a continuum singularity nor a physical viscosity or particle transition.",
            "No packaged-source equivalence, upstream-case reproduction or new solver verdict is established.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidence/tests/openfoam-stress-operator-controls-2026-10-03.json"))
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    if args.source_root:
        count = verify_source_tree(json.loads((ROOT / SOURCE_MANIFEST).read_text()), args.source_root)
        print(f"Verified {count} current-source file hashes.")
    result = derive()
    encoded = json.dumps(result, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
