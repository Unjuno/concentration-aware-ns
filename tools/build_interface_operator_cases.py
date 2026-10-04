"""Build aligned planar Couette inputs for an OpenFOAM Foundation 13 probe.

Generation does not run blockMesh, a diffusion solve, or a Navier--Stokes
solver.  The nonuniform arrays assume blockMesh's single-block ordering:
x varies fastest, followed by y and z.  A runtime probe must check that
assumption against the mesh cell centres before interpreting field data.
"""

import argparse
import hashlib
import json
import math
from numbers import Integral, Real
from pathlib import Path


NY = NZ = 2
DEFAULT_RESOLUTIONS = (16, 32, 64)
APPLICATION = "interfaceOperatorProbe"
PATCH_FACES = {
    "xm": (0, 4, 7, 3),
    "xp": (1, 2, 6, 5),
    "ym": (0, 1, 5, 4),
    "yp": (3, 7, 6, 2),
    "zm": (0, 3, 2, 1),
    "zp": (4, 5, 6, 7),
}
CYCLIC_PAIRS = {"ym": "yp", "yp": "ym", "zm": "zp", "zp": "zm"}


def _finite_real(name, value, *, positive=False, nonzero=False):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number")
    try:
        value = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{name} must be a finite real number") from error
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if nonzero and value == 0:
        raise ValueError(f"{name} must be nonzero")
    return value


def _parameters(nx, mu_left, mu_right, traction):
    if isinstance(nx, bool) or not isinstance(nx, Integral) or nx < 2 or nx % 2:
        raise ValueError("nx must be an even integer >= 2")
    mu_left = _finite_real("mu_left", mu_left, positive=True)
    mu_right = _finite_real("mu_right", mu_right, positive=True)
    traction = _finite_real("traction", traction, nonzero=True)
    for coefficient in (mu_left, mu_right):
        if not math.isfinite(traction / coefficient):
            raise ValueError("traction / mu must give finite wall and cell values")
    return {
        "nx": int(nx), "ny": NY, "nz": NZ,
        "bounds": {"x": [-1.0, 1.0], "y": [0.0, 1.0], "z": [0.0, 1.0]},
        "interface_x": 0.0, "density": 1.0,
        "mu_left": mu_left, "mu_right": mu_right, "traction": traction,
    }


def _canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _number(value):
    return format(value, ".17g")


def _foam_file(path, body, kind="dictionary"):
    location = path.parent.as_posix()
    return (
        "FoamFile\n{\n"
        "    version 2.0;\n    format ascii;\n"
        f"    class {kind};\n    location \"{location}\";\n"
        f"    object {path.name};\n}}\n\n{body}\n"
    )


def _boundary_field(left, right, *, vector=False):
    def value(number):
        return f"(0 {_number(number)} 0)" if vector else _number(number)

    entries = [
        f"    xm {{ type fixedValue; value uniform {value(left)}; }}",
        f"    xp {{ type fixedValue; value uniform {value(right)}; }}",
    ]
    entries.extend(f"    {name} {{ type cyclic; }}" for name in CYCLIC_PAIRS)
    return "boundaryField\n{\n" + "\n".join(entries) + "\n}"


def generate(root, nx=16, mu_left=1.0, mu_right=100.0, traction=1.0):
    """Write one new case, refusing existing files, directories and symlinks.

    The walls prescribe the exact continuum values.  Fixed coefficient wall
    values retain the one-sided material coefficient at each half-cell wall
    resistance.  The coefficient field has kinematic-viscosity dimensions;
    with density one its numerical value equals the dynamic viscosity.
    """
    parameters = _parameters(nx, mu_left, mu_right, traction)
    root = Path(root)
    if root.exists() or root.is_symlink():
        raise ValueError("refusing to overwrite an existing case")

    nx = parameters["nx"]
    mu_left, mu_right, traction = (
        parameters[key] for key in ("mu_left", "mu_right", "traction")
    )
    h = 2.0 / nx
    centres = [
        [-1.0 + (i + 0.5) * h, (j + 0.5) / NY, (k + 0.5) / NZ]
        for k in range(NZ) for j in range(NY) for i in range(nx)
    ]
    coefficients = [mu_left if point[0] < 0 else mu_right for point in centres]
    shear = [traction * point[0] / mu for point, mu in zip(centres, coefficients)]
    left_wall, right_wall = -traction / mu_left, traction / mu_right

    vertices = [
        (-1, 0, 0), (1, 0, 0), (1, 1, 0), (-1, 1, 0),
        (-1, 0, 1), (1, 0, 1), (1, 1, 1), (-1, 1, 1),
    ]
    mesh_boundary = []
    for name, face in PATCH_FACES.items():
        face_text = " ".join(map(str, face))
        patch_type = (
            f"type cyclic; neighbourPatch {CYCLIC_PAIRS[name]};"
            if name in CYCLIC_PAIRS else "type wall;"
        )
        mesh_boundary.append(f"    {name} {{ {patch_type} faces (({face_text})); }}")
    mesh = (
        "scale 1;\nvertices\n(\n"
        + "\n".join("    (" + " ".join(map(str, row)) + ")" for row in vertices)
        + "\n);\n"
        + f"blocks (hex (0 1 2 3 4 5 6 7) ({nx} {NY} {NZ}) simpleGrading (1 1 1));\n"
        + "edges ();\nboundary\n(\n" + "\n".join(mesh_boundary)
        + "\n);\nmergePatchPairs ();"
    )
    control = f"""application {APPLICATION};
startFrom startTime;
startTime 0;
stopAt endTime;
endTime 1;
deltaT 1;
writeControl timeStep;
writeInterval 1;
purgeWrite 0;
writeFormat ascii;
writePrecision 17;
writeCompression off;
timeFormat general;
timePrecision 12;
runTimeModifiable false;"""
    schemes = """ddtSchemes { default steadyState; }
gradSchemes { default Gauss linear; }
divSchemes { default none; }
laplacianSchemes { default Gauss linear orthogonal; }
interpolationSchemes { default linear; }
snGradSchemes { default orthogonal; }
fluxRequired { default no; shear; constantControl; }"""
    solution = """solvers
{
    shear
    {
        solver PCG;
        preconditioner DIC;
        tolerance 1e-12;
        relTol 0;
    }
}"""

    def scalar_list(values):
        return "\n".join("    " + _number(value) for value in values)

    velocity_values = "\n".join(f"    (0 {_number(value)} 0)" for value in shear)
    count = len(centres)
    velocity = (
        "dimensions [0 1 -1 0 0 0 0];\n"
        f"internalField nonuniform List<vector>\n{count}\n(\n{velocity_values}\n);\n"
        + _boundary_field(left_wall, right_wall, vector=True)
    )
    shear_field = (
        "dimensions [0 1 -1 0 0 0 0];\n"
        f"internalField nonuniform List<scalar>\n{count}\n(\n{scalar_list(shear)}\n);\n"
        + _boundary_field(left_wall, right_wall)
    )
    mu_field = (
        "dimensions [0 2 -1 0 0 0 0];\n"
        f"internalField nonuniform List<scalar>\n{count}\n(\n{scalar_list(coefficients)}\n);\n"
        + _boundary_field(mu_left, mu_right)
    )
    constant_control = (
        "dimensions [0 1 -1 0 0 0 0];\ninternalField uniform 1;\n"
        + _boundary_field(1, 1)
    )
    bodies = {
        "system/blockMeshDict": (mesh, "dictionary"),
        "system/controlDict": (control, "dictionary"),
        "system/fvSchemes": (schemes, "dictionary"),
        "system/fvSolution": (solution, "dictionary"),
        "0/U": (velocity, "volVectorField"),
        "0/shear": (shear_field, "volScalarField"),
        "0/mu": (mu_field, "volScalarField"),
        "0/constantControl": (constant_control, "volScalarField"),
    }
    files = {
        name: _foam_file(Path(name), body, kind).encode("utf-8")
        for name, (body, kind) in bodies.items()
    }
    metadata = {
        "schema": "planar-couette-operator-case/v1",
        "target": "OpenFOAM Foundation 13",
        "application": APPLICATION,
        "purpose": "scalar diffusion and velocity-gradient operator probe inputs",
        "execution_status": "NOT_RUN",
        "inputs": parameters,
        "inputs_sha256": _sha256(_canonical_json(parameters).encode("utf-8")),
        "generator_sha256": _sha256(Path(__file__).read_bytes()),
        "mesh": {
            "cell_count": count,
            "spacing": [h, 1.0 / NY, 1.0 / NZ],
            "cell_order": "x-fastest, then y, then z; cell=i+nx*(j+ny*k)",
            "cell_centres": centres,
            "interface": {"axis": "x", "x": 0.0, "face_index_along_x": nx // 2},
            "patch_faces": {name: list(face) for name, face in PATCH_FACES.items()},
            "cyclic_pairs": dict(CYCLIC_PAIRS),
        },
        "continuum": {
            "velocity": "(0, traction*x/mu_side, 0)",
            "wall_shear": {"xm": left_wall, "xp": right_wall},
            "interface_velocity_trace": [0.0, 0.0, 0.0],
            "viscous_shear_traction": traction,
            "density": 1.0,
            "pressure": "constant (not needed by the scalar utility)",
        },
        "constant_control": {
            "field": "constantControl", "value": 1.0,
            "purpose": "constant null-mode diffusion and cyclic matrix residual diagnostic",
        },
        "files_sha256": {name: _sha256(data) for name, data in files.items()},
    }

    # All validation and formatting finish before the destination is created.
    root.mkdir(parents=True, exist_ok=False)
    (root / "constant").mkdir()
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(data)
    (root / "case_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return metadata


def build_cases(root, nx_values=DEFAULT_RESOLUTIONS, mu_left=1.0, mu_right=100.0,
                traction=1.0):
    """Write a fresh collection, defaulting to the preregistered 16/32/64 grids."""
    parameters = [_parameters(nx, mu_left, mu_right, traction) for nx in nx_values]
    if not parameters or len({row["nx"] for row in parameters}) != len(parameters):
        raise ValueError("nx_values must contain distinct even resolutions")
    root = Path(root)
    if root.exists() or root.is_symlink():
        raise ValueError("refusing to overwrite an existing case collection")
    root.mkdir(parents=True, exist_ok=False)
    return [generate(root / f"nx{row['nx']}", row["nx"], mu_left, mu_right, traction)
            for row in parameters]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--nx", type=int, nargs="+", default=DEFAULT_RESOLUTIONS)
    parser.add_argument("--mu-left", type=float, default=1.0)
    parser.add_argument("--mu-right", type=float, default=100.0)
    parser.add_argument("--traction", type=float, default=1.0)
    args = parser.parse_args()
    metadata = build_cases(args.directory, args.nx, args.mu_left, args.mu_right,
                           args.traction)
    print(json.dumps({"execution_status": "NOT_RUN", "nx": [
        row["inputs"]["nx"] for row in metadata
    ]}, sort_keys=True))


if __name__ == "__main__":
    main()
