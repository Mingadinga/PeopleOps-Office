"""Isolated test fixtures never change the canonical review outputs."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.mission1_dataset.common import load_rules, read_data, write_data, file_hashes, parse, stamp, plus
from scripts.mission1_dataset.generate import generate, Generator
from scripts.mission1_dataset.validate import validate, validate_manifest
from scripts.mission1_dataset.report import summarize, distribution
from scripts.mission1_dataset.evidence import interpret, calibrate
from scripts.mission1_dataset.schema import SCHEMA, OPTIONAL_TABLES


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=load_rules(__import__('pathlib').Path(__file__).resolve().parents[1]/'data/generation/v0.2/generation_rules.json')
        cls.base=generate(cls.rules)
        cls.valid=validate(cls.base,cls.rules)

    def corrupt(self, mutate, code):
        data=copy.deepcopy(self.base);mutate(data)
        result=validate(data,self.rules)
        self.assertEqual(result['status'],'ERROR')
        self.assertIn(code,{e['code'] for e in result['errors']},result['errors'][:4])

    def test_generated_data_and_csv_roundtrip(self):
        self.assertEqual(self.valid['errors'],[])
        with tempfile.TemporaryDirectory() as directory:
            write_data(directory,self.base)
            loaded=read_data(directory)
            self.assertEqual(validate(loaded,self.rules)['errors'],[])
            self.assertEqual(set(SCHEMA)-OPTIONAL_TABLES,{p.stem for p in Path(directory).glob('*.csv')})

    def test_identical_input_produces_identical_bytes(self):
        again=generate(copy.deepcopy(self.rules))
        with tempfile.TemporaryDirectory() as first,tempfile.TemporaryDirectory() as second:
            write_data(first,self.base);write_data(second,again)
            self.assertEqual(file_hashes(first),file_hashes(second))

    def test_channel_is_not_an_evidence_or_decision_input(self):
        rules=copy.deepcopy(self.rules);rules['applications']['channel_options']=['CAMPUS']
        changed=generate(rules)
        for table in SCHEMA:
            if table!='applications':self.assertEqual(self.base[table],changed[table],table)

    def test_target_is_not_a_quota_or_generation_control(self):
        rules=copy.deepcopy(self.rules)
        for row in rules['funnel_targets']:row[2]+=11
        changed=generate(rules)
        for table in SCHEMA:self.assertEqual(self.base[table],changed[table],table)

    def test_seed_changes_artifacts(self):
        rules=copy.deepcopy(self.rules);rules['seed']+=1
        self.assertNotEqual(self.base['assessment_evidence'],generate(rules)['assessment_evidence'])

    def test_missing_column_is_rejected(self):
        self.corrupt(lambda d:d['applications'][0].pop('job_id'),'schema')

    def test_duplicate_primary_key_is_rejected(self):
        self.corrupt(lambda d:d['applications'].append(copy.deepcopy(d['applications'][0])),'primary_key')

    def test_unknown_enum_is_rejected(self):
        self.corrupt(lambda d:d['stage_history'][0].update(result='PASS'),'enum')

    def test_naive_timestamp_is_rejected(self):
        self.corrupt(lambda d:d['applications'][0].update(started_at='2026-10-12T09:00:00'),'timestamp')

    def test_time_outside_window_is_rejected(self):
        self.corrupt(lambda d:d['applications'][0].update(started_at='2020-01-01T09:00:00+09:00'),'observation_window')

    def test_reversed_time_is_rejected(self):
        self.corrupt(lambda d:next(r for r in d['applications'] if r['submitted_at']).update(submitted_at='2026-10-02T09:00:00+09:00'),'temporal')

    def test_orphan_activity_is_rejected(self):
        self.corrupt(lambda d:d['assessment_activities'][0].update(stage_event_id='MISSING'),'foreign_key')

    def test_wrong_candidate_evidence_is_rejected(self):
        self.corrupt(lambda d:d['assessment_evidence'][0].update(candidate_id='C0342'),'candidate_relation')

    def test_foreign_skill_source_is_rejected(self):
        def mutate(data):
            row=data['skill_decision_observations'][0];decision=data['evidence_decisions'][0]
            other=next(e for e in data['assessment_observations'] if e['candidate_id']!=decision['candidate_id'])
            row['observation_id']=other['observation_id']
        self.corrupt(mutate,'decision_relation')

    def test_decision_without_sources_is_rejected(self):
        def mutate(data):
            did=data['evidence_decisions'][0]['decision_id']
            data['skill_decision_observations']=[r for r in data['skill_decision_observations'] if r['decision_id']!=did]
        self.corrupt(mutate,'decision_relation')

    def test_forbidden_hidden_field_is_rejected(self):
        def mutate(data):
            row=data['assessment_evidence'][0];raw=json.loads(row['raw_evidence']);raw['candidate_ability']=.8
            row['raw_evidence']=json.dumps(raw)
        self.corrupt(mutate,'forbidden')

    def test_missing_synthetic_provenance_is_rejected(self):
        self.corrupt(lambda d:d['assessment_observations'][0].update(decision_provenance='PUBLIC'),'provenance')

    def test_withdrawal_must_have_confirmation_time(self):
        self.corrupt(lambda d:next(r for r in d['stage_history'] if r['result']=='WITHDRAWN').update(withdrawn_at=''),'withdrawal')

    def test_final_decision_cannot_ignore_trace(self):
        self.corrupt(lambda d:next(r for r in d['final_decisions'] if r['decision']=='HOLD').update(decision='PROCEED_TO_OFFER'),'final_decision')

    def test_join_is_not_offer_event(self):
        self.corrupt(lambda d:d['offer_events'][0].update(event_type='JOINED'),'enum')

    def test_actual_counts_candidates_not_activities(self):
        report=summarize(self.base,self.rules,self.valid)
        first=report['stage_outcomes']['FIRST_INTERVIEW']['ENTERED']
        self.assertEqual(first,len({r['candidate_id'] for r in self.base['stage_history'] if r['stage']=='FIRST_INTERVIEW'}))
        self.assertGreater(len([r for r in self.base['assessment_activities'] if r['activity_type'] in ('AI_CASE','TECHNICAL_ASSESSMENT','PRACTITIONER_QA')]),first)
        for stage,out in report['stage_outcomes'].items():
            self.assertEqual(out['ENTERED'],sum(out[k] for k in ('ADVANCED','FAILED','WITHDRAWN','IN_PROGRESS'))+out.get('FINAL_REVIEW_COMPLETED',0))

    def test_null_duration_is_not_zero(self):
        report=summarize(self.base,self.rules,self.valid)
        row=report['time_distributions']['scheduling_wait']['DOCUMENT_SCREEN']
        self.assertEqual(row['n'],0);self.assertIsNone(row['median'])
        self.assertIsNone(distribution([])['median'])

    def test_percentiles_are_ordered_for_small_samples(self):
        values=distribution([1,7])
        self.assertEqual(values['median'],4)
        self.assertAlmostEqual(values['p90'],6.4)

    def test_explained_disagreement_and_missing_are_distinct(self):
        ambiguous={'action':'팀 구현','ownership':'TEAM_UNCLEAR','verification':'팀 검증','revision':''}
        self.assertEqual(interpret(ambiguous,'ML_ENGINEER')[0],'LIMITED')
        self.assertEqual(interpret(ambiguous,'HIRING_MANAGER')[0],'MODERATE')
        evidence={'e':{'verification_mode':'DIRECT_TASK','context_id':'c'}}
        observations=[{'evidence_id':'e','observation_id':'o1','proposed_level':'LIMITED'}, {'evidence_id':'e','observation_id':'o2','proposed_level':'MODERATE'}]
        self.assertEqual(calibrate(observations,evidence)[:2],('','DISAGREEMENT_REMAINS'))
        for o in observations:o['proposed_level']='NOT_OBSERVED'
        self.assertEqual(calibrate(observations,evidence)[:2],('','INSUFFICIENT_EVIDENCE'))

    def onboarding_fixture(self,work):
        # Branch fixture only. Never persists or changes canonical generation rules.
        rules=copy.deepcopy(self.rules);rules['observation_end']='2028-12-31T23:59:59+09:00'
        rules['onboarding']['work_records']=[work]
        rules['onboarding']['mentor_reviews']=['CONFIRM']
        return generate(rules),rules

    def test_join_and_ready_require_verified_work(self):
        data,rules=self.onboarding_fixture('VERIFIED')
        self.assertEqual(validate(data,rules)['errors'],[])
        report=summarize(data,rules,validate(data,rules))
        self.assertGreater(report['workforce']['joined'],0)
        eligible={p['employee_id'] for p in data['onboarding_profiles'] if plus(parse(p['planned_ready_at']),days=14)<=parse(rules['observation_end'])}
        ready_ids={e['employee_id'] for e in data['workforce_events'] if e['event_type']=='READY_CONFIRMED'}
        self.assertTrue(eligible <= ready_ids)
        self.assertGreater(len(ready_ids),0)
        ready=next(r for r in data['workforce_events'] if r['event_type']=='READY_CONFIRMED')
        ready['source_ref']=json.dumps({'work_evidence_refs':['onboarding_tasks.csv#MISSING/work_evidence'],'gap_ids':[],'human_rationale':'invalid fixture'})
        self.assertIn('work_evidence',{e['code'] for e in validate(data,rules)['errors']})

    def test_six_months_alone_does_not_mean_ready(self):
        data,rules=self.onboarding_fixture('CHECK_PENDING')
        self.assertEqual(validate(data,rules)['errors'],[])
        kinds=[r['event_type'] for r in data['workforce_events']]
        self.assertIn('RAMP_UP_EXTENDED',kinds);self.assertNotIn('READY_CONFIRMED',kinds)

    def test_false_stage_rejection_is_rejected(self):
        self.corrupt(lambda d:d['stage_history'][0].update(result='FAILED',decision_reason_code='REPEATED_MUST_LIMITATION'),'stage_lifecycle')

    def test_overlapping_participant_time_is_rejected(self):
        def mutate(data):
            row=copy.deepcopy(data['activity_participants'][0])
            row['participation_started_at']=stamp(plus(parse(row['participation_started_at']),minutes=1))
            data['activity_participants'].append(row)
        self.corrupt(mutate,'participant_time')

    def test_invalid_plan_type_returns_error_not_exception(self):
        self.corrupt(lambda d:d['workforce_plan'].update(current_fte='twelve'),'plan_value')

    def test_manifest_detects_data_tampering(self):
        import hashlib
        from scripts.mission1_dataset.common import DEFAULT_RULES
        import scripts.mission1_dataset.validate as validation_module
        with tempfile.TemporaryDirectory() as directory:
            write_data(directory,self.base)
            manifest={k:self.rules[k] for k in ('dataset_version','generation_version','generation_rules_version','schema_version','seed','generated_at','observation_start','observation_end','timezone','case_id','job_id')}
            manifest.update(record_counts={n+'.csv':len(self.base[n]) for n in SCHEMA if n not in OPTIONAL_TABLES},file_sha256=file_hashes(directory),
                            generation_rules_sha256=hashlib.sha256(DEFAULT_RULES.read_bytes()).hexdigest(),
                            generator_source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(validation_module.__file__).parent.glob('*.py'))},
                            review_status='UNREVIEWED',frozen=False,implementation_parameters=self.rules['implementation_parameters'],random_stream_version=self.rules['random_stream_version'],source_matrix=self.rules['source_matrix'],capacity_parameters=self.rules['capacity'],response_window_days=self.rules['offers']['response_window_days'])
            manifest['record_counts'].update({n+'.json':len(self.base[n]) if isinstance(self.base[n],list) else 1 for n in ('workforce_plan','funnel_plan','talent_profile')})
            self.assertEqual(validate_manifest(manifest,self.base,self.rules,directory,DEFAULT_RULES),[])
            target=Path(directory)/'offers.csv';target.write_text(target.read_text()+'\n')
            self.assertTrue(validate_manifest(manifest,self.base,self.rules,directory,DEFAULT_RULES))

    def test_frozen_or_presentation_output_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ('synthetic/v1','presentation','generated/v0.1'):
                with self.assertRaises(ValueError):write_data(Path(directory)/name,self.base)


if __name__=='__main__':unittest.main()
