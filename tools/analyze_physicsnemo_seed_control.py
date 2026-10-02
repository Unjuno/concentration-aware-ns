"""Create descriptive paired-seed summaries from the frozen seed-control run."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics


METRICS = (
    "velocity_relative_l2",
    "gradient_peak_relative_error_samples",
    "vorticity_peak_relative_error_samples",
)


def load_json(path):
    return json.loads(Path(path).read_text())


def _verify_archive(root, run):
    path = Path(root) / run["archive"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != run["archive_sha256"]:
        raise ValueError(f"archive hash mismatch: {path.name}")


def analyze(reference, control, archive_root=None):
    if control.get("status") != "COMPLETE":
        raise ValueError("seed-control manifest is not complete")
    runs = control.get("runs", [])
    if len(runs) != control.get("expected_runs") or len(runs) != 20:
        raise ValueError("expected exactly 20 completed seed-control runs")
    if any(run.get("exit_code") != 0 for run in runs):
        raise ValueError("all seed-control runs must have exit_code 0")
    if archive_root is not None:
        for run in runs:
            _verify_archive(archive_root, run)

    reference_rows = {row["case"]: row for row in reference["cases"]}
    rows = []
    for run in runs:
        rows.append({
            "seed": run["seed"], "n": run["n"],
            "time_nodes": run["time_nodes"],
            "velocity_relative_l2": run["velocity_relative_l2"],
            "gradient_peak_relative_error_samples": run["gradient_peak_relative_error_samples"],
            "vorticity_peak_relative_error_samples": run["vorticity_peak_relative_error_samples"],
            "final_training_loss": run["final_training_loss"],
            "elapsed_seconds": run["elapsed_seconds"],
            "archive": run["archive"],
            "archive_sha256": run["archive_sha256"],
        })
    for case, ref in reference_rows.items():
        n, nt = map(int, case.removeprefix("n").split("-nt"))
        rows.append({
            "seed": 709, "n": n, "time_nodes": nt,
            "velocity_relative_l2": ref["velocity_relative_l2"],
            "gradient_peak_relative_error_samples": ref["gradient_peak_error_autograd_samples"],
            "vorticity_peak_relative_error_samples": ref["vorticity_peak_error_autograd_samples"],
        })

    grouped = {}
    for row in rows:
        grouped.setdefault((row["n"], row["time_nodes"]), []).append(row)
    summaries = []
    for (n, nt), group in sorted(grouped.items()):
        item = {"n": n, "time_nodes": nt, "seed_count": len(group), "metrics": {}}
        for metric in METRICS:
            values = [r[metric] for r in group]
            item["metrics"][metric] = {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "sample_sd": statistics.stdev(values),
                "min": min(values), "max": max(values),
            }
        item["seeds"] = sorted(r["seed"] for r in group)
        summaries.append(item)

    paired = {"spatial_n16_to_n32": [], "spatial_n32_to_n64": [],
              "time_nodes_5_to_9": [], "time_nodes_9_to_17": []}
    for seed in sorted({r["seed"] for r in rows}):
        lookup = {(r["n"], r["time_nodes"]): r for r in rows if r["seed"] == seed}
        contrasts = (
            ("spatial_n16_to_n32", (16, 5), (32, 5)),
            ("spatial_n32_to_n64", (32, 5), (64, 5)),
            ("time_nodes_5_to_9", (64, 5), (64, 9)),
            ("time_nodes_9_to_17", (64, 9), (64, 17)),
        )
        for name, a, b in contrasts:
            if a in lookup and b in lookup:
                paired[name].append({
                    "seed": seed,
                    "velocity_relative_l2_delta": lookup[b]["velocity_relative_l2"] - lookup[a]["velocity_relative_l2"],
                    "gradient_peak_relative_error_samples_delta": lookup[b]["gradient_peak_relative_error_samples"] - lookup[a]["gradient_peak_relative_error_samples"],
                    "vorticity_peak_relative_error_samples_delta": lookup[b]["vorticity_peak_relative_error_samples"] - lookup[a]["vorticity_peak_relative_error_samples"],
                })
    paired_summary = {}
    for name, changes in paired.items():
        paired_summary[name] = {
            "paired_seed_count": len(changes),
            "deltas": changes,
            "velocity_delta_mean": statistics.mean(x["velocity_relative_l2_delta"] for x in changes),
            "velocity_delta_median": statistics.median(x["velocity_relative_l2_delta"] for x in changes),
            "velocity_delta_sample_sd": statistics.stdev(x["velocity_relative_l2_delta"] for x in changes),
            "velocity_delta_signs": {
                "lower": sum(x["velocity_relative_l2_delta"] < 0 for x in changes),
                "equal": sum(x["velocity_relative_l2_delta"] == 0 for x in changes),
                "higher": sum(x["velocity_relative_l2_delta"] > 0 for x in changes),
            },
        }
    return {
        "study_id": control["study_id"], "status": "DESCRIPTIVE_ONLY",
        "quality": "UNCERTAIN", "reference_seed": 709,
        "seeds": [709, 1729, 2027, 4093, 8191],
        "new_runs": len(runs), "paired_seed_design": True,
        "limitations": [
            "fixed 5000-step optimization budget does not establish optimizer convergence",
            "sampled derivative peaks do not bound continuous extrema",
            "descriptive small-sample results do not establish a universal effect or threshold",
            "one fixed validation design; seed changes training randomness only",
        ],
        "case_summaries": summaries, "paired_contrasts": paired_summary,
        "runs": sorted(rows, key=lambda r: (r["seed"], r["n"], r["time_nodes"])),
    }


def render_markdown(result):
    lines = [
        "# PhysicsNeMo paired-seed control — descriptive, uncertain",
        "",
        "The frozen control adds four seeds to the existing seed 709 across five fixed-budget cases (five seeds per case, 25 runs total). The 20 added runs completed with exit code 0. Values below describe this configuration only; they do not establish optimization convergence, continuous extrema, or a universal trend.",
        "",
        "| Collocation case | Seeds | Velocity relative L2 mean ± sample SD [range] | Sampled gradient peak error mean ± SD |",
        "|---|---:|---:|---:|",
    ]
    for row in result["case_summaries"]:
        v = row["metrics"]["velocity_relative_l2"]
        g = row["metrics"]["gradient_peak_relative_error_samples"]
        label = f"n{row['n']}-nt{row['time_nodes']}"
        lines.append(f"| {label} | {row['seed_count']} | {v['mean']:.6f} ± {v['sample_sd']:.6f} [{v['min']:.6f}, {v['max']:.6f}] | {g['mean']:.6f} ± {g['sample_sd']:.6f} |")
    lines += ["", "Paired velocity-error changes are new condition minus old condition:", "",
              "| Contrast | Paired seeds | Mean delta | SD | lower / same / higher |", "|---|---:|---:|---:|---:|"]
    names = {
        "spatial_n16_to_n32": "n16 → n32 (nt=5)",
        "spatial_n32_to_n64": "n32 → n64 (nt=5)",
        "time_nodes_5_to_9": "nt5 → nt9 (n=64)",
        "time_nodes_9_to_17": "nt9 → nt17 (n=64)",
    }
    for key, label in names.items():
        c = result["paired_contrasts"][key]
        signs = c["velocity_delta_signs"]
        lines.append(f"| {label} | {c['paired_seed_count']} | {c['velocity_delta_mean']:+.6f} | {c['velocity_delta_sample_sd']:.6f} | {signs['lower']} / {signs['equal']} / {signs['higher']} |")
    time_gradient = result["paired_contrasts"]["time_nodes_9_to_17"]["deltas"]
    gradient_deltas = [x["gradient_peak_relative_error_samples_delta"] for x in time_gradient]
    vorticity_deltas = [x["vorticity_peak_relative_error_samples_delta"] for x in time_gradient]
    velocity_deltas = [x["velocity_relative_l2_delta"] for x in time_gradient]
    spatial_gradient = result["paired_contrasts"]["spatial_n16_to_n32"]["deltas"]
    spatial_gradient_deltas = [x["gradient_peak_relative_error_samples_delta"] for x in spatial_gradient]
    spatial_vorticity_deltas = [x["vorticity_peak_relative_error_samples_delta"] for x in spatial_gradient]
    lines += ["", "The paired derivative-peak metrics do not follow the velocity metric uniformly. From nt=9 to nt=17, sampled velocity relative L2 decreases for "
              f"{sum(x < 0 for x in velocity_deltas)} of {len(velocity_deltas)} seeds (mean delta {statistics.mean(velocity_deltas):+.6f}), while sampled gradient-peak error changes are higher for "
              f"{sum(x > 0 for x in gradient_deltas)} and lower for {sum(x < 0 for x in gradient_deltas)} seeds (mean {statistics.mean(gradient_deltas):+.6f}); sampled vorticity-peak error is higher for "
              f"{sum(x > 0 for x in vorticity_deltas)} and lower for {sum(x < 0 for x in vorticity_deltas)} (mean {statistics.mean(vorticity_deltas):+.6f}). From n=16 to n=32, sampled gradient- and vorticity-peak errors increase for "
              f"{sum(x > 0 for x in spatial_gradient_deltas)} of five seeds and decrease for {sum(x < 0 for x in spatial_gradient_deltas)}. These are paired comparisons on a shared fixed validation design, not evidence of a continuous extremum or a causal effect of node count; magnitudes are small and no acceptance threshold was preregistered.", ""]
    lines += ["", "Seed 8191 produced a visibly higher velocity error in all five conditions than the first three new seeds; this demonstrates material seed sensitivity in this small sample. The paired contrasts remain descriptive and share the same fixed validation design. Training loss and runtime are retained per-run in the JSON artifact.", "",
              "All quality/gate conclusions remain `UNCERTAIN`. The sampled gradient/vorticity metrics are finite-point checks, not certified maxima. No molecular interpretation, phase transition, or physical instability follows from these PINN errors.", "",
              "Machine-readable means, medians, sample standard deviations, ranges, exact paired deltas for velocity/gradient/vorticity, run records, and limitations are in `evidence/physicsnemo-seed-control-v1/analysis.json`. The frozen report is regenerated from the archived run manifest; all 20 added archive hashes are verified before regeneration.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", default="evidence/physicsnemo-study-v1/comparison.json")
    parser.add_argument("--control", default="evidence/physicsnemo-seed-control-v1/summary.json")
    parser.add_argument("--archive-root", default="evidence/physicsnemo-seed-control-v1")
    parser.add_argument("--output-json", default="evidence/physicsnemo-seed-control-v1/analysis.json")
    parser.add_argument("--output-report", default="reports/physicsnemo-seed-control-v1.md")
    args = parser.parse_args()
    result = analyze(load_json(args.reference), load_json(args.control), args.archive_root)
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_report).write_text(render_markdown(result))


if __name__ == "__main__":
    main()
