// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only replay of a frozen local witness; no field writes or evolution.
#include "argList.H"
#include "Time.H"
#include "fvMesh.H"
#include "volFields.H"
#include "interpolationCellPoint.H"
#include "polyMeshTetDecomposition.H"
#include <fstream>
#include <iomanip>
#include <cmath>
using namespace Foam;
namespace {
void vec(std::ostream& s,const vector& v) {s<<','<<v.x()<<','<<v.y()<<','<<v.z();}
}
int main(int argc,char* argv[]) {
    #include "setRootCase.H"
    #include "createTime.H"
    runTime.setTime(0.05,1);
    fvMesh mesh(IOobject(fvMesh::defaultRegion,runTime.name(),runTime,IOobject::MUST_READ));
    volVectorField U(IOobject("U",runTime.name(),mesh,IOobject::MUST_READ,IOobject::NO_WRITE),mesh);
    interpolationCellPoint<vector> interpolation(U);
    #include "frozenTarget.H"
    List<tetIndices> tets=polyMeshTetDecomposition::cellTetIndices(mesh,cell);
    label target=-1;
    forAll(tets,i) if(tets[i].face()==face && tets[i].tetPt()==tetPt) target=i;
    if(target<0) FatalErrorInFunction<<"Frozen witness missing"<<exit(FatalError);
    const tetIndices& index=tets[target]; const triFace tri=index.faceTriIs(mesh);
    const tetPointRef tet=index.tet(mesh);
    point nodes[4]={mesh.cellCentres()[cell],mesh.points()[tri[0]],mesh.points()[tri[1]],mesh.points()[tri[2]]};
    vector values[4]={U[cell],interpolation.psip()[tri[0]],interpolation.psip()[tri[1]],interpolation.psip()[tri[2]]};
    std::ofstream ns("/capture/nodes.csv"),qs("/capture/queries.csv"),cs("/capture/candidates.csv");
    for(auto* s:{&ns,&qs,&cs}) {
        if(!s->good()) FatalErrorInFunction<<"Cannot write replay"<<exit(FatalError);
        *s<<std::setprecision(17);
    }
    ns<<"node,label,x,y,z,Ux,Uy,Uz\n";
    for(label i=0;i<4;++i) {ns<<i<<','<<(i==0?cell:tri[i-1]);vec(ns,nodes[i]);vec(ns,values[i]);ns<<'\n';}
    qs<<"query,axis,h,sign,x,y,z,p0,p1,p2,w0,w1,w2,w3,Ux,Uy,Uz,Ex,Ey,Ez,det,first_face,first_tetPt\n";
    cs<<"query,ordinal,face,tetPt,p0,p1,p2,det,cellV,tol,w0,w1,w2,w3,accepted\n";
    const point centre=(nodes[0]+nodes[1]+nodes[2]+nodes[3])/4;
    cellPointWeight::debug=1;
    auto sample=[&](label q,label axis,scalar h,label sign) {
        point position=centre;if(axis>=0) position[axis]+=sign*h;
        cellPointWeight cpw(mesh,position,cell);
        vector actual=interpolation.interpolate(position,cell);
        barycentric targetWeights;scalar determinant=tet.pointToBarycentric(position,targetWeights);
        vector explicitValue=interpolation.interpolate(targetWeights,index);
        label first=-1;
        forAll(tets,i) {
            barycentric w;scalar d=tets[i].tet(mesh).pointToBarycentric(position,w);
            bool accepted=mag(d/mesh.cellVolumes()[cell])>cellPointWeight::tol
                && w[0]+cellPointWeight::tol>0 && w[1]+cellPointWeight::tol>0
                && w[2]+cellPointWeight::tol>0 && w[0]+w[1]+w[2]<1+cellPointWeight::tol;
            if(accepted && first<0) first=i;
            triFace ftri=tets[i].faceTriIs(mesh);
            cs<<q<<','<<i<<','<<tets[i].face()<<','<<tets[i].tetPt()
              <<','<<ftri[0]<<','<<ftri[1]<<','<<ftri[2]<<','<<d<<','<<mesh.cellVolumes()[cell]<<','<<cellPointWeight::tol;
            for(label j=0;j<4;++j)cs<<','<<w[j];cs<<','<<accepted<<'\n';
        }
        qs<<q<<','<<axis<<','<<h<<','<<sign;vec(qs,position);
        for(label j=0;j<3;++j)qs<<','<<cpw.faceVertices()[j];
        for(label j=0;j<4;++j)qs<<','<<cpw.weights()[j];
        vec(qs,actual);vec(qs,explicitValue);qs<<','<<determinant<<','<<(first<0?-1:tets[first].face())
          <<','<<(first<0?-1:tets[first].tetPt())<<'\n';
    };
    label q=0;sample(q++,-1,0,0);
    for(int power:{14,16,18}) for(label axis=0;axis<3;++axis) for(label sign:{-1,1})
        sample(q++,axis,std::ldexp(1.0,-power),sign);
    Info<<"CELL_POINT_QUERY_REPLAY_COMPLETE queries="<<q<<nl;
    return 0;
}
