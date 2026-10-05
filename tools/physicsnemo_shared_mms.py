"""Torch representation of the shared localized periodic high-gradient MMS."""


def velocity_torch(points, time, frequency=4):
    """Evaluate the exact MMS velocity with native Torch differentiation.

    ``points`` has shape ``(..., 3)`` and ``time`` is scalar or broadcastable
    over ``points.shape[:-1]``. The analytic NumPy reference remains the
    independent source for force and validation values.
    """
    import torch

    if not torch.is_tensor(points) or points.ndim == 0 or points.shape[-1] != 3:
        raise ValueError("points must be a Torch tensor with final dimension 3")
    if (not isinstance(frequency, int) or isinstance(frequency, bool)
            or frequency < 1):
        raise ValueError("frequency must be a positive integer")
    if not torch.isfinite(points).all():
        raise ValueError("points must be finite")

    if torch.is_tensor(time):
        t = time.to(dtype=points.dtype, device=points.device)
    else:
        t = points.new_tensor(time)
    if t.ndim == points.ndim - 1 and tuple(t.shape) == tuple(points.shape[:-1]):
        t = t.unsqueeze(-1)
    try:
        torch.broadcast_shapes(tuple(t.shape), tuple(points.shape[:-1]) + (1,))
    except RuntimeError as error:
        raise ValueError("time must be scalar or broadcastable over points") from error
    if not torch.isfinite(t).all():
        raise ValueError("time must be finite")

    x, y, z = points.unbind(dim=-1)
    half_cos_y = (1 + torch.cos(y)) / 2
    half_cos_z = (1 + torch.cos(z)) / 2
    envelope_y = half_cos_y.pow(4)
    envelope_z = half_cos_z.pow(4)
    derivative_y = -2 * half_cos_y.pow(3) * torch.sin(y)
    chi = envelope_y * envelope_z
    chi_y = derivative_y * envelope_z
    decay = torch.exp(-t.squeeze(-1) if t.ndim == points.ndim else -t)
    n = float(frequency)
    return decay.unsqueeze(-1) * torch.stack((
        chi_y * torch.sin(n * x) / n**2,
        -chi * torch.cos(n * x) / n,
        torch.zeros_like(x),
    ), dim=-1)
