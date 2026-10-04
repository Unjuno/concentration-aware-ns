import unittest

import numpy as np

from tools.analyze_amr_stage_snapshots import parent_value_injection_audit


class ParentInjectionAuditTests(unittest.TestCase):
    def test_piecewise_constant_parent_injection_and_volume_closure(self):
        n = 2
        h = np.pi
        axis = (np.arange(n) + 0.5) * h
        centers = np.array([(x, y, z) for z in axis for y in axis for x in axis])
        values = np.column_stack((centers[:, 0], centers[:, 1], centers[:, 2]))
        parent_volume = np.full(n**3, h**3)

        child_centers = []
        child_values = []
        child_volumes = []
        for center, value in zip(centers, values):
            offsets = (-h/4, h/4)
            for dz in offsets:
                for dy in offsets:
                    for dx in offsets:
                        child_centers.append(center + (dx, dy, dz))
                        child_values.append(value)
                        child_volumes.append(h**3/8)

        audit = parent_value_injection_audit(
            centers, values, parent_volume,
            np.asarray(child_centers), np.asarray(child_values),
            np.asarray(child_volumes), domain_length=2*np.pi,
        )
        self.assertEqual(audit["parent_grid_cells_per_axis"], n)
        self.assertEqual(audit["mapped_cells"], 8*n**3)
        self.assertEqual(audit["parent_group_size_counts"], {"8": n**3})
        self.assertLess(audit["parent_volume_closure_relative_max"], 1e-14)
        self.assertEqual(audit["mapped_vs_parent_injection_relative_l2"], 0.0)
        self.assertEqual(audit["mapped_vs_parent_injection_max_abs"], 0.0)

    def test_parent_grid_must_be_complete_uniform_cube(self):
        centers = np.array([[0.5, 0.5, 0.5], [1.5, 0.5, 0.5]])
        with self.assertRaisesRegex(ValueError, r"n\^3"):
            parent_value_injection_audit(
                centers, centers, np.ones(2), centers, centers, np.ones(2),
                domain_length=2.0,
            )


if __name__ == "__main__":
    unittest.main()
