"""Derivative of the real trigonometric interpolant at periodic uniform samples."""
import numpy as np


def gradient(velocity, lengths=(2*np.pi,)*3):
    u = np.asarray(velocity, dtype=float)
    lengths = np.asarray(lengths, dtype=float)
    if u.ndim != 4 or u.shape[-1] != 3 or min(u.shape[:3]) < 4:
        raise ValueError('expected uniform (nx,ny,nz,3), dimensions >=4')
    if not np.isfinite(u).all() or lengths.shape != (3,) or not np.isfinite(lengths).all() or np.any(lengths <= 0):
        raise ValueError('finite field and positive domain lengths required')
    modes = np.fft.fftn(u, axes=(0,1,2))
    derivatives = []
    for j, n in enumerate(u.shape[:3]):
        wave = 2*np.pi*np.fft.fftfreq(n, d=lengths[j]/n)
        # The even-grid real Nyquist cosine has zero derivative at grid nodes.
        if n % 2 == 0:
            wave[n//2] = 0
        shape = [1]*4; shape[j] = n
        derivatives.append(np.fft.ifftn(1j*wave.reshape(shape)*modes, axes=(0,1,2)).real)
    return np.stack(derivatives, axis=-1)
