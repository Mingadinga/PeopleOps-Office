"""Independent structural/invariant validator; reports errors without repairing rows."""
import json
from collections import Counter, defaultdict
from datetime import timedelta
from .common import parse, compact
from .schema import SCHEMA, KEYS, NULLABLE, ENUMS, STAGES, LEVELS, ACTIVITIES, PROVENANCE, FORBIDDEN



def _validate(data, rules):
    errors=[];warnings=[];checks=Counter()
    def check(ok, code, message):
        checks[code]+=1
        if not ok:errors.append({'code':code,'message':message})
    def result():
        return {'status':'ERROR' if errors else 'PASS','errors':errors,'warnings':warnings,'checks':dict(sorted(checks.items()))}
    start,end=parse(rules['observation_start']),parse(rules['observation_end'])
    indexes={}
    for table,columns in SCHEMA.items():
        rows=data.get(table)
        check(isinstance(rows,list),'schema',f'{table}: missing table')
        if not isinstance(rows,list):continue
        if '_headers_'+table in data:
            check(data['_headers_'+table]==columns,'schema',f'{table}: CSV headers/order mismatch')
        seen=set();indexes[table]={}
        for n,row in enumerate(rows):
            loc=f'{table}[{n}]'
            check(set(row)==set(columns),'schema',f'{loc}: unexpected/missing columns')
            if set(row)!=set(columns):continue
            check(all(isinstance(v,str) for v in row.values()),'schema',f'{loc}: CSV cells must be strings')
            key=tuple(row[k] for k in KEYS[table]);check(key not in seen,'primary_key',f'{loc}: duplicate {key}');seen.add(key)
            indexes[table][key[0]]=row
            for col,value in row.items():
                check(col.lower() not in FORBIDDEN,'forbidden',f'{loc}.{col}: forbidden field')
                if col not in NULLABLE.get(table,set()):check(value!='','required',f'{loc}.{col}: NULL forbidden')
                options=ENUMS.get((table,col))
                if value and options:check(value in options,'enum',f'{loc}.{col}: {value}')
                if value and (col.endswith('_at') or col=='response_deadline'):
                    try:
                        dt=parse(value)
                        check(dt.utcoffset()==timedelta(hours=9),'timestamp',f'{loc}.{col}: not Asia/Seoul offset')
                        if col not in ('scheduled_at','expected_join_at','planned_ready_at','response_deadline'):
                            check(start<=dt<=end,'observation_window',f'{loc}.{col}: outside observation window')
                    except (ValueError,TypeError):check(False,'timestamp',f'{loc}.{col}: invalid timestamp')
    if errors:return result()

    def scan(value, location):
        if isinstance(value,dict):
            for key,item in value.items():
                check(key.lower() not in FORBIDDEN,'forbidden',f'{location}.{key}')
                scan(item,location+'.'+key)
        elif isinstance(value,list):
            for i,item in enumerate(value):scan(item,f'{location}[{i}]')
    for name in ('workforce_plan','funnel_plan','talent_profile'):
        scan(data.get(name),name)
    plan=data.get('workforce_plan',{});funnel=data.get('funnel_plan',[]);skills=data.get('talent_profile',[])
    needed=set(rules['workforce_plan'])|{'forecast_supply_fte','workforce_gap','evidence_type'}
    check(isinstance(plan,dict) and needed<=set(plan),'plan_schema','workforce_plan required fields')
    check(isinstance(funnel,list) and len(funnel)==8,'plan_schema','eight Target buckets required')
    check(isinstance(skills,list) and len(skills)==len(rules['skills']),'plan_schema','talent profile required')
    if errors:return result()
    for field,value in rules['workforce_plan'].items():check(plan[field]==value,'plan_value',f'workforce_plan.{field}')
    if errors:return result()
    forecast=plan['current_fte']+plan['confirmed_transfer_in']-plan['confirmed_transfer_out']+plan['confirmed_joiners']
    check(plan['forecast_supply_fte']==forecast and plan['workforce_gap']==max(plan['demand_fte']-forecast,0),'derived_plan','Forecast/Gap mismatch')
    check(plan['evidence_type']=='SYNTHETIC','provenance','Plan provenance')
    for row,expected in zip(funnel,rules['funnel_targets']):
        fields={'plan_id','stage','label','target_count','expected_conversion_rate','unit_effort_person_hours','available_capacity_person_hours','assumption_note','evidence_type'}
        check(set(row)==fields,'plan_schema','funnel fields; Actual is not a Plan field')
        check([row.get('stage'),row.get('label'),row.get('target_count')]==expected,'plan_value','Target bucket changed')
        check(row.get('plan_id')==plan['plan_id'],'foreign_key','Funnel→Workforce Plan')
        check(row.get('evidence_type')=='SYNTHETIC','provenance','Funnel provenance')
    skill_index={s.get('skill_id'):s for s in skills}
    check(len(skill_index)==len(skills),'primary_key','duplicate Skill ID')
    for row,expected in zip(skills,rules['skills']):
        for col in ('skill_id','skill_name','requirement_type','description','expected_evidence'):
            check(row.get(col)==expected[col],'plan_value',f'Skill.{col}')
    if errors:return result()

    def fk(table,key,location):
        parent=indexes[table].get(key)
        check(parent is not None,'foreign_key',f'{location}: {key} not in {table}')
        return parent
    def ordered(row,before,after,label):
        if row.get(before) and row.get(after):
            check(parse(row[after])>=parse(row[before]),'temporal',f'{label}: {after} < {before}')
    apps=indexes['applications'];candidates={a['candidate_id']:a for a in apps.values()}
    check(len(candidates)==len(apps),'candidate_identity','This case uses one application per candidate')
    for a in apps.values():
        check(a['application_id']!=a['candidate_id'],'candidate_identity','Application ID must differ from candidate ID')
        check(a['job_id']==rules['job_id'],'foreign_key','Job ID not in Case')
        check((a['application_status']=='SUBMITTED')==bool(a['submitted_at']),'application_state',a['application_id'])
        ordered(a,'started_at','submitted_at',a['application_id'])
    for table,rows in data.items():
        if table not in SCHEMA:continue
        for row in rows:
            if 'application_id' in row and table!='applications':
                app=fk('applications',row['application_id'],table)
                if app:check(row['candidate_id']==app['candidate_id'],'candidate_relation',table)
            if 'candidate_id' in row:check(row['candidate_id'] in candidates,'foreign_key',table+': candidate')
            if row.get('skill_id'):check(row['skill_id'] in skill_index,'foreign_key',table+': skill')
    if errors:return result()
    stage_by_app=defaultdict(list)
    for row in data['stage_history']:
        aid=row['application_id'];stage_by_app[aid].append(row);app=apps[aid]
        check(app['application_status']=='SUBMITTED','stage_lifecycle','Unsubmitted application in process')
        check(parse(row['entered_at'])>=parse(app['submitted_at']),'temporal','Stage before submission')
        for a,b in [('entered_at','invited_at'),('invited_at','scheduled_at'),('scheduled_at','completed_at'),('entered_at','completed_at'),('completed_at','decision_at'),('decision_at','notified_at'),('entered_at','withdrawn_at')]:ordered(row,a,b,row['stage_event_id'])
        if row['result'] in ('ADVANCED','FAILED'):
            check(bool(row['completed_at'] and row['decision_at'] and row['rationale'] and row['decision_reason_code']),'stage_decision','Terminal decision lacks completion/trace')
        if row['stage']=='DOCUMENT_SCREEN' and row['result']=='FAILED':
            trace=json.loads(row['rationale'])
            check(bool(trace.get('public_requirement_ref') and trace.get('explicit_violation_ref')),'stage_decision','Document failure lacks verified public requirement violation')
        if row['stage']!='FINAL_REVIEW':check(bool(row['result']),'stage_decision','Only FINAL_REVIEW may have NULL result')
        check(bool(row['withdrawn_at'])==(row['result']=='WITHDRAWN'),'withdrawal','withdrawn_at/result mismatch')
        check(bool(row['withdrawal_reason_code'])==(row['result']=='WITHDRAWN'),'withdrawal','withdrawal reason mismatch')
        if row['result']=='WITHDRAWN':check(not row['decision_at'] and not row['notified_at'] and not row['decision_reason_code'],'withdrawal','Withdrawal is not company decision')
        if row['decision_at']:check(row['decision_provenance']==PROVENANCE,'provenance','Stage judgment provenance')
        if row['notified_at']:check(bool(row['decision_at']),'temporal','Notification without decision')
        if row['result']=='IN_PROGRESS' and row['decision_at']:
            check((row['stage']=='FINAL_REVIEW' and row['decision_reason_code']=='ADDITIONAL_EVIDENCE_REQUIRED') or ('interview_model' in rules and row['stage']=='FIRST_INTERVIEW' and row['decision_reason_code']=='EVIDENCE_PENDING'),'stage_decision','Unexpected pending judgment')
    for aid,rows in stage_by_app.items():
        sequence=sorted(rows,key=lambda r:STAGES.index(r['stage']))
        names=[r['stage'] for r in sequence]
        check(names==list(STAGES[:len(names)]),'stage_lifecycle',aid+': missing/duplicate/out-of-order Stage')
        for prior,current in zip(sequence,sequence[1:]):
            check(prior['result']=='ADVANCED' and bool(prior['notified_at']),'stage_lifecycle',aid+': advanced before prior notification')
            if prior['notified_at']:check(parse(current['entered_at'])>=parse(prior['notified_at']),'temporal','Next Stage precedes notice')
    for row in data['assessment_activities']:
        stage=fk('stage_history',row['stage_event_id'],'Activity')
        if stage:
            check((row['application_id'],row['candidate_id'])==(stage['application_id'],stage['candidate_id']),'activity_relation',row['activity_id'])
            check(row['activity_type'] in ACTIVITIES[stage['stage']],'activity_relation','Activity in wrong Stage')
            if row['started_at']:check(parse(row['started_at'])>=parse(stage['entered_at']),'temporal','Activity before Stage')
        ordered(row,'started_at','completed_at',row['activity_id'])
        if row['activity_status']=='COMPLETED':check(bool(row['started_at'] and row['completed_at']),'activity_state','Complete Activity missing timestamps')
        if row['activity_status']=='PLANNED':check(not row['started_at'] and not row['completed_at'],'activity_state','Planned Activity has actual timestamps')
    for row in data['activity_participants']:
        activity=fk('assessment_activities',row['activity_id'],'Participant')
        if activity:
            check(bool(activity['started_at']),'participant_time','Participant in unstarted activity')
            if activity['started_at']:check(parse(row['participation_started_at'])>=parse(activity['started_at']),'participant_time','Participant before Activity')
            if row['participation_ended_at'] and activity['completed_at']:check(parse(row['participation_ended_at'])<=parse(activity['completed_at']),'participant_time','Participant after Activity')
        ordered(row,'participation_started_at','participation_ended_at','Participant')
    intervals=defaultdict(list)
    for row in data['activity_participants']:
        if row['participation_ended_at']:
            intervals[row['participant_id']].append((parse(row['participation_started_at']),parse(row['participation_ended_at'])))
    for actor,periods in intervals.items():
        periods.sort()
        for earlier,later in zip(periods,periods[1:]):
            check(later[0]>=earlier[1],'participant_time',actor+': overlapping participation intervals')
    raw={}
    for row in data['assessment_evidence']:
        if row['activity_id']:
            activity=fk('assessment_activities',row['activity_id'],'Evidence')
            if activity:
                check((row['application_id'],row['candidate_id'])==(activity['application_id'],activity['candidate_id']),'evidence_relation',row['evidence_id'])
                check(bool(activity['completed_at']),'evidence_relation','Evidence for unfinished Activity')
                if activity['completed_at']:check(row['created_at']==activity['completed_at'],'temporal','Evidence does not match completed source')
        else:check(row['source_type']=='APPLICATION_RESPONSE','evidence_relation','Only application response may lack Activity')
        check(row['source_ref']==f"assessment_evidence.csv#{row['evidence_id']}/raw_evidence",'source_reference','Raw Evidence reference')
        try:
            artifact=json.loads(row['raw_evidence']);raw[row['evidence_id']]=artifact;scan(artifact,row['evidence_id'])
            check(set(artifact)=={'task','action','verification','revision','ownership','response','context'},'evidence_schema',row['evidence_id'])
            check(artifact.get('ownership') in ('SELF','TEAM_UNCLEAR','UNSPECIFIED'),'evidence_schema','Unknown ownership')
        except (ValueError,TypeError):check(False,'evidence_schema','Invalid raw Evidence JSON')
    if errors:return result()
    from .invariants import evidence_and_decisions, capacity_history, workforce_and_offers
    evidence_and_decisions(data,rules,indexes,check,fk,ordered,scan)
    capacity_history(data,rules,indexes,check,fk)
    workforce_and_offers(data,rules,indexes,check,fk,ordered,scan)
    warnings.append({'code':'REVIEW_PENDING','message':'Synthetic rules/realism review remains pending; no freeze.'})
    warnings.append({'code':'SYNTHETIC_POLICY_ASSUMPTIONS','message':'Source matrix, resource blocks, re-review uncertainty handling and mentor scenarios require human rule audit; not employer policies.'})
    if not data['offers']:warnings.append({'code':'EMPTY_OFFER_COHORT','message':'No offers; preserve empty sample.'})
    if not data['onboarding_profiles']:warnings.append({'code':'EMPTY_ONBOARDING_COHORT','message':'No joiners; preserve empty sample.'})
    return result()


def validate(data,rules):
    try:return _validate(data,rules)
    except (ValueError,TypeError,KeyError,AttributeError,IndexError,OverflowError) as exc:
        return {'status':'ERROR','errors':[{'code':'invalid_format','message':str(exc)}],'warnings':[],'checks':{'invalid_format':1}}


def validate_manifest(manifest, data, rules, directory, rules_path):
    """Verify the single manifest owner against persisted bytes, not in-memory rows."""
    import hashlib
    from pathlib import Path
    from .common import file_hashes
    errors=[]
    def require(condition,message):
        if not condition:errors.append({'code':'manifest','message':message})
    for field in ('dataset_version','generation_version','generation_rules_version','schema_version','seed','generated_at','observation_start','observation_end','timezone','case_id','job_id'):
        require(manifest.get(field)==rules[field],'Manifest mismatch: '+field)
    counts={n+'.csv':len(data[n]) for n in SCHEMA}
    counts.update({n+'.json':len(data[n]) if isinstance(data[n],list) else 1 for n in ('workforce_plan','funnel_plan','talent_profile')})
    require(manifest.get('record_counts')==counts,'Manifest record counts differ from persisted data')
    require(manifest.get('file_sha256')==file_hashes(directory),'Dataset file hashes do not match manifest')
    require(manifest.get('generation_rules_sha256')==hashlib.sha256(Path(rules_path).read_bytes()).hexdigest(),'Rules hash differs')
    code_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))}
    require(manifest.get('generator_source_sha256')==code_hashes,'Generator source differs; regenerate/review candidate after implementation fixes')
    require(manifest.get('review_status')=='UNREVIEWED' and manifest.get('frozen') is False,'Review candidate must remain unfrozen and unreviewed')
    for key in ('implementation_parameters','random_stream_version','source_matrix'):
        require(manifest.get(key)==rules.get(key),'Manifest parameters differ: '+key)
    require(manifest.get('capacity_parameters')==rules.get('capacity'),'Manifest capacity parameters differ')
    require(manifest.get('response_window_days')==rules['offers']['response_window_days'],'Manifest response window differs')
    return errors
