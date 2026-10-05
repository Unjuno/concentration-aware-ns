"""Exploratory local interval enclosure for a frozen PhysicsNeMo MLP.

Uses mpmath.iv arithmetic to bound the spatial derivative error over one
coordinate box. This is a feasibility probe, not a formal certificate: the
library's directed-rounding implementation has not been independently
validated for proof use, and no cover of the full periodic domain is built.
"""
import math

from mpmath import iv


def _tanh_interval(value):
    """Monotone tanh hull, evaluated at outward interval endpoints."""
    at_lower = (1 - iv.exp(-2 * value.a)) / (1 + iv.exp(-2 * value.a))
    at_upper = (1 - iv.exp(-2 * value.b)) / (1 + iv.exp(-2 * value.b))
    return iv.mpf([at_lower.a, at_upper.b])


def _reference_gradient_u0(box, sigma):
    d = [coordinate - iv.pi for coordinate in box]
    beta = iv.mpf(1) / (sigma * sigma)
    q = [-iv.sin(value) * beta for value in d]
    psi = iv.exp(sum((iv.cos(value) - 1) * beta for value in d))
    a = (1, 2, 3)
    # u0 = grad(psi) x a, so D_j u0 = D_j grad(psi) x a.
    hessian_psi = [[
        psi * (q[i] * q[j] - (iv.cos(d[j]) * beta if i == j else 0))
        for j in range(3)
    ] for i in range(3)]
    velocity_jacobian = [[
        hessian_psi[1][j] * a[2] - hessian_psi[2][j] * a[1],
        hessian_psi[2][j] * a[0] - hessian_psi[0][j] * a[2],
        hessian_psi[0][j] * a[1] - hessian_psi[1][j] * a[0],
    ] for j in range(3)]
    return velocity_jacobian


def gradient_error_enclosure(hidden_layers, output_layer, box, *, time, sigma, endpoint=0.05, dps=50):
    """Enclose each entry of grad(u_pred-u_ref) over a spatial box.

    `hidden_layers` is a sequence of `(weights, biases)` row-major affine
    tanh layers. `output_layer` is `(weights, biases)` for a linear map whose
    first three outputs are velocity corrections. Input order matches the
    frozen harness: sin(x), sin(y), sin(z), cos(x), cos(y), cos(z), t/end.
    The returned object is a 3x3 matrix of mpmath intervals.
    """
    if len(hidden_layers) != 3:
        raise ValueError("the frozen model must have three hidden layers")
    if len(box) != 3:
        raise ValueError("box must contain three coordinate intervals")
    if (not math.isfinite(time) or not math.isfinite(sigma) or not math.isfinite(endpoint)
            or sigma <= 0 or endpoint <= 0 or time < 0 or time > endpoint):
        raise ValueError("time must lie in a finite positive endpoint and sigma must be positive")
    endpoints_by_axis = []
    for endpoints in box:
        if len(endpoints) != 2 or not all(math.isfinite(x) for x in endpoints):
            raise ValueError("each box coordinate needs two finite endpoints")
        if endpoints[0] > endpoints[1]:
            raise ValueError("box interval endpoints must be ordered")
        endpoints_by_axis.append(endpoints)

    previous_dps = iv.dps
    iv.dps = dps
    try:
        intervals = [iv.mpf([lo, hi]) for lo, hi in endpoints_by_axis]
        sine = [iv.sin(x) for x in intervals]
        cosine = [iv.cos(x) for x in intervals]
        features = sine + cosine + [iv.mpf(time) / iv.mpf(endpoint)]
        derivatives = [[iv.mpf(0) for _ in range(3)] for _ in range(7)]
        for axis in range(3):
            derivatives[axis][axis] = cosine[axis]
            derivatives[axis + 3][axis] = -sine[axis]

        for weights, biases in hidden_layers:
            if len(weights) != len(biases) or any(len(row) != len(features) for row in weights):
                raise ValueError("incompatible affine layer dimensions")
            preactivation = []
            preactivation_derivative = []
            for row, bias in zip(weights, biases):
                preactivation.append(
                    sum((iv.mpf(float(weight)) * value for weight, value in zip(row, features)), iv.mpf(float(bias)))
                )
                preactivation_derivative.append([
                    sum((iv.mpf(float(weight)) * derivatives[j][axis] for j, weight in enumerate(row)), iv.mpf(0))
                    for axis in range(3)
                ])
            activations = [_tanh_interval(value) for value in preactivation]
            derivatives = [
                [(1 - activations[i] * activations[i]) * preactivation_derivative[i][axis]
                 for axis in range(3)]
                for i in range(len(activations))
            ]
            features = activations

        output_weights, output_biases = output_layer
        if len(output_weights) < 3 or len(output_biases) < 3:
            raise ValueError("output layer must provide three velocity components")
        mlp_gradient = [[
            sum((iv.mpf(float(weight)) * derivatives[j][axis]
                 for j, weight in enumerate(output_weights[component])), iv.mpf(0))
            for axis in range(3)] for component in range(3)
        ]
        reference_gradient = _reference_gradient_u0(intervals, iv.mpf(sigma))
        t = iv.mpf(time)
        reference_factor = 1 - iv.exp(-t)
        return [[
            t * mlp_gradient[i][j] + reference_factor * reference_gradient[j][i]
            for j in range(3)] for i in range(3)
        ]
    finally:
        iv.dps = previous_dps
