import unittest

from tools.check_singular_affine_alignment import verify


class SingularAffineAlignmentTests(unittest.TestCase):
    def test_exact_solution_separates_alignment_from_density_and_viscosity(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["facts"].values()))
        self.assertTrue(result["negative_control_nonzero_viscous_laplacian"])
        self.assertEqual(result["transverse_to_axial_material_line_ratio_factor"],
                         "((T-t)/(T-t0))^3")
        self.assertEqual(result["gaussian_peak_density_ratio"], "1")


if __name__ == "__main__":
    unittest.main()
