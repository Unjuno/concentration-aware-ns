import numpy as np
import pytest
from flint import arb,ctx
from tools.cell_point_local_derivative import affine_gradient,reference_gradient
from tools.high_gradient_reference import fields


def test_affine_recovery_and_vertex_permutation():
    p=np.array([[0,0,0],[1,0,0],[0,2,0],[0,0,4]],float)
    matrix=np.array([[2,3,5],[-1,4,2],[0,-2,1]],float)
    u=p@matrix.T+np.array([1,2,3])
    for order in ([0,1,2,3],[2,0,3,1]):
        g,_,det=affine_gradient(p[order],u[order])
        assert not det.contains(0)
        for i in range(3):
            for j in range(3):assert g[i,j].contains(int(matrix[i,j]))


def test_independent_reference_gradient_formula():
    old=ctx.prec;ctx.prec=96
    try:
        p=[.7,1.2,2.1];expected=fields(np.array([p]),N=3,time=.05)['grad_u'][0]
        actual=reference_gradient([arb(x) for x in p])
        assert max(abs(float(actual[i,j])-expected[i,j]) for i in range(3) for j in range(3))<3e-16
    finally:ctx.prec=old


def test_degenerate_tet_is_rejected():
    with pytest.raises(ValueError,match='nondegenerate'):
        affine_gradient(np.zeros((4,3)),np.zeros((4,3)))
