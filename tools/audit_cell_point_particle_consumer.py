"""Pin one carrier-velocity consumer and a conditional frozen-drag sensitivity."""
import argparse,json,subprocess,hashlib
from pathlib import Path
import sympy as sp
from tools.audit_cell_point_contract import PIN

FILES=('src/lagrangian/solidParticle/solidParticleCloud.C','src/lagrangian/solidParticle/solidParticle.C','src/lagrangian/solidParticle/solidParticleI.H')


def audit(source,output,analysis_commit):
    source=Path(source);output=Path(output)
    if output.exists():raise FileExistsError('preserve previous consumer audit')
    records=[];texts={}
    for name in FILES:
        data=subprocess.check_output(['git','-C',str(source),'show',PIN+':'+name])
        if (source/name).read_bytes()!=data:raise ValueError('local consumer differs from pinned Git blob')
        texts[name]=data.decode();records.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'url':'https://github.com/OpenFOAM/OpenFOAM-13/blob/'+PIN+'/'+name})
    cloud=texts[FILES[0]];particle=texts[FILES[1]]
    expected={FILES[0]:['interpolationCellPoint<vector> UInterp(U);'],FILES[1]:['trackToAndHitFace(f*trackTime*U_, f, cloud, td);','vector Uc = td.UInterp().interpolate(this->coordinates(), tetIs);','scalar Re = magUr*d_/nuc;','U_ = (U_ + dt*(Dc*Uc + (1.0 - rhoc/rhop)*td.g()))/(1.0 + dt*Dc);']}
    lines={}
    for name,fragments in expected.items():
        lines[name]={}
        for fragment in fragments:
            matches=[i+1 for i,line in enumerate(texts[name].splitlines()) if fragment in line]
            if len(matches)!=1:raise ValueError('source signature absent or ambiguous')
            lines[name][fragment]=matches[0]
    dt,dc=sp.symbols('dt Dc',nonnegative=True);old,carrier,body=sp.symbols('U_old U_carrier body')
    update=(old+dt*(dc*carrier+body))/(1+dt*dc);gain=sp.simplify(sp.diff(update,carrier))
    assert sp.simplify(gain-dt*dc/(1+dt*dc))==0
    controls=0
    for h in (sp.Rational(0),sp.Rational(1,100),sp.Rational(1,2),sp.Integer(1),sp.Integer(10)):
        for d in (0,1,3,100):
            a=gain.subs({dt:h,dc:d});assert a>=0 and a<1;controls+=1
    result={'status':'PINNED_CONSUMER_TRACE_AND_CONDITIONAL_SYMBOLIC_SENSITIVITY','upstream_commit':PIN,'analysis_source_commit':analysis_commit,'sources':records,'source_lines':lines,'frozen_dc_velocity_gain':str(gain),'exact_nonnegative_parameter_controls':controls,'limits':['Source trace only; no solidParticleCloud execution or trajectory experiment','Frozen nonnegative Dc and body term only; actual Dc depends on relative speed, viscosity, diameter and density','Particle tracking uses U_, not direct Uc advection; carrier-field divergence does not equal particle-volume rate','No violated divergence-preservation contract, upstream defect or physical viscosity claim']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.source,a.output,a.source_commit)
