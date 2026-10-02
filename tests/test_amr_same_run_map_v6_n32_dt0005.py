import hashlib
import json
import os
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v6-n32-dt0005"
PROTOCOL = ROOT / "protocols/high-gradient-of13-amr-same-run-map-v6-n32-dt0005.json"
ARCHIVE = EVIDENCE / "amr-stage-snapshot-n32-dt0005.tar.gz"


class SameRunMapV6N32Dt0005Tests(unittest.TestCase):
    def test_fixed_map_time_half_dt_capture_replays(self):
        manifest = json.loads((EVIDENCE / "manifest.json").read_text())
        protocol = json.loads(PROTOCOL.read_text())
        case = protocol["case"]
        self.assertEqual(manifest["status"], "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED")
        self.assertEqual(manifest["exit_code"], 0)
        self.assertTrue(manifest["end_marker"])
        self.assertEqual(
            manifest["protocol_sha256"], hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
        )
        self.assertEqual(manifest["stage_times"]["mapped"], "0.002")
        self.assertEqual(manifest["stage_times"]["postSolve"], "0.0025")
        self.assertEqual(
            hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), manifest["archive_sha256"]
        )
        with tarfile.open(ARCHIVE, "r:gz") as archive:
            names = archive.getnames()
            log = archive.extractfile(
                f"{case['case_directory']}/log.foamRun"
            ).read().decode(errors="replace")
        self.assertIn("Time = 0.0025s", log)
        self.assertIn("Selected 12288 cells for refinement out of 32768", log)
        self.assertIn("Refined from 32768 to 118784 cells", log)
        self.assertEqual(sum(name.endswith("_cells.csv") for name in names), 2)
        self.assertEqual(sum(name.endswith("_faces.csv") for name in names), 1)
        self.assertTrue(any(name.endswith("/mapped_faces.csv") for name in names))
        self.assertTrue(any(name.endswith("/preMap_cells.csv") for name in names))
        self.assertTrue(any(name.endswith("/mapped_cells.csv") for name in names))
        self.assertFalse(
            any("/postProcessing/amrStages/0.0025/" in name and name.endswith(".csv")
                for name in names)
        )

        env = os.environ.copy()
        env["CANS_AMR_STAGE_PROTOCOL"] = str(PROTOCOL.relative_to(ROOT))
        env["CANS_AMR_STAGE_EVIDENCE"] = str(EVIDENCE.relative_to(ROOT))
        subprocess.run(
            [sys.executable, "-m", "tools.analyze_amr_same_run_map"],
            cwd=ROOT, env=env, check=True, capture_output=True, text=True,
        )
        result = json.loads((EVIDENCE / "analysis.json").read_text())
        self.assertEqual(result["preMap_cells"], case["initial_cells"])
        self.assertEqual(result["mapped_cells"], case["expected_mapped_cells"])
        self.assertEqual(
            result["parent_value_injection"]["mapped_vs_parent_injection_relative_l2"],
            0.0,
        )
        subprocess.run(
            [sys.executable, "-m", "tools.analyze_amr_gauss_gradient"],
            cwd=ROOT, env=env, check=True, capture_output=True, text=True,
        )
        gradient = json.loads((EVIDENCE / "gauss-gradient-audit.json").read_text())
        self.assertAlmostEqual(
            gradient["stages"][0]["interior_gauss_gradient_relative_l2_vs_exact_point_gradient"],
            0.08719723446052442, places=12,
        )
        self.assertAlmostEqual(
            gradient["stages"][1]["interior_gauss_gradient_relative_l2_vs_exact_point_gradient"],
            0.2208557558808142, places=12,
        )
        self.assertAlmostEqual(
            gradient["stages"][0]["interior_gauss_vorticity_relative_l2_vs_exact_point_vorticity"],
            0.09055738308351031, places=12,
        )
        self.assertAlmostEqual(
            gradient["stages"][1]["interior_gauss_vorticity_relative_l2_vs_exact_point_vorticity"],
            0.2155709070680602, places=12,
        )


if __name__ == "__main__":
    unittest.main()
