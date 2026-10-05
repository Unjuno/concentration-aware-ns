"""Audit a saved full Lean log against the exact AxisForceSign source bytes.

This checks a recorded elaboration/axiom log for consistency. It never runs
Lean and cannot authenticate who produced the log.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def audit(source_bytes, log_bytes, manifest, source_name, log_name):
    source = source_bytes.decode("utf-8")
    log = log_bytes.decode("utf-8")
    namespaces = re.findall(r"^namespace\s+([A-Za-z0-9_.]+)\s*$", source, re.M)
    namespace = namespaces[-1] if namespaces else ""
    printed_names = re.findall(r"^#print axioms\s+([A-Za-z0-9_.]+)\s*$", source, re.M)
    expected = {f"{namespace}.{name}" if namespace and "." not in name else name
                for name in printed_names}
    reports = re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]", log, re.S)
    observed = {}
    for name, raw_axioms in reports:
        axioms = {item.strip() for item in raw_axioms.replace("\n", " ").split(",") if item.strip()}
        observed.setdefault(name, []).append(axioms)

    expected_source_hash = manifest.get("sha256", {}).get(source_name)
    expected_log_hash = manifest.get("sha256", {}).get(log_name)
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    log_hash = hashlib.sha256(log_bytes).hexdigest()
    checks = {
        "source_sha256_matches_manifest": bool(expected_source_hash) and source_hash == expected_source_hash,
        "log_sha256_matches_manifest": bool(expected_log_hash) and log_hash == expected_log_hash,
        "printed_declarations_have_axiom_reports": bool(expected) and expected <= set(observed),
        "no_unexpected_axiom_reports": bool(expected) and set(observed) <= expected,
        "all_axioms_allowed": all(axioms <= ALLOWED_AXIOMS for group in observed.values() for axioms in group),
        "no_sorryAx": "sorryAx" not in log,
        "no_lean_errors": not re.search(r"(?:^|\n)[^\n]*\berror:\s", log),
    }
    return {
        "success": all(checks.values()),
        "checks": checks,
        "source": source_name,
        "source_sha256": source_hash,
        "log": log_name,
        "log_sha256": log_hash,
        "printed_declaration_count": len(expected),
        "axiom_report_count": sum(map(len, observed.values())),
        "unreported_declarations": sorted(expected - set(observed)),
        "unexpected_reports": sorted(set(observed) - expected),
        "unexpected_axioms": {
            name: sorted(axioms - ALLOWED_AXIOMS)
            for name, groups in observed.items()
            for axioms in groups
            if axioms - ALLOWED_AXIOMS
        },
        "scope": "Checks saved source/log hash consistency, complete #print coverage, allowed axioms, and absence of Lean error/sorryAx markers. Does not run Lean or authenticate the log origin.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    source_bytes = Path(args.source).read_bytes()
    log_bytes = Path(args.log).read_bytes()
    report = audit(source_bytes, log_bytes, manifest, Path(args.source).as_posix(), Path(args.log).as_posix())
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
