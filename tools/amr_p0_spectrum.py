"""Continuum Fourier coefficients of a declared dyadic-cube P0 velocity field."""
import math

import numpy as np

from tools.analyze_amr_mean_quality import verify_cube_coverage
from tools.compare_amr_resolution_volume_integrated import LENGTH, _cell_widths_and_validate


def _modes(modes):
    modes = np.asarray(modes)
    if (modes.ndim != 2 or modes.shape[1] != 3 or len(modes) == 0
            or modes.dtype.kind == 'b' or not np.isfinite(modes).all()
            or np.any(modes != np.rint(modes)) or np.any(np.abs(modes) > 2**20)):
        raise ValueError('finite bounded integer wavevectors required')
    return modes.astype(np.int64)


def voxel_fft(centers, volumes, velocity, n):
    """Repeat parent constants on finest voxels, preserving the P0 function."""
    if type(n) is not int or n < 2 or (2*n)**3 > 2**24:
        raise ValueError('valid base grid within the declared memory bound required')
    centers, volumes, velocity = map(np.asarray, (centers, volumes, velocity))
    widths = _cell_widths_and_validate(centers, volumes, n)
    coverage = verify_cube_coverage(centers, widths, n)
    if velocity.shape != (len(volumes), 3) or not np.isfinite(velocity).all():
        raise ValueError('finite cell velocity vectors required')
    m = 2*n; unit = LENGTH/m
    sizes = np.rint(widths/unit).astype(int)
    starts = np.rint((centers-widths[:, None]/2)/unit).astype(int)
    grid = np.empty((m, m, m, 3), dtype=float)
    for size in (1, 2):
        chosen = sizes == size; base = starts[chosen]; values = velocity[chosen]
        for dx in range(size):
            for dy in range(size):
                for dz in range(size):
                    p = base+np.array([dx, dy, dz])
                    grid[p[:, 0], p[:, 1], p[:, 2]] = values
    with np.errstate(over='raise', invalid='raise'):
        voxel_norm = float(np.mean(np.sum(grid**2, axis=-1)))
        cell_norm = float(np.sum(volumes*np.sum(velocity**2, axis=-1))/LENGTH**3)
    if abs(voxel_norm-cell_norm) > 2e-11*max(voxel_norm, cell_norm, 1e-300):
        raise ValueError('cell and voxel norms disagree')
    transformed = np.fft.fftn(grid, axes=(0, 1, 2))/m**3
    if not np.isfinite(transformed).all():
        raise ValueError('nonfinite Fourier transform')
    return transformed, {'m': m, 'coverage': coverage, 'voxel_mean_square': voxel_norm,
                         'cell_mean_square': cell_norm, 'cell_voxel_norm_difference': voxel_norm-cell_norm}


def fft_coefficients(transformed, modes):
    """Exact analytic voxel integral, including center phase and sinc window.

    FFT stores sums at voxel indices, not continuum Fourier coefficients.
    The correction is exp(-i*pi*sum(k)/m)*prod_j sinc(k_j/m).
    Integer modes beyond Nyquist are allowed via their FFT residue; no claim
    that a finite FFT contains the complete continuum spectrum is made.
    """
    modes = _modes(modes)
    m = transformed.shape[0]
    if transformed.shape != (m, m, m, 3):
        raise ValueError('cubic three-component Fourier array required')
    residues = modes % m
    sums = transformed[residues[:, 0], residues[:, 1], residues[:, 2]]
    window = np.exp(-1j*np.pi*np.sum(modes, axis=1)/m)*np.prod(np.sinc(modes/m), axis=1)
    return sums*window[:, None]


def direct_cube_coefficients(centers, widths, volumes, velocity, modes):
    """Independent direct sum of analytic cube integrals; no voxel FFT."""
    centers, widths, volumes, velocity = map(np.asarray, (centers, widths, volumes, velocity))
    modes = _modes(modes)
    if (centers.shape != (len(widths), 3) or velocity.shape != centers.shape
            or volumes.shape != widths.shape or not all(np.isfinite(a).all() for a in (centers, widths, volumes, velocity))
            or np.any(widths <= 0) or np.any(volumes <= 0)):
        raise ValueError('finite cube geometry and velocity required')
    result = []
    for k in modes:
        factor = volumes/LENGTH**3*np.exp(-1j*np.sum(centers*k, axis=1))
        factor *= np.prod(np.sinc(widths[:, None]*k/LENGTH), axis=1)
        result.append(np.sum(factor[:, None]*velocity, axis=0))
    return np.asarray(result)


def reference_coefficients(modes, frequency, time):
    """Binomial coefficients of cos(q/2)^8, independent of sampled reference."""
    modes = _modes(modes)
    if type(frequency) is not int or frequency < 1 or not math.isfinite(time):
        raise ValueError('positive integer MMS frequency and finite time required')
    result = np.zeros((len(modes), 3), dtype=complex)
    for i, (kx, ky, kz) in enumerate(modes):
        if abs(kx) != frequency or abs(ky) > 4 or abs(kz) > 4:
            continue
        coefficient = math.exp(-time)*math.comb(8, 4+int(ky))*math.comb(8, 4+int(kz))/256**2
        result[i, 0] = np.sign(kx)*ky*coefficient/(2*frequency**2)
        result[i, 1] = -coefficient/(2*frequency)
    return result


def spectrum(transformed, mean_square, frequency, time, cutoff=7):
    """Complete L2 split: coefficient mismatch inside cube plus exact outside mass."""
    m = transformed.shape[0]
    if type(cutoff) is not int or cutoff < max(4, frequency) or cutoff >= m//2:
        raise ValueError('cutoff must contain the MMS support and lie below voxel Nyquist')
    if not math.isfinite(mean_square) or mean_square < 0:
        raise ValueError('finite nonnegative P0 norm required')
    axis = np.arange(-cutoff, cutoff+1)
    modes = np.stack(np.meshgrid(axis, axis, axis, indexing='ij'), axis=-1).reshape(-1, 3)
    actual = fft_coefficients(transformed, modes)
    reference = reference_coefficients(modes, frequency, time)
    mode_norm = np.sum(np.abs(actual)**2, axis=1)
    ref_norm = np.sum(np.abs(reference)**2, axis=1)
    error_norm = np.sum(np.abs(actual-reference)**2, axis=1)
    band_norm, exact_norm, band_error = map(float, (mode_norm.sum(), ref_norm.sum(), error_norm.sum()))
    outside = mean_square-band_norm
    if outside < -2e-12*max(mean_square, exact_norm):
        raise ValueError('finite-band Fourier mass exceeds P0 norm')
    outside = max(0., outside)
    if exact_norm <= 0:
        raise ValueError('invalid continuum reference norm')
    shells = np.floor(np.linalg.norm(modes, axis=1)+.5).astype(int)
    rows = [{'shell': j, 'complete_integer_shell': j <= cutoff,
             'actual_mean_square_velocity': float(mode_norm[shells == j].sum()),
             'reference_mean_square_velocity': float(ref_norm[shells == j].sum()),
             'coefficient_error_mean_square': float(error_norm[shells == j].sum())}
            for j in range(int(shells.max())+1)]
    summary = {'cutoff_cube': cutoff, 'mode_count': len(modes), 'reference_mean_square': exact_norm,
               'actual_p0_mean_square': mean_square, 'inside_cube_mean_square': band_norm,
               'outside_cube_mean_square': outside, 'inside_cube_coefficient_error_mean_square': band_error,
               'outside_cube_fraction_of_actual_norm': outside/mean_square if mean_square > 0 else None,
               'inside_cube_error_relative_l2': math.sqrt(band_error/exact_norm),
               'outside_cube_norm_relative_to_reference': math.sqrt(outside/exact_norm),
               'p0_global_error_relative_l2': math.sqrt((band_error+outside)/exact_norm),
               'shells': rows,
               'normalization': '(2*pi)^-3 integral |velocity|^2; no kinetic-energy factor 1/2',
               'scope': 'Specified cube-constant velocity field. Analytic integral formulas evaluated in floating point; no interval certificate or numerical continuous-gradient bound.'}
    return summary, modes, actual, reference
