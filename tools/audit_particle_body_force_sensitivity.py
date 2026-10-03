"""Conditional scalar body-force counterexample, not a particle trajectory."""
import argparse
import json
from pathlib import Path
from flint import arb, ctx
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints
from tools.run_amr_mean_quality import ROOT, sha


def audit(output, source_commit):
    if output.exists():
        raise FileExistsError('preserve earlier body-force audit')
    consumer = ROOT/'evidence/cell-point-particle-consumer-v1/analysis.json'
    provenance = json.loads(consumer.read_text())
    if provenance['upstream_commit'] != '18870c24d21c6b982e2cdec27b2f59738cca5f90':
        raise ValueError('wrong pinned consumer')
    old = ctx.prec
    ctx.prec = 128
    try:
        # nu=d=dt=r=1, density ratio=1/2, old particle velocity=0.
        # b=dt*(1-density_ratio)*g; g=-40 gives b=-20.
        p, k = exact_float(.687), exact_float(.15)
        x = 9*(1+k)
        dx = 9*k*p
        controls = {}
        for name, b in [('zero_force', 0), ('opposing_force', -20)]:
            derivative = x/(1+x)+(1-b)*dx/(1+x)**2
            if name == 'zero_force' and not (derivative > 0 and derivative < 1):
                raise ValueError('zero-force contraction not enclosed')
            if name == 'opposing_force' and not derivative > 1:
                raise ValueError('body-force amplification not enclosed')
            controls[name] = {'dt_body_force': b, 'derivative': endpoints(derivative)}
        # The exact algebraic threshold is b < 1-(1+x)/dx.
        threshold = 1-(1+x)/dx
        result = {'status': 'CONDITIONAL_BODY_FORCE_COUNTEREXAMPLE',
                  'analysis_source_commit': source_commit,
                  'consumer_record_sha256': sha(consumer),
                  'upstream_commit': provenance['upstream_commit'],
                  'precision_bits': 128,
                  'assumptions': {'nu': 1, 'diameter': 1, 'dt': 1,
                                  'carrier_speed': 1, 'density_ratio': .5,
                                  'old_particle_velocity': 0, 'Re': 1},
                  'update_formula': '(x*r+b)/(1+x)',
                  'derivative_formula': 'x/(1+x)+(r-b)*dx_dr/(1+x)^2',
                  'controls': controls,
                  'amplification_body_force_threshold': endpoints(threshold),
                  'limits': ['Fixed scalar positive high-Re branch; local derivative only',
                             'No native solver, cloud, trajectory or physical-instability claim',
                             'No body-force-free result is contradicted or gate changed']}
    finally:
        ctx.prec = old
    output.mkdir(parents=True)
    (output/'analysis.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(result['status'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    audit(args.output, args.source_commit)
