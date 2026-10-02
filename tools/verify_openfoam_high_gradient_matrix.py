"""Independently replay the current six-case OpenFOAM matrix index from archives."""

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path

from tools.high_gradient_acceptance import local_quality, matrix_reproduction, standard_acceptance


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json"
PROTOCOL = ROOT / "protocols/high-gradient-of13-v2.json"
BASE_MANIFEST = ROOT / "evidence/of13-high-gradient-v2/manifest.json"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _n128_archive(entry, temporary_directory):
    package = ROOT / "evidence/of13-high-gradient-v2/n128-dt0.001.tar.zst.parts.json"
    metadata = json.loads(package.read_text())
    zst_path = Path(temporary_directory) / metadata["archive"]
    digest = hashlib.sha256()
    with zst_path.open("wb") as output:
        for part in metadata["parts"]:
            path = package.parent / part["path"]
            if path.stat().st_size != part["bytes"] or sha256_file(path) != part["sha256"]:
                raise ValueError(f"n=128 package part failed integrity check: {path}")
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1 << 20), b""):
                    digest.update(chunk)
                    output.write(chunk)
    if zst_path.stat().st_size != metadata["archive_bytes"]:
        raise ValueError("n=128 concatenated Zstandard size mismatch")
    if digest.hexdigest() != metadata["archive_sha256"]:
        raise ValueError("n=128 concatenated Zstandard checksum mismatch")
    tar_path = Path(temporary_directory) / "n128-dt0.001.tar.gz"
    subprocess.run(["zstd", "-d", str(zst_path), "-o", str(tar_path)],
                   check=True, capture_output=True, text=True)
    if sha256_file(tar_path) != entry["archive_sha256"]:
        raise ValueError("reconstructed n=128 gzip tar checksum mismatch")
    return tar_path


def _archive_path(entry, temporary_directory):
    archive_text = entry["archive"].split(" (", 1)[0]
    candidate = ROOT / archive_text
    if candidate.is_file():
        return candidate
    base_candidate = ROOT / "evidence/of13-high-gradient-v2" / Path(archive_text).name
    if base_candidate.is_file():
        return base_candidate
    if entry["case"] == "n128-dt0.001":
        return _n128_archive(entry, temporary_directory)
    raise FileNotFoundError(candidate)


def verify_matrix():
    index_bytes = INDEX.read_bytes()
    index = json.loads(index_bytes)
    protocol_bytes = PROTOCOL.read_bytes()
    base_manifest_bytes = BASE_MANIFEST.read_bytes()
    if sha256_bytes(protocol_bytes) != index["protocol_sha256"]:
        raise ValueError("frozen v2 protocol hash does not match current matrix index")
    if sha256_bytes(base_manifest_bytes) != index["base_run_manifest_sha256"]:
        raise ValueError("immutable base run manifest hash mismatch")
    protocol = json.loads(protocol_bytes)
    if index["status"] != "COMPLETE":
        raise ValueError(f"matrix index is not complete: {index['status']}")
    expected = set(index["expected_cases"])
    entries = index["completed_cases"]
    names = [entry["case"] for entry in entries]
    if set(names) != expected or len(names) != len(expected):
        raise ValueError("current index does not contain exactly one row per expected case")
    if index.get("incomplete_cases") != []:
        raise ValueError("current index contains incomplete cases")

    reproduced = []
    with tempfile.TemporaryDirectory(prefix="cans-openfoam-matrix-") as temp:
        for entry in entries:
            archive_path = _archive_path(entry, temp)
            if sha256_file(archive_path) != entry["archive_sha256"]:
                raise ValueError(f"archive checksum mismatch: {entry['case']}")
            with tarfile.open(archive_path, "r:gz") as archive:
                members = {member.name: member for member in archive.getmembers() if member.isfile()}
                root = entry["case"]
                required = [f"{root}/log.foamRun", f"{root}/system/fvSolution",
                            f"{root}/diagnostics.json"]
                end = f"{protocol['end_time']:g}"
                required.extend(f"{root}/{end}/{field}" for field in ("U", "p", "C", "phi"))
                absent = [name for name in required if name not in members]
                if absent:
                    raise ValueError(f"required archive files missing for {root}: {absent}")

                def read(name):
                    stream = archive.extractfile(members[name])
                    if stream is None:
                        raise ValueError(f"cannot read archive member {name}")
                    return stream.read()

                log_bytes = read(f"{root}/log.foamRun")
                source_log_hash = entry.get("log_sha256", entry.get("source_log_sha256"))
                if source_log_hash and sha256_bytes(log_bytes) != source_log_hash:
                    raise ValueError(f"solver log hash mismatch: {entry['case']}")
                diagnostics = json.loads(read(f"{root}/diagnostics.json"))
                dt = float(diagnostics["parameters"]["dt"])
                expected_n = int(root.split("-", 1)[0][1:])
                expected_dt = float(root.rsplit("dt", 1)[1])
                if (diagnostics["parameters"].get("n") != expected_n
                        or dt != expected_dt):
                    raise ValueError(f"case parameters disagree with archive row name: {root}")
                acceptance = standard_acceptance(
                    log_bytes.decode(errors="replace"), protocol["end_time"], dt,
                    protocol["standard_acceptance"]["outer_corrector_residual_absolute"],
                    protocol["standard_acceptance"]["maximum_outer_correctors"],
                    read(f"{root}/system/fvSolution").decode(errors="replace"),
                )
                metrics = {
                    "velocity_l2": diagnostics["velocity_relative_l2"],
                    "energy": diagnostics["energy_relative_error_cell_samples"],
                    "max_gradient": diagnostics["gradient_peak_relative_error_cell_samples"],
                    "max_vorticity": diagnostics["vorticity_peak_relative_error_cell_samples"],
                    "shell_spectrum": diagnostics["shell_spectrum_relative_l1_error"],
                }
                quality = local_quality(metrics, protocol["local_quality_relative_error_thresholds"])
                if (entry.get("time_steps", acceptance["observed_time_steps"])
                        != acceptance["observed_time_steps"]):
                    raise ValueError(f"index timestep count mismatch for {entry['case']}")
                if (entry.get("converged_steps", acceptance["pimple_convergence_records"])
                        != acceptance["pimple_convergence_records"]):
                    raise ValueError(f"index convergence count mismatch for {entry['case']}")
                if acceptance["status"] != entry["standard_acceptance"]:
                    raise ValueError(f"standard gate mismatch for {entry['case']}")
                if quality["status"] != entry["local_quality"]:
                    raise ValueError(f"local-quality gate mismatch for {entry['case']}")
                if diagnostics.get("standard_acceptance", {}).get("status") != acceptance["status"]:
                    raise ValueError(f"embedded diagnostic gate mismatch for {entry['case']}")
                if diagnostics.get("quality") != quality["status"]:
                    raise ValueError(f"embedded local-quality mismatch for {entry['case']}")
                reproduced.append({
                    "case": entry["case"],
                    "archive_sha256": entry["archive_sha256"],
                    "observed_steps": acceptance["observed_time_steps"],
                    "standard_acceptance": acceptance["status"],
                    "local_quality": quality["status"],
                    "endpoint_fields_present": True,
                })

    matrix = matrix_reproduction([
        {"parameters": {"n": int(case["case"].split("-")[0][1:]),
                         "dt": 0.001},
         "standard_acceptance": {"status": case["standard_acceptance"]},
         "local_quality": {"status": case["local_quality"]}}
        for case in reproduced if case["case"].endswith("dt0.001")
    ])
    if matrix["status"] != index["matrix_reproduction"]["status"]:
        raise ValueError("replayed matrix-reproduction verdict differs from index")
    return {
        "status": "PASS",
        "index_sha256": sha256_bytes(index_bytes),
        "protocol_sha256": index["protocol_sha256"],
        "base_manifest_sha256": index["base_run_manifest_sha256"],
        "case_count": len(reproduced),
        "cases": reproduced,
        "matrix_reproduction": matrix["status"],
        "scope": "Archive integrity, stored diagnostics, PIMPLE log/config acceptance, local sampled quality gates, and the declared six-case index; not an independent solver-source proof or physical validation.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify_matrix()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        path = args.output if args.output.is_absolute() else ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
