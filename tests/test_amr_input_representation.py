import unittest
import numpy as np
from tools.audit_amr_input_representation import diagnose
from tools.high_gradient_reference import fields
from tools.high_gradient_cell_average import exact_cell_average_velocity


class InputRepresentationTests(unittest.TestCase):
    def centers(self,n):
        return np.stack(np.meshgrid(*[(np.arange(n)+.5)*2*np.pi/n]*3,indexing='ij'),axis=-1).reshape(-1,3)

    def test_point_recipe_is_distinguished_from_exact_mean_recipe(self):
        n=8;c=self.centers(n)
        point=diagnose(c,fields(c,N=3)['u'],n)
        mean=diagnose(c,exact_cell_average_velocity(c,2*np.pi/n,0.,3),n)
        self.assertTrue(point['point_matches_at_recipe_tolerance'])
        self.assertFalse(point['exact_mean_matches_at_recipe_tolerance'])
        self.assertFalse(mean['point_matches_at_recipe_tolerance'])
        self.assertTrue(mean['exact_mean_matches_at_recipe_tolerance'])

    def test_smooth_point_mean_gap_decreases_with_refinement(self):
        errors=[]
        for n in (8,16,32):
            c=self.centers(n);q=diagnose(c,fields(c,N=3)['u'],n)
            errors.append(q['point_to_mean_relative_l2'])
        self.assertGreater(errors[0]/errors[1],3.)
        self.assertGreater(errors[1]/errors[2],3.)


if __name__=='__main__':unittest.main()
