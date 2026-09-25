"""Deterministic event generation. Funnel Targets never gate outcomes."""
import json
from .common import empty_data, rng, parse, stamp, plus, compact
from .schema import SCHEMA, STAGES, ACTIVITIES, PROVENANCE
from .evidence import EvidenceWriter, final_review, stage_transition_decision, latest_decisions
from .capacity import Capacity

class Generator:
    def __init__(self, rules):
        self.rules = rules
        self.data = empty_data()
        self.end = parse(rules['observation_end'])
        self.evidence = EvidenceWriter(self.data, rules, self.add)
        self.capacity = Capacity(self)
        self.modern = 'interview_model' in rules
        self.pool_blocks = {}

    def add(self, table, **values):
        unknown = set(values)-set(SCHEMA[table])
        if unknown:
            raise ValueError(f'{table}: unexpected fields {unknown}')
        row = {k: str(values.get(k,'')) for k in SCHEMA[table]}
        self.data[table].append(row)
        return row

    def plans(self):
        plan = dict(self.rules['workforce_plan'])
        forecast = plan['current_fte']+plan['confirmed_transfer_in']-plan['confirmed_transfer_out']+plan['confirmed_joiners']
        plan.update(forecast_supply_fte=forecast,workforce_gap=max(plan['demand_fte']-forecast,0),evidence_type='SYNTHETIC')
        self.data['workforce_plan'] = plan
        funnel = []
        previous = None
        for stage, label, count in self.rules['funnel_targets']:
            funnel.append({'plan_id':plan['plan_id'],'stage':stage,'label':label,'target_count':count,
                           'expected_conversion_rate':count/previous if previous else None,
                           'unit_effort_person_hours':self.rules['capacity']['planned_unit_person_hours'] if stage=='FIRST_INTERVIEW' else None,
                           'available_capacity_person_hours':self.rules['capacity']['initial_person_hours'] if stage=='FIRST_INTERVIEW' else None,
                           'assumption_note':('SYNTHETIC Plan; not quota. FIRST: single 60min × 3; calibration separate.' if self.modern else 'SYNTHETIC Plan; not quota. FIRST_INTERVIEW: (90+30)min × 2 evaluators.'),
                           'evidence_type':'SYNTHETIC'})
            previous = count
        self.data['funnel_plan'] = funnel
        self.data['talent_profile'] = [{k:v for k,v in s.items() if k not in ('example_action','example_check')} for s in self.rules['skills']]

    def applications(self):
        config = self.rules['applications']; start = parse(config['arrival_start'])
        index = 0
        for day in range(config['arrival_days']):
            arrival_rng = rng(self.rules,'arrivals',day)
            for _ in range(arrival_rng.randint(config['daily_arrivals_min'],config['daily_arrivals_max'])):
                index += 1; cid=f'C{index:04d}'; aid=f'APP{index:04d}'
                clock=rng(self.rules,'application',cid)
                began=plus(start,days=day,minutes=clock.randrange(480))
                if began>self.end:
                    continue
                action=clock.choice(config['draft_actions']); submitted=''; status='STARTED'
                if action=='SUBMIT':
                    at=plus(began,days=clock.choice(config['submission_delay_days']))
                    if at<=self.end:
                        submitted=stamp(at);status='SUBMITTED'
                elif action=='ABANDON':
                    status='ABANDONED'
                self.add('applications',application_id=aid,candidate_id=cid,job_id=self.rules['job_id'],
                         source_channel=rng(self.rules,'channel',cid).choice(config['channel_options']),
                         started_at=stamp(began),submitted_at=submitted,application_status=status)

    def activity(self, app, stage, kind, begin, minutes, participants, panel=1, follow_skills=None):
        aid=stage['stage_event_id']+'_'+kind
        group='FIRST' if stage['stage']=='FIRST_INTERVIEW' else stage['stage']
        actors=[(f'{group}_PANEL_{panel:02d}_{role}',role) for role in participants]
        # A lightweight reusable pool; only occupied blocks, no personal calendar.
        while True:
            end=plus(begin,minutes=minutes)
            overlaps=[b for actor,role in actors for a,b in self.pool_blocks.get(actor,[]) if begin<b and end>a]
            if not overlaps:break
            begin=max(overlaps)
        for actor,role in actors:self.pool_blocks.setdefault(actor,[]).append((begin,end))
        status='PLANNED' if begin>self.end else 'IN_PROGRESS' if end>self.end else 'COMPLETED'
        row=self.add('assessment_activities',activity_id=aid,stage_event_id=stage['stage_event_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],activity_type=kind,started_at=stamp(begin) if begin<=self.end else '',completed_at=stamp(end) if end<=self.end else '',activity_status=status)
        if begin<=self.end:
            for actor,role in actors:
                self.add('activity_participants',activity_id=aid,participant_id=actor,participant_role=role,participation_started_at=stamp(begin),participation_ended_at=stamp(end) if end<=self.end else '')
                if stage['stage']=='FIRST_INTERVIEW' and end<=self.end and (not self.modern or kind=='FIRST_INTERVIEW_SESSION'):
                    self.capacity.assignment(stage,'CONSUMED',minutes/60,end,'ACTUAL_PARTICIPATION',aid,actor)
        if self.modern and kind in ('CALIBRATION','FOLLOW_UP_CALIBRATION'):
            from .interview import calibration_ledger
            calibration_ledger(self,stage,row,actors,begin,end)
        matrix=self.rules['source_matrix'].get(kind)
        if status=='COMPLETED' and matrix:
            self.evidence.collect(app,row,[f'M1_SKILL_{i:02d}' for i in matrix['skills']],end)
        if status=='COMPLETED' and kind=='FOCUSED_FOLLOW_UP':
            if self.modern:
                from .interview import collect_targeted
                collect_targeted(self,app,row,end)
                return end
            for sid in follow_skills:
                technical=sid in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03')
                self.evidence.collect(app,row,[sid],end,'TECHNICAL_ASSESSMENT_RESPONSE' if technical else 'INTERVIEW_RESPONSE','DIRECT_TASK' if technical else 'BEHAVIORAL_INTERACTION','HOLD 질문: '+self.rules['hold']['questions']['technical' if technical else 'behavioral'])
        return end

    def write_final(self,app,when,round_name,follow_id=''):
        conclusion,trace=final_review(self.data,app['application_id'],self.rules,stamp(when),round_name)
        reason='';plan=''
        if conclusion=='HOLD':
            reason='EVALUATOR_DISAGREEMENT' if trace['disagreement_must'] else 'MISSING_EVIDENCE' if trace['missing_must'] else 'UNRESOLVED_EVIDENCE'
            plan=compact([{'skill_id':s,'question':self.rules['hold']['questions']['technical' if s in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03') else 'behavioral'],'context':'앞선 관찰의 미확인/검증 범위','method':'DIRECT_TASK' if s in ('M1_SKILL_01','M1_SKILL_02','M1_SKILL_03') else 'BEHAVIORAL_INTERACTION'} for s in trace['unresolved_must']])
        row=self.add('final_decisions',final_decision_id='FD_'+app['application_id']+'_'+round_name,review_round=round_name,hold_reason_code=reason,resolution_plan=plan,follow_up_activity_id=follow_id,application_id=app['application_id'],candidate_id=app['candidate_id'],must_evidence_status='REPEATED_LIMITATION' if trace['repeated_must_limitations'] else 'UNRESOLVED' if trace['unresolved_must'] else 'COVERED',remaining_uncertainty=compact(trace['unresolved_must']),learnable_gap_summary=compact(trace['learnable_gaps']),decision=conclusion,rationale=compact(trace),decided_by='FINAL_PANEL_01',decided_at=stamp(when),decision_provenance=PROVENANCE)
        if self.modern and conclusion=='HOLD':
            from .interview import resolution_plan
            row['resolution_plan']=compact(resolution_plan(self,row))
        return row

    def stage(self,app,name,entered):
        if entered>self.end:return None
        config=self.rules['process'];clock=rng(self.rules,'stage',app['candidate_id'],name)
        record=self.add('stage_history',stage_event_id=app['application_id']+'_'+name,application_id=app['application_id'],candidate_id=app['candidate_id'],stage=name,entered_at=stamp(entered),result='IN_PROGRESS')
        internal=name in ('DOCUMENT_SCREEN','FINAL_REVIEW');panel=1
        if internal:
            record['completed_at']=stamp(entered)
            begin=plus(entered,days=clock.choice(config['document_review_days']))
        else:
            if name=='FIRST_INTERVIEW' and self.capacity.ready>self.end:
                record['rationale']=compact({'operational_state':'CAPACITY_WAIT','reason':'resource decision not observed'})
                return None
            invited=max(plus(entered,days=1),self.capacity.ready) if name=='FIRST_INTERVIEW' else plus(entered,days=1)
            if invited>self.end:return None
            record['invited_at']=stamp(invited)
            if name=='FIRST_INTERVIEW':
                if self.capacity.ready>self.end:
                    record['rationale']=compact({'operational_state':'CAPACITY_WAIT','reason':'resource decision not observed'})
                    return None
                begin,panel=self.capacity.next_slot(plus(invited,days=4))
                self.capacity.stage_panels[record['stage_event_id']]=panel
                self.capacity.assignment(record,'RESERVED',self.rules['capacity']['planned_unit_person_hours'],invited,'SCHEDULED_ALLOCATION')
            else:
                field='preassessment_wait_days' if name=='PRE_ASSESSMENT' else 'second_interview_wait_days'
                begin=plus(invited,days=clock.choice(config[field]))
            record['scheduled_at']=stamp(begin)
            contact=clock.choice(config['withdrawal_contacts'])
            if contact=='WITHDRAW_CONFIRMED_UNKNOWN':
                at=plus(invited,days=2)
                if at<=self.end:
                    record.update(result='WITHDRAWN',withdrawn_at=stamp(at),withdrawal_reason_code='UNKNOWN')
                    if name=='FIRST_INTERVIEW':self.capacity.close(record,at,'CONFIRMED_WITHDRAWAL_UNUSED')
                return None
            if contact=='CANCEL_CONFIRMED':
                at=plus(invited,days=2)
                if at<=self.end:
                    record['rationale']=compact({'operational_state':'CANCELLED','confirmed_at':stamp(at),'motive':'UNKNOWN'})
                    for kind in ACTIVITIES[name]:
                        self.add('assessment_activities',activity_id=record['stage_event_id']+'_'+kind,stage_event_id=record['stage_event_id'],application_id=app['application_id'],candidate_id=app['candidate_id'],activity_type=kind,activity_status='CANCELLED')
                    if name=='FIRST_INTERVIEW':self.capacity.close(record,at,'CANCELLED_UNUSED')
                return None
            if contact=='NO_RESPONSE_PENDING':
                record['rationale']=compact({'operational_state':'NO_RESPONSE_PENDING','motive':'UNKNOWN'})
                if name=='FIRST_INTERVIEW':self.capacity.close(record,plus(begin,days=self.rules['capacity']['no_response_release_days']),'NO_RESPONSE_UNUSED')
                return None
        activity_end=begin
        kinds=('FINAL_REVIEW_DISCUSSION',) if name=='FINAL_REVIEW' else tuple(k for k in ACTIVITIES[name] if k!='FIRST_INTERVIEW_SESSION' and not (name=='SECOND_INTERVIEW' and k=='CALIBRATION'))
        if self.modern and name=='FIRST_INTERVIEW':
            from .interview import first_session
            activity_end=first_session(self,app,record,begin,panel)
            kinds=()
        for kind in kinds:
            roles=() if kind in ('APTITUDE','CODING_TEST') else ('RECRUITER',) if kind=='DOCUMENT_REVIEW' else ('ML_ENGINEER','HIRING_MANAGER')
            activity_end=self.activity(app,record,kind,activity_end,clock.choice(config['activity_minutes'][kind]),roles,panel)
        if self.modern and name in ('FIRST_INTERVIEW','SECOND_INTERVIEW') and activity_end<=self.end:
            from .interview import observe_and_calibrate
            activity_end=observe_and_calibrate(self,app,record,activity_end,panel,'CALIBRATION')
        if name=='FIRST_INTERVIEW':self.capacity.close(record,activity_end,'COMPLETED_UNUSED')
        if not internal:
            candidate_activities=[a for a in self.data['assessment_activities'] if a['stage_event_id']==record['stage_event_id'] and a['activity_type']!='CALIBRATION']
            if candidate_activities[-1]['completed_at']:record['completed_at']=candidate_activities[-1]['completed_at']
        decision=plus(activity_end,days=clock.choice(config['decision_delay_days']))
        if decision>self.end:return None
        self.evidence.review(app,decision,canonical=name!='DOCUMENT_SCREEN')
        if name=='FINAL_REVIEW':
            final=self.write_final(app,decision,'INITIAL')
            if final['decision']=='HOLD':
                record.update(decision_at=stamp(decision),decision_provenance=PROVENANCE,decision_reason_code='ADDITIONAL_EVIDENCE_REQUIRED',rationale=compact({'final_decision_ref':final['final_decision_id']}))
                begin=plus(decision,days=self.rules['hold']['follow_up_wait_days'])
                skills=[p['skill_id'] for p in json.loads(final['resolution_plan'])]
                end=self.activity(app,record,'FOCUSED_FOLLOW_UP',begin,clock.choice(config['activity_minutes']['FOCUSED_FOLLOW_UP']),('ML_ENGINEER','HIRING_MANAGER'),follow_skills=skills)
                follow_id=record['stage_event_id']+'_FOCUSED_FOLLOW_UP'
                final['follow_up_activity_id']=follow_id
                if end>self.end:return None
                if self.modern:
                    from .interview import observe_and_calibrate
                    end=observe_and_calibrate(self,app,record,end,1,'FOLLOW_UP_CALIBRATION')
                else:
                    end=self.activity(app,record,'FOLLOW_UP_CALIBRATION',end,clock.choice(config['activity_minutes']['FOLLOW_UP_CALIBRATION']),('ML_ENGINEER','HIRING_MANAGER'))
                decision=plus(end,days=1)
                if decision>self.end:return None
                self.evidence.review(app,decision)
                final=self.write_final(app,decision,'RE_REVIEW',follow_id)
            record.update(result='',decision_reason_code='FINAL_REVIEW_COMPLETE',rationale=compact({'final_decision_ref':final['final_decision_id']}))
            advance=final['decision']=='PROCEED_TO_OFFER'
        else:
            if self.modern and name=='FIRST_INTERVIEW':
                from .interview import first_transition
                result,reason,trace=first_transition(self.data,app,record,stamp(decision),self.rules.get('final_candidate_contract',False))
            else:
                result,reason,trace=stage_transition_decision(self.data,app,record,stamp(decision))
            advance=result=='ADVANCED'
            record.update(result=result,decision_reason_code=reason,rationale=compact(trace));advance=result=='ADVANCED'
        record.update(decision_at=stamp(decision),decision_provenance=PROVENANCE)
        notified=plus(decision,days=clock.choice(config['notification_delay_days']))
        if notified<=self.end:record['notified_at']=stamp(notified)
        return notified if advance and notified<=self.end else None

    def process(self):
        queue=[(a,parse(a['submitted_at'])) for a in self.data['applications'] if a['application_status']=='SUBMITTED']
        for name in STAGES:
            if name=='FIRST_INTERVIEW':
                self.capacity.plan(queue)
                queue=[(a,max(t,self.capacity.cohort_at)) for a,t in queue]
            next_queue=[]
            for app,entered in sorted(queue,key=lambda item:(item[1],item[0]['application_id'])):
                advanced=self.stage(app,name,entered)
                if advanced is not None:next_queue.append((app,plus(advanced,days=1)))
            queue=next_queue
        for app,at in queue:self.offer(app,at)

    def offer(self,app,when):
        if when>self.end:return
        config=self.rules['offers'];clock=rng(self.rules,'offer',app['candidate_id'])
        oid='OF_'+app['application_id'];join=max(parse(config['expected_join_floor']),plus(when,days=clock.choice(config['join_delay_days'])))
        deadline=plus(when,days=config['response_window_days'])
        self.add('offers',offer_id=oid,application_id=app['application_id'],candidate_id=app['candidate_id'],offered_at=stamp(when),expected_join_at=stamp(join),response_deadline=stamp(deadline))
        def event(kind,at,reason=''):
            self.add('offer_events',offer_event_id=oid+'_'+kind,offer_id=oid,event_type=kind,occurred_at=stamp(at),reason_code=reason)
        event('OFFERED',when)
        reply=plus(when,days=clock.choice(config['response_days']));response=clock.choice(config['response_events'])
        if response=='NO_RESPONSE' or reply>deadline:
            if deadline<=self.end:event('EXPIRED',deadline,'UNKNOWN')
            return
        if reply>self.end:return
        event(response,reply,'UNKNOWN' if response=='DECLINED' else '')
        if response!='ACCEPTED':return
        if clock.choice(config['post_acceptance_contacts'])=='PRE_JOIN_WITHDRAWAL':
            at=plus(reply,days=1)
            if at<=self.end:event('PRE_JOIN_WITHDRAWAL',at,'UNKNOWN')
            return
        if join<=self.end:self.onboard(app,oid,max(join,reply))

    def workforce(self,employee,kind,at,source):
        if at>self.end:return
        human=kind in ('READY_CONFIRMED','RAMP_UP_EXTENDED')
        self.add('workforce_events',workforce_event_id=f'WF_{employee}_{kind}',employee_id=employee,event_type=kind,effective_at=stamp(at),source_ref=source,confirmed_by='MENTOR_POOL_01' if human else '',confirmed_at=stamp(at) if human else '',decision_provenance=PROVENANCE if human else '')

    def onboard(self,app,offer_id,joined):
        import json
        employee='EMP_'+app['candidate_id'];config=self.rules['onboarding'];clock=rng(self.rules,'onboard',app['candidate_id'])
        final=max((f for f in self.data['final_decisions'] if f['application_id']==app['application_id']),key=lambda f:f['decided_at'])
        latest=latest_decisions(self.data,app['application_id'],final['decided_at'])
        self.add('onboarding_profiles',employee_id=employee,source_candidate_id=app['candidate_id'],joined_at=stamp(joined),onboarding_started_at=stamp(joined),planned_ready_at=stamp(plus(joined,days=config['milestone_days'][-1])))
        self.workforce(employee,'JOINED',joined,'offers.csv#'+offer_id)
        self.workforce(employee,'ONBOARDING_STARTED',joined,'onboarding_profiles.csv#'+employee)
        requirements={s:{'requirement_id':'FINAL_LEARNABLE_GAP','context':'Final Review의 학습 가능한 업무 Gap'} for s in json.loads(final['learnable_gap_summary'])}
        for req in config['work_prep_requirements']:
            d=latest.get(req['skill_id'])
            if not d or d['final_level']!='STRONG':requirements[req['skill_id']]=req
        for s in json.loads(final['remaining_uncertainty']):
            requirements[s]={'requirement_id':'ACCEPTED_UNCERTAINTY','context':'재검토에서 수용한 미확인 범위의 업무 준비 확인'}
        for sid,req in sorted(requirements.items()):
            own=[o for o in self.data['assessment_observations'] if o['application_id']==app['application_id'] and o['skill_id']==sid]
            evidence=own[-1]['evidence_id'] if own else ''
            self.add('onboarding_skill_gaps',gap_id='GAP_'+employee+'_'+sid,employee_id=employee,skill_id=sid,gap_level='DEVELOPMENT_REQUIRED' if req['requirement_id']=='FINAL_LEARNABLE_GAP' else 'RECONFIRM_AT_WORK',gap_source='SELECTION_EVIDENCE',source_evidence_id=evidence,final_decision_id=final['final_decision_id'],requirement_ref=req['requirement_id'],rationale=req['context'],confirmed_by='MENTOR_POOL_01',confirmed_at=stamp(joined),decision_provenance=PROVENANCE)
        tasks=[]
        def task(number,day,milestone,kind,sid):
            tid=f'TASK_{employee}_{number:02d}';due=plus(joined,days=day);finished=plus(due,days=clock.choice(config['completion_delay_days']));completed=finished<=self.end
            artifact={};confirmed=False
            if completed:
                record=clock.choice(config['work_records'])
                artifact={'task':kind,'skill_id':sid,'performed_action':'업무 요구에 맞춰 작은 산출물을 만들고 실행/검토 기록을 남겼다.','verification':'CHECK_PENDING' if record=='CHECK_PENDING' else 'OUTPUT_AND_RECOVERY_CHECKED','revision':'확인한 예외를 수정 후 재실행했다.' if record=='REVISED' else '', 'artifact_id':'WORK_'+tid,'evidence_type':'SYNTHETIC','observed_at':stamp(finished)}
                review=rng(self.rules,'mentor',tid).choice(config['mentor_reviews'])
                confirmed=record!='CHECK_PENDING' and review=='CONFIRM'
            row=self.add('onboarding_tasks',task_id=tid,candidate_id=app['candidate_id'],employee_id=employee,milestone=milestone,task_type=kind,related_skill_id=sid,planned_at=stamp(joined),assigned_at=stamp(due) if due<=self.end else '',completed_at=stamp(finished) if completed else '',evidence_ref=f'onboarding_tasks.csv#{tid}/work_evidence' if completed else '',work_evidence=compact(artifact) if completed else '',status='COMPLETED' if completed else 'IN_PROGRESS' if due<=self.end else 'PLANNED',mentor_confirmed=str(confirmed).lower(),decision_provenance=PROVENANCE if completed else '')
            tasks.append(row);return row
        # A local integration task is always required; Skill-specific work is added only for actual gaps.
        skills=sorted(requirements) or ['']
        for sid in skills:
            for day,milestone,kind in zip(config['milestone_days'],('MONTH_1','MONTH_3','MONTH_6'),('ENVIRONMENT_CHECK','PIPELINE_REVIEW','WORK_TASK')):
                task(len(tasks)+1,day,milestone,kind,sid)
        if not all(t['completed_at'] for t in tasks):return
        unfinished=[t for t in tasks if t['mentor_confirmed']!='true']
        at=max(parse(t['completed_at']) for t in tasks)
        if unfinished:
            self.workforce(employee,'RAMP_UP_EXTENDED',at,unfinished[0]['evidence_ref'])
            for sid in sorted({t['related_skill_id'] for t in unfinished}):
                row=task(len(tasks)+1,(at-joined).days+config['extension_days'],'EXTENDED','FOLLOW_UP_WORK',sid)
            extensions=[t for t in tasks if t['task_type']=='FOLLOW_UP_WORK']
            if not all(t['mentor_confirmed']=='true' for t in extensions):return
            at=max(parse(t['completed_at']) for t in extensions)
        self.workforce(employee,'READY_CONFIRMED',at,compact({'work_evidence_refs':[t['evidence_ref'] for t in tasks if t['mentor_confirmed']=='true'],'gap_ids':[g['gap_id'] for g in self.data['onboarding_skill_gaps'] if g['employee_id']==employee],'human_rationale':'개인별 필요한 업무/Gap의 검증과 후속 확인을 검토하여 업무 수행 준비를 확인했다.'}))

    def run(self):
        self.plans();self.applications();self.process()
        return self.data


def generate(rules):
    return Generator(rules).run()
