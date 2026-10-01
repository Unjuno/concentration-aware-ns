import hashlib
import json
import unittest
from pathlib import Path

from tools.analyze_amr_same_run_map import ARCHIVE, EVIDENCE, analyze


class SameRunMappingTests(unittest.TestCase):
    def test_archived_same_run_parent_injection_result(self):
        manifest = json.loads((EVIDENCE / "manifest.json").read_text())
        self.assertEqual(manifest["status"], "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED")
        self.assertEqual(
            hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
            manifest["archive_sha256"],
        )
        analyze()
        result = json.loads((EVIDENCE / "analysis.json").read_text())
        self.assertEqual(result["preMap_cells"], 4096)
        self.assertEqual(result["mapped_cells"], 16640)
        audit = result["parent_value_injection"]
        self.assertEqual(audit["mapped_vs_parent_injection_relative_l2"], 0.0)
        self.assertLess(audit["parent_volume_closure_relative_max"], 1e-12)
        self.assertAlmostEqual(
            result["mapped_velocity_point_sample_error_vs_exact_mms"],
            0.41795531114604173,
            places=12,
        )


if __name__ == "__main__":
    unittest.main()
