import hashlib

import pytest

from tools.analyze_physicsnemo_seed_control import analyze, render_markdown


CASES = [(16, 5), (32, 5), (64, 5), (64, 9), (64, 17)]
SEEDS = [1729, 2027, 4093, 8191]


def fixtures(tmp_path):
    runs = []
    for seed in SEEDS:
        for n, nt in CASES:
            name = f"seed{seed}-n{n}-nt{nt}.tar.gz"
            payload = f"fixture-{seed}-{n}-{nt}".encode()
            (tmp_path / name).write_bytes(payload)
            runs.append({
                "seed": seed, "n": n, "time_nodes": nt,
                "exit_code": 0, "archive": name,
                "archive_sha256": hashlib.sha256(payload).hexdigest(),
                "velocity_relative_l2": seed / 100000 + n / 1000000 + nt / 10000000,
                "gradient_peak_relative_error_samples": 0.01,
                "vorticity_peak_relative_error_samples": 0.02,
                "final_training_loss": 0.03, "elapsed_seconds": 52.0,
            })
    control = {
        "status": "COMPLETE", "study_id": "fixture", "expected_runs": 20,
        "runs": runs,
    }
    ref_cases = []
    for n, nt in CASES:
        ref_cases.append({
            "case": f"n{n}-nt{nt}", "velocity_relative_l2": 0.02,
            "gradient_peak_error_autograd_samples": 0.01,
            "vorticity_peak_error_autograd_samples": 0.02,
        })
    return {"quality": "UNCERTAIN", "cases": ref_cases}, control


def test_analyzer_summarizes_five_seeds_and_paired_changes(tmp_path):
    reference, control = fixtures(tmp_path)
    result = analyze(reference, control, tmp_path)
    case = next(x for x in result["case_summaries"] if (x["n"], x["time_nodes"]) == (16, 5))
    assert case["seed_count"] == 5
    assert case["seeds"] == [709, 1729, 2027, 4093, 8191]
    assert case["metrics"]["velocity_relative_l2"]["sample_sd"] > 0
    contrast = result["paired_contrasts"]["spatial_n16_to_n32"]
    assert contrast["paired_seed_count"] == 5
    assert contrast["velocity_delta_signs"] == {"lower": 0, "equal": 1, "higher": 4}
    report = render_markdown(result)
    assert "UNCERTAIN" in report
    assert "not certified maxima" in report
    assert "derivative-peak metrics do not follow the velocity metric uniformly" in report
    assert "not evidence of a continuous extremum" in report


def test_analyzer_rejects_changed_archive(tmp_path):
    reference, control = fixtures(tmp_path)
    (tmp_path / control["runs"][0]["archive"]).write_text("changed")
    with pytest.raises(ValueError, match="archive hash mismatch"):
        analyze(reference, control, tmp_path)


def test_analyzer_rejects_incomplete_control(tmp_path):
    reference, control = fixtures(tmp_path)
    control["status"] = "IN_PROGRESS"
    with pytest.raises(ValueError, match="not complete"):
        analyze(reference, control)
