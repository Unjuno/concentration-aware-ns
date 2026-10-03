import tempfile,unittest
from pathlib import Path
from tools.audit_cell_point_matrix_neighborhood import selected_nodes

class SelectedNodeControls(unittest.TestCase):
    def run_nodes(self,text,wanted,count):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'nodes.csv';p.write_text(text)
            return selected_nodes(p,('point','x','y','z'),'point',tuple('xyz'),wanted,count,1)
    def test_selection_across_batch_boundaries(self):
        self.assertEqual(self.run_nodes('point,x,y,z\n0,1,2,3\n1,4,5,6\n2,7,8,9\n',{0,2},3),{0:[1.,2.,3.],2:[7.,8.,9.]})
    def test_unselected_label_corruption_rejected(self):
        with self.assertRaisesRegex(ValueError,'unordered'):
            self.run_nodes('point,x,y,z\n0,1,2,3\n2,4,5,6\n',{0},2)
    def test_missing_unselected_node_rejected(self):
        with self.assertRaisesRegex(ValueError,'incomplete'):
            self.run_nodes('point,x,y,z\n0,1,2,3\n',{0},2)
    def test_nonfinite_unselected_node_rejected(self):
        with self.assertRaisesRegex(ValueError,'finite'):
            self.run_nodes('point,x,y,z\n0,1,2,3\n1,nan,5,6\n',{0},2)
