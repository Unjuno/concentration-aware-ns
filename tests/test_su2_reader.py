import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from tools.analyze_su2 import analyze
from tools.reference import fields

class SU2ReaderTests(unittest.TestCase):
    def fixture(self,root):
        p=Path(root);n=4
        (p/'parameters.json').write_text(json.dumps({'n':n,'dt':.001,'end':.001,'sigma':.5,'nu':.01}))
        for name,text in [('exit_code','0'),('solver.log','Exit Success (SU2_CFD)'),('case.cfg','fixture'),('mesh.su2','fixture')]:
            (p/name).write_text(text)
        (p/'history.csv').write_text('Time_Iter,Cur_Time,rms[P],rms[U],rms[V],rms[W]\n0,0,-11,-11,-11,-11\n')
        x=np.array([(i,j,k) for i in range(n+1) for j in range(n+1) for k in range(n+1)])*2*np.pi/n
        u=fields(x,.001)['u']
        np.savetxt(p/'restart_00000.csv',np.column_stack((x,u)),delimiter=',',header='x,y,z,Velocity_x,Velocity_y,Velocity_z',comments='')
        return p
    def test_reordered_vertex_grid_and_time(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fixture(td);d=analyze(p)
            self.assertEqual(d['unique_points'],64)
            self.assertLess(d['velocity_relative_l2'],1e-14)
            self.assertEqual(d['updated_solution_time'],.001)
            self.assertEqual(d['reported_and_source_time'],0)
    def test_missing_periodic_grid_point_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fixture(td);f=p/'restart_00000.csv';lines=f.read_text().splitlines();f.write_text('\n'.join([lines[0]]+lines[2:])+'\n')
            with self.assertRaisesRegex(ValueError,'incomplete unique'):analyze(p)
    def test_changed_time_convention_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.fixture(td);f=p/'history.csv';f.write_text(f.read_text().replace('0,0,-11','0,.001,-11'))
            with self.assertRaisesRegex(ValueError,'reported-time'):analyze(p)
