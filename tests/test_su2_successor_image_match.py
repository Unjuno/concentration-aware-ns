import copy

import pytest

from tools.verify_su2_successor_image_match import verify_image_match


def receipt():
    return {
        "image_id": "sha256:" + "a" * 64,
        "source_commit": "12eb826f049ef7f67df974dfcb44cf36ee07c0f8",
        "architecture": "linux/arm64",
        "build_inputs_sha256": {"Dockerfile": "b" * 64},
        "binary_sha256": "c" * 64,
        "patched_source_sha256": "d" * 64,
        "package_versions_sha256": "e" * 64,
        "compiler_version": "g++ fixture",
    }


def test_exact_same_image_receipt_passes():
    result = verify_image_match(receipt(), receipt())
    assert result["status"] == "EXACT_BASELINE_IMAGE_IDENTITY_MATCH"


@pytest.mark.parametrize("field", [
    "image_id", "source_commit", "architecture", "build_inputs_sha256",
    "binary_sha256", "patched_source_sha256", "package_versions_sha256",
    "compiler_version",
])
def test_any_image_or_build_identity_change_stops_before_solver(field):
    altered = copy.deepcopy(receipt())
    altered[field] = "different"
    with pytest.raises(ValueError):
        verify_image_match(receipt(), altered)


def test_unpinned_image_identifier_is_rejected():
    altered = receipt()
    altered["image_id"] = "latest"
    with pytest.raises(ValueError):
        verify_image_match(altered, altered)
