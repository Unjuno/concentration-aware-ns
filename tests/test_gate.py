import copy
import unittest
from tools.acceptance_gate import evaluate


class GateTests(unittest.TestCase):
    def setUp(self):
        self.report = {
            "standard_acceptance": "PASS",
            "evidence": {k: True for k in (
                "reference_verified", "forcing_verified", "derivatives_verified",
                "space_time_study_verified", "thresholds_preregistered",
                "raw_artifacts_reviewed", "evaluation_time_verified")},
            "metrics": [{"name": n, "error": 0.02, "tolerance": 0.01}
                        for n in ("max_gradient", "max_vorticity")],
        }

    def test_missing_evidence_never_reproduces(self):
        for key in self.report["evidence"]:
            report = copy.deepcopy(self.report)
            del report["evidence"][key]
            self.assertEqual(evaluate(report)["hypothesis"], "UNCERTAIN")

    def test_valid_discrepancy(self):
        self.assertEqual(evaluate(self.report)["hypothesis"], "REPRODUCED")

    def test_standard_failure_is_not_a_missed_acceptance(self):
        self.report["standard_acceptance"] = "FAIL"
        self.assertEqual(evaluate(self.report)["hypothesis"], "UNCERTAIN")

    def test_invalid_numeric_values(self):
        for value in (None, True, -1, float("nan"), float("inf"), "0.1"):
            self.report["metrics"][0]["error"] = value
            self.assertEqual(evaluate(self.report)["local_quality"], "UNCERTAIN")

    def test_passing_local_errors(self):
        for metric in self.report["metrics"]:
            metric["error"] = 0.001
        self.assertEqual(evaluate(self.report)["hypothesis"], "NOT_OBSERVED")

    def test_missing_required_metric(self):
        self.report["metrics"].pop()
        self.assertEqual(evaluate(self.report)["local_quality"], "UNCERTAIN")
