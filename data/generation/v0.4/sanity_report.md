# Mission 1 Dataset v0.4 — Sanity Report

Synthetic Dataset v0.4 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 794 |
| assessment_activities.csv | 1636 |
| activity_participants.csv | 1293 |
| assessment_evidence.csv | 3127 |
| evidence_skill_links.csv | 3127 |
| assessment_observations.csv | 6581 |
| evidence_decisions.csv | 2561 |
| skill_decision_observations.csv | 10918 |
| final_decisions.csv | 69 |
| offers.csv | 32 |
| offer_events.csv | 67 |
| onboarding_profiles.csv | 17 |
| onboarding_skill_gaps.csv | 29 |
| onboarding_tasks.csv | 107 |
| interview_capacity_events.csv | 3 |
| capacity_assignments.csv | 730 |
| workforce_events.csv | 54 |
| calibration_reviews.csv | 242 |
| activity_sessions.csv | 519 |
| evaluator_reservations.csv | 1728 |
| targeted_followups.csv | 21 |
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
| 2차면접 대상 | 8 | 59 | +51 |
| Offer | 5 | 32 | +27 |
| Join 목표 | 4 | 17 | +13 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Failed | Withdrawn | In Progress | Final lifecycle completed |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 246 | 0 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 246 | 217 | 192 | 25 | 9 | 20 | 0 |
| FIRST_INTERVIEW | 192 | 173 | 59 | 37 | 5 | 91 | 0 |
| SECOND_INTERVIEW | 59 | 51 | 51 | 0 | 4 | 4 | 0 |
| FINAL_REVIEW | 51 | 51 | 0 | 0 | 0 | 0 | 51 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0413 | 12.0174 | 3.0174–14.0458 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 217 | 12.0799 | 17.0618 | 6.0694–20.0764 | 29 |
| stage_lead_time / FIRST_INTERVIEW | 173 | 43.841 | 69.6326 | 8.841–77.841 | 19 |
| stage_lead_time / SECOND_INTERVIEW | 51 | 15.0208 | 20.0208 | 9.0208–24.0208 | 8 |
| stage_lead_time / FINAL_REVIEW | 51 | 11.0174 | 18.0556 | 4.0174–24.0382 | 0 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 246 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 192 | 36.7889 | 64.7889 | 5.7889–71.7889 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 59 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 51 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 217 | 2.0 | 5.0 | 1.0–5.0 | 29 |
| decision_time / FIRST_INTERVIEW | 173 | 3.0 | 5.0104 | 1.0–5.0104 | 19 |
| decision_time / SECOND_INTERVIEW | 51 | 2.0 | 5.0 | 1.0–5.0 | 8 |
| decision_time / FINAL_REVIEW | 51 | 9.0174 | 16.059 | 3.0208–20.0382 | 0 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 217 | 2.0 | 4.0 | 0.0–4.0 | 29 |
| notification_delay / FIRST_INTERVIEW | 173 | 1.0 | 4.0 | 0.0–4.0 | 19 |
| notification_delay / SECOND_INTERVIEW | 51 | 1.0 | 4.0 | 0.0–4.0 | 8 |
| notification_delay / FINAL_REVIEW | 51 | 2.0 | 4.0 | 0.0–4.0 | 0 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 0.0, 'CALIBRATION': 67.0, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 42.6667, 'FIRST_INTERVIEW_SESSION': 519.0, 'FOCUSED_FOLLOW_UP': 23.3333, 'FOLLOW_UP_CALIBRATION': 5.0, 'PRACTITIONER_QA': 0.0, 'TECHNICAL_ASSESSMENT': 0.0, 'VALUES_BEHAVIOR_INTERVIEW': 51.0}
- total_person_hours: 788.8333
- first_interview_and_calibration_person_hours: 583.0
- interview_consumed_person_hours: 519.0
- first_calibration_person_hours: 64.0
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

- OFFERED: 32
- ACCEPTED: 20
- DECLINED: 4
- EXPIRED: 8
- PRE_JOIN_WITHDRAWAL: 3

## Offer Current State

- ACCEPTED: 17
- DECLINED: 4
- EXPIRED: 8
- PRE_JOIN_WITHDRAWAL: 3

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 17
- ready_observed: 8
- ready_by_target_date: 1
- target_date: 2027-09-01
- available_supply_at_target_fte: 13
- demand_fte: 16
- fulfillment_ratio: 0.8125
- ramp_up_extended: 12
- join_to_ready_days: {'n': 8, 'min': 183.0, 'median': 194.0, 'p90': 220.5, 'max': 231.0}

## Evidence

- assessment_evidence: 3127
- assessment_observations: 6581
- evidence_decisions: 2561
- skill_decision_observations: 10918
- final_decisions: 69

## Calibration

- AGREED: 2039
- DISAGREEMENT_REMAINS: 286
- INSUFFICIENT_EVIDENCE: 236

## Calibration Activities

- eligible: 242
- triggered: 144
- actual: 144
- person_hours: 72.0

## Final Decision History

- PROCEED_TO_OFFER: 32
- DO_NOT_PROCEED: 19
- HOLD: 18

## Latest Final Decisions

- PROCEED_TO_OFFER: 32
- DO_NOT_PROCEED: 19

## HOLD Follow-up

- initial_proceed: 31
- initial_do_not_proceed: 2
- targeted_completed: 18
- initial: 18
- follow_up_activities: 18
- re_reviews: 18
- pending: 0
- re_review_outcomes: {'DO_NOT_PROCEED': 17, 'PROCEED_TO_OFFER': 1}

## Ready Coverage

- not_yet_ready: 9
- gap_skill_counts: {'M1_SKILL_03': 9, 'M1_SKILL_05': 11, 'M1_SKILL_06': 9}

## Validation

- WARNING REVIEW_PENDING: Synthetic rules/realism review remains pending; no freeze.
- WARNING SYNTHETIC_POLICY_ASSUMPTIONS: Source matrix, resource blocks, re-review uncertainty handling and mentor scenarios require human rule audit; not employer policies.

## Interpretation Boundary

- Target differences are not validation errors.
- Calibration counts include successive review snapshots, not unique candidates.
- All people, judgments and work artifacts are synthetic. Human rule review remains pending.
