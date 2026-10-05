import tempfile,unittest
from pathlib import Path
import numpy as np
from tools.cell_point_capture_chunks import chunks,nodes


class ChunkControls(unittest.TestCase):
    def file(self,root,text):
        p=Path(root)/'data.csv';p.write_text(text);return p
    def test_batch_boundaries_preserve_all_rows(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.file(d,'a,b\n1,2\n3,4\n5,6\n')
            for size in (1,2,10):
                rows=list(chunks(p,('a','b'),size));self.assertEqual(np.concatenate([r['a'] for r in rows]).tolist(),[1.,3.,5.]);self.assertTrue(all(len(r['a'])<=size for r in rows))
    def test_nonfinite_or_ragged_rejected(self):
        for text in ('a,b\n1,nan\n','a,b\n1\n'):
            with self.subTest(text=text),tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):list(chunks(self.file(d,text),('a','b'),1))
    def test_wrong_header_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):list(chunks(self.file(d,'a,a\n1,2\n'),('a','b')))
    def test_missing_or_unordered_nodes_rejected(self):
        for row in ('1,0,0,0,1,2,3','0,0,0,0,1,2,3'):
            with self.subTest(row=row),tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):nodes(self.file(d,'point,x,y,z,Ux,Uy,Uz\n'+row+'\n'),'points',2,1)
    def test_node_values_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.file(d,'point,x,y,z,Ux,Uy,Uz\n0,0,1,2,3,4,5\n1,6,7,8,9,10,11\n')
            x,u=nodes(p,'points',2,1);self.assertEqual(x.tolist(),[[0,1,2],[6,7,8]]);self.assertEqual(u.tolist(),[[3,4,5],[9,10,11]])
