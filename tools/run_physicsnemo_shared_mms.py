"""Run and archive the preregistered shared-MMS PhysicsNeMo model matrix."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile


def main():
    protocol_path = Path("protocols/physicsnemo-shared-high-gradient-v1.json")
    protocol = json.loads(protocol_path.read_text())
    work = Path("work/physicsnemo-shared-high-gradient-v1")
    evidence = Path("evidence/physicsnemo-shared-high-gradient-v1")
    work.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=False)
    rows = []
    cases = protocol["cases"]["unique_case_pairs"]
    seeds = protocol["cases"]["seeds"]
    expected = len(cases) * len(seeds)
    (evidence / "protocol.json").write_bytes(protocol_path.read_bytes())
    for seed in seeds:
        for n, time_nodes in cases:
            name = f"seed{seed}-n{n}-nt{time_nodes}"
            config = work / f"{name}.json"
            case_dir = work / name
            config.write_text(json.dumps({**protocol, "_case": [n, time_nodes], "_seed": seed}, indent=2) + "\n")
            command = [sys.executable, "-m", "tools.train_physicsnemo_shared_mms",
                       "--protocol", str(config), "--output", str(case_dir)]
            print("START", name, flush=True)
            with (work / f"{name}.log").open("w") as log:
                completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
            if completed.returncode:
                raise RuntimeError(f"{name} failed with exit {completed.returncode}; logs preserved")
            (case_dir / "command.json").write_text(json.dumps(command) + "\n")
            (case_dir / "console.log").write_bytes((work / f"{name}.log").read_bytes())
            archive = evidence / f"{name}.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                for path in sorted(case_dir.iterdir()):
                    tar.add(path, arcname=path.name)
            diagnostics = json.loads((case_dir / "diagnostics.json").read_text())
            rows.append({"seed": seed, "case": f"n{n}-nt{time_nodes}",
                         "sampled_quality": diagnostics["sampled_quality"],
                         "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest()})
            summary = {"study_id": protocol["study_id"], "expected_models": expected,
                       "completed_models": len(rows),
                       "status": "COMPLETE" if len(rows) == expected else "INCOMPLETE",
                       "continuous_local_quality": "UNCERTAIN", "runs": rows}
            (evidence / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
            print("END", name, diagnostics["sampled_quality"], flush=True)


if __name__ == "__main__":
    main()
