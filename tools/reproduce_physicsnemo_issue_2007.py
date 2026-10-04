"""Reproduce NVIDIA PhysicsNeMo issue #2007 without importing the full package."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path



def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_power_spectrum(source_file):
    spec = importlib.util.spec_from_file_location("physicsnemo_power_spectrum_audit", source_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import target source file: {source_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.power_spectrum


def radial_peak(power_spectrum, field):
    _, power = power_spectrum(field)
    flat = power.reshape(-1)
    return {"index": int(flat.argmax()), "power": float(flat.max()), "bins": flat.tolist()}


def classify_controls(results):
    """Require healthy positive spectra and every symmetry control for a fix."""
    healthy = True
    for n in ("32", "33"):
        for axis in ("height_wave_peak", "width_wave_peak"):
            peak = results[n][axis]
            bins = peak["bins"]
            healthy = healthy and bool(bins) and all(
                math.isfinite(value) and value >= 0 for value in bins
            ) and math.isfinite(peak["power"]) and peak["power"] > 0
    controls = results["transpose_controls"]
    healthy = healthy and all(math.isfinite(controls[key]) for key in (
        "odd_33x33_max_abs_difference", "even_32x32_max_abs_difference"
    ))
    even = (results["32"]["height_vs_width_peak_equal"]
            and results["32"]["height_vs_width_spectrum_allclose"]
            and controls["even_32x32_allclose"])
    odd = (results["33"]["height_vs_width_peak_equal"]
           and results["33"]["height_vs_width_spectrum_allclose"]
           and controls["odd_33x33_allclose"])
    reproduced = (healthy and even
                  and not results["33"]["height_vs_width_peak_equal"]
                  and not results["33"]["height_vs_width_spectrum_allclose"]
                  and not controls["odd_33x33_allclose"])
    repaired = healthy and even and odd
    return bool(reproduced), bool(repaired)


def run(source_file, output_file, expect_bug, source_reference):
    import torch

    source_file = Path(source_file)
    power_spectrum = load_power_spectrum(source_file)
    device = torch.device("cpu")

    def axis_cosines(n):
        coordinate = torch.arange(n, dtype=torch.float32, device=device)
        wave = torch.cos(2 * torch.pi * 5 * coordinate / n)
        return wave[:, None].expand(n, n).contiguous(), wave[None, :].expand(n, n).contiguous()

    results = {}
    for n in (32, 33):
        height_wave, width_wave = axis_cosines(n)
        height_peak = radial_peak(power_spectrum, height_wave)
        width_peak = radial_peak(power_spectrum, width_wave)
        _, height_power = power_spectrum(height_wave)
        _, width_power = power_spectrum(width_wave)
        results[str(n)] = {
            "height_wave_peak": height_peak,
            "width_wave_peak": width_peak,
            "height_vs_width_peak_equal": abs(height_peak["power"] - width_peak["power"]) <= 1e-6,
            "height_vs_width_spectrum_allclose": bool(torch.allclose(height_power, width_power, rtol=1e-4, atol=1e-6)),
        }

    torch.manual_seed(2007)
    odd = torch.randn((33, 33), dtype=torch.float32, device=device)
    _, odd_power = power_spectrum(odd)
    _, odd_transpose_power = power_spectrum(odd.T.contiguous())
    even = torch.randn((32, 32), dtype=torch.float32, device=device)
    _, even_power = power_spectrum(even)
    _, even_transpose_power = power_spectrum(even.T.contiguous())
    results["transpose_controls"] = {
        "odd_33x33_max_abs_difference": float((odd_power - odd_transpose_power).abs().max()),
        "odd_33x33_allclose": bool(torch.allclose(odd_power, odd_transpose_power, rtol=1e-4, atol=1e-6)),
        "even_32x32_max_abs_difference": float((even_power - even_transpose_power).abs().max()),
        "even_32x32_allclose": bool(torch.allclose(even_power, even_transpose_power, rtol=1e-4, atol=1e-6)),
    }
    reproduced, repaired = classify_controls(results)
    expected_outcome = "defect_reproduced" if expect_bug else "fix_suppresses_defect"
    expectation_met = reproduced if expect_bug else repaired
    evidence = {
        "scope": "Focused deterministic reproduction of odd-width radial-spectrum asymmetry; not a full PhysicsNeMo test suite.",
        "upstream_issue": "https://github.com/NVIDIA/physicsnemo/issues/2007",
        "upstream_fix_pr": "https://github.com/NVIDIA/physicsnemo/pull/2008",
        "source_file": str(source_file),
        "source_reference": source_reference or str(source_file),
        "source_file_sha256": sha256(source_file),
        "torch_version": torch.__version__,
        "device": "CPU",
        "results": results,
        "reproduced": bool(reproduced),
        "all_fix_controls_pass": bool(repaired),
        "fix_rule": "Positive finite spectra and all even/odd axis and transpose controls must pass; absence of the old failure pattern alone is insufficient.",
        "expected_outcome": expected_outcome,
        "expectation_met": bool(expectation_met),
    }
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, allow_nan=False) + "\n")
    print(json.dumps(evidence, indent=2, allow_nan=False))
    return expectation_met


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-file",
        default="work/physicsnemo-source/physicsnemo/metrics/general/power_spectrum.py",
        help="path to an unmodified NVIDIA PhysicsNeMo power_spectrum.py file",
    )
    parser.add_argument("--expect-fixed", action="store_true", help="pass only if the issue symptoms are absent")
    parser.add_argument(
        "--output",
        default="evidence/upstream-refresh/physicsnemo-issue-2007-reproduction.json",
        help="path for the JSON evidence record",
    )
    parser.add_argument("--source-reference", help="upstream tag/commit associated with the source file")
    args = parser.parse_args()
    raise SystemExit(0 if run(args.source_file, args.output, not args.expect_fixed, args.source_reference) else 1)
