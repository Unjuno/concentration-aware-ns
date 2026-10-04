import unittest

from tools.check_fluid_of_light_bridge import verify


class FluidOfLightBridgeTests(unittest.TestCase):
    def test_nlse_madelung_identities_hold_and_are_not_viscous_ns(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["identities"].values()))
        self.assertFalse(result["viscous_laplacian_term_present"])
        self.assertIn("No photon molecular positions", result["scope"])


if __name__ == "__main__":
    unittest.main()
