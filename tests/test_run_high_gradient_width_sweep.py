import hashlib
import json
import unittest
from pathlib import Path

from tools.audit_high_gradient_width_sweep import audit
from tools.run_high_gradient_width_sweep import (
    build_cases, resolution_gate, classify_width, verify_reference_artifact,
)


class RunHighGradientWidthSweepTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = Path("protocols/high-gradient-of13-width-v1.json")
        cls.protocol = json.loads(cls.path.read_text())

    def test_matrix_is_deduplicated_and_contains_each_frozen_case(self):
        cases = build_cases(self.protocol)
        self.assertEqual(len(cases), 15)
        self.assertEqual(len({case["name"] for case in cases}), 15)
        for power in self.protocol["envelope_powers"]:
            rows = [case for case in cases if case["envelope_power"] == power]
            self.assertEqual(len(rows), 5)
            self.assertEqual(sum(case["group"] == "spatial" for case in rows), 3)
            self.assertEqual(sum(case["group"] == "temporal" for case in rows), 2)

    def test_reference_gate_clears_both_fine_grids_for_all_widths(self):
        counts = (32, 64, 128)
        result = audit(tuple(self.protocol["envelope_powers"]), counts,
                       str(self.path))
        gate = resolution_gate(self.protocol, result)
        self.assertTrue(all(gate[str(power)][str(n)]["passed"]
                            for power in self.protocol["envelope_powers"]
                            for n in (64, 128)))

    def test_frozen_reference_artifact_replays_before_solver_run(self):
        result = audit(tuple(self.protocol["envelope_powers"]), (32, 64, 128),
                       str(self.path))
        artifact = Path(self.protocol["reference_resolution_gate"]["artifact"])
        self.assertEqual(verify_reference_artifact(artifact, result),
                         hashlib.sha256(artifact.read_bytes()).hexdigest())

    def test_width_classification_requires_both_fine_grid_cases(self):
        cases = []
        for n in (64, 128):
            cases.append({"parameters": {"envelope_power": 2, "n": n,
                                          "dt": 0.001},
                          "standard_acceptance": {"status": "PASS"},
                          "local_quality": {"status": "FAIL"}})
        resolution = {"2": {"64": {"passed": True}, "128": {"passed": True}}}
        result = classify_width(cases, 2, (64, 128), resolution)
        self.assertEqual(result["status"], "REPRODUCED")
        cases.pop()
        self.assertEqual(classify_width(cases, 2, (64, 128), resolution)["status"],
                         "UNCERTAIN")


if __name__ == "__main__":
    unittest.main()
