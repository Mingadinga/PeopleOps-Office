"""Independent eligibility gate checks based on persisted facts and event times."""
import json
from collections import defaultdict
from datetime import timedelta
from .common import parse


def validate_resolution(data,rules,check):
    initial={r['application_id']:r for r in data['application_eligibility']};docs={s['application_id']:s for s in data['stage_history'] if s['stage']=='DOCUMENT_SCREEN'};events=defaultdict(dict)
    cfg=rules['eligibility_resolution'];end=parse(rules['observation_end'])
    for e in data['eligibility_verifications']:
        aid=e['application_id'];req=e['requirement'];row=initial.get(aid);doc=docs.get(aid);previous=json.loads(row['requirement_states']) if row else {}
        check(doc is not None and doc['result']=='CONDITIONAL_ADVANCE' and req in previous and previous.get(req)=='UNKNOWN' and e['previous_status']=='UNKNOWN','eligibility_resolution','Only conditional UNKNOWN requirements can be verified')
        check(req not in events[aid],'eligibility_resolution','Duplicate verification');events[aid][req]=e
        if not row or not doc:continue
        check(e['verification_id']=='VERIFY_'+aid+'_'+req and e['eligibility_id']==row['eligibility_id'],'eligibility_resolution','Stable requirement reference')
        requested=parse(e['verification_requested_at']);deadline=parse(e['verification_deadline'])
        check(bool(doc['notified_at']) and requested==parse(doc['notified_at'])+timedelta(days=1) and deadline==requested+timedelta(days=cfg['deadline_days']),'eligibility_resolution','Request/deadline ordering')
        result=e['verification_result'];status=e['resulting_status'];fact=json.loads(e['verification_evidence'])
        check(result in ('VERIFIED_PASS','VERIFIED_FAIL','ELIGIBILITY_NOT_VERIFIED','PENDING') and e['decision_provenance']=='SYNTHETIC_HUMAN_SCENARIO' and bool(e['rationale']),'eligibility_resolution','Result/provenance')
        if result in ('VERIFIED_PASS','VERIFIED_FAIL'):
            approved={'degree':{'BACHELOR_GRADUATED':'PASS','NON_QUALIFYING_DEGREE':'FAIL'},'language':{'VALID_ACCEPTED_TEST':'PASS','EXPIRED_ACCEPTED_TEST':'FAIL'},'travel_visa':{'ELIGIBLE':'PASS','INELIGIBLE':'FAIL'},'military':{'COMPLETED':'PASS','NOT_COMPLETED':'FAIL'}}
            expected=approved.get(req,{}).get(fact.get('confirmed_fact'))
            check(expected==status and result==('VERIFIED_PASS' if status=='PASS' else 'VERIFIED_FAIL'),'eligibility_resolution','Confirmation lacks matching requirement fact')
            check(set(fact)=={'requirement','confirmed_fact','reference_date','expected_join_date','evidence_type'} and fact.get('requirement')==req and fact.get('reference_date')==row['eligibility_reference_date'] and fact.get('expected_join_date')==row['expected_join_date'] and fact.get('evidence_type')=='SYNTHETIC','eligibility_resolution','Fact context/provenance')
            check(bool(e['verified_at']) and e['resolved_at']==e['verified_at'] and e['confirmed_by']=='HR_OPERATIONS_01','eligibility_resolution','Human confirmation missing')
            if e['verified_at']:check(requested<parse(e['verified_at'])<=deadline and parse(e['verified_at'])==requested+timedelta(days=cfg['response_days']),'eligibility_resolution','Response time')
        else:
            check(status=='UNKNOWN' and not fact and not e['verified_at'] and not e['confirmed_by'],'eligibility_resolution','No response is not FAIL or invented verification')
            if result=='ELIGIBILITY_NOT_VERIFIED':check(e['resolved_at']==e['verification_deadline'] and deadline<=end,'eligibility_resolution','Premature expiry')
            else:check(not e['resolved_at'] and deadline>end,'eligibility_resolution','Pending must be censored before deadline')
    for aid,doc in docs.items():
        if doc['result']!='CONDITIONAL_ADVANCE':continue
        reqs={k for k,v in json.loads(initial[aid]['requirement_states']).items() if v=='UNKNOWN'}
        check(bool(reqs),'eligibility_resolution','Conditional without unknown')
        if doc['notified_at'] and parse(doc['notified_at'])+timedelta(days=1)<=end:check(set(events[aid])==reqs,'eligibility_resolution','Missing verification request')
    def passed_at(aid,at):
        if aid not in initial:return False
        for req,status in json.loads(initial[aid]['requirement_states']).items():
            if status in ('PASS','NOT_APPLICABLE'):continue
            e=events[aid].get(req,{})
            if status!='UNKNOWN' or e.get('verification_result')!='VERIFIED_PASS' or not e.get('verified_at') or parse(e['verified_at'])>=parse(at):return False
        return True
    pre={s['stage_event_id']:s for s in data['stage_history'] if s['stage']=='PRE_ASSESSMENT'}
    for s in pre.values():check(passed_at(s['application_id'],s['entered_at']),'eligibility_gate','PRE entry without resolved PASS/N/A')
    for a in data['assessment_activities']:
        if a['stage_event_id'] in pre and a['started_at']:check(passed_at(a['application_id'],a['started_at']),'eligibility_gate','PRE activity before verification')
    for o in data['offers']:check(passed_at(o['application_id'],o['offered_at']),'eligibility_gate','Offer with unresolved eligibility')
    apps={r['candidate_id']:r['application_id'] for r in data['applications']}
    for p in data['onboarding_profiles']:check(passed_at(apps[p['source_candidate_id']],p['joined_at']),'eligibility_gate','Join with unresolved eligibility')
