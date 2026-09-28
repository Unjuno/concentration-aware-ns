import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.archive_high_gradient_openfoam import resolve_archive_roots
from tools.check_high_gradient_cpp_mock import resolve_compiler
from tools.run_high_gradient_openfoam import (
    resolve_docker_cli,
    resolve_docker_context,
    resolve_run_root,
)
from tools.run_high_gradient_amr import resolve_amr_run_root


class DockerCliResolutionTests(unittest.TestCase):
    def test_explicit_absolute_cli_is_preserved_and_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            cli = Path(directory) / "docker"
            cli.write_text("#!/bin/sh\nexit 0\n")
            cli.chmod(0o755)
            with patch.dict(os.environ, {"CANS_DOCKER_CLI": str(cli)}):
                requested, resolved = resolve_docker_cli()
            self.assertEqual(requested, str(cli))
            self.assertEqual(resolved, str(cli.resolve()))

    def test_relative_override_is_rejected(self):
        with patch.dict(os.environ, {"CANS_DOCKER_CLI": "docker"}):
            with self.assertRaisesRegex(ValueError, "absolute path"):
                resolve_docker_cli()

    def test_default_cli_comes_from_path(self):
        with tempfile.TemporaryDirectory() as directory:
            cli = Path(directory) / "docker"
            cli.write_text("#!/bin/sh\nexit 0\n")
            cli.chmod(0o755)
            with patch.dict(os.environ, {"PATH": directory}):
                with patch.dict(os.environ, {}, clear=False):
                    os.environ.pop("CANS_DOCKER_CLI", None)
                    requested, resolved = resolve_docker_cli()
            self.assertEqual(requested, str(cli))
            self.assertEqual(resolved, str(cli.resolve()))

    def test_context_is_read_from_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            cli = Path(directory) / "docker"
            cli.write_text("#!/bin/sh\nprintf 'orbstack\\n'\n")
            cli.chmod(0o755)
            with patch.dict(os.environ, {"CANS_DOCKER_CONTEXT": ""}):
                self.assertEqual(resolve_docker_context(str(cli)), "orbstack")

    def test_explicit_context_is_used_verbatim_after_trimming(self):
        with patch.dict(os.environ, {"CANS_DOCKER_CONTEXT": " orbstack "}):
            self.assertEqual(resolve_docker_context("not-executed"), "orbstack")

    def test_run_root_can_be_given_a_collision_free_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "fresh-run"
            with patch.dict(os.environ, {"CANS_OF13_RUN_ROOT": str(root)}):
                self.assertEqual(resolve_run_root(), root.resolve())

    def test_amr_run_root_can_be_given_a_collision_free_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "fresh-amr-run"
            with patch.dict(os.environ, {"CANS_OF13_AMR_RUN_ROOT": str(root)}):
                self.assertEqual(resolve_amr_run_root(), root.resolve())

    def test_custom_evidence_root_refuses_existing_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "evidence"
            evidence.mkdir()
            (evidence / "prior.json").write_text("{}\n")
            with patch.dict(os.environ, {
                "CANS_OF13_RUN_ROOT": str(Path(directory) / "run"),
                "CANS_OF13_EVIDENCE_ROOT": str(evidence),
            }):
                with self.assertRaisesRegex(FileExistsError, "refusing to overwrite"):
                    resolve_archive_roots()

    def test_explicit_absolute_cxx_is_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            compiler = Path(directory) / "clang++"
            compiler.write_text("#!/bin/sh\nexit 0\n")
            compiler.chmod(0o755)
            with patch.dict(os.environ, {"CXX": str(compiler)}):
                self.assertEqual(resolve_compiler(), str(compiler.resolve()))

    def test_missing_explicit_cxx_fails_instead_of_falling_back(self):
        with patch.dict(os.environ, {"CXX": "/missing/compiler"}):
            with self.assertRaises(FileNotFoundError):
                resolve_compiler()


if __name__ == "__main__":
    unittest.main()
