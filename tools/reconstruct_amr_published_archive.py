"""Verify and reconstruct a split Zstandard AMR evidence archive."""

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def reconstruct(parts_manifest, output):
    parts_manifest = Path(parts_manifest).resolve()
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    metadata = json.loads(parts_manifest.read_text())
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cans-amr-reassemble-", dir=output.parent) as temp:
        compressed = Path(temp) / metadata["archive"]
        whole = hashlib.sha256()
        total = 0
        with compressed.open("wb") as destination:
            for item in metadata["parts"]:
                part = parts_manifest.parent / item["path"]
                if part.stat().st_size != item["bytes"] or sha256(part) != item["sha256"]:
                    raise ValueError(f"part integrity failure: {part}")
                with part.open("rb") as source:
                    for block in iter(lambda: source.read(1 << 20), b""):
                        destination.write(block)
                        whole.update(block)
                        total += len(block)
        if total != metadata["archive_bytes"] or whole.hexdigest() != metadata["archive_sha256"]:
            raise ValueError("reassembled Zstandard archive size or SHA-256 mismatch")
        # zstd prints the destination path on success. The destination is a
        # temporary file in replay use, so suppress that nondeterministic path
        # while leaving stderr available for actionable failures.
        command = ["zstd", "-d", str(compressed), "-o", str(output)]
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError as error:
            # Keep actionable decompressor diagnostics on failure, without
            # publishing successful temporary paths into replay logs.
            if error.stderr:
                sys.stderr.write(error.stderr)
            raise
    if output.stat().st_size != metadata["source_tar_gz_bytes"]:
        output.unlink(missing_ok=True)
        raise ValueError("decompressed tarball size mismatch")
    if sha256(output) != metadata["source_tar_gz_sha256"]:
        output.unlink(missing_ok=True)
        raise ValueError("decompressed tarball SHA-256 mismatch")
    return {
        "status": "PASS",
        "parts_manifest": str(parts_manifest),
        "output": str(output),
        "bytes": output.stat().st_size,
        "sha256": metadata["source_tar_gz_sha256"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parts_manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(reconstruct(args.parts_manifest, args.output), indent=2))
