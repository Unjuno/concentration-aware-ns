"""Verify Foundation 14 matrix case archives and replay comparisons."""
import hashlib
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path

from tools.run_openfoam_foundation14_matrix import (
    ROOT,
    complete_case,
    compare_completed_replay,
    expected_cases,
    sha256,
)


PROTOCOL = ROOT / "protocols/high-gradient-of14-v1.json"
RUN_ROOT = ROOT / "work/of14-high-gradient-v1"
EVIDENCE = ROOT / "evidence/of14-high-gradient-v1-matrix"
V13_INDEX = ROOT / "evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json"
V13_ADDENDUM = ROOT / "evidence/of13-high-gradient-v2-temporal-addendum"
METRICS = (
    "velocity_relative_l2",
    "energy_relative_error_cell_samples",
    "gradient_peak_relative_error_cell_samples",
    "vorticity_peak_relative_error_cell_samples",
    "shell_spectrum_relative_l1_error",
)


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def materialize_archive(case_name, row, temp_root):
    archive_ref = row["archive"]
    if case_name == "n64-dt0.001":
        return ROOT / archive_ref
    if archive_ref.endswith(".parts.json"):
        parts_path = EVIDENCE / archive_ref
        metadata = json.loads(parts_path.read_text())
        archive_path = Path(temp_root) / metadata["archive"]
        digest = hashlib.sha256()
        total = 0
        with archive_path.open("wb") as output:
            for part in metadata["parts"]:
                part_path = EVIDENCE / part["file"]
                data_sha = sha256(part_path)
                if part_path.stat().st_size != part["bytes"] or data_sha != part["sha256"]:
                    raise ValueError(f"archive part integrity mismatch: {part_path}")
                with part_path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1 << 20), b""):
                        output.write(chunk)
                        digest.update(chunk)
                        total += len(chunk)
        if total != metadata["archive_bytes"] or digest.hexdigest() != metadata["archive_sha256"]:
            raise ValueError(f"reassembled split archive failed integrity: {parts_path}")
        return archive_path
    return EVIDENCE / archive_ref


def verify_case_archive(case_name, row, temp_root):
    archive_path = materialize_archive(case_name, row, temp_root)
    if not archive_path.is_file() or sha256(archive_path) != row["archive_sha256"]:
        raise ValueError(f"archive hash mismatch for {case_name}: {archive_path}")
    case_path = RUN_ROOT / case_name
    if not complete_case(case_path, json.loads(PROTOCOL.read_text())["end_time"]):
        raise ValueError(f"work case fails full completion check: {case_name}")
    source_files = {str(path.relative_to(case_path)): path
                    for path in case_path.rglob("*") if path.is_file() or path.is_symlink()}
    archived_root = case_name
    with tarfile.open(archive_path, "r:gz") as archive:
        members = {member.name: member for member in archive.getmembers()
                   if member.isfile() or member.issym() or member.islnk()}
        archived_files = {name.removeprefix(archived_root + "/"): member
                          for name, member in members.items()
                          if name.startswith(archived_root + "/")}
        if set(archived_files) != set(source_files):
            raise ValueError(f"archive file set differs from source case: {case_name}")
        for relative, source in source_files.items():
            member = archived_files[relative]
            if source.is_symlink():
                if not (member.issym() or member.islnk()) or member.linkname != os.readlink(source):
                    raise ValueError(f"archive symlink differs from work case: {case_name}/{relative}")
                continue
            if not member.isfile():
                raise ValueError(f"archive file type differs from work case: {case_name}/{relative}")
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f"unreadable archive member: {case_name}/{relative}")
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1 << 20), b""):
                digest.update(chunk)
            if digest.hexdigest() != sha256(source):
                raise ValueError(f"archive member differs from work case: {case_name}/{relative}")
    return json.loads((case_path / "diagnostics.json").read_text()), archive_path


def v13_archive_path(case_name, temp_root):
    if case_name in {"n64-dt0.0005", "n64-dt0.00025"}:
        archive_path = V13_ADDENDUM / f"{case_name}.tar.gz"
    elif case_name == "n128-dt0.001":
        parts_path = ROOT / "evidence/of13-high-gradient-v2/n128-dt0.001.tar.zst.parts.json"
        metadata = json.loads(parts_path.read_text())
        zstd_path = Path(temp_root) / metadata["archive"]
        digest = hashlib.sha256()
        size = 0
        with zstd_path.open("wb") as output:
            for part in metadata["parts"]:
                part_path = parts_path.parent / part["path"]
                if part_path.stat().st_size != part["bytes"] or sha256(part_path) != part["sha256"]:
                    raise ValueError(f"Foundation 13 n128 part failed integrity: {part_path}")
                with part_path.open("rb") as source:
                    for chunk in iter(lambda: source.read(1 << 20), b""):
                        output.write(chunk)
                        digest.update(chunk)
                        size += len(chunk)
        if size != metadata["archive_bytes"] or digest.hexdigest() != metadata["archive_sha256"]:
            raise ValueError("Foundation 13 n128 Zstandard archive failed reassembly check")
        current = json.loads(V13_INDEX.read_text())
        expected_hash = next(row["archive_sha256"] for row in current["completed_cases"]
                             if row["case"] == case_name)
        archive_path = Path(temp_root) / "n128-of13-dt0.001.tar.gz"
        if archive_path.exists():
            if sha256(archive_path) != expected_hash:
                raise ValueError("existing temporary Foundation 13 n128 tar has an unexpected hash")
        else:
            subprocess.run(["zstd", "-d", str(zstd_path), "-o", str(archive_path)],
                           check=True, capture_output=True, text=True)
        if sha256(archive_path) != expected_hash:
            raise ValueError("Foundation 13 n128 decompressed tar hash mismatch")
    else:
        archive_path = ROOT / "evidence/of13-high-gradient-v2" / f"{case_name}.tar.gz"
    return archive_path


def v13_diagnostics(case_name, temp_root):
    archive_path = v13_archive_path(case_name, temp_root)
    with tarfile.open(archive_path, "r:gz") as archive:
        member = next(item for item in archive.getmembers()
                      if item.isfile() and item.name.endswith("/diagnostics.json"))
        return json.load(archive.extractfile(member))


def normalized_endpoint_field_hashes(archive_path, case_name, version):
    normalized = {}
    with tarfile.open(archive_path, "r:gz") as archive:
        for field in ("U", "p", "C", "phi"):
            suffix = f"{case_name}/0.05/{field}"
            member = next(item for item in archive.getmembers()
                          if item.isfile() and item.name.endswith(suffix))
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f"cannot read endpoint field {suffix}")
            header = stream.read(4096)
            marker = b"Version:  " + str(version).encode("ascii")
            if header.count(marker) != 1:
                raise ValueError(f"expected one version-{version} banner in {suffix}")
            header = header.replace(marker, b"Version:  XX", 1)
            digest = hashlib.sha256(header)
            for chunk in iter(lambda: stream.read(1 << 20), b""):
                digest.update(chunk)
            normalized[field] = digest.hexdigest()
    return normalized


def verify_attempt_archive(item):
    source = RUN_ROOT / item["path"]
    archive_path = EVIDENCE / item["evidence_archive"]
    if sha256(archive_path) != item["evidence_archive_sha256"]:
        raise ValueError(f"preserved attempt archive hash mismatch: {archive_path}")
    complete = item["status"] == "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION"
    if complete:
        paths = [path for path in source.rglob("*") if path.is_file() or path.is_symlink()]
    else:
        paths = []
        for folder in ("0", "system", "constant"):
            base = source / folder
            if base.is_dir():
                paths.extend(path for path in base.rglob("*") if path.is_file() or path.is_symlink())
        for filename in ("parameters.json", "input-hashes.json", "command.json", "exit.json",
                         "log.container", "log.blockMesh", "log.foamRun", "log.centres"):
            path = source / filename
            if path.is_file():
                paths.append(path)
    expected = {f"{source.name}/{path.relative_to(source)}": path for path in set(paths)}
    with tarfile.open(archive_path, "r:gz") as archive:
        members = {member.name: member for member in archive.getmembers()
                   if member.isfile() or member.issym() or member.islnk()}
        if set(members) != set(expected):
            raise ValueError(f"preserved attempt archive member set differs: {archive_path}")
        for name, path in expected.items():
            member = members[name]
            if path.is_symlink():
                if not (member.issym() or member.islnk()) or member.linkname != os.readlink(path):
                    raise ValueError(f"preserved attempt symlink differs: {archive_path}:{name}")
                continue
            digest = hashlib.sha256()
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f"unreadable preserved attempt member: {archive_path}:{name}")
            for chunk in iter(lambda: stream.read(1 << 20), b""):
                digest.update(chunk)
            if digest.hexdigest() != sha256(path):
                raise ValueError(f"preserved attempt member differs: {archive_path}:{name}")


def verify_matrix():
    protocol = json.loads(PROTOCOL.read_text())
    manifest = json.loads((EVIDENCE / "manifest.json").read_text())
    if manifest.get("matrix_status") != "COMPLETE":
        raise ValueError(f"matrix is not complete: {manifest.get('matrix_status')}")
    if sha256(PROTOCOL) != manifest["protocol_sha256"]:
        raise ValueError("protocol hash differs from the frozen run manifest")
    if manifest["expected_cases"] != expected_cases(protocol):
        raise ValueError("manifest case list differs from the frozen protocol")
    rows = {item["case"]: item for item in manifest["completed_cases"]}
    if set(rows) != set(manifest["expected_cases"]):
        raise ValueError("manifest does not contain exactly one completion row per case")

    case_results = []
    with tempfile.TemporaryDirectory(prefix="cans-of14-verify-") as temp_root:
        for name in manifest["expected_cases"]:
            of14, of14_archive = verify_case_archive(name, rows[name], temp_root)
            of13 = v13_diagnostics(name, temp_root)
            of13_archive = v13_archive_path(name, temp_root)
            differences = {metric: of14[metric] - of13[metric] for metric in METRICS}
            metrics_identical = all(of14[metric] == of13[metric] for metric in METRICS)
            v13_fields = normalized_endpoint_field_hashes(of13_archive, name, 13)
            v14_fields = normalized_endpoint_field_hashes(of14_archive, name, 14)
            fields_identical = v13_fields == v14_fields
            case_results.append({
                "case": name,
                "standard_acceptance_of13_of14": [
                    of13["standard_acceptance"]["status"],
                    of14["standard_acceptance"]["status"],
                ],
                "local_quality_of13_of14": [
                    of13.get("local_quality", {}).get("status", "UNCERTAIN"),
                    of14.get("local_quality", {}).get("status", "UNCERTAIN"),
                ],
                "metric_differences_of14_minus_of13": differences,
                "stored_metrics_exactly_equal": metrics_identical,
                "endpoint_field_hashes_equal_after_version_banner_normalization": fields_identical,
                "endpoint_fields_normalized_sha256": v14_fields,
            })

        replay_checks = [item for item in manifest.get("attempt_history", [])
                         if item.get("status") == "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION"]
        for item in replay_checks:
            computed = compare_completed_replay(
                RUN_ROOT / item["path"], RUN_ROOT / item["case"]
            )
            if computed["status"] != "PASS" or computed != item["replay_comparison"]:
                raise ValueError(f"preserved replay comparison mismatch: {item['case']}")
        for item in manifest.get("attempt_history", []):
            verify_attempt_archive(item)

        partial = next((item for item in manifest.get("attempt_history", [])
                        if item["case"] == "n128-dt0.001"
                        and item["status"] in {
                            "INCOMPLETE_PRIOR_ATTEMPT_PRESERVED",
                            "INCOMPLETE_PRESERVED_BEFORE_RETRY",
                        }), None)
        partial_actual_steps = None
        if partial:
            log = RUN_ROOT / partial["path"] / "log.foamRun"
            partial_actual_steps = sum(1 for line in log.read_text(errors="replace").splitlines()
                                       if line.startswith("Time = "))
            if partial.get("observed_steps") != partial_actual_steps:
                raise ValueError("preserved partial attempt step count differs from its line-anchored log recount")

    result = {
        "status": "PASS",
        "protocol_sha256": sha256(PROTOCOL),
        "matrix_manifest_sha256": sha256(EVIDENCE / "manifest.json"),
        "case_count": len(case_results),
        "cases": case_results,
        "preserved_complete_replay_count": len(replay_checks),
        "preserved_attempt_archives_verified": len(manifest.get("attempt_history", [])),
        "initial_n128_interrupted_attempt": {
            "recorded_step_count": partial.get("observed_steps") if partial else None,
            "line_anchored_step_count": partial_actual_steps,
            "exit": partial.get("prior_exit") if partial else None,
        },
        "scope": "Archive-to-work byte replay, pinned package matrix completion, and comparison of stored diagnostic scalars only; no physical validation, continuum-extrema certificate, or solver-defect verdict.",
    }
    output = ROOT / "evidence/tests/openfoam-foundation14-matrix-verification-2026-10-02.json"
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(verify_matrix(), indent=2, allow_nan=False))
