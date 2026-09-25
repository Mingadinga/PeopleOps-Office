"""Whole-cycle resource decisions and append-only reservation accounting."""
import math
from .common import parse, stamp, plus, compact
from .schema import PROVENANCE


class Capacity:
    def __init__(self, generator):
        self.gen=generator;self.rules=generator.rules;self.cfg=self.rules['capacity']
        self.stage_panels={};self.modern='interview_model' in self.rules
        self.panels=self.cfg['initial_panels'];self.ready=parse(self.rules['observation_start']);self.cohort_at=self.ready;self.slot=0
        self.event('INITIAL_PLAN',self.cfg['initial_person_hours'],self.ready,[],0,'INITIAL_CYCLE_PLAN',rationale=(compact({'planned_candidates':self.cfg['initial_planned_candidates'],'unit_person_hours':self.cfg['planned_unit_person_hours'],'evaluator_count':self.panels*3,'initial_hours_each':self.cfg['initial_hours_per_evaluator'],'scope':'interview only, not quota'}) if self.modern else 'whole-cycle 80h; 4h per candidate is planning, not quota'))

    def event(self,kind,hours,at,cohort,demand,reason,source='',rationale=''):
        return self.gen.add('interview_capacity_events',capacity_event_id=f"CAP_{len(self.gen.data['interview_capacity_events']):04d}",stage='FIRST_INTERVIEW',event_type=kind,person_hours=hours,effective_at=stamp(at),reason_code=reason,decided_by='HR_OPERATIONS_01' if kind!='GAP_IDENTIFIED' else '',decision_provenance=PROVENANCE if kind!='GAP_IDENTIFIED' else '',cohort_application_ids=compact(cohort),demand_person_hours=demand,scope='WHOLE_CYCLE',source_event_id=source,rationale=rationale)

    def plan(self,queue):
        if not queue:return
        at=max(t for a,t in queue)
        if at>self.gen.end:return
        cohort=sorted(a['application_id'] for a,t in queue)
        demand=len(cohort)*self.cfg['planned_unit_person_hours'];gap=max(demand-self.cfg['initial_person_hours'],0)
        event=self.event('GAP_IDENTIFIED',gap,at,cohort,demand,'WHOLE_CYCLE_DEMAND',rationale='all notified PRE_ASSESSMENT advanced candidates; demand minus total initial budget')
        self.ready=at;self.cohort_at=at
        if gap:
            self.ready=plus(at,days=self.cfg['resource_decision_days'])
            if self.ready>self.gen.end:return
            if self.modern:
                n=self.panels*len(self.rules['interview_model']['first_roles'])
                unit=self.cfg['additional_hours_per_evaluator_unit']
                hours_each=math.ceil(gap/(n*unit))*unit
                self.event('CAPACITY_ADDED',n*hours_each,self.ready,cohort,demand,'ADDITIONAL_EVALUATOR_RESOURCES',event['capacity_event_id'],compact({'selected':'ADD_EVALUATOR_RESOURCES','alternatives':['EXTEND_WINDOW','REDESIGN_ASSESSMENT'],'rationale':'Fixed synthetic pool receives additional interview hours in whole one-hour allocations; no added panels','evaluator_count':n,'additional_hours_each':hours_each,'pool_panels':self.panels}))
                return
            added_panels=math.ceil(gap/self.cfg['additional_panel_person_hours']);self.panels+=added_panels
            self.event('CAPACITY_ADDED',added_panels*self.cfg['additional_panel_person_hours'],self.ready,cohort,demand,'ADDITIONAL_EVALUATOR_RESOURCES',event['capacity_event_id'],compact({'selected':'ADD_EVALUATOR_RESOURCES','alternatives':['EXTEND_WINDOW','REDESIGN_ASSESSMENT'],'rationale':'동일 평가 범위를 유지하며 추가 합성 평가자 pool 확보','added_panels':added_panels,'total_panels':self.panels}))

    def next_slot(self,earliest):
        base=parse(self.rules['process']['first_interview_calendar_start']);offsets=self.rules['process']['first_interview_weekday_offsets']
        while True:
            block,panel=divmod(self.slot,self.panels);week,position=divmod(block,len(offsets));self.slot+=1
            at=plus(base,days=7*week+offsets[position])
            if at>=max(earliest,self.ready):return at,panel+1

    def assignment(self,stage,kind,hours,at,reason,activity_id='',participant_id=''):
        if at>self.gen.end or hours<=0:return
        self.gen.add('capacity_assignments',assignment_event_id=f"ASG_{len(self.gen.data['capacity_assignments']):06d}",stage_event_id=stage['stage_event_id'],reservation_id='RSV_'+stage['stage_event_id'],event_type=kind,person_hours=round(hours,8),effective_at=stamp(at),activity_id=activity_id,participant_id=participant_id,reason_code=reason)

        if self.modern:
            from .interview import interview_ledger
            interview_ledger(self.gen,stage,kind,hours,at,reason,activity_id,participant_id)

    def close(self,stage,at,reason):
        rows=[r for r in self.gen.data['capacity_assignments'] if r['stage_event_id']==stage['stage_event_id']]
        unused=sum(float(r['person_hours'])*(1 if r['event_type']=='RESERVED' else -1) for r in rows)
        self.assignment(stage,'RELEASED',unused,at,reason)
