"""Observable artifacts -> persisted human observations -> calibration snapshots.

These are offline synthetic human scenarios, not a production hiring engine.
Only observation creation interprets raw artifacts. Later judgments consume rows.
"""
import json
from collections import defaultdict
from .common import compact, rng, stamp
from .schema import PROVENANCE


def observable(rules, candidate, activity, skill, context=None):
    pattern = rng(rules, 'observable', candidate, activity, skill['skill_id']).choice(rules['evidence']['patterns'])
    source = {'task': skill['skill_name'], 'action': '', 'verification': '', 'revision': '', 'ownership': 'UNSPECIFIED'}
    source['context'] = context or '명시된 작업 맥락'
    if pattern == 'NOT_DOCUMENTED':
        source['response'] = '해당 작업을 확인할 답변/산출물이 기록되지 않았다.'
    elif pattern == 'AMBIGUOUS':
        source.update(action=skill['example_action'], verification=skill['example_check'], ownership='TEAM_UNCLEAR', response='팀 산출물을 설명했지만 개인이 확인한 범위는 구분하지 않았다.')
    else:
        source.update(action=skill['example_action'], ownership='SELF', response='해당 맥락에서 수행한 작업과 확인 범위를 기록했다.')
        source['verification'] = '추가 검증은 실행하지 않았다.' if pattern == 'PARTIAL' else skill['example_check']
        if pattern == 'REVISED':
            source['revision'] = '검증에서 발견한 예외를 수정하고 같은 조건에서 다시 확인했다.'
    return source


def interpret(source, role):
    if not source['action']:
        return 'NOT_OBSERVED', '원문에 해당 행동을 확인할 내용이 없다. 능력 부재를 뜻하지 않는다.'
    if source['ownership'] == 'TEAM_UNCLEAR':
        if role == 'ML_ENGINEER':
            return 'LIMITED', '팀 산출물에서 개인의 검증 범위를 분리할 수 없다.'
        return 'MODERATE', '맥락과 검증 설명은 구체적이나 개인 수행 범위는 추가 확인이 필요하다.'
    if source['verification'] == '추가 검증은 실행하지 않았다.':
        return 'LIMITED', '행동은 확인했지만 원문에 검증 미실행이 명시됐다.'
    if source['revision']:
        return 'STRONG', '행동·검증·수정과 재확인의 구체적 근거가 있다.'
    return 'MODERATE', '구체적인 행동과 검증을 확인했다.'


def calibrate(observations, evidence):
    """No raw parsing. All levels/limitations are persisted observation facts.

Same-artifact interpretation disagreement is distinct from cross-context variation.
A corroborated direct observation can resolve limited scope in another context;
we retain both and state that rationale rather than silently choosing the newest.
"""
    groups = defaultdict(list)
    for row in observations:
        groups[row['evidence_id']].append(row)
    positive, limited, disputed, missing = [], [], [], []
    for eid, rows in groups.items():
        if evidence[eid]['verification_mode'] == 'SELF_REPORTED':
            continue
        levels = {o['proposed_level'] for o in rows}
        if len(levels) > 1:
            disputed.append(eid)
        elif levels <= {'NOT_OBSERVED'}:
            missing.append(eid)
        elif levels <= {'MODERATE', 'STRONG'}:
            positive.append(eid)
        else:
            limited.append(eid)
    context_positive={evidence[e]['context_id'] for e in positive}
    conflicting=[e for e in limited if evidence[e]['context_id'] in context_positive]
    differences = []
    if positive and (limited or missing or any(evidence[e]['verification_mode']=='SELF_REPORTED' for e in groups)):
        differences.append('EVIDENCE_EVOLUTION')
    if positive and limited:
        differences.append('CONTEXT_DIFFERENCE')
    if disputed or conflicting:
        differences.append('EVALUATOR_DISAGREEMENT')
    support = [o['observation_id'] for eid in positive for o in groups[eid]]
    trace = {'difference_types':differences,'supporting_observation_ids':support,
             'disputed_evidence_ids':disputed,'limited_evidence_ids':limited,
             'missing_evidence_ids':missing,'meaningful_conflict_refs':conflicting,'rubric_review':'직접 관찰의 행동·검증을 검토하며 다른 맥락의 한계와 평가자 차이를 보존한다.'}
    if conflicting:
        trace['reason']='동일 직접검증 맥락에서 확인된 상충 관찰이 남아 별도 검토가 필요하다.'
        return '', 'DISAGREEMENT_REMAINS', trace
    if positive:
        level = 'STRONG' if any(o['proposed_level']=='STRONG' for eid in positive for o in groups[eid]) else 'MODERATE'
        trace['reason']='동일 Skill의 독립된 직접 관찰로 수행 범위를 확인했다. 다른 맥락의 제한/모호성은 해당 근거의 한계로 보존한다.'
        return level, 'AGREED', trace
    if disputed:
        trace['reason']='동일 근거에 대한 평가자 해석 차이를 해소할 직접 관찰이 부족하다.'
        return '', 'DISAGREEMENT_REMAINS', trace
    if limited:
        trace['supporting_observation_ids']=[o['observation_id'] for eid in limited for o in groups[eid]]
        trace['reason']='관찰된 직접 근거의 범위가 제한적이다. 자기기술만으로 보완하지 않는다.'
        return 'LIMITED', 'AGREED', trace
    trace['reason']='직접 판단 근거 부족. 미관찰을 역량 부재로 해석하지 않는다.'
    return '', 'INSUFFICIENT_EVIDENCE', trace


def latest_decisions(data, application_id, as_of):
    rows = sorted((d for d in data['evidence_decisions'] if d['application_id']==application_id and d['decided_at']<=as_of), key=lambda d:(d['decided_at'],d['decision_id']))
    return {d['skill_id']:d for d in rows}


def decision_observations(data, decisions):
    ids={d['decision_id'] for d in decisions}
    refs={r['observation_id'] for r in data['skill_decision_observations'] if r['decision_id'] in ids}
    return [o for o in data['assessment_observations'] if o['observation_id'] in refs]


def final_review(data, application_id, rules, as_of, review_round='INITIAL'):
    latest=latest_decisions(data,application_id,as_of)
    evidence={e['evidence_id']:e for e in data['assessment_evidence']}
    missing=[];unresolved=[];disagreements=[];repeated=[];adverse=[]
    for skill in rules['skills']:
        if skill['requirement_type']!='MUST':continue
        sid=skill['skill_id'];d=latest.get(sid)
        if d and d['decision_status']=='AGREED' and d['final_level'] in ('MODERATE','STRONG'):continue
        obs=decision_observations(data,[d]) if d else []
        explicit={o['evidence_id'] for o in obs if o['explicit_limitation']=='true' and evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED'}
        if len(explicit)>=2:repeated.append(sid)
        if explicit:adverse.append(sid)
        if not d or d['decision_status']=='INSUFFICIENT_EVIDENCE':missing.append(sid)
        elif d['decision_status']=='DISAGREEMENT_REMAINS':disagreements.append(sid)
        else:unresolved.append(sid)
    learnable=[s['skill_id'] for s in rules['skills'] if s['requirement_type']=='LEARNABLE' and (s['skill_id'] not in latest or latest[s['skill_id']]['final_level'] not in ('MODERATE','STRONG'))]
    uncertainty=sorted(set(missing+unresolved+disagreements))
    trace={'talent_profile':'talent_profile.json','rubric_id':rules['rubric']['rubric_id'],
           'decision_refs':[d['decision_id'] for d in latest.values()], 'repeated_must_limitations':repeated,
           'unresolved_must':uncertainty,'missing_must':missing,'disagreement_must':disagreements,
           'adverse_must':adverse,'learnable_gaps':learnable,'review_round':review_round}
    if review_round=='INITIAL':
        result='DO_NOT_PROCEED' if repeated else 'HOLD' if uncertainty else 'PROCEED_TO_OFFER'
        trace['human_rationale']='필수 근거·반복된 명시적 제한·남은 확인 질문을 검토한 합성 패널 판단.'
    else:
        result='DO_NOT_PROCEED' if repeated or adverse or disagreements else 'PROCEED_TO_OFFER'
        trace['human_rationale']=('추가 검증 후에도 남은 명시적 필수 검증 제한/해석 충돌을 검토하여 이번 역할 진행을 보류하지 않고 종료한다.' if result=='DO_NOT_PROCEED' else '추가 직접 관찰과 기존 근거를 검토했다. 남은 미관찰 자체는 탈락 사유가 아니며 업무 준비 지원으로 추적한다.')
        trace['accepted_uncertainty_plan']=[{'skill_id':s,'action':'입사 후 해당 업무 범위를 멘토와 확인'} for s in uncertainty] if result=='PROCEED_TO_OFFER' else []
    if rules.get('final_candidate_contract'):
        from .final_candidate import finish_final_review
        result,trace=finish_final_review(data,latest,evidence,rules,result,trace,review_round)
    return result,trace


def stage_transition_decision(data, app, stage, when):
    name=stage['stage'];aid=app['application_id'];sid=stage['stage_event_id']
    activities={a['activity_id'] for a in data['assessment_activities'] if a['stage_event_id']==sid}
    evidence={e['evidence_id']:e for e in data['assessment_evidence'] if e['application_id']==aid}
    current=[o for o in data['assessment_observations'] if o['evidence_id'] in evidence and evidence[o['evidence_id']]['activity_id'] in activities and o['created_at']<=when]
    trace={'stage':name,'observation_refs':[o['observation_id'] for o in current], 'criterion':'','human_rationale':''}
    if name=='DOCUMENT_SCREEN':
        trace.update(criterion='NO_VERIFIED_PUBLIC_REQUIREMENT_VIOLATION',evidence_candidate_refs=sorted({o['evidence_id'] for o in current}),follow_up_skills=sorted({o['skill_id'] for o in current}),human_rationale='공개 기본요건의 검증된 위반 없음. 자기기술을 후속검증 질문으로 전달하며 Skill을 확정하지 않는다.')
        return 'ADVANCED','EVIDENCE_CANDIDATES_FOUND',trace
    direct=[o for o in current if evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED']
    explicit={o['skill_id'] for o in direct if o['explicit_limitation']=='true'}
    latest=latest_decisions(data,aid,when)
    positives={s for s,d in latest.items() if d['decision_status']=='AGREED' and d['final_level'] in ('MODERATE','STRONG')}
    if name=='PRE_ASSESSMENT':
        failed='M1_SKILL_03' in explicit
        trace['criterion']='CODING_VERIFICATION_OMISSION';reason='DIRECT_TASK_LIMITATION' if failed else 'PRE_TASK_COMPLETE'
    elif name=='FIRST_INTERVIEW':
        refs=decision_observations(data,latest.values())
        repeated={s for s in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03') if len({o['evidence_id'] for o in refs if o['skill_id']==s and o['explicit_limitation']=='true' and evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED'})>=2}
        failed=bool(repeated-positives);trace['criterion']='REPEATED_DIRECT_TECHNICAL_LIMITATION';reason='REPEATED_MUST_LIMITATION' if failed else 'FIRST_EVIDENCE_REVIEWED'
    elif name=='SECOND_INTERVIEW':
        failed={'M1_SKILL_04','M1_SKILL_05'} <= (explicit-positives)
        trace['criterion']='BOTH_BEHAVIORAL_LIMITATIONS';reason='BEHAVIOR_LIMITATION' if failed else 'BEHAVIOR_REVIEWED'
    else:raise ValueError('Final review is not a stage transition decision')
    trace['human_rationale']='해당 단계 직접 근거의 명시적 비진행 기준을 검토했다.' if failed else '단계 활동과 관찰을 검토하여 다음 판단으로 진행한다. 미관찰은 부족/탈락과 동일하지 않다.'
    return ('FAILED' if failed else 'ADVANCED'),reason,trace


class EvidenceWriter:
    def __init__(self,data,rules,add):
        self.data,self.rules,self.add=data,rules,add

    def collect(self,app,activity,skill_ids,when,source_type=None,mode=None,context=None):
        kind=activity['activity_type'];matrix=self.rules['source_matrix'].get(kind)
        for sid in skill_ids:
            skill=dict(next(s for s in self.rules['skills'] if s['skill_id']==sid))
            if matrix:
                if int(sid.rsplit('_',1)[1]) not in matrix['skills']:raise ValueError('Source-skill matrix violation')
                source_type=matrix['source_type'];mode=matrix['verification_mode'];ctx=matrix['context']
            else:ctx=context or 'HOLD 질문에 한정된 후속 확인'
            # The artifact text describes what this particular source actually exposes.
            prefix={'SELF_REPORTED':'지원 답변에서 주장: ','DIRECT_TASK':'제출된 과제/실행기록에서 확인: ','DIRECT_INTERACTION':'현장 설명과 후속 질의에서 확인: ','BEHAVIORAL_INTERACTION':'과거 행동과 피드백의 후속 확인: '}[mode]
            skill['example_action']=prefix+ctx+' — '+skill['example_action']
            skill['example_check']=ctx+' — '+skill['example_check']
            source=observable(self.rules,app['candidate_id'],activity['activity_id'],skill,ctx)
            eid=f"EV_{activity['activity_id']}_{sid}"
            self.add('assessment_evidence',evidence_id=eid,activity_id=activity['activity_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],source_type=source_type,verification_mode=mode,context_id=kind+'_'+sid,source_ref=f'assessment_evidence.csv#{eid}/raw_evidence',raw_evidence=compact(source),created_at=stamp(when))

    def review(self,app,when,canonical=True):
        old={r['evidence_id'] for r in self.data['assessment_observations']}
        candidates=[e for e in self.data['assessment_evidence'] if e['application_id']==app['application_id'] and e['created_at']<=stamp(when)]
        for e in candidates:
            if e['evidence_id'] in old:continue
            sid='M1_SKILL_'+e['evidence_id'].rsplit('_M1_SKILL_',1)[1]
            self.add('evidence_skill_links',link_id='LK_'+e['evidence_id'],evidence_id=e['evidence_id'],suggestion_source='HUMAN',confirmed_skill_id=sid,confirmation_status='CONFIRMED',confirmed_by='REVIEW_ML_01',confirmed_at=stamp(when),decision_provenance=PROVENANCE)
            raw=json.loads(e['raw_evidence'])
            actors=[('REVIEW_ML_01','ML_ENGINEER'),('REVIEW_HM_01','HIRING_MANAGER')]
            if 'interview_model' in self.rules:
                parent=next((x['session_activity_id'] for x in self.data['activity_sessions'] if x['activity_id']==e['activity_id']),e['activity_id'])
                people=[p for p in self.data['activity_participants'] if p['activity_id']==parent]
                if people:actors=[(p['participant_id'],p['participant_role']) for p in people]
            for actor,role in actors:
                level,reason=interpret(raw,role)
                self.add('assessment_observations',observation_id='OB_'+actor+'_'+e['evidence_id'],evidence_id=e['evidence_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],evaluator_id=actor,evaluator_role=role,skill_id=sid,rubric_id=self.rules['rubric']['rubric_id'],observation_text=reason,proposed_level=level,explicit_limitation=str(raw['ownership']=='SELF' and raw['verification']=='추가 검증은 실행하지 않았다.').lower(),created_at=stamp(when),decision_provenance=PROVENANCE)
        if not canonical:return
        groups=defaultdict(list);evidence={e['evidence_id']:e for e in candidates}
        for o in self.data['assessment_observations']:
            if o['application_id']==app['application_id'] and o['created_at']<=stamp(when):groups[o['skill_id']].append(o)
        for sid,obs in sorted(groups.items()):
            if not any(evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED' for o in obs):continue
            level,status,reason=calibrate(obs,evidence)
            did=f"DC_{app['application_id']}_{sid}_{len(self.data['evidence_decisions']):06d}"
            self.add('evidence_decisions',decision_id=did,application_id=app['application_id'],candidate_id=app['candidate_id'],skill_id=sid,final_level=level,decision_status=status,rationale=compact(reason),decided_by='CALIBRATION_PANEL_01',decided_at=stamp(when),decision_provenance=PROVENANCE,rubric_id=self.rules['rubric']['rubric_id'])
            for o in obs:self.add('skill_decision_observations',decision_id=did,observation_id=o['observation_id'])
