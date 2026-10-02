import unittest
import json
import tarfile
from pathlib import Path

from tools.high_gradient_acceptance import local_quality, matrix_reproduction, standard_acceptance


def case(n, standard, quality, dt=0.001):
    return {
        "parameters": {"n": n, "dt": dt},
        "standard_acceptance": {"status": standard},
        "local_quality": {"status": quality},
    }


def fv_solution(tolerance="1e-8", outer=12):
    return (f"PIMPLE {{ nOuterCorrectors {outer}; outerCorrectorResidualControl "
            f"{{ p {{ tolerance {tolerance}; relTol 0; }} "
            f"U {{ tolerance {tolerance}; relTol 0; }} }} }}")


class HighGradientAcceptanceTests(unittest.TestCase):
    def test_standard_gate_requires_every_expected_step_to_converge(self):
        log = "Time = 0.001s\nPIMPLE: Converged in 4 iterations\nTime = 0.002s\nPIMPLE: Converged in 5 iterations\nEnd\n"
        result = standard_acceptance(log, 0.002, 0.001, 1e-8, 12, fv_solution())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observed_time_steps"], 2)
        self.assertEqual(result["maximum_observed_outer_correctors"], 5)
        self.assertTrue(result["time_sequence_matches_fixed_delta_t"])

    def test_standard_gate_rejects_duplicate_or_skipped_time_records(self):
        log = "\n".join(
            line
            for time_value in (0.001, 0.001, 0.003)
            for line in (f"Time = {time_value:g}s", "PIMPLE: Converged in 5 iterations")
        ) + "\nEnd\n"
        result = standard_acceptance(log, 0.003, 0.001, 1e-8, 12, fv_solution())
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["time_sequence_matches_fixed_delta_t"])
        self.assertEqual(result["time_sequence_mismatches_zero_based"], [1])

    def test_standard_gate_fails_completed_run_missing_convergence(self):
        log = "Time = 0.001s\nPIMPLE: Converged in 4 iterations\nTime = 0.002s\nEnd\n"
        result = standard_acceptance(log, 0.002, 0.001, 1e-8, 12, fv_solution())
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["failed_or_missing_convergence_steps_zero_based"], [1])

    def test_standard_gate_rejects_configuration_outside_frozen_thresholds(self):
        log = "Time = 0.001s\nPIMPLE: Converged in 4 iterations\nEnd\n"
        result = standard_acceptance(log, 0.001, 0.001, 1e-8, 12, fv_solution("1e-6"))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["outer_residual_control_configuration_matches_protocol"])

    def test_standard_gate_leaves_truncated_or_unparseable_run_uncertain(self):
        self.assertEqual(standard_acceptance("Time = 0.001s\n", 0.002, 0.001, 1e-8, 12, fv_solution())["status"], "UNCERTAIN")
        self.assertEqual(standard_acceptance("End\n", 0.002, 0.001, 1e-8, 12, fv_solution())["status"], "UNCERTAIN")

    def test_parser_accepts_a_preserved_foundation13_run_log(self):
        archive = Path("evidence/of13-study-v1/n64-dt0.001.tar.gz")
        with tarfile.open(archive) as tar:
            params = json.load(tar.extractfile("parameters.json"))
            log = tar.extractfile("log.foamRun").read().decode()
            config = tar.extractfile("system/fvSolution").read().decode()
        result = standard_acceptance(log, params["end"], params["dt"], 1e-8, 12, config)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observed_time_steps"], 50)
        self.assertEqual(result["pimple_convergence_records"], 50)

    def test_parser_accepts_a_preserved_high_gradient_v2_run_log(self):
        archive = Path("evidence/of13-high-gradient-v2/n64-dt0.001.tar.gz")
        with tarfile.open(archive) as tar:
            params = json.load(tar.extractfile("n64-dt0.001/parameters.json"))
            log = tar.extractfile("n64-dt0.001/log.foamRun").read().decode()
            config = tar.extractfile("n64-dt0.001/system/fvSolution").read().decode()
        result = standard_acceptance(log, params["end"], params["dt"], 1e-8, 12, config)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["time_sequence_matches_fixed_delta_t"])
        self.assertEqual(result["time_sequence_mismatches_zero_based"], [])

    def test_blind_spot_requires_both_adequately_resolved_levels(self):
        self.assertEqual(matrix_reproduction([case(64, "PASS", "FAIL"), case(128, "PASS", "FAIL")])["status"], "REPRODUCED")
        self.assertEqual(matrix_reproduction([case(64, "PASS", "PASS"), case(128, "PASS", "PASS")])["status"], "NOT_OBSERVED")
        self.assertEqual(matrix_reproduction([case(64, "PASS", "FAIL")])["status"], "UNCERTAIN")
        self.assertEqual(matrix_reproduction([case(64, "FAIL", "FAIL"), case(128, "PASS", "FAIL")])["status"], "UNCERTAIN")

    def test_coarse_disagreement_is_reported_but_does_not_override_fine_grid_rule(self):
        cases = [
            case(16, "PASS", "FAIL"),
            case(32, "PASS", "FAIL"),
            case(64, "PASS", "PASS"),
            case(128, "PASS", "PASS"),
        ]
        self.assertEqual(matrix_reproduction(cases)["status"], "NOT_OBSERVED")

    def test_local_gate_keeps_missing_metrics_uncertain_and_reports_threshold_failures(self):
        thresholds = {"max_gradient": 0.05, "shell_spectrum": 0.05}
        self.assertEqual(local_quality({"max_gradient": 0.01}, thresholds)["status"], "UNCERTAIN")
        result = local_quality({"max_gradient": 0.06, "shell_spectrum": 0.01}, thresholds)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["metrics"]["max_gradient"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
