"""Exact continuum mean kinetic energy formula, numerically evaluated via Bessel I."""
import math
from scipy.special import ive

def mean_energy(time=0.,sigma=.5):
    if not math.isfinite(time) or not math.isfinite(sigma) or sigma<=0:raise ValueError('finite time and positive sigma required')
    beta=1/sigma**2
    return float(7*beta*math.exp(-2*time)*ive(1,2*beta)*ive(0,2*beta)**2)
