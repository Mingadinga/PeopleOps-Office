import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from scripts.mission1_dataset.common import load_rules,write_data,read_data,file_hashes
from scripts.mission1_dataset.generate import generate
from scripts.mission1_dataset.validate import validate

class ResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rules=load_rules('data/generation/v0.6/generation_rules.json');cls.base=generate(cls.rules)
    def reject(self,fn,code):
        d=copy.deepcopy(self.base);fn(d);v=validate(d,self.rules);self.assertIn(code,{x['code'] for x in v['errors']},v['errors'][:4])
    def test_valid_independent(self):
        with patch('scripts.mission1_dataset.resolution.resolve_queue',side_effect=AssertionError),patch('scripts.mission1_dataset.application.decision',side_effect=AssertionError):self.assertEqual(validate(self.base,self.rules)['errors'],[])
    def test_v05_initial_immutable(self):
        old=read_data('data/generated/v0.5')
        for table in ('applications','application_eligibility','application_experiences'):self.assertEqual(self.base[table],old[table],table)
        current=[e for e in self.base['assessment_evidence'] if e['source_type']=='APPLICATION_RESPONSE'];prior=[e for e in old['assessment_evidence'] if e['source_type']=='APPLICATION_RESPONSE'];self.assertEqual(current,prior)
    def test_only_resolution_rule_changed(self):
        old=load_rules('data/generation/v0.5/generation_rules.json')
        for k,v in old.items():
            if k not in ('dataset_version','generation_version','generation_rules_version','schema_version','implementation_parameters'):self.assertEqual(self.rules[k],v,k)
        old_params=old['implementation_parameters'];new=copy.deepcopy(self.rules['implementation_parameters']);new.pop('eligibility_resolution');self.assertEqual(new,old_params)
    def test_targets_independent(self):
        r=copy.deepcopy(self.rules)
        for t in r['funnel_targets']:t[2]+=900
        r['workforce_plan']['target_join']=999
        d=generate(r)
        for k in self.base:
            if k not in ('workforce_plan','funnel_plan'):self.assertEqual(d[k],self.base[k],k)
    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            write_data(a,self.base);write_data(b,generate(self.rules));self.assertEqual(file_hashes(a),file_hashes(b));self.assertEqual(validate(read_data(a),self.rules)['errors'],[])
    def test_v05_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            write_data(t,generate(load_rules('data/generation/v0.5/generation_rules.json')));self.assertEqual(file_hashes(t),file_hashes('data/generated/v0.5'))
    def test_unknown_cannot_advance_unconditionally(self):self.reject(lambda d:next(s for s in d['stage_history'] if s['result']=='CONDITIONAL_ADVANCE').update(result='ADVANCED',decision_reason_code='APPLICATION_EVIDENCE_CANDIDATE'),'document_rule')
    def test_missing_verification(self):self.reject(lambda d:d['eligibility_verifications'].clear(),'eligibility_gate')
    def test_fake_pass_fact(self):self.reject(lambda d:next(e for e in d['eligibility_verifications'] if e['verification_result']=='VERIFIED_PASS').update(verification_evidence='{}'),'eligibility_resolution')
    def test_fail_requirement(self):self.reject(lambda d:next(e for e in d['eligibility_verifications'] if e['verification_result']=='VERIFIED_FAIL').update(requirement='other'),'eligibility_resolution')
    def test_not_verified_is_unknown(self):self.reject(lambda d:next(e for e in d['eligibility_verifications'] if e['verification_result']=='ELIGIBILITY_NOT_VERIFIED').update(resulting_status='FAIL'),'eligibility_resolution')
    def test_response_deadline(self):self.reject(lambda d:d['eligibility_verifications'][0].update(verification_deadline=d['eligibility_verifications'][0]['verification_requested_at']),'eligibility_resolution')
    def test_request_after_notification(self):self.reject(lambda d:d['eligibility_verifications'][0].update(verification_requested_at='2026-10-01T00:00:00+09:00'),'eligibility_resolution')
    def test_late_pass_cannot_enter_pre(self):
        def change(d):
            e=next(e for e in d['eligibility_verifications'] if e['verification_result']=='VERIFIED_PASS');e['verified_at']='2027-10-31T23:00:00+09:00';e['resolved_at']=e['verified_at']
        self.reject(change,'eligibility_gate')
    def test_confirmation_human(self):self.reject(lambda d:next(e for e in d['eligibility_verifications'] if e['verification_result']=='VERIFIED_PASS').update(confirmed_by='AI_PREDICTION'),'eligibility_resolution')
    def test_censoring(self):
        r=copy.deepcopy(self.rules);r['observation_end']='2026-10-24T23:59:59+09:00';d=generate(r)
        self.assertTrue(any(e['verification_result']=='PENDING' for e in d['eligibility_verifications']));self.assertEqual(validate(d,r)['errors'],[])
