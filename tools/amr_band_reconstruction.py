"""Named trigonometric reconstruction and continuum derivative diagnostics.

All bounds concern the finite polynomial P_B v, never the original P0 field.
Analytical bounds are evaluated in floating point, without interval rounding.
"""
import numpy as np

from tools.amr_p0_spectrum import _modes


def validate(modes, coefficients):
    modes = _modes(modes)
    coefficients = np.asarray(coefficients, dtype=complex)
    if coefficients.shape != modes.shape or not np.isfinite(coefficients).all():
        raise ValueError('finite three-component coefficients required')
    lookup = {tuple(k): i for i, k in enumerate(modes)}
    if len(lookup) != len(modes):
        raise ValueError('duplicate modes')
    for i, k in enumerate(modes):
        j = lookup.get(tuple(-k))
        if j is None or np.max(np.abs(coefficients[i]-coefficients[j].conj())) > 2e-12:
            raise ValueError('real-field conjugate symmetry required')
    return modes, coefficients


def derivative_coefficients(modes, coefficients, kind):
    modes, coefficients = validate(modes, coefficients)
    if kind == 'gradient':
        return (1j*coefficients[:, :, None]*modes[:, None, :]).reshape(len(modes), 9)
    if kind == 'curl':
        return 1j*np.cross(modes, coefficients)
    if kind == 'divergence':
        return 1j*np.sum(modes*coefficients, axis=1)[:, None]
    raise ValueError('unknown derivative')


def sampled_peak_bounds(modes, coefficients, samples):
    """Grid lower bound and analytic Lipschitz upper bound for a vector norm.

    Grid spacing is 2*pi/samples; every torus point is at distance at most
    sqrt(3)*pi/samples from a grid point. Each coefficient contributes
    |k|*|a_k| to a global Lipschitz bound for the vector-valued polynomial.
    Coefficients may be flattened gradient tensors (Frobenius norm).
    """
    modes = _modes(modes); coefficients = np.asarray(coefficients, dtype=complex)
    if (type(samples) is not int or samples <= 2*np.max(np.abs(modes))
            or samples**3 > 2**22 or coefficients.ndim != 2
            or len(coefficients) != len(modes) or not np.isfinite(coefficients).all()):
        raise ValueError('resolved finite polynomial and bounded sampling grid required')
    if len({tuple(k) for k in modes}) != len(modes):
        raise ValueError('duplicate modes')
    residues = modes % samples
    squared = np.zeros((samples,)*3)
    maximum_imaginary = 0.
    for j in range(coefficients.shape[1]):
        transformed = np.zeros((samples,)*3, dtype=complex)
        transformed[residues[:, 0], residues[:, 1], residues[:, 2]] = coefficients[:, j]
        values = np.fft.ifftn(transformed)*samples**3
        maximum_imaginary = max(maximum_imaginary, float(np.max(np.abs(values.imag))))
        squared += values.real**2
    if maximum_imaginary > 2e-11*max(1., float(np.sum(np.abs(coefficients)))):
        raise ValueError('polynomial is not real on the evaluation grid')
    lower = float(np.sqrt(np.max(squared)))
    lipschitz = float(np.sum(np.linalg.norm(modes, axis=1)*np.linalg.norm(coefficients, axis=1)))
    radius = float(np.sqrt(3)*np.pi/samples)
    mean_square = float(squared.mean())
    parseval = float(np.sum(np.abs(coefficients)**2))
    if abs(mean_square-parseval) > 2e-12*max(parseval, 1e-300):
        raise ValueError('independent spatial grid mean differs from Parseval')
    return {'sample_count_per_axis': samples, 'sampled_peak_lower': lower,
            'analytic_peak_upper': lower+radius*lipschitz,
            'lipschitz_bound': lipschitz, 'covering_radius': radius,
            'grid_mean_square': mean_square, 'parseval_mean_square': parseval,
            'maximum_imaginary_residual': maximum_imaginary,
            'arithmetic_scope': 'Analytical enclosure formula evaluated in floating point; no interval-arithmetic certificate.'}


def diagnostics(modes, actual, reference, samples=64):
    modes, actual = validate(modes, actual)
    _, reference = validate(modes, reference)
    delta = actual-reference
    rows = {}
    for kind in ('gradient', 'curl'):
        error = derivative_coefficients(modes, delta, kind)
        exact = derivative_coefficients(modes, reference, kind)
        error_bounds = sampled_peak_bounds(modes, error, samples)
        reference_bounds = sampled_peak_bounds(modes, exact, samples)
        if reference_bounds['sampled_peak_lower'] <= 0:
            raise ValueError('nonzero reference derivative required')
        rows[kind] = {'relative_l2': float(np.linalg.norm(error)/np.linalg.norm(exact)),
                      'relative_peak_error_lower': error_bounds['sampled_peak_lower']/reference_bounds['analytic_peak_upper'],
                      'relative_peak_error_upper': error_bounds['analytic_peak_upper']/reference_bounds['sampled_peak_lower'],
                      'error': error_bounds, 'reference': reference_bounds}
    norm2 = np.sum(modes**2, axis=1)
    dot = np.sum(modes*actual, axis=1)
    longitudinal = np.zeros_like(actual)
    nonzero = norm2 > 0
    longitudinal[nonzero] = modes[nonzero]*dot[nonzero, None]/norm2[nonzero, None]
    corrected = actual-longitudinal
    rows['helmholtz'] = {
        'reference_maximum_divergence_coefficient': float(np.max(np.abs(np.sum(modes*reference, axis=1)))),
        'band_divergence_mean_square': float(np.sum(np.abs(dot)**2)),
        'longitudinal_mean_square': float(np.sum(np.abs(longitudinal)**2)),
        'longitudinal_relative_to_reference_l2': float(np.linalg.norm(longitudinal)/np.linalg.norm(reference)),
        'divergence_free_band_error_relative_l2': float(np.linalg.norm(corrected-reference)/np.linalg.norm(reference)),
        'orthogonal_error_identity_residual': float(np.sum(np.abs(delta)**2)-np.sum(np.abs(corrected-reference)**2)-np.sum(np.abs(longitudinal)**2)),
        'scope': 'Removing longitudinal modes gives the L2-nearest divergence-free polynomial in this band; this is not a CFD correction or evidence about omitted modes.'}
    return rows
