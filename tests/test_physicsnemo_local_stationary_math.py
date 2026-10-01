from flint import arb

from tools.certify_physicsnemo_local_stationary import _objective_jet


def test_objective_jet_matches_scalar_square_derivatives():
    gradient = [[arb(0) for _ in range(3)] for _ in range(3)]
    hessian = [[[arb(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    third = [[[[arb(0) for _ in range(3)] for _ in range(3)]
              for _ in range(3)] for _ in range(3)]

    # One nonzero entry is G(x)=x^2 at x=2: f=G^2 has f'=32 and f''=48.
    gradient[0][0] = arb(4)
    hessian[0][0][0] = arb(4)
    third[0][0][0][0] = arb(2)
    grad_f, hess_f = _objective_jet(gradient, hessian, third)

    assert float(grad_f[0].lower()) <= 32 <= float(grad_f[0].upper())
    assert float(hess_f[0][0].lower()) <= 48 <= float(hess_f[0][0].upper())
    assert hess_f[0][1] == 0
    assert hess_f[1][0] == 0
