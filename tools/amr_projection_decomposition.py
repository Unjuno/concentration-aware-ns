"""L2-orthogonal decomposition for an explicit piecewise-constant field."""
import math
from fractions import Fraction
import numpy as np


def exact_mms_mean_square_velocity(time, frequency=4):
    """Parseval mean of |u|^2 for the localized cosine-envelope MMS."""
    if not math.isfinite(time) or type(frequency) is not int or frequency < 1:
        raise ValueError("finite time and positive integer frequency required")
    a = Fraction(6435, 32768)  # mean of g(q)^2
    b = Fraction(429, 2048)   # mean of g'(q)^2
    return math.exp(-2*time)*(
        float(b*a)/(2*frequency**4)+float(a*a)/(2*frequency**2))


def exact_cell_mean_square_velocity(centers, widths, time, frequency=4):
    """Exact cell means of |u|^2 for Cartesian cubes of possibly varying widths."""
    centers, widths = _validated_cells(centers, widths, time, frequency)
    avg_g2_y = _cell_average_g_derivative_squared(centers[:, 1], widths, 0)
    avg_g2_z = _cell_average_g_derivative_squared(centers[:, 2], widths, 0)
    avg_dg2_y = _cell_average_g_derivative_squared(centers[:, 1], widths, 1)
    sinc_x = np.sinc(frequency*widths/np.pi)
    avg_sin2 = .5*(1-sinc_x*np.cos(2*frequency*centers[:, 0]))
    avg_cos2 = .5*(1+sinc_x*np.cos(2*frequency*centers[:, 0]))
    return np.exp(-2*time)*(
        avg_sin2*avg_dg2_y*avg_g2_z/frequency**4
        + avg_cos2*avg_g2_y*avg_g2_z/frequency**2
    )


def exact_mms_mean_square_gradient(time, frequency=4):
    """Parseval mean of the squared Frobenius norm of the MMS velocity gradient."""
    if not math.isfinite(time) or type(frequency) is not int or frequency < 1:
        raise ValueError("finite time and positive integer frequency required")
    a = float(Fraction(6435, 32768))
    b = float(Fraction(429, 2048))
    c = float(Fraction(165, 256))
    n = frequency
    return math.exp(-2*time)*(
        .5*(c*a+b*b)/n**4+.5*a*a+1.5*b*a/n**2)


def exact_cell_mean_square_gradient(centers, widths, time, frequency=4):
    """Exact cube means of |grad u|_F^2 for the localized cosine-envelope MMS."""
    centers, widths = _validated_cells(centers, widths, time, frequency)
    gy0 = _cell_average_g_derivative_squared(centers[:, 1], widths, 0)
    gz0 = _cell_average_g_derivative_squared(centers[:, 2], widths, 0)
    gy1 = _cell_average_g_derivative_squared(centers[:, 1], widths, 1)
    gz1 = _cell_average_g_derivative_squared(centers[:, 2], widths, 1)
    gy2 = _cell_average_g_derivative_squared(centers[:, 1], widths, 2)
    sinc_x = np.sinc(frequency*widths/np.pi)
    avg_sin2 = .5*(1-sinc_x*np.cos(2*frequency*centers[:, 0]))
    avg_cos2 = .5*(1+sinc_x*np.cos(2*frequency*centers[:, 0]))
    return np.exp(-2*time)*(
        avg_sin2*(gy2*gz0+gy1*gz1)/frequency**4
        + avg_sin2*gy0*gz0
        + avg_cos2*(2*gy1*gz0+gy0*gz1)/frequency**2
    )


def _validated_cells(centers, widths, time, frequency):
    centers = np.asarray(centers, dtype=float)
    widths = np.asarray(widths, dtype=float)
    if (centers.ndim != 2 or centers.shape[1] != 3 or widths.shape != (len(centers),)
            or not np.isfinite(centers).all() or not np.isfinite(widths).all()
            or np.any(widths <= 0) or not math.isfinite(time)
            or type(frequency) is not int or frequency < 1):
        raise ValueError("finite centers, positive cube widths and valid MMS parameters required")
    return centers, widths


def _cell_average_g_derivative_squared(points, widths, derivative_order):
    amplitudes = {1: 56.0, 2: 28.0, 3: 8.0, 4: 1.0}
    modes = np.arange(-4, 5)
    g = np.zeros(9, dtype=complex)
    g[4] = 35/128
    for mode, amplitude in amplitudes.items():
        g[4+mode] = g[4-mode] = amplitude/256
    derivative = (1j*modes)**derivative_order*g
    squared = np.convolve(derivative, derivative)
    square_modes = np.arange(-8, 9)
    phase = np.exp(1j*points[:, None]*square_modes[None, :])
    # The Fourier average over each symmetric interval is sinc(k*h/2).
    weights = np.sinc(square_modes[None, :]*widths[:, None]/(2*np.pi))
    return np.real(np.sum(phase*weights*squared[None, :], axis=1))


def decompose_p0_error(exact_mean_square, projected_mean_square,
                       dof_mismatch_mean_square):
    """Split ||U_P0-u||^2 into mean-DOF error and unresolved projection error."""
    values = (exact_mean_square, projected_mean_square, dof_mismatch_mean_square)
    if any(not math.isfinite(v) for v in values):
        raise ValueError("energies must be finite")
    if exact_mean_square <= 0 or projected_mean_square < 0 or dof_mismatch_mean_square < 0:
        raise ValueError("invalid squared norms")
    scale = exact_mean_square
    projection_remainder = exact_mean_square-projected_mean_square
    if projection_remainder < -1e-12*scale:
        raise ValueError("cell-average projection norm exceeds exact norm")
    projection_remainder = max(0.0, projection_remainder)
    total_error = dof_mismatch_mean_square+projection_remainder
    return {
        "mean_dof_mismatch_relative_l2": math.sqrt(dof_mismatch_mean_square/exact_mean_square),
        "unresolved_projection_relative_l2": math.sqrt(projection_remainder/exact_mean_square),
        "p0_total_relative_l2": math.sqrt(total_error/exact_mean_square),
        "projection_energy_fraction": projected_mean_square/exact_mean_square,
        "orthogonality_identity_residual": (
            total_error-dof_mismatch_mean_square-projection_remainder),
    }
