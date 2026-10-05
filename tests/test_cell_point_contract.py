"""Independent negative control: point constraints alone cannot bound gradients."""
import sympy as sp


def test_discontinuous_point_interpolant_invalidates_the_chord_inference():
    z=sp.symbols('z',real=True)
    # Two cell-constant patches reproduce point values at z=-1,+1, with
    # zero classical derivative on each open cell and a jump at their face.
    left=sp.Integer(-1);right=sp.Integer(1)
    point_chord=abs(right-left)/2
    assert sp.diff(left,z)==sp.diff(right,z)==0
    assert point_chord==1
    assert right-left!=0  # A Lipschitz/shared-trace hypothesis is indispensable.
