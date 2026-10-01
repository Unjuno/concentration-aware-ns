import tarfile
import tempfile
import unittest
from pathlib import Path

from tools.package_amr_stage_evidence import package_case


class PackageAmrStageEvidenceTests(unittest.TestCase):
    def test_protocol_exclusions_preserve_cells_and_omit_faces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "case-n32"
            stage = root / "postProcessing/amrStages/0.002"
            stage.mkdir(parents=True)
            (stage / "mapped_cells.csv").write_text("cell,Ux\n0,1\n")
            (stage / "mapped_faces.csv").write_text("face,phi\n0,1\n")
            (root / "log.foamRun").write_text("End\n")
            (root / "dynamicCode/generated.C").parent.mkdir(parents=True)
            (root / "dynamicCode/generated.C").write_text("generated\n")
            archive_path = Path(tmp) / "case.tar.gz"
            record = package_case(root, archive_path, [
                "postProcessing/amrStages/*/*_faces.csv", "dynamicCode"
            ])
            self.assertEqual(record["excluded_patterns_observed"], [
                "dynamicCode", "postProcessing/amrStages/*/*_faces.csv"
            ])
            with tarfile.open(archive_path, "r:gz") as archive:
                names = archive.getnames()
            self.assertIn("case-n32/postProcessing/amrStages/0.002/mapped_cells.csv", names)
            self.assertIn("case-n32/log.foamRun", names)
            self.assertFalse(any(name.endswith("_faces.csv") for name in names))
            self.assertFalse(any("dynamicCode" in name for name in names))


if __name__ == "__main__":
    unittest.main()
