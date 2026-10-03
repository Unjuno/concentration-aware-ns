import csv,tempfile,unittest
from pathlib import Path
from tools.analyze_of13_cell_point_capture_stream import measure,CELL_HEADER,POINT_HEADER,FACE_HEADER,TET_HEADER
from tests.test_cell_point_capture_validation import fixture


class StreamTopologyControls(unittest.TestCase):
    def evaluate(self,mutation=None,batch=1):
        data=fixture()
        if mutation:mutation(data)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for table,header in [('cells',CELL_HEADER),('points',POINT_HEADER),('faces',FACE_HEADER),('tets',TET_HEADER)]:
                values=data[table];count=len(next(iter(values.values())))
                with (root/(table+'.csv')).open('w') as f:
                    w=csv.writer(f);w.writerow(header)
                    for i in range(count):w.writerow([values[k][i] if k in values else 0 for k in header])
            return measure(root,data['summary'],root/'scratch',batch)
    def test_pair_reversed_orientation_across_batch_boundary(self):
        for size in (1,2,7):
            r=self.evaluate(batch=size);self.assertTrue(r['shared_internal_face_triangles_match_owner_neighbour']);self.assertEqual(r['disk_backed_internal_triangle_keys'],1)
    def test_wrong_vertex_not_hidden_by_equal_face_samples(self):
        r=self.evaluate(lambda x:x['tets']['p2'].__setitem__(1,2));self.assertFalse(r['shared_internal_face_triangles_match_owner_neighbour'])
    def test_duplicate_owner_rejected_by_pair_counts(self):
        r=self.evaluate(lambda x:x['tets']['cell'].__setitem__(1,0));self.assertFalse(r['shared_internal_face_triangles_match_owner_neighbour'])
    def test_degenerate_and_volume_deficit_reported(self):
        def mutate(x):x['tets']['det'][0]=0;x['tets']['volume'][0]=0
        r=self.evaluate(mutate);self.assertFalse(r['all_recorded_tet_determinants_above_native_small']);self.assertEqual(r['maximum_cell_tet_volume_relative_mismatch'],1)
    def test_incomplete_row_count_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing or excess'):self.evaluate(lambda x:x['summary'].__setitem__('tets',3))
