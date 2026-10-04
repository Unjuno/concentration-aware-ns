import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from tools.analyze_interface_operator_probe import analyze_case, maximum, reconstruct, snapshot_metrics
from tools.build_interface_operator_cases import generate


def cartesian_snapshots(metadata, mode):
    """Assemble an independent complete 3D conductance graph, including wraps.

    This synthetic fixture is not packaged CFD output.  The solved values come
    from a dense graph solve, independent of the analytic resistance chain.
    """
    nx = metadata['inputs']['nx']; h = 2 / nx; count = 4 * nx
    centres = np.asarray(metadata['mesh']['cell_centres'])
    material = np.where(centres[:, 0] < 0, 1., 100.)
    area = np.array([.25, h / 2, h / 2])
    width = np.array([h, .5, .5])
    faces, patches = [], []
    raw = np.zeros(count); matrix = np.zeros((count, count)); rhs = np.zeros(count)
    label = lambda i, j, k: int(np.ravel_multi_index((k, j, i), (2, 2, nx)))

    def append_face(owner, neighbour, axis, sign=1, boundary=None):
        sf = np.zeros(3); sf[axis] = sign * area[axis]
        cf = centres[owner].copy()
        coefficient = material[owner]
        if mode == 'constant':
            coefficient = 1.
        elif boundary is None:
            left, right = material[owner], material[neighbour]
            coefficient = (left + right) / 2 if mode == 'arithmetic' else 2 / (1 / left + 1 / right)
        if boundary is None:
            cf = (centres[owner] + centres[neighbour]) / 2
            delta = 1 / width[axis]
        else:
            cf[axis] = sign if axis == 0 else (0 if sign < 0 else 1)
            delta = 2 / h if axis == 0 else 2.
        conductance = coefficient * area[axis] * delta
        faces.append({'owner':owner, 'neighbour':neighbour, 'axis':axis,
                      'areas':sf, 'centres':cf, 'gamma':coefficient, 'delta':delta,
                      'g':conductance, 'boundary':boundary})
        return conductance

    for axis in range(3):
        for k in range(2):
            for j in range(2):
                for i in range(nx):
                    coordinates = [i, j, k]
                    if coordinates[axis] == (nx if axis == 0 else 2) - 1:
                        continue
                    neighbour = coordinates.copy(); neighbour[axis] += 1
                    p, q = label(*coordinates), label(*neighbour)
                    g = append_face(p, q, axis)
                    raw[p] += g; raw[q] += g
                    matrix[p, p] += g; matrix[q, q] += g
                    matrix[p, q] -= g; matrix[q, p] -= g
    internal_count = len(faces)
    for name in ('xm', 'xp', 'ym', 'yp', 'zm', 'zp'):
        axis = 'xyz'.index(name[0]); sign = -1 if name.endswith('m') else 1
        side = 0 if sign < 0 else (nx if axis == 0 else 2) - 1
        owners, internal_coeffs, boundary_coeffs, opposite = [], [], [], []
        start = len(faces)
        for k in range(2):
            for j in range(2):
                for i in range(nx):
                    coordinates = [i, j, k]
                    if coordinates[axis] != side:
                        continue
                    p = label(*coordinates); wrapped = coordinates.copy()
                    wrapped[axis] = (nx if axis == 0 else 2) - 1 - side
                    q = label(*wrapped) if axis else -1
                    wall = 1. if mode == 'constant' else sign / (1 if sign < 0 else 100)
                    g = append_face(p, q, axis, sign, wall if axis == 0 else 'cyclic')
                    matrix[p, p] += g
                    if axis:
                        matrix[p, q] -= g; bc = g
                    else:
                        rhs[p] += g * wall; bc = g * wall
                    owners.append(p); internal_coeffs.append(g); boundary_coeffs.append(bc); opposite.append(q)
        patches.append({'name':name, 'type':'wall' if axis == 0 else 'cyclic',
                        'fieldType':'fixedValue' if axis == 0 else 'cyclic',
                        'coupled':axis != 0, 'start':start, 'size':len(owners),
                        'faceCells':owners, 'internalCoeffs':internal_coeffs,
                        'boundaryCoeffs':boundary_coeffs, 'opposite':opposite})

    def snapshot(values, stage):
        flux, sn, face_values = [], [], []
        for face in faces:
            p, q = face['owner'], face['neighbour']
            neighbour_value = values[q] if q >= 0 else face['boundary']
            difference = neighbour_value - values[p]
            sn.append(difference * face['delta']); flux.append(difference * face['g'])
            face_values.append((values[p] + neighbour_value) / 2 if q >= 0 else neighbour_value)
        flux = np.asarray(flux); balance = np.zeros(count); cyclic = np.zeros(count)
        derivative = np.zeros(count)
        for index, face in enumerate(faces):
            p, q = face['owner'], face['neighbour']
            balance[p] += flux[index]
            derivative[p] += face['areas'][0] * face_values[index]
            if index < internal_count:
                balance[q] -= flux[index]; derivative[q] -= face['areas'][0] * face_values[index]
            elif q >= 0:
                cyclic[p] += face['g'] * values[q]
        derivative /= h / 4
        output_patches = []
        for patch in patches:
            row = {key:value for key,value in patch.items() if key != 'opposite'}
            row['neighbourValues'] = [float(values[q]) for q in patch['opposite']] if patch['coupled'] else []
            output_patches.append(row)
        correction = None
        if mode != 'constant':
            gradient = np.zeros((count, 9)); gradient[:, 1] = derivative
            transposed = np.zeros((count, 9)); transposed[:, 3] = derivative
            explicit = np.zeros((len(faces), 3))
            for index, face in enumerate(faces):
                p, q = face['owner'], face['neighbour']
                grad_face = (derivative[p] + derivative[q]) / 2 if q >= 0 else derivative[p]
                explicit[index, 0] = -material[p] * face['areas'][1] * grad_face
            integrated = np.zeros((count, 3))
            for index, face in enumerate(faces):
                integrated[face['owner']] += explicit[index]
                if index < internal_count:
                    integrated[face['neighbour']] -= explicit[index]
            correction = {'coefficientMode':'arithmetic', 'gradU':gradient.tolist(),
                          'dev2TransposeGradU':transposed.tolist(),
                          'separateFlux':explicit.tolist(), 'parentProductFlux':explicit.tolist(),
                          'divSeparateTimesVolume':integrated.tolist(),
                          'divParentProductTimesVolume':integrated.tolist()}
        return {'schemaVersion':1, 'mode':mode, 'stage':stage,
                'fieldName':f'shear_{mode}' if mode != 'constant' else 'constantControl_probe',
                'operator':'negative_fvm_laplacian',
                'fieldDimensions':[0,1,-1,0,0,0,0], 'equationDimensions':[0,4,-2,0,0,0,0],
                'cells':{'centres':centres.tolist(), 'volumes':[h/4]*count,
                         'values':values.tolist(), 'rawDiag':raw.tolist(),
                         'completeDiag':np.diag(matrix).tolist(), 'source':[0.]*count,
                         'nativeResidual':(rhs-matrix@values+cyclic).tolist(),
                         'divPhysicalFluxTimesVolume':balance.tolist()},
                'internalMatrix':{'owner':[f['owner'] for f in faces[:internal_count]],
                                  'neighbour':[f['neighbour'] for f in faces[:internal_count]],
                                  'upper':[-f['g'] for f in faces[:internal_count]],
                                  'lower':[-f['g'] for f in faces[:internal_count]],
                                  'symmetric':True, 'hasLower':False},
                'faces':{'owner':[f['owner'] for f in faces],
                         'neighbour':[f['neighbour'] if index < internal_count else -1
                                      for index,f in enumerate(faces)],
                         'centres':[f['centres'].tolist() for f in faces],
                         'areas':[f['areas'].tolist() for f in faces],
                         'gamma':[f['gamma'] for f in faces], 'deltaCoeffs':[f['delta'] for f in faces],
                         'snGrad':sn, 'physicalFlux':flux.tolist(), 'matrixFlux':(-flux).tolist()},
                'patches':output_patches,
                'solverPerformance':{'initialResidual':1., 'finalResidual':0., 'iterations':1} if stage == 'after' else None,
                'explicitCorrection':correction}

    initial = np.ones(count) if mode == 'constant' else centres[:, 0] / material
    before = snapshot(initial, 'before')
    after = None if mode == 'constant' else snapshot(np.linalg.solve(matrix, rhs), 'after')
    return before, after, matrix, rhs


def write_cartesian_case(case):
    metadata = generate(case, nx=16)
    snapshots = {}
    for mode in ('arithmetic', 'harmonic', 'constant'):
        before, after, matrix, rhs = cartesian_snapshots(metadata, mode)
        directory = case/'probe'/mode; directory.mkdir(parents=True)
        for stage, snapshot in (('before',before),('after',after)):
            if snapshot is not None:
                (directory/f'{stage}.json').write_text(json.dumps(snapshot))
                snapshots[(mode,stage)] = snapshot
    return snapshots


def small_cyclic_matrix():
    """Two DOFs joined by both internal and periodic faces and fixed walls.

    A=[[5,-4],[-4,5]], b=(1,1), u=(1,1), so complete residual is zero.
    The hypothesized native addition is 2 per row. This is not CFD output.
    """
    return {
        "cells": {"values": [1, 1], "centres": [[0, .25, .5], [0, .75, .5]],
                  "rawDiag": [2, 2], "completeDiag": [5, 5], "source": [0, 0],
                  "nativeResidual": [2, 2], "divPhysicalFluxTimesVolume": [0, 0]},
        "internalMatrix": {"owner": [0], "neighbour": [1], "upper": [-2], "lower": [-2]},
        "faces": {"owner": [0, 0, 1, 0, 1], "neighbour": [1, -1, -1, -1, -1],
                  "areas": [[0, 1, 0], [0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0]],
                  "physicalFlux": [0]*5, "matrixFlux": [0]*5},
        "patches": [
            {"name": "ym", "start": 1, "size": 1, "coupled": True, "faceCells": [0],
             "internalCoeffs": [2], "boundaryCoeffs": [2], "neighbourValues": [1]},
            {"name": "yp", "start": 2, "size": 1, "coupled": True, "faceCells": [1],
             "internalCoeffs": [2], "boundaryCoeffs": [2], "neighbourValues": [1]},
            {"name": "xm", "start": 3, "size": 1, "coupled": False, "faceCells": [0],
             "internalCoeffs": [1], "boundaryCoeffs": [1], "neighbourValues": []},
            {"name": "xp", "start": 4, "size": 1, "coupled": False, "faceCells": [1],
             "internalCoeffs": [1], "boundaryCoeffs": [1], "neighbourValues": []},
        ],
    }


class IndependentBoundaryMatrix(unittest.TestCase):
    def test_periodic_and_internal_edges_to_same_neighbour_accumulate_once(self):
        matrix, rhs, balance, cyclic = reconstruct(small_cyclic_matrix())
        np.testing.assert_array_equal(matrix, [[5, -4], [-4, 5]])
        np.testing.assert_array_equal(rhs, [1, 1])
        np.testing.assert_array_equal(balance, [0, 0])
        np.testing.assert_array_equal(cyclic, [2, 2])

    def test_native_extra_term_is_separate_from_zero_complete_balance(self):
        metrics = snapshot_metrics(small_cyclic_matrix())
        self.assertEqual(metrics['complete_integrated_residual_Linf'], 0)
        self.assertEqual(metrics['native_integrated_residual_Linf'], 2)
        self.assertEqual(metrics['native_minus_complete_minus_cyclic_load_Linf'], 0)

    def test_corrected_native_api_would_disagree_with_extra_term_prediction(self):
        row = small_cyclic_matrix(); row['cells']['nativeResidual'] = [0, 0]
        metrics = snapshot_metrics(row)
        self.assertEqual(metrics['native_integrated_residual_Linf'], 0)
        self.assertEqual(metrics['native_minus_complete_minus_cyclic_load_Linf'], 2)

    def test_corrupt_patch_and_missing_boundary_diagonal_are_rejected(self):
        for field, replacement in [('faceCells', [1]), ('internalCoeffs', [0])]:
            row = copy.deepcopy(small_cyclic_matrix()); row['patches'][0][field] = replacement
            with self.assertRaises(ValueError):
                reconstruct(row)

    def test_wrong_periodic_neighbour_values_are_rejected(self):
        row = small_cyclic_matrix(); row['patches'][0]['neighbourValues'] = [2]
        with self.assertRaisesRegex(ValueError, 'neighbour values'):
            reconstruct(row)

    def test_nonfinite_matrix_evidence_is_rejected(self):
        row = small_cyclic_matrix(); row['internalMatrix']['upper'] = [float('nan')]
        with self.assertRaisesRegex(ValueError, 'finite array'):
            reconstruct(row)


class FullCartesianOperatorEvidence(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.case = Path(self.directory.name)/'nx16'
        self.snapshots = write_cartesian_case(self.case)
        self.protocol = json.loads(Path('protocols/of13-interface-operator-v1.json').read_text())

    def rewrite(self, mode, stage, snapshot):
        (self.case/'probe'/mode/f'{stage}.json').write_text(json.dumps(snapshot))

    def test_independent_graph_recovers_both_chains_and_nonzero_initial_residual(self):
        result = analyze_case(self.case, self.protocol)
        self.assertEqual(result['operator_quality'], 'PASS')
        self.assertGreater(result['modes']['arithmetic']['before']['complete_integrated_residual_Linf'], 1)
        self.assertLess(result['modes']['harmonic']['cell_error_to_chain_Linf'], 1e-12)
        self.assertEqual(result['constant_control']['source_predicted_extra_cyclic_term'], 'OBSERVED')
        metadata = json.loads((self.case/'case_metadata.json').read_text())
        for mode in ('arithmetic', 'harmonic', 'constant'):
            before, _, expected_matrix, expected_rhs = cartesian_snapshots(metadata, mode)
            matrix, rhs, balance, _ = reconstruct(before)
            np.testing.assert_allclose(matrix, expected_matrix, rtol=0, atol=1e-12)
            np.testing.assert_allclose(rhs, expected_rhs, rtol=0, atol=1e-12)
            np.testing.assert_allclose(rhs-matrix@before['cells']['values'], balance,
                                       rtol=0, atol=1e-12)

    def test_hostile_dimensions_schema_arrays_and_patch_types_are_rejected(self):
        def mutate(path, value):
            def apply(snapshot):
                current = snapshot
                for key in path[:-1]:
                    current = current[key]
                current[path[-1]] = value
            return apply

        attacks = [
            ('arithmetic','before',mutate(['schemaVersion'],2)),
            ('arithmetic','after',mutate(['operator'],'positive_laplacian')),
            ('harmonic','before',mutate(['fieldName'],'shear_arithmetic')),
            ('constant','before',mutate(['fieldDimensions'],[0,0,0,0,0,0,0])),
            ('arithmetic','after',mutate(['equationDimensions'],[0,5,-2,0,0,0,0])),
            ('harmonic','before',mutate(['cells','volumes',0],1.)),
            ('arithmetic','before',mutate(['explicitCorrection','gradU'],[[0]*9])),
            ('harmonic','after',mutate(['explicitCorrection','dev2TransposeGradU',0,0],float('nan'))),
            ('arithmetic','before',mutate(['explicitCorrection','separateFlux',0,0],float('nan'))),
            ('harmonic','after',mutate(['explicitCorrection','divParentProductTimesVolume'],[[0,0]])),
            ('arithmetic','after',mutate(['solverPerformance','finalResidual'],float('inf'))),
            ('harmonic','before',mutate(['internalMatrix','owner',0],.5)),
            ('constant','before',mutate(['patches',0,'fieldType'],'zeroGradient')),
            ('arithmetic','before',mutate(['faces','areas',0,0],-.25)),
        ]
        for mode, stage, attack in attacks:
            with self.subTest(mode=mode, stage=stage, attack=attack):
                baseline = self.snapshots[(mode,stage)]
                hostile = copy.deepcopy(baseline); attack(hostile)
                self.rewrite(mode,stage,hostile)
                with self.assertRaises(ValueError):
                    analyze_case(self.case,self.protocol)
                self.rewrite(mode,stage,baseline)

    def test_before_matrix_balance_and_flux_sign_are_quality_gates(self):
        baseline = self.snapshots[('arithmetic','before')]
        for attack in ('matrix','flux-sign','normal-gradient'):
            with self.subTest(attack=attack):
                hostile = copy.deepcopy(baseline)
                if attack == 'matrix':
                    hostile['cells']['rawDiag'][0] += 1
                    hostile['cells']['completeDiag'][0] += 1
                elif attack == 'flux-sign':
                    hostile['faces']['matrixFlux'] = hostile['faces']['physicalFlux']
                else:
                    hostile['faces']['snGrad'][0] += .1
                self.rewrite('arithmetic','before',hostile)
                result = analyze_case(self.case,self.protocol)
                self.assertEqual(result['operator_quality'],'FAIL_SPECIFIED_OPERATOR_GATE')
                self.rewrite('arithmetic','before',baseline)

    def test_native_api_prediction_is_separate_from_physical_quality(self):
        constant = copy.deepcopy(self.snapshots[('constant','before')])
        constant['cells']['nativeResidual'] = [0.]*len(constant['cells']['values'])
        self.rewrite('constant','before',constant)
        result = analyze_case(self.case,self.protocol)
        self.assertEqual(result['operator_quality'],'PASS')
        self.assertEqual(result['constant_control']['source_predicted_extra_cyclic_term'],'NOT_OBSERVED')

    def test_nonfinite_maximum_cannot_silently_become_a_zero_gate(self):
        for value in (float('nan'), float('inf'), -float('inf')):
            with self.assertRaisesRegex(ValueError,'nonfinite'):
                maximum([value])


if __name__ == '__main__':
    unittest.main()
