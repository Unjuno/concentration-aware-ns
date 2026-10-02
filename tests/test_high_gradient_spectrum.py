import contextlib
import io
import unittest

from tools.check_high_gradient_spectrum import check
from tools.high_gradient_spectrum import shell_spectrum


class HighGradientSpectrumTests(unittest.TestCase):
    def test_analytic_shell_sum_matches_resolved_fft(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = check()
        self.assertTrue(result["passed"])
        self.assertEqual([row["N"] for row in result["cases"]], [4, 8, 16])

    def test_reject_invalid_parameters(self):
        for n in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                shell_spectrum(n)
        with self.assertRaises(ValueError):
            shell_spectrum(4, float("nan"))


if __name__ == "__main__":
    unittest.main()
