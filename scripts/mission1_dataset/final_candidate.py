"""Approved v0.4 generation policy; independent checks live in another module."""
import json
from collections import defaultdict
from .common import compact,stamp


def calibration_triggers(data,current,at):
    evidence={e['evidence_id']:e for e in data['assessment_evidence']}
    current_ids={o['evidence_id'] for o in current};by_evidence=defaultdict(set)
    for o in current:by_evidence[o['evidence_id']].add(o['proposed_level'])
    triggers=[]
    if any(len(levels)>1 for levels in by_evidence.values()):triggers.append('EVALUATOR_DISAGREEMENT')
    contexts=defaultdict(list)
    applications={o['application_id'] for o in current}
    for o in data['assessment_observations']:
        e=evidence[o['evidence_id']]
        if o['application_id'] in applications and o['created_at']<=stamp(at) and e['verification_mode']!='SELF_REPORTED':contexts[(o['skill_id'],e['context_id'])].append(o)
    for rows in contexts.values():
        limited={o['evidence_id'] for o in rows if o['explicit_limitation']=='true'}
        positive={o['evidence_id'] for o in rows if o['proposed_level'] in ('MODERATE','STRONG')}
        if limited and positive-limited and (limited|positive)&current_ids:
            triggers.append('DIRECT_CONTEXT_CONFLICT');break
    return sorted(triggers)


def record_calibration_review(gen,app,stage,at,kind,current):
    triggers=calibration_triggers(gen.data,current,at)
    return gen.add('calibration_reviews',review_id=stage['stage_event_id']+'_'+kind+'_REVIEW',stage_event_id=stage['stage_event_id'],review_round='FOLLOW_UP' if kind=='FOLLOW_UP_CALIBRATION' else 'INTERVIEW',evaluated_at=stamp(at),observation_ids=compact(sorted(o['observation_id'] for o in current)),trigger_codes=compact(triggers),rationale='직접 Observation의 평가자/Rubric 차이와 동일 맥락 충돌 검토. 합의된 LIMITED/NOT_OBSERVED만으로 회의를 만들지 않으며 품질 신호로 쓰지 않는다.')


def finish_final_review(data,latest,evidence,rules,result,trace,round_name):
    observations={o['observation_id']:o for o in data['assessment_observations']}
    relations=defaultdict(list)
    for r in data['skill_decision_observations']:relations[r['decision_id']].append(observations[r['observation_id']])
    decisionable={}
    for skill in rules['skills']:
        if skill['requirement_type']!='MUST':continue
        sid=skill['skill_id'];d=latest.get(sid,{})
        direct=[o for o in relations[d.get('decision_id','')] if evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED']
        decisionable[sid]=d.get('decision_status')=='AGREED' and d.get('final_level') in ('LIMITED','MODERATE','STRONG') and any(o['proposed_level'] in ('LIMITED','MODERATE','STRONG') for o in direct)
    trace['must_not_decisionable']=sorted(s for s,ok in decisionable.items() if not ok)
    trace['decision_basis']='EXISTING_EVIDENCE_REVIEW'
    if round_name=='RE_REVIEW':
        if trace['must_not_decisionable']:
            result='DO_NOT_PROCEED';trace['decision_basis']='INSUFFICIENT_DECISION_BASIS_AFTER_ONE_FOLLOW_UP'
            trace['human_rationale']='한 차례 질문별 후속검증 뒤에도 필수 Skill 자체를 판단할 직접 근거가 미확보/미해결이다. 이번 채용 진행은 종료하되 역량 부족을 확인했다고 추론하지 않는다.'
        elif result=='PROCEED_TO_OFFER':
            trace['human_rationale']='모든 필수 Skill을 판단할 직접 근거와 Skill Decision을 확인하고 기존 제한/상충 기준을 검토했다. 판단 가능한 Skill의 비핵심 맥락 및 Learnable 준비 범위만 업무 지원으로 추적한다.'
        trace['accepted_uncertainty_plan']=[]
        if result=='PROCEED_TO_OFFER':
            for sid,d in latest.items():
                reason=json.loads(d['rationale'])
                if reason.get('limited_evidence_ids') or reason.get('disputed_evidence_ids'):
                    trace['accepted_uncertainty_plan'].append({'skill_id':sid,'scope':'NONCORE_CONTEXT','decision_ref':d['decision_id'],'action':'확인된 수행 범위 밖의 맥락 차이를 업무 배정과 멘토 확인에서 추적'})
            trace['accepted_uncertainty_plan'] += [{'skill_id':sid,'scope':'LEARNABLE','action':'개인별 학습 Gap과 업무 확인으로 추적'} for sid in trace['learnable_gaps']]
    return result,trace
