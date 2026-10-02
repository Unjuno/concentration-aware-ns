"""Experimental Arb enclosures for the frozen PhysicsNeMo velocity Jacobian.

The direct form uses ball arithmetic for the frozen three-layer tanh network
and analytic manufactured reference. The centered form applies the mean-value
theorem to the error Jacobian using an interval Hessian over the box. This is a
research probe, not yet a domain-wide benchmark certificate.
"""
import math

from flint import arb, ctx


_A = (arb(1), arb(2), arb(3))
_UNIT_INTERVAL = arb(-1).union(1)
_TANH_FIRST_DERIVATIVE_RANGE = arb(0).union(1)
_TANH_SECOND_DERIVATIVE_RANGE = arb(-0.8).union(0.8)
_TANH_THIRD_DERIVATIVE_RANGE = arb(-2).union(2)


def _unit_range(value):
    """Intersect a rigorous ball with the analytic range [-1, 1]."""
    return value.intersection(_UNIT_INTERVAL)


def _tanh_first_derivative_range(value):
    return value.intersection(_TANH_FIRST_DERIVATIVE_RANGE)


def _tanh_second_derivative_range(value):
    return value.intersection(_TANH_SECOND_DERIVATIVE_RANGE)


def _monotone_tanh_range(value):
    """Enclose tanh over a real ball by evaluating its monotone endpoints."""
    endpoint_hull = value.lower().tanh().union(value.upper().tanh())
    return _unit_range(endpoint_hull)


def _validate(hidden_layers, output_layer, box, time, sigma, endpoint):
    if len(hidden_layers) != 3:
        raise ValueError("the frozen model must have three hidden layers")
    if len(box) != 3:
        raise ValueError("box must contain three coordinate intervals")
    if (not all(math.isfinite(v) for v in (time, sigma, endpoint))
            or time < 0 or sigma <= 0 or endpoint <= 0 or time > endpoint):
        raise ValueError("time must lie in [0, endpoint], with positive finite sigma/endpoint")
    bounds = []
    for axis in box:
        if len(axis) != 2 or not all(math.isfinite(v) for v in axis):
            raise ValueError("each box coordinate needs two finite endpoints")
        lo, hi = axis
        if lo > hi:
            raise ValueError("box interval endpoints must be ordered")
        bounds.append((float(lo), float(hi)))
    features = 7
    for weights, biases in hidden_layers:
        if len(weights) != len(biases) or any(len(row) != features for row in weights):
            raise ValueError("incompatible affine layer dimensions")
        if not weights:
            raise ValueError("hidden layers must be nonempty")
        features = len(weights)
    output_weights, output_biases = output_layer
    if len(output_weights) < 3 or len(output_biases) < 3:
        raise ValueError("output layer must provide three velocity components")
    if any(len(row) != features for row in output_weights[:3]):
        raise ValueError("output layer dimensions do not match final hidden layer")
    return bounds


def _affine(weights, features, biases):
    return [
        sum((arb(float(weight)) * feature for weight, feature in zip(row, features)), arb(float(bias)))
        for row, bias in zip(weights, biases)
    ]


def _network_jet(hidden_layers, output_layer, box, time, endpoint, *, include_third=False):
    """Return value, gradient, Hessian enclosures of three network outputs."""
    sine_cosine = [tuple(_unit_range(value) for value in coordinate.sin_cos())
                   for coordinate in box]
    sine = [pair[0] for pair in sine_cosine]
    cosine = [pair[1] for pair in sine_cosine]
    features = sine + cosine + [arb(time) / arb(endpoint)]
    zero = arb(0)
    gradient = [[zero for _ in range(3)] for _ in range(7)]
    hessian = [[[zero for _ in range(3)] for _ in range(3)] for _ in range(7)]
    third = ([[[[zero for _ in range(3)] for _ in range(3)] for _ in range(3)]
              for _ in range(7)] if include_third else None)
    for axis in range(3):
        gradient[axis][axis] = cosine[axis]
        gradient[axis + 3][axis] = -sine[axis]
        hessian[axis][axis][axis] = -sine[axis]
        hessian[axis + 3][axis][axis] = -cosine[axis]
        if include_third:
            third[axis][axis][axis][axis] = -cosine[axis]
            third[axis + 3][axis][axis][axis] = sine[axis]

    for weights, biases in hidden_layers:
        preactivation = _affine(weights, features, biases)
        pre_gradient = [
            [sum((arb(float(w)) * gradient[j][axis] for j, w in enumerate(row)), zero)
             for axis in range(3)]
            for row in weights
        ]
        pre_hessian = [
            [[sum((arb(float(w)) * hessian[j][a][b] for j, w in enumerate(row)), zero)
              for b in range(3)] for a in range(3)]
            for row in weights
        ]
        if include_third:
            pre_third = [[[[sum((arb(float(w)) * third[j][a][b][c]
                                 for j, w in enumerate(row)), zero)
                            for c in range(3)] for b in range(3)] for a in range(3)]
                         for row in weights]
        features = [_monotone_tanh_range(value) for value in preactivation]
        gradient = []
        hessian = []
        if include_third:
            next_third = []
        for neuron, activation in enumerate(features):
            first = _tanh_first_derivative_range(1 - activation * activation)
            second = _tanh_second_derivative_range(-2 * activation * first)
            third_factor = (-2 * first * first + 4 * activation * activation * first)
            third_factor = third_factor.intersection(_TANH_THIRD_DERIVATIVE_RANGE)
            gradient.append([first * pre_gradient[neuron][axis] for axis in range(3)])
            hessian.append([
                [second * pre_gradient[neuron][a] * pre_gradient[neuron][b]
                 + first * pre_hessian[neuron][a][b]
                 for b in range(3)]
                for a in range(3)
            ])
            if include_third:
                next_third.append([[[
                    third_factor * pre_gradient[neuron][a] * pre_gradient[neuron][b]
                    * pre_gradient[neuron][c]
                    + second * (pre_hessian[neuron][a][b] * pre_gradient[neuron][c]
                                + pre_hessian[neuron][a][c] * pre_gradient[neuron][b]
                                + pre_hessian[neuron][b][c] * pre_gradient[neuron][a])
                    + first * pre_third[neuron][a][b][c]
                    for c in range(3)] for b in range(3)] for a in range(3)])
        if include_third:
            third = next_third

    output_weights, output_biases = output_layer
    values = _affine(output_weights[:3], features, output_biases[:3])
    out_gradient = [[
        sum((arb(float(w)) * gradient[j][axis]
             for j, w in enumerate(output_weights[component])), zero)
        for axis in range(3)
    ] for component in range(3)]
    out_hessian = [[[sum((arb(float(w)) * hessian[j][a][b]
                          for j, w in enumerate(output_weights[component])), zero)
                     for b in range(3)] for a in range(3)] for component in range(3)]
    if not include_third:
        return values, out_gradient, out_hessian
    out_third = [[[[sum((arb(float(w)) * third[j][a][b][c]
                         for j, w in enumerate(output_weights[component])), zero)
                    for c in range(3)] for b in range(3)] for a in range(3)]
                  for component in range(3)]
    return values, out_gradient, out_hessian, out_third


def _reference_jet(box, sigma, *, include_fourth=False):
    d = [coordinate - arb.pi() for coordinate in box]
    beta = 1 / (arb(sigma) * arb(sigma))
    q = [-value.sin() * beta for value in d]
    r = [-value.cos() * beta for value in d]
    s = [value.sin() * beta for value in d]
    psi = sum(((value.cos() - 1) * beta for value in d), arb(0)).exp()
    hessian_psi = [[psi * (q[i] * q[j] + (r[i] if i == j else 0))
                    for j in range(3)] for i in range(3)]
    third_psi = [[[
        psi * (q[i] * q[j] * q[k]
               + (r[i] * q[k] if i == j else 0)
               + (r[i] * q[j] if i == k else 0)
               + (r[j] * q[i] if j == k else 0)
               + (s[i] if i == j == k else 0))
        for k in range(3)] for j in range(3)] for i in range(3)]
    if include_fourth:
        fourth_psi = [[[[
            psi * (
                q[i] * q[j] * q[k] * q[l]
                + (r[i] * q[k] * q[l] if i == j else 0)
                + (r[i] * q[j] * q[l] if i == k else 0)
                + (r[i] * q[j] * q[k] if i == l else 0)
                + (r[j] * q[i] * q[l] if j == k else 0)
                + (r[j] * q[i] * q[k] if j == l else 0)
                + (r[k] * q[i] * q[j] if k == l else 0)
                + (r[i] * r[k] if i == j and k == l else 0)
                + (r[i] * r[j] if i == k and j == l else 0)
                + (r[i] * r[j] if i == l and j == k else 0)
                + (s[i] * q[l] if i == j == k else 0)
                + (s[i] * q[k] if i == j == l else 0)
                + (s[i] * q[j] if i == k == l else 0)
                + (s[j] * q[i] if j == k == l else 0)
                + (beta * d[i].cos() if i == j == k == l else 0)
            )
            for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)]
    velocity_gradient = [[
        hessian_psi[1][axis] * _A[2] - hessian_psi[2][axis] * _A[1],
        hessian_psi[2][axis] * _A[0] - hessian_psi[0][axis] * _A[2],
        hessian_psi[0][axis] * _A[1] - hessian_psi[1][axis] * _A[0],
    ] for axis in range(3)]
    velocity_hessian = [[[ 
        third_psi[1][axis][other] * _A[2] - third_psi[2][axis][other] * _A[1],
        third_psi[2][axis][other] * _A[0] - third_psi[0][axis][other] * _A[2],
        third_psi[0][axis][other] * _A[1] - third_psi[1][axis][other] * _A[0],
    ] for other in range(3)] for axis in range(3)]
    # Return derivatives in grad_u[component][axis] convention.
    grad = [[velocity_gradient[axis][component] for axis in range(3)] for component in range(3)]
    hess = [[[velocity_hessian[a][b][component] for b in range(3)]
             for a in range(3)] for component in range(3)]
    if not include_fourth:
        return grad, hess
    velocity_third = []
    for component in range(3):
        component_jet = []
        for a in range(3):
            axis_jet = []
            for b in range(3):
                row = []
                for c in range(3):
                    cross = (
                        fourth_psi[a][b][c][1] * _A[2] - fourth_psi[a][b][c][2] * _A[1],
                        fourth_psi[a][b][c][2] * _A[0] - fourth_psi[a][b][c][0] * _A[2],
                        fourth_psi[a][b][c][0] * _A[1] - fourth_psi[a][b][c][1] * _A[0],
                    )
                    row.append(cross[component])
                axis_jet.append(row)
            component_jet.append(axis_jet)
        velocity_third.append(component_jet)
    return grad, hess, velocity_third


def _error_jet(hidden_layers, output_layer, box, *, time, sigma, endpoint,
               include_third=False):
    network_jet = _network_jet(hidden_layers, output_layer, box, time, endpoint,
                               include_third=include_third)
    _, network_gradient, network_hessian = network_jet[:3]
    reference_jet = _reference_jet(box, sigma, include_fourth=include_third)
    reference_gradient, reference_hessian = reference_jet[:2]
    t = arb(time)
    reference_factor = 1 - (-t).exp()
    error_gradient = [[
        t * network_gradient[i][j] + reference_factor * reference_gradient[i][j]
        for j in range(3)
    ] for i in range(3)]
    error_hessian = [[[
        t * network_hessian[i][j][k] + reference_factor * reference_hessian[i][j][k]
        for k in range(3)
    ] for j in range(3)] for i in range(3)]
    if not include_third:
        return error_gradient, error_hessian
    network_third = network_jet[3]
    reference_third = reference_jet[2]
    error_third = [[[[(
        t * network_third[i][j][k][l]
        + reference_factor * reference_third[i][j][k][l]
    ) for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)]
    return error_gradient, error_hessian, error_third


def gradient_error_enclosure(hidden_layers, output_layer, box, *, time, sigma, endpoint=0.05, dps=50):
    """Direct ball enclosure of each spatial Jacobian-error component."""
    bounds = _validate(hidden_layers, output_layer, box, time, sigma, endpoint)
    old_prec = ctx.prec
    ctx.dps = dps
    try:
        intervals = [arb(lo).union(hi) for lo, hi in bounds]
        gradient, _ = _error_jet(hidden_layers, output_layer, intervals,
                                 time=time, sigma=sigma, endpoint=endpoint)
        return gradient
    finally:
        ctx.prec = old_prec


def centered_gradient_error_enclosure(hidden_layers, output_layer, box, *, time, sigma,
                                      endpoint=0.05, dps=50):
    """Mean-value enclosure: center Jacobian plus local Hessian times radii."""
    bounds = _validate(hidden_layers, output_layer, box, time, sigma, endpoint)
    old_prec = ctx.prec
    ctx.dps = dps
    try:
        intervals = [arb(lo).union(hi) for lo, hi in bounds]
        centers = [(lo + hi) / 2 for lo, hi in bounds]
        center_points = [arb(center) for center in centers]
        center_gradient, _ = _error_jet(
            hidden_layers, output_layer, center_points,
            time=time, sigma=sigma, endpoint=endpoint,
        )
        _, box_hessian = _error_jet(
            hidden_layers, output_layer, intervals,
            time=time, sigma=sigma, endpoint=endpoint,
        )
        delta_bounds = [(interval - center).abs_upper()
                        for interval, center in zip(intervals, center_points)]
        result = []
        for i in range(3):
            row = []
            for j in range(3):
                radius = sum((box_hessian[i][j][k].abs_upper() * delta_bounds[k]
                              for k in range(3)), arb(0))
                row.append(center_gradient[i][j] + arb(0, radius))
            result.append(row)
        return result
    finally:
        ctx.prec = old_prec


def quadratic_taylor_gradient_error_enclosure(
    hidden_layers, output_layer, box, *, time, sigma, endpoint=0.05, dps=50
):
    """Second-order Taylor enclosure with interval third-derivative remainder."""
    bounds = _validate(hidden_layers, output_layer, box, time, sigma, endpoint)
    old_prec = ctx.prec
    ctx.dps = dps
    try:
        intervals = [arb(lo).union(hi) for lo, hi in bounds]
        centers = [(lo + hi) / 2 for lo, hi in bounds]
        center_points = [arb(center) for center in centers]
        center_gradient, center_hessian = _error_jet(
            hidden_layers, output_layer, center_points,
            time=time, sigma=sigma, endpoint=endpoint,
        )
        _, _, box_third = _error_jet(
            hidden_layers, output_layer, intervals,
            time=time, sigma=sigma, endpoint=endpoint, include_third=True,
        )
        radii = [(interval - center).abs_upper()
                 for interval, center in zip(intervals, center_points)]
        result = []
        for i in range(3):
            row = []
            for j in range(3):
                linear_radius = sum((center_hessian[i][j][k].abs_upper() * radii[k]
                                     for k in range(3)), arb(0))
                quadratic_radius = sum((box_third[i][j][k][l].abs_upper()
                                        * radii[k] * radii[l]
                                        for k in range(3) for l in range(3)), arb(0)) / 2
                row.append(center_gradient[i][j] + arb(0, linear_radius + quadratic_radius))
            result.append(row)
        return result
    finally:
        ctx.prec = old_prec
