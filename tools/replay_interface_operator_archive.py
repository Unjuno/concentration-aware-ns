"""Verify frozen operator evidence and replay its JSON analysis without binaries."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]
AUDIT = "evidence/upstream-refresh/openfoam-package-source-comparison-2026-10-03.json"
ANALYZER = "tools/analyze_interface_operator_probe.py"
GENERATOR = "tools/build_interface_operator_cases.py"
DEPENDENCY = "tools/check_interface_stress_compatibility.py"
SNAPSHOTS = ("arithmetic/before.json", "arithmetic/after.json", "harmonic/before.json",
             "harmonic/after.json", "constant/before.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    require(bool(path.parts) and not path.is_absolute() and ".." not in path.parts
            and path.as_posix() == name and "\\" not in name and "\x00" not in name,
            f"unsafe/noncanonical member path: {name}")
    return name


def git_blob(commit, name):
    safe_path(name)
    return subprocess.check_output(["git", "show", f"{commit}:{name}"],
                                   cwd=REPOSITORY, timeout=15, stderr=subprocess.PIPE)


def read_json(path):
    def reject(value):
        raise ValueError(f"nonstandard JSON number: {value}")
    return json.loads(path.read_bytes(), parse_constant=reject)


def unpack(archive_path, manifest, root):
    require(file_digest(archive_path) == manifest["archive"]["sha256"], "archive SHA256 mismatch")
    expected = manifest["work_files_sha256"]
    for name in expected:
        safe_path(name)
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        require(len(members) <= 20000 and sum(item.size for item in members) <= 512*1024*1024,
                "archive exceeds replay bounds")
        names = [safe_path(item.name) for item in members]
        require(all(item.isfile() and not item.issparse() for item in members), "archive has nonregular members")
        require(len(set(names)) == len(names) and set(names) == set(expected)
                and len(names) == manifest["archive"]["regular_file_count"], "archive member map differs")
        for member in members:
            data = archive.extractfile(member).read()
            require(digest(data) == expected[member.name], f"work file SHA256 mismatch: {member.name}")
            path = root/member.name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)


def checksum_rows(path):
    rows = {}
    for line in path.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})\s+(.+)", line)
        require(match is not None, f"malformed checksum row in {path.name}")
        value, name = match.groups()
        require(name not in rows, f"duplicate checksum path: {name}")
        rows[name] = value
    return rows


def package_provenance(root, head, protocol):
    supplied = checksum_rows(root/"package-source-sha256.log")
    linked = checksum_rows(root/"linked-library-sha256.log")
    paths = (root/"app/package-source-paths.txt").read_text().splitlines()
    require(len(paths) == 25 and len(set(paths)) == 25
            and set(supplied) == {"/opt/openfoam13/"+name for name in paths}, "wrong supplied source hash map")
    result = {"source_log": "package-source-sha256.log", "linked_log": "linked-library-sha256.log",
              "supplied_source_rows": supplied, "linked_library_rows": linked, "audit_path": AUDIT}
    try:
        raw = git_blob(head, AUDIT)
    except subprocess.CalledProcessError:
        result["comparison"] = "AUDIT_UNAVAILABLE_AT_NAMED_COMMIT"
        return result
    audit = json.loads(raw)
    require(audit["package_sha256"] == protocol["target"]["package_sha256"]
            and audit["inspected_source_commit"] == protocol["target"]["inspected_source_commit"], "audit target differs")
    comparisons = [{"path": row["path"], "expected_sha256": row["package_source_sha256"],
                    "runtime_sha256": supplied.get("/opt/openfoam13/"+row["path"])} for row in audit["files"]]
    libraries = [{"path": "/"+row["path"].removeprefix("./"), "expected_sha256": row["sha256"],
                  "runtime_sha256": linked.get("/"+row["path"].removeprefix("./"))}
                 for row in audit["linked_library_payloads"]]
    require(len(comparisons) == 25 and len(libraries) == 3
            and all(row["runtime_sha256"] == row["expected_sha256"] for row in comparisons+libraries),
            "supplied source or OpenFOAM linked library differs from named audit")
    require(all(row["path"] in (root/"linked-libraries.log").read_text() for row in libraries),
            "audited library is not present in actual ldd log")
    result.update(comparison="MATCH_SELECTED_PACKAGE_PAYLOADS", audit_sha256=digest(raw),
                  source_comparisons=comparisons, linked_library_comparisons=libraries)
    return result


def replay(evidence_root, source_commit=None):
    evidence_root = Path(evidence_root); manifest = read_json(evidence_root/"run-manifest.json")
    head = manifest["git_head"]
    require(re.fullmatch(r"[0-9a-f]{40}", head) and (source_commit is None or source_commit == head), "source commit mismatch")
    state, image = manifest["container_state"], manifest["image_inspect"]
    require(manifest["schema"] == "of13-interface-operator-run/v1"
            and manifest["status"] == "RUN_COMPLETE_OPERATOR_ONLY" and manifest["disposition"] == "COMPLETE"
            and manifest["tracked_status"].strip() == "" and manifest["docker_run_exit_code"] == 0
            and type(manifest["docker_run_exit_code"]) is int and type(state["ExitCode"]) is int
            and state["Status"] == "exited" and state["Running"] is False and state["ExitCode"] == 0,
            "runner integrity/state is incomplete")
    require(image["Os"] == "linux" and image["Architecture"] == "arm64"
            and re.fullmatch(r"sha256:[0-9a-f]{64}", image["Id"])
            and re.fullmatch(r"[0-9a-f]{64}", manifest["container_id"])
            and image["Id"] == manifest["resolved_image_id"] == manifest["container_image_id"], "image identity/platform mismatch")
    sources = manifest["source_files_sha256"]
    required = {ANALYZER, GENERATOR, "tools/run_interface_operator_probe.py", "runtime/of13-interface-operator/interfaceOperatorProbe.C",
                "runtime/of13-interface-operator/run_cases.sh", "runtime/of13-interface-operator/package-source-paths.txt",
                "runtime/of13-interface-operator/Make/files", "runtime/of13-interface-operator/Make/options"}
    require(required.issubset(sources), "missing frozen harness source hashes")
    for name, value in sources.items():
        require(digest(git_blob(head, name)) == value, f"Git source blob SHA256 mismatch: {name}")
    for name in (ANALYZER, GENERATOR, DEPENDENCY):
        require(digest((REPOSITORY/name).read_bytes()) == digest(git_blob(head,name)), f"current replay code differs: {name}")
    with tempfile.TemporaryDirectory(prefix="of13-interface-replay-") as directory:
        root = Path(directory)/"raw"; root.mkdir()
        unpack(evidence_root/"raw.tar.gz", manifest, root)
        for name, value in sources.items():
            if name.startswith("runtime/of13-interface-operator/"):
                copied = root/"app"/name.removeprefix("runtime/of13-interface-operator/")
                require(digest(copied.read_bytes()) == value, f"archived utility source mismatch: {name}")
        commands = {row["label"]:row for row in manifest["commands"]}
        command = read_json(root/"container-command.json")
        require(commands["container-run"]["return_code"] == 0
                and commands["container-run"]["argv"] == command and "--rm" not in command
                and "--pull=never" in command and image["Id"] in command, "run command mismatch")
        for option, value in (("--network","none"),("--cpus","2"),("--memory","2g"),
                              ("--pids-limit","512"),("--platform","linux/arm64"),("--entrypoint","/bin/bash")):
            require(option in command and command[command.index(option)+1] == value, "run resource/entrypoint mismatch")
        observed = read_json(root/safe_path(commands["container-inspect"]["stdout_file"]))[0]
        require(observed["Id"] == manifest["container_id"] and observed["Image"] == image["Id"]
                and observed["State"] == state, "saved engine container state mismatch")
        require(read_json(root/safe_path(commands["image-inspect"]["stdout_file"])) == [image], "saved engine image inspection mismatch")
        protocol = read_json(root/"protocol-frozen.json")
        require(digest((root/"protocol-frozen.json").read_bytes()) == manifest["protocol"]["sha256"]
                == digest(git_blob(head,manifest["protocol"]["path"]))
                and protocol == manifest["protocol"]["content"], "frozen protocol mismatch")
        require(protocol["inputs"] == {"nx":[16,32,64], "ny":2, "nz":2, "mu_left":1, "mu_right":100, "traction":1, "density":1}, "unexpected protocol inputs")
        require(protocol["target"]["runtime_recipe"] in sources, "missing frozen runtime recipe hash")
        require(set(manifest["runtime_logs_sha256"]) == {"runtime-environment.log","package-inventory.log","linked-libraries.log",
                "binary-sha256.txt","build.log","package-source-sha256.log","linked-library-sha256.log"}, "runtime log map differs")
        for name, value in manifest["runtime_logs_sha256"].items():
            require(digest((root/safe_path(name)).read_bytes()) == value, f"runtime log mismatch: {name}")
        require(digest((root/"interfaceOperatorProbe").read_bytes()) == manifest["utility_binary_sha256"], "binary SHA256 mismatch")
        require(checksum_rows(root/"binary-sha256.txt") == {"/probe/interfaceOperatorProbe":manifest["utility_binary_sha256"]}, "binary log mismatch")
        require((root/"COMPLETED").read_text().strip() == "RUN_CASES_COMPLETE"
                and (root/"container-id").read_text().strip() == manifest["container_id"], "completion/container marker mismatch")
        from tools.build_interface_operator_cases import build_cases
        from tools.analyze_interface_operator_probe import analyze_case
        regenerated = Path(directory)/"regenerated"; build_cases(regenerated)
        require(set(manifest["case_input_hashes"]) == {"nx16","nx32","nx64"}, "wrong case matrix")
        cases = []
        for nx in (16,32,64):
            case_name = f"nx{nx}"; case = root/"cases"/case_name; generated = regenerated/case_name
            metadata = read_json(generated/"case_metadata.json"); record = manifest["case_input_hashes"][case_name]
            require(record["inputs_sha256"] == metadata["inputs_sha256"] and record["files_sha256"] == metadata["files_sha256"]
                    and record["metadata_sha256"] == digest((case/"case_metadata.json").read_bytes())
                    == digest((generated/"case_metadata.json").read_bytes()), "generated metadata/hash mismatch")
            for name, value in metadata["files_sha256"].items():
                require(digest((case/name).read_bytes()) == value, f"generated case input mismatch: {case_name}/{name}")
            require((case/"log.interfaceOperatorProbe").read_text().rstrip().endswith("INTERFACE_OPERATOR_PROBE_COMPLETE"), "case end marker missing")
            for name in SNAPSHOTS:
                read_json(case/"probe"/name)
            cases.append(analyze_case(case, protocol))
        provenance = package_provenance(root, head, protocol)
    return {"status":"REPLAY_COMPLETE_OPERATOR_ONLY", "integrity":"VERIFIED_ARCHIVE_AND_FROZEN_INPUTS", "git_head":head,
            "archive_sha256":manifest["archive"]["sha256"], "cases":cases, "package_provenance":provenance,
            "operator_quality":"PASS" if all(row["operator_quality"] == "PASS" for row in cases) else "FAIL_SPECIFIED_OPERATOR_GATE",
            "native_diagnostic":{str(row["nx"]):row["constant_control"]["source_predicted_extra_cyclic_term"] for row in cases}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit"); args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        parser.error("refusing to overwrite existing output")
    try:
        result = replay(args.evidence_root, args.source_commit)
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError, tarfile.TarError) as error:
        result = {"status":"STOP_INTEGRITY", "operator_quality":"NOT_ASSESSED", "reason":str(error)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False); stream.write("\n")
    print(json.dumps({key:result[key] for key in ("status","operator_quality")}))
    return 2 if result["status"] == "STOP_INTEGRITY" else (0 if result["operator_quality"] == "PASS" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
