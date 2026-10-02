import unittest

from tools.check_optical_madelung import audit


class OpticalMadelungTests(unittest.TestCase):
    def test_paraxial_equation_maps_to_compressible_hydrodynamics(self):
        result = audit()
        self.assertTrue(result["success"])
        self.assertTrue(all(result["checks"].values()))
        self.assertIn("div_perp", result["identities"]["continuity"])
        self.assertIn("Delta_perp(sqrt(rho))", result["identities"]["momentum"])

    def test_scope_does_not_claim_viscous_navier_stokes(self):
        result = audit()
        self.assertIn("not Maxwell derivation or Navier-Stokes validation", result["scope"])
        self.assertTrue(result["checks"]["model_has_no_viscosity_parameter_or_laplacian_velocity_term"])


if __name__ == "__main__":
    unittest.main()
