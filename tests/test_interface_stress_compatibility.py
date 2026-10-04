import unittest
import sympy as sp

from tools.check_interface_stress_compatibility import couette_chain, normal_dev2_jump


class InterfaceStressCompatibility(unittest.TestCase):
    def test_admissible_tangential_jump_annihilates_normal_correction(self):
        normal=sp.Matrix([sp.Rational(1,3),sp.Rational(2,3),sp.Rational(2,3)])
        self.assertEqual(normal_dev2_jump(normal,[-2,1,0]),sp.zeros(1,3))
        self.assertEqual(normal_dev2_jump([1,0,0],[3,0,0]),sp.Matrix([[1,0,0]]))

    def test_resistance_solution_matches_independent_stiffness_matrix(self):
        for n in (6,12):
            for harmonic in (False,True):
                h=sp.Rational(2,n);left,right=sp.Integer(1),sp.Integer(100)
                matrix=sp.zeros(n);rhs=sp.zeros(n,1)
                for face in range(1,n):
                    mu=(left if face<n//2 else right if face>n//2 else
                        2*left*right/(left+right) if harmonic else (left+right)/2)
                    conductance=mu/h;i,j=face-1,face
                    matrix[i,i]+=conductance;matrix[j,j]+=conductance
                    matrix[i,j]-=conductance;matrix[j,i]-=conductance
                matrix[0,0]+=2*left/h;rhs[0]=2*left/h*(-1/left)
                matrix[-1,-1]+=2*right/h;rhs[-1]=2*right/h*(1/right)
                direct=matrix.inv()*rhs
                result=couette_chain(n,left,right,harmonic=harmonic)
                self.assertEqual(list(direct),result['values'])
                self.assertEqual(matrix*direct-rhs,sp.zeros(n,1))

    def test_harmonic_interface_recovers_exact_piecewise_shear(self):
        for n in (16,32,64):
            row=couette_chain(n,1,100,harmonic=True)
            self.assertEqual(row['flux'],1)
            self.assertEqual(row['values'],row['reference'])

    def test_arithmetic_solved_flux_has_uniform_contrast_bound(self):
        for n in (16,32,64):
            row=couette_chain(n,1,100)
            self.assertGreater(row['flux'],1)
            self.assertLess(row['flux'],sp.Rational(n,n-1))

    def test_relative_metrics_require_nonzero_traction(self):
        with self.assertRaisesRegex(ValueError, "nonzero traction"):
            couette_chain(16,1,100,traction=0)
        negative=couette_chain(16,1,100,traction=-1)
        positive=couette_chain(16,1,100,traction=1)
        self.assertEqual(negative['flux'],-positive['flux'])
        self.assertEqual(negative['relative_flux_error'],positive['relative_flux_error'])
        self.assertEqual(negative['relative_velocity_L2_squared'],positive['relative_velocity_L2_squared'])


if __name__ == '__main__':
    unittest.main()
