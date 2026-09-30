import math

import unittest


class AdaptiveLocalCoverTests(unittest.TestCase):
    def test_binary_cover_refines_worst_cell_and_covers_parent(self):
        from tools.arb_local_branch_cover import adaptive_axis_bisect_cover

        result = adaptive_axis_bisect_cover(
            [(-1.0, 1.0)] * 3,
            lambda box: sum((hi-lo)**2 for lo, hi in box),
            target=7.0,
            max_evaluations=15,
        )
        self.assertTrue(result["target_met"])
        self.assertEqual(result["evaluation_count"], 7)
        self.assertEqual(result["leaf_count"], 4)
        self.assertAlmostEqual(sum(
            math.prod(hi-lo for lo, hi in leaf["box"])
            for leaf in result["leaves"]
        ), 8.0)
        self.assertLessEqual(result["maximum_leaf_upper"], 7.0)

    def test_budget_stop_is_explicit_and_keeps_cover(self):
        from tools.arb_local_branch_cover import adaptive_axis_bisect_cover

        result = adaptive_axis_bisect_cover(
            [(-1.0, 1.0)] * 3,
            lambda box: sum((hi-lo)**2 for lo, hi in box),
            target=1.0,
            max_evaluations=3,
        )
        self.assertFalse(result["target_met"])
        self.assertEqual(result["stop_reason"], "evaluation_budget")
        self.assertEqual(result["evaluation_count"], 3)
        self.assertAlmostEqual(sum(
            math.prod(hi-lo for lo, hi in leaf["box"])
            for leaf in result["leaves"]
        ), 8.0)


if __name__ == "__main__":
    import math
    unittest.main()
