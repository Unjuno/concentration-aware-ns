import numpy as np
import pytest

from tools.high_gradient_reference import fields


def _torch():
    return pytest.importorskip("torch")


def test_torch_velocity_matches_shared_analytic_mms_values_and_gradient():
    torch = _torch()
    from tools.physicsnemo_shared_mms import velocity_torch

    points_np = np.array([
        [0.17, 0.43, 1.29],
        [2.11, 3.07, 4.91],
        [5.72, 2.83, 0.64],
    ])
    time = 0.023
    points = torch.tensor(points_np, dtype=torch.float64, requires_grad=True)
    actual = velocity_torch(points, time, frequency=4)
    actual_gradient = torch.stack([
        torch.autograd.grad(actual[:, i].sum(), points, retain_graph=True)[0]
        for i in range(3)
    ], dim=1)
    reference = fields(points_np, N=4, time=time)

    np.testing.assert_allclose(actual.detach().numpy(), reference["u"], rtol=2e-14, atol=2e-14)
    np.testing.assert_allclose(
        actual_gradient.detach().numpy(), reference["grad_u"], rtol=2e-13, atol=2e-13
    )


def test_torch_mms_and_independent_numpy_forcing_close_momentum_equation():
    torch = _torch()
    from tools.physicsnemo_shared_mms import velocity_torch

    points_np = np.array([
        [0.17, 0.43, 1.29],
        [2.11, 3.07, 4.91],
        [5.72, 2.83, 0.64],
    ])
    time_value = 0.023
    nu = 0.01
    points = torch.tensor(points_np, dtype=torch.float64, requires_grad=True)
    time = torch.full((len(points_np), 1), time_value, dtype=torch.float64, requires_grad=True)
    velocity = velocity_torch(points, time, frequency=4)
    gradient_rows = [
        torch.autograd.grad(velocity[:, i].sum(), points, create_graph=True, retain_graph=True)[0]
        for i in range(3)
    ]
    gradient = torch.stack(gradient_rows, dim=1)
    time_derivative = torch.stack([
        torch.autograd.grad(velocity[:, i].sum(), time, create_graph=True, retain_graph=True)[0][:, 0]
        for i in range(3)
    ], dim=1)
    laplacian_components = []
    for i in range(3):
        second_derivatives = [
            torch.autograd.grad(
                gradient[:, i, j].sum(), points, create_graph=True, retain_graph=True
            )[0][:, j]
            for j in range(3)
        ]
        laplacian_components.append(torch.stack(second_derivatives, dim=1).sum(dim=1))
    laplacian = torch.stack(laplacian_components, dim=1)
    force = torch.tensor(fields(points_np, N=4, nu=nu, time=time_value)["force"])
    residual = time_derivative + torch.einsum("bij,bj->bi", gradient, velocity) - nu * laplacian - force

    assert float(residual.detach().abs().max()) < 2e-11
