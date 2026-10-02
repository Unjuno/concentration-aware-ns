import hashlib
import json
import tarfile

from tools import run_openfoam_foundation14_matrix as runner


def test_of14_protocol_reuses_of13_equations_matrix_and_gates():
    of13 = json.loads((runner.ROOT / "protocols/high-gradient-of13-v2.json").read_text())
    of14 = json.loads(runner.PROTOCOL.read_text())
    for key in (
        "profile", "domain", "frequency_N", "amplitude", "viscosity", "end_time",
        "spatial_matrix", "temporal_matrix", "standard_acceptance",
        "local_quality_relative_error_thresholds",
    ):
        assert of14[key] == of13[key]
    assert runner.expected_cases(of14) == [
        "n16-dt0.001", "n32-dt0.001", "n64-dt0.001", "n128-dt0.001",
        "n64-dt0.0005", "n64-dt0.00025",
    ]
    assert of14["comparison"]["reused_case"]["case"] == "n64-dt0.001"
    assert runner.sha256(runner.BASELINE) == of14["comparison"]["reused_case"]["archive_sha256"]


def test_archive_case_splits_and_preserves_reassembly_hash(tmp_path, monkeypatch):
    case = tmp_path / "n16-dt0.001"
    (case / "system").mkdir(parents=True)
    (case / "system/controlDict").write_text("frozen input\n")
    (case / "diagnostics.json").write_text('{"status":"PASS"}\n')
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    monkeypatch.setattr(runner, "MAX_ARCHIVE_PART_BYTES", 40)

    result = runner.archive_case(case, evidence, case.name)
    manifest = json.loads((evidence / result["archive"]).read_text())
    rebuilt = tmp_path / "rebuilt.tar.gz"
    with rebuilt.open("wb") as output:
        for part in manifest["parts"]:
            output.write((evidence / part["file"]).read_bytes())
    assert hashlib.sha256(rebuilt.read_bytes()).hexdigest() == result["archive_sha256"]
    with tarfile.open(rebuilt, "r:gz") as archive:
        assert archive.extractfile("n16-dt0.001/system/controlDict").read() == b"frozen input\n"


def test_complete_case_requires_all_steps_end_marker_and_endpoint_fields(tmp_path):
    case = tmp_path / "n16-dt0.001"
    endpoint = case / "0.05"
    endpoint.mkdir(parents=True)
    for field in ("U", "p", "C", "phi"):
        (endpoint / field).write_text("field\n")
    (case / "exit.json").write_text('{"exit_code":0}\n')
    (case / "diagnostics.json").write_text(json.dumps({"parameters": {"dt": 0.001}}))
    (case / "log.foamRun").write_text(
        "".join(f"Time = {index / 1000:g}\nPIMPLE: Converged in 1 iterations\n"
                for index in range(1, 51)) + "End\n"
    )
    assert runner.complete_case(case, 0.05)
    (case / "log.foamRun").write_text("Time = 0.001\nEnd\n")
    assert not runner.complete_case(case, 0.05)
