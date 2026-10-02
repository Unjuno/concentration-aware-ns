"""Recheck fixed-step schedules in every complete archived high-gradient run."""
import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

from tools.high_gradient_acceptance import standard_acceptance


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_case(archive, case_name):
    with tarfile.open(archive, "r:gz") as tar:
        params = json.load(tar.extractfile(f"{case_name}/parameters.json"))
        log = tar.extractfile(f"{case_name}/log.foamRun").read().decode()
        config = tar.extractfile(f"{case_name}/system/fvSolution").read().decode()
    return params, log, config


def _reconstruct_zstd_parts(parts_manifest, destination):
    metadata = json.loads(Path(parts_manifest).read_text())
    archive_zst = destination / metadata["archive"]
    with archive_zst.open("wb") as output:
        for part in metadata["parts"]:
            path = Path(parts_manifest).parent / part["path"]
            if path.stat().st_size != part["bytes"] or sha256(path) != part["sha256"]:
                raise ValueError(f"archive part failed identity check: {path}")
            with path.open("rb") as source:
                shutil.copyfileobj(source, output)
    if archive_zst.stat().st_size != metadata["archive_bytes"]:
        raise ValueError("reassembled zstd archive size mismatch")
    if sha256(archive_zst) != metadata["archive_sha256"]:
        raise ValueError("reassembled zstd archive hash mismatch")
    zstd = shutil.which("zstd")
    if zstd is None:
        raise RuntimeError("zstd CLI is required to inspect the published split n=128 archive")
    archive_gz = destination / "n128-dt0.001.tar.gz"
    subprocess.run([zstd, "-d", "-q", "-f", str(archive_zst), "-o", str(archive_gz)], check=True)
    return archive_gz


def run(root=Path(".")):
    root = Path(root)
    manifest_path = root / "evidence/of13-high-gradient-v2/manifest.json"
    protocol_path = root / "protocols/high-gradient-of13-v2.json"
    manifest = json.loads(manifest_path.read_text())
    protocol = json.loads(protocol_path.read_text())
    acceptance = protocol["standard_acceptance"]
    rows = []
    with tempfile.TemporaryDirectory(prefix="cans-time-sequence-") as temp:
        temp = Path(temp)
        for case in manifest["completed_cases"]:
            name = case["case"]
            archive_field = case["archive"]
            if "reconstructed from zstd package" in archive_field:
                parts_manifest = root / "evidence/of13-high-gradient-v2" / case["publication_package"]
                archive = _reconstruct_zstd_parts(parts_manifest, temp)
            else:
                archive = root / "evidence/of13-high-gradient-v2" / archive_field
            actual_hash = sha256(archive)
            if actual_hash != case["archive_sha256"]:
                raise ValueError(f"case archive hash mismatch: {name}")
            params, log, config = _load_case(archive, name)
            result = standard_acceptance(
                log, params["end"], params["dt"],
                acceptance["outer_corrector_residual_absolute"],
                acceptance["maximum_outer_correctors"], config,
            )
            rows.append({
                "case": name,
                "archive_sha256": actual_hash,
                "standard_acceptance": result["status"],
                "time_sequence_matches_fixed_delta_t": result["time_sequence_matches_fixed_delta_t"],
                "time_sequence_mismatches_zero_based": result["time_sequence_mismatches_zero_based"],
                "observed_time_steps": result["observed_time_steps"],
                "expected_time_steps": result["expected_time_steps"],
            })
    success = bool(rows) and all(
        row["standard_acceptance"] == "PASS"
        and row["time_sequence_matches_fixed_delta_t"]
        and not row["time_sequence_mismatches_zero_based"]
        for row in rows
    )
    evidence = {
        "scope": "Archived OpenFOAM high-gradient v2 run-log schedule recheck only; no solver rerun and no accuracy verdict upgrade.",
        "manifest_sha256": sha256(manifest_path),
        "protocol_sha256": sha256(protocol_path),
        "cases": rows,
        "success": success,
    }
    output = root / "evidence/tests/high-gradient-time-sequence.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))
    return success


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
