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

    def test_rejects_invalid_resolution(self):
        with self.assertRaisesRegex(ValueError, "integer"):
            predict(3.5)


if __name__ == "__main__":
    unittest.main()
