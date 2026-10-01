"""Create an isolated Foundation-13 incompressible module with AMR snapshots.

The instrumented copy writes cell U/p and face phi/Uf at five solver stages
when topology changes at t=0.003. It does not modify the equation assembly.
The caller must provide the exact pinned source checkout and a fresh output
directory; the canonical source tree is never modified.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


PINNED_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
PINNED_FILES = {
    "applications/modules/incompressibleFluid/incompressibleFluid.H":
        "8781de41392ad7dc30d65c80d6cc4564744d16c672eaeede6fcdbce5571173b7",
    "applications/modules/incompressibleFluid/incompressibleFluid.C":
        "07435202057db9850178690b61b4bc99cf46202cac9b0e78163a5f6ff52ae9d5",
    "applications/modules/incompressibleFluid/moveMesh.C":
        "f6543b7b004e67221d0a977d926198f0b0f6d56dd63d1d8647c887a457c9612e",
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def replace_once(path, before, after):
    text = path.read_text()
    count = text.count(before)
    if count != 1:
        raise ValueError(f"expected one patch anchor in {path}, found {count}: {before[:80]!r}")
    path.write_text(text.replace(before, after, 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_tree", type=Path)
    parser.add_argument("output_module", type=Path)
    args = parser.parse_args()
    source = args.source_tree.resolve()
    output = args.output_module.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    commit = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if commit != PINNED_COMMIT:
        raise ValueError(f"expected Foundation source {PINNED_COMMIT}, got {commit}")

    module_rel = Path("applications/modules/incompressibleFluid")
    module_source = source / module_rel
    for rel, expected in PINNED_FILES.items():
        actual = sha(source / rel)
        if actual != expected:
            raise ValueError(f"pinned source hash mismatch for {rel}: {actual}")
    shutil.copytree(module_source, output)

    header = output / "incompressibleFluid.H"
    replace_once(
        header,
        "        void continuityErrors();\n\n        //- Construct the pressure equation",
        "        void continuityErrors();\n\n"
        "        //- Write read-only AMR stage snapshots for the frozen diagnostic\n"
        "        void writeAmrSnapshot(const word& stage) const;\n\n"
        "        //- Construct the pressure equation",
    )

    source_c = output / "incompressibleFluid.C"
    replace_once(
        source_c,
        '#include "addToRunTimeSelectionTable.H"\n',
        '#include "addToRunTimeSelectionTable.H"\n'
        '#include "OFstream.H"\n'
        '#include "OSspecific.H"\n',
    )
    snapshot_method = r'''void Foam::solvers::incompressibleFluid::writeAmrSnapshot
(
    const word& stage
) const
{
    // Frozen checkpoint for the first-refinement instrumentation protocol.
    if (!mesh.topoChanged() || mag(runTime.value() - 0.003) > 1e-12)
    {
        return;
    }

    const fileName dir
    (
        runTime.path()/"postProcessing"/"amrStages"/runTime.name()
    );
    mkDir(dir);

    OFstream cells(dir/(stage + "_cells.csv"));
    cells.precision(17);
    cells << "cell,cx,cy,cz,V,Ux,Uy,Uz,p\n";
    const vectorField& C = mesh.C();
    forAll(U_, celli)
    {
        cells << celli << ','
              << C[celli].x() << ',' << C[celli].y() << ',' << C[celli].z()
              << ',' << mesh.V()[celli]
              << ',' << U_[celli].x() << ',' << U_[celli].y() << ','
              << U_[celli].z() << ',' << p_[celli] << '\n';
    }

    OFstream faces(dir/(stage + "_faces.csv"));
    faces.precision(17);
    faces << "face,owner,neighbour,cx,cy,cz,Sx,Sy,Sz,phi,Ufx,Ufy,Ufz\n";
    const vectorField& Cf = mesh.Cf();
    const vectorField& Sf = mesh.Sf();
    const labelUList& owner = mesh.owner();
    const labelUList& neighbour = mesh.neighbour();
    forAll(phi_, facei)
    {
        const vector UfFace = Uf.valid() ? Uf()[facei] : vector::zero;
        const label nei = facei < mesh.nInternalFaces() ? neighbour[facei] : -1;
        faces << facei << ',' << owner[facei] << ',' << nei << ','
              << Cf[facei].x() << ',' << Cf[facei].y() << ',' << Cf[facei].z()
              << ',' << Sf[facei].x() << ',' << Sf[facei].y() << ','
              << Sf[facei].z() << ',' << phi_[facei]
              << ',' << UfFace.x() << ',' << UfFace.y() << ',' << UfFace.z()
              << '\n';
    }

    Info<< "AMR_STAGE_SNAPSHOT stage=" << stage
        << " time=" << runTime.name()
        << " cells=" << mesh.nCells()
        << " internalFaces=" << mesh.nInternalFaces() << endl;
}


'''
    replace_once(
        source_c,
        "void Foam::solvers::incompressibleFluid::continuityErrors()\n"
        "{\n    fluidSolver::continuityErrors(phi);\n}\n\n\n",
        "void Foam::solvers::incompressibleFluid::continuityErrors()\n"
        "{\n    fluidSolver::continuityErrors(phi);\n}\n\n\n" + snapshot_method,
    )
    replace_once(
        source_c,
        "    mesh_.update();\n}\n\n\nvoid Foam::solvers::incompressibleFluid::prePredictor()",
        "    mesh_.update();\n    writeAmrSnapshot(\"mapped\");\n}\n\n\n"
        "void Foam::solvers::incompressibleFluid::prePredictor()",
    )
    replace_once(
        source_c,
        "void Foam::solvers::incompressibleFluid::postSolve()\n{}",
        "void Foam::solvers::incompressibleFluid::postSolve()\n"
        "{\n    writeAmrSnapshot(\"postSolve\");\n}",
    )
    replace_once(
        source_c,
        "void Foam::solvers::incompressibleFluid::pressureCorrector()\n{\n"
        "    while (pimple.correct())\n    {\n        correctPressure();\n    }\n\n"
        "    tUEqn.clear();\n}",
        "void Foam::solvers::incompressibleFluid::pressureCorrector()\n{\n"
        "    writeAmrSnapshot(\"prePressure\");\n"
        "    while (pimple.correct())\n    {\n        correctPressure();\n    }\n"
        "    writeAmrSnapshot(\"postPressure\");\n\n"
        "    tUEqn.clear();\n}",
    )

    move_mesh = output / "moveMesh.C"
    replace_once(
        move_mesh,
        "                // Make the flux relative to the mesh motion\n"
        "                MRF.makeRelative(phi_);\n"
        "                fvc::makeRelative(phi_, U);",
        "                // Make the flux relative to the mesh motion\n"
        "                MRF.makeRelative(phi_);\n"
        "                fvc::makeRelative(phi_, U);\n\n"
        "                if (pimple.firstIter())\n"
        "                {\n"
        "                    writeAmrSnapshot(\"afterCorrectPhi\");\n"
        "                }",
    )

    result = {
        "source_commit": commit,
        "source_file_sha256": PINNED_FILES,
        "instrumented_file_sha256": {
            name: sha(output / name)
            for name in ("incompressibleFluid.H", "incompressibleFluid.C", "moveMesh.C")
        },
        "instrumentation": [
            "mapped", "afterCorrectPhi", "prePressure", "postPressure", "postSolve"
        ],
        "checkpoint": "mesh.topoChanged() at t=0.003",
        "changes_equation_assembly": False,
        "output": "postProcessing/amrStages/<time>/{stage}_cells.csv and {stage}_faces.csv",
    }
    (output / "instrumentation-provenance.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
