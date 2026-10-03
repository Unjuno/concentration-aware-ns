"""Conditional gradient obstruction for C1 fields interpolating native points.

For e=w-u, the segment fundamental theorem gives
||grad e||_infinity,F >= ||e(b)-e(a)||_2 / ||b-a||_2.
No cell-average interpretation or curl conclusion is used.
"""
import numpy as np
from flint import arb, fmpq
from scipy.spatial import cKDTree

from tools.amr_arb_mean_certificate import endpoints, reference_bounds
from tools.high_gradient_reference import fields


def exact_float(value):
    numerator, denominator = float(value).as_integer_ratio()
    return arb(fmpq(numerator, denominator))


def square(value):
    return value * value


def point_reference(point, time, frequency=3):
    x, y, z = map(exact_float, point)
    def envelope(q):
        c = (q / 2).cos(); s = (q / 2).sin()
        c2 = c * c; c4 = c2 * c2
        return c4 * c4, -4 * c4 * c2 * c * s
    g, dg = envelope(y); h, _ = envelope(z)
    decay = (-arb(time)).exp()
    return (decay * dg * h * (frequency*x).sin() / frequency**2,
            -decay * g * h * (frequency*x).cos() / frequency, arb(0))


def chord_certificate(a, b, ua, ub, time='0.05', frequency=3):
    a, b, ua, ub = (np.asarray(v, dtype=float) for v in (a, b, ua, ub))
    if any(v.shape != (3,) or not np.isfinite(v).all() for v in (a, b, ua, ub)):
        raise ValueError('finite three-component point data required')
    if np.array_equal(a, b):
        raise ValueError('distinct points required')
    ra, rb = point_reference(a, time, frequency), point_reference(b, time, frequency)
    difference = [(exact_float(ub[j])-rb[j])-(exact_float(ua[j])-ra[j]) for j in range(3)]
    numerator = sum((square(x) for x in difference), arb(0)).sqrt()
    distance = sum((square(exact_float(b[j])-exact_float(a[j])) for j in range(3)), arb(0)).sqrt()
    if not numerator > 0 or not distance > 0:
        raise ValueError('strictly positive enclosed chord error and distance required')
    absolute = (numerator.lower()/distance.upper()).lower()
    _, reference_peak, _ = reference_bounds(time, frequency)
    relative = (absolute/reference_peak.upper()).lower()
    return {'a':a.tolist(), 'b':b.tolist(), 'Ua':ua.tolist(), 'Ub':ub.tolist(),
            'error_chord_norm':endpoints(numerator), 'point_distance':endpoints(distance),
            'gradient_absolute_peak_error_lower':endpoints(absolute),
            'reference_gradient_peak_upper':endpoints(reference_peak),
            'gradient_relative_peak_error_lower':endpoints(relative),
            'above_disclosed_five_percent_target':bool(relative > arb(1)/20)}


def select_witness(centers, values, time='0.05', frequency=3):
    centers, values = np.asarray(centers), np.asarray(values)
    if (centers.ndim != 2 or centers.shape[1] != 3 or centers.shape != values.shape
            or len(centers)<7 or not np.isfinite(centers).all() or not np.isfinite(values).all()):
        raise ValueError('complete finite point vectors required')
    errors = values-fields(centers, N=frequency, time=float(time))['u']
    distances, neighbors = cKDTree(centers).query(centers, k=7)
    if np.any(distances[:, 1:]<=0):
        raise ValueError('duplicate points')
    slopes=np.linalg.norm(errors[:,None,:]-errors[neighbors[:,1:]], axis=2)/distances[:,1:]
    row, column=np.unravel_index(np.argmax(slopes), slopes.shape)
    other=int(neighbors[row,column+1])
    # Floating search only selects a witness; its certificate uses exact decoded data.
    result=chord_certificate(centers[row], centers[other], values[row], values[other], time, frequency)
    result.update(cell_rows=[int(row),other], floating_search_slope=float(slopes[row,column]),
                  search_scope='six nearest neighbors per point, no periodic wrapping; not a global maximum claim')
    return result
