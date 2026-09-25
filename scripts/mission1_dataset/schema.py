"""Executable serialization contract for docs/09. Empty CSV cells represent NULL."""
PROVENANCE = 'SYNTHETIC_HUMAN_SCENARIO'
STAGES = ('DOCUMENT_SCREEN', 'PRE_ASSESSMENT', 'FIRST_INTERVIEW', 'SECOND_INTERVIEW', 'FINAL_REVIEW')
LEVELS = ('NOT_OBSERVED', 'LIMITED', 'MODERATE', 'STRONG')
RESULTS = ('ADVANCED', 'FAILED', 'WITHDRAWN', 'IN_PROGRESS', 'CLOSED', 'CONDITIONAL_ADVANCE')
ACTIVITIES = {
    'DOCUMENT_SCREEN': ('DOCUMENT_REVIEW',),
    'PRE_ASSESSMENT': ('APTITUDE', 'CODING_TEST'),
    'FIRST_INTERVIEW': ('FIRST_INTERVIEW_SESSION', 'TECHNICAL_ASSESSMENT', 'AI_CASE', 'PRACTITIONER_QA', 'CALIBRATION'),
    'SECOND_INTERVIEW': ('VALUES_BEHAVIOR_INTERVIEW','CALIBRATION'),
    'FINAL_REVIEW': ('FINAL_REVIEW_DISCUSSION', 'FOCUSED_FOLLOW_UP', 'FOLLOW_UP_CALIBRATION'),
}
SCHEMA = {
    'applications': 'application_id candidate_id job_id source_channel started_at submitted_at application_status',
    'stage_history': 'stage_event_id application_id candidate_id stage entered_at invited_at scheduled_at completed_at decision_at notified_at withdrawn_at result decision_reason_code withdrawal_reason_code decision_provenance rationale',
    'assessment_activities': 'activity_id stage_event_id application_id candidate_id activity_type started_at completed_at activity_status',
    'activity_participants': 'activity_id participant_id participant_role participation_started_at participation_ended_at',
    'assessment_evidence': 'evidence_id activity_id application_id candidate_id source_type verification_mode context_id source_ref raw_evidence created_at',
    'evidence_skill_links': 'link_id evidence_id suggested_skill_id suggestion_source confirmed_skill_id confirmation_status confirmed_by confirmed_at decision_provenance',
    'assessment_observations': 'observation_id evidence_id application_id candidate_id evaluator_id evaluator_role skill_id rubric_id observation_text proposed_level explicit_limitation created_at decision_provenance',
    'evidence_decisions': 'decision_id application_id candidate_id skill_id final_level decision_status rationale decided_by decided_at decision_provenance rubric_id',
    'skill_decision_observations': 'decision_id observation_id',
    'final_decisions': 'final_decision_id review_round hold_reason_code resolution_plan follow_up_activity_id application_id candidate_id must_evidence_status remaining_uncertainty learnable_gap_summary decision rationale decided_by decided_at decision_provenance',
    'offers': 'offer_id application_id candidate_id offered_at expected_join_at response_deadline',
    'offer_events': 'offer_event_id offer_id event_type occurred_at reason_code',
    'onboarding_profiles': 'employee_id source_candidate_id joined_at onboarding_started_at planned_ready_at',
    'onboarding_skill_gaps': 'gap_id employee_id skill_id gap_level gap_source source_evidence_id final_decision_id requirement_ref rationale confirmed_by confirmed_at decision_provenance',
    'onboarding_tasks': 'task_id candidate_id employee_id milestone task_type related_skill_id planned_at assigned_at completed_at evidence_ref work_evidence status mentor_confirmed decision_provenance',
    'interview_capacity_events': 'capacity_event_id stage event_type person_hours effective_at reason_code decided_by decision_provenance cohort_application_ids demand_person_hours scope source_event_id rationale',
    'capacity_assignments': 'assignment_event_id stage_event_id reservation_id event_type person_hours effective_at activity_id participant_id reason_code',
    'workforce_events': 'workforce_event_id employee_id event_type effective_at source_ref confirmed_by confirmed_at decision_provenance',
}
SCHEMA.update({
 'calibration_reviews':'review_id stage_event_id review_round evaluated_at observation_ids trigger_codes activity_id rationale',
 'activity_sessions':'activity_id session_activity_id',
 'evaluator_reservations':'allocation_id stage_event_id activity_id participant_id purpose event_type person_hours effective_at reason_code',
 'targeted_followups':'evidence_id hold_decision_id skill_id hold_reason question existing_evidence_ids existing_observation_ids response_kind',
})
OPTIONAL_TABLES = {'application_eligibility', 'application_experiences', 'eligibility_verifications'}
SCHEMA.update({
 'eligibility_verifications': 'verification_id application_id candidate_id eligibility_id requirement previous_status verification_requested_at verification_deadline verification_result verified_at resolved_at resulting_status verification_evidence confirmed_by decision_provenance rationale',
 'application_eligibility': 'eligibility_id application_id candidate_id degree_level graduation_status expected_graduation_date language_test_type language_test_valid_until travel_visa_eligibility military_requirement_applicable military_requirement_status eligibility_reference_date expected_join_date requirement_states overall_state public_source_ref source_provenance date_provenance decision_provenance',
 'application_experiences': 'experience_id application_id candidate_id experience_type ownership actions evidence_categories evidence_refs recorded_at decision_provenance',
})
SCHEMA = {k: v.split() for k, v in SCHEMA.items()}
KEYS = {name: (fields[0],) for name, fields in SCHEMA.items()}
KEYS['skill_decision_observations'] = ('decision_id', 'observation_id')
KEYS['activity_participants'] = ('activity_id', 'participant_id', 'participation_started_at')
NULLABLE = {
    'eligibility_verifications': {'verified_at','resolved_at','confirmed_by'},
    'application_eligibility': {'expected_graduation_date','language_test_valid_until'},
    'calibration_reviews': {'activity_id'},
    'evaluator_reservations': {'activity_id'},
    'applications': {'submitted_at'},
    'stage_history': {'result','invited_at','scheduled_at','completed_at','decision_at','notified_at','withdrawn_at','decision_reason_code','withdrawal_reason_code','decision_provenance','rationale'},
    'assessment_activities': {'started_at','completed_at'},
    'activity_participants': {'participation_ended_at'},
    'assessment_evidence': {'activity_id'},
    'evidence_skill_links': {'suggested_skill_id','suggestion_source','confirmed_skill_id','confirmed_by','confirmed_at','decision_provenance'},
    'evidence_decisions': {'final_level'},
    'final_decisions': {'remaining_uncertainty','learnable_gap_summary','hold_reason_code','resolution_plan','follow_up_activity_id'},
    'offers': {'expected_join_at'},
    'offer_events': {'reason_code'},
    'onboarding_tasks': {'related_skill_id','assigned_at','completed_at','evidence_ref','work_evidence','decision_provenance'},
    'workforce_events': {'decision_provenance','confirmed_by','confirmed_at'},
    'onboarding_skill_gaps': {'source_evidence_id'},
    'capacity_assignments': {'activity_id','participant_id'},
    'interview_capacity_events': {'decided_by','decision_provenance','source_event_id'},
}
ENUMS = {
    ('applications','application_status'): ('STARTED','SUBMITTED','ABANDONED'),
    ('applications','source_channel'): ('CAREER_SITE','TECH_COMMUNITY','CAMPUS','RECRUITING_EVENT'),
    ('stage_history','stage'): STAGES,
    ('stage_history','result'): RESULTS,
    ('stage_history','decision_reason_code'): ('EVIDENCE_CANDIDATES_FOUND','BASIC_REQUIREMENT_VIOLATION','PRE_TASK_COMPLETE','DIRECT_TASK_LIMITATION','FIRST_EVIDENCE_REVIEWED','CORE_DIRECT_LIMITATION','EVIDENCE_PENDING','REPEATED_MUST_LIMITATION','BEHAVIOR_REVIEWED','BEHAVIOR_LIMITATION','ADDITIONAL_EVIDENCE_REQUIRED','FINAL_REVIEW_COMPLETE'),
    ('stage_history','withdrawal_reason_code'): ('UNKNOWN',),
    ('assessment_activities','activity_type'): tuple(a for activities in ACTIVITIES.values() for a in activities),
    ('assessment_activities','activity_status'): ('PLANNED','IN_PROGRESS','COMPLETED','CANCELLED'),
    ('activity_participants','participant_role'): ('ML_ENGINEER','HIRING_MANAGER','TECHNICAL_REVIEWER','RECRUITER'),
    ('assessment_evidence','source_type'): ('APPLICATION_RESPONSE','CODING_TEST_RESPONSE','TECHNICAL_ASSESSMENT_RESPONSE','AI_CASE_RESPONSE','INTERVIEW_RESPONSE'),
    ('evidence_skill_links','suggestion_source'): ('SYSTEM','HUMAN'),
    ('evidence_skill_links','confirmation_status'): ('PENDING','CONFIRMED','MODIFIED','REJECTED'),
    ('assessment_observations','evaluator_role'): ('ML_ENGINEER','HIRING_MANAGER','TECHNICAL_REVIEWER','RECRUITER'),
    ('assessment_observations','proposed_level'): LEVELS,
    ('evidence_decisions','final_level'): LEVELS,
    ('evidence_decisions','decision_status'): ('AGREED','DISAGREEMENT_REMAINS','INSUFFICIENT_EVIDENCE'),
    ('final_decisions','must_evidence_status'): ('COVERED','UNRESOLVED','REPEATED_LIMITATION'),
    ('final_decisions','decision'): ('PROCEED_TO_OFFER','DO_NOT_PROCEED','HOLD'),
    ('offer_events','event_type'): ('OFFERED','ACCEPTED','DECLINED','EXPIRED','PRE_JOIN_WITHDRAWAL'),
    ('offer_events','reason_code'): ('UNKNOWN','NO_RESPONSE'),
    ('onboarding_skill_gaps','gap_level'): ('DEVELOPMENT_REQUIRED','RECONFIRM_AT_WORK'),
    ('onboarding_skill_gaps','gap_source'): ('SELECTION_EVIDENCE','POST_JOIN_ASSESSMENT','MENTOR_OBSERVATION'),
    ('onboarding_tasks','milestone'): ('MONTH_1','MONTH_3','MONTH_6','EXTENDED'),
    ('onboarding_tasks','task_type'): ('ENVIRONMENT_CHECK','PIPELINE_REVIEW','WORK_TASK','FOLLOW_UP_WORK'),
    ('onboarding_tasks','status'): ('PLANNED','IN_PROGRESS','COMPLETED','DELAYED','CANCELLED'),
    ('onboarding_tasks','mentor_confirmed'): ('true','false'),
    ('workforce_events','event_type'): ('JOINED','ONBOARDING_STARTED','READY_CONFIRMED','RAMP_UP_EXTENDED'),
}
FORBIDDEN = {'candidate_ability','ability_score','hidden_score','aggregate_candidate_quality','aggregate_candidate_score','total_candidate_score','ai_fit_score','fit_score','culture_fit_score','candidate_rank','candidate_ranking','pass_probability','performance_probability','turnover_probability','success_probability','performance_prediction','turnover_prediction','representative','representative_flag','display_id','gender','age','race','religion','disability','marital_status','photo','school_name','real_name'}
PLAN_FILES = ('workforce_plan','funnel_plan','talent_profile')

ENUMS.update({
 ('calibration_reviews','review_round'):('INTERVIEW','FOLLOW_UP'),
 ('evaluator_reservations','purpose'):('INTERVIEW','CALIBRATION'),
 ('evaluator_reservations','event_type'):('RESERVED','CONSUMED','RELEASED'),
 ('assessment_evidence','verification_mode'): ('SELF_REPORTED','DIRECT_TASK','DIRECT_INTERACTION','BEHAVIORAL_INTERACTION'),
 ('assessment_observations','explicit_limitation'): ('true','false'),
 ('final_decisions','review_round'): ('INITIAL','RE_REVIEW'),
 ('final_decisions','hold_reason_code'): ('MISSING_EVIDENCE','UNRESOLVED_EVIDENCE','EVALUATOR_DISAGREEMENT'),
 ('capacity_assignments','event_type'): ('RESERVED','RELEASED','CONSUMED'),
 ('interview_capacity_events','stage'): ('FIRST_INTERVIEW',),
 ('interview_capacity_events','event_type'): ('INITIAL_PLAN','GAP_IDENTIFIED','CAPACITY_ADDED','CAPACITY_RELEASED'),
 ('interview_capacity_events','scope'): ('WHOLE_CYCLE',),
})

ENUMS[('stage_history','decision_reason_code')] += ('APPLICATION_EVIDENCE_CANDIDATE','INSUFFICIENT_APPLICATION_EVIDENCE','ELIGIBILITY_CONFIRMATION_REQUIRED')
