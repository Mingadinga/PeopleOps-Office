"""Document v0.5: independent mutation tests and preservation of downstream policy."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from scripts.mission1_dataset.common import load_rules,read_data,write_data,file_hashes
from scripts.mission1_dataset.generate import generate
from scripts.mission1_dataset.validate import validate
from scripts.mission1_dataset.application import eligibility_states,decision

class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=load_rules('data/generation/v0.5/generation_rules.json');cls.data=generate(cls.rules)
    def rejected(self,change,code):
        d=copy.deepcopy(self.data);change(d);v=validate(d,self.rules)
        self.assertIn(code,{e['code'] for e in v['errors']},v['errors'][:5])
    def test_valid(self):self.assertEqual(validate(self.data,self.rules)['errors'],[])
    def test_no_oracle(self):
        with patch('scripts.mission1_dataset.application.decision',side_effect=AssertionError),patch('scripts.mission1_dataset.application.eligibility_states',side_effect=AssertionError):
            self.assertEqual(validate(self.data,self.rules)['errors'],[])
    def test_target_independence(self):
        r=copy.deepcopy(self.rules)
        for row in r['funnel_targets']:row[2]+=777
        r['workforce_plan']['target_join']=888
        changed=generate(r)
        for key in self.data:
            if key not in ('workforce_plan','funnel_plan'):self.assertEqual(changed[key],self.data[key],key)
    def test_unchanged_downstream_rules(self):
        prior=load_rules()
        for key in ['seed','random_stream_version','applications','process','evidence','capacity','hold','targeted_followup','offers','onboarding','interview_model','final_candidate_contract']:
            self.assertEqual(self.rules[key],prior[key],key)
    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            write_data(a,self.data);write_data(b,generate(self.rules));self.assertEqual(file_hashes(a),file_hashes(b));self.assertEqual(validate(read_data(a),self.rules)['errors'],[])
    def test_unknown_not_failure(self):
        unknown={r['application_id'] for r in self.data['application_eligibility'] if r['overall_state']=='UNKNOWN'}
        rows=[s for s in self.data['stage_history'] if s['stage']=='DOCUMENT_SCREEN' and s['application_id'] in unknown]
        self.assertTrue(rows);self.assertTrue(all(s['result']!='FAILED' for s in rows));self.assertTrue(any(s['result']=='ADVANCED' for s in rows))
    def test_fake_eligibility(self):self.rejected(lambda d:d['application_eligibility'][0].update(overall_state='FAIL' if d['application_eligibility'][0]['overall_state']!='FAIL' else 'PASS'),'eligibility')
    def test_wrong_na(self):self.rejected(lambda d:next(r for r in d['application_eligibility'] if r['military_requirement_applicable']=='NO').update(military_requirement_status='COMPLETED'),'eligibility')
    def test_bad_reference_date(self):self.rejected(lambda d:d['application_eligibility'][0].update(eligibility_reference_date='2026-04-13'),'eligibility')
    def test_false_advance(self):self.rejected(lambda d:next(s for s in d['stage_history'] if s['result']=='CLOSED').update(result='ADVANCED',decision_reason_code='APPLICATION_EVIDENCE_CANDIDATE'),'document_rule')
    def test_wrong_failure_ref(self):
        def change(d):
            s=next(s for s in d['stage_history'] if s['stage']=='DOCUMENT_SCREEN' and s['result']=='FAILED');t=json.loads(s['rationale']);t['explicit_violation_ref']=['EL_FOREIGN#degree'];s['rationale']=json.dumps(t)
        self.rejected(change,'document_rule')
    def test_wrong_card(self):self.rejected(lambda d:next(e for e in d['assessment_evidence'] if e['source_type']=='APPLICATION_RESPONSE').update(context_id='XP_FOREIGN'),'experience')
    def test_invalid_category(self):self.rejected(lambda d:d['application_experiences'][0].update(evidence_categories='["QUALITY"]'),'experience')
    def test_unclear_never_suffices(self):
        d=copy.deepcopy(self.data);app=d['applications'][0];app=next(a for a in d['applications'] if a['submitted_at']);aid=app['application_id'];r=next(r for r in d['application_eligibility'] if r['application_id']==aid);r.update(requirement_states='{"degree":"UNKNOWN"}',overall_state='UNKNOWN')
        xs=[x for x in d['application_experiences'] if x['application_id']==aid]
        for x in xs:x.update(ownership='TEAM_UNCLEAR',actions='{"PROBLEM":"목표 정의","BUILD":"함수 작성"}')
        self.assertEqual(decision(d,app)[0],'CLOSED')
        # Two unrelated single-category experiences cannot be pooled.
        for i,x in enumerate(xs):x.update(ownership='SELF',actions=json.dumps({['PROBLEM','BUILD'][i%2]:'구체적 행동'}))
        self.assertEqual(decision(d,app)[0],'CLOSED')
    def test_date_edges(self):
        r=copy.deepcopy(self.data['application_eligibility'][0]);r.update(degree_level='BACHELOR',graduation_status='EXPECTED',expected_graduation_date='2027-03-01',expected_join_date='2027-03-01',language_test_type='OPIC',language_test_valid_until=r['eligibility_reference_date'])
        st,_=eligibility_states(r);self.assertEqual(st['degree'],'PASS');self.assertEqual(st['language'],'PASS')
        r['expected_graduation_date']='2027-03-02';self.assertEqual(eligibility_states(r)[0]['degree'],'FAIL')
    def test_no_document_skill_decision(self):
        for s in self.data['stage_history']:
            if s['stage']=='DOCUMENT_SCREEN':self.assertFalse(any(dc['application_id']==s['application_id'] and dc['decided_at']<=s['decision_at'] for dc in self.data['evidence_decisions']))
    def test_v04_canonical_identity(self):
        with tempfile.TemporaryDirectory() as path:
            write_data(path,generate(load_rules()));self.assertEqual(file_hashes(path),file_hashes('data/generated/v0.4'))
