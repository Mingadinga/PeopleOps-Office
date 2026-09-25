"""Independent v0.3 SSOT assertions; never imports generation/decision code."""
import json
import math
from datetime import timedelta
from collections import defaultdict, Counter
from .common import parse
from .schema import PROVENANCE


def validate_interview(data,rules,idx,check,fk):
    acts=idx['assessment_activities'];stages=idx['stage_history'];ev=idx['assessment_evidence'];obs=idx['assessment_observations']
    cfg=rules['capacity'];model=rules['interview_model']
    check(cfg['initial_person_hours']==60 and cfg['planned_unit_person_hours']==3 and cfg['initial_planned_candidates']==20,'capacity_initial','20 × 3h = immutable Initial 60h')
    check(model['first_minutes']==60 and len(model['first_roles'])==3 and len(set(model['first_roles']))==3,'interview_session','Single 60 minute, three distinct evaluator roles')
    check('additional_panel_person_hours' not in cfg,'capacity_resource','Legacy panel block allocation forbidden')
    check(model['second_minutes']==30 and len(model['second_roles'])==2,'interview_session','Synthetic second interview: two evaluators, 30 minutes')
    plan=next(r for r in data['funnel_plan'] if r['stage']=='FIRST_INTERVIEW')
    check(plan['unit_effort_person_hours']==3 and plan['available_capacity_person_hours']==60,'capacity_initial','Serialized plan mismatch')
    parts=defaultdict(list)
    for p in data['activity_participants']:parts[p['activity_id']].append(p)
    parents={r['activity_id']:r['session_activity_id'] for r in data['activity_sessions']}
    areas={'TECHNICAL_ASSESSMENT','AI_CASE','PRACTITIONER_QA'}
    for rel in data['activity_sessions']:
        a=fk('assessment_activities',rel['activity_id'],'Area');parent=fk('assessment_activities',rel['session_activity_id'],'Session')
        if a and parent:
            check(a['activity_type'] in areas and parent['activity_type']=='FIRST_INTERVIEW_SESSION' and a['stage_event_id']==parent['stage_event_id'],'interview_session','Foreign/invalid parent session')
    for a in acts.values():
        kind=a['activity_type']
        if kind in areas and a['activity_status']=='COMPLETED':
            check(a['activity_id'] in parents and not parts[a['activity_id']],'interview_session','Domain must link parent, with no duplicate participant effort')
            parent=acts.get(parents.get(a['activity_id']),{})
            check(a['started_at']==a['completed_at']==parent.get('completed_at'),'interview_session','Domain timestamp is session evidence completion, not extra interview time')
        if kind in ('FIRST_INTERVIEW_SESSION','VALUES_BEHAVIOR_INTERVIEW') and a['activity_status']=='COMPLETED':
            first=kind=='FIRST_INTERVIEW_SESSION';expected=3 if first else 2;minutes=60 if first else 30
            people=parts[a['activity_id']]
            check((parse(a['completed_at'])-parse(a['started_at'])).total_seconds()==minutes*60,'interview_session','Session duration mismatch')
            check(len(people)==expected and len({p['participant_id'] for p in people})==expected,'interview_session','Wrong interviewer participation count')
            for p in people:check(p['participation_started_at']==a['started_at'] and p['participation_ended_at']==a['completed_at'],'interview_session','Full session participation required')
            if first:
                linked=[acts[r['activity_id']]['activity_type'] for r in data['activity_sessions'] if r['session_activity_id']==a['activity_id'] and r['activity_id'] in acts]
                check(Counter(linked)==Counter(areas),'interview_session','Session must own exactly three evidence domains')
        if kind in ('CALIBRATION','FOLLOW_UP_CALIBRATION') and a['activity_status']=='COMPLETED':
            check((parse(a['completed_at'])-parse(a['started_at'])).total_seconds()==model['calibration_minutes']*60 and len(parts[a['activity_id']])==len(model['calibration_roles']),'calibration_activity','Calibration parameter mismatch')
            current=[o for o in obs.values() if o['application_id']==a['application_id'] and o['created_at']<=a['started_at'] and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' and acts[ev[o['evidence_id']]['activity_id']]['stage_event_id']==a['stage_event_id']]
            check(any(o['proposed_level'] in ('LIMITED','NOT_OBSERVED') for o in current),'calibration_activity','Unnecessary meeting or observations not persisted before calibration')
    for o in obs.values():
        e=ev[o['evidence_id']];parent=parents.get(e['activity_id'],e['activity_id'])
        if parent in acts and acts[parent]['activity_type']=='FIRST_INTERVIEW_SESSION':
            check(o['evaluator_id'] in {p['participant_id'] for p in parts[parent]},'observation_participant','Observation evaluator not in interview pool')
    for e in ev.values():
        parent=parents.get(e['activity_id'])
        if parent:
            own=[o for o in obs.values() if o['evidence_id']==e['evidence_id']]
            if own:check({o['evaluator_id'] for o in own}=={p['participant_id'] for p in parts[parent]},'observation_participant','Missing interviewer observation')
    if rules.get('final_candidate_contract'):
        from .final_candidate_invariants import validate_final_candidate
        validate_final_candidate(data,rules,idx,check,fk)
    # Recompute technical coverage from stored observations, not producer labels.
    for s in stages.values():
        if rules.get('final_candidate_contract') or s['stage']!='FIRST_INTERVIEW' or not s['decision_at']:continue
        current=[o for o in obs.values() if o['created_at']<=s['decision_at'] and ev[o['evidence_id']]['verification_mode']=='DIRECT_TASK' and acts[ev[o['evidence_id']]['activity_id']]['stage_event_id']==s['stage_event_id']]
        decisions={d['skill_id']:d for d in sorted(data['evidence_decisions'],key=lambda d:(d['decided_at'],d['decision_id'])) if d['application_id']==s['application_id'] and d['decided_at']<=s['decision_at']}
        actual={}
        for skill in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03'):
            own=[o for o in current if o['skill_id']==skill];groups=defaultdict(set)
            for o in own:groups[o['evidence_id']].add(o['proposed_level'])
            d=decisions.get(skill,{})
            pos=any(levels and levels<={'MODERATE','STRONG'} for levels in groups.values())
            if pos and d.get('decision_status')=='AGREED' and d.get('final_level') in ('MODERATE','STRONG'):state='A'
            elif d.get('decision_status')=='AGREED' and d.get('final_level')=='LIMITED' and any(o['explicit_limitation']=='true' for o in own):state='B'
            elif d.get('decision_status')=='DISAGREEMENT_REMAINS' or any(len(levels)>1 for levels in groups.values()):state='D'
            else:state='C'
            actual[skill]=state
        trace=json.loads(s['rationale']);recorded=trace.get('coverage',{})
        check({k:v.get('state') for k,v in recorded.items()}==actual,'first_coverage','Coverage label differs from direct observations')
        for skill,item in recorded.items():
            expected={o['observation_id'] for o in current if o['skill_id']==skill}
            check(set(item.get('observation_refs',[]))==expected and item.get('skill_decision_ref')==decisions.get(skill,{}).get('decision_id'),'first_coverage','Coverage lacks canonical snapshot lineage')
        if s['result']=='ADVANCED':check(set(actual.values())=={'A'},'first_coverage','Advanced without each technical core coverage')
        elif s['result']=='FAILED':check('B' in actual.values() and s['decision_reason_code']=='CORE_DIRECT_LIMITATION','first_coverage','Failure from missing/unresolved/capacity')
        else:check('B' not in actual.values() and set(actual.values())!={'A'} and s['decision_reason_code']=='EVIDENCE_PENDING','first_coverage','Incorrect pending coverage')
    # Resource history: fixed pool, additional per-evaluator hour allocations.
    events=sorted(data['interview_capacity_events'],key=lambda r:(r['effective_at'],r['capacity_event_id']))
    initial=[r for r in events if r['event_type']=='INITIAL_PLAN'];check(len(initial)==1 and float(initial[0]['person_hours'])==60,'capacity_initial','Initial plan changed')
    budget=0
    for r in events:
        h=float(r['person_hours']);check(h>=0,'capacity_history','Negative resource event')
        if r['event_type']=='INITIAL_PLAN':budget+=h
        elif r['event_type']=='GAP_IDENTIFIED':
            cohort={s['application_id'] for s in stages.values() if s['stage']=='PRE_ASSESSMENT' and s['result']=='ADVANCED' and s['notified_at'] and s['notified_at']<=r['effective_at']}
            check(set(json.loads(r['cohort_application_ids']))==cohort and float(r['demand_person_hours'])==len(cohort)*3,'capacity_demand','Wrong observed cohort demand')
            check(abs(h-max(len(cohort)*3-budget,0))<1e-6,'capacity_gap','Wrong resource gap')
        else:
            parent=fk('interview_capacity_events',r['source_event_id'],'Resource decision')
            check(r['decided_by']=='HR_OPERATIONS_01' and r['decision_provenance']==PROVENANCE,'capacity_history','Human resource decision missing')
            if parent:
                check(parent['event_type']=='GAP_IDENTIFIED' and parent['effective_at']<=r['effective_at'],'capacity_history','Resource decision before gap')
                n=cfg['initial_panels']*3;unit=cfg['additional_hours_per_evaluator_unit'];each=math.ceil(float(parent['person_hours'])/(n*unit))*unit
                detail=json.loads(r['rationale'])
                check(h==n*each and detail.get('additional_hours_each')==each and detail.get('evaluator_count')==n and detail.get('pool_panels')==cfg['initial_panels'],'capacity_resource','Added hours must follow fixed pool allocation')
            budget+=h if r['event_type']=='CAPACITY_ADDED' else -h
    actual={}
    for a in acts.values():
        if a['activity_type']=='FIRST_INTERVIEW_SESSION':
            for p in parts[a['activity_id']]:
                if p['participation_ended_at']:actual[(a['activity_id'],p['participant_id'])]=(parse(p['participation_ended_at'])-parse(p['participation_started_at'])).total_seconds()/3600
    consumed=defaultdict(float);by_stage=defaultdict(list)
    for r in data['capacity_assignments']:
        h=float(r['person_hours']);s=fk('stage_history',r['stage_event_id'],'Capacity allocation');by_stage[r['stage_event_id']].append(r)
        check(h>0 and s is not None and s['stage']=='FIRST_INTERVIEW','capacity_assignment','Invalid reservation')
        if r['event_type']=='CONSUMED':
            key=(r['activity_id'],r['participant_id']);consumed[key]+=h
            check(key in actual and abs(actual.get(key,0)-h)<1e-6,'capacity_consumption','Consumption must match parent session only')
            check(r['effective_at']==acts.get(r['activity_id'],{}).get('completed_at'),'capacity_consumption','Consumption timestamp mismatch')
    check(dict(consumed)==actual,'capacity_consumption','Missing or duplicate interview effort')
    for sid,rows in by_stage.items():
        reserves=[r for r in rows if r['event_type']=='RESERVED'];balance=0;s=stages[sid]
        check(len(reserves)==1 and float(reserves[0]['person_hours'])==3,'capacity_assignment','One 3h session reservation')
        for r in sorted(rows,key=lambda r:(r['effective_at'],r['assignment_event_id'])):
            balance+=float(r['person_hours'])*(1 if r['event_type']=='RESERVED' else -1)
            check(balance>=-1e-6,'capacity_assignment','Reservation overdrawn')
            if r['event_type']=='RELEASED':
                check(r['reason_code'] in ('CONFIRMED_WITHDRAWAL_UNUSED','NO_RESPONSE_UNUSED','CANCELLED_UNUSED','COMPLETED_UNUSED'),'capacity_assignment','Invalid release reason')
                if r['reason_code']=='CONFIRMED_WITHDRAWAL_UNUSED':check(s['result']=='WITHDRAWN' and s['withdrawn_at']==r['effective_at'],'capacity_assignment','Unconfirmed withdrawal release')
                if r['reason_code']=='NO_RESPONSE_UNUSED':check(s['result']=='IN_PROGRESS' and not s['withdrawn_at'] and 'NO_RESPONSE_PENDING' in s['rationale'],'capacity_assignment','No response inferred as withdrawal')
        if s['decision_at'] or s['withdrawn_at'] or ('NO_RESPONSE_PENDING' in s['rationale'] and s['scheduled_at'] and parse(s['scheduled_at'])+timedelta(days=cfg['no_response_release_days'])<=parse(rules['observation_end'])):check(abs(balance)<1e-6,'capacity_assignment','Unused reservation not returned')
    timeline=[(r['effective_at'],0,r) for r in events if r['event_type']!='GAP_IDENTIFIED']+[(r['effective_at'],1,r) for r in data['capacity_assignments']]
    budget=reserved=used=0
    for _,kind,r in sorted(timeline,key=lambda x:(x[0],x[1],x[2].get('assignment_event_id',''))):
        h=float(r['person_hours']);event=r['event_type']
        if kind==0:budget+=-h if event=='CAPACITY_RELEASED' else h
        elif event=='RESERVED':reserved+=h
        elif event=='RELEASED':reserved-=h
        else:reserved-=h;used+=h
        check(reserved>=-1e-6 and budget-reserved-used>=-1e-6,'capacity_replay','Global available/reserved/consumed replay invalid')
    for st in stages.values():
        if st['stage']=='FIRST_INTERVIEW' and st['scheduled_at']:
            check(st['stage_event_id'] in by_stage,'capacity_assignment','Scheduled interview without reservation')
    check(cfg['initial_panels']*3*cfg['initial_hours_per_evaluator']==60,'capacity_initial','Pool initial allocations do not sum to initial plan')
    # Per-evaluator reservations mirror aggregate interview ledger. Calibration separate.
    ledger=defaultdict(float);balances=defaultdict(float);roles={}
    for p in data['activity_participants']:
        check(p['participant_id'] not in roles or roles[p['participant_id']]==p['participant_role'],'evaluator_pool','Role changed')
        roles[p['participant_id']]=p['participant_role']
    allocated=defaultdict(lambda:cfg['initial_hours_per_evaluator'])
    busy=defaultdict(float);spent=defaultdict(float)
    additions=[e for e in events if e['event_type']=='CAPACITY_ADDED']
    resource_timeline=[(e['effective_at'],0,e) for e in additions]+[(r['effective_at'],1,r) for r in data['evaluator_reservations'] if r['purpose']=='INTERVIEW']
    extra=0
    for _,kind,r in sorted(resource_timeline,key=lambda x:(x[0],x[1],x[2].get('allocation_id',''))):
        if kind==0:extra+=json.loads(r['rationale'])['additional_hours_each'];continue
        actor=r['participant_id'];h=float(r['person_hours'])
        if r['event_type']=='RESERVED':busy[actor]+=h
        elif r['event_type']=='RELEASED':busy[actor]-=h
        else:busy[actor]-=h;spent[actor]+=h
        check(busy[actor]>=-1e-6 and allocated[actor]+extra-busy[actor]-spent[actor]>=-1e-6,'evaluator_reservation','Evaluator hours overdrawn; release must restore available hours')
    for r in sorted(data['evaluator_reservations'],key=lambda r:(r['effective_at'],r['allocation_id'])):
        s=fk('stage_history',r['stage_event_id'],'Evaluator reservation');h=float(r['person_hours']);actor=r['participant_id'];purpose=r['purpose'];kind=r['event_type']
        key=(r['stage_event_id'],actor,purpose,r['activity_id'] if purpose=='CALIBRATION' else '')
        balances[key]+=h if kind=='RESERVED' else -h
        check(h>0 and balances[key]>=-1e-6,'evaluator_reservation','Evaluator reservation overdrawn')
        if purpose=='INTERVIEW':
            allowed={f'FIRST_PANEL_{n:02d}_{role}' for n in range(1,cfg['initial_panels']+1) for role in model['first_roles']}
            check(actor in allowed,'evaluator_pool','Activity-specific or foreign evaluator ID')
            ledger[(r['stage_event_id'],kind,r['effective_at'])]+=h
        if kind=='CONSUMED':
            p=next((p for p in parts[r['activity_id']] if p['participant_id']==actor),None)
            check(p is not None and bool(p['participation_ended_at']),'evaluator_reservation','Consumption lacks real participation')
            if p and p['participation_ended_at']:check(abs(h-(parse(p['participation_ended_at'])-parse(p['participation_started_at'])).total_seconds()/3600)<1e-6,'evaluator_reservation','Evaluator effort mismatch')
    expected=defaultdict(float)
    for r in data['capacity_assignments']:expected[(r['stage_event_id'],r['event_type'],r['effective_at'])]+=float(r['person_hours'])
    check(dict(ledger)==dict(expected),'evaluator_reservation','Aggregate and evaluator ledger differ')
    for a in acts.values():
        if a['activity_type'] in ('CALIBRATION','FOLLOW_UP_CALIBRATION') and a['activity_status']=='COMPLETED':
            for p in parts[a['activity_id']]:
                rows=[r for r in data['evaluator_reservations'] if r['activity_id']==a['activity_id'] and r['participant_id']==p['participant_id'] and r['purpose']=='CALIBRATION']
                check(Counter(r['event_type'] for r in rows)==Counter({'RESERVED':1,'CONSUMED':1}),'calibration_activity','Missing separate calibration effort')
    # Targeted collection proves its actual inputs, not just a mode label.
    follow_evidence={e['evidence_id'] for e in ev.values() if acts[e['activity_id']]['activity_type']=='FOCUSED_FOLLOW_UP'}
    check({r['evidence_id'] for r in data['targeted_followups']}==follow_evidence,'targeted_followup','Every follow-up evidence needs targeted input provenance')
    options={'MISSING_EVIDENCE':{'ARTIFACT_SUPPLIED','ARTIFACT_UNAVAILABLE','CHECK_OMITTED'},'UNRESOLVED_EVIDENCE':{'CHECK_COMPLETED','LIMITATION_CONFIRMED','QUESTION_UNANSWERED'},'EVALUATOR_DISAGREEMENT':{'OWNERSHIP_TRACE_SUPPLIED','SHARED_SCOPE_CONFIRMED','OWNERSHIP_STILL_AMBIGUOUS'}}
    for r in data['targeted_followups']:
        h=fk('final_decisions',r['hold_decision_id'],'Targeted input');e=fk('assessment_evidence',r['evidence_id'],'Targeted output')
        if not h or not e:continue
        plan=next((p for p in json.loads(h['resolution_plan'] or '[]') if p['skill_id']==r['skill_id']),{})
        source_obs={o['observation_id'] for o in obs.values() if o['application_id']==h['application_id'] and o['skill_id']==r['skill_id'] and o['created_at']<=h['decided_at']}
        source_ev={obs[o]['evidence_id'] for o in source_obs}
        check(h['decision']=='HOLD' and h['review_round']=='INITIAL' and e['application_id']==h['application_id'],'targeted_followup','Wrong initial HOLD')
        check(set(json.loads(r['existing_observation_ids']))==source_obs and set(json.loads(r['existing_evidence_ids']))==source_ev,'targeted_followup','Target inputs omit or invent prior evidence/observations')
        anchor=plan.get('anchor_evidence_id','')
        check(not anchor or (anchor in source_ev and anchor in r['question']),'targeted_followup','Question does not identify existing evidence anchor')
        if anchor in ev:check(json.loads(ev[anchor]['raw_evidence'])['context'] in r['question'],'targeted_followup','Question ignores original evidence context')
        check(r['question']==plan.get('question') and r['hold_reason']==plan.get('reason') and r['response_kind'] in options.get(r['hold_reason'],set()),'targeted_followup','Response not tied to unresolved question/reason')
        trace=json.loads(h['rationale']);sid=r['skill_id'];expected_reason='EVALUATOR_DISAGREEMENT' if sid in trace['disagreement_must'] else 'MISSING_EVIDENCE' if sid in trace['missing_must'] else 'UNRESOLVED_EVIDENCE'
        check(r['hold_reason']==expected_reason,'targeted_followup','Question type differs from unresolved snapshot')
        raw=json.loads(e['raw_evidence']);response=r['response_kind']
        check(raw['task']==r['question'] and '['+response+']' in raw['response'],'targeted_followup','Generic lottery output instead of targeted answer')
        if response in ('ARTIFACT_UNAVAILABLE','QUESTION_UNANSWERED'):check(not raw['action'],'targeted_followup','Unavailable evidence invented action')
        elif response in ('CHECK_OMITTED','LIMITATION_CONFIRMED'):check(raw['ownership']=='SELF' and raw['verification']=='추가 검증은 실행하지 않았다.','targeted_followup','Confirmed limitation changed to positive')
        elif response in ('SHARED_SCOPE_CONFIRMED','OWNERSHIP_STILL_AMBIGUOUS'):check(raw['ownership']=='TEAM_UNCLEAR','targeted_followup','Ownership uncertainty hidden')
        else:check(bool(raw['action'] and raw['verification']) and raw['ownership']=='SELF','targeted_followup','Requested positive artifact missing')
