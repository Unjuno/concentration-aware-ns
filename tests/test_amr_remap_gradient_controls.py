import numpy as np
import pytest

from tools.replay_amr_remap_gradient_controls import (
    openfoam_gradient_to_math_convention,
)


def test_openfoam_gradient_storage_transposes_to_velocity_component_first():
    expected = np.array([
        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        [[-1.0, 0.5, 2.0], [3.0, -4.0, 0.0], [1.5, 2.5, -3.0]],
    ])
    stored_openfoam = expected.transpose(0, 2, 1)

    np.testing.assert_array_equal(
        openfoam_gradient_to_math_convention(stored_openfoam), expected
    )


@pytest.mark.parametrize("shape", [(3, 3), (2, 3, 2), (2, 3, 3, 1)])
def test_openfoam_gradient_conversion_rejects_invalid_shapes(shape):
    with pytest.raises(ValueError, match=r"shape \(cells, 3, 3\)"):
        openfoam_gradient_to_math_convention(np.zeros(shape))
