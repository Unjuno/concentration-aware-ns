// SPDX-License-Identifier: GPL-3.0-or-later
// Read-only reconstruction capture; no evolution, field write or solver change.
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
void vectorCsv(std::ostream& os, const vector& v) {
    os << ',' << v.x() << ',' << v.y() << ',' << v.z();
}
}

int main(int argc, char *argv[]) {
    #include "setRootCase.H"
    #include "createTime.H"
    runTime.setTime(0.05, 1);
    fvMesh mesh(IOobject(fvMesh::defaultRegion, runTime.name(), runTime, IOobject::MUST_READ));
    volVectorField U(IOobject("U",runTime.name(),mesh,IOobject::MUST_READ,IOobject::NO_WRITE),mesh);
    interpolationCellPoint<vector> interpolation(U);
    const pointField& points=mesh.points();
    const vectorField& centres=mesh.cellCentres();
    const auto& pointValues=interpolation.psip();
    const labelList& bases=mesh.tetBasePtIs();
    std::ofstream cells("/capture/cells.csv"), vertices("/capture/points.csv"),
                  tets("/capture/tets.csv"), faces("/capture/faces.csv");
    for (auto* s : {&cells,&vertices,&tets,&faces}) {
        if (!s->good()) FatalErrorInFunction << "Cannot create capture files" << exit(FatalError);
        *s << std::setprecision(17);
    }
    cells << "cell,V,cx,cy,cz,Ux,Uy,Uz,Ix,Iy,Iz\n";
    vertices << "point,x,y,z,Ux,Uy,Uz\n";
    tets << "cell,face,tetPt,p0,p1,p2,det,volume,w0,w1,w2,w3\n";
    faces << "face,owner,neighbour,base,cx,cy,cz,Ox,Oy,Oz,Nx,Ny,Nz\n";
    forAll(points,p) {
        vertices << p; vectorCsv(vertices,points[p]);vectorCsv(vertices,pointValues[p]);vertices << '\n';
    }
    scalar maximumCentreError=0, minimumAbsDet=great;
    label tetCount=0, nearDegenerate=0, invalidBase=0;
    forAll(U,c) {
        vector sampled=interpolation.interpolate(centres[c],c);
        maximumCentreError=max(maximumCentreError,mag(sampled-U[c]));
        cells << c << ',' << mesh.cellVolumes()[c];vectorCsv(cells,centres[c]);
        vectorCsv(cells,U[c]);vectorCsv(cells,sampled);cells << '\n';
        List<tetIndices> indices=polyMeshTetDecomposition::cellTetIndices(mesh,c);
        forAll(indices,k) {
            const tetIndices& index=indices[k];
            const triFace tri=index.faceTriIs(mesh);
            const tetPointRef tet=index.tet(mesh);
            barycentric weights;
            scalar determinant=tet.pointToBarycentric(centres[c],weights);
            minimumAbsDet=min(minimumAbsDet,mag(determinant));
            if (mag(determinant)<small) ++nearDegenerate;
            tets << c << ',' << index.face() << ',' << index.tetPt()
                 << ',' << tri[0] << ',' << tri[1] << ',' << tri[2]
                 << ',' << determinant << ',' << tet.mag()
                 << ',' << weights[0] << ',' << weights[1] << ',' << weights[2] << ',' << weights[3] << '\n';
            ++tetCount;
        }
    }
    scalar maximumFaceError=0;
    forAll(bases,f) if(bases[f]<0) ++invalidBase;
    for (label f=0;f<mesh.nInternalFaces();++f) {
        label owner=mesh.faceOwner()[f], neighbour=mesh.faceNeighbour()[f];
        vector o=interpolation.interpolate(mesh.faceCentres()[f],owner);
        vector n=interpolation.interpolate(mesh.faceCentres()[f],neighbour);
        maximumFaceError=max(maximumFaceError,mag(o-n));
        faces << f << ',' << owner << ',' << neighbour << ',' << bases[f];
        vectorCsv(faces,mesh.faceCentres()[f]);vectorCsv(faces,o);vectorCsv(faces,n);faces << '\n';
    }
    std::ofstream summary("/capture/summary.json");summary << std::setprecision(17)
        << "{\"cells\":" << mesh.nCells() << ",\"points\":" << mesh.nPoints()
        << ",\"internal_faces\":" << mesh.nInternalFaces() << ",\"tets\":" << tetCount
        << ",\"near_degenerate_tets\":" << nearDegenerate
        << ",\"invalid_face_base_indices\":" << invalidBase
        << ",\"small\":" << small << ",\"minimum_abs_det\":" << minimumAbsDet
        << ",\"maximum_centre_interpolation_error\":" << maximumCentreError
        << ",\"maximum_internal_face_trace_difference\":" << maximumFaceError << "}\n";
    Info << "CELL_POINT_CAPTURE_COMPLETE cells=" << mesh.nCells() << " tets=" << tetCount << nl;
    return 0;
}
