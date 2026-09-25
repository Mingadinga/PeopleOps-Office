"""Descriptive quality/sanity checks only. No causal or Mission 2 interpretation."""
import json
from collections import Counter, defaultdict
from datetime import datetime, time, timedelta
from statistics import median
from math import floor, ceil
from zoneinfo import ZoneInfo
from .common import parse
from .application_report import summarize_application
from .resolution_report import summarize_resolution
from .schema import OPTIONAL_TABLES, SCHEMA, STAGES, RESULTS, PLAN_FILES


def distribution(values):
    ordered=sorted(values)
    if not ordered:return {'n':0,'min':None,'median':None,'p90':None,'max':None}
    position=(len(ordered)-1)*.9
    percentile=ordered[floor(position)]+(ordered[ceil(position)]-ordered[floor(position)])*(position-floor(position))
    return {'n':len(ordered),'min':round(ordered[0],4),'median':round(median(ordered),4),
            'p90':round(percentile,4),'max':round(ordered[-1],4)}


def summarize(data, rules, validation):
    stage_rows=defaultdict(list)
    for r in data['stage_history']:stage_rows[r['stage']].append(r)
    counts={k+'.csv':len(data[k]) for k in SCHEMA if k not in OPTIONAL_TABLES or data.get(k)}
    counts.update({n+'.json':len(data[n]) if isinstance(data[n],list) else 1 for n in PLAN_FILES})
    workforce=data['workforce_events'];offer_events=data['offer_events']
    profiles={r['employee_id']:r for r in data['onboarding_profiles']}
    unique=lambda rows,key='candidate_id':len({r[key] for r in rows})
    actual={
        'APPLICATION_STARTED':unique(data['applications']),
        'APPLICATION_SUBMITTED':unique([r for r in data['applications'] if r['application_status']=='SUBMITTED']),
        'DOCUMENT_SCREEN':unique([r for r in stage_rows['DOCUMENT_SCREEN'] if r['result'] in ('ADVANCED','CONDITIONAL_ADVANCE')]),
        'PRE_ASSESSMENT':unique([r for r in stage_rows['PRE_ASSESSMENT'] if r['result']=='ADVANCED']),
        'FIRST_INTERVIEW':unique(stage_rows['FIRST_INTERVIEW']),
        'SECOND_INTERVIEW':unique(stage_rows['SECOND_INTERVIEW']),
        'OFFER':unique(data['offers']),
        'JOIN':len({profiles[r['employee_id']]['source_candidate_id'] for r in workforce if r['event_type']=='JOINED'}),
    }
    funnel=[{'stage':p['stage'],'label':('서류 근거 충족(조건부 포함)' if rules.get('eligibility_resolution') and p['stage']=='DOCUMENT_SCREEN' else p['label']),'target':p['target_count'],'actual':actual[p['stage']],'difference':actual[p['stage']]-p['target_count']} for p in data['funnel_plan']]
    outcomes={}
    for stage in STAGES:
        rows=stage_rows[stage];entered=unique(rows)
        out={'ENTERED':entered,'COMPLETED':unique([r for r in rows if r['completed_at']])}
        out.update({result:unique([r for r in rows if r['result']==result]) for result in RESULTS})
        out['FINAL_REVIEW_COMPLETED']=unique([r for r in rows if r['result']==''])
        out['rates']={k:out[k]/entered if entered and stage!='FINAL_REVIEW' else None for k in ('ADVANCED','FAILED','WITHDRAWN')}
        outcomes[stage]=out
    formulas={'stage_lead_time':('entered_at','notified_at'),'scheduling_wait':('invited_at','scheduled_at'),
              'decision_time':('completed_at','decision_at'),'notification_delay':('decision_at','notified_at')}
    timings={}
    for name,(a,b) in formulas.items():
        timings[name]={}
        for stage in STAGES:
            rows=stage_rows[stage]
            # Scheduling Wait uses the known appointment even when it is in the future.
            # It describes the reserved interval, not completed waiting/exposure.
            values=[(parse(r[b])-parse(r[a])).total_seconds()/86400 for r in rows if r[a] and r[b]]
            d=distribution(values);d['unit']='days';d['null_count']=len(rows)-len(values)
            timings[name][stage]=d
    activity={a['activity_id']:a for a in data['assessment_activities']}
    effort=defaultdict(float);incomplete=0
    for r in data['activity_participants']:
        if not r['participation_ended_at']:
            incomplete+=1;continue
        duration=(parse(r['participation_ended_at'])-parse(r['participation_started_at'])).total_seconds()/3600
        effort[activity[r['activity_id']]['activity_type']]+=duration
    interview_effort=sum(effort[k] for k in ('TECHNICAL_ASSESSMENT','AI_CASE','PRACTITIONER_QA','CALIBRATION'))
    first_calibration=sum((parse(p['participation_ended_at'])-parse(p['participation_started_at'])).total_seconds()/3600 for p in data['activity_participants'] if p['participation_ended_at'] and activity[p['activity_id']]['activity_type']=='CALIBRATION' and any(st['stage_event_id']==activity[p['activity_id']]['stage_event_id'] and st['stage']=='FIRST_INTERVIEW' for st in data['stage_history']))
    if 'interview_model' in rules:interview_effort=effort['FIRST_INTERVIEW_SESSION']
    target_date=datetime.combine(datetime.fromisoformat(data['workforce_plan']['target_date']).date(),time.max,ZoneInfo('Asia/Seoul'))
    ready=[r for r in workforce if r['event_type']=='READY_CONFIRMED']
    by_target=unique([r for r in ready if parse(r['effective_at'])<=target_date], 'employee_id')
    plan=data['workforce_plan'];supply=plan['forecast_supply_fte']+by_target
    waits=[(parse(r['effective_at'])-parse(profiles[r['employee_id']]['joined_at'])).total_seconds()/86400 for r in ready]
    capacity_events=data['interview_capacity_events']
    revised=sum(float(e['person_hours'])*( -1 if e['event_type']=='CAPACITY_RELEASED' else 1) for e in capacity_events if e['event_type']!='GAP_IDENTIFIED')
    reserved=sum(float(e['person_hours'])*(1 if e['event_type']=='RESERVED' else -1) for e in data['capacity_assignments'])
    released=sum(float(e['person_hours']) for e in data['capacity_assignments'] if e['event_type']=='RELEASED')
    hold_apps={f['application_id'] for f in data['final_decisions'] if f['decision']=='HOLD'}
    rereviews=[f for f in data['final_decisions'] if f['review_round']=='RE_REVIEW']
    return {'scope':'Synthetic Dataset '+rules['dataset_version']+' sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.',
            'eligibility_resolution':(summarize_resolution(data) if rules.get('eligibility_resolution') else None),
            'application_document':(summarize_application(data) if rules.get('application_model') else None),
            'dataset_version':rules['dataset_version'],'record_counts':counts,'funnel':funnel,'stage_outcomes':outcomes,
            'time_distributions':timings,'capacity':{'by_activity_person_hours':{k:round(v,4) for k,v in sorted(effort.items())},
            'total_person_hours':round(sum(effort.values()),4),'first_interview_and_calibration_person_hours':round(interview_effort+first_calibration if 'interview_model' in rules else interview_effort,4),'interview_consumed_person_hours':round(interview_effort,4),'first_calibration_person_hours':round(first_calibration,4),'additional_person_hours':sum(float(e['person_hours']) for e in capacity_events if e['event_type']=='CAPACITY_ADDED'),
            'initial_person_hours':sum(float(e['person_hours']) for e in capacity_events if e['event_type']=='INITIAL_PLAN'),
            'demand_person_hours':max((float(e['demand_person_hours']) for e in capacity_events),default=0),
            'gap_person_hours':sum(float(e['person_hours']) for e in capacity_events if e['event_type']=='GAP_IDENTIFIED'),
            'revised_person_hours':revised,'reserved_remaining_person_hours':round(reserved,4),
            'released_reservation_person_hours':round(released,4),'available_remaining_person_hours':round(revised-reserved-interview_effort,4),
            'history':capacity_events,
            'first_interview_plan_capacity_person_hours':rules['capacity']['initial_person_hours'],'incomplete_participation_intervals':incomplete},
            'offer_events':{kind:sum(r['event_type']==kind for r in offer_events) for kind in ('OFFERED','ACCEPTED','DECLINED','EXPIRED','PRE_JOIN_WITHDRAWAL')},
            'offer_current_states':dict(sorted(Counter(sorted([e for e in offer_events if e['offer_id']==o['offer_id']],key=lambda r:r['occurred_at'])[-1]['event_type'] for o in data['offers']).items())),
            'workforce':{'forecast_supply_fte':plan['forecast_supply_fte'],'joined':actual['JOIN'],
            'ready_observed':unique(ready,'employee_id'),'ready_by_target_date':by_target,'target_date':plan['target_date'],
            'available_supply_at_target_fte':supply,'demand_fte':plan['demand_fte'],'fulfillment_ratio':supply/plan['demand_fte'],
            'ramp_up_extended':unique([r for r in workforce if r['event_type']=='RAMP_UP_EXTENDED'],'employee_id'),
            'join_to_ready_days':distribution(waits)},
            'evidence_counts':{k:len(data[k]) for k in ('assessment_evidence','assessment_observations','evidence_decisions','skill_decision_observations','final_decisions')},
            'calibration_activity':{'eligible':len(data['calibration_reviews']),'triggered':sum(bool(json.loads(r['trigger_codes'])) for r in data['calibration_reviews']),'actual':sum(a['activity_type'] in ('CALIBRATION','FOLLOW_UP_CALIBRATION') and a['activity_status']=='COMPLETED' for a in data['assessment_activities']),'person_hours':round(effort['CALIBRATION']+effort['FOLLOW_UP_CALIBRATION'],4)},
            'calibration':dict(sorted(Counter(r['decision_status'] for r in data['evidence_decisions']).items())),
            'first_coverage':dict(Counter('COVERED' if all(v.get('decisionable',v['state']=='A') for v in json.loads(s['rationale'])['coverage'].values()) else 'NOT_COVERED' for s in stage_rows['FIRST_INTERVIEW'] if s['decision_at'] and 'coverage' in json.loads(s['rationale']))),
            'hold':{'initial_proceed':sum(f['review_round']=='INITIAL' and f['decision']=='PROCEED_TO_OFFER' for f in data['final_decisions']),'initial_do_not_proceed':sum(f['review_round']=='INITIAL' and f['decision']=='DO_NOT_PROCEED' for f in data['final_decisions']),'targeted_completed':sum(a['activity_type']=='FOCUSED_FOLLOW_UP' and a['activity_status']=='COMPLETED' for a in data['assessment_activities']),'initial':len(hold_apps),'follow_up_activities':sum(a['activity_type']=='FOCUSED_FOLLOW_UP' for a in data['assessment_activities']),'re_reviews':len(rereviews),'pending':len(hold_apps)-len(rereviews),'re_review_outcomes':dict(Counter(f['decision'] for f in rereviews))},
            'ready':{'not_yet_ready':len(profiles)-len(ready),'gap_skill_counts':dict(Counter(g['skill_id'] for g in data['onboarding_skill_gaps']))},
            'final_decisions':{kind:sum(r['decision']==kind for r in data['final_decisions']) for kind in ('PROCEED_TO_OFFER','DO_NOT_PROCEED','HOLD')},
            'final_current_states':dict(Counter(max([f for f in data['final_decisions'] if f['application_id']==aid],key=lambda f:f['decided_at'])['decision'] for aid in {f['application_id'] for f in data['final_decisions']})),
            'validation':validation,'notes':['Target differences are not validation errors.','Calibration counts include successive review snapshots, not unique candidates.','All people, judgments and work artifacts are synthetic. Human rule review remains pending.']}


def markdown(report):
    lines=['# Mission 1 Dataset '+report['dataset_version']+' — Sanity Report','',report['scope'],'',
           f"Validation: **{report['validation']['status']}** · Errors: {len(report['validation']['errors'])} · Warnings: {len(report['validation']['warnings'])}",'',
           '## Record Counts','','| File | Records |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in report['record_counts'].items()]
    lines += ['','## Target vs Actual','','| Bucket | Target | Actual | Difference |','|---|---:|---:|---:|']
    lines += [f"| {r['label']} | {r['target']} | {r['actual']} | {r['difference']:+} |" for r in report['funnel']]
    lines += ['','## Stage Outcomes','','| Stage | Entered | Completed | Advanced | Conditional | Failed | Closed | Withdrawn | In Progress | Final lifecycle completed |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    lines += [f"| {s} | "+' | '.join(str(row[k]) for k in ('ENTERED','COMPLETED','ADVANCED','CONDITIONAL_ADVANCE','FAILED','CLOSED','WITHDRAWN','IN_PROGRESS','FINAL_REVIEW_COMPLETED'))+' |' for s,row in report['stage_outcomes'].items()]
    lines += ['','## Time Distributions','','Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.','','| Metric / Stage | n | Median | p90 | Range | NULL endpoints |','|---|---:|---:|---:|---|---:|']
    for metric,stages in report['time_distributions'].items():
        for stage,d in stages.items():lines.append(f"| {metric} / {stage} | {d['n']} | {d['median']} | {d['p90']} | {d['min']}–{d['max']} | {d['null_count']} |")
    for title,key in [('Capacity','capacity'),('Offer Lifecycle','offer_events'),('Offer Current State','offer_current_states'),('Workforce / Onboarding','workforce'),('Evidence','evidence_counts'),('Calibration','calibration'),('Calibration Activities','calibration_activity'),('Final Decision History','final_decisions'),('Latest Final Decisions','final_current_states'),('HOLD Follow-up','hold'),('Ready Coverage','ready')]:
        lines += ['',f'## {title}','']
        for k,v in report[key].items():
            if k=='history':
                lines += ['', '| Event | Hours | Demand | Effective at | Human role |', '|---|---:|---:|---|---|']
                lines += [f"| {e['event_type']} | {e['person_hours']} | {e['demand_person_hours']} | {e['effective_at']} | {e['decided_by']} |" for e in v]
            else:lines.append(f'- {k}: {v}')
    lines += ['','## Validation','']
    for error in report['validation']['errors']:lines.append(f"- ERROR {error['code']}: {error['message']}")
    for warning in report['validation']['warnings']:lines.append(f"- WARNING {warning['code']}: {warning['message']}")
    lines += ['','## Interpretation Boundary','']+['- '+note for note in report['notes']]
    if report.get('application_document'):
        lines += ['','## Application / Document (v0.5)','', 'CLOSED means insufficient submitted application evidence; it is not Skill limitation.', '', '```json', json.dumps(report['application_document'],ensure_ascii=False,indent=2), '```']
    if report.get('eligibility_resolution'):
        lines += ['', '## Eligibility Resolution (v0.6)', '', '```json', json.dumps(report['eligibility_resolution'],ensure_ascii=False,indent=2), '```']
    return '\n'.join(lines)+'\n'
