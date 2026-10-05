import hashlib
from pathlib import Path
import tempfile
import unittest

import sympy as sp

from tools.audit_openfoam_stress_operator import (
    internal_face_balance, interpolation_defect, verify_source_tree,
)


class StressOperatorControls(unittest.TestCase):
    def test_constant_product_large_contrast_is_not_preserved_by_separate_blends(self):
        # Each endpoint product is one; the separate midpoint product is 25.5025.
        actual = interpolation_defect(1, 100, 1, sp.Rational(1, 100),
                                     sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2))
        self.assertEqual(actual, -sp.Rational(9801, 400))

    def test_constant_coefficient_requires_matching_tensor_weights(self):
        self.assertEqual(interpolation_defect(2, 2, 0, 1,
                         sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(1, 2)), 0)
        self.assertEqual(interpolation_defect(2, 2, 0, 1,
                         sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(3, 4)), sp.Rational(1, 2))

    def test_multiple_faces_cancel_in_integrated_balance(self):
        volumes = [sp.Integer(2), sp.Integer(3), sp.Integer(5)]
        density = internal_face_balance([sp.Integer(7), sp.Integer(-4)], [0, 1], [1, 2], volumes)
        self.assertEqual(density, [sp.Rational(7, 2), -sp.Rational(11, 3), sp.Rational(4, 5)])
        self.assertEqual(sum(v * d for v, d in zip(volumes, density)), 0)

    def test_refined_planar_layer_conserves_globally_while_local_norm_grows(self):
        rows = []
        for n in (8, 16):
            h = sp.Rational(1, n)
            fluxes = [h**2] * n**2
            owners, neighbours = list(range(n**2)), list(range(n**2, 2*n**2))
            volumes = [h**3] * (2*n**2)
            d = internal_face_balance(fluxes, owners, neighbours, volumes)
            rows.append((sum(v*x for v,x in zip(volumes,d)),
                         sum(v*abs(x) for v,x in zip(volumes,d)),
                         sum(v*x*x for v,x in zip(volumes,d)), max(abs(x) for x in d)))
        self.assertEqual(rows, [(0, 2, 16, 8), (0, 2, 32, 16)])

    def test_source_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'source.C'
            path.write_bytes(b'fixed source\n')
            manifest = {'files': [{'role': 'current', 'path': 'source.C',
                                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}
            self.assertEqual(verify_source_tree(manifest, folder), 1)
            path.write_bytes(b'changed source\n')
            with self.assertRaisesRegex(ValueError, 'source hash mismatch'):
                verify_source_tree(manifest, folder)


if __name__ == '__main__':
    unittest.main()
