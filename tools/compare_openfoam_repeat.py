"""Compare two completed archives of the same frozen OpenFOAM case."""
import argparse
import hashlib
import json
import re
import tarfile
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def members(path, case):
    with tarfile.open(path, "r:gz") as archive:
        result = {}
        prefix = case + "/"
        for member in archive.getmembers():
            if member.isfile() and member.name.startswith(prefix):
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"cannot read archive member {member.name}")
                result[member.name[len(prefix):]] = stream.read()
    return result


def json_bytes(files, name):
    return json.loads(files[name])


def normalize_log(data):
    lines = data.decode(errors="replace").splitlines()
    patterns = (
        (r"^(Date|Time|Host)\s*:.*$", r"\1: <runtime>"),
        (r"^PID\s*:.*$", "PID    : <runtime>"),
        (r"ExecutionTime = .* ClockTime = .*", "ExecutionTime = <runtime> ClockTime = <runtime>"),
    )
    for i, line in enumerate(lines):
        for pattern, replacement in patterns:
            if re.match(pattern, line):
                lines[i] = re.sub(pattern, replacement, line)
                break
    return "\n".join(lines).encode()


def strip_log_hash(value):
    value = json.loads(json.dumps(value))
    value.get("sha256", {}).pop("log.foamRun", None)
    return value


def compare(args):
    base_manifest = json.loads(args.baseline_manifest.read_text())
    repeat_manifest = json.loads(args.repeat_manifest.read_text())
    base_archive = args.baseline_archive.read_bytes()
    repeat_archive = args.repeat_archive.read_bytes()
    for label, manifest, blob in (("baseline", base_manifest, base_archive),
                                  ("repeat", repeat_manifest, repeat_archive)):
        if sha(blob) != manifest["archive_sha256"]:
            raise ValueError(f"{label} archive hash differs from its manifest")
        if not manifest.get("complete") or manifest.get("time_steps") != 100 \
                or manifest.get("converged_steps") != 100 or not manifest.get("end_marker"):
            raise ValueError(f"{label} run is not the expected complete 100-step case")
    if base_manifest["case"] != repeat_manifest["case"]:
        raise ValueError("case identifiers differ")
    case = base_manifest["case"]
    base, repeat = members(args.baseline_archive, case), members(args.repeat_archive, case)
    if base.keys() != repeat.keys():
        raise ValueError("archive member sets differ")
    byte_equal = sorted(name for name in base if base[name] == repeat[name])
    raw_differences = sorted(name for name in base if base[name] != repeat[name])

    if json_bytes(base, "parameters.json") != json_bytes(repeat, "parameters.json"):
        raise ValueError("frozen case parameters differ")
    if json_bytes(base, "input-hashes.json") != json_bytes(repeat, "input-hashes.json"):
        raise ValueError("generated input hash maps differ")
    fields = [f"0.05/{name}" for name in ("U", "p", "C", "phi")]
    field_hashes = {name: {"baseline": sha(base[name]), "repeat": sha(repeat[name]),
                           "byte_identical": base[name] == repeat[name]}
                    for name in fields}
    if not all(row["byte_identical"] for row in field_hashes.values()):
        raise ValueError("at least one endpoint field differs")

    base_diag = json_bytes(base, "diagnostics.json")
    repeat_diag = json_bytes(repeat, "diagnostics.json")
    if strip_log_hash(base_diag) != strip_log_hash(repeat_diag):
        raise ValueError("diagnostics differ beyond the expected source-log hash")
    normalized_logs = {}
    for name in ("log.blockMesh", "log.centres", "log.foamRun"):
        normalized_logs[name] = normalize_log(base[name]) == normalize_log(repeat[name])
    if not all(normalized_logs.values()):
        raise ValueError("solver/preprocessing logs differ beyond runtime metadata")

    command_base = json.loads(base["command.json"])
    command_repeat = json.loads(repeat["command.json"])
    if len(command_base) != len(command_repeat):
        raise ValueError("container commands differ structurally")
    command_base = [re.sub(r"/[^ ]+/n64-dt0\.0005:/case", "<CASE>:/case", x)
                    if isinstance(x, str) else x for x in command_base]
    command_repeat = [re.sub(r"/[^ ]+/n64-dt0\.0005:/case", "<CASE>:/case", x)
                      if isinstance(x, str) else x for x in command_repeat]
    if command_base != command_repeat:
        raise ValueError("container commands differ beyond the case mount path")

    metric_names = ("velocity_relative_l2", "energy_relative_error_cell_samples",
                    "shell_spectrum_relative_l1_error", "gradient_peak_relative_error_cell_samples",
                    "vorticity_peak_relative_error_cell_samples")
    metrics = {key: {"baseline": base_diag[key], "repeat": repeat_diag[key],
                     "exactly_equal": base_diag[key] == repeat_diag[key]}
               for key in metric_names}
    return {
        "scope": "One repeated OpenFOAM Foundation 13 n=64, dt=0.0005 case; numerical reproducibility only, not physical validation.",
        "case": case,
        "baseline_archive_sha256": sha(base_archive),
        "repeat_archive_sha256": sha(repeat_archive),
        "baseline_log_sha256": base_manifest["source_log_sha256"],
        "repeat_log_sha256": repeat_manifest["source_log_sha256"],
        "same_case_parameters_and_input_hashes": True,
        "time_steps_each": [base_manifest["time_steps"], repeat_manifest["time_steps"]],
        "converged_steps_each": [base_manifest["converged_steps"], repeat_manifest["converged_steps"]],
        "standard_acceptance_each": [base_manifest["standard_acceptance"], repeat_manifest["standard_acceptance"]],
        "local_quality_each": [base_manifest["local_quality"], repeat_manifest["local_quality"]],
        "archive_files_total": len(base),
        "byte_identical_files": byte_equal,
        "raw_different_files": raw_differences,
        "endpoint_field_hashes": field_hashes,
        "diagnostics_identical_except_source_log_hash": True,
        "logs_identical_after_runtime_metadata_normalization": normalized_logs,
        "diagnostic_metrics_identical": metrics,
        "interpretation": "All four endpoint fields and listed diagnostics reproduce exactly for this one run. Raw archive/log hashes differ because run-root, timestamp/host, timing metadata and the log-hash reference differ. No solver-wide guarantee or analytic/physical conclusion follows.",
        "success": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-manifest", type=Path, required=True)
    parser.add_argument("--baseline-archive", type=Path, required=True)
    parser.add_argument("--repeat-manifest", type=Path, required=True)
    parser.add_argument("--repeat-archive", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare(args)
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
