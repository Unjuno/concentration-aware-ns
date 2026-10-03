import copy,io,json,tarfile,tempfile,unittest
from pathlib import Path
import numpy as np
from tools.analyze_of13_cell_point_query import measure
from tools.run_of13_cell_point_query import PROTOCOL,unpack_verified


class NativeQueryControls(unittest.TestCase):
    def fixture(self):
        spec=json.loads(PROTOCOL.read_text());v=np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
        u=np.array([[1.,2.,3.],[2.,5.,7.],[-1.,1.,5.],[4.,0.,6.]])
        nodes=[dict(node=i,label=([spec['cell']]+spec['point_indices'])[i],**dict(zip('xyz',v[i])),**dict(zip(('Ux','Uy','Uz'),u[i]))) for i in range(4)]
        expected=[(-1,0,0)]+[(a,2.**-p,s) for p in spec['step_powers'] for a in range(3) for s in (-1,1)]
        queries=[];candidates=[]
        for q,(axis,h,sign) in enumerate(expected):
            pos=np.array([.25,.25,.25]);
            if axis>=0:pos[axis]+=sign*h
            w=np.r_[1-pos.sum(),pos];val=w@u
            queries.append(dict(query=q,axis=axis,h=h,sign=sign,**dict(zip('xyz',pos)),**dict(zip(('p0','p1','p2'),spec['point_indices'])),**dict(zip(('w0','w1','w2','w3'),w)),**dict(zip(('Ux','Uy','Uz'),val)),**dict(zip(('Ex','Ey','Ez'),val)),det=1,first_face=spec['face'],first_tetPt=spec['tetPt']))
            candidates.append(dict(query=q,ordinal=0,face=spec['face'],tetPt=spec['tetPt'],**dict(zip(('p0','p1','p2'),spec['point_indices'])),det=1,cellV=1/6,tol=np.finfo(float).eps,**dict(zip(('w0','w1','w2','w3'),w)),accepted=1))
        return nodes,queries,candidates,dict(vertices=v.tolist(),nodal_values=u.tolist()),spec

    def test_known_affine_field(self):
        r=measure(*self.fixture());self.assertEqual(r['queries'],19)
        self.assertEqual([x['maximum_absolute_component_discrepancy'] for x in r['floating_secant_diagnostics']],[0.,0.,0.])

    def test_wrong_branch_even_identical_values_rejected(self):
        a=list(self.fixture());a[1][0]['p0']=0
        with self.assertRaisesRegex(ValueError,'addressing'):measure(*a)

    def test_missing_candidate_scan_rejected(self):
        a=list(self.fixture());a[2].pop()
        with self.assertRaisesRegex(ValueError,'candidate scan'):measure(*a)

    def test_false_accepted_flag_rejected(self):
        a=list(self.fixture());a[2][0]['w0']=-1
        with self.assertRaisesRegex(ValueError,'predicate inconsistent'):measure(*a)

    def test_constant_native_values_do_not_fake_derivative(self):
        a=list(self.fixture())
        for row in a[1]:
            for key in ('Ux','Uy','Uz','Ex','Ey','Ez'):row[key]=a[1][0][key]
        with self.assertRaisesRegex(ValueError,'values differ'):measure(*a)

    def test_missing_query_rejected(self):
        a=list(self.fixture());a[1].pop()
        with self.assertRaisesRegex(ValueError,'coverage'):measure(*a)


class ArchiveControls(unittest.TestCase):
    def test_traversal_and_link_rejected(self):
        for name,kind in [('../escape',tarfile.REGTYPE),('link',tarfile.SYMTYPE)]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'archive.tar.gz'
                with tarfile.open(p,'w:gz') as t:
                    m=tarfile.TarInfo(name);m.type=kind;m.size=1 if kind==tarfile.REGTYPE else 0
                    t.addfile(m,io.BytesIO(b'x') if m.size else None)
                with self.assertRaises(ValueError):unpack_verified(p,Path(d)/'out')
                self.assertFalse((Path(d)/'escape').exists())

    def test_changed_member_digest_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'archive.tar.gz'
            with tarfile.open(p,'w:gz') as t:
                m=tarfile.TarInfo('x');m.size=1;t.addfile(m,io.BytesIO(b'x'))
            with self.assertRaisesRegex(ValueError,'digest'):unpack_verified(p,Path(d)/'out',{'x':'0'*64})
