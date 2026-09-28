"""Exact finite Fourier-shell energy for the high-gradient periodic MMS."""
import math

import numpy as np


_G = {
    0: 35/128,
    1: 7/32, -1: 7/32,
    2: 7/64, -2: 7/64,
    3: 1/32, -3: 1/32,
    4: 1/256, -4: 1/256,
}


def shell_spectrum(N=4, time=0.0):
    """Return shell energy from analytic complex velocity Fourier coefficients.

    The periodic cube has side 2*pi, hence integer wavevectors and unit shell
    width. Shell assignment matches ``tools.metrics.diagnostics``: nearest
    integer magnitude, with half-integer boundaries rounded upward.
    """
    if type(N) is not int or N < 1:
        raise ValueError("N must be a positive integer")
    if not math.isfinite(time):
        raise ValueError("time must be finite")
    decay2 = math.exp(-2*time)
    shell = {}
    # chi(y,z)=g(y)g(z). For each y/z mode pair, both +/-N x modes
    # have the same modal energy. Their sum cancels the 1/2 from sin/cos.
    for my, gy in _G.items():
        for mz, gz in _G.items():
            chi_mode2 = gy**2 * gz**2
            modal_pair_energy = decay2 * chi_mode2 * (
                my**2/(4*N**4) + 1/(4*N**2)
            )
            radius = math.sqrt(N**2 + my**2 + mz**2)
            index = math.floor(radius + 0.5)
            shell[index] = shell.get(index, 0.0) + modal_pair_energy
    last = max(shell)
    values = [shell.get(k, 0.0) for k in range(last+1)]
    return {
        "N": N,
        "time": time,
        "shell_width": 1.0,
        "shell_energy": values,
        "total_energy": math.fsum(values),
        "mode_count": 2*len(_G)**2,
        "method": "finite analytic Fourier coefficients; no sampled FFT reference",
    }


if __name__ == "__main__":
    import json
    print(json.dumps([shell_spectrum(n, .137) for n in (4, 8, 16)], indent=2))
