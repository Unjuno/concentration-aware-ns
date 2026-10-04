import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools import run_of13_cell_point_capture_matrix as module


class CaptureIdentityControls(unittest.TestCase):
    def exercise(self,change=None,recipe='original'):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);case='n32-dt0.001'
            original={'source_files_sha256':{'recipe.py':'original'},'runs':[{'label':'main','inputs_sha256':{'U':'input'},'final_field_sha256':{'U':'final','p':'pressure'}}]}
            current=copy.deepcopy(original)
            if change=='input':current['runs'][0]['inputs_sha256']['U']='different'
            if change=='final':current['runs'][0]['final_field_sha256']['U']='different'
            manifest=root/'evidence/of13-amr-mean-quality-v1'/case/'manifest.json';manifest.parent.mkdir(parents=True);manifest.write_text(json.dumps(original))
            with patch.object(module,'ROOT',root),patch.object(module,'SOURCE_FILES',('recipe.py',)),patch.object(module,'FILES',()),patch.object(module,'sha',return_value=recipe),patch.object(module,'run',return_value=current) as run,patch.object(module,'resolve_docker_cli') as docker:
                with self.assertRaisesRegex(ValueError,'recipe changed' if recipe!='original' else 'rerun differs'):
                    module.capture(case,'unused',root/'upstream',root/'work',root/'capture')
                docker.assert_not_called()
                self.assertEqual(run.call_count,0 if recipe!='original' else 1)

    def test_different_initial_input_rejected_before_probe(self):self.exercise('input')
    def test_different_final_field_rejected_before_probe(self):self.exercise('final')
    def test_changed_recipe_rejected_before_solver(self):self.exercise(recipe='changed')
    def test_unfrozen_case_rejected(self):
        with self.assertRaisesRegex(ValueError,'outside frozen'):
            module.capture('n128-dt0.001','unused',Path('/unused'),Path('/unused'),Path('/unused'))
