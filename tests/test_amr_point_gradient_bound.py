import numpy as np
import pytest
from flint import arb, ctx
from tools.amr_point_gradient_bound import point_reference, chord_certificate
from tools.high_gradient_reference import fields


def test_independent_point_formula_matches_fourier_reference():
    old=ctx.prec;ctx.prec=96
    try:
        points=np.array([[.3,1.4,2.2],[0.,0.,0.],[2.9,3.1,4.2]])
        expected=fields(points,N=3,time=.05)['u']
        for point, vector in zip(points,expected):
            actual=point_reference(point,'0.05')
            assert max(abs(float(a)-b) for a,b in zip(actual,vector))<2e-16
    finally:ctx.prec=old


def test_known_linear_error_has_certified_chord_slope():
    old=ctx.prec;ctx.prec=96
    try:
        # y=z=pi is avoided: at y=z=0 and x=0 both references are exactly known.
        a=np.array([0.,0.,0.]);b=np.array([0.,0.,.125])
        ra=np.array([float(x) for x in point_reference(a,'0.05')])
        rb=np.array([float(x) for x in point_reference(b,'0.05')])
        rb[2]=.25
        result=chord_certificate(a,b,ra,rb)
        lower=arb(result['gradient_absolute_peak_error_lower']['lower_rational'])
        assert lower>arb('1.999999999999') and lower<=2
        assert result['above_disclosed_five_percent_target']
    finally:ctx.prec=old


def test_coincident_points_are_rejected():
    with pytest.raises(ValueError,match='distinct'):
        chord_certificate([0,0,0],[0,0,0],[1,0,0],[0,0,0])
