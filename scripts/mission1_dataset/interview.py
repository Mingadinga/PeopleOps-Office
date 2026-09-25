"""v0.3 synthetic session, coverage and question-specific collection policy.

Generation only. Independent validators do not import this module.
"""
import json
from collections import defaultdict
from .common import compact, parse, stamp, rng
from .evidence import latest_decisions

CORE=('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03')
AREAS=('TECHNICAL_ASSESSMENT','AI_CASE','PRACTITIONER_QA')


def first_session(gen,app,stage,begin,panel):
    cfg=gen.rules['interview_model']
    end=gen.activity(app,stage,'FIRST_INTERVIEW_SESSION',begin,cfg['first_minutes'],cfg['first_roles'],panel)
    session=gen.data['assessment_activities'][-1]
    for kind in AREAS:
        # Evaluation domains have no independently measured labor duration.
        # Their timestamp is the observation source completion point.
        row=gen.add('assessment_activities',activity_id=stage['stage_event_id']+'_'+kind,stage_event_id=stage['stage_event_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],activity_type=kind,started_at=stamp(end) if end<=gen.end else '',completed_at=stamp(end) if end<=gen.end else '',activity_status='COMPLETED' if end<=gen.end else 'PLANNED')
        gen.add('activity_sessions',activity_id=row['activity_id'],session_activity_id=session['activity_id'])
        if end<=gen.end:
            spec=gen.rules['source_matrix'][kind]
            gen.evidence.collect(app,row,[f'M1_SKILL_{i:02d}' for i in spec['skills']],end)
    return end


def observe_and_calibrate(gen,app,stage,at,panel,kind):
    # Persist before scheduling the meeting. Skill decisions are written later.
    gen.evidence.review(app,at,canonical=False)
    ev={e['evidence_id']:e for e in gen.data['assessment_evidence']}
    acts={a['activity_id']:a for a in gen.data['assessment_activities']}
    obs=[o for o in gen.data['assessment_observations'] if o['application_id']==app['application_id'] and o['created_at']==stamp(at) and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' and acts[ev[o['evidence_id']]['activity_id']]['stage_event_id']==stage['stage_event_id']]
    groups=defaultdict(set)
    for o in obs:groups[o['evidence_id']].add(o['proposed_level'])
    needs=any(len(levels)>1 or bool(levels & {'LIMITED','NOT_OBSERVED'}) for levels in groups.values())
    audit=None
    if gen.rules.get('final_candidate_contract'):
        from .final_candidate import record_calibration_review
        audit=record_calibration_review(gen,app,stage,at,kind,obs)
        needs=bool(json.loads(audit['trigger_codes']))
    if needs:
        cfg=gen.rules['interview_model']
        end=gen.activity(app,stage,kind,at,cfg['calibration_minutes'],cfg['calibration_roles'],panel)
        if audit:audit['activity_id']=stage['stage_event_id']+'_'+kind
        return end
    return at


def allocation(gen,stage,activity,actor,purpose,kind,hours,at,reason):
    if at>gen.end or hours<=0:return
    gen.add('evaluator_reservations',allocation_id=f"EA_{len(gen.data['evaluator_reservations']):06d}",stage_event_id=stage['stage_event_id'],activity_id=activity,participant_id=actor,purpose=purpose,event_type=kind,person_hours=round(hours,8),effective_at=stamp(at),reason_code=reason)


def interview_ledger(gen,stage,kind,hours,at,reason,activity,actor):
    if actor:
        allocation(gen,stage,activity,actor,'INTERVIEW',kind,hours,at,reason)
    else:
        panel=gen.capacity.stage_panels[stage['stage_event_id']]
        roles=gen.rules['interview_model']['first_roles']
        for role in roles:allocation(gen,stage,'',f'FIRST_PANEL_{panel:02d}_{role}','INTERVIEW',kind,hours/len(roles),at,reason)


def calibration_ledger(gen,stage,activity,actors,begin,end):
    hours=(end-begin).total_seconds()/3600
    for actor,role in actors:
        allocation(gen,stage,activity['activity_id'],actor,'CALIBRATION','RESERVED',hours,begin,'CALIBRATION_REQUIRED')
        allocation(gen,stage,activity['activity_id'],actor,'CALIBRATION','CONSUMED',hours,end,'ACTUAL_PARTICIPATION')


def first_transition(data,app,stage,when,final_candidate=False):
    acts={a['activity_id'] for a in data['assessment_activities'] if a['stage_event_id']==stage['stage_event_id'] and a['activity_type'] in AREAS}
    ev={e['evidence_id']:e for e in data['assessment_evidence']}
    current=[o for o in data['assessment_observations'] if ev[o['evidence_id']]['activity_id'] in acts and o['created_at']<=when]
    latest=latest_decisions(data,app['application_id'],when)
    coverage={}
    for sid in CORE:
        own=[o for o in current if o['skill_id']==sid and ev[o['evidence_id']]['verification_mode']=='DIRECT_TASK']
        groups=defaultdict(list)
        for o in own:groups[o['evidence_id']].append(o)
        direct_positive=any({o['proposed_level'] for o in rows}<={'MODERATE','STRONG'} for rows in groups.values())
        d=latest.get(sid,{})
        if direct_positive and d.get('decision_status')=='AGREED' and d.get('final_level') in ('MODERATE','STRONG'):state='A'
        elif d.get('decision_status')=='AGREED' and d.get('final_level')=='LIMITED' and any(o['explicit_limitation']=='true' for o in own):state='B'
        elif d.get('decision_status')=='DISAGREEMENT_REMAINS' or any(len({o['proposed_level'] for o in rows})>1 for rows in groups.values()):state='D'
        else:state='C'
        coverage[sid]={'state':state,'observation_refs':[o['observation_id'] for o in own],'skill_decision_ref':d.get('decision_id','')}
        if final_candidate:
            agreed_direct=any(len({o['proposed_level'] for o in rows})==1 and rows[0]['proposed_level'] in ('LIMITED','MODERATE','STRONG') for rows in groups.values())
            decisionable=agreed_direct and d.get('decision_status')=='AGREED' and d.get('final_level') in ('LIMITED','MODERATE','STRONG')
            coverage[sid]['decisionable']=decisionable
            if decisionable and state not in ('A','B'):coverage[sid]['state']='A'
    states={v['state'] for v in coverage.values()}
    result='ADVANCED' if states=={'A'} else 'FAILED' if 'B' in states else 'IN_PROGRESS'
    if final_candidate:
        result='FAILED' if 'B' in states else 'ADVANCED' if all(v['decisionable'] for v in coverage.values()) else 'IN_PROGRESS'
    reason={'ADVANCED':'FIRST_EVIDENCE_REVIEWED','FAILED':'CORE_DIRECT_LIMITATION','IN_PROGRESS':'EVIDENCE_PENDING'}[result]
    trace={'criterion':'CORE_DIRECT_COVERAGE','coverage':coverage,'observation_refs':[o['observation_id'] for o in current],'human_rationale':'기술 핵심01/02/03의 직접 지지·명시적 제한·부족·미해결을 각각 검토. 점수/정원 없음.'}
    if result=='IN_PROGRESS':trace['operational_state']='EVIDENCE_PENDING'
    return result,reason,trace


def resolution_plan(gen,hold):
    trace=json.loads(hold['rationale']);plans=[]
    for sid in trace['unresolved_must']:
        reason='EVALUATOR_DISAGREEMENT' if sid in trace['disagreement_must'] else 'MISSING_EVIDENCE' if sid in trace['missing_must'] else 'UNRESOLVED_EVIDENCE'
        question={'MISSING_EVIDENCE':'누락된 개인 수행 산출물과 검증 기록을 제시할 수 있는가?', 'UNRESOLVED_EVIDENCE':'앞선 검증 미실행의 범위를 재확인하고 요청한 검증을 수행했는가?', 'EVALUATOR_DISAGREEMENT':'공동 산출물 중 본인이 수행하고 검증한 범위를 기록으로 분리할 수 있는가?'}[reason]
        obs=[o for o in gen.data['assessment_observations'] if o['application_id']==hold['application_id'] and o['skill_id']==sid and o['created_at']<=hold['decided_at']]
        evidence={e['evidence_id']:e for e in gen.data['assessment_evidence']}
        direct=[o for o in obs if evidence[o['evidence_id']]['verification_mode']!='SELF_REPORTED']
        anchors=[o for o in direct if o['proposed_level'] in ('LIMITED','NOT_OBSERVED')] or direct
        anchor=max(anchors,key=lambda o:(o['created_at'],o['observation_id'])) if anchors else None
        anchor_id=anchor['evidence_id'] if anchor else ''
        context=json.loads(evidence[anchor_id]['raw_evidence'])['context'] if anchor else '아직 직접 검증되지 않은 '+sid
        question=question+' 대상: '+anchor_id+' / '+(anchor['observation_text'] if anchor else '직접 관찰 없음')+' / '+context
        plans.append({'skill_id':sid,'reason':reason,'question':question,'context':context,'anchor_evidence_id':anchor_id,'method':'DIRECT_TASK' if sid in CORE else 'BEHAVIORAL_INTERACTION','existing_observation_ids':sorted(o['observation_id'] for o in obs),'existing_evidence_ids':sorted({o['evidence_id'] for o in obs})})
    return plans


def collect_targeted(gen,app,activity,at):
    hold=next(f for f in gen.data['final_decisions'] if f['application_id']==app['application_id'] and f['decision']=='HOLD')
    for p in json.loads(hold['resolution_plan']):
        sid=p['skill_id'];skill=next(s for s in gen.rules['skills'] if s['skill_id']==sid)
        # Input snapshot, including the question and actual prior references, drives
        # this dedicated collection stream. No ordinary observable() call.
        response=rng(gen.rules,'targeted_followup',app['candidate_id'],compact(p)).choice(gen.rules['targeted_followup']['response_options'][p['reason']])
        previous=next((json.loads(e['raw_evidence']) for e in gen.data['assessment_evidence'] if e['evidence_id']==p['anchor_evidence_id']),{})
        requested_action=previous.get('action') or skill['example_action']
        raw={'task':p['question'],'context':p['context'],'action':'','verification':'','revision':'','ownership':'UNSPECIFIED','response':''}
        if response in ('ARTIFACT_SUPPLIED','CHECK_COMPLETED','OWNERSHIP_TRACE_SUPPLIED'):
            raw.update(action='요청한 범위의 직접 확인: '+requested_action,verification=skill['example_check'],ownership='SELF')
        elif response in ('CHECK_OMITTED','LIMITATION_CONFIRMED'):
            raw.update(action='후속 질문에서 확인한 수행: '+requested_action,verification='추가 검증은 실행하지 않았다.',ownership='SELF')
        elif response in ('SHARED_SCOPE_CONFIRMED','OWNERSHIP_STILL_AMBIGUOUS'):
            raw.update(action='공동 산출물의 작업 설명: '+requested_action,verification=skill['example_check'],ownership='TEAM_UNCLEAR')
        raw['response']=p['question']+' '+raw['action']+' '+raw['verification']+' ['+response+']'
        eid='EV_'+activity['activity_id']+'_'+sid
        gen.add('assessment_evidence',evidence_id=eid,activity_id=activity['activity_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],source_type='TECHNICAL_ASSESSMENT_RESPONSE' if p['method']=='DIRECT_TASK' else 'INTERVIEW_RESPONSE',verification_mode=p['method'],context_id='FOCUSED_FOLLOW_UP_'+sid,source_ref=f'assessment_evidence.csv#{eid}/raw_evidence',raw_evidence=compact(raw),created_at=stamp(at))
        gen.add('targeted_followups',evidence_id=eid,hold_decision_id=hold['final_decision_id'],skill_id=sid,hold_reason=p['reason'],question=p['question'],existing_evidence_ids=compact(p['existing_evidence_ids']),existing_observation_ids=compact(p['existing_observation_ids']),response_kind=response)
