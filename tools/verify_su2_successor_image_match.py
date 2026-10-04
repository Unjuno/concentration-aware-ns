"""Require a resumed SU2 case to use the exact already-completed baseline image."""

import argparse
import json
from pathlib import Path


IDENTITY_FIELDS = (
    "image_id",
    "source_commit",
    "architecture",
    "build_inputs_sha256",
    "binary_sha256",
    "patched_source_sha256",
    "package_versions_sha256",
    "compiler_version",
)


def verify_image_match(expected, actual):
    for field in IDENTITY_FIELDS:
        if field not in expected or field not in actual:
            raise ValueError(f"missing image identity field: {field}")
        if expected[field] != actual[field]:
            raise ValueError(f"successor image differs from completed baseline: {field}")
    if not isinstance(actual["image_id"], str) or not actual["image_id"].startswith("sha256:"):
        raise ValueError("successor image identity is not immutable")
    return {
        "status": "EXACT_BASELINE_IMAGE_IDENTITY_MATCH",
        "image_id": actual["image_id"],
        "matched_fields": list(IDENTITY_FIELDS),
        "scope": "Image ID, build inputs, installed binary/source/packages, and compiler match; this does not prove solver quality.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--actual", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("preserve previous image-match result")
    result = verify_image_match(
        json.loads(args.expected.read_text()), json.loads(args.actual.read_text())
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
