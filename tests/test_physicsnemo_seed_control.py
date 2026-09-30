import unittest
import hashlib
import tarfile
import tempfile
from pathlib import Path

from tools.physicsnemo_seed_control import (
    expand_runs,
    validate_plan,
    verify_source_tree,
)


class PhysicsNeMoSeedControlTests(unittest.TestCase):
    def test_expands_only_new_seeds_across_every_case(self):
        plan = {
            "reference_seed": 709,
            "seeds": [709, 1729, 2027],
            "cases": [[16, 5], [64, 17]],
        }

        validate_plan(plan)

        self.assertEqual(
            expand_runs(plan),
            [
                {"seed": 1729, "n": 16, "time_nodes": 5},
                {"seed": 1729, "n": 64, "time_nodes": 17},
                {"seed": 2027, "n": 16, "time_nodes": 5},
                {"seed": 2027, "n": 64, "time_nodes": 17},
            ],
        )

    def test_rejects_duplicate_or_missing_reference_seed(self):
        plan = {
            "reference_seed": 709,
            "seeds": [709, 709],
            "cases": [[16, 5]],
        }

        with self.assertRaisesRegex(ValueError, "unique"):
            validate_plan(plan)

        plan["seeds"] = [1729]
        with self.assertRaisesRegex(ValueError, "reference seed"):
            validate_plan(plan)

    def test_rejects_duplicate_or_invalid_cases(self):
        plan = {
            "reference_seed": 709,
            "seeds": [709, 1729],
            "cases": [[16, 5], [16, 5], [64, 2]],
        }

        with self.assertRaisesRegex(ValueError, "unique"):
            validate_plan(plan)

        plan["cases"] = [[64, 1]]
        with self.assertRaisesRegex(ValueError, "time_nodes"):
            validate_plan(plan)

    def test_verifies_pinned_source_tree_and_only_allows_python_caches(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            local = root / "source"
            (local / "package").mkdir(parents=True)
            (local / "package" / "module.py").write_text("value = 1\n")
            cache = local / "package" / "__pycache__"
            cache.mkdir()
            (cache / "module.pyc").write_bytes(b"cache")
            archive = root / "source.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(local / "package" / "module.py", arcname="pinned/package/module.py")

            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            result = verify_source_tree(archive, local, digest)

            self.assertEqual(result["matching_files"], 1)
            self.assertEqual(result["allowed_extra_files"], 1)

            (local / "package" / "module.py").write_text("value = 2\n")
            with self.assertRaisesRegex(ValueError, "source mismatch"):
                verify_source_tree(archive, local, digest)


if __name__ == "__main__":
    unittest.main()
