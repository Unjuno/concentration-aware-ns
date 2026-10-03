"""Diagnose parent-value injection and integral preservation from same-time snapshots."""
import argparse
import json
from pathlib import Path

import numpy as np

from tools.analyze_amr_gauss_gradient import _read_csv, _vector
from tools.run_amr_mean_quality import PROTOCOL
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.amr_projection_decomposition import exact_cell_mean_square_velocity


def transfer_diagnostics(pre, mapped, n, frequency=3, time=.002):
    h = 2*np.pi/n
    centers = _vector(pre, ('cx', 'cy', 'cz'))
    coordinates = np.rint(centers/h-.5).astype(int)
    child_centers = _vector(mapped, ('cx', 'cy', 'cz'))
    parents = np.floor(child_centers/h).astype(int)
    if (len(centers) != n**3 or np.max(np.abs(centers/h-.5-coordinates)) > 1e-10
            or np.any(coordinates < 0) or np.any(coordinates >= n)
            or not np.isfinite(child_centers).all() or np.any(parents < 0) or np.any(parents >= n)):
        raise ValueError('invalid uniform parent grid or mapped centers')
    ids = lambda c: (c[:, 0]*n+c[:, 1])*n+c[:, 2]
    if len(np.unique(ids(coordinates))) != n**3:
        raise ValueError('duplicated parent grid centers')
    lookup = np.empty(n**3, dtype=int); lookup[ids(coordinates)] = np.arange(n**3)
    parent_rows = lookup[ids(parents)]
    before, after = _vector(pre, ('Ux', 'Uy', 'Uz')), _vector(mapped, ('Ux', 'Uy', 'Uz'))
    pv, cv = pre['V'], mapped['V']
    if (not all(np.isfinite(a).all() for a in (before, after, pv, cv, pre['p'], mapped['p']))
            or np.any(pv <= 0) or np.any(cv <= 0)):
        raise ValueError('invalid or nonfinite transfer fields')
    velocity_difference = float(np.max(np.abs(after-before[parent_rows])))
    pressure_difference = float(np.max(np.abs(mapped['p']-pre['p'][parent_rows])))
    delta = np.sum(cv[:, None]*after, axis=0)-np.sum(pv[:, None]*before, axis=0)
    scale = max(float(np.sum(pv*np.linalg.norm(before, axis=1))), 1e-300)
    decompositions = {}
    for name, table, values in (('preMap', pre, before), ('mapped', mapped, after)):
        cc = _vector(table, ('cx', 'cy', 'cz')); volumes = table['V']; widths = np.cbrt(volumes)
        means = exact_cell_average_velocity(cc, widths, time, frequency)
        reference_energy = float(np.sum(volumes*exact_cell_mean_square_velocity(cc, widths, time, frequency)))
        mismatch = float(np.sum(volumes*np.sum((values-means)**2, axis=1)))
        projection_energy = float(np.sum(volumes*np.sum(means**2, axis=1)))
        floor = reference_energy-projection_energy
        decompositions[name] = {'mean_mismatch_relative_l2_squared': mismatch/reference_energy,
            'projection_floor_relative_l2_squared': floor/reference_energy,
            'p0_total_relative_l2_squared': (mismatch+floor)/reference_energy}
    a, b = decompositions['preMap'], decompositions['mapped']
    identity = (b['mean_mismatch_relative_l2_squared']-a['mean_mismatch_relative_l2_squared']
                -(a['projection_floor_relative_l2_squared']-b['projection_floor_relative_l2_squared']))
    return {'parent_cells': len(before), 'mapped_cells': len(after),
            'velocity_parent_injection_max_absolute_difference': velocity_difference,
            'pressure_parent_injection_max_absolute_difference': pressure_difference,
            'exact_captured_parent_value_copy': velocity_difference == 0 and pressure_difference == 0,
            'velocity_integral_difference': delta.tolist(),
            'velocity_repartition_decomposition': decompositions,
            'velocity_mean_error_floor_exchange_identity_residual': identity,
            'velocity_p0_total_squared_difference': b['p0_total_relative_l2_squared']-a['p0_total_relative_l2_squared'],
            'interpretation': 'If parent injection is exact, the same P0 velocity function is merely repartitioned: its continuum L2 error remains constant, while a lower projection floor becomes higher cell-mean mismatch. No new continuum velocity error is inferred from that mean-error jump.',
            'velocity_integral_difference_relative_to_parent_l1': float(np.linalg.norm(delta)/scale),
            'scope': 'Empirical comparison of archived cell values at the same map event; no mapping contract violation, continuous-field accuracy or universality claim.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.evidence_root/'manifest.json').read_text())
    spec = json.loads(PROTOCOL.read_text())
    case = next(c for c in spec['cases'] if c['id'] == manifest['case_id'])
    # Caller first verifies the frozen archive with analyze_amr_mean_quality.
    from tools.analyze_amr_mean_quality import verify_archive
    archive = args.evidence_root/manifest['archive']['path']; verify_archive(archive, manifest)
    pre = _read_csv(archive, 'main/postProcessing/amrStages/0.002/preMap_cells.csv')
    mapped = _read_csv(archive, 'main/postProcessing/amrStages/0.002/mapped_cells.csv')
    result = transfer_diagnostics(pre, mapped, case['n'], spec['model']['frequency'], spec['model']['pre_map_time'])
    result.update(case_id=case['id'], source_commit=manifest['source_commit'],
                  archive_sha256=manifest['archive']['sha256'])
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
