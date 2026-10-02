import unittest

from tools.verify_openfoam_amr_archives import verify


class OpenFoamAMRArchiveTests(unittest.TestCase):
    def test_all_published_amr_and_remap_archives_match_manifests(self):
        result = verify()
        self.assertEqual(len(result["cases"]), 5)
        self.assertTrue(all(row["verified"] for row in result["cases"]))
        self.assertIn("does not re-execute OpenFOAM", result["scope"])


if __name__ == "__main__":
    unittest.main()
