"""Check the archived AMR sensor against its prescribed analytic envelope."""
import hashlib
import json
import re
import tarfile
from pathlib import Path

import numpy as np


ROOT = Path("evidence/of13-amr-first-refinement-v1")
RUN = "amr-cap5000"
TIME = "0.003"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_field(raw, kind):
    text = raw.decode("ascii")
    match = re.search(
        rf"internalField\s+nonuniform\s+List<{kind}>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S)
    if not match:
        raise ValueError(f"expected ASCII nonuniform List<{kind}>")
    count = int(match[1])
    body = match[2]
    if kind == "vector":
        values = np.fromstring(body.replace("(", " ").replace(")", " "), sep=" ")
        if values.size != 3*count:
            raise ValueError("vector count mismatch")
        return values.reshape(count, 3)
    values = np.fromstring(body, sep=" ")
    if values.size != count or not np.isfinite(values).all():
        raise ValueError("scalar count or finiteness mismatch")
    return values


def g(q):
    return (35 + 56*np.cos(q) + 28*np.cos(2*q)
            + 8*np.cos(3*q) + np.cos(4*q))/128


def main():
    manifest = json.loads((ROOT/"manifest.json").read_text())
    archive_path = ROOT/f"{RUN}.tar.gz"
    archived = {row["case"]: row["archive_sha256"] for row in manifest["cases"]}
    archive_hash = sha256(archive_path)
    if archive_hash != archived.get(RUN):
        raise ValueError("AMR archive hash differs from manifest")
    protocol = Path("protocols/high-gradient-of13-amr-first-refinement-v1.json")
    proto = json.loads(protocol.read_text())
    if "analytic localized envelope chi(y,z)" not in json.dumps(proto):
        raise ValueError("protocol does not declare the localized analytic sensor")
    with tarfile.open(archive_path) as archive:
        def field(name, kind):
            member = archive.extractfile(f"{RUN}/{TIME}/{name}")
            if member is None:
                raise ValueError(f"missing archived field {name}")
            return parse_field(member.read(), kind)
        centers = field("C", "vector")
        volume = field("Vc", "scalar")
        sensor = field("refineSensor", "scalar")
        levels = field("cellLevel", "scalar")
    if not (len(centers) == len(volume) == len(sensor) == len(levels)):
        raise ValueError("archived field counts differ")
    if np.any(volume <= 0) or np.any(levels != np.rint(levels)):
        raise ValueError("invalid volumes or non-integral cell levels")
    levels = np.rint(levels).astype(int)
    expected = g(centers[:, 1])*g(centers[:, 2])
    residual = sensor-expected
    rows = []
    for level in np.unique(levels):
        mask = levels == level
        rows.append({
            "level": int(level), "cells": int(mask.sum()),
            "cell_fraction": float(mask.mean()),
            "volume_fraction": float(volume[mask].sum()/volume.sum()),
            "sensor_quantiles_min_median_p95_max": [
                float(x) for x in np.quantile(sensor[mask], [0, .5, .95, 1])],
        })
    thresholds = {}
    for threshold in (.01, .1, .5):
        selected = sensor >= threshold
        thresholds[str(threshold)] = {
            "cell_fraction": float(selected.mean()),
            "volume_fraction": float(volume[selected].sum()/volume.sum()),
            "selected_volume_at_level1_fraction": float(
                volume[selected & (levels == 1)].sum()/volume[selected].sum()),
            "level1_volume_above_threshold_fraction": float(
                volume[selected & (levels == 1)].sum()/volume[levels == 1].sum()),
        }
    result = {
        "scope": "Archived AMR sensor-to-level correspondence; not an independent discovery test.",
        "archive": str(archive_path), "archive_sha256": archive_hash,
        "protocol": str(protocol), "protocol_sha256": sha256(protocol),
        "audit_script": str(Path(__file__)), "audit_script_sha256": sha256(__file__),
        "checkpoint": TIME, "cells": len(sensor),
        "sensor_formula": "g(y)*g(z), g(q)=(1+cos(q))^4/16",
        "analytic_formula_max_abs_residual": float(np.max(np.abs(residual))),
        "analytic_formula_rms_residual": float(np.sqrt(np.mean(residual**2))),
        "levels": rows, "thresholds": thresholds,
        "interpretation": "The source hook prescribes this analytic envelope; level overlap is by construction, with threshold and buffer effects.",
    }
    output = ROOT/"sensor-mapping-audit.json"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
