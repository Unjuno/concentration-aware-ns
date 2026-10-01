import numpy as np

from tools.high_gradient_reference import fields
from tools.audit_openfoam_gradient_reconstruction import fd2_symbol_gain
from tools.spectral_derivative import gradient


def _curl(grad):
    return np.stack((grad[..., 2, 1] - grad[..., 1, 2],
                     grad[..., 0, 2] - grad[..., 2, 0],
                     grad[..., 1, 0] - grad[..., 0, 1]), axis=-1)


def test_spectral_derivatives_reconstruct_resolved_high_gradient_mms():
    n, frequency, end = 16, 4, 0.05
    axis = (np.arange(n) + 0.5) * 2 * np.pi / n
    z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
    points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
    reference = fields(points, N=frequency, nu=0.01, time=end)
    velocity = reference["u"].reshape(n, n, n, 3).transpose(2, 1, 0, 3)
    exact_gradient = reference["grad_u"].reshape(n, n, n, 3, 3).transpose(2, 1, 0, 3, 4)
    exact_vorticity = reference["vorticity"].reshape(n, n, n, 3).transpose(2, 1, 0, 3)

    reconstructed_gradient = gradient(velocity)
    np.testing.assert_allclose(reconstructed_gradient, exact_gradient, rtol=0, atol=2e-13)
    np.testing.assert_allclose(_curl(reconstructed_gradient), exact_vorticity, rtol=0, atol=2e-13)


def test_centered_fd2_fourier_symbol_matches_exact_single_mode_attenuation():
    wavenumber, length = 4, 2 * np.pi
    for n in (16, 32, 64, 128):
        spacing = length / n
        x = (np.arange(n) + 0.5) * spacing
        velocity = np.sin(wavenumber * x)
        fd2 = (np.roll(velocity, -1) - np.roll(velocity, 1)) / (2 * spacing)
        exact_derivative = wavenumber * np.cos(wavenumber * x)
        gain = fd2_symbol_gain(wavenumber, n, length)
        np.testing.assert_allclose(fd2, gain * exact_derivative, rtol=2e-14, atol=2e-14)
    assert fd2_symbol_gain(wavenumber, 128, length) > fd2_symbol_gain(wavenumber, 64, length)
    assert fd2_symbol_gain(wavenumber, 64, length) > fd2_symbol_gain(wavenumber, 32, length)
