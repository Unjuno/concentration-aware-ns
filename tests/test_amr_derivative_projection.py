import unittest

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.amr_derivative_projection import derivative_moments, split_derivative_error


def direct_gradient(points, frequency, time):
    """Independent real-space differentiation of g=((1+cos q)/2)^4."""
    x, y, z = points.T
    def factors(q):
        a = (1+np.cos(q))/2
        return a**4, -2*np.sin(q)*a**3, -2*np.cos(q)*a**3+3*np.sin(q)**2*a**2
    gy, dy, ddy = factors(y)
    gz, dz, _ = factors(z)
    s, c, n = np.sin(frequency*x), np.cos(frequency*x), frequency
    gradient = np.zeros((len(points), 3, 3))
    gradient[:, 0, 0] = c*dy*gz/n
    gradient[:, 0, 1] = s*ddy*gz/n**2
    gradient[:, 0, 2] = s*dy*dz/n**2
    gradient[:, 1, 0] = s*gy*gz
    gradient[:, 1, 1] = -c*dy*gz/n
    gradient[:, 1, 2] = -c*gy*dz/n
    return gradient*np.exp(-time)


class DerivativeProjectionTests(unittest.TestCase):
    def test_means_and_energies_match_independent_real_space_quadrature(self):
        centers = np.array([[.1, .2, .4], [2.2, 1.9, 3.1], [6.1, 5.8, 5.4]])
        widths = np.array([2*np.pi/16, 2*np.pi/32, 2*np.pi/64])
        nodes, weights = leggauss(12)
        for n in (1, 4, 7):
            with self.subTest(frequency=n):
                result = derivative_moments(centers, widths, .002, n)
                means = np.zeros((3, 3, 3))
                curls = np.zeros((3, 3))
                grad_sq, curl_sq = np.zeros(3), np.zeros(3)
                for i, wi in zip(nodes, weights):
                    for j, wj in zip(nodes, weights):
                        for k, wk in zip(nodes, weights):
                            p = centers+widths[:, None]*np.array([i, j, k])/2
                            g = direct_gradient(p, n, .002)
                            curl = np.stack((g[:, 2, 1]-g[:, 1, 2], g[:, 0, 2]-g[:, 2, 0],
                                             g[:, 1, 0]-g[:, 0, 1]), axis=-1)
                            w = wi*wj*wk/8
                            means += w*g
                            curls += w*curl
                            grad_sq += w*np.sum(g*g, axis=(-2, -1))
                            curl_sq += w*np.sum(curl*curl, axis=-1)
                for key, value in (("gradient_mean", means), ("curl_mean", curls),
                                   ("gradient_mean_square", grad_sq), ("curl_mean_square", curl_sq)):
                    np.testing.assert_allclose(result[key], value, atol=2e-14, rtol=2e-10)

    def test_exact_projection_attains_floor_and_constant_perturbation_adds_known_energy(self):
        centers = np.array([[.4, .3, .2], [1.1, .5, .6]])
        widths = np.array([.2, .1])
        means = derivative_moments(centers, widths, .002)["gradient_mean"]
        exact = split_derivative_error(centers, widths, widths**3, means, .002, chunk_cells=1)
        self.assertEqual(exact["gradient"]["mean_mismatch_relative_l2"], 0)
        self.assertEqual(exact["curl"]["mean_mismatch_relative_l2"], 0)
        self.assertGreater(exact["gradient"]["projection_floor_relative_l2"], 0)
        shift = np.zeros((3, 3))
        shift[1, 0] = 2
        perturbed = split_derivative_error(centers, widths, widths**3, means+shift, .002)
        for kind in ("gradient", "curl"):
            self.assertAlmostEqual(perturbed[kind]["mean_mismatch_integrated_energy"],
                                   4*np.sum(widths**3), places=14)
            self.assertEqual(perturbed[kind]["projection_floor_integrated_energy"],
                             exact[kind]["projection_floor_integrated_energy"])

    def test_nested_exact_moments_preserve_integrals(self):
        center, width = np.array([[.4, .3, .2]]), .4
        parent = derivative_moments(center, np.array([width]), .002)
        offsets = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)])
        child = derivative_moments(center+width*offsets/4, np.full(8, width/2), .002)
        for key in parent:
            np.testing.assert_allclose(child[key].mean(axis=0), parent[key][0], atol=2e-14, rtol=2e-12)
        self.assertGreater(np.sum(child["gradient_mean"]**2)/8,
                           np.sum(parent["gradient_mean"]**2))

    def test_invalid_geometry_and_nonfinite_tensors_rejected(self):
        centers, widths = np.zeros((1, 3)), np.ones(1)
        bad = ((centers, np.array([0.])), (centers, np.array([np.nan])),
               (np.full((1, 3), np.inf), widths), (centers, np.ones(2)),
               (np.zeros((0, 3)), np.zeros(0)))
        for c, w in bad:
            with self.subTest(centers=c, widths=w), self.assertRaises(ValueError):
                derivative_moments(c, w, .002)
        for time, frequency in ((np.nan, 4), (-1000, 4), (1000, 4), (.002, 0), (.002, 4.0)):
            with self.subTest(time=time, frequency=frequency), self.assertRaises(ValueError):
                derivative_moments(centers, widths, time, frequency)
        for tensor, volume in ((np.full((1, 3, 3), np.nan), np.ones(1)),
                               (np.zeros((1, 3, 3)), np.array([2.])),
                               (np.zeros((1, 3)), np.ones(1))):
            with self.assertRaises(ValueError):
                split_derivative_error(centers, widths, volume, tensor, .002)


if __name__ == "__main__":
    unittest.main()
