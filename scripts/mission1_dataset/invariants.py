"""Independent SSOT constraints. No imports of generator or decision algorithms.

The allowed matrix is deliberately specified here, not read as an oracle from
producer code. Mutation tests check adversarial persisted datasets.
"""
import json
from collections import defaultdict, Counter
from .common import parse
from .schema import PROVENANCE

# docs/07 §4 + docs/09 §6.1; concrete reviewed scope in Implementation Notes.
MATRIX={
 'DOCUMENT_REVIEW':('APPLICATION_RESPONSE','SELF_REPORTED',{1,4,5,6,8}),
 'CODING_TEST':('CODING_TEST_RESPONSE','DIRECT_TASK',{3}),
 'TECHNICAL_ASSESSMENT':('TECHNICAL_ASSESSMENT_RESPONSE','DIRECT_TASK',{1,2,7}),
 'AI_CASE':('AI_CASE_RESPONSE','DIRECT_TASK',{1,3}),
 'PRACTITIONER_QA':('INTERVIEW_RESPONSE','DIRECT_INTERACTION',{4,5,6,8}),
 'VALUES_BEHAVIOR_INTERVIEW':('INTERVIEW_RESPONSE','BEHAVIORAL_INTERACTION',{4,5}),
}


def evidence_and_decisions(data,rules,idx,check,fk,ordered,scan):
    ev=idx['assessment_evidence'];obs=idx['assessment_observations'];dc=idx['evidence_decisions'];acts=idx['assessment_activities']
    stages=idx['stage_history'];finals=idx['final_decisions']
    links=defaultdict(set)
    for r in data['evidence_skill_links']:
        e=fk('assessment_evidence',r['evidence_id'],'Skill link')
        for col in ('suggested_skill_id','confirmed_skill_id'):
            if r[col]:check(any(s['skill_id']==r[col] for s in data['talent_profile']),'foreign_key','Unknown linked Skill')
        if r['confirmation_status'] in ('CONFIRMED','MODIFIED'):
            check(bool(r['confirmed_by'] and r['confirmed_at'] and r['confirmed_skill_id']),'skill_link','Missing human confirmation')
            check(r['decision_provenance']==PROVENANCE,'provenance','Skill link provenance')
            links[r['evidence_id']].add(r['confirmed_skill_id'])
        if r['confirmation_status']=='PENDING':check(not r['confirmed_skill_id'] and not r['confirmed_at'],'skill_link','Pending relation became canonical')
        if e and r['confirmed_at']:check(r['confirmed_at']>=e['created_at'],'temporal','Link precedes Evidence')
    holds={f['application_id']:f for f in finals.values() if f['review_round']=='INITIAL' and f['decision']=='HOLD'}
    for e in ev.values():
        activity=acts.get(e['activity_id']);kind=activity['activity_type'] if activity else 'DOCUMENT_REVIEW'
        if kind=='FOCUSED_FOLLOW_UP':
            hold=holds.get(e['application_id']);plan=json.loads(hold['resolution_plan']) if hold else []
            allowed={p['skill_id']:p['method'] for p in plan}
            check(bool(hold),'hold_contract','Follow-up without INITIAL HOLD')
            for sid in links[e['evidence_id']]:
                check(sid in allowed and e['verification_mode']==allowed.get(sid),'source_skill_matrix','Follow-up outside resolution plan')
            check(e['verification_mode'] in ('DIRECT_TASK','DIRECT_INTERACTION','BEHAVIORAL_INTERACTION'),'verification_mode','Follow-up must verify directly')
            expected_source='TECHNICAL_ASSESSMENT_RESPONSE' if e['verification_mode']=='DIRECT_TASK' else 'INTERVIEW_RESPONSE'
            check(e['source_type']==expected_source,'verification_mode','Follow-up source/mode mismatch')
        else:
            spec=MATRIX.get(kind)
            if kind=='DOCUMENT_REVIEW' and rules.get('application_model'):spec=('APPLICATION_RESPONSE','SELF_REPORTED',{1,3})
            check(spec is not None,'source_skill_matrix','Evidence from non-evidence activity')
            if spec:
                check((e['source_type'],e['verification_mode'])==spec[:2],'verification_mode',e['evidence_id'])
                check(all(int(s.rsplit('_',1)[1]) in spec[2] for s in links[e['evidence_id']]),'source_skill_matrix',e['evidence_id'])
        # Unreviewed raw evidence may be right-censored before human linking.
        # Every observation/decision, when present, still requires full lineage.
    for o in obs.values():
        e=fk('assessment_evidence',o['evidence_id'],'Observation')
        if e:
            check((o['application_id'],o['candidate_id'])==(e['application_id'],e['candidate_id']),'observation_relation',o['observation_id'])
            check(o['skill_id'] in links[e['evidence_id']],'observation_relation','Observation lacks confirmed link')
            check(o['created_at']>=e['created_at'],'temporal','Observation precedes Evidence')
            raw=json.loads(e['raw_evidence'])
            if o['explicit_limitation']=='true':
                check(raw['ownership']=='SELF' and raw['verification']=='추가 검증은 실행하지 않았다.' and o['proposed_level']=='LIMITED','rubric','Explicit limitation must be affirmative adverse evidence')
            if o['proposed_level']=='STRONG':check(bool(raw['action'] and raw['verification'] and raw['revision']),'rubric','STRONG observation lacks revision evidence')
            if not raw['action']:check(o['proposed_level']=='NOT_OBSERVED','rubric','Absent action cannot prove capability')
        check(o['rubric_id']==rules['rubric']['rubric_id'] and o['decision_provenance']==PROVENANCE,'provenance','Observation rubric/provenance')
    by_decision=defaultdict(list)
    check('evidence_decision_sources' not in data,'canonical_lineage','Raw-decision bypass relation is forbidden in vNext')
    for r in data['skill_decision_observations']:
        d=fk('evidence_decisions',r['decision_id'],'Skill lineage');o=fk('assessment_observations',r['observation_id'],'Skill lineage')
        if d and o:
            check(all(d[k]==o[k] for k in ('application_id','candidate_id','skill_id')),'decision_relation','Foreign observation in Skill decision')
            check(o['created_at']<=d['decided_at'],'temporal','Skill decision uses future observation')
            by_decision[d['decision_id']].append(o)
    for d in dc.values():
        refs=by_decision[d['decision_id']]
        check(bool(refs),'decision_relation','Skill decision has no observation lineage')
        check(d['rubric_id']==rules['rubric']['rubric_id'] and d['decision_provenance']==PROVENANCE,'provenance','Skill decision rubric/provenance')
        check(bool(d['final_level'])==(d['decision_status']=='AGREED'),'calibration','Unresolved Skill must have NULL level')
        direct=[o for o in refs if ev.get(o['evidence_id'],{}).get('verification_mode')!='SELF_REPORTED']
        check(bool(direct),'canonical_lineage','Application-only canonical Skill decision forbidden')
        trace=json.loads(d['rationale']);scan(trace,d['decision_id'])
        support=[obs[o] for o in trace.get('supporting_observation_ids',[]) if o in obs]
        check(all(oid in obs for oid in trace.get('supporting_observation_ids',[])),'canonical_lineage','Missing supporting observation')
        check(all(o in refs for o in support),'canonical_lineage','Support not in canonical relation')
        if d['final_level']=='STRONG':
            check(any(ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' and o['proposed_level']=='STRONG' for o in support),'self_reported_strong','STRONG lacks supporting non-self-reported STRONG observation')
        if d['final_level'] in ('MODERATE','STRONG'):
            check(any(o['proposed_level'] in ('MODERATE','STRONG') for o in direct),'calibration','Positive conclusion lacks direct positive observation')
        context_levels=defaultdict(set)
        for o in direct:context_levels[ev[o['evidence_id']]['context_id']].add(o['proposed_level'])
        if d['decision_status']=='AGREED' and d['final_level'] in ('MODERATE','STRONG'):
            for context,levels in context_levels.items():
                # Same-artifact role ambiguity may be contextualized by another artifact;
                # affirmative conflicting direct records in the same context may not.
                same=[o for o in direct if ev[o['evidence_id']]['context_id']==context]
                limits={o['evidence_id'] for o in same if o['explicit_limitation']=='true'}
                positive={o['evidence_id'] for o in same if o['proposed_level'] in ('MODERATE','STRONG')}
                check(not (limits and positive-limits),'calibration','Unresolved direct same-context conflict hidden by AGREED')
        if d['decision_status']=='DISAGREEMENT_REMAINS':
            same=defaultdict(set)
            for o in direct:same[o['evidence_id']].add(o['proposed_level'])
            check(any(len(v)>1 for v in same.values()) or bool(trace.get('meaningful_conflict_refs')),'calibration','Cross-context level changes alone are not evaluator disagreement')
        screen=next((s for s in stages.values() if s['application_id']==d['application_id'] and s['stage']=='DOCUMENT_SCREEN'),None)
        if screen and screen['decision_at']:check(d['decided_at']>screen['decision_at'],'canonical_lineage','Document screen must not confirm canonical Skill')
    by_app=defaultdict(list)
    for f in finals.values():by_app[f['application_id']].append(f)
    for aid,rows in by_app.items():
        rounds=Counter(f['review_round'] for f in rows)
        check(rounds['INITIAL']==1 and rounds['RE_REVIEW']<=1,'hold_contract','Invalid final review rounds')
        follow=[a for a in acts.values() if a['application_id']==aid and a['activity_type']=='FOCUSED_FOLLOW_UP']
        check(len(follow)<=1,'hold_contract','Multiple focused follow-ups')
    for f in finals.values():
        trace=json.loads(f['rationale']);scan(trace,f['final_decision_id'])
        refs=trace.get('decision_refs',[])
        check(bool(refs),'final_decision','Final review lacks Skill snapshot refs')
        for did in refs:
            d=fk('evidence_decisions',did,'Final review snapshot')
            if d:check(d['application_id']==f['application_id'] and d['candidate_id']==f['candidate_id'] and d['decided_at']<=f['decided_at'],'final_decision','Final uses foreign/future snapshot')
        snapshot=[dc[did] for did in refs if did in dc]
        skill_refs={d['skill_id']:d for d in snapshot}
        check(len(skill_refs)==len(snapshot),'final_decision','Duplicate Skill snapshots in final review')
        for sid in trace.get('repeated_must_limitations',[]):
            source_obs=by_decision.get(skill_refs.get(sid,{}).get('decision_id'),[])
            limitations={o['evidence_id'] for o in source_obs if o['explicit_limitation']=='true' and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED'}
            check(len(limitations)>=2,'final_decision','Claimed repeated limitation lacks independent direct observations')
        for sid in trace.get('adverse_must',[]):
            source_obs=by_decision.get(skill_refs.get(sid,{}).get('decision_id'),[])
            check(any(o['explicit_limitation']=='true' and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' for o in source_obs),'final_decision','Claimed adverse evidence is missing-only')
        for sid in trace.get('disagreement_must',[]):
            check(skill_refs.get(sid,{}).get('decision_status')=='DISAGREEMENT_REMAINS','final_decision','Claimed disagreement lacks Skill review')
        expected_status='REPEATED_LIMITATION' if trace.get('repeated_must_limitations') else 'UNRESOLVED' if trace['unresolved_must'] else 'COVERED'
        check(f['must_evidence_status']==expected_status,'final_decision','Must status disagrees with snapshot')
        if f['must_evidence_status']=='COVERED':
            for skill in data['talent_profile']:
                if skill['requirement_type']=='MUST':
                    d=skill_refs.get(skill['skill_id'],{})
                    check(d.get('decision_status')=='AGREED' and d.get('final_level') in ('MODERATE','STRONG'),'final_decision','Covered Must lacks supported Skill judgment')
        check(f['decision_provenance']==PROVENANCE and bool(f['decided_by']),'provenance','Final human judgment required')
        stage=next((s for s in stages.values() if s['application_id']==f['application_id'] and s['stage']=='FINAL_REVIEW'),None)
        check(stage is not None,'final_decision','Final decision outside FINAL_REVIEW')
        if stage:check(stage['entered_at']<=f['decided_at'],'temporal','Final decision before final stage')
        check(json.loads(f['remaining_uncertainty'])==trace['unresolved_must'] and json.loads(f['learnable_gap_summary'])==trace['learnable_gaps'],'final_decision','Uncertainty/learnable snapshot mismatch')
        if f['decision']=='HOLD':
            check(f['review_round']=='INITIAL','hold_contract','RE_REVIEW cannot issue HOLD')
            check(f['hold_reason_code'] in ('MISSING_EVIDENCE','UNRESOLVED_EVIDENCE','EVALUATOR_DISAGREEMENT') and bool(f['resolution_plan']),'hold_contract','HOLD needs reason and resolution plan')
            plan=json.loads(f['resolution_plan'] or '[]')
            check(bool(plan) and all(all(p.get(k) for k in ('question','skill_id','context','method')) for p in plan),'hold_contract','Incomplete resolution question/skill/context/method')
            check({p['skill_id'] for p in plan}==set(trace['unresolved_must']),'hold_contract','Plan must target unresolved questions only')
        else:check(not f['hold_reason_code'] and not f['resolution_plan'],'hold_contract','Non-HOLD carries HOLD attributes')
        if f['decision']=='DO_NOT_PROCEED':
            check(bool(trace.get('repeated_must_limitations') or trace.get('adverse_must') or trace.get('disagreement_must') or (rules.get('final_candidate_contract') and f['review_round']=='RE_REVIEW' and trace.get('must_not_decisionable'))),'final_decision','Missing evidence alone cannot cause rejection')
        if f['decision']=='PROCEED_TO_OFFER' and trace['unresolved_must']:
            check(f['review_round']=='RE_REVIEW' and bool(trace.get('accepted_uncertainty_plan')),'final_decision','Proceed with uncertainty needs re-review human support plan')
        if f['review_round']=='RE_REVIEW':
            hold=holds.get(f['application_id']);a=acts.get(f['follow_up_activity_id'])
            check(bool(hold and a),'hold_contract','Re-review lacks INITIAL HOLD/follow-up')
            if hold and a:
                check(a['activity_type']=='FOCUSED_FOLLOW_UP' and a['application_id']==f['application_id'] and hold['follow_up_activity_id']==a['activity_id'],'hold_contract','Follow-up identity mismatch')
                check(bool(a['completed_at']) and hold['decided_at']<a['started_at']<=a['completed_at']<=f['decided_at'],'hold_contract','Re-review before completed follow-up')
                for p in json.loads(hold['resolution_plan']):
                    new=[o for o in obs.values() if o['skill_id']==p['skill_id'] and ev[o['evidence_id']]['activity_id']==a['activity_id']]
                    check(bool(new),'hold_contract','Resolution Skill lacks new observation')
                    calibrated=[o for did in refs for o in by_decision[did]]
                    check(any(o in calibrated for o in new),'hold_contract','Re-review bypasses follow-up calibration')
        if f['follow_up_activity_id']:fk('assessment_activities',f['follow_up_activity_id'],'Final follow-up')
    for a in acts.values():
        if a['activity_type']=='FOCUSED_FOLLOW_UP':
            check(a['application_id'] in holds,'hold_contract','Orphan focused follow-up')
            if a['application_id'] in holds and a['started_at']:check(a['started_at']>holds[a['application_id']]['decided_at'],'hold_contract','Follow-up before HOLD')
    for s in stages.values():
        if s['stage']=='FINAL_REVIEW':
            check(s['result'] in ('','IN_PROGRESS','WITHDRAWN'),'stage_decision','Final outcome duplicated in stage result')
            if not s['result']:
                own=by_app[s['application_id']]
                check(bool(own) and max(own,key=lambda f:f['decided_at'])['decision']!='HOLD','final_decision','Completed final stage still HOLD')
            continue
        if not s['decision_at']:continue
        trace=json.loads(s['rationale']);scan(trace,s['stage_event_id'])
        check(not any(x in s['rationale'] for x in ('PROCEED_TO_OFFER','DO_NOT_PROCEED','"HOLD"')),'stage_decision','Offer-level conclusion outside FINAL_REVIEW')
        refs=trace.get('observation_refs',[])
        current=[]
        for oid in refs:
            o=fk('assessment_observations',oid,'Stage observation')
            if o:
                check(o['application_id']==s['application_id'] and o['created_at']<=s['decision_at'],'stage_decision','Stage observation identity/time')
                current.append(o)
        if s['result']=='FAILED':
            if s['stage']=='DOCUMENT_SCREEN':
                check(bool(trace.get('public_requirement_ref') and trace.get('explicit_violation_ref')) and s['decision_reason_code']=='BASIC_REQUIREMENT_VIOLATION','stage_decision','Document failure without verified public eligibility violation')
            else:
                adverse=[o for o in current if o['explicit_limitation']=='true' and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED']
                check(bool(adverse),'stage_decision','Stage failure lacks explicit direct adverse evidence')
                if s['stage']=='PRE_ASSESSMENT':check(any(o['skill_id']=='M1_SKILL_03' for o in adverse),'stage_decision','Pre-assessment failure unrelated to coding')
                if s['stage']=='FIRST_INTERVIEW' and 'interview_model' not in rules:
                    historical=[o for o in obs.values() if o['application_id']==s['application_id'] and o['created_at']<=s['decision_at'] and o['explicit_limitation']=='true' and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED']
                    check(any(len({o['evidence_id'] for o in historical if o['skill_id']==sid})>=2 for sid in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03')),'stage_decision','First-stage failure lacks repeated direct Must limitation')
                if s['stage']=='SECOND_INTERVIEW':check({'M1_SKILL_04','M1_SKILL_05'}<={o['skill_id'] for o in adverse},'stage_decision','Behavior failure criteria missing')
        check(s['decision_reason_code'] not in ('CAPACITY_WAIT','NO_RESPONSE','INSUFFICIENT_EVIDENCE','NOT_OBSERVED'),'stage_decision','Operational/missing state used as rejection')


def capacity_history(data,rules,idx,check,fk):
    if 'interview_model' in rules:
        from .interview_invariants import validate_interview
        validate_interview(data,rules,idx,check,fk)
        return
    events=sorted(data['interview_capacity_events'],key=lambda r:(r['effective_at'],r['capacity_event_id']))
    initial=[r for r in events if r['event_type']=='INITIAL_PLAN']
    check(len(initial)==1 and float(initial[0]['person_hours'])==80,'capacity_initial','Immutable cycle initial plan must be exactly 80h')
    check(rules['capacity']['planned_unit_person_hours']==4,'capacity_initial','Planned effort must remain 4h, not quota')
    budget=0
    for r in events:
        hours=float(r['person_hours']);check(hours>=0,'capacity_history','Negative capacity')
        cohort=json.loads(r['cohort_application_ids']);demand=float(r['demand_person_hours'])
        check(len(cohort)==len(set(cohort)),'capacity_history','Duplicate demand application')
        if r['event_type']=='INITIAL_PLAN':budget+=hours
        elif r['event_type']=='GAP_IDENTIFIED':
            expected={s['application_id'] for s in data['stage_history'] if s['stage']=='PRE_ASSESSMENT' and s['result']=='ADVANCED' and s['notified_at'] and s['notified_at']<=r['effective_at']}
            check(set(cohort)==expected and demand==len(cohort)*4,'capacity_demand','Demand must trace to all eligible PRE cohort, not 20-person quota')
            check(abs(hours-max(demand-budget,0))<1e-6,'capacity_gap','Whole-cycle Gap is demand minus revised total budget')
        elif r['event_type'] in ('CAPACITY_ADDED','CAPACITY_RELEASED'):
            check(bool(r['decided_by']) and r['decision_provenance']==PROVENANCE and bool(r['rationale']),'capacity_history','Resource change lacks human decision')
            parent=fk('interview_capacity_events',r['source_event_id'],'Capacity decision')
            if parent:check(parent['event_type']=='GAP_IDENTIFIED' and parent['effective_at']<=r['effective_at'],'capacity_history','Capacity decision lacks prior Gap')
            budget+=hours if r['event_type']=='CAPACITY_ADDED' else -hours
        check(budget>=0,'capacity_history','Negative total budget')
    stageidx=idx['stage_history'];actual={};roles={}
    for p in data['activity_participants']:
        actor=p['participant_id']
        check(actor not in roles or roles[actor]==p['participant_role'],'evaluator_pool','Participant role changed')
        roles[actor]=p['participant_role']
        a=idx['assessment_activities'].get(p['activity_id'])
        if a and stageidx[a['stage_event_id']]['stage']=='FIRST_INTERVIEW' and p['participation_ended_at']:
            key=(a['activity_id'],actor)
            hours=(parse(p['participation_ended_at'])-parse(p['participation_started_at'])).total_seconds()/3600
            actual[key]=actual.get(key,0)+hours
    allocations=defaultdict(list);consumption=defaultdict(float)
    for r in data['capacity_assignments']:
        stage=fk('stage_history',r['stage_event_id'],'Reservation');hours=float(r['person_hours'])
        check(hours>0,'capacity_assignment','Nonpositive assignment hours')
        if stage:
            check(stage['stage']=='FIRST_INTERVIEW' and r['effective_at']>=stage['entered_at'],'capacity_assignment','Assignment stage/time mismatch')
            check(r['reservation_id']=='RSV_'+stage['stage_event_id'],'capacity_assignment','Reservation identity mismatch')
        allocations[r['reservation_id']].append(r)
        if r['event_type']=='CONSUMED':
            key=(r['activity_id'],r['participant_id']);consumption[key]+=hours
            check(key in actual and abs(actual.get(key,0)-hours)<1e-6,'capacity_consumption','Consumption must equal real participant interval, not planned 4h')
            participant=next((p for p in data['activity_participants'] if (p['activity_id'],p['participant_id'])==key),None)
            if participant:check(r['effective_at']==participant['participation_ended_at'],'capacity_consumption','Consumption time differs from actual interval')
        else:check(not r['activity_id'] and not r['participant_id'],'capacity_assignment','Reservation/release should not duplicate actual participant')
        if r['event_type']=='RELEASED':
            check(r['reason_code'] in ('CONFIRMED_WITHDRAWAL_UNUSED','NO_RESPONSE_UNUSED','COMPLETED_UNUSED','CANCELLED_UNUSED'),'capacity_assignment','Unknown unused release reason')
            if stage and r['reason_code']=='CONFIRMED_WITHDRAWAL_UNUSED':check(stage['result']=='WITHDRAWN' and stage['withdrawn_at']==r['effective_at'],'capacity_assignment','Release lacks confirmed withdrawal')
            if stage and r['reason_code']=='CANCELLED_UNUSED':check('CANCELLED' in stage['rationale'],'capacity_assignment','Cancellation release lacks confirmed cancellation')
            if stage and r['reason_code']=='NO_RESPONSE_UNUSED':check(stage['result']=='IN_PROGRESS' and not stage['withdrawn_at'],'capacity_assignment','No-response inferred as withdrawal')
    check(set(actual)==set(consumption) and all(abs(consumption[k]-v)<1e-6 for k,v in actual.items()),'capacity_consumption','Missing or duplicate actual consumption')
    for rid,rows in allocations.items():
        reserved=[r for r in rows if r['event_type']=='RESERVED'];balance=0
        check(len(reserved)==1 and float(reserved[0]['person_hours'])==4,'capacity_assignment','One 4h planned reservation per assignment')
        for r in sorted(rows,key=lambda r:(r['effective_at'],r['assignment_event_id'])):
            balance+=float(r['person_hours'])*(1 if r['event_type']=='RESERVED' else -1)
            check(balance>=-1e-6,'capacity_assignment','Released/consumed more than reserved')
        stage=stageidx.get(rows[0]['stage_event_id'])
        if stage and (stage['result']=='WITHDRAWN' or stage['decision_at']):check(abs(balance)<1e-6,'capacity_assignment','Finished/withdrawn stage retains unused reservation')
        if stage and 'NO_RESPONSE_PENDING' in stage['rationale'] and stage['scheduled_at']:
            due=parse(stage['scheduled_at'])+__import__('datetime').timedelta(days=rules['capacity']['no_response_release_days'])
            if due<=parse(rules['observation_end']):check(abs(balance)<1e-6,'capacity_assignment','No-response unused reservation not released')
    # Global replay: reservation release returns availability; it does not reduce budget.
    timeline=[(r['effective_at'],0,r) for r in events if r['event_type']!='GAP_IDENTIFIED']+[(r['effective_at'],1,r) for r in data['capacity_assignments']]
    budget=reserved=consumed=0
    for at,kind,r in sorted(timeline,key=lambda v:(v[0],v[1],v[2].get('assignment_event_id',''))):
        h=float(r['person_hours']);event=r['event_type']
        if kind==0:budget+= -h if event=='CAPACITY_RELEASED' else h
        elif event=='RESERVED':reserved+=h
        elif event=='RELEASED':reserved-=h
        else:reserved-=h;consumed+=h
        check(reserved>=-1e-5 and budget-reserved-consumed>=-1e-5,'capacity_replay','Budget/reservation/consumption replay went negative')
    for stage in stageidx.values():
        if stage['stage']=='FIRST_INTERVIEW' and stage['scheduled_at']:
            check('RSV_'+stage['stage_event_id'] in allocations,'capacity_assignment','Scheduled interview lacks reservation')
    # Pool IDs must be reused, not minted per activity.
    counts=Counter(p['participant_id'] for p in data['activity_participants'])
    check(not any('_PART_' in p for p in counts),'evaluator_pool','Per-activity evaluator ID forbidden')


def workforce_and_offers(data,rules,idx,check,fk,ordered,scan):
    end=parse(rules['observation_end']);events=defaultdict(list);finals=defaultdict(list)
    for f in data['final_decisions']:finals[f['application_id']].append(f)
    for e in data['offer_events']:
        offer=fk('offers',e['offer_id'],'Offer event');events[e['offer_id']].append(e)
        if offer:check(e['occurred_at']>=offer['offered_at'],'temporal','Offer event before offer')
    offers_by_candidate={}
    for o in data['offers']:
        offers_by_candidate[o['candidate_id']]=o
        rows=sorted(events[o['offer_id']],key=lambda e:(e['occurred_at'],e['offer_event_id']));kinds=[e['event_type'] for e in rows]
        check(kinds in (['OFFERED'],['OFFERED','ACCEPTED'],['OFFERED','DECLINED'],['OFFERED','EXPIRED'],['OFFERED','ACCEPTED','PRE_JOIN_WITHDRAWAL']),'offer_lifecycle','Invalid offer lifecycle')
        check(bool(rows) and rows[0]['occurred_at']==o['offered_at'],'offer_lifecycle','OFFERED canonical time mismatch')
        check(o['offered_at']<o['response_deadline'],'offer_deadline','Deadline must follow offer')
        own=finals[o['application_id']];final=max(own,key=lambda f:f['decided_at']) if own else None
        check(final is not None and final['decision']=='PROCEED_TO_OFFER' and final['decided_at']<=o['offered_at'],'offer_lifecycle','Offer before final proceed')
        responses=[e for e in rows if e['event_type'] in ('ACCEPTED','DECLINED')]
        expired=[e for e in rows if e['event_type']=='EXPIRED']
        for e in responses:check(e['occurred_at']<=o['response_deadline'],'offer_deadline','Response after expired offer needs new offer')
        if expired:
            check(not responses and parse(o['response_deadline'])<=end and expired[0]['occurred_at']>=o['response_deadline'],'offer_deadline','EXPIRED without deadline/event absence')
            check(expired[0]['reason_code']=='UNKNOWN','offer_motive','Absence is not a motive')
        if parse(o['response_deadline'])<=end and not responses:check(len(expired)==1,'offer_deadline','Missing derived expiry after deadline')
        for e in rows:
            if e['event_type'] in ('DECLINED','PRE_JOIN_WITHDRAWAL'):check(e['reason_code']=='UNKNOWN','offer_motive','Unverified motive/NO_RESPONSE cannot imply decline/withdrawal')
    check(len(offers_by_candidate)==len(data['offers']),'offer_lifecycle','Duplicate offer for candidate')
    workforce=defaultdict(list)
    for e in data['workforce_events']:
        fk('onboarding_profiles',e['employee_id'],'Workforce');workforce[e['employee_id']].append(e)
    profiles=idx['onboarding_profiles'];tasks=idx['onboarding_tasks'];gaps=defaultdict(list)
    for g in data['onboarding_skill_gaps']:
        p=fk('onboarding_profiles',g['employee_id'],'Gap');f=fk('final_decisions',g['final_decision_id'],'Gap final snapshot')
        gaps[g['employee_id']].append(g)
        check(g['decision_provenance']==PROVENANCE and bool(g['confirmed_by'] and g['confirmed_at']),'provenance','Gap human confirmation required')
        if p and f:check(f['candidate_id']==p['source_candidate_id'] and f['decision']=='PROCEED_TO_OFFER','workforce_relation','Gap Final Review identity mismatch')
        if g['source_evidence_id']:
            e=fk('assessment_evidence',g['source_evidence_id'],'Gap evidence')
            if e and p:
                check(e['candidate_id']==p['source_candidate_id'],'workforce_relation','Gap foreign evidence')
                check(any(l['evidence_id']==e['evidence_id'] and l['confirmed_skill_id']==g['skill_id'] for l in data['evidence_skill_links']),'onboarding_gap','Gap source Evidence concerns another Skill')
        if f:
            if g['requirement_ref']=='FINAL_LEARNABLE_GAP':check(g['skill_id'] in json.loads(f['learnable_gap_summary']),'onboarding_gap','Gap not in final learnable summary')
            elif g['requirement_ref']=='ACCEPTED_UNCERTAINTY':check(g['skill_id'] in json.loads(f['remaining_uncertainty']),'onboarding_gap','Gap not in accepted uncertainty')
            else:check(any(r['requirement_id']==g['requirement_ref'] and r['skill_id']==g['skill_id'] for r in rules['onboarding']['work_prep_requirements']),'onboarding_gap','Unknown work-prep requirement')
    for t in tasks.values():
        p=fk('onboarding_profiles',t['employee_id'],'Task')
        if p:
            check(t['candidate_id']==p['source_candidate_id'],'workforce_relation','Task foreign candidate')
            check(t['planned_at']>=p['joined_at'],'temporal','Onboarding task before Join')
        ordered(t,'planned_at','assigned_at','Task');ordered(t,'assigned_at','completed_at','Task')
        if t['related_skill_id']:check(any(s['skill_id']==t['related_skill_id'] for s in data['talent_profile']),'foreign_key','Task Skill missing')
        if t['status']=='COMPLETED':check(bool(t['completed_at'] and t['work_evidence'] and t['evidence_ref']),'work_evidence','Completed task lacks work artifact')
        else:check(not t['completed_at'] and t['mentor_confirmed']=='false','work_evidence','Incomplete task was confirmed')
        if t['work_evidence']:
            artifact=json.loads(t['work_evidence']);scan(artifact,t['task_id'])
            check(t['evidence_ref']==f"onboarding_tasks.csv#{t['task_id']}/work_evidence",'source_reference','Invalid work ref')
            check(artifact.get('evidence_type')=='SYNTHETIC' and bool(artifact.get('performed_action')) and artifact.get('observed_at')==t['completed_at'],'work_evidence','Work observation missing time/action')
            if t['mentor_confirmed']=='true':
                check(artifact.get('verification')=='OUTPUT_AND_RECOVERY_CHECKED' and t['decision_provenance']==PROVENANCE,'work_evidence','Mentor confirmation lacks verified work')
            if p:check(p['joined_at']<t['completed_at'],'work_evidence','Work evidence must be post-join')
    check(len({p['source_candidate_id'] for p in profiles.values()})==len(profiles),'workforce_relation','Duplicate employee for candidate')
    for employee,p in profiles.items():
        rows=workforce[employee];joins=[e for e in rows if e['event_type']=='JOINED'];starts=[e for e in rows if e['event_type']=='ONBOARDING_STARTED'];ready=[e for e in rows if e['event_type']=='READY_CONFIRMED']
        check(len(joins)==1 and len(starts)==1 and len(ready)<=1,'workforce_lifecycle','Join/onboarding/Ready multiplicity')
        offer=offers_by_candidate.get(p['source_candidate_id'])
        check(bool(offer),'workforce_lifecycle','Joined without offer')
        if offer:
            responses=events[offer['offer_id']];accepted=[e for e in responses if e['event_type']=='ACCEPTED']
            check(len(accepted)==1 and accepted[0]['occurred_at']<=p['joined_at'] and not any(e['event_type']=='PRE_JOIN_WITHDRAWAL' for e in responses),'workforce_lifecycle','Joined without active acceptance')
            if joins:check(joins[0]['source_ref']=='offers.csv#'+offer['offer_id'],'source_reference','Join Offer ref mismatch')
        if joins and starts:
            check(p['joined_at']==joins[0]['effective_at'] and p['onboarding_started_at']==starts[0]['effective_at'],'canonical_owner','Profile timestamps differ from Workforce owner')
            check(starts[0]['effective_at']>=joins[0]['effective_at'],'temporal','Onboarding before Join')
        # Recompute expected per-person requirements from the frozen final snapshot.
        own=finals.get(offer['application_id'],[]) if offer else []
        f=max(own,key=lambda r:r['decided_at']) if own else None
        if f:
            trace=json.loads(f['rationale']);snap={idx['evidence_decisions'][d]['skill_id']:idx['evidence_decisions'][d] for d in trace['decision_refs'] if d in idx['evidence_decisions']}
            required=set(json.loads(f['learnable_gap_summary'])+json.loads(f['remaining_uncertainty']))
            required.update(r['skill_id'] for r in rules['onboarding']['work_prep_requirements'] if r['skill_id'] not in snap or snap[r['skill_id']]['final_level']!='STRONG')
            check({g['skill_id'] for g in gaps[employee]}==required,'onboarding_gap','Individual gaps differ from Final Review/work requirements')
        own_tasks=[t for t in tasks.values() if t['employee_id']==employee]
        for e in rows:
            check(e['effective_at']>=p['joined_at'],'temporal','Workforce event before Join')
            if e['event_type'] in ('READY_CONFIRMED','RAMP_UP_EXTENDED'):
                check(bool(e['confirmed_by'] and e['confirmed_at']) and e['decision_provenance']==PROVENANCE,'ready_confirmation','Human Ready/extension confirmation missing')
                check(e['confirmed_at']<=e['effective_at'],'temporal','Effective Ready precedes confirmation')
            if e['event_type']=='READY_CONFIRMED':
                trace=json.loads(e['source_ref']);refs=trace.get('work_evidence_refs',[])
                check(bool(refs) and bool(trace.get('human_rationale')),'work_evidence','Ready lacks human work review')
                check(set(trace.get('gap_ids',[]))=={g['gap_id'] for g in gaps[employee]},'work_evidence','Ready omits individual Gap review')
                for ref in refs:
                    tid=ref.partition('#')[2].split('/')[0];t=tasks.get(tid)
                    check(t is not None and t in own_tasks and t['evidence_ref']==ref and t['mentor_confirmed']=='true' and bool(t['work_evidence']),'work_evidence','Ready lacks own confirmed work evidence')
                    if t:check(p['joined_at']<t['completed_at']<=e['confirmed_at'],'work_evidence','Ready evidence not post-join/prior to confirmation')
                check(bool(own_tasks),'work_evidence','Ready without work tasks')
                for t in own_tasks:
                    confirmed=t['mentor_confirmed']=='true' and t['completed_at']<=e['confirmed_at'] and t['evidence_ref'] in refs
                    replacement=any(x['task_type']=='FOLLOW_UP_WORK' and x['related_skill_id']==t['related_skill_id'] and x['mentor_confirmed']=='true' and x['completed_at']<=e['confirmed_at'] and x['evidence_ref'] in refs for x in own_tasks)
                    check(confirmed or replacement,'work_evidence','Required task/Gap lacks confirmed work or follow-up')
            if e['event_type']=='RAMP_UP_EXTENDED':
                tid=e['source_ref'].partition('#')[2].split('/')[0];t=tasks.get(tid)
                check(t is not None and t in own_tasks and bool(t['completed_at']) and t['completed_at']<=e['confirmed_at'],'work_evidence','Extension lacks observed work review')
