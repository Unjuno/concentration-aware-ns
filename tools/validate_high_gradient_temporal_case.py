"""Validate, analyze, and archive a preserved single temporal OpenFOAM case."""
import argparse
import hashlib
import json
import os
import re
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.archive_high_gradient_openfoam import completion_check


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_and_archive(root):
    root = Path(root).expanduser().resolve()
    environment_path = root / "run-environment.json"
    environment = json.loads(environment_path.read_text())
    protocol_path = Path(environment["protocol"])
    spec = json.loads(protocol_path.read_text())
    if sha256(protocol_path) != environment["protocol_sha256"]:
        raise ValueError("frozen protocol hash mismatch")
    parent_manifest = Path("evidence/of13-high-gradient-v2/manifest.json")
    if sha256(parent_manifest) != environment["parent_matrix_manifest_sha256"]:
        raise ValueError("parent matrix manifest changed since this run")

    cases = [path for path in root.iterdir() if path.is_dir() and path.name.startswith("n64-dt")]
    if len(cases) != 1:
        raise ValueError(f"expected exactly one n64 temporal case directory; found {len(cases)}")
    case = cases[0]
    input_hashes = json.loads((case / "input-hashes.json").read_text())
    for relative, expected_hash in input_hashes.items():
        path = case / relative
        if not path.is_file() or sha256(path) != expected_hash:
            raise ValueError(f"frozen input hash mismatch: {relative}")
    dt = float(json.loads((case / "parameters.json").read_text())["dt"])
    if dt not in (0.0005, 0.00025):
        raise ValueError(f"unexpected temporal step: {dt}")

    diagnostics_path = case / "diagnostics.json"
    if not diagnostics_path.exists():
        diagnostics = analyze(case, spec)
        diagnostics_path.write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
    result = completion_check(case, spec["end_time"])
    if result is None:
        log = (case / "log.foamRun").read_text(errors="replace")
        raise RuntimeError(json.dumps({
            "exit_code": json.loads((case / "exit.json").read_text()).get("exit_code"),
            "time_steps": len(re.findall(r"^Time = ", log, re.MULTILINE)),
            "expected_steps": round(spec["end_time"] / dt),
            "converged_steps": log.count("PIMPLE: Converged in"),
            "end_marker": log.rstrip().endswith("End"),
            "endpoint_fields": {name: (case / f"{spec['end_time']:g}" / name).is_file()
                                for name in ("U", "p", "C", "phi")},
        }, indent=2))

    archive = root / f"{case.name}.tar.gz"
    temporary = archive.with_suffix(".tar.gz.tmp")
    temporary.unlink(missing_ok=True)
    with tarfile.open(temporary, "w:gz") as tar:
        tar.add(case, arcname=case.name)
    with tarfile.open(temporary, "r:gz") as tar:
        members = {member.name: member for member in tar.getmembers()
                   if member.isfile() or member.issym() or member.islnk()}
        expected_paths = [path for path in case.rglob("*")
                          if path.is_file() or path.is_symlink()]
        if len(members) != len(expected_paths):
            temporary.unlink(missing_ok=True)
            raise RuntimeError("archive member count does not match the completed case")
        for path in expected_paths:
            name = f"{case.name}/{path.relative_to(case)}"
            member = members.get(name)
            if member is None:
                temporary.unlink(missing_ok=True)
                raise RuntimeError(f"archive member missing: {name}")
            if path.is_symlink():
                if not (member.issym() or member.islnk()) or member.linkname != os.readlink(path):
                    temporary.unlink(missing_ok=True)
                    raise RuntimeError(f"archive symlink verification failed: {name}")
            else:
                stream = tar.extractfile(member)
                if not member.isfile() or stream is None or hashlib.sha256(stream.read()).hexdigest() != sha256(path):
                    temporary.unlink(missing_ok=True)
                    raise RuntimeError(f"archive content verification failed: {name}")
    temporary.replace(archive)

    manifest = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "matrix_status": "SINGLE_CASE_COMPLETE_NOT_FULL_MATRIX",
        "case": case.name,
        "complete": True,
        "time_steps": result["time_steps"],
        "converged_steps": result["converged_steps"],
        "end_marker": True,
        "endpoint_fields": ["U", "p", "C", "phi"],
        "standard_acceptance": result["diagnostics"]["standard_acceptance"]["status"],
        "local_quality": result["diagnostics"].get("local_quality", {}).get("status", "UNCERTAIN"),
        "archive": archive.name,
        "archive_sha256": sha256(archive),
        "source_log_sha256": sha256(case / "log.foamRun"),
        "run_environment": "run-environment.json",
        "scope": "One frozen temporal row only; does not complete or independently validate the six-case matrix.",
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(validate_and_archive(args.run_root), indent=2))


if __name__ == "__main__":
    main()
