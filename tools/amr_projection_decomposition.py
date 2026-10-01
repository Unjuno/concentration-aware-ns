"""L2-orthogonal decomposition for an explicit piecewise-constant field."""
import math
from fractions import Fraction


def exact_mms_mean_square_velocity(time, frequency=4):
    """Parseval mean of |u|^2 for the localized cosine-envelope MMS."""
    if not math.isfinite(time) or type(frequency) is not int or frequency < 1:
        raise ValueError("finite time and positive integer frequency required")
    a = Fraction(6435, 32768)  # mean of g(q)^2
    b = Fraction(429, 2048)   # mean of g'(q)^2
    return math.exp(-2*time)*(
        float(b*a)/(2*frequency**4)+float(a*a)/(2*frequency**2))


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
