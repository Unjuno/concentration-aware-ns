import unittest


class GradientGlobalCoverHelpersTests(unittest.TestCase):
    def test_bisection_children_cover_parent_without_gaps(self):
        from tools.physicsnemo_gradient_global_cover import split_box
        parent = ((-3.2, 3.2), (-1.0, 1.0), (2.0, 4.0))
        left, right = split_box(parent)
        changed = [i for i in range(3) if left[i] != parent[i]]
        self.assertEqual(len(changed), 1)
        axis = changed[0]
        self.assertEqual(left[axis][0], parent[axis][0])
        self.assertEqual(left[axis][1], right[axis][0])
        self.assertEqual(right[axis][1], parent[axis][1])
        for other in range(3):
            if other != axis:
                self.assertEqual(left[other], parent[other])
                self.assertEqual(right[other], parent[other])

    def test_arb_frobenius_bounds_enclose_point_matrix(self):
        from flint import arb
        from tools.physicsnemo_gradient_global_cover import frobenius_lower, frobenius_upper
        matrix = [[arb(3, "0.01"), arb(-4, "0.02"), arb(0)],
                  [arb(0), arb(0), arb(0)], [arb(0), arb(0), arb(0)]]
        lower, upper = frobenius_lower(matrix), frobenius_upper(matrix)
        self.assertLessEqual(lower, 5.0)
        self.assertGreaterEqual(upper, 5.0)


if __name__ == "__main__":
    unittest.main()
