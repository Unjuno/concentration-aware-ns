import io
import tarfile

import pytest

from tools.compare_high_gradient_temporal import extract_case_archive


def write_tar(path, member_name, payload=b"archive-backed"):
    with tarfile.open(path, "w:gz") as archive:
        member = tarfile.TarInfo(member_name)
        member.size = len(payload)
        archive.addfile(member, io.BytesIO(payload))


def test_extract_case_archive_reads_expected_case(tmp_path):
    archive = tmp_path / "case.tar.gz"
    write_tar(archive, "n64-dt0.001/diagnostics.json")

    case = extract_case_archive(archive, tmp_path / "out", "n64-dt0.001")

    assert (case / "diagnostics.json").read_bytes() == b"archive-backed"


@pytest.mark.parametrize("member_name", [
    "other-case/diagnostics.json",
    "n64-dt0.001/../../escape.txt",
    "/absolute/escape.txt",
])
def test_extract_case_archive_rejects_unexpected_paths(tmp_path, member_name):
    archive = tmp_path / "case.tar.gz"
    write_tar(archive, member_name)

    with pytest.raises(ValueError, match="unsafe or unexpected archive member"):
        extract_case_archive(archive, tmp_path / "out", "n64-dt0.001")
