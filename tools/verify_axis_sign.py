"""Run the pinned Lean check and bind its result to exact source bytes."""
import hashlib
import json
import re
from pathlib import Path
import subprocess


def verify():
    source=Path('verification/AxisForceSign.lean')
    runner=Path('runtime/lean-verification/check_axis_sign.sh')
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    run=subprocess.run(['sh',str(runner)],capture_output=True,text=True)
    log=run.stdout+run.stderr
    logpath=Path('evidence/lean-verification/axis-force-sign.log')
    logpath.write_text(log)
    expected=['selected_base_velocity_on_candidate_axis','selected_stream_on_candidate_axis','selected_stream_sum_axis_value','root_axis_curve_hasDerivAt','candidate_axis_curve_hasDerivAt','candidate_normalized_stream_derivative_limit','candidate_axis_physicalChart','candidate_axis_forward_coordinate','candidate_axis_inverse_coordinate','trajectory_scale_tends_zero_right','selected_stream_normalized_radial_derivative','selected_averaged_derivative_sum_tends_natural','slowSum_axis_proportional','averaged_derivative_slowSum_at_axis','bundle_average_derivative_at_axis','selected_bundle_average_derivative_at_axis','average_radial_derivative_at_axis','radial_derivative_compact_integral','selected_stream_radial_derivative_physical','selected_base_velocity_laplacian_on_axis','selected_base_velocity_slice_eq','curl_velocity_eq_profile_velocity','selected_profile_velocity_laplacian_on_axis','selected_transverse_profiles_sliceC2','selected_stream_axial_velocity_sliceC2','selected_stream_sliceC2','physical_stream_laplacian_of_sliceC2','physical_stream_laplacian_on_axis','stream_axial_second_derivative_on_axis','axial_slice_derivative_eq_partialZ','axial_second_derivative_eq_slice','stream_axial_radial_derivative_on_axis','physical_axial_laplacian_on_axis','prepared_root_with_negative_radial_derivative','exists_selected_root_with_negative_radial_derivative','selected_axial_radial_derivative_eventually_negative','selected_natural_derivative_negative','original_axis_derivative_eq_natural','selected_axial_radial_derivative_tends_natural','modulated_axis_derivative_eq_original','selected_axial_radial_derivative_tends_original','selected_axial_radial_derivative_tends_modulated','deriv_eq_of_nonnegative_agreement','selected_leading_derivative_eq_modulated','selected_axial_radial_derivative_tends_leading','axial_radial_derivative_tends_leading','axial_radial_tail_tends_zero','radial_derivative_limit_of_first_jet','chart_radial_derivative_eq_fderiv','first_jet_radial_component_tends_zero','axial_derivative_tail_tends_zero','power_bounded_remainder_tends_zero','uncut_prefix_derivative_tends_leading','uncut_prefix_as_positive_sum','finite_prefix_derivative_tends_leading','finite_prefix_radial_derivative','finite_positive_prefix_tends_zero','selected_axial_component_derivative_tail','axial_component_derivative_tail','natural_radial_derivative_quantitative','natural_radial_derivative_negative_at_root','natural_axis_radial_identity_from_solution','natural_axis_radial_identity','actual_axis_force_ratio_negative','exists_negative_axis_force_ratio']
    printed=all("'ConcentrationAware."+name+"' depends on axioms:" in log for name in expected)
    reports=re.findall(r"'ConcentrationAware\.([^']+)' depends on axioms: \[(.*?)\]",log,re.S)
    allowed={'propext','Classical.choice','Quot.sound'}
    axioms={name:[x.strip() for x in body.split(',') if x.strip()] for name,body in reports}
    allowed_only=all(name in axioms and set(axioms[name])<=allowed for name in expected)
    unchanged=hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
    success=run.returncode==0 and printed and allowed_only and 'sorryAx' not in log and unchanged
    result={'exit_code':run.returncode,'success':success,'source':str(source),'source_sha256':source_hash,'runner_sha256':hashlib.sha256(runner.read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(logpath.read_bytes()).hexdigest(),'axioms':axioms,'only_allowed_axioms':allowed_only,'expected_axiom_reports_present':printed,'source_unchanged_during_run':unchanged,'contains_sorryAx':'sorryAx' in log,'scope':'Pinned Lean check of scalar sign, existence, natural-profile radial derivatives, finite-prefix limits, ordinary radial derivative tail convergence and the full axial slow-sum radial derivative limit. Full assembled-field identity and asymptotic force limit are not formalized here. Not an independent nanoda check.','replay':'python3 -m tools.verify_axis_sign'}
    Path('evidence/lean-verification/axis-force-sign.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return success

if __name__=='__main__':
    raise SystemExit(0 if verify() else 1)
