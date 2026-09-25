"""Presentation reference integrity; no generator or dataset writes."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_mission1_presentation import ROOT, MAPPING, validate


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = json.loads((ROOT / MAPPING).read_text())

    def reject(self, mutate, expected):
        mapping = copy.deepcopy(self.mapping)
        mutate(mapping)
        result = validate(mapping)
        self.assertEqual(result['status'], 'ERROR')
        self.assertTrue(any(expected in e for e in result['errors']), result)

    def test_valid_mapping_does_not_modify_baseline(self):
        files = list((ROOT / 'data/synthetic/v1').iterdir())
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        self.assertEqual(validate(self.mapping)['status'], 'PASS')
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

    def test_no_automatic_v2_rebinding(self):
        self.reject(lambda m: m.update(dataset_version='v2'), 'version binding')

    def test_manifest_binding(self):
        self.reject(lambda m: m.update(baseline_manifest_sha256='wrong'), 'manifest hash')

    def test_identity_pair(self):
        self.reject(lambda m: m['cases'][0].update(candidate_id='C0005'), 'identity')

    def test_missing_evidence(self):
        self.reject(lambda m: m['cases'][0]['steps'][0]['refs']['assessment_evidence'].append('MISSING'), 'missing reference')

    def test_foreign_candidate_evidence(self):
        self.reject(lambda m: m['cases'][0]['steps'][0]['refs']['assessment_evidence'].append(m['cases'][1]['evidence_cards'][0]['evidence_id']), 'foreign candidate')

    def test_missing_observation(self):
        self.reject(lambda m: m['cases'][0]['steps'][0]['refs']['assessment_observations'].append('MISSING'), 'missing reference')

    def test_missing_skill_decision(self):
        self.reject(lambda m: m['cases'][0]['steps'][-1]['refs']['evidence_decisions'].append('MISSING'), 'missing reference')

    def test_missing_final_decision(self):
        self.reject(lambda m: m['cases'][1]['refs']['final_decisions'].append('MISSING'), 'missing reference')

    def test_observation_lineage_not_omitted(self):
        self.reject(lambda m: m['cases'][0]['steps'][0]['refs'].update(assessment_observations=[]), 'card observation lineage')

    def test_self_report_skill_boundary(self):
        self.reject(lambda m: m['cases'][0]['evidence_cards'][0].update(purpose='PRIMARY_SKILL'), 'card skill boundary')

    def test_no_invented_final_for_pending(self):
        self.reject(lambda m: m['cases'][0]['refs'].update(final_decisions=['FD_APP0005_INITIAL']), 'A must not invent')

    def test_missing_targeted_followup(self):
        def mutate(m):
            case = m['cases'][1]
            case['refs']['targeted_followups'] = []
            for step in case['steps']:
                step['refs'].pop('targeted_followups', None)
        self.reject(mutate, 'targeted follow-up reference')

    def test_foreign_resolution_plan(self):
        def mutate(m):
            step = next(s for s in m['cases'][1]['steps'] if 'resolution_plan_ref' in s)
            step['resolution_plan_ref']['final_decision_id'] = 'FD_APP0228_INITIAL'
        self.reject(mutate, 'foreign resolution plan')

    def test_existing_scene_roles_and_space(self):
        self.reject(lambda m: m['cases'][0]['steps'][0].update(space_label='Invented room'), 'space/role')

    def test_no_live_ai_evaluation(self):
        self.reject(lambda m: m['presentation_contract'].update(live_ai_evaluation=True), 'stored trace')

    def test_canonical_hash_tamper_rejected_in_temp_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for directory in ['data/synthetic/v1', 'data/generation/v1']:
                shutil.copytree(ROOT / directory, root / directory)
            for name in ['data/generation/baseline_registry.json', 'docs/06_mission1_experience_specification.md']:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, root / name)
            p = root / 'data/synthetic/v1/applications.csv'
            p.write_bytes(p.read_bytes() + b'\n')
            result = validate(self.mapping, root)
            self.assertEqual(result['status'], 'ERROR')
            self.assertIn('canonical hash: applications.csv', result['errors'])


if __name__ == '__main__':
    unittest.main()
