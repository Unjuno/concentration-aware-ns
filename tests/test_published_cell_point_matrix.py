import json,tempfile,unittest,shutil
from pathlib import Path
from tools.run_amr_mean_quality import ROOT
from tools.verify_published_cell_point_matrix import native_identity

class PublishedIdentityControls(unittest.TestCase):
    def mutated(self,mutate):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'e';shutil.copytree(ROOT/'evidence/cell-point-matrix-native-query-v1/n32',p)
            mutate(p)
            return native_identity(p,ROOT/'protocols/of13-cell-point-matrix-query-n32-v1.json')
    def test_known_receipt(self):self.mutated(lambda p:None)
    def test_self_asserted_pin_substitution_rejected(self):
        def alter(p):
            f=p/'manifest.json';r=json.loads(f.read_text());r['upstream_commit']='0'*40;f.write_text(json.dumps(r))
        with self.assertRaisesRegex(ValueError,'independent pin'):self.mutated(alter)
    def test_duplicate_installed_file_rejected(self):
        def alter(p):
            f=p/'installed-source-files.sha256';s=f.read_text();f.write_text(s+s.splitlines()[0]+'\n')
        with self.assertRaisesRegex(ValueError,'installed source'):self.mutated(alter)
