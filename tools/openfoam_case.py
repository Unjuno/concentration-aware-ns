"""Generate a pilot periodic MMS case. Not a completed acceptance experiment."""
import argparse
import json
from pathlib import Path
import numpy as np
from tools.reference import fields


def generate(root, n=8, dt=0.001, end=0.005, sigma=0.5, nu=0.01):
    root = Path(root)
    if root.exists():
        raise ValueError('refusing to overwrite an existing case')
    if n < 4 or min(dt, end, sigma, nu) <= 0:
        raise ValueError('invalid case parameters')
    root.mkdir(parents=True)
    def write(path, body, kind='dictionary'):
        p = root / path
        p.parent.mkdir(exist_ok=True)
        p.write_text(f'FoamFile {{ format ascii; class {kind}; object {p.name}; }}\n'+body+'\n')
    L = 2*np.pi
    vertices = [(0,0,0),(L,0,0),(L,L,0),(0,L,0),(0,0,L),(L,0,L),(L,L,L),(0,L,L)]
    faces = [('xm','xp',(0,4,7,3)),('xp','xm',(1,2,6,5)),
             ('ym','yp',(0,1,5,4)),('yp','ym',(3,7,6,2)),
             ('zm','zp',(0,3,2,1)),('zp','zm',(4,5,6,7))]
    boundary = '\n'.join(f'{name} {{ type cyclic; neighbourPatch {peer}; faces (({" ".join(map(str,face))})); }}' for name,peer,face in faces)
    write('system/blockMeshDict', 'scale 1;\nvertices (\n'+ '\n'.join('('+ ' '.join(map(str,v))+')' for v in vertices)+f'\n);\nblocks (hex (0 1 2 3 4 5 6 7) ({n} {n} {n}) simpleGrading (1 1 1));\nedges ();\nboundary (\n'+boundary+'\n);')
    write('system/controlDict', f'''solver incompressibleFluid;
startFrom startTime; startTime 0; stopAt endTime; endTime {end}; deltaT {dt};
writeControl timeStep; writeInterval 1; writeFormat ascii; writePrecision 16;
writeCompression off; timeFormat general; timePrecision 12; runTimeModifiable false;''')
    write('system/fvSchemes', '''ddtSchemes { default Euler; }
gradSchemes { default Gauss linear; }
divSchemes { default none; div(phi,U) Gauss linear; div((nuEff*dev2(T(grad(U))))) Gauss linear; }
laplacianSchemes { default Gauss linear corrected; }
interpolationSchemes { default linear; }
snGradSchemes { default corrected; }''')
    write('system/fvSolution', '''solvers {
p { solver GAMG; tolerance 1e-10; relTol 0; smoother GaussSeidel; }
pFinal { $p; }
U { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-10; relTol 0; }
UFinal { $U; }
}
PIMPLE { nOuterCorrectors 3; nCorrectors 2; nNonOrthogonalCorrectors 0; pRefCell 0; pRefValue 0; }''')
    write('constant/momentumTransport', 'simulationType laminar;')
    write('constant/physicalProperties', f'viscosityModel constant; nu {nu} [m^2/s];')
    coordinates = (np.arange(n)+0.5)*L/n
    z,y,x = np.meshgrid(coordinates, coordinates, coordinates, indexing='ij')
    points = np.stack([x,y,z],axis=-1).reshape(-1,3)
    u = fields(points, sigma=sigma, nu=nu)['u']
    bcs = 'boundaryField {\n'+'\n'.join(f'{name} {{ type cyclic; }}' for name,_,_ in faces)+'\n}'
    values = '\n'.join('('+ ' '.join(f'{v:.17g}' for v in row)+')' for row in u)
    write('0/U', f'dimensions [0 1 -1 0 0 0 0];\ninternalField nonuniform List<vector>\n{len(u)}\n(\n{values}\n);\n'+bcs, 'volVectorField')
    write('0/p', 'dimensions [0 2 -2 0 0 0 0]; internalField uniform 0;\n'+bcs, 'volScalarField')
    code = '''mmsForce {
 type coded;
 cellZone all;
 field U;
 codeAddSup
 #{
 const scalar width = SIGMA, viscosity = NU;
 const scalar now = mesh().time().value();
 const vector a(1,2,3);
 const vectorField& centers = mesh().C();
 const scalarField& volumes = mesh().V();
 vectorField& source = eqn.source();
 forAll(centers, celli) {
   vector q, r, s;
   scalar exponent = -now;
   for (direction j=0; j<3; ++j) {
     const scalar d = centers[celli][j] - constant::mathematical::pi;
     q[j] = -sin(d)/sqr(width);
     r[j] = -cos(d)/sqr(width);
     s[j] = sin(d)/sqr(width);
     exponent += (cos(d)-1)/sqr(width);
   }
   const scalar psi = exp(exponent);
   const vector u = (psi*q)^a;
   vector conv = vector::zero;
   scalar trace = 0;
   for (direction j=0; j<3; ++j) {
     vector h = q*q[j];
     h[j] += r[j];
     conv += u[j]*((psi*h)^a);
     trace += sqr(q[j])+r[j];
   }
   vector lg;
   for (direction j=0; j<3; ++j) lg[j] = psi*(q[j]*trace+2*q[j]*r[j]+s[j]);
   const vector f = -u+conv-viscosity*(lg^a);
   source[celli] -= volumes[celli]*f;
 }
 #};
}'''.replace('SIGMA',repr(sigma)).replace('NU',repr(nu))
    write('constant/fvModels', code)
    (root/'parameters.json').write_text(json.dumps(dict(n=n,dt=dt,end=end,sigma=sigma,nu=nu,purpose='integration pilot, not production'),indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('--n',type=int,default=8)
    args=parser.parse_args()
    generate(args.directory,n=args.n)
