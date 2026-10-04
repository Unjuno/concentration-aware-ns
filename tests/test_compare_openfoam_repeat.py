import copy
import hashlib
import io
import json
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools.compare_openfoam_repeat import compare


ROOT = Path(__file__).resolve().parents[1]
BASE_MANIFEST = ROOT / "evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005-manifest.json"
BASE_ARCHIVE = ROOT / "evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005.tar.gz"
REPEAT_MANIFEST = ROOT / "evidence/of13-high-gradient-repeat-2026-10-01/manifest.json"
REPEAT_ARCHIVE = ROOT / "evidence/of13-high-gradient-repeat-2026-10-01/n64-dt0.0005.tar.gz"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_manifest(tmp_path, blob, updates=None):
    manifest = json.loads(REPEAT_MANIFEST.read_text())
    manifest["archive_sha256"] = digest(blob)
    manifest.update(updates or {})
    path = tmp_path / "repeat-manifest.json"
    path.write_text(json.dumps(manifest))
    return path


def mutate_archive(tmp_path, member_name, transform):
    output = tmp_path / "mutated.tar.gz"
    log_data = None
    with tarfile.open(REPEAT_ARCHIVE, "r:gz") as source, \
            tarfile.open(output, "w:gz") as target:
        for info in source.getmembers():
            data = source.extractfile(info).read() if info.isfile() else None
            if info.name == f"n64-dt0.0005/{member_name}":
                data = transform(data)
            if info.isfile():
                info.size = len(data)
                target.addfile(info, io.BytesIO(data))
                if info.name.endswith("/log.foamRun"):
                    log_data = data
            else:
                target.addfile(info)
    return output, log_data


def args(repeat_manifest=REPEAT_MANIFEST, repeat_archive=REPEAT_ARCHIVE):
    return SimpleNamespace(
        baseline_manifest=BASE_MANIFEST,
        baseline_archive=BASE_ARCHIVE,
        repeat_manifest=repeat_manifest,
        repeat_archive=repeat_archive,
    )


def test_real_case_repeat_cross_checks_raw_provenance():
    result = compare(args())
    assert result["success"]
    assert result["raw_log_steps_end_and_convergence_independently_verified"]
    assert result["archived_input_hashes_independently_verified"]
    assert result["unexpected_raw_differences"] == []


def test_changed_time_label_fails_even_if_hash_records_are_updated(tmp_path):
    archive, log = mutate_archive(
        tmp_path, "log.foamRun",
        lambda raw: raw.replace(b"Time = 0.0005s", b"Time = 0.0006s", 1),
    )
    assert log is not None
    blob = archive.read_bytes()
    manifest = write_manifest(tmp_path, blob, {"source_log_sha256": digest(log)})
    with tarfile.open(archive, "r:gz") as tar:
        diagnostics = json.load(tar.extractfile("n64-dt0.0005/diagnostics.json"))
    diagnostics["sha256"]["log.foamRun"] = digest(log)
    # Rebuild one archive coherently with both the altered solver log and its hash reference.
    rebuilt = tmp_path / "coherent-mutated.tar.gz"
    with tarfile.open(archive, "r:gz") as source, tarfile.open(rebuilt, "w:gz") as target:
        for info in source.getmembers():
            data = source.extractfile(info).read() if info.isfile() else None
            name = info.name.split("/", 1)[1] if "/" in info.name else ""
            if name == "diagnostics.json":
                data = json.dumps(diagnostics, indent=2).encode()
            if info.isfile():
                info.size = len(data)
                target.addfile(info, io.BytesIO(data))
            else:
                target.addfile(info)
    manifest = write_manifest(tmp_path, rebuilt.read_bytes(), {"source_log_sha256": digest(log)})
    with pytest.raises(ValueError, match="time sequence"):
        compare(args(manifest, rebuilt))


def test_unrelated_raw_file_change_is_rejected(tmp_path):
    archive, _ = mutate_archive(
        tmp_path, "log.container", lambda raw: raw + b"unexpected diagnostic alteration\n"
    )
    manifest = write_manifest(tmp_path, archive.read_bytes())
    with pytest.raises(ValueError, match="allowlist"):
        compare(args(manifest, archive))


def test_manifest_gate_cannot_override_diagnostics():
    manifest = json.loads(REPEAT_MANIFEST.read_text())
    manifest["local_quality"] = "FAIL"
    path = ROOT / "work/repeat-manifest-tamper.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(manifest))
    try:
        with pytest.raises(ValueError, match="manifest local verdict"):
            compare(args(path))
    finally:
        path.unlink(missing_ok=True)
