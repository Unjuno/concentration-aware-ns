"""Conditional drag-branch sensitivity; no native cloud or trajectory run."""
import argparse,json,math,sys,platform
from pathlib import Path
from fractions import Fraction
from flint import arb,ctx
from tools.run_amr_mean_quality import ROOT,sha
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints


def update(u,mode='source'):
    re=math.sqrt(u*u);factor=1.
    if mode=='continuous' or (mode=='source' and re>.01):factor+=.15*re**.687
    dc=18*factor
    return dc*u/(1+dc)


def audit(output,source_commit):
    output=Path(output)
    if output.exists():raise FileExistsError('preserve previous branch audit')
    consumer=ROOT/'evidence/cell-point-particle-consumer-v1/analysis.json';provenance=json.loads(consumer.read_text())
    if provenance['upstream_commit']!='18870c24d21c6b982e2cdec27b2f59738cca5f90':raise ValueError('wrong source pin')
    p=Fraction.from_float(.687);controls=0
    for x in (Fraction(0),Fraction(1,100),Fraction(1),Fraction(10),Fraction(100)):
        for theta in (Fraction(0),Fraction(1,3),Fraction(1,2),Fraction(1)):
            radial=x/(1+x)+p*theta*x/(1+x)**2
            margin=(1+(1-p*theta)*x)/(1+x)**2
            if radial<0 or not radial<1 or radial+margin!=1:raise ValueError('branch sensitivity control failed')
            elasticity=1-p*theta
            if not 1-p<=elasticity<=1:raise ValueError('viscosity elasticity control failed')
            controls+=1
    low=.01;high=math.nextafter(low,math.inf);measures={}
    for mode in ('source','continuous','constant'):
        delta=update(high,mode)-update(low,mode)
        measures[mode]={'input_difference':high-low,'output_difference':delta,'two_float_quotient':delta/(high-low)}
    if measures['source']['output_difference']<3e-6 or any(abs(measures[k]['output_difference'])>1e-16 for k in ('constant','continuous')):
        raise ValueError('branch/negative-control pattern not reproduced')
    old=ctx.prec;ctx.prec=128
    try:
        r=exact_float(.01);exponent=exact_float(.687);right=18*(1+exact_float(.15)*(exponent*r.log()).exp())
        jump=r*(right-18)/((1+right)*19)
        if not jump>0:raise ValueError('positive idealized branch jump unproved')
        enclosed=endpoints(jump)
    finally:ctx.prec=old
    result={'status':'CONDITIONAL_DRAG_BRANCH_AUDIT','analysis_source_commit':source_commit,'consumer_record_sha256':sha(consumer),'upstream_commit':provenance['upstream_commit'],'precision_bits':128,'assumptions':{'nu':1,'diameter':1,'density_ratio':1,'dt':1,'old_particle_velocity':0,'gravity':0,'carrier_direction':'one positive coordinate axis'},'idealized_branch_jump':enclosed,'python_transcription_controls':measures,'exact_radial_sensitivity_controls':controls,'radial_formula':'x/(1+x)+p*theta*x/(1+x)^2','positive_margin_formula':'(1+(1-p*theta)*x)/(1+x)^2','viscosity_elasticity_formula':'(1+(1-p)*z)/(1+z) = 1-p*theta','viscosity_elasticity_bounds':{'lower_limit':str(1-p),'upper_limit':'1'},'symbolic_family_assumptions':'Fixed positive density/diameter/viscosity, zero body force; within one Reynolds branch; x=dt*Dc, z=0.15*Re^p, theta=z/(1+z)','environment':{'python':sys.version,'platform':platform.platform()},'limits':['Body-force-free fixed positive properties; actual trajectories/fields not executed','Real branch limits with decoded binary64 literals; Python two-float quotients are not continuous derivatives','Continuous and constant variants are negative controls, not production fixes','No native OpenFOAM binary equivalence, physical transition, viscosity law or violated contract claim']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(result['status'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.output,a.source_commit)
