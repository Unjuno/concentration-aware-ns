import hashlib
import json
import tarfile

from tools import run_openfoam_foundation14_matrix as runner
from tools.verify_openfoam_foundation14_matrix import (
    _extract_archive,
    _verify_input_hashes,
    normalized_endpoint_field_hashes,
)


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


def test_completed_replay_compares_inputs_metrics_and_endpoint_fields(tmp_path):
    original = tmp_path / "original"
    replay = tmp_path / "replay"
    for case, log_hash in ((original, "a"), (replay, "b")):
        (case / "0.05").mkdir(parents=True)
        (case / "input-hashes.json").write_text('{"input":"same"}\n')
        (case / "diagnostics.json").write_text(json.dumps({
            "local_quality": {"status": "FAIL"},
            "sha256": {"log.foamRun": log_hash},
        }))
        for field in ("U", "p", "C", "phi"):
            (case / "0.05" / field).write_text(field + " data\n")
    result = runner.compare_completed_replay(original, replay)
    assert result["status"] == "PASS"
    assert result["preserved_run_log_sha256"] != result["replay_run_log_sha256"]


def test_version_banner_is_the_only_normalized_endpoint_difference(tmp_path):
    archives = []
    for version in (13, 14):
        archive_path = tmp_path / f"of{version}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            for field in ("U", "p", "C", "phi"):
                data = (f"OpenFOAM Version:  {version}\n" + field + " field\n").encode()
                import io
                import tarfile as tar

                info = tar.TarInfo(f"n64-dt0.001/0.05/{field}")
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        archives.append(archive_path)
    left = normalized_endpoint_field_hashes(archives[0], "n64-dt0.001", 13)
    right = normalized_endpoint_field_hashes(archives[1], "n64-dt0.001", 14)
    assert left == right


def test_archive_verification_uses_preserved_inputs_and_rejects_escape_paths(tmp_path):
    import io

    case = tmp_path / "n16-dt0.001"
    case.mkdir()
    payload = b"frozen input\n"
    (case / "controlDict").write_bytes(payload)
    (case / "input-hashes.json").write_text(json.dumps({
        "controlDict": hashlib.sha256(payload).hexdigest(),
    }))
    archive_path = tmp_path / "case.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for path in case.iterdir():
            archive.add(path, arcname=f"{case.name}/{path.name}")
    extracted = _extract_archive(archive_path, tmp_path / "extract", case.name)
    _verify_input_hashes(extracted)
    assert (extracted / "controlDict").read_bytes() == payload

    malicious = tmp_path / "malicious.tar.gz"
    with tarfile.open(malicious, "w:gz") as archive:
        member = tarfile.TarInfo("../outside")
        member.size = 1
        archive.addfile(member, io.BytesIO(b"x"))
    try:
        _extract_archive(malicious, tmp_path / "malicious-extract", case.name)
    except ValueError as error:
        assert "unexpected top-level path" in str(error)
    else:
        raise AssertionError("archive path escape was accepted")
    assert not (tmp_path / "outside").exists()


def test_preserved_incomplete_attempt_archive_excludes_partial_time_fields(tmp_path):
    run_root = tmp_path / "work"
    attempt = run_root / "attempts/n128-dt0.001-attempt-01-incomplete"
    (attempt / "0").mkdir(parents=True)
    (attempt / "system").mkdir()
    (attempt / "0/U").write_text("initial field\n")
    (attempt / "system/controlDict").write_text("control input\n")
    (attempt / "constant/transportProperties").parent.mkdir()
    (attempt / "constant/transportProperties").write_text("transport input\n")
    (attempt / "input-hashes.json").write_text(json.dumps({
        "0/U": "input-hash", "system/controlDict": "input-hash",
        "constant/transportProperties": "input-hash",
    }))
    (attempt / "constant/polyMesh").mkdir()
    (attempt / "constant/polyMesh/points").write_text("generated mesh\n")
    (attempt / "0.01").mkdir()
    (attempt / "0.01/U").write_text("partial output\n")
    (attempt / "log.foamRun").write_text("Time = 0.001\n")
    evidence = tmp_path / "evidence"

    result = runner.archive_preserved_attempt({
        "path": "attempts/n128-dt0.001-attempt-01-incomplete",
        "status": "INCOMPLETE_PRIOR_ATTEMPT_PRESERVED",
    }, evidence, run_root)
    archive_path = evidence / result["evidence_archive"]
    with tarfile.open(archive_path, "r:gz") as archive:
        names = {member.name for member in archive.getmembers() if member.isfile()}
    assert any(name.endswith("/0/U") for name in names)
    assert any(name.endswith("/system/controlDict") for name in names)
    assert any(name.endswith("/constant/transportProperties") for name in names)
    assert not any("polyMesh" in name for name in names)
    assert any(name.endswith("/log.foamRun") for name in names)
    assert not any("0.01" in name for name in names)
    assert result["excluded_partial_outputs"] == ["generated mesh and partial time directories"]
