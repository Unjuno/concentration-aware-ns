#include "argList.H"
#include "Time.H"
#include "fvMesh.H"
#include "fvMatrices.H"
#include "OFstream.H"
#include "OSspecific.H"
#include "surfaceInterpolate.H"
#include "fvcGrad.H"
#include "fvcSnGrad.H"
#include "fvcFlux.H"
#include "fvcDiv.H"
#include "fvmLaplacian.H"

#include <cmath>

// A source-informed operator probe. Its JSON keeps the native residual separate
// from the boundary-complete matrix and the independently integrated face flux.
// In particular, the scalar residual specialization is not the generic path in
// fvMatrixSolve.C. No pressure, transport, or constitutive model is solved here.

namespace
{
using namespace Foam;

IOobject diagnosticIO(const word& name, const fvMesh& mesh)
{
    return IOobject
    (
        name, mesh.time().name(), mesh,
        IOobject::NO_READ, IOobject::NO_WRITE, false
    );
}

void jsonString(Ostream& os, const string& value)
{
    static const char hex[] = "0123456789abcdef";
    os << '"';
    for (const char ch : value)
    {
        const unsigned char c = static_cast<unsigned char>(ch);
        switch (c)
        {
            case '"': os << "\\\""; break;
            case '\\': os << "\\\\"; break;
            case '\n': os << "\\n"; break;
            case '\r': os << "\\r"; break;
            case '\t': os << "\\t"; break;
            case '\b': os << "\\b"; break;
            case '\f': os << "\\f"; break;
            default:
                if (c < 0x20)
                {
                    os << "\\u00" << hex[c >> 4] << hex[c & 15];
                }
                else
                {
                    os << ch;
                }
        }
    }
    os << '"';
}

void jsonNumber(Ostream& os, const scalar value)
{
    if (!std::isfinite(static_cast<double>(value)))
    {
        FatalErrorInFunction << "A nonfinite probe value cannot be JSON"
            << exit(FatalError);
    }
    os << value;
}

template<class Values>
void jsonScalars(Ostream& os, const Values& values)
{
    os << '[';
    forAll(values, i)
    {
        if (i) os << ',';
        jsonNumber(os, values[i]);
    }
    os << ']';
}

template<class Values>
void jsonLabels(Ostream& os, const Values& values)
{
    os << '[';
    forAll(values, i)
    {
        if (i) os << ',';
        os << values[i];
    }
    os << ']';
}

template<class Values>
void jsonVectors(Ostream& os, const Values& values)
{
    os << '[';
    forAll(values, i)
    {
        if (i) os << ',';
        os << '[';
        jsonNumber(os, values[i].x()); os << ',';
        jsonNumber(os, values[i].y()); os << ',';
        jsonNumber(os, values[i].z()); os << ']';
    }
    os << ']';
}

template<class Values>
void jsonTensors(Ostream& os, const Values& values)
{
    os << '[';
    forAll(values, i)
    {
        if (i) os << ',';
        const tensor& t = values[i];
        const scalar components[] =
        {
            t.xx(), t.xy(), t.xz(), t.yx(), t.yy(), t.yz(),
            t.zx(), t.zy(), t.zz()
        };
        os << '[';
        for (label j = 0; j < 9; ++j)
        {
            if (j) os << ',';
            jsonNumber(os, components[j]);
        }
        os << ']';
    }
    os << ']';
}

void jsonDimensions(Ostream& os, const dimensionSet& dimensions)
{
    os << '[';
    for (label i = 0; i < 7; ++i)
    {
        if (i) os << ',';
        jsonNumber(os, dimensions[i]);
    }
    os << ']';
}

template<class Type>
Field<Type> allFaces(const SurfaceField<Type>& field)
{
    const fvMesh& mesh = field.mesh();
    Field<Type> values(mesh.nFaces(), pTraits<Type>::zero);
    forAll(field.primitiveField(), facei)
    {
        values[facei] = field[facei];
    }
    forAll(mesh.boundary(), patchi)
    {
        const fvPatch& patch = mesh.boundary()[patchi];
        forAll(patch, i)
        {
            values[patch.start() + i] = field.boundaryField()[patchi][i];
        }
    }
    return values;
}

template<class Type>
Field<Type> integratedDivergence(const SurfaceField<Type>& flux)
{
    const tmp<VolField<Type>> divergence = fvc::div(flux);
    Field<Type> values(divergence().primitiveField());
    forAll(values, celli)
    {
        values[celli] *= flux.mesh().V()[celli];
    }
    return values;
}

void writeExplicitCorrection
(
    Ostream& os,
    const fvMesh& mesh,
    const volVectorField& U,
    const volScalarField& mu,
    const surfaceScalarField& muArithmetic,
    const volScalarField& shear
)
{
    volVectorField evaluatedU(diagnosticIO("probeEvaluatedU", mesh), U);
    forAll(evaluatedU, celli)
    {
        evaluatedU.primitiveFieldRef()[celli].y() = shear[celli];
    }
    evaluatedU.correctBoundaryConditions();

    const volTensorField gradU
    (
        diagnosticIO("probeGradU", mesh), fvc::grad(evaluatedU)
    );
    const volTensorField G
    (
        diagnosticIO("probeTransposeCorrectionTensor", mesh), dev2(T(gradU))
    );
    const surfaceVectorField separateFlux
    (
        diagnosticIO("probeSeparateCorrectionFlux", mesh),
        -muArithmetic*fvc::dotInterpolate(mesh.Sf(), G)
    );
    const surfaceVectorField parentProductFlux
    (
        diagnosticIO("probeParentProductCorrectionFlux", mesh),
        fvc::flux(-mu*G)
    );

    os << "{\"coefficientMode\":\"arithmetic\",\"gradU\":";
    jsonTensors(os, gradU.primitiveField());
    os << ",\"dev2TransposeGradU\":";
    jsonTensors(os, G.primitiveField());
    os << ",\"separateFlux\":";
    jsonVectors(os, allFaces(separateFlux));
    os << ",\"parentProductFlux\":";
    jsonVectors(os, allFaces(parentProductFlux));
    os << ",\"divSeparateTimesVolume\":";
    jsonVectors(os, integratedDivergence(separateFlux));
    os << ",\"divParentProductTimesVolume\":";
    jsonVectors(os, integratedDivergence(parentProductFlux));
    os << '}';
}

void writeSnapshot
(
    const fileName& path,
    const word& mode,
    const word& stage,
    fvScalarMatrix& equation,
    const volScalarField& psi,
    const surfaceScalarField& gamma,
    const volVectorField* U,
    const volScalarField* mu,
    const surfaceScalarField* muArithmetic,
    const solverPerformance* performance
)
{
    const fvMesh& mesh = psi.mesh();
    const lduMatrix& storage = equation;
    const tmp<scalarField> completeDiag = equation.D();
    const tmp<scalarField> nativeResidual = equation.residual();
    const surfaceScalarField snGradPsi
    (
        diagnosticIO("probeSnGradPsi", mesh), fvc::snGrad(psi)
    );
    const surfaceScalarField physicalFlux
    (
        diagnosticIO("probePhysicalDiffusionFlux", mesh),
        gamma*mesh.magSf()*snGradPsi
    );
    const tmp<surfaceScalarField> matrixFlux = equation.flux();
    labelList faceNeighbours(mesh.nFaces(), -1);
    forAll(mesh.neighbour(), facei)
    {
        faceNeighbours[facei] = mesh.neighbour()[facei];
    }

    mkDir(path.path());
    OFstream os(path);
    os.precision(17);
    os << "{\"schemaVersion\":1,\"mode\":"; jsonString(os, mode);
    os << ",\"stage\":"; jsonString(os, stage);
    os << ",\"fieldName\":"; jsonString(os, psi.name());
    os << ",\"operator\":\"negative_fvm_laplacian\",\"fieldDimensions\":";
    jsonDimensions(os, psi.dimensions());
    os << ",\"equationDimensions\":";
    jsonDimensions(os, equation.dimensions());
    os << ",\"cells\":{\"centres\":";
    jsonVectors(os, mesh.C().primitiveField());
    os << ",\"volumes\":"; jsonScalars(os, mesh.V());
    os << ",\"values\":"; jsonScalars(os, psi.primitiveField());
    os << ",\"rawDiag\":"; jsonScalars(os, storage.diag());
    os << ",\"completeDiag\":"; jsonScalars(os, completeDiag());
    os << ",\"source\":"; jsonScalars(os, equation.source());
    os << ",\"nativeResidual\":"; jsonScalars(os, nativeResidual());
    os << ",\"divPhysicalFluxTimesVolume\":";
    jsonScalars(os, integratedDivergence(physicalFlux));
    os << "},\"internalMatrix\":{\"owner\":";
    jsonLabels(os, mesh.owner());
    os << ",\"neighbour\":"; jsonLabels(os, mesh.neighbour());
    os << ",\"upper\":"; jsonScalars(os, storage.upper());
    os << ",\"lower\":"; jsonScalars(os, storage.lower());
    os << ",\"symmetric\":" << (storage.symmetric() ? "true" : "false");
    os << ",\"hasLower\":" << (storage.hasLower() ? "true" : "false");
    os << "},\"faces\":{\"centres\":";
    jsonVectors(os, allFaces(mesh.Cf()));
    os << ",\"areas\":"; jsonVectors(os, allFaces(mesh.Sf()));
    os << ",\"owner\":"; jsonLabels(os, mesh.faceOwner());
    os << ",\"neighbour\":"; jsonLabels(os, faceNeighbours);
    os << ",\"gamma\":"; jsonScalars(os, allFaces(gamma));
    os << ",\"deltaCoeffs\":"; jsonScalars(os, allFaces(mesh.deltaCoeffs()));
    os << ",\"snGrad\":"; jsonScalars(os, allFaces(snGradPsi));
    os << ",\"physicalFlux\":"; jsonScalars(os, allFaces(physicalFlux));
    os << ",\"matrixFlux\":"; jsonScalars(os, allFaces(matrixFlux()));
    os << "},\"patches\":[";
    forAll(mesh.boundary(), patchi)
    {
        if (patchi) os << ',';
        const fvPatch& patch = mesh.boundary()[patchi];
        os << "{\"name\":"; jsonString(os, patch.name());
        os << ",\"type\":"; jsonString(os, patch.type());
        os << ",\"fieldType\":";
        jsonString(os, psi.boundaryField()[patchi].type());
        os << ",\"start\":" << patch.start() << ",\"size\":" << patch.size();
        os << ",\"coupled\":" << (patch.coupled() ? "true" : "false");
        os << ",\"faceCells\":"; jsonLabels(os, patch.faceCells());
        os << ",\"internalCoeffs\":";
        jsonScalars(os, equation.internalCoeffs()[patchi]);
        os << ",\"boundaryCoeffs\":";
        jsonScalars(os, equation.boundaryCoeffs()[patchi]);
        os << ",\"neighbourValues\":";
        if (psi.boundaryField()[patchi].coupled())
        {
            const tmp<scalarField> neighbourValues =
                psi.boundaryField()[patchi].patchNeighbourField();
            jsonScalars(os, neighbourValues());
        }
        else
        {
            os << "[]";
        }
        os << '}';
    }
    os << "],\"solverPerformance\":";
    if (performance)
    {
        os << "{\"initialResidual\":";
        jsonNumber(os, performance->initialResidual());
        os << ",\"finalResidual\":";
        jsonNumber(os, performance->finalResidual());
        os << ",\"iterations\":" << performance->nIterations() << '}';
    }
    else
    {
        os << "null";
    }
    os << ",\"explicitCorrection\":";
    if (U && mu && muArithmetic)
    {
        writeExplicitCorrection(os, mesh, *U, *mu, *muArithmetic, psi);
    }
    else
    {
        os << "null";
    }
    os << "}\n";
    os.flush();
    if (!os.good() || !os.stdStream().good())
    {
        FatalErrorInFunction << "Could not write probe snapshot " << path
            << exit(FatalError);
    }
}

void runCouetteMode
(
    const word& mode,
    const fvMesh& mesh,
    const volScalarField& originalShear,
    const volVectorField& U,
    const volScalarField& mu,
    const surfaceScalarField& gamma,
    const surfaceScalarField& muArithmetic
)
{
    volScalarField shear
    (
        diagnosticIO("shear_" + mode, mesh), originalShear
    );
    shear.correctBoundaryConditions();
    mesh.schemes().setFluxRequired(shear.name());
    fvScalarMatrix equation
    (
        -fvm::laplacian(gamma, shear, "laplacian(muFace,shear)")
    );
    const fileName directory(mesh.time().path()/"probe"/mode);
    writeSnapshot
    (
        directory/"before.json", mode, "before", equation, shear, gamma,
        &U, &mu, &muArithmetic, nullptr
    );
    const solverPerformance performance =
        equation.solve(mesh.solution().solverDict("shear"));
    writeSnapshot
    (
        directory/"after.json", mode, "after", equation, shear, gamma,
        &U, &mu, &muArithmetic, &performance
    );
}
}

int main(int argc, char* argv[])
{
    using namespace Foam;
    argList::noParallel();
    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"

    volVectorField U
    (
        IOobject("U", runTime.name(), mesh, IOobject::MUST_READ, IOobject::NO_WRITE),
        mesh
    );
    volScalarField shear
    (
        IOobject("shear", runTime.name(), mesh, IOobject::MUST_READ, IOobject::NO_WRITE),
        mesh
    );
    volScalarField mu
    (
        IOobject("mu", runTime.name(), mesh, IOobject::MUST_READ, IOobject::NO_WRITE),
        mesh
    );
    volScalarField constantControl
    (
        IOobject
        (
            "constantControl", runTime.name(), mesh,
            IOobject::MUST_READ, IOobject::NO_WRITE
        ),
        mesh
    );
    U.correctBoundaryConditions();
    shear.correctBoundaryConditions();
    mu.correctBoundaryConditions();
    constantControl.correctBoundaryConditions();

    const surfaceScalarField muArithmetic
    (
        diagnosticIO("muArithmetic", mesh), fvc::interpolate(mu)
    );
    surfaceScalarField muHarmonic
    (
        diagnosticIO("muHarmonic", mesh), muArithmetic
    );
    const surfaceScalarField& weights = mesh.weights();
    forAll(mesh.owner(), facei)
    {
        const scalar muP = mu[mesh.owner()[facei]];
        const scalar muN = mu[mesh.neighbour()[facei]];
        if (!(muP > 0 && muN > 0))
        {
            FatalErrorInFunction << "Positive cell coefficients are required"
                << exit(FatalError);
        }
        // reverseLinear weights encode the two series-resistance distances.
        const scalar w = weights[facei];
        muHarmonic.primitiveFieldRef()[facei] =
            1.0/((1.0 - w)/muP + w/muN);
    }

    runCouetteMode("arithmetic", mesh, shear, U, mu, muArithmetic, muArithmetic);
    runCouetteMode("harmonic", mesh, shear, U, mu, muHarmonic, muArithmetic);

    volScalarField constantPsi
    (
        diagnosticIO("constantControl_probe", mesh), constantControl
    );
    constantPsi.correctBoundaryConditions();
    mesh.schemes().setFluxRequired(constantPsi.name());
    const surfaceScalarField unitGamma
    (
        diagnosticIO("constantGamma", mesh), mesh,
        dimensionedScalar("one", mu.dimensions(), 1.0)
    );
    fvScalarMatrix constantEquation
    (
        -fvm::laplacian(unitGamma, constantPsi, "laplacian(muFace,shear)")
    );
    writeSnapshot
    (
        runTime.path()/"probe"/"constant"/"before.json",
        "constant", "before", constantEquation, constantPsi, unitGamma,
        nullptr, nullptr, nullptr, nullptr
    );
    Info << "INTERFACE_OPERATOR_PROBE_COMPLETE" << endl;
    return 0;
}
