import hashlib
import json
import os
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v5-n32"
PROTOCOL = ROOT / "protocols/high-gradient-of13-amr-same-run-map-v5-n32.json"
ARCHIVE = EVIDENCE / "amr-stage-snapshot-n32.tar.gz"


class SameRunMapV5N32Tests(unittest.TestCase):
    def test_frozen_n32_run_and_compact_archive_replay(self):
        manifest = json.loads((EVIDENCE / "manifest.json").read_text())
        protocol = json.loads(PROTOCOL.read_text())
        self.assertEqual(manifest["status"], "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED")
        self.assertEqual(manifest["exit_code"], 0)
        self.assertTrue(manifest["end_marker"])
        self.assertTrue(manifest["instrumented_library_load_confirmed"])
        self.assertEqual(manifest["protocol_sha256_at_execution"],
                         hashlib.sha256(PROTOCOL.read_bytes()).hexdigest())
        self.assertEqual(
            hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), manifest["archive_sha256"]
        )
        with tarfile.open(ARCHIVE, "r:gz") as archive:
            names = archive.getnames()
            log_member = archive.extractfile("amr-n32-cap120000/log.foamRun")
            self.assertIsNotNone(log_member)
            log = log_member.read().decode(errors="replace")
        self.assertIn("Selected 12288 cells for refinement out of 32768", log)
        self.assertIn("Refined from 32768 to 118784 cells", log)
        self.assertEqual(sum(name.endswith("_cells.csv") for name in names), 6)
        self.assertEqual(sum(name.endswith("_faces.csv") for name in names), 1)
        self.assertTrue(any(name.endswith("/mapped_faces.csv") for name in names))
        self.assertTrue(any(name.endswith("/log.foamRun") for name in names))

        env = os.environ.copy()
        env["CANS_AMR_STAGE_PROTOCOL"] = str(PROTOCOL.relative_to(ROOT))
        env["CANS_AMR_STAGE_EVIDENCE"] = str(EVIDENCE.relative_to(ROOT))
        subprocess.run(
            [sys.executable, "-m", "tools.analyze_amr_same_run_map"],
            cwd=ROOT, env=env, check=True, capture_output=True, text=True,
        )
        result = json.loads((EVIDENCE / "analysis.json").read_text())
        self.assertEqual(result["preMap_cells"], protocol["case"]["initial_cells"])
        self.assertEqual(result["mapped_cells"], protocol["case"]["expected_mapped_cells"])
        self.assertEqual(
            result["parent_value_injection"]["mapped_vs_parent_injection_relative_l2"],
            0.0,
        )
        self.assertLess(
            result["parent_value_injection"]["parent_volume_closure_relative_max"],
            2e-14,
        )
        subprocess.run(
            [sys.executable, "-m", "tools.analyze_amr_gauss_gradient"],
            cwd=ROOT, env=env, check=True, capture_output=True, text=True,
        )
        gradient = json.loads((EVIDENCE / "gauss-gradient-audit.json").read_text())
        self.assertAlmostEqual(
            gradient["stages"][0]["interior_volume_fraction"],
            gradient["stages"][1]["interior_volume_fraction"], places=14,
        )
        self.assertAlmostEqual(
            gradient["stages"][0]["interior_gauss_gradient_relative_l2_vs_exact_point_gradient"],
            0.0871878180342279, places=12,
        )
        self.assertAlmostEqual(
            gradient["stages"][1]["interior_gauss_gradient_relative_l2_vs_exact_point_gradient"],
            0.22084781212152987, places=12,
        )
        self.assertEqual(
            gradient["same_parent_face_audit"]["same_parent_internal_faces"], 147456
        )
        self.assertEqual(
            gradient["same_parent_face_audit"][
                "same_parent_Uf_max_abs_difference_from_injected_parent_value"
            ], 0.0,
        )


if __name__ == "__main__":
    unittest.main()
