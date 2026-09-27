import contextlib
import io
import unittest

from tools.check_high_gradient_mms import run


class HighGradientMmsTests(unittest.TestCase):
    def test_exact_continuum_identities(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = run()
        self.assertTrue(result["passed"])
        self.assertEqual([case["N"] for case in result["cases"]], [4, 8, 16])
        self.assertEqual(
            [case["selected_gradient_component_peak"] for case in result["cases"]],
            ["1 (attained at x=pi/(2N), y=z=0)"] * 3,
        )


if __name__ == "__main__":
    unittest.main()
