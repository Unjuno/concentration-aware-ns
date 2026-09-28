"""Run the frozen six-case high-gradient OpenFOAM matrix once."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    protocol_path = Path("protocols/high-gradient-of13-v2.json")
    spec = json.loads(protocol_path.read_text())
    root = Path("work/of13-high-gradient-v2").resolve()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if dirty:
        raise RuntimeError("commit the run sources first so the recorded source revision is reproducible")
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    image_info = subprocess.run(
        ["docker", "image", "inspect", "concentration-aware-ns:of13",
         "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        capture_output=True, text=True, timeout=8, check=True,
    ).stdout.strip()
    image_id, image_platform = image_info.split(maxsplit=1)
    root.mkdir(parents=True, exist_ok=False)
    (root / "run-environment.json").write_text(json.dumps({
        "source_commit": source_commit,
        "container_image_id": image_id,
        "container_platform": image_platform,
        "protocol_sha256": sha256(protocol_path),
        "scope": "OpenFOAM Foundation 13 high-gradient uniform-grid matrix",
    }, indent=2) + "\n")

    spatial = spec["spatial_matrix"]
    temporal = spec["temporal_matrix"]
    matrix = [(n, spatial["delta_t"]) for n in spatial["cell_counts"]]
    matrix.extend((temporal["cell_count"], dt) for dt in temporal["delta_t"]
                  if (temporal["cell_count"], dt) not in matrix)
    cases = []
    for n, dt in matrix:
        case = root / f"n{n}-dt{dt:g}"
        generate(case, n=n, dt=dt, end=spec["end_time"], nu=spec["viscosity"],
                 profile="high-gradient", frequency=spec["frequency_N"])
        (case / "input-hashes.json").write_text(json.dumps({
            str(path.relative_to(case)): sha256(path)
            for path in sorted(case.rglob("*")) if path.is_file()
        }, indent=2) + "\n")
        command = [
            "docker", "run", "--rm", "--name", f"cans-hg-{case.name}",
            "--network", "none", "--entrypoint", "/bin/bash",
            "-v", f"{case}:/case", image_id, "-c",
            "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
            "\"source /opt/openfoam13/etc/bashrc && cd /case && "
            "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
            "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1\"",
            "--", str(os.getuid()),
        ]
        (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
        with (case / "log.container").open("w") as log:
            run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        (case / "exit.json").write_text(json.dumps({"exit_code": run.returncode}) + "\n")
        if run.returncode:
            raise RuntimeError(f"case {case.name} failed; preserve inputs and logs at {case}")
        result = analyze(case)
        (case / "diagnostics.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        cases.append(result)

    (root / "summary.json").write_text(json.dumps({
        "protocol": str(protocol_path),
        "cases": cases,
        "scope": "Diagnostics only; standard acceptance and continuous extrema remain UNCERTAIN.",
    }, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"completed": len(cases), "root": str(root)}, indent=2))


if __name__ == "__main__":
    main()
