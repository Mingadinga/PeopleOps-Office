"""v0.4 persisted-data invariants, independent of all generation policies."""
import json
from collections import defaultdict
from .common import parse


def validate_final_candidate(data,rules,idx,check,fk):
    obs=idx['assessment_observations'];ev=idx['assessment_evidence'];acts=idx['assessment_activities'];stages=idx['stage_history'];decisions=idx['evidence_decisions']
    linked=defaultdict(set);relations=defaultdict(list)
    for r in data['evidence_skill_links']:
        if r['confirmation_status'] in ('CONFIRMED','MODIFIED'):linked[r['evidence_id']].add(r['confirmed_skill_id'])
    for r in data['skill_decision_observations']:
        if r['observation_id'] in obs:relations[r['decision_id']].append(obs[r['observation_id']])
    for stage in stages.values():
        if stage['stage']!='FIRST_INTERVIEW' or not stage['decision_at']:continue
        latest={d['skill_id']:d for d in sorted(decisions.values(),key=lambda d:(d['decided_at'],d['decision_id'])) if d['application_id']==stage['application_id'] and d['decided_at']<=stage['decision_at']}
        trace=json.loads(stage['rationale']);coverage=trace.get('coverage',{});flags={};adverse=[]
        for sid in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03'):
            own=[o for o in obs.values() if o['application_id']==stage['application_id'] and o['skill_id']==sid and o['created_at']<=stage['decision_at'] and ev[o['evidence_id']]['verification_mode']=='DIRECT_TASK' and sid in linked[o['evidence_id']] and acts[ev[o['evidence_id']]['activity_id']]['stage_event_id']==stage['stage_event_id']]
            groups=defaultdict(set)
            for o in own:groups[o['evidence_id']].add(o['proposed_level'])
            direct=any(len(levels)==1 and levels<={'LIMITED','MODERATE','STRONG'} for levels in groups.values())
            d=latest.get(sid,{})
            flags[sid]=direct and d.get('decision_status')=='AGREED' and d.get('final_level') in ('LIMITED','MODERATE','STRONG')
            if d.get('decision_status')=='AGREED' and d.get('final_level')=='LIMITED' and any(o['explicit_limitation']=='true' for o in own):adverse.append(sid)
            item=coverage.get(sid,{})
            check(item.get('decisionable')==flags[sid] and item.get('skill_decision_ref')==d.get('decision_id') and set(item.get('observation_refs',[]))=={o['observation_id'] for o in own},'decisionable_coverage','Coverage differs from direct Skill-linked observation/snapshot')
        check(set(coverage)==set(flags),'decisionable_coverage','Missing/extra core Skill')
        if stage['result']=='ADVANCED':check(all(flags.values()) and not adverse,'decisionable_coverage','FIRST advancement requires coverage and independent limitation review')
        elif stage['result']=='FAILED':check(bool(adverse) and stage['decision_reason_code']=='CORE_DIRECT_LIMITATION','decisionable_coverage','Missing evidence/capacity is not failure')
        else:check(not all(flags.values()) and not adverse and stage['decision_reason_code']=='EVIDENCE_PENDING','decisionable_coverage','Wrong evidence pending status')
    # A SECOND entry (not only an advanced SECOND) requires a valid FIRST snapshot.
    for stage in stages.values():
        if stage['stage']=='SECOND_INTERVIEW':
            first=next((s for s in stages.values() if s['application_id']==stage['application_id'] and s['stage']=='FIRST_INTERVIEW'),None)
            check(first is not None and first['result']=='ADVANCED','decisionable_coverage','SECOND without eligible FIRST')
    audits=defaultdict(list)
    meeting_ids=set()
    for review in data['calibration_reviews']:
        stage=fk('stage_history',review['stage_event_id'],'Calibration review')
        if not stage:continue
        audits[(review['stage_event_id'],review['review_round'])].append(review)
        at=review['evaluated_at'];ids=json.loads(review['observation_ids'])
        expected={o['observation_id'] for o in obs.values() if o['application_id']==stage['application_id'] and o['created_at']==at and ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' and acts[ev[o['evidence_id']]['activity_id']]['stage_event_id']==stage['stage_event_id']}
        check(set(ids)==expected and len(ids)==len(set(ids)) and bool(ids),'calibration_trigger','Review must contain all new direct observations')
        current=[obs[o] for o in ids if o in obs];groups=defaultdict(set)
        for o in current:groups[o['evidence_id']].add(o['proposed_level'])
        expected_triggers=set()
        if any(len(levels)>1 for levels in groups.values()):expected_triggers.add('EVALUATOR_DISAGREEMENT')
        contexts=defaultdict(list)
        for o in obs.values():
            e=ev[o['evidence_id']]
            if o['application_id']==stage['application_id'] and o['created_at']<=at and e['verification_mode']!='SELF_REPORTED':contexts[(o['skill_id'],e['context_id'])].append(o)
        for rows in contexts.values():
            bad={o['evidence_id'] for o in rows if o['explicit_limitation']=='true'};good={o['evidence_id'] for o in rows if o['proposed_level'] in ('MODERATE','STRONG')}
            if bad and good-bad and (bad|good)&set(groups):expected_triggers.add('DIRECT_CONTEXT_CONFLICT')
        check(set(json.loads(review['trigger_codes']))==expected_triggers,'calibration_trigger','Trigger not supported by actual observations')
        check(bool(review['activity_id'])==bool(expected_triggers),'calibration_trigger','Missing required meeting or meeting without trigger')
        if review['activity_id']:
            a=fk('assessment_activities',review['activity_id'],'Calibration meeting');meeting_ids.add(review['activity_id'])
            if a:
                expected_kind='FOLLOW_UP_CALIBRATION' if review['review_round']=='FOLLOW_UP' else 'CALIBRATION'
                check(a['stage_event_id']==stage['stage_event_id'] and a['activity_type']==expected_kind and (not a['started_at'] or a['started_at']>=at),'calibration_trigger','Wrong stage/round/time for meeting')
                after=[d for d in decisions.values() if d['application_id']==stage['application_id'] and any(o['observation_id'] in expected for o in relations[d['decision_id']])]
                if after:check(bool(a['completed_at']) and all(d['decided_at']>=a['completed_at'] for d in after),'calibration_trigger','Skill Decision bypassed necessary meeting')
    for a in acts.values():
        if a['activity_type'] in ('CALIBRATION','FOLLOW_UP_CALIBRATION'):
            check(a['activity_id'] in meeting_ids,'calibration_trigger','Orphan meeting without explicit review trigger')
        if a['activity_type'] in ('FIRST_INTERVIEW_SESSION','VALUES_BEHAVIOR_INTERVIEW','FOCUSED_FOLLOW_UP') and a['completed_at']:
            round_name='FOLLOW_UP' if a['activity_type']=='FOCUSED_FOLLOW_UP' else 'INTERVIEW'
            own=audits[(a['stage_event_id'],round_name)]
            check(len(own)==1 and own[0]['evaluated_at']==a['completed_at'],'calibration_trigger','Completed collection must have one trigger assessment, even when skipped')
    for key,rows in audits.items():check(len(rows)==1,'calibration_trigger','Duplicate review opportunity')
    must={s['skill_id'] for s in data['talent_profile'] if s['requirement_type']=='MUST'}
    learnable={s['skill_id'] for s in data['talent_profile'] if s['requirement_type']=='LEARNABLE'}
    for f in data['final_decisions']:
        trace=json.loads(f['rationale']);snapshot={decisions[d]['skill_id']:decisions[d] for d in trace.get('decision_refs',[]) if d in decisions};not_decisionable=[]
        for sid in must:
            d=snapshot.get(sid,{})
            direct=[o for o in relations[d.get('decision_id','')] if ev[o['evidence_id']]['verification_mode']!='SELF_REPORTED' and sid in linked[o['evidence_id']]]
            if not (d.get('decision_status')=='AGREED' and d.get('final_level') in ('LIMITED','MODERATE','STRONG') and any(o['proposed_level'] in ('LIMITED','MODERATE','STRONG') for o in direct)):not_decisionable.append(sid)
        check(set(trace.get('must_not_decisionable',[]))==set(not_decisionable),'rereview_decisionable','Must decisionability must match actual snapshot')
        if f['review_round']=='RE_REVIEW':
            check(f['decision']!='HOLD','hold_contract','Re-review cannot HOLD')
            if f['decision']=='PROCEED_TO_OFFER':check(not not_decisionable,'rereview_decisionable','Offer cannot accept nondecisionable MUST')
            if not_decisionable:check(f['decision']=='DO_NOT_PROCEED' and trace.get('decision_basis')=='INSUFFICIENT_DECISION_BASIS_AFTER_ONE_FOLLOW_UP' and bool(trace.get('human_rationale')),'rereview_decisionable','Unresolved MUST must terminate with truthful decision-basis rationale')
            for accepted in trace.get('accepted_uncertainty_plan',[]):
                sid=accepted['skill_id']
                check(sid not in not_decisionable and bool(accepted.get('action')),'accepted_uncertainty','Accepted uncertainty hides unjudgeable MUST')
                if accepted.get('scope')=='LEARNABLE':check(sid in learnable,'accepted_uncertainty','MUST relabeled Learnable')
                else:check(accepted.get('scope')=='NONCORE_CONTEXT' and accepted.get('decision_ref')==snapshot.get(sid,{}).get('decision_id'),'accepted_uncertainty','Unscoped uncertainty or missing decision link')
