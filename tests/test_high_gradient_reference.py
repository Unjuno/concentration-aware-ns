import contextlib
import io
import unittest

from tools.check_high_gradient_reference import check


class HighGradientReferenceTests(unittest.TestCase):
    def test_numpy_reference_matches_symbolic_derivatives(self):
        with contextlib.redirect_stdout(io.StringIO()):
            check()


if __name__ == "__main__":
    unittest.main()
