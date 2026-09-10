"""Replay deterministic report generation from published archived inputs.

Does not rerun PDE solvers, train networks, or verify the OpenAI proof.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

steps = [
    ('tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests']),
    ('global_peaks', [sys.executable, '-m', 'tools.compare_global_peaks']),
    ('peak_decomposition', [sys.executable, '-m', 'tools.decompose_peak_diagnostic']),
    ('spectral_derivatives', [sys.executable, '-m', 'tools.compare_openfoam_spectral']),
    ('su2_archive_review', [sys.executable, '-m', 'tools.review_su2_archives']),
    ('su2_diagnostic_replay', [sys.executable, '-m', 'tools.replay_su2_diagnostics']),
    ('su2_spectral_derivatives', [sys.executable, '-m', 'tools.compare_su2_spectral']),
    ('openfoam_gate', [sys.executable, '-m', 'tools.build_openfoam_report']),
    ('physicsnemo_gates', [sys.executable, '-m', 'tools.build_physicsnemo_report']),
    ('artifact_links', [sys.executable, '-m', 'tools.audit_gate_artifacts']),
]
output = Path('evidence/report-replay');output.mkdir(exist_ok=True)
records = []
for name, command in steps:
    run = subprocess.run(command, capture_output=True, text=True)
    log = output/(name+'.log');log.write_text(run.stdout+run.stderr)
    records.append({'step':name,'command':command,'exit_code':run.returncode,
                    'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
    if run.returncode:
        break
success = len(records)==len(steps) and all(r['exit_code']==0 for r in records)
(output/'summary.json').write_text(json.dumps({'scope':'Report generation replay only. No new solver/training/proof run and no scientific verdict upgrade.', 'success':success, 'steps':records},indent=2)+'\n')
print(json.dumps({'success':success,'completed_steps':len(records)},indent=2))
raise SystemExit(0 if success else 1)
