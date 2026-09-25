# Mission 1 Dataset v0.3 — Sanity Report

Synthetic Dataset v0.3 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 766 |
| assessment_activities.csv | 1671 |
| activity_participants.csv | 1363 |
| assessment_evidence.csv | 3096 |
| evidence_skill_links.csv | 3096 |
| assessment_observations.csv | 6519 |
| evidence_decisions.csv | 2313 |
| skill_decision_observations.csv | 9734 |
| final_decisions.csv | 52 |
| offers.csv | 22 |
| offer_events.csv | 46 |
| onboarding_profiles.csv | 11 |
| onboarding_skill_gaps.csv | 17 |
| onboarding_tasks.csv | 63 |
| interview_capacity_events.csv | 3 |
| capacity_assignments.csv | 730 |
| workforce_events.csv | 35 |
| activity_sessions.csv | 519 |
| evaluator_reservations.csv | 1992 |
| targeted_followups.csv | 18 |
| workforce_plan.json | 1 |
| funnel_plan.json | 8 |
| talent_profile.json | 9 |

## Target vs Actual

| Bucket | Target | Actual | Difference |
|---|---:|---:|---:|
| 지원 시작 | 320 | 342 | +22 |
| 지원 완료 | 240 | 246 | +6 |
| 서류 통과 | 120 | 246 | +126 |
| 사전검증 통과 | 60 | 192 | +132 |
| 1차면접 계획 인원 | 20 | 192 | +172 |
| 2차면접 대상 | 8 | 45 | +37 |
| Offer | 5 | 22 | +17 |
| Join 목표 | 4 | 11 | +7 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Failed | Withdrawn | In Progress | Final lifecycle completed |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 246 | 0 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 246 | 217 | 192 | 25 | 9 | 20 | 0 |
| FIRST_INTERVIEW | 192 | 173 | 45 | 37 | 5 | 105 | 0 |
| SECOND_INTERVIEW | 45 | 37 | 37 | 0 | 4 | 4 | 0 |
| FINAL_REVIEW | 37 | 37 | 0 | 0 | 0 | 0 | 37 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0413 | 12.0174 | 3.0174–14.0458 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 217 | 12.0799 | 17.0618 | 6.0694–20.0764 | 29 |
| stage_lead_time / FIRST_INTERVIEW | 173 | 43.841 | 69.641 | 8.841–77.841 | 19 |
| stage_lead_time / SECOND_INTERVIEW | 37 | 15.0312 | 18.8312 | 9.0312–24.0312 | 8 |
| stage_lead_time / FINAL_REVIEW | 37 | 12.0139 | 18.4618 | 4.0174–20.059 | 0 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 246 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 192 | 36.7889 | 64.7889 | 5.7889–71.7889 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 45 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 37 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 217 | 2.0 | 5.0 | 1.0–5.0 | 29 |
| decision_time / FIRST_INTERVIEW | 173 | 3.0104 | 5.0104 | 1.0104–5.0104 | 19 |
| decision_time / SECOND_INTERVIEW | 37 | 2.0 | 5.0104 | 1.0–5.0104 | 8 |
| decision_time / FINAL_REVIEW | 37 | 9.0174 | 16.059 | 3.0208–18.066 | 0 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 217 | 2.0 | 4.0 | 0.0–4.0 | 29 |
| notification_delay / FIRST_INTERVIEW | 173 | 1.0 | 4.0 | 0.0–4.0 | 19 |
| notification_delay / SECOND_INTERVIEW | 37 | 1.0 | 4.0 | 0.0–4.0 | 8 |
| notification_delay / FINAL_REVIEW | 37 | 1.0 | 4.0 | 0.0–4.0 | 0 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 0.0, 'CALIBRATION': 98.0, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 31.5, 'FIRST_INTERVIEW_SESSION': 519.0, 'FOCUSED_FOLLOW_UP': 19.6667, 'FOLLOW_UP_CALIBRATION': 7.0, 'PRACTITIONER_QA': 0.0, 'TECHNICAL_ASSESSMENT': 0.0, 'VALUES_BEHAVIOR_INTERVIEW': 37.0}
- total_person_hours: 793.0
- first_interview_and_calibration_person_hours: 604.5
- interview_consumed_person_hours: 519.0
- first_calibration_person_hours: 85.5
- additional_person_hours: 540.0
- initial_person_hours: 60.0
- demand_person_hours: 576.0
- gap_person_hours: 516.0
- revised_person_hours: 600.0
- reserved_remaining_person_hours: 0.0
- released_reservation_person_hours: 57.0
- available_remaining_person_hours: 81.0

| Event | Hours | Demand | Effective at | Human role |
|---|---:|---:|---|---|
| INITIAL_PLAN | 60 | 0 | 2026-10-01T00:00:00+09:00 | HR_OPERATIONS_01 |
| GAP_IDENTIFIED | 516 | 576 | 2026-12-06T14:04:00+09:00 |  |
| CAPACITY_ADDED | 540 | 576 | 2026-12-08T14:04:00+09:00 | HR_OPERATIONS_01 |
- first_interview_plan_capacity_person_hours: 60
- incomplete_participation_intervals: 0

## Offer Lifecycle

- OFFERED: 22
- ACCEPTED: 13
- DECLINED: 3
- EXPIRED: 6
- PRE_JOIN_WITHDRAWAL: 2

## Offer Current State

- ACCEPTED: 11
- DECLINED: 3
- EXPIRED: 6
- PRE_JOIN_WITHDRAWAL: 2

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 11
- ready_observed: 6
- ready_by_target_date: 1
- target_date: 2027-09-01
- available_supply_at_target_fte: 13
- demand_fte: 16
- fulfillment_ratio: 0.8125
- ramp_up_extended: 7
- join_to_ready_days: {'n': 6, 'min': 183.0, 'median': 190.5, 'p90': 213.0, 'max': 216.0}

## Evidence

- assessment_evidence: 3096
- assessment_observations: 6519
- evidence_decisions: 2313
- skill_decision_observations: 9734
- final_decisions: 52

## Calibration

- AGREED: 1809
- DISAGREEMENT_REMAINS: 279
- INSUFFICIENT_EVIDENCE: 225

## Final Decision History

- PROCEED_TO_OFFER: 22
- DO_NOT_PROCEED: 15
- HOLD: 15

## Latest Final Decisions

- PROCEED_TO_OFFER: 22
- DO_NOT_PROCEED: 15

## HOLD Follow-up

- initial_proceed: 20
- initial_do_not_proceed: 2
- targeted_completed: 15
- initial: 15
- follow_up_activities: 15
- re_reviews: 15
- pending: 0
- re_review_outcomes: {'DO_NOT_PROCEED': 13, 'PROCEED_TO_OFFER': 2}

## Ready Coverage

- not_yet_ready: 5
- gap_skill_counts: {'M1_SKILL_03': 5, 'M1_SKILL_05': 6, 'M1_SKILL_06': 6}

## Validation

- WARNING REVIEW_PENDING: Synthetic rules/realism review remains pending; no freeze.
- WARNING SYNTHETIC_POLICY_ASSUMPTIONS: Source matrix, resource blocks, re-review uncertainty handling and mentor scenarios require human rule audit; not employer policies.

## Interpretation Boundary

- Target differences are not validation errors.
- Calibration counts include successive review snapshots, not unique candidates.
- All people, judgments and work artifacts are synthetic. Human rule review remains pending.
