import io
import tarfile
import tempfile
import unittest

import numpy as np

from tools.analyze_amr_gauss_gradient import (
    _read_csv,
    gauss_gradient_from_internal_faces,
    interior_periodic_mask,
    vorticity_from_gradient,
)


class AmrGaussGradientTests(unittest.TestCase):
    def test_snapshot_csv_is_streamed_across_multiple_batches(self):
        rows = ["x,y"] + [f"{index},{index * 2}" for index in range(9000)]
        payload = ("\n".join(rows) + "\n").encode()
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as archive_path:
            with tarfile.open(archive_path.name, "w:gz") as archive:
                member = tarfile.TarInfo("snapshot.csv")
                member.size = len(payload)
                archive.addfile(member, io.BytesIO(payload))
            table = _read_csv(archive_path.name, "snapshot.csv")
        self.assertEqual(len(table["x"]), 9000)
        np.testing.assert_array_equal(table["x"][[0, -1]], [0, 8999])
        np.testing.assert_array_equal(table["y"][[0, -1]], [0, 17998])

    def test_gauss_reconstruction_and_curl_for_linear_vector_field(self):
        matrix = np.array([[1.0, 2.0, -1.0], [0.5, -2.0, 3.0], [4.0, 1.0, 0.25]])
        offset = np.array([0.2, -0.7, 1.3])
        area = np.vstack((np.eye(3), -np.eye(3)))
        centers = 0.5*area
        face_u = centers @ matrix.T + offset
        gradient = gauss_gradient_from_internal_faces(
            np.ones(7), np.zeros(6, dtype=int), np.arange(1, 7), face_u, area
        )
        np.testing.assert_allclose(gradient[0], matrix, atol=1e-15, rtol=0)
        expected_vorticity = np.array([
            matrix[2, 1]-matrix[1, 2],
            matrix[0, 2]-matrix[2, 0],
            matrix[1, 0]-matrix[0, 1],
        ])
        np.testing.assert_allclose(
            vorticity_from_gradient(gradient)[0], expected_vorticity,
            atol=1e-15, rtol=0,
        )

    def test_mask_excludes_periodic_boundary_cells(self):
        centers = np.array([[0.1, 1.0, 1.0], [0.5, 1.0, 1.0]])
        mask = interior_periodic_mask(centers, np.full(2, 0.04), domain_length=2.0)
        np.testing.assert_array_equal(mask, [False, True])


if __name__ == "__main__":
    unittest.main()
