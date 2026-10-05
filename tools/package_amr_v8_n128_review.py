"""Build compact, hash-verified review evidence from the completed n=128 run."""

import hashlib
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v8-n128"
CASE = ROOT / "work/of13-amr-same-run-map-v8-n128/amr-n128-cap7000000"
RAW = EVIDENCE / "amr-stage-snapshot-n128.tar.gz"
FULL_RECOVERY = ROOT / "work/of13-amr-same-run-map-v8-n128/archive-recovery/amr-stage-snapshot-n128-full.tar.gz"
REVIEW = EVIDENCE / "amr-stage-snapshot-n128-review.tar.gz"


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    manifest_path = EVIDENCE / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if sha(RAW) != manifest["archive_sha256"]:
        raise ValueError("full as-run archive does not match immutable run manifest")
    FULL_RECOVERY.parent.mkdir(parents=True, exist_ok=True)
    if not FULL_RECOVERY.exists():
        shutil.copy2(RAW, FULL_RECOVERY)
    if sha(FULL_RECOVERY) != manifest["archive_sha256"]:
        raise ValueError("full recovery copy hash mismatch")
    if REVIEW.exists():
        raise FileExistsError(REVIEW)

    included = {
        "postProcessing/amrStages/0.002/preMap_cells.csv",
        "postProcessing/amrStages/0.002/mapped_cells.csv",
        "postProcessing/amrStages/0.002/mapped_faces.csv",
    }
    with tarfile.open(REVIEW, "w:gz", compresslevel=6) as archive:
        for path in sorted(CASE.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(CASE).as_posix()
            if (relative in included or relative.startswith("0/") or
                    relative.startswith("constant/") or relative.startswith("system/") or
                    relative in {"log.foamRun", "log.container", "exit.json", "parameters.json"}):
                archive.add(path, arcname=f"{CASE.name}/{relative}")

    compressed = EVIDENCE / "amr-stage-snapshot-n128-review.tar.gz.zst"
    subprocess.run(["zstd", "-q", "-f", str(REVIEW), "-o", str(compressed)], check=True)
    part_size = 78_643_200
    parts = []
    with compressed.open("rb") as source:
        index = 0
        while block := source.read(part_size):
            part = EVIDENCE / f"{compressed.name}.part-{index:02d}"
            part.write_bytes(block)
            parts.append({"path": part.name, "bytes": part.stat().st_size, "sha256": sha(part)})
            index += 1
    parts_manifest = {
        "format": "zstandard-compressed compact AMR review tarball split into GitHub-compatible parts",
        "archive": compressed.name,
        "archive_bytes": compressed.stat().st_size,
        "archive_sha256": sha(compressed),
        "source_tar_gz": REVIEW.name,
        "source_tar_gz_sha256": sha(REVIEW),
        "source_tar_gz_bytes": REVIEW.stat().st_size,
        "parts": parts,
        "reassemble": f"cat {compressed.name}.part-* > {compressed.name}",
        "decompress": f"zstd -d {compressed.name} -o {REVIEW.name}",
    }
    parts_path = EVIDENCE / f"{compressed.name}.parts.json"
    parts_path.write_text(json.dumps(parts_manifest, indent=2) + "\n")
    package = {
        "version": "high-gradient-of13-amr-same-run-map-v8-n128-package-a1",
        "scope": "Post-run publication packaging only; solver inputs, run protocol, solver execution, and acceptance criteria are unchanged.",
        "run_protocol": manifest["protocol"],
        "run_protocol_sha256": manifest["protocol_sha256"],
        "archive": str(REVIEW.relative_to(ROOT)),
        "archive_sha256": sha(REVIEW),
        "archive_bytes": REVIEW.stat().st_size,
        "split_zstandard_manifest": str(parts_path.relative_to(ROOT)),
        "split_zstandard_manifest_sha256": sha(parts_path),
        "included": ["preMap cells at t=0.002", "mapped cells at t=0.002", "mapped internal faces at t=0.002", "case inputs and solver logs"],
        "excluded": ["preMap face snapshot", "all t=0.003 PIMPLE stage snapshots", "generated polyMesh and dynamicCode files; time directories containing native fields are omitted"],
        "full_as_run_archive": {"path": str(FULL_RECOVERY.relative_to(ROOT)), "bytes": FULL_RECOVERY.stat().st_size, "sha256": sha(FULL_RECOVERY), "public": False},
        "reconstruction": f"python3 -m tools.reconstruct_amr_published_archive {parts_path.relative_to(ROOT)} work/of13-amr-same-run-map-v8-n128/reconstructed-review.tar.gz",
        "limits": ["The compact archive supports replay of same-run parent injection and mapped-face Gauss-gradient/vorticity diagnostics.", "Later PIMPLE stage numerical comparisons are not published from this compact package.", "The full archive and raw case remain under ignored work/; the original as-run archive hash remains in manifest.json."],
    }
    (EVIDENCE / "package-a1.json").write_text(json.dumps(package, indent=2) + "\n")
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    RAW.unlink()
    REVIEW.unlink()
    print(json.dumps({"full_archive_recovery": str(FULL_RECOVERY), "parts": len(parts), "parts_manifest": str(parts_path), "package": str(EVIDENCE / 'package-a1.json')}, indent=2))


if __name__ == "__main__":
    main()
