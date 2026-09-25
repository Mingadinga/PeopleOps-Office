"""Independent persisted application contract; never imports generation decisions."""
import json
from datetime import date
from collections import defaultdict


def validate_application(data,rules,check):
    apps={a['application_id']:a for a in data['applications']};submitted={k for k,a in apps.items() if a['submitted_at']}
    elig={r['application_id']:r for r in data['application_eligibility']};experiences=defaultdict(list);ev={e['evidence_id']:e for e in data['assessment_evidence']};states={};eligible_x=defaultdict(list)
    check(set(elig)==submitted and len(elig)==len(data['application_eligibility']),'eligibility','Exactly one eligibility row per submission')
    for aid,r in elig.items():
        check(r['eligibility_id']=='EL_'+aid,'eligibility','Stable identity')
        check(r['source_provenance']=='PUBLIC_REPOSTED_SOURCE' and r['date_provenance']=='SYNTHETIC_DATE_ADAPTATION' and r['public_source_ref']=='KIA-02-REPOST' and r['decision_provenance']=='SYNTHETIC_HUMAN_SCENARIO','eligibility','Provenance boundary')
        check(r['eligibility_reference_date']==apps[aid]['submitted_at'][:10] and r['expected_join_date']==rules['application_model']['expected_join_date'],'eligibility','Synthetic date contract')
        for k in ['eligibility_reference_date','expected_join_date','expected_graduation_date','language_test_valid_until']:
            if r[k]:date.fromisoformat(r[k])
        enums={'degree_level':['BACHELOR','MASTER','OTHER','UNKNOWN'],'graduation_status':['GRADUATED','EXPECTED','UNKNOWN'],'language_test_type':['TOEIC_SPEAKING','OPIC','NONE','UNKNOWN'],'travel_visa_eligibility':['ELIGIBLE','INELIGIBLE','UNKNOWN'],'military_requirement_applicable':['YES','NO','UNKNOWN'],'military_requirement_status':['COMPLETED','EXEMPT','NOT_COMPLETED','NOT_APPLICABLE','UNKNOWN']}
        for k,values in enums.items():check(r[k] in values,'eligibility',k)
        degree='UNKNOWN'
        if r['degree_level']=='OTHER':degree='FAIL'
        elif r['degree_level'] in ('BACHELOR','MASTER'):
            if r['graduation_status']=='GRADUATED':degree='PASS'
            elif r['graduation_status']=='EXPECTED' and r['expected_graduation_date']:degree='PASS' if date.fromisoformat(r['expected_graduation_date'])<=date.fromisoformat(r['expected_join_date']) else 'FAIL'
        language='FAIL' if r['language_test_type']=='NONE' else 'UNKNOWN'
        if r['language_test_type'] in ('TOEIC_SPEAKING','OPIC') and r['language_test_valid_until']:language='PASS' if date.fromisoformat(r['language_test_valid_until'])>=date.fromisoformat(r['eligibility_reference_date']) else 'FAIL'
        travel={'ELIGIBLE':'PASS','INELIGIBLE':'FAIL'}.get(r['travel_visa_eligibility'],'UNKNOWN')
        military='UNKNOWN'
        if r['military_requirement_applicable']=='NO':
            military='NOT_APPLICABLE';check(r['military_requirement_status']=='NOT_APPLICABLE','eligibility','N/A consistency')
        elif r['military_requirement_applicable']=='YES':
            check(r['military_requirement_status']!='NOT_APPLICABLE','eligibility','Applicable cannot be N/A')
            military={'COMPLETED':'PASS','EXEMPT':'PASS','NOT_COMPLETED':'FAIL'}.get(r['military_requirement_status'],'UNKNOWN')
        st={'degree':degree,'language':language,'travel_visa':travel,'military':military};states[aid]=st
        overall='FAIL' if any(v=='FAIL' for v in st.values()) else 'UNKNOWN' if any(v=='UNKNOWN' for v in st.values()) else 'PASS'
        check(json.loads(r['requirement_states'])==st and r['overall_state']==overall,'eligibility','Recorded state differs from raw facts')
    allrefs=[]
    for x in data['application_experiences']:
        aid=x['application_id'];experiences[aid].append(x);actions=json.loads(x['actions']);categories=json.loads(x['evidence_categories']);refs=json.loads(x['evidence_refs']);allrefs+=refs
        check(aid in submitted and x['experience_id'].startswith('XP_'+aid+'_') and x['recorded_at']==apps[aid]['submitted_at'],'experience','Submission/stable ID/time')
        check(x['decision_provenance']=='SYNTHETIC_HUMAN_SCENARIO','experience','Provenance')
        check(set(actions)==set(categories) and len(categories)==len(set(categories)) and set(categories)<={'PROBLEM','BUILD','VALIDATE'} and all(isinstance(v,str) and v.strip() for v in actions.values()),'experience','Categories require concrete actions')
        check(x['ownership'] in ('SELF','TEAM_CLEAR','TEAM_UNCLEAR'),'experience','Ownership enum')
        phrases={
          'COURSE_PROJECT': {'PROBLEM':'과제의 예측 목표와 허용 오차를 정의했다.','BUILD':'입력 데이터를 처리하고 예측을 수행하는 함수를 작성했다.','VALIDATE':'분리한 검증 입력에서 예측 오차를 비교했다.'},
          'PERSONAL_PROTOTYPE': {'PROBLEM':'반복 작업의 입력 조건과 자동화 범위를 정했다.','BUILD':'작업 순서를 실행하는 모듈을 구현했다.','VALIDATE':'빈 입력과 실패 상황 테스트를 실행하고 오류를 수정했다.'},
          'TEAM_PROJECT': {'PROBLEM':'담당 기능의 목표와 서비스 제약을 정리했다.','BUILD':'담당 기능의 모델 호출 코드를 구현했다.','VALIDATE':'담당 기능의 변경 전후 결과를 비교했다.'}}
        check(x['experience_type'] in phrases and all(value==phrases.get(x['experience_type'],{}).get(cat) for cat,value in actions.items()),'experience','Unsubstantiated action/category in fixed synthetic catalog')
        # A closed/censored Document Activity need not yet have emitted its raw rows.
        screen=next((s for s in data['stage_history'] if s['application_id']==aid and s['stage']=='DOCUMENT_SCREEN'),{})
        if any(a['stage_event_id']==screen.get('stage_event_id') and a['activity_type']=='DOCUMENT_REVIEW' and a['activity_status']=='COMPLETED' for a in data['assessment_activities']):check(len(refs)==len(actions),'experience','Evidence missing for completed review')
        linked_categories=[]
        for ref in refs:
            e=ev.get(ref);check(e is not None,'experience','Dangling Evidence')
            if not e:continue
            raw=json.loads(e['raw_evidence']);category=raw['task'];linked_categories.append(category)
            check(e['application_id']==aid and e['candidate_id']==x['candidate_id'] and e['context_id']==x['experience_id'] and e['source_type']=='APPLICATION_RESPONSE' and e['verification_mode']=='SELF_REPORTED','experience','Foreign experience or source')
            check(raw['action']==actions.get(category) and raw['ownership']==x['ownership'] and raw['context']==x['experience_type'],'experience','Application cards disagree with experience')
            expected='M1_SKILL_01' if category=='PROBLEM' else 'M1_SKILL_03'
            for link in data['evidence_skill_links']:
                if link['evidence_id']==ref:check(link['confirmed_skill_id']==expected,'experience','Category Skill boundary')
        if refs:check(set(linked_categories)==set(categories) and len(linked_categories)==len(set(linked_categories)),'experience','Missing/duplicate category evidence')
        if len(actions)>=2 and x['ownership'] in ('SELF','TEAM_CLEAR'):eligible_x[aid].append(x['experience_id'])
    check(set(experiences)==submitted,'experience','One or more experiences per submission')
    check(len(allrefs)==len(set(allrefs)) and set(allrefs)=={e['evidence_id'] for e in ev.values() if e['source_type']=='APPLICATION_RESPONSE'},'experience','Orphan/duplicate application Evidence')
    for s in data['stage_history']:
        if s['result']=='CLOSED':check(s['stage']=='DOCUMENT_SCREEN','document_rule','CLOSED is Document-only')
        if s['stage']!='DOCUMENT_SCREEN' or not s['decision_at']:continue
        aid=s['application_id'];t=json.loads(s['rationale']);failed=sorted(k for k,v in states.get(aid,{}).items() if v=='FAIL')
        result,reason=('FAILED','BASIC_REQUIREMENT_VIOLATION') if failed else ('ADVANCED','APPLICATION_EVIDENCE_CANDIDATE') if eligible_x[aid] else ('CLOSED','INSUFFICIENT_APPLICATION_EVIDENCE')
        if rules.get('eligibility_resolution') and result=='ADVANCED' and elig[aid]['overall_state']=='UNKNOWN':result,reason='CONDITIONAL_ADVANCE','ELIGIBILITY_CONFIRMATION_REQUIRED'
        check((s['result'],s['decision_reason_code'])==(result,reason),'document_rule','Wrong same-experience/eligibility decision')
        check(t.get('eligibility_ref')==elig[aid]['eligibility_id'] and t.get('eligibility_state')==elig[aid]['overall_state'] and sorted(t.get('failed_requirements',[]))==failed,'document_rule','Eligibility trace')
        check(set(t.get('experience_refs',[]))=={x['experience_id'] for x in experiences[aid]} and set(t.get('qualifying_experience_refs',[]))==set(eligible_x[aid]),'document_rule','Experience trace')
        check(t.get('skill_sufficiency_assessed') is False and bool(t.get('human_rationale')),'document_rule','Document is not a Skill judgment')
        if failed:check(t.get('public_requirement_ref')=='KIA-02-REPOST' and set(t.get('explicit_violation_ref',[]))=={elig[aid]['eligibility_id']+'#'+k for k in failed},'document_rule','Missing requirement failure reference')
        check(not any(dc['application_id']==aid and dc['decided_at']<=s['decision_at'] for dc in data['evidence_decisions']),'document_rule','Document cannot create canonical Skill Decision')
