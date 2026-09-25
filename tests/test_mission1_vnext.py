"""Adversarial SSOT regression fixtures, never persisted as review data."""
import copy
import json
import unittest
from unittest.mock import patch
from scripts.mission1_dataset.common import load_rules, parse
from scripts.mission1_dataset.generate import generate, Generator
from scripts.mission1_dataset.evidence import calibrate
from scripts.mission1_dataset.validate import validate
from scripts.mission1_dataset.report import summarize


class InvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=load_rules(__import__('pathlib').Path(__file__).resolve().parents[1]/'data/generation/v0.2/generation_rules.json');cls.base=generate(cls.rules)

    def reject(self,mutate,code):
        d=copy.deepcopy(self.base);mutate(d);v=validate(d,self.rules)
        self.assertEqual(v['status'],'ERROR')
        self.assertIn(code,{e['code'] for e in v['errors']},v['errors'][:5])

    def test_validator_has_no_generator_oracle(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            for name in ('interpret','calibrate','final_review','stage_transition_decision'):
                stack.enter_context(patch('scripts.mission1_dataset.evidence.'+name,side_effect=AssertionError('oracle')))
            self.assertEqual(validate(self.base,self.rules)['status'],'PASS')

    def test_self_reported_only_strong(self):
        def change(d):
            decision=next(r for r in d['evidence_decisions'] if r['skill_id']=='M1_SKILL_01');ev={e['evidence_id']:e for e in d['assessment_evidence']}
            obs=[o for o in d['assessment_observations'] if o['application_id']==decision['application_id'] and o['skill_id']==decision['skill_id'] and ev[o['evidence_id']]['verification_mode']=='SELF_REPORTED']
            d['skill_decision_observations']=[r for r in d['skill_decision_observations'] if r['decision_id']!=decision['decision_id']]+[{'decision_id':decision['decision_id'],'observation_id':o['observation_id']} for o in obs]
            trace=json.loads(decision['rationale']);trace['supporting_observation_ids']=[o['observation_id'] for o in obs]
            decision.update(final_level='STRONG',decision_status='AGREED',rationale=json.dumps(trace))
        self.reject(change,'self_reported_strong')

    def test_self_reported_strong_observation_allowed(self):
        ev={e['evidence_id']:e for e in self.base['assessment_evidence']}
        self.assertTrue(any(o['proposed_level']=='STRONG' and ev[o['evidence_id']]['verification_mode']=='SELF_REPORTED' for o in self.base['assessment_observations']))
        self.assertEqual(validate(self.base,self.rules)['errors'],[])

    def test_wrong_verification_mode(self):
        self.reject(lambda d:d['assessment_evidence'][0].update(verification_mode='DIRECT_TASK'),'verification_mode')

    def test_independent_source_matrix(self):
        def change(d):
            e=next(e for e in d['assessment_evidence'] if e['source_type']=='CODING_TEST_RESPONSE')
            next(l for l in d['evidence_skill_links'] if l['evidence_id']==e['evidence_id'])['confirmed_skill_id']='M1_SKILL_05'
        self.reject(change,'source_skill_matrix')

    def test_no_raw_bypass_relation(self):
        self.reject(lambda d:d.update(evidence_decision_sources=[]),'canonical_lineage')

    def test_future_observation(self):
        def change(d):
            rel=d['skill_decision_observations'][0];next(o for o in d['assessment_observations'] if o['observation_id']==rel['observation_id'])['created_at']=self.rules['observation_end']
        self.reject(change,'temporal')

    def test_no_document_skill_confirmation(self):
        for s in self.base['stage_history']:
            if s['stage']=='DOCUMENT_SCREEN' and s['decision_at']:
                self.assertFalse(any(d['application_id']==s['application_id'] and d['decided_at']<=s['decision_at'] for d in self.base['evidence_decisions']))

    def test_document_failure_needs_public_violation(self):
        self.reject(lambda d:d['stage_history'][0].update(result='FAILED',decision_reason_code='BASIC_REQUIREMENT_VIOLATION'),'stage_decision')

    def test_no_offer_decision_in_stage(self):
        def change(d):
            s=d['stage_history'][0];trace=json.loads(s['rationale']);trace['decision']='PROCEED_TO_OFFER';s['rationale']=json.dumps(trace)
        self.reject(change,'stage_decision')

    def test_final_stage_cannot_duplicate_outcome(self):
        self.reject(lambda d:next(s for s in d['stage_history'] if s['stage']=='FINAL_REVIEW' and s['decision_at']).update(result='ADVANCED'),'stage_decision')

    def test_persisted_observations_and_context_difference(self):
        ev={'a':{'verification_mode':'DIRECT_TASK','context_id':'a'},'b':{'verification_mode':'DIRECT_TASK','context_id':'b'}}
        obs=[{'evidence_id':'a','observation_id':'a','proposed_level':'LIMITED'},{'evidence_id':'b','observation_id':'b','proposed_level':'STRONG'}]
        level,status,trace=calibrate(obs,ev)
        self.assertEqual((level,status),('STRONG','AGREED'));self.assertIn('CONTEXT_DIFFERENCE',trace['difference_types'])
        obs[-1]['proposed_level']='NOT_OBSERVED';self.assertEqual(calibrate(obs,ev)[0],'LIMITED')

    def test_same_context_conflict(self):
        ev={'a':{'verification_mode':'DIRECT_TASK','context_id':'same'},'b':{'verification_mode':'DIRECT_TASK','context_id':'same'}}
        obs=[{'evidence_id':'a','observation_id':'a','proposed_level':'LIMITED'},{'evidence_id':'b','observation_id':'b','proposed_level':'STRONG'}]
        self.assertEqual(calibrate(obs,ev)[1],'DISAGREEMENT_REMAINS')

    def test_hold_reason_required(self):
        self.reject(lambda d:next(f for f in d['final_decisions'] if f['decision']=='HOLD').update(hold_reason_code=''),'hold_contract')

    def test_hold_resolution_required(self):
        self.reject(lambda d:next(f for f in d['final_decisions'] if f['decision']=='HOLD').update(resolution_plan='[]'),'hold_contract')

    def test_rereview_hold_forbidden(self):
        self.reject(lambda d:next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW').update(decision='HOLD'),'hold_contract')

    def test_rereview_followup_required(self):
        self.reject(lambda d:next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW').update(follow_up_activity_id=''),'hold_contract')

    def test_followup_calibration_required(self):
        def change(d):
            f=next(f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW');initial=next(g for g in d['final_decisions'] if g['application_id']==f['application_id'] and g['review_round']=='INITIAL')
            trace=json.loads(f['rationale']);trace['decision_refs']=json.loads(initial['rationale'])['decision_refs'];f['rationale']=json.dumps(trace)
        self.reject(change,'hold_contract')

    def test_only_one_followup(self):
        def change(d):
            a=copy.deepcopy(next(a for a in d['assessment_activities'] if a['activity_type']=='FOCUSED_FOLLOW_UP'));a['activity_id']+='SECOND';d['assessment_activities'].append(a)
        self.reject(change,'hold_contract')

    def test_missing_alone_not_rereview_failure(self):
        r=copy.deepcopy(self.rules);r['evidence']['patterns']=['NOT_DOCUMENTED'];d=generate(r)
        finals=[f for f in d['final_decisions'] if f['review_round']=='RE_REVIEW'];self.assertTrue(finals)
        self.assertTrue(all(f['decision']=='PROCEED_TO_OFFER' for f in finals));self.assertEqual(validate(d,r)['errors'],[])

    def test_capacity_initial_immutable(self):
        self.reject(lambda d:d['interview_capacity_events'][0].update(person_hours='800'),'capacity_initial')

    def test_capacity_not_quota(self):
        self.assertGreater(sum(s['stage']=='FIRST_INTERVIEW' for s in self.base['stage_history']),20)
        e=next(e for e in self.base['interview_capacity_events'] if e['event_type']=='GAP_IDENTIFIED')
        self.assertEqual(float(e['demand_person_hours']),len(json.loads(e['cohort_application_ids']))*4)

    def test_capacity_gap_recomputed(self):
        self.reject(lambda d:next(e for e in d['interview_capacity_events'] if e['event_type']=='GAP_IDENTIFIED').update(person_hours='0'),'capacity_gap')

    def test_capacity_actual_not_plan(self):
        self.reject(lambda d:next(e for e in d['capacity_assignments'] if e['event_type']=='CONSUMED').update(person_hours='4'),'capacity_consumption')

    def test_unused_reservation_release(self):
        def change(d):
            d['capacity_assignments'].remove(next(e for e in d['capacity_assignments'] if e['event_type']=='RELEASED' and e['reason_code']=='CONFIRMED_WITHDRAWAL_UNUSED'))
        self.reject(change,'capacity_assignment')

    def test_no_response_is_not_withdrawal(self):
        idx={s['stage_event_id']:s for s in self.base['stage_history']};rows=[r for r in self.base['capacity_assignments'] if r['reason_code']=='NO_RESPONSE_UNUSED']
        self.assertTrue(rows);self.assertTrue(all(idx[r['stage_event_id']]['result']=='IN_PROGRESS' for r in rows))

    def test_pool_role_consistency(self):
        def change(d):
            r=d['activity_participants'][0];next(p for p in d['activity_participants'][1:] if p['participant_id']==r['participant_id'])['participant_role']='HIRING_MANAGER'
        self.reject(change,'evaluator_pool')

    def test_expired_requires_elapsed_deadline(self):
        def change(d):
            e=next(e for e in d['offer_events'] if e['event_type']=='EXPIRED');next(o for o in d['offers'] if o['offer_id']==e['offer_id'])['response_deadline']='2028-01-01T09:00:00+09:00'
        self.reject(change,'offer_deadline')

    def test_expired_cannot_have_response(self):
        def change(d):
            e=copy.deepcopy(next(e for e in d['offer_events'] if e['event_type']=='EXPIRED'));e.update(event_type='ACCEPTED',offer_event_id=e['offer_event_id']+'_response',reason_code='');d['offer_events'].append(e)
        self.reject(change,'offer_deadline')

    def test_no_response_not_motive(self):
        self.reject(lambda d:next(e for e in d['offer_events'] if e['event_type']=='EXPIRED').update(reason_code='NO_RESPONSE'),'offer_motive')

    def test_ready_human_confirmation(self):
        self.reject(lambda d:next(e for e in d['workforce_events'] if e['event_type']=='READY_CONFIRMED').update(confirmed_by=''),'ready_confirmation')

    def test_ready_work_required(self):
        def change(d):
            e=next(e for e in d['workforce_events'] if e['event_type']=='READY_CONFIRMED');trace=json.loads(e['source_ref']);trace['work_evidence_refs']=[];e['source_ref']=json.dumps(trace)
        self.reject(change,'work_evidence')

    def test_ready_every_gap(self):
        def change(d):
            e=next(e for e in d['workforce_events'] if e['event_type']=='READY_CONFIRMED' and json.loads(e['source_ref'])['gap_ids']);trace=json.loads(e['source_ref']);trace['gap_ids']=[];e['source_ref']=json.dumps(trace)
        self.reject(change,'work_evidence')

    def test_individual_onboarding_gaps(self):
        gaps={p['employee_id']:tuple(sorted(g['skill_id'] for g in self.base['onboarding_skill_gaps'] if g['employee_id']==p['employee_id'])) for p in self.base['onboarding_profiles']}
        self.assertGreater(len(set(gaps.values())),1)
        self.reject(lambda d:d['onboarding_skill_gaps'][0].update(skill_id='M1_SKILL_09'),'onboarding_gap')

    def test_cancel_releases_unused_without_withdrawal(self):
        r=copy.deepcopy(self.rules);r['process']['withdrawal_contacts']=['CANCEL_CONFIRMED']
        g=Generator(r);g.plans();g.applications();app=next(a for a in g.data['applications'] if a['submitted_at'])
        g.stage(app,'FIRST_INTERVIEW',parse('2026-12-01T09:00:00+09:00'))
        stage=g.data['stage_history'][0];self.assertEqual(stage['result'],'IN_PROGRESS');self.assertFalse(stage['withdrawn_at'])
        released=[e for e in g.data['capacity_assignments'] if e['event_type']=='RELEASED']
        self.assertEqual(float(released[0]['person_hours']),4);self.assertEqual(released[0]['reason_code'],'CANCELLED_UNUSED')
        self.assertTrue(all(a['activity_status']=='CANCELLED' for a in g.data['assessment_activities']))

    def test_open_before_deadline(self):
        r=copy.deepcopy(self.rules);r['offers']['response_events']=['NO_RESPONSE'];r['offers']['response_window_days']=365;d=generate(r)
        self.assertTrue(d['offers']);self.assertFalse(any(e['event_type']=='EXPIRED' for e in d['offer_events']));self.assertEqual(validate(d,r)['errors'],[])

    def test_right_censoring(self):
        r=copy.deepcopy(self.rules);r['observation_end']='2027-03-01T09:15:00+09:00';d=generate(r);v=validate(d,r)
        self.assertEqual(v['errors'],[]);self.assertTrue(any(s['result']=='IN_PROGRESS' for s in d['stage_history']))
        self.assertTrue(all(not s['notified_at'] or s['notified_at']<=r['observation_end'] for s in d['stage_history']))
        self.assertIsNone(summarize(d,r,v)['time_distributions']['scheduling_wait']['DOCUMENT_SCREEN']['median'])


if __name__=='__main__':unittest.main()
