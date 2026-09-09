"""Generate periodic Cartesian hexahedra and transient SU2 MMS pilot input."""
import argparse
import json
import math
from pathlib import Path


def generate(root,n=8,dt=.001,end=.005,inner=1000):
    root=Path(root);root.mkdir(parents=True,exist_ok=False)
    length=2*math.pi
    def node(i,j,k):return i+(n+1)*(j+(n+1)*k)
    with (root/'mesh.su2').open('w') as f:
        f.write(f'NDIME= 3\nNELEM= {n**3}\n')
        for k in range(n):
            for j in range(n):
                for i in range(n):
                    ids=[node(i+a,j+b,k+c) for a,b,c in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]]
                    f.write('12 '+' '.join(map(str,ids))+'\n')
        f.write(f'NPOIN= {(n+1)**3}\n')
        for k in range(n+1):
            for j in range(n+1):
                for i in range(n+1):f.write(f'{i*length/n:.17g} {j*length/n:.17g} {k*length/n:.17g} {node(i,j,k)}\n')
        f.write('NMARK= 6\n')
        for axis in range(3):
            for side in range(2):
                f.write(f'MARKER_TAG= {"xyz"[axis]}{side}\nMARKER_ELEMS= {n*n}\n')
                for b in range(n):
                    for a in range(n):
                        ids=[]
                        for da,db in [(0,0),(1,0),(1,1),(0,1)]:
                            xyz=[0,0,0];xyz[axis]=side*n;xyz[(axis+1)%3]=a+da;xyz[(axis+2)%3]=b+db
                            ids.append(node(*xyz))
                        if side==0:ids.reverse()
                        f.write('9 '+' '.join(map(str,ids))+'\n')
    periodic=[]
    for a in range(3):
        translation=[0.,0.,0.];translation[a]=length
        periodic.extend([f'{"xyz"[a]}0',f'{"xyz"[a]}1',*([0]*6),*translation])
    config=f'''SOLVER= INC_NAVIER_STOKES
KIND_VERIFICATION_SOLUTION= USER_DEFINED_SOLUTION
INC_DENSITY_MODEL= CONSTANT
INC_ENERGY_EQUATION= NO
INC_DENSITY_INIT= 1.0
INC_VELOCITY_INIT= (1.0, 0.0, 0.0)
INC_NONDIM= DIMENSIONAL
VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 0.01
TIME_DOMAIN= YES
TIME_MARCHING= DUAL_TIME_STEPPING-1ST_ORDER
TIME_STEP= {dt}
MAX_TIME= {end}
TIME_ITER= {round(end/dt)}
INNER_ITER= {inner}
CONV_FIELD= (RMS_PRESSURE, RMS_VELOCITY-X, RMS_VELOCITY-Y, RMS_VELOCITY-Z)
CONV_RESIDUAL_MINVAL= -10
CONV_STARTITER= 0
CFL_NUMBER= 10
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
NUM_METHOD_GRAD= GREEN_GAUSS
TIME_DISCRE_FLOW= EULER_IMPLICIT
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-10
LINEAR_SOLVER_ITER= 100
MGLEVEL= 0
MESH_FILENAME= mesh.su2
MESH_FORMAT= SU2
MARKER_PERIODIC= ({', '.join(map(str,periodic))})
OUTPUT_FILES= (RESTART_ASCII, PARAVIEW_ASCII)
OUTPUT_WRT_FREQ= 1
SCREEN_OUTPUT= (TIME_ITER, INNER_ITER, RMS_PRESSURE, RMS_VELOCITY-X, RMS_VELOCITY-Y, RMS_VELOCITY-Z)
HISTORY_OUTPUT= (ITER, RMS_RES, TIME_DOMAIN)
'''
    (root/'case.cfg').write_text(config)
    (root/'parameters.json').write_text(json.dumps({'n':n,'dt':dt,'end':end,'sigma':.5,'nu':.01,'status':'pilot; convergence unverified'},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('--n',type=int,default=8);args=p.parse_args();generate(args.root,args.n)
