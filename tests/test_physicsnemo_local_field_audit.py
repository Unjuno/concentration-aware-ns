import unittest

from tools.audit_physicsnemo_local_fields import audit


class PhysicsNeMoLocalFieldAuditTests(unittest.TestCase):
    def test_archived_metrics_are_linked_and_remain_sample_scoped(self):
        result = audit()
        self.assertEqual(len(result["cases"]), 5)
        for row in result["cases"]:
            self.assertTrue(row["checkpoint_matches"])
            self.assertTrue(row["evaluation_matches"])
            self.assertGreater(row["sample_count"], 0)
        self.assertIn("no continuous extrema", result["scope"])


if __name__ == "__main__":
    unittest.main()
