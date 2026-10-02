import unittest

from tools.check_high_gradient_openfoam_sign import check


class OpenFoamSourceSignTests(unittest.TestCase):
    def test_negative_model_matrix_source_becomes_positive_rhs_force(self):
        sources = {
            "momentumPredictor.C": "tUEqn = (momentumTransport->divDevSigma(U) == fvModels().source(U));",
            "fvMatrix.C": "return (A - B); source_ -= fvmv.source_;",
            "codedFvModel.H": "scalarField& heSource = eqn.source();",
        }
        result = check(sources, "source[celli] -= volumes[celli]*forcing;")

        self.assertTrue(all(result["checks"].values()))
        self.assertIn("+V*f", result["derivation"][-1])

    def test_sign_audit_rejects_a_changed_matrix_assembly_contract(self):
        sources = {
            "momentumPredictor.C": "momentumTransport->divDevSigma(U) == fvModels().source(U)",
            "fvMatrix.C": "return (A + B); source_ += fvmv.source_;",
            "codedFvModel.H": "scalarField& heSource = eqn.source();",
        }

        with self.assertRaises(AssertionError):
            check(sources, "source[celli] -= volumes[celli]*forcing;")


if __name__ == "__main__":
    unittest.main()
