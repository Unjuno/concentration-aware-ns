import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.reconstruct_amr_published_archive import reconstruct


class ReconstructPublishedArchiveTests(unittest.TestCase):
    def test_suppresses_nondeterministic_zstd_success_path(self):
        compressed_part = b"fixture compressed payload"
        reconstructed_archive = b"fixture tarball payload"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            part_path = root / "archive.part-00"
            part_path.write_bytes(compressed_part)
            manifest_path = root / "parts.json"
            manifest_path.write_text(json.dumps({
                "archive": "archive.tar.zst",
                "archive_bytes": len(compressed_part),
                "archive_sha256": hashlib.sha256(compressed_part).hexdigest(),
                "source_tar_gz_bytes": len(reconstructed_archive),
                "source_tar_gz_sha256": hashlib.sha256(reconstructed_archive).hexdigest(),
                "parts": [{
                    "path": part_path.name,
                    "bytes": len(compressed_part),
                    "sha256": hashlib.sha256(compressed_part).hexdigest(),
                }],
            }))
            output = root / "reconstructed.tar.gz"

            def fake_zstd(command, *, check, stdout, stderr, text):
                self.assertTrue(check)
                self.assertEqual(stdout, subprocess.DEVNULL)
                self.assertEqual(stderr, subprocess.PIPE)
                self.assertTrue(text)
                Path(command[-1]).write_bytes(reconstructed_archive)

            with patch("tools.reconstruct_amr_published_archive.subprocess.run",
                       side_effect=fake_zstd) as run:
                result = reconstruct(manifest_path, output)

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["sha256"], hashlib.sha256(reconstructed_archive).hexdigest())
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
