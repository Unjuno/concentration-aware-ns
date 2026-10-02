import contextlib
import io
import unittest

import sympy as sp

from tools.check_high_gradient_mms import run


class HighGradientMmsTests(unittest.TestCase):
    def test_exact_continuum_identities(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = run()
        self.assertTrue(result["passed"])
        self.assertEqual([case["N"] for case in result["cases"]], [4, 8, 16])
        self.assertEqual(
            [case["selected_gradient_component_peak_at_t0"] for case in result["cases"]],
            ["1 (attained at x=pi/(2N), y=z=0)"] * 3,
        )
        for case in result["cases"]:
            n = case["N"]
            self.assertAlmostEqual(
                float(sp.sympify(case["gradient_frobenius_at_selected_point_t0"])),
                (1 + 4/n**4)**0.5,
            )
            self.assertAlmostEqual(
                float(sp.sympify(case["vorticity_at_same_point_t0"])), 1 + 2/n**2,
            )


if __name__ == "__main__":
    unittest.main()
