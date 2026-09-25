"""Final Human Review contracts: independent mutation and policy regressions."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
from scripts.mission1_dataset.common import load_rules,write_data,read_data,file_hashes,parse
from scripts.mission1_dataset.generate import generate
from scripts.mission1_dataset.validate import validate
from scripts.mission1_dataset.evidence import final_review
from scripts.mission1_dataset.final_candidate import calibration_triggers
from scripts.mission1_dataset.schema import SCHEMA


class FinalCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rules=load_rules();cls.base=generate(cls.rules)

    def reject(self,mutate,code):
        d=copy.deepcopy(self.base);mutate(d);v=validate(d,self.rules)
        self.assertIn(code,{e['code'] for e in v['errors']},v['errors'][:6])

    def test_valid_and_deterministic_bytes(self):
        self.assertEqual(validate(self.base,self.rules)['errors'],[])
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            write_data(a,self.base);write_data(b,generate(copy.deepcopy(self.rules)))
            self.assertEqual(file_hashes(a),file_hashes(b));self.assertEqual(validate(read_data(a),self.rules)['errors'],[])

    def test_validator_without_oracles(self):
        with ExitStack() as stack:
            for module,names in [('evidence',['interpret','calibrate','final_review','stage_transition_decision']),('interview',['first_transition']),('final_candidate',['calibration_triggers','finish_final_review'])]:
                for name in names:stack.enter_context(patch('scripts.mission1_dataset.'+module+'.'+name,side_effect=AssertionError('oracle')))
            self.assertEqual(validate(self.base,self.rules)['errors'],[])

    def test_target_independence_and_unchanged_distributions(self):
        r=copy.deepcopy(self.rules)
        for t in r['funnel_targets']:t[2]+=101
        r['workforce_plan']['target_join']=1000;d=generate(r)
        for table in SCHEMA:self.assertEqual(self.base[table],d[table],table)
        prior=load_rules(Path(__file__).resolve().parents[1]/'data/generation/v0.3/generation_rules.json')
        for key in ('offers','onboarding','evidence','targeted_followup','capacity'):self.assertEqual(self.rules[key],prior[key],key)
        self.assertEqual(self.rules['seed'],20260924)

    def test_all_legacy_paths_protected(self):
        with tempfile.TemporaryDirectory() as d:
            for version in ('v0.1','v0.2','v0.3'):
                with self.assertRaises(ValueError):write_data(Path(d)/version,self.base)

    def test_limited_is_decisionable_not_automatic_pass(self):
        dc={d['decision_id']:d for d in self.base['evidence_decisions']};found=False
        for s in self.base['stage_history']:
            if s['stage']=='FIRST_INTERVIEW' and s['decision_at']:
                for item in json.loads(s['rationale'])['coverage'].values():
                    if dc[item['skill_decision_ref']]['final_level']=='LIMITED':
                        self.assertTrue(item['decisionable']);found=True
        self.assertTrue(found)
        self.assertTrue(any(s['result']=='FAILED' and all(x['decisionable'] for x in json.loads(s['rationale'])['coverage'].values()) for s in self.base['stage_history'] if s['stage']=='FIRST_INTERVIEW' and s['decision_at']))

    def test_false_coverage_flag(self):
        def change(d):
            s=next(s for s in d['stage_history'] if s['decision_reason_code']=='EVIDENCE_PENDING');t=json.loads(s['rationale'])
            for v in t['coverage'].values():v['decisionable']=True
            s['rationale']=json.dumps(t);s['result']='ADVANCED'
        self.reject(change,'decisionable_coverage')

    def test_self_reported_coverage_forbidden(self):
        def change(d):
            s=next(s for s in d['stage_history'] if s['stage']=='FIRST_INTERVIEW' and s['result']=='ADVANCED');ids={a['activity_id'] for a in d['assessment_activities'] if a['stage_event_id']==s['stage_event_id']}
            for e in d['assessment_evidence']:
                if e['activity_id'] in ids:e['verification_mode']='SELF_REPORTED'
        self.reject(change,'decisionable_coverage')

    def test_nondecisionable_skill_not_coverage(self):
        def change(d):
            s=next(s for s in d['stage_history'] if s['stage']=='FIRST_INTERVIEW' and s['result']=='ADVANCED');ref=json.loads(s['rationale'])['coverage']['M1_SKILL_02']['skill_decision_ref']
            next(x for x in d['evidence_decisions'] if x['decision_id']==ref).update(decision_status='INSUFFICIENT_EVIDENCE',final_level='')
        self.reject(change,'decisionable_coverage')

    def test_calibration_false_trigger(self):
        self.reject(lambda d:next(r for r in d['calibration_reviews'] if r['trigger_codes']=='[]').update(trigger_codes='["EVALUATOR_DISAGREEMENT"]'),'calibration_trigger')

    def test_calibration_without_audit(self):
        self.reject(lambda d:d['calibration_reviews'].remove(next(r for r in d['calibration_reviews'] if r['activity_id'])),'calibration_trigger')

    def test_skipped_calibration_still_has_lineage(self):
        skip=next(r for r in self.base['calibration_reviews'] if not r['activity_id']);ids=set(json.loads(skip['observation_ids']))
        self.assertTrue(any(r['observation_id'] in ids for r in self.base['skill_decision_observations']))
        def change(d):
            did=next(r['decision_id'] for r in d['skill_decision_observations'] if r['observation_id'] in ids)
            d['skill_decision_observations']=[r for r in d['skill_decision_observations'] if r['decision_id']!=did]
        self.reject(change,'decision_relation')

    def fixture(self,levels,contexts=None):
        when='2027-01-01T09:00:00+09:00';observations=[];evidence=[]
        for i,group in enumerate(levels):
            eid=str(i);evidence.append({'evidence_id':eid,'verification_mode':'DIRECT_TASK','context_id':(contexts or ['same']*len(levels))[i]})
            for j,level in enumerate(group):observations.append({'observation_id':f'{i}-{j}','evidence_id':eid,'skill_id':'M1_SKILL_01','application_id':'APP','created_at':when,'proposed_level':level,'explicit_limitation':'true' if level=='LIMITED' and len(set(group))==1 else 'false'})
        return {'assessment_evidence':evidence,'assessment_observations':observations},observations,parse(when)

    def test_consensus_limited_and_missing_no_meeting(self):
        for level in ('LIMITED','NOT_OBSERVED','MODERATE','STRONG'):
            data,obs,at=self.fixture([[level,level,level]])
            self.assertEqual(calibration_triggers(data,obs,at),[])

    def test_same_evidence_disagreement_triggers(self):
        data,obs,at=self.fixture([['LIMITED','MODERATE']]);self.assertEqual(calibration_triggers(data,obs,at),['EVALUATOR_DISAGREEMENT'])

    def test_evolution_not_conflict(self):
        data,obs,at=self.fixture([['LIMITED','LIMITED'],['MODERATE','MODERATE']],['early','later'])
        self.assertEqual(calibration_triggers(data,obs[-2:],at),[])
        data['assessment_evidence'][1]['context_id']='early'
        self.assertEqual(calibration_triggers(data,obs[-2:],at),['DIRECT_CONTEXT_CONFLICT'])

    def test_rereview_missing_must_cannot_proceed(self):
        d=copy.deepcopy(self.base);f=next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW');aid=f['application_id'];when=f['decided_at']
        for row in d['evidence_decisions']:
            if row['application_id']==aid and row['skill_id']=='M1_SKILL_02':row.update(decision_status='INSUFFICIENT_EVIDENCE',final_level='')
        result,trace=final_review(d,aid,self.rules,when,'RE_REVIEW')
        self.assertEqual(result,'DO_NOT_PROCEED');self.assertIn('M1_SKILL_02',trace['must_not_decisionable']);self.assertEqual(trace['decision_basis'],'INSUFFICIENT_DECISION_BASIS_AFTER_ONE_FOLLOW_UP')
        self.assertEqual(trace['accepted_uncertainty_plan'],[])

    def test_rereview_false_acceptance(self):
        def change(d):
            f=next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW' and json.loads(f['rationale'])['must_not_decisionable']);f['decision']='PROCEED_TO_OFFER'
        self.reject(change,'rereview_decisionable')

    def test_accepted_uncertainty_cannot_hide_must(self):
        def change(d):
            f=next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW' and json.loads(f['rationale'])['must_not_decisionable']);t=json.loads(f['rationale']);t['accepted_uncertainty_plan']=[{'skill_id':t['must_not_decisionable'][0],'scope':'LEARNABLE','action':'assume okay'}];f['rationale']=json.dumps(t)
        self.reject(change,'accepted_uncertainty')

    def test_censoring(self):
        r=copy.deepcopy(self.rules);r['observation_end']='2026-12-14T09:30:00+09:00';d=generate(r)
        self.assertEqual(validate(d,r)['errors'],[])


if __name__=='__main__':unittest.main()
