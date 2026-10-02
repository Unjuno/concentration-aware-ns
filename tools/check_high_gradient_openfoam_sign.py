"""Audit the localized MMS forcing sign against the pinned OF13 image sources.

This is a source-level equation-assembly check. It does not establish that the
installed package was built from a particular Git commit or validate numerical
accuracy in a completed solver run.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
FILES = {
    "momentumPredictor.C": "/opt/openfoam13/applications/modules/incompressibleFluid/momentumPredictor.C",
    "fvMatrix.C": "/opt/openfoam13/src/finiteVolume/fvMatrices/fvMatrix/fvMatrix.C",
    "codedFvModel.H": "/opt/openfoam13/src/fvModels/general/codedFvModel/codedFvModel.H",
}


def read_image_sources():
    quoted = [f"printf '\\n__CANS_FILE_{name}__\\n'; cat {path}" for name, path in FILES.items()]
    result = subprocess.run(
        ["docker", "run", "--rm", "--network", "none", "--entrypoint", "/bin/bash",
         IMAGE, "-c", "; ".join(quoted)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode:
        raise RuntimeError(f"cannot read pinned OpenFOAM image sources: {result.stderr[-1000:]}")
    source = {}
    body = result.stdout
    for index, name in enumerate(FILES):
        marker = f"__CANS_FILE_{name}__\n"
        if marker not in body:
            raise RuntimeError(f"missing source delimiter: {name}")
        remainder = body.split(marker, 1)[1]
        if index + 1 < len(FILES):
            next_marker = f"\n__CANS_FILE_{list(FILES)[index + 1]}__\n"
            content = remainder.split(next_marker, 1)[0]
        else:
            content = remainder
        source[name] = content
        body = remainder
    return source


def check(source, generated_model):
    momentum = source["momentumPredictor.C"]
    matrix = source["fvMatrix.C"]
    coded = source["codedFvModel.H"]
    checks = {
        "momentum_equation_places_fvModels_source_on_rhs":
            re.search(r"momentumTransport->divDevSigma\(U\)\s*==\s*fvModels\(\)\.source\(U\)", momentum) is not None,
        "matrix_equality_is_left_minus_right":
            "return (A - B);" in matrix,
        "matrix_subtraction_subtracts_internal_source":
            "source_ -= fvmv.source_;" in matrix,
        "coded_example_exposes_eqn_source_as_model_matrix_source":
            "scalarField& heSource = eqn.source();" in coded,
        "generated_model_subtracts_volume_weighted_forcing_into_model_matrix":
            "source[celli] -= volumes[celli]*forcing;" in generated_model,
    }
    if not all(checks.values()):
        raise AssertionError(f"OpenFOAM source sign audit failed: {checks}")
    return {
        "schema_version": 1,
        "scope": "source-level forcing-sign assembly audit in the exact runtime image",
        "image_id": IMAGE,
        "files": {
            name: {"path": FILES[name],
                   "sha256": hashlib.sha256(source[name].encode()).hexdigest()}
            for name in FILES
        },
        "generated_model_sha256": hashlib.sha256(generated_model.encode()).hexdigest(),
        "checks": checks,
        "derivation": [
            "The incompressibleFluid momentum equation constructs A == fvModels().source(U).",
            "fvMatrix operator== returns A - B, and matrix subtraction subtracts B.source from A.source.",
            "The generated codedFvModel adds -V*f to B.source; subtracting B therefore contributes +V*f to the assembled equation RHS.",
        ],
        "conclusion": "The coded source uses the positive manufactured forcing in the assembled momentum equation.",
        "limitations": [
            "This reads the source files shipped in the pinned image; it does not prove source-to-binary equivalence.",
            "It is not a solver run or a numerical accuracy certification.",
        ],
    }


def main():
    generated_model = Path("work/of13-high-gradient-v2/n64-dt0.001/constant/fvModels").read_text()
    result = check(read_image_sources(), generated_model)
    destination = Path("evidence/tests/high-gradient-openfoam-sign-audit.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
