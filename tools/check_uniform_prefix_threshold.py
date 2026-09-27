"""Exact rational upper bound for the conditional local prefix criterion."""
from fractions import Fraction as F
import json
import sympy as sp
from pathlib import Path

# 0<h<=1/1000 and -j/4<eta<-j/5, 0<j<=1/1000 imply
# 0<D=1/2-h<1/2 and x=eta^2<1/16000000.
# B = D/(10*(1-x))*(1+2*D*x/(1-x))*(1+x)^2.
# Positive-factor bounds D<=1/2, 2D<=1 give
# B <= (1+x)^2/(20*(1-x)^2).
# (1+x)/(1-x) increases on [0,1); use x<=xmax.
D, x, y = sp.symbols('D x y', real=True)
B = D*(1-x+2*D*x)*(1+x)**2/(10*(1-x)**2)
upper_at_x = (1+x)**2/(20*(1-x)**2)
upper_at_y = (1+y)**2/(20*(1-y)**2)
# Both right sides are nonnegative on 0<D<=1/2 and 0<=x<=y<1.
D_gap = (1+x)**2*(1-2*D)*(1+2*D*x)/(20*(1-x)**2)
x_gap = (y-x)*(1-x*y)/(5*(1-y)**2*(1-x)**2)
assert sp.cancel(upper_at_x-B-D_gap) == 0
assert sp.cancel(upper_at_y-upper_at_x-x_gap) == 0
xmax = F(1, 16000000)
upper = (1+xmax)**2 / (20*(1-xmax)**2)
amplitude = F(9, 40)
margin = amplitude**2-upper
assert 0 < xmax < 1
assert margin > 0
# Algebraic certificate for monotonicity, without floating-point sampling:
# (1+y)/(1-y)-(1+x)/(1-x) = 2*(y-x)/((1-y)*(1-x)).
result = {
    'assumptions': '0<h<=1/1000; 0<j<=1/1000; -j/4<eta<-j/5; outgoing root equation and source prefix bound',
    'eta_squared_upper': str(xmax),
    'amplitude_squared_threshold_upper': str(upper),
    'sufficient_amplitude': str(amplitude),
    'strict_squared_margin': str(margin),
    'rational_comparison_pass': True,
    'symbolic_gap_identities_pass': True,
    'amplitude_gap_factorization': str(D_gap),
    'endpoint_gap_factorization': str(x_gap),
    'sympy': sp.__version__,
    'actual_profile_amplitude_bound_proved': False,
    'scope': 'Symbolically checked nonnegative-gap identities and exact rational endpoint arithmetic; factor signs use the stated real inequalities. Not a Lean proof or complete-profile existence construction'
}
Path('evidence/tests/uniform-prefix-threshold.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
