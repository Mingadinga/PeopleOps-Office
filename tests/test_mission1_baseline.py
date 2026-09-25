"""Freeze metadata and immutable snapshot regressions; mutations stay outside repository."""
import json
import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.verify_mission1_baseline import ROOT, verify


class BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='peopleops-baseline-')
        cls.root = Path(cls.temp.name)
        for rel in ('data/generation', 'data/synthetic', 'data/generated/v0.4',
                    'data/generated/v0.6', 'scripts/mission1_dataset'):
            shutil.copytree(ROOT / rel, cls.root / rel)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def reject(self, relative, mutation, expected):
        path = self.root / relative
        before = path.read_bytes()
        try:
            value = json.loads(before)
            mutation(value)
            path.write_text(json.dumps(value))
            result = verify(root=self.root)
            self.assertEqual(result['status'], 'ERROR')
            self.assertTrue(any(expected in e for e in result['errors']), result['errors'])
        finally:
            path.write_bytes(before)

    def test_all_candidate_versions_match_historical_manifests(self):
        # Physical files include v0.1's retired evidence_decision_sources table.
        for n in range(1, 7):
            version = f'v0.{n}'
            meta = ROOT / 'data/generation' / (version if n > 1 else '')
            manifest = json.loads((meta / 'dataset_manifest.json').read_text())
            actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ROOT / 'data/generated' / version).iterdir() if p.is_file()}
            self.assertEqual(actual, manifest['file_sha256'], version)

    def test_active_v2(self):
        result = verify(root=self.root)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['canonical_file_count'], 28)

    def test_historical_v1(self):
        self.assertEqual(verify('v1', self.root)['errors'], [])

    def test_duplicate_active_rejected(self):
        self.reject('data/generation/baseline_registry.json',
                    lambda r: r['baselines'][0].update(status='ACTIVE'), 'Wrong active')

    def test_source_manifest_tamper_rejected(self):
        self.reject('data/generation/v0.6/dataset_manifest.json',
                    lambda m: m.update(seed=1), 'Source manifest hash')

    def test_unapproved_rejected(self):
        self.reject('data/generation/v2/dataset_manifest.json',
                    lambda m: m.update(human_review_status='UNREVIEWED'), 'Missing approval')

    def test_snapshot_outcome_tamper_rejected(self):
        self.reject('data/generation/v2/human_review_snapshot.json',
                    lambda s: s['metrics']['workforce'].update(ready_by_target_date=4),
                    'Approved snapshot differs')

    def test_canonical_byte_change_rejected(self):
        path = self.root / 'data/synthetic/v2/applications.csv'
        before = path.read_bytes()
        try:
            path.write_bytes(before + b'\n')
            self.assertIn('Canonical hashes differ', verify(root=self.root)['errors'])
        finally:
            path.write_bytes(before)

    def test_synthetic_assumption_missing_rejected(self):
        self.reject('data/generation/v2/synthetic_assumptions.json',
                    lambda a: a['assumptions'].pop(), 'Missing synthetic assumption')


if __name__ == '__main__':
    unittest.main()
