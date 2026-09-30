"""Exact-rational global Hessian envelope for the frozen PhysicsNeMo MLP.

This is a deliberately coarse global bound used to assess whether a uniform
Lipschitz-cover certificate for continuous derivative peaks is computationally
plausible. It is not an accuracy verdict or a PhysicsNeMo acceptance gate.
"""
from fractions import Fraction
from math import ceil


def _exact_abs(value):
    if isinstance(value, Fraction):
        return abs(value)
    # Fraction.from_float preserves the exact stored binary floating-point value.
    return abs(Fraction.from_float(float(value)))


def network_hessian_entry_bound(hidden_weights, output_weights, *, time_factor=Fraction(1, 20)):
    """Bound every spatial Hessian entry of time_factor*MLP(sin,cos,t/end).

    Hidden layers use tanh; the output layer is linear. Inputs follow the
    frozen training code: sin(x), sin(y), sin(z), cos(x), cos(y), cos(z), t/end.
    The final coordinate is fixed in space. The bound uses |tanh'|<=1 and
    |tanh''|<=1.
    """
    if len(hidden_weights) != 3:
        raise ValueError("the frozen architecture has exactly three hidden layers")
    if len(hidden_weights[0]) == 0 or len(hidden_weights[0][0]) != 7:
        # Matrices are row-major (out_features, in_features).
        raise ValueError("first hidden matrix must have seven input features")

    d1 = [[Fraction(0) for _ in range(3)] for _ in range(7)]
    d2 = [[Fraction(0) for _ in range(9)] for _ in range(7)]
    for axis in range(3):
        for feature in (axis, axis + 3):
            d1[feature][axis] = Fraction(1)
            d2[feature][3 * axis + axis] = Fraction(1)

    for matrix in hidden_weights:
        abs_w = [[_exact_abs(v) for v in row] for row in matrix]
        if any(len(row) != len(d1) for row in abs_w):
            raise ValueError("incompatible hidden-layer matrix dimensions")
        pre_d1 = [
            [sum((row[j] * d1[j][axis] for j in range(len(row))), Fraction(0))
             for axis in range(3)]
            for row in abs_w
        ]
        pre_d2 = [
            [sum((row[j] * d2[j][ij] for j in range(len(row))), Fraction(0))
             + pre_d1[i][ij // 3] * pre_d1[i][ij % 3]
             for ij in range(9)]
            for i, row in enumerate(abs_w)
        ]
        d1, d2 = pre_d1, pre_d2

    abs_out = [[_exact_abs(v) for v in row] for row in output_weights]
    if len(abs_out) < 3 or any(len(row) != len(d2) for row in abs_out[:3]):
        raise ValueError("output matrix must provide three compatible velocity rows")
    output_hessians = [
        [sum((row[j] * d2[j][ij] for j in range(len(row))), Fraction(0))
         * time_factor for ij in range(9)]
        for row in abs_out[:3]
    ]
    return max(max(row) for row in output_hessians)


def total_error_hessian_entry_bound(network_bound):
    """Bound the endpoint error Hessian using 1-exp(-t) <= t = 1/20."""
    return Fraction(29) + network_bound


def best_case_uniform_grid_nodes(error_hessian_bound, *, tolerance=Fraction(1, 20)):
    """Optimistic lower bound on per-axis nodes for this gradient-cover bound.

    On a periodic 2pi cube, nearest-grid coordinate distance is pi/N. If every
    Hessian entry of the derivative-error field is bounded by B, its Frobenius
    gradient norm can change by at most 9*pi*B/N between a point and its nearest
    grid node. For a lower floor on N, use pi>3 and a rational upper bound 21
    on the exact reference peak, granting the most generous (largest)
    threshold. With zero sampled-grid error this gives a lower bound on nodes
    required by this particular Hessian envelope; nonzero grid error can only
    increase the count.
    """
    if error_hessian_bound < 0 or tolerance <= 0:
        raise ValueError("bounds and tolerance must be positive")
    budget = tolerance * 21
    required = Fraction(27) * error_hessian_bound / budget
    # pi>3 and peak<21 make the actual requirement strictly greater than this
    # rational, so use floor+1 even when the quotient is an integer.
    return required.numerator // required.denominator + 1
