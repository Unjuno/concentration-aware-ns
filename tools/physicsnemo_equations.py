"""Original transient 3D PDE specification for the pinned PhysicsNeMo API."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path("work/physicsnemo-source").resolve()))
from sympy import Function, Symbol
from physicsnemo.sym.eq.pde import PDE

class TransientNS(PDE):
    def __init__(self):
        self.dim=3
        x,y,z,t=[Symbol(v) for v in ('x','y','z','t')];xs=(x,y,z)
        us=[Function(v)(x,y,z,t) for v in ('u','v','w')];p=Function('p')(x,y,z,t)
        self.equations={'continuity':sum(u.diff(q) for u,q in zip(us,xs))}
        for i,name in enumerate(('x','y','z')):
            u=us[i]
            self.equations['momentum_'+name]=u.diff(t)+sum(v*u.diff(q) for v,q in zip(us,xs))+p.diff(xs[i])-.01*sum(u.diff(q,2) for q in xs)-Symbol('f'+name)

