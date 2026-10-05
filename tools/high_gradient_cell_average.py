"""Analytic finite-volume averages for the periodic high-gradient MMS."""

import numpy as np


FREQUENCY = 4


def exact_cell_average_velocity(centers, width, time, frequency=FREQUENCY):
    """Return exact averages of the MMS velocity over axis-aligned cubes.

    ``centers`` has shape ``(n, 3)`` and ``width`` is either a scalar or one
    positive cube width per center. Periodic trigonometric modes are integrated
    using their exact sinc factors. The result is an average, not an integral.
    """
    centers = np.asarray(centers, dtype=float)
    if centers.ndim != 2 or centers.shape[1] != 3:
        raise ValueError("centers must have shape (n, 3)")
    if not np.isfinite(centers).all():
        raise ValueError("centers must be finite")
    if (not np.isfinite(time) or int(frequency) != frequency
            or frequency < 1):
        raise ValueError("time must be finite and frequency a positive integer")

    modes = np.array((1.0, 2.0, 3.0, 4.0))
    amplitudes = np.array((56.0, 28.0, 8.0, 1.0))
    x, y, z = centers.T
    try:
        widths = np.broadcast_to(np.asarray(width, dtype=float), x.shape)
    except ValueError as exc:
        raise ValueError("width must be scalar or have one value per center") from exc
    if not np.isfinite(widths).all() or np.any(widths <= 0):
        raise ValueError("cell widths must be finite and positive")

    sinc_modes = np.sinc(widths[:, None] * modes[None, :] / (2 * np.pi))
    average_g_y = (35.0 + np.sum(
        amplitudes * np.cos(y[:, None] * modes) * sinc_modes, axis=1
    )) / 128.0
    average_g_z = (35.0 + np.sum(
        amplitudes * np.cos(z[:, None] * modes) * sinc_modes, axis=1
    )) / 128.0
    average_g_prime_y = -np.sum(
        amplitudes * modes * np.sin(y[:, None] * modes) * sinc_modes, axis=1
    ) / 128.0
    x_scale = frequency * widths / (2 * np.pi)
    average_sin = np.sin(frequency * x) * np.sinc(x_scale)
    average_cos = np.cos(frequency * x) * np.sinc(x_scale)
    decay = np.exp(-time)
    return np.stack((
        decay * average_g_prime_y * average_g_z * average_sin / frequency**2,
        -decay * average_g_y * average_g_z * average_cos / frequency,
        np.zeros_like(x),
    ), axis=1)
