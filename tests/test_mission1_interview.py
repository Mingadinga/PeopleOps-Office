"""v0.3 adversarial persisted-data regressions and generation independence."""
import copy
import json
import tempfile
import unittest
from collections import Counter
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from scripts.mission1_dataset.common import load_rules, write_data, read_data, file_hashes, parse
from scripts.mission1_dataset.generate import generate, Generator
from scripts.mission1_dataset.validate import validate
from scripts.mission1_dataset.interview import collect_targeted
from scripts.mission1_dataset.schema import SCHEMA


class InterviewModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=load_rules(Path(__file__).resolve().parents[1]/'data/generation/v0.3/generation_rules.json');cls.base=generate(cls.rules)

    def reject(self,mutate,code):
        d=copy.deepcopy(self.base);mutate(d);v=validate(d,self.rules)
        self.assertIn(code,{e['code'] for e in v['errors']},v['errors'][:8])

    def test_valid_roundtrip_and_determinism(self):
        self.assertEqual(validate(self.base,self.rules)['errors'],[])
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            write_data(a,self.base);write_data(b,generate(copy.deepcopy(self.rules)))
            self.assertEqual(file_hashes(a),file_hashes(b));self.assertEqual(validate(read_data(a),self.rules)['errors'],[])

    def test_all_decision_oracles_unavailable(self):
        with ExitStack() as stack:
            for name in ('interpret','calibrate','final_review','stage_transition_decision'):
                stack.enter_context(patch('scripts.mission1_dataset.evidence.'+name,side_effect=AssertionError('oracle')))
            stack.enter_context(patch('scripts.mission1_dataset.interview.first_transition',side_effect=AssertionError('oracle')))
            self.assertEqual(validate(self.base,self.rules)['errors'],[])

    def test_target_and_channel_independence(self):
        r=copy.deepcopy(self.rules)
        for row in r['funnel_targets']:row[2]+=37
        r['workforce_plan']['target_join']=999;r['workforce_plan']['target_ready']=999
        r['applications']['channel_options']=['CAMPUS'];d=generate(r)
        for table in SCHEMA:
            if table!='applications':self.assertEqual(self.base[table],d[table],table)

    def test_legacy_write_protection(self):
        with tempfile.TemporaryDirectory() as root:
            for v in ('v0.1','v0.2'):
                with self.assertRaises(ValueError):write_data(Path(root)/v,self.base)

    def test_session_duration(self):
        self.reject(lambda d:next(a for a in d['assessment_activities'] if a['activity_type']=='FIRST_INTERVIEW_SESSION').update(completed_at='2027-01-01T09:00:00+09:00'),'interview_session')

    def test_three_interviewers(self):
        def change(d):
            a=next(a for a in d['assessment_activities'] if a['activity_type']=='FIRST_INTERVIEW_SESSION')
            d['activity_participants'].remove(next(p for p in d['activity_participants'] if p['activity_id']==a['activity_id']))
        self.reject(change,'interview_session')

    def test_domain_parent_required(self):
        self.reject(lambda d:d['activity_sessions'].pop(),'interview_session')

    def test_domain_effort_not_double_counted(self):
        def change(d):
            rel=d['activity_sessions'][0];p=copy.deepcopy(next(p for p in d['activity_participants'] if p['activity_id']==rel['session_activity_id']));p['activity_id']=rel['activity_id'];d['activity_participants'].append(p)
        self.reject(change,'participant_time')

    def test_initial_60(self):
        self.reject(lambda d:d['interview_capacity_events'][0].update(person_hours='80'),'capacity_initial')

    def test_resource_formula(self):
        self.reject(lambda d:next(e for e in d['interview_capacity_events'] if e['event_type']=='CAPACITY_ADDED').update(person_hours='800'),'capacity_resource')

    def test_consumption_parent_only(self):
        self.reject(lambda d:next(e for e in d['capacity_assignments'] if e['event_type']=='CONSUMED').update(person_hours='0.5'),'capacity_consumption')

    def test_release_replay(self):
        def change(d):d['capacity_assignments'].remove(next(r for r in d['capacity_assignments'] if r['event_type']=='RELEASED'))
        self.reject(change,'capacity_assignment')
        cap=self.base['capacity_assignments'];released=sum(float(r['person_hours']) for r in cap if r['event_type']=='RELEASED')
        reserved=sum(float(r['person_hours']) for r in cap if r['event_type']=='RESERVED');used=sum(float(r['person_hours']) for r in cap if r['event_type']=='CONSUMED')
        self.assertGreater(released,0);self.assertAlmostEqual(reserved,used+released)

    def test_evaluator_ledger_required(self):
        self.reject(lambda d:d['evaluator_reservations'].pop(0),'evaluator_reservation')

    def test_coverage_pending_not_advancement(self):
        def change(d):next(s for s in d['stage_history'] if s['decision_reason_code']=='EVIDENCE_PENDING').update(result='ADVANCED')
        self.reject(change,'first_coverage')

    def test_missing_not_failure(self):
        def change(d):next(s for s in d['stage_history'] if s['decision_reason_code']=='EVIDENCE_PENDING').update(result='FAILED',decision_reason_code='CORE_DIRECT_LIMITATION')
        self.reject(change,'first_coverage')

    def test_all_missing_stays_pending(self):
        r=copy.deepcopy(self.rules);r['evidence']['patterns']=['NOT_DOCUMENTED'];d=generate(r)
        first=[s for s in d['stage_history'] if s['stage']=='FIRST_INTERVIEW' and s['completed_at']]
        self.assertTrue(first);self.assertTrue(all(s['result']=='IN_PROGRESS' for s in first));self.assertFalse(d['offers']);self.assertEqual(validate(d,r)['errors'],[])

    def test_calibration_is_conditional(self):
        r=copy.deepcopy(self.rules);r['evidence']['patterns']=['EXPLICIT'];d=generate(r)
        self.assertFalse(any(a['activity_type'] in ('CALIBRATION','FOLLOW_UP_CALIBRATION') for a in d['assessment_activities']))
        self.assertEqual(validate(d,r)['errors'],[])

    def test_targeted_input_required(self):
        self.reject(lambda d:d['targeted_followups'][0].update(existing_observation_ids='[]'),'targeted_followup')

    def test_targeted_question_required(self):
        self.reject(lambda d:d['targeted_followups'][0].update(question='generic retest'),'targeted_followup')

    def test_targeted_outcome_family(self):
        self.reject(lambda d:d['targeted_followups'][0].update(response_kind='EXPLICIT'),'targeted_followup')

    def test_targeted_output_not_generic_pattern(self):
        def change(d):
            eid=d['targeted_followups'][0]['evidence_id'];e=next(e for e in d['assessment_evidence'] if e['evidence_id']==eid);raw=json.loads(e['raw_evidence']);raw['task']='generic';e['raw_evidence']=json.dumps(raw)
        self.reject(change,'targeted_followup')

    def test_no_ordinary_lottery_in_followup(self):
        g=Generator(self.rules);g.data=copy.deepcopy(self.base)
        a=next(a for a in g.data['assessment_activities'] if a['activity_type']=='FOCUSED_FOLLOW_UP');app=next(app for app in g.data['applications'] if app['application_id']==a['application_id'])
        with patch('scripts.mission1_dataset.evidence.observable',side_effect=AssertionError('ordinary lottery')):
            collect_targeted(g,app,a,parse(a['completed_at']))
        self.assertGreater(len(g.data['targeted_followups']),len(self.base['targeted_followups']))

    def test_rereview_never_hold(self):
        self.reject(lambda d:next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW').update(decision='HOLD'),'hold_contract')

    def test_current_self_only_strong_rejected(self):
        def change(d):
            decision=next(x for x in d['evidence_decisions'] if x['skill_id']=='M1_SKILL_01' and x['final_level']=='STRONG')
            ev={e['evidence_id']:e for e in d['assessment_evidence']}
            own=[o for o in d['assessment_observations'] if o['application_id']==decision['application_id'] and o['skill_id']==decision['skill_id'] and ev[o['evidence_id']]['verification_mode']=='SELF_REPORTED']
            d['skill_decision_observations']=[r for r in d['skill_decision_observations'] if r['decision_id']!=decision['decision_id']]+[{'decision_id':decision['decision_id'],'observation_id':o['observation_id']} for o in own]
            trace=json.loads(decision['rationale']);trace['supporting_observation_ids']=[o['observation_id'] for o in own];decision['rationale']=json.dumps(trace)
        self.reject(change,'self_reported_strong')

    def test_current_expiry_deadline(self):
        def change(d):
            event=next(e for e in d['offer_events'] if e['event_type']=='EXPIRED')
            next(o for o in d['offers'] if o['offer_id']==event['offer_id'])['response_deadline']='2028-01-01T09:00:00+09:00'
        self.reject(change,'offer_deadline')

    def test_current_ready_work_required(self):
        def change(d):
            event=next(e for e in d['workforce_events'] if e['event_type']=='READY_CONFIRMED');trace=json.loads(event['source_ref']);trace['work_evidence_refs']=[];event['source_ref']=json.dumps(trace)
        self.reject(change,'work_evidence')

    def test_current_observation_lineage(self):
        def change(d):
            did=d['evidence_decisions'][0]['decision_id'];d['skill_decision_observations']=[r for r in d['skill_decision_observations'] if r['decision_id']!=did]
        self.reject(change,'decision_relation')

    def test_censored_window(self):
        r=copy.deepcopy(self.rules);r['observation_end']='2026-12-14T09:30:00+09:00';d=generate(r)
        self.assertEqual(validate(d,r)['errors'],[])
        self.assertTrue(any(not p['participation_ended_at'] for p in d['activity_participants']))


if __name__=='__main__':unittest.main()
