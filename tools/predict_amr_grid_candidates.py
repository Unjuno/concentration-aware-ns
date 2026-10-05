"""Predict first-level candidates for the frozen periodic analytic AMR sensor.

This is an independent structured-grid calculation, not an OpenFOAM run. The
one-layer six-face-neighbor buffer mirrors the inspected Foundation-13 source
semantics and must be rechecked if the target source changes.
"""

import argparse
import json

import numpy as np


def predict(n, lower=0.01, upper=1.1, length=2*np.pi):
    if int(n) != n or n < 2:
        raise ValueError("n must be an integer >= 2")
    if not (np.isfinite(lower) and np.isfinite(upper) and lower < upper):
        raise ValueError("sensor thresholds must be finite and increasing")
    axis = (np.arange(n) + 0.5) * (length/n)
    _, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    g = lambda q: ((1 + np.cos(q))/2)**4
    sensor = g(y)*g(z)
    raw = (sensor > lower) & (sensor < upper)
    buffered = raw.copy()
    for _ in range(1):
        expanded = buffered.copy()
        for dimension in range(3):
            expanded |= (np.roll(buffered, 1, axis=dimension)
                         | np.roll(buffered, -1, axis=dimension))
        buffered = expanded
    raw_count = int(raw.sum())
    candidate_count = int(buffered.sum())
    return {
        "n": int(n), "initial_cells": int(n**3),
        "raw_sensor_candidates": raw_count,
        "one_layer_periodic_face_buffer_candidates": candidate_count,
        "predicted_cells_after_one_level": int(n**3 + 7*candidate_count),
        "sensor_thresholds_strict": [float(lower), float(upper)],
        "buffer_layers": 1,
        "status": "INDEPENDENT_STRUCTURED_GRID_PREDICTION_NOT_SOLVER_EVIDENCE",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--lower", type=float, default=0.01)
    parser.add_argument("--upper", type=float, default=1.1)
    args = parser.parse_args()
    print(json.dumps(predict(args.n, args.lower, args.upper), indent=2))
