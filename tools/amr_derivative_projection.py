"""Closed-form cube moments for the frequency-localized MMS derivatives.

These moments define an explicit P0 tensor/vector representation. They do not
declare that OpenFOAM's cell values are volume averages or continuous fields.
"""
import math

import numpy as np


def _cells(centers, widths, time, frequency):
    centers = np.asarray(centers, dtype=float)
    widths = np.asarray(widths, dtype=float)
    if (centers.ndim != 2 or centers.shape[1] != 3
            or widths.shape != (len(centers),) or len(centers) == 0
            or not np.isfinite(centers).all() or not np.isfinite(widths).all()
            or np.any(widths <= 0) or not math.isfinite(time)
            or type(frequency) is not int or frequency < 1):
        raise ValueError("finite nonempty cube geometry and valid MMS parameters required")
    with np.errstate(over="ignore", under="ignore"):
        decay = np.exp(-time)
        energy_scale = decay**2
    if not np.isfinite(decay) or decay == 0 or not np.isfinite(energy_scale) or energy_scale == 0:
        raise ValueError("MMS amplitude outside supported floating-point range")
    return centers, widths, decay


def _coefficients(order):
    modes = np.arange(-4, 5)
    g = np.array([1, 8, 28, 56, 70, 56, 28, 8, 1], dtype=float)/256
    return (1j*modes)**order*g


def _average_fourier(points, widths, coefficients):
    half = (len(coefficients)-1)//2
    modes = np.arange(-half, half+1)
    phase = np.exp(1j*points[:, None]*modes)
    weights = np.sinc(widths[:, None]*modes/(2*np.pi))
    return np.real(np.sum(phase*weights*coefficients, axis=1))


def _average_g(points, widths, order):
    return _average_fourier(points, widths, _coefficients(order))


def _average_product(points, widths, first, second):
    return _average_fourier(
        points, widths, np.convolve(_coefficients(first), _coefficients(second)))


def derivative_moments(centers, widths, time, frequency=4):
    """Return exact cube means of grad(u), curl(u), and their squared norms.

    Finite Fourier products and sinc interval integrals are evaluated in
    floating point; 'exact' refers to the formula, not interval certification.
    grad[i,j] means d(u_i)/d(x_j).
    """
    centers, widths, decay = _cells(centers, widths, time, frequency)
    x, y, z = centers.T
    n = frequency
    sy, dy, ddy = (_average_g(y, widths, k) for k in range(3))
    sz, dz = (_average_g(z, widths, k) for k in range(2))
    sx = np.sin(n*x)*np.sinc(n*widths/(2*np.pi))
    cx = np.cos(n*x)*np.sinc(n*widths/(2*np.pi))
    gradient = np.zeros((len(centers), 3, 3))
    gradient[:, 0, 0] = cx*dy*sz/n
    gradient[:, 0, 1] = sx*ddy*sz/n**2
    gradient[:, 0, 2] = sx*dy*dz/n**2
    gradient[:, 1, 0] = sx*sy*sz
    gradient[:, 1, 1] = -cx*dy*sz/n
    gradient[:, 1, 2] = -cx*sy*dz/n
    gradient *= decay
    curl = np.stack((-gradient[:, 1, 2], gradient[:, 0, 2],
                     gradient[:, 1, 0]-gradient[:, 0, 1]), axis=-1)

    y00 = _average_product(y, widths, 0, 0)
    y11 = _average_product(y, widths, 1, 1)
    y22 = _average_product(y, widths, 2, 2)
    y02 = _average_product(y, widths, 0, 2)
    z00 = _average_product(z, widths, 0, 0)
    z11 = _average_product(z, widths, 1, 1)
    s2 = .5*(1-np.cos(2*n*x)*np.sinc(n*widths/np.pi))
    c2 = .5*(1+np.cos(2*n*x)*np.sinc(n*widths/np.pi))
    grad_energy = decay**2*(
        s2*((y22*z00+y11*z11)/n**4+y00*z00)
        + c2*(2*y11*z00+y00*z11)/n**2)
    curl_energy = decay**2*(
        c2*y00*z11/n**2
        + s2*(y11*z11/n**4+(y00-2*y02/n**2+y22/n**4)*z00))
    if not all(np.isfinite(a).all() for a in (gradient, curl, grad_energy, curl_energy)):
        raise ValueError("MMS moments outside supported floating-point range")
    return {"gradient_mean": gradient, "curl_mean": curl,
            "gradient_mean_square": grad_energy, "curl_mean_square": curl_energy}


def split_derivative_error(centers, widths, volumes, gradient, time,
                           frequency=4, chunk_cells=8192):
    """Split integrated P0 errors into mean mismatch and projection floor."""
    centers, widths, _ = _cells(centers, widths, time, frequency)
    volumes = np.asarray(volumes, dtype=float)
    gradient = np.asarray(gradient, dtype=float)
    if (volumes.shape != (len(centers),) or not np.isfinite(volumes).all()
            or np.any(volumes <= 0)
            or not np.allclose(volumes, widths**3, rtol=2e-10, atol=0)
            or gradient.shape != (len(centers), 3, 3)
            or not np.isfinite(gradient).all()
            or type(chunk_cells) is not int or chunk_cells < 1):
        raise ValueError("finite tensor values, cubic volumes and positive chunk size required")
    totals = {kind: np.zeros(3) for kind in ("gradient", "curl")}
    for start in range(0, len(centers), chunk_cells):
        stop = min(start+chunk_cells, len(centers))
        moments = derivative_moments(centers[start:stop], widths[start:stop], time, frequency)
        g = gradient[start:stop]
        discrete_curl = np.stack((g[:, 2, 1]-g[:, 1, 2],
                                  g[:, 0, 2]-g[:, 2, 0],
                                  g[:, 1, 0]-g[:, 0, 1]), axis=-1)
        for kind, discrete, axes in (("gradient", g, (-2, -1)),
                                     ("curl", discrete_curl, -1)):
            mean = moments[kind+"_mean"]
            v = volumes[start:stop]
            totals[kind] += np.array([
                np.sum(v*moments[kind+"_mean_square"]),
                np.sum(v*np.sum(mean**2, axis=axes)),
                np.sum(v*np.sum((discrete-mean)**2, axis=axes)),
            ])
    result = {}
    for kind, (energy, projected, mismatch) in totals.items():
        if (not np.isfinite([energy, projected, mismatch]).all()
                or energy <= 0 or projected < 0 or mismatch < 0
                or projected > energy*(1+2e-12)):
            raise ValueError("invalid derivative-energy decomposition")
        variance = max(0.0, energy-projected)
        total = variance+mismatch
        result[kind] = {
            "exact_reference_integrated_energy": float(energy),
            "exact_cell_mean_integrated_energy": float(projected),
            "mean_mismatch_integrated_energy": float(mismatch),
            "projection_floor_integrated_energy": float(variance),
            "mean_mismatch_relative_l2": float(np.sqrt(mismatch/energy)),
            "projection_floor_relative_l2": float(np.sqrt(variance/energy)),
            "p0_total_relative_l2": float(np.sqrt(total/energy)),
            "projection_fraction_of_squared_error": float(variance/total) if total > 0 else None,
        }
    return result
