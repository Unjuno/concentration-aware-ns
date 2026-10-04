import pytest

from tools.analyze_amr_cap100000_integrated import _field


def test_field_parser_reads_tensor_and_scalar_lists():
    tensor = b"internalField nonuniform List<tensor> 1 ((1 2 3 4 5 6 7 8 9));"
    scalar = b"internalField nonuniform List<scalar> 2 (0.25 0.75);"
    assert _field(tensor, "tensor", 9).tolist() == [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
    assert _field(scalar, "scalar", 1).tolist() == [0.25, 0.75]


def test_field_parser_rejects_truncated_archive_field():
    truncated = b"internalField nonuniform List<vector> 2 ((1 2 3));"
    with pytest.raises(ValueError, match="dimensions"):
        _field(truncated, "vector", 3)
