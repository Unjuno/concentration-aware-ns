import json
import subprocess
import sys
import tempfile
from pathlib import Path

import sympy as sp


def test_uniform_extension_drives_strain_axes_but_keeps_viscous_coefficient_fixed():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "internal-state.json"
        run = subprocess.run(
            [
                sys.executable,
                "-m",
                "tools.check_visco_morphoelastic_internal_state",
                "--output",
                str(output),
            ],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        assert run.returncode == 0, run.stdout + run.stderr
        result = json.loads(output.read_text(encoding="utf-8"))

    t, alpha, beta, shear_rate, mu1, lam = sp.symbols(
        "t alpha beta shear_rate mu1 lambda", positive=True
    )
    qstar = 3 * beta / alpha
    decay = 1 - sp.exp(-alpha * t)
    expected_f_xx = -(qstar - 1) * shear_rate * decay / alpha
    expected_f_yy = +(qstar - 1) * shear_rate * decay / alpha
    expected_stress_ratio = mu1 - lam * (qstar - 1) * decay / alpha
    symbols = {
        "t": t,
        "alpha": alpha,
        "beta": beta,
        "shear_rate": shear_rate,
        "mu1": mu1,
        "lam": lam,
        "exp": sp.exp,
    }
    assert sp.simplify(sp.sympify(result["F_xx"], locals=symbols) - expected_f_xx) == 0
    assert sp.simplify(sp.sympify(result["F_yy"], locals=symbols) - expected_f_yy) == 0
    assert sp.simplify(
        sp.sympify(result["projected_total_stress_coefficient"], locals=symbols)
        - expected_stress_ratio
    ) == 0
    assert result["constitutive_viscous_coefficient"] == "mu1"


if __name__ == "__main__":
    test_uniform_extension_drives_strain_axes_but_keeps_viscous_coefficient_fixed()
