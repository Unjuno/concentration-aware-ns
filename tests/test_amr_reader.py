import tempfile,unittest
from pathlib import Path
import numpy as np
from tools.analyze_amr import values


class AmrReaderTests(unittest.TestCase):
    def test_uniform_volume_field(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'Vc';p.write_text('internalField uniform 0.125;')
            np.testing.assert_array_equal(values(p,8),np.full(8,0.125))

    def test_nonuniform_volumes_preserve_weights(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'Vc';p.write_text('internalField nonuniform List<scalar> 3 (1 0.125 0.125);')
            np.testing.assert_array_equal(values(p,3),[1,0.125,0.125])
            with self.assertRaises(ValueError):values(p,4)

    def test_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'Vc';p.write_text('internalField uniform nan;')
            with self.assertRaises(ValueError):values(p,8)
