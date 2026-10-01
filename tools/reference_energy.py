"""Exact continuum mean kinetic energy formula, numerically evaluated via Bessel I."""
import math
from scipy.special import ive

def mean_energy(time=0.,sigma=.5):
    if not math.isfinite(time) or not math.isfinite(sigma) or sigma<=0:raise ValueError('finite time and positive sigma required')
    beta=1/sigma**2
    return float(7*beta*math.exp(-2*time)*ive(1,2*beta)*ive(0,2*beta)**2)


def periodic_vertex_mean_energy(n, time=0., sigma=.5):
    """Exact finite-grid mean of the analytic field's kinetic energy.

    This is the mean over unique Cartesian vertices x_j=2*pi*j/n on each
    periodic axis, not a continuum integral and not an estimate from a solver
    field. Separability and reflection symmetry reduce the 3-D sum to two
    one-dimensional finite sums.
    """
    import numpy as np

    if type(n) is not int or n < 1:
        raise ValueError('n must be a positive integer')
    if not math.isfinite(time) or not math.isfinite(sigma) or sigma <= 0:
        raise ValueError('finite time and positive sigma required')
    beta = 1 / sigma**2
    z = 2 * beta
    d = 2 * math.pi * np.arange(n, dtype=float) / n - math.pi
    weight = np.exp(z * np.cos(d))
    mean_weight = float(np.mean(weight))
    mean_sin2_weight = float(np.mean(weight * np.sin(d)**2))
    # For a=(1,2,3), |q x a|^2 has diagonal weights (13,10,5)*beta^2.
    # Cross terms vanish in the symmetric periodic grid; their sum is 28.
    return float(14 * beta**2 * math.exp(-2*time - 3*z)
                 * mean_sin2_weight * mean_weight**2)
