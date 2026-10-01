"""Replay published evidence, reports, and exact algebra checks.

Does not rerun PDE solvers, train networks, or verify the OpenAI proof.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

steps = [
    ('tests', [sys.executable, '-m', 'pytest', '-q', 'tests']),
    ('global_peaks', [sys.executable, '-m', 'tools.compare_global_peaks']),
    ('peak_decomposition', [sys.executable, '-m', 'tools.decompose_peak_diagnostic']),
    ('spectral_derivatives', [sys.executable, '-m', 'tools.compare_openfoam_spectral']),
    ('openfoam_uniform_archive_schedules', [sys.executable, '-m', 'tools.audit_high_gradient_time_sequence']),
    ('openfoam_fd2_synthetic_controls', [sys.executable, '-m', 'tools.check_openfoam_fd2_synthetic_controls']),
    ('openfoam_trig_supremum_arb', [sys.executable, '-m', 'tools.audit_openfoam_trig_supremum']),
    ('openfoam_temporal_triplet', [sys.executable, '-m', 'tools.compare_high_gradient_temporal']),
    ('openfoam_amr_archive_integrity', [sys.executable, '-m', 'tools.verify_openfoam_amr_archives']),
    ('su2_archive_review', [sys.executable, '-m', 'tools.review_su2_archives']),
    ('su2_standard_review', [sys.executable, '-m', 'tools.review_su2_standard']),
    ('su2_diagnostic_replay', [sys.executable, '-m', 'tools.replay_su2_diagnostics']),
    ('su2_spectral_derivatives', [sys.executable, '-m', 'tools.compare_su2_spectral']),
    ('su2_time_comparison', [sys.executable, '-m', 'tools.compare_su2_time']),
    ('su2_localized_source_lag', [sys.executable, '-m', 'tools.audit_su2_localized_source_lag']),
    ('su2_bdf2_control', [sys.executable, '-m', 'tools.check_su2_bdf2_control']),
    ('su2_boundary_time_pilot', [sys.executable, '-m', 'tools.check_su2_boundary_time_pilot']),
    ('su2_restart_findings', [sys.executable, '-m', 'tools.replay_su2_restart_findings']),
    ('openfoam_gate', [sys.executable, '-m', 'tools.build_openfoam_report']),
    ('physicsnemo_gates', [sys.executable, '-m', 'tools.build_physicsnemo_report']),
    ('physicsnemo_sampled_derivative_replay', [sys.executable, '-m', 'tools.audit_physicsnemo_local_fields']),
    ('su2_gates', [sys.executable, '-m', 'tools.build_su2_report']),
    ('root_pressure_threshold', [sys.executable, '-m', 'tools.check_root_pressure_threshold']),
    ('pressure_moment_threshold', [sys.executable, '-m', 'tools.check_pressure_moment_threshold']),
    ('cone_sign_symmetry', [sys.executable, '-m', 'tools.check_cone_sign_symmetry']),
    ('su2_output_clock_control', [sys.executable, '-m', 'tools.check_su2_output_clock_control']),
    ('uniform_prefix_threshold', [sys.executable, '-m', 'tools.check_uniform_prefix_threshold']),
    ('high_gradient_mms', [sys.executable, '-m', 'tools.check_high_gradient_mms']),
    ('high_gradient_reference', [sys.executable, '-m', 'tools.check_high_gradient_reference']),
    ('support_hole_tube_geometry', [sys.executable, '-m', 'tools.check_support_hole_tube_geometry']),
    ('openfoam_iteration_archives', [sys.executable, '-m', 'tools.replay_openfoam_iteration_archives']),
    ('openfoam_pressure_pilot', [sys.executable, '-m', 'tools.replay_openfoam_pressure_pilot']),
    ('openfoam_solenoidal_startup', [sys.executable, '-m', 'tools.check_openfoam_solenoidal_control']),
    ('artifact_links', [sys.executable, '-m', 'tools.audit_gate_artifacts']),
]
output = Path('evidence/report-replay');output.mkdir(exist_ok=True)
records = []
for name, command in steps:
    run = subprocess.run(command, capture_output=True, text=True)
    log = output/(name+'.log');log.write_text(run.stdout+run.stderr)
    records.append({'step':name,'command':command,
                    'replay_command':['python3', *command[1:]],
                    'exit_code':run.returncode,
                    'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
    if run.returncode:
        break
success = len(records)==len(steps) and all(r['exit_code']==0 for r in records)
(output/'summary.json').write_text(json.dumps({'scope':'Archived-input report generation and exact algebra replay. No new solver, training or Lean run and no scientific verdict upgrade.', 'success':success, 'steps':records},indent=2)+'\n')
print(json.dumps({'success':success,'completed_steps':len(records)},indent=2))
raise SystemExit(0 if success else 1)
