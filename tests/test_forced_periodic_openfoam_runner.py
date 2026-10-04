import json
import tempfile
import unittest
from pathlib import Path

from tools.run_forced_periodic_openfoam import build_cases
from tools.verify_forced_periodic_openfoam_run import observed_order


class ForcedPeriodicOpenFoamRunnerTests(unittest.TestCase):
    def test_frozen_case_schedule_contains_three_space_and_time_levels(self):
        protocol = json.loads(Path("protocols/of13-forced-periodic-control-v1.json").read_text())
        cases = build_cases(protocol)
        spatial = [row for row in cases if row["group"] == "spatial"]
        temporal = [row for row in cases if row["group"] == "temporal"]
        self.assertEqual([row["n"] for row in spatial], [16, 32, 64])
        self.assertEqual([row["dt"] for row in spatial], [0.001, 0.001, 0.001])
        self.assertEqual([row["dt"] for row in temporal], [0.002, 0.001, 0.0005])
        self.assertTrue(all(row["n"] == 32 for row in temporal))
        self.assertEqual(len({row["name"] for row in cases}), len(cases))

    def test_schedule_rejects_unfrozen_invalid_parameters(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.json"
            path.write_text(json.dumps({"end": 0.05, "nu": 0.01, "cases": []}))
            with self.assertRaisesRegex(ValueError, "spatial_cases"):
                build_cases(json.loads(path.read_text()))

    def test_observed_order_uses_the_refinement_ratio(self):
        self.assertAlmostEqual(observed_order(1.0, 0.25), 2.0)
        with self.assertRaisesRegex(ValueError, "positive"):
            observed_order(0.0, 0.25)


if __name__ == "__main__":
    unittest.main()
