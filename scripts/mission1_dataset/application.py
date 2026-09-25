"""v0.5 self-reported experience and minimal eligibility scenario generation."""
import json
from datetime import date,timedelta
from .common import rng,compact,stamp
from .schema import PROVENANCE

ACTIONS={
 'COURSE_PROJECT': {'PROBLEM':'과제의 예측 목표와 허용 오차를 정의했다.','BUILD':'입력 데이터를 처리하고 예측을 수행하는 함수를 작성했다.','VALIDATE':'분리한 검증 입력에서 예측 오차를 비교했다.'},
 'PERSONAL_PROTOTYPE': {'PROBLEM':'반복 작업의 입력 조건과 자동화 범위를 정했다.','BUILD':'작업 순서를 실행하는 모듈을 구현했다.','VALIDATE':'빈 입력과 실패 상황 테스트를 실행하고 오류를 수정했다.'},
 'TEAM_PROJECT': {'PROBLEM':'담당 기능의 목표와 서비스 제약을 정리했다.','BUILD':'담당 기능의 모델 호출 코드를 구현했다.','VALIDATE':'담당 기능의 변경 전후 결과를 비교했다.'},
}


def eligibility_states(row):
    degree='UNKNOWN'
    if row['degree_level'] not in ('UNKNOWN','BACHELOR','MASTER'):degree='FAIL'
    elif row['degree_level']!='UNKNOWN':
        if row['graduation_status']=='GRADUATED':degree='PASS'
        elif row['graduation_status']=='EXPECTED' and row['expected_graduation_date']:
            degree='PASS' if row['expected_graduation_date']<=row['expected_join_date'] else 'FAIL'
    language='UNKNOWN'
    if row['language_test_type'] not in ('UNKNOWN','TOEIC_SPEAKING','OPIC'):language='FAIL'
    elif row['language_test_type']!='UNKNOWN' and row['language_test_valid_until']:
        language='PASS' if row['language_test_valid_until']>=row['eligibility_reference_date'] else 'FAIL'
    travel={'ELIGIBLE':'PASS','INELIGIBLE':'FAIL','UNKNOWN':'UNKNOWN'}[row['travel_visa_eligibility']]
    applicable=row['military_requirement_applicable']
    military='NOT_APPLICABLE' if applicable=='NO' else 'UNKNOWN' if applicable=='UNKNOWN' else {'COMPLETED':'PASS','EXEMPT':'PASS','NOT_COMPLETED':'FAIL','UNKNOWN':'UNKNOWN'}[row['military_requirement_status']]
    states={'degree':degree,'language':language,'travel_visa':travel,'military':military}
    return states, 'FAIL' if 'FAIL' in states.values() else 'UNKNOWN' if 'UNKNOWN' in states.values() else 'PASS'


def populate(gen,app):
    cfg=gen.rules['application_model'];clock=rng(gen.rules,'application-v05',app['candidate_id']);ref=app['submitted_at'][:10]
    applicable=clock.choice(['YES','NO'])
    row=dict(eligibility_id='EL_'+app['application_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],degree_level=clock.choice(['BACHELOR','MASTER']),graduation_status=clock.choice(['GRADUATED','EXPECTED']),expected_graduation_date='',language_test_type=clock.choice(['TOEIC_SPEAKING','OPIC']),language_test_valid_until=(date.fromisoformat(ref)+timedelta(days=180)).isoformat(),travel_visa_eligibility='ELIGIBLE',military_requirement_applicable=applicable,military_requirement_status='COMPLETED' if applicable=='YES' else 'NOT_APPLICABLE',eligibility_reference_date=ref,expected_join_date=cfg['expected_join_date'],public_source_ref=cfg['public_source_ref'],source_provenance=cfg['source_provenance'],date_provenance=cfg['date_provenance'],decision_provenance=PROVENANCE)
    if row['graduation_status']=='EXPECTED':row['expected_graduation_date']=(date.fromisoformat(row['expected_join_date'])-timedelta(days=1)).isoformat()
    scenario=clock.choice(cfg['eligibility_scenarios'])
    if scenario.startswith('DEGREE_'):row['degree_level']='OTHER' if scenario.endswith('FAIL') else 'UNKNOWN'
    elif scenario.startswith('LANGUAGE_'):
        row['language_test_valid_until']=(date.fromisoformat(ref)-timedelta(days=1)).isoformat() if scenario.endswith('FAIL') else ''
    elif scenario.startswith('TRAVEL_'):row['travel_visa_eligibility']='INELIGIBLE' if scenario.endswith('FAIL') else 'UNKNOWN'
    elif scenario.startswith('MILITARY_') and applicable=='YES':row['military_requirement_status']='NOT_COMPLETED' if scenario.endswith('FAIL') else 'UNKNOWN'
    states,overall=eligibility_states(row);row.update(requirement_states=compact(states),overall_state=overall)
    gen.add('application_eligibility',**row)
    ec=rng(gen.rules,'experience-v05',app['candidate_id'])
    for i in range(ec.choice(cfg['experience_counts'])):
        context=ec.choice(cfg['contexts']);cats=ec.choice(cfg['category_sets']);ownership=ec.choice(cfg['ownership'])
        gen.add('application_experiences',experience_id=f"XP_{app['application_id']}_{i+1:02d}",application_id=app['application_id'],candidate_id=app['candidate_id'],experience_type=context,ownership=ownership,actions=compact({c:ACTIONS[context][c] for c in cats}),evidence_categories=compact(cats),evidence_refs='[]',recorded_at=app['submitted_at'],decision_provenance=PROVENANCE)


def collect(gen,app,activity,when):
    for x in gen.data['application_experiences']:
        if x['application_id']!=app['application_id']:continue
        refs=[]
        for category,action in json.loads(x['actions']).items():
            skill='M1_SKILL_01' if category=='PROBLEM' else 'M1_SKILL_03'
            eid=f"EV_{x['experience_id']}_{category}_{skill}";refs.append(eid)
            raw={'task':category,'action':action,'verification':action if category=='VALIDATE' else '', 'revision':'','ownership':x['ownership'],'response':'지원서의 자기기술이며 직접 수행 검증이 아니다.','context':x['experience_type']}
            gen.add('assessment_evidence',evidence_id=eid,activity_id=activity['activity_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],source_type='APPLICATION_RESPONSE',verification_mode='SELF_REPORTED',context_id=x['experience_id'],source_ref=f'assessment_evidence.csv#{eid}/raw_evidence',raw_evidence=compact(raw),created_at=stamp(when))
        x['evidence_refs']=compact(refs)


def decision(data,app,resolution=False):
    row=next(r for r in data['application_eligibility'] if r['application_id']==app['application_id'])
    experiences=[x for x in data['application_experiences'] if x['application_id']==app['application_id']]
    qualifying=[x['experience_id'] for x in experiences if len(json.loads(x['actions']))>=2 and x['ownership'] in ('SELF','TEAM_CLEAR')]
    failed=[key for key,value in json.loads(row['requirement_states']).items() if value=='FAIL']
    trace={'eligibility_ref':row['eligibility_id'],'eligibility_state':row['overall_state'],'failed_requirements':failed,'experience_refs':[x['experience_id'] for x in experiences],'qualifying_experience_refs':qualifying,'observation_refs':[o['observation_id'] for o in data['assessment_observations'] if o['application_id']==app['application_id']],'skill_sufficiency_assessed':False}
    if failed:
        trace.update(public_requirement_ref=row['public_source_ref'],explicit_violation_ref=[row['eligibility_id']+'#'+key for key in failed],human_rationale='공개 자격 구조를 합성 일정에 적용한 명시적 미충족으로 이번 지원을 종료한다.')
        return 'FAILED','BASIC_REQUIREMENT_VIOLATION',trace
    if qualifying:
        trace['human_rationale']='동일 경험 안의 구체적 자기기술과 개인 역할을 후속 직접검증 대상으로 확인했다. UNKNOWN 자격은 미확인 상태로 보존한다.'
        if resolution and row['overall_state']=='UNKNOWN':
            trace['human_rationale']='직무 관련 자기기술은 후속검증 대상이다. 미확인 필수 자격은 사람의 확인을 거쳐야 하며 PRE 시작을 허용하지 않는다.'
            return 'CONDITIONAL_ADVANCE','ELIGIBILITY_CONFIRMATION_REQUIRED',trace
        return 'ADVANCED','APPLICATION_EVIDENCE_CANDIDATE',trace
    trace['human_rationale']='현재 제출된 지원서에서 다음 직접검증 단계로 진행할 충분한 직무 관련 Evidence Candidate를 확인하지 못했다. Skill 또는 능력 부족 판정이 아니다.'
    return 'CLOSED','INSUFFICIENT_APPLICATION_EVIDENCE',trace
