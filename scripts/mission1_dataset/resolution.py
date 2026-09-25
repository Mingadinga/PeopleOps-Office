"""Synthetic administrative confirmation; initial eligibility is immutable."""
import json
from .common import rng,stamp,plus,parse,compact
from .schema import PROVENANCE

FACTS={
 'degree':('BACHELOR_GRADUATED','NON_QUALIFYING_DEGREE'),
 'language':('VALID_ACCEPTED_TEST','EXPIRED_ACCEPTED_TEST'),
 'travel_visa':('ELIGIBLE','INELIGIBLE'),
 'military':('COMPLETED','NOT_COMPLETED'),
}


def resolve_queue(gen,queue):
    cfg=gen.rules['eligibility_resolution'];out=[]
    for app,requested in queue:
        row=next(e for e in gen.data['application_eligibility'] if e['application_id']==app['application_id'])
        if row['overall_state']=='PASS':out.append((app,requested));continue
        if row['overall_state']!='UNKNOWN' or requested>gen.end:continue
        deadline=plus(requested,days=cfg['deadline_days']);resolved=[]
        for requirement,previous in json.loads(row['requirement_states']).items():
            if previous!='UNKNOWN':continue
            selected=rng(gen.rules,'eligibility-verification',app['application_id'],requirement).choice(cfg['response_scenarios'])
            when=deadline if selected=='ELIGIBILITY_NOT_VERIFIED' else plus(requested,days=cfg['response_days'])
            result=selected if when<=gen.end else 'PENDING';fact={};status='UNKNOWN';verified='';at='';actor=''
            if result!='PENDING':
                at=stamp(when)
                if result in ('VERIFIED_PASS','VERIFIED_FAIL'):
                    status='PASS' if result=='VERIFIED_PASS' else 'FAIL';verified=at;actor='HR_OPERATIONS_01'
                    fact={'requirement':requirement,'confirmed_fact':FACTS[requirement][status=='FAIL'],'reference_date':row['eligibility_reference_date'],'expected_join_date':row['expected_join_date'],'evidence_type':'SYNTHETIC'}
            event=gen.add('eligibility_verifications',verification_id='VERIFY_'+app['application_id']+'_'+requirement,application_id=app['application_id'],candidate_id=app['candidate_id'],eligibility_id=row['eligibility_id'],requirement=requirement,previous_status=previous,verification_requested_at=stamp(requested),verification_deadline=stamp(deadline),verification_result=result,verified_at=verified,resolved_at=at,resulting_status=status,verification_evidence=compact(fact),confirmed_by=actor,decision_provenance=PROVENANCE,rationale='필수 지원자격을 사람이 확인한 합성 기록. 기한 내 미확인은 자격 미달/Skill 부족이 아니며 이번 절차 진행을 종료한다.')
            resolved.append(event)
        if resolved and all(e['verification_result']=='VERIFIED_PASS' for e in resolved):
            out.append((app,plus(max(parse(e['verified_at']) for e in resolved),days=1)))
    return out
