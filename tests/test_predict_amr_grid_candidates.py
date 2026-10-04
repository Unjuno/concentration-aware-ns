import json
from pathlib import Path
import unittest

from tools.predict_amr_grid_candidates import predict


class PredictAmrGridCandidatesTests(unittest.TestCase):
    def test_matches_archived_n16_selection_and_predicts_n32(self):
        self.assertEqual(
            predict(16)["one_layer_periodic_face_buffer_candidates"], 1792
        )
        result = predict(32)
        self.assertEqual(result["raw_sensor_candidates"], 10368)
        self.assertEqual(
            result["one_layer_periodic_face_buffer_candidates"], 12288
        )
        self.assertEqual(result["predicted_cells_after_one_level"], 118784)

    def test_frozen_n64_amr_protocol_matches_independent_prediction(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "protocols/high-gradient-of13-amr-same-run-map-v7-n64.json"
        protocol = json.loads(path.read_text())
        case = protocol["case"]
        prediction = predict(64)
        self.assertEqual(case["initial_cells"], prediction["initial_cells"])
        self.assertEqual(
            case["predicted_sensor_candidates"], prediction["raw_sensor_candidates"]
        )
        self.assertEqual(
            case["predicted_buffered_candidates"],
            prediction["one_layer_periodic_face_buffer_candidates"],
        )
        self.assertEqual(
            case["expected_mapped_cells"],
            prediction["predicted_cells_after_one_level"],
        )

    def test_rejects_invalid_resolution(self):
        with self.assertRaisesRegex(ValueError, "integer"):
            predict(3.5)


if __name__ == "__main__":
    unittest.main()
