"""Create a reviewable OpenFOAM AMR archive with protocol-selected members."""

import hashlib
import fnmatch
import tarfile
from pathlib import Path


def package_case(case, archive, excluded_relative_paths=()):
    case = Path(case)
    archive = Path(archive)
    excluded = tuple(Path(item).as_posix().strip("/") for item in excluded_relative_paths)
    excluded_seen = set()

    def include(info):
        name = info.name
        prefix = case.name + "/"
        rel = name[len(prefix):] if name.startswith(prefix) else name
        for pattern in excluded:
            # The v5 pattern is deliberately narrow and does not use recursive
            # shell expansion semantics.
            if pattern == "dynamicCode" and (rel == pattern or rel.startswith(pattern + "/")):
                excluded_seen.add(pattern)
                return None
            if fnmatch.fnmatchcase(rel, pattern):
                excluded_seen.add(pattern)
                return None
        return info

    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz", compresslevel=6) as tf:
        tf.add(case, arcname=case.name, filter=include)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    return {
        "archive": archive.name,
        "archive_sha256": digest,
        "excluded_patterns": list(excluded),
        "excluded_patterns_observed": sorted(excluded_seen),
        "status": "PACKAGED_WITH_PROTOCOL_DECLARED_EXCLUSIONS",
    }
