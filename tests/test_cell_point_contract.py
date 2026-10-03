from tools.audit_cell_point_contract import affine_controls


def test_exact_affine_trace_and_chord_controls():
    result=affine_controls()
    assert result['endpoint_residuals']==['0','0']
    assert result['shared_face_trace_residual']=='0'
    assert result['gradient_slope_sum_residual']=='0'
    assert result['integer_chord_controls']==125
    assert result['degenerate_fallback_centre_error']!='0'
