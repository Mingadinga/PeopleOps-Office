# Mission 1 Dataset v0.2 — Sanity Report

Synthetic Dataset v0.2 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 1001 |
| assessment_activities.csv | 1874 |
| activity_participants.csv | 2634 |
| assessment_evidence.csv | 3456 |
| evidence_skill_links.csv | 3456 |
| assessment_observations.csv | 6912 |
| evidence_decisions.csv | 4785 |
| skill_decision_observations.csv | 19472 |
| final_decisions.csv | 251 |
| offers.csv | 86 |
| offer_events.csv | 178 |
| onboarding_profiles.csv | 56 |
| onboarding_skill_gaps.csv | 90 |
| onboarding_tasks.csv | 351 |
| interview_capacity_events.csv | 3 |
| capacity_assignments.csv | 1765 |
| workforce_events.csv | 189 |
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
| 2차면접 대상 | 8 | 170 | +162 |
| Offer | 5 | 86 | +81 |
| Join 목표 | 4 | 56 | +52 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Failed | Withdrawn | In Progress | Final lifecycle completed |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 246 | 0 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 246 | 217 | 192 | 25 | 9 | 20 | 0 |
| FIRST_INTERVIEW | 192 | 173 | 170 | 3 | 5 | 14 | 0 |
| SECOND_INTERVIEW | 170 | 147 | 147 | 0 | 13 | 10 | 0 |
| FINAL_REVIEW | 147 | 147 | 0 | 0 | 0 | 0 | 147 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0413 | 12.0174 | 3.0174–14.0458 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 217 | 12.0799 | 17.0618 | 6.0694–20.0764 | 29 |
| stage_lead_time / FIRST_INTERVIEW | 173 | 43.8653 | 71.8576 | 9.8549–79.8653 | 19 |
| stage_lead_time / SECOND_INTERVIEW | 147 | 16.0278 | 20.4757 | 9.0521–24.0278 | 23 |
| stage_lead_time / FINAL_REVIEW | 147 | 15.066 | 20.059 | 4.0208–24.1111 | 0 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 246 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 192 | 36.7889 | 64.7889 | 5.7889–71.7889 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 170 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 147 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 217 | 2.0 | 5.0 | 1.0–5.0 | 29 |
| decision_time / FIRST_INTERVIEW | 173 | 2.0174 | 5.0139 | 1.0104–5.0174 | 19 |
| decision_time / SECOND_INTERVIEW | 147 | 2.0 | 5.0 | 1.0–5.0 | 23 |
| decision_time / FINAL_REVIEW | 147 | 13.0972 | 18.0618 | 3.0208–20.1111 | 0 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 217 | 2.0 | 4.0 | 0.0–4.0 | 29 |
| notification_delay / FIRST_INTERVIEW | 173 | 1.0 | 4.0 | 0.0–4.0 | 19 |
| notification_delay / SECOND_INTERVIEW | 147 | 1.0 | 4.0 | 0.0–4.0 | 23 |
| notification_delay / FINAL_REVIEW | 147 | 1.0 | 4.0 | 0.0–4.0 | 0 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 171.8333, 'CALIBRATION': 116.5, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 122.1667, 'FOCUSED_FOLLOW_UP': 137.6667, 'FOLLOW_UP_CALIBRATION': 71.8333, 'PRACTITIONER_QA': 128.8333, 'TECHNICAL_ASSESSMENT': 173.1667, 'VALUES_BEHAVIOR_INTERVIEW': 245.3333}
- total_person_hours: 1248.1667
- first_interview_and_calibration_person_hours: 590.3333
- initial_person_hours: 80.0
- demand_person_hours: 768.0
- gap_person_hours: 688.0
- revised_person_hours: 800.0
- reserved_remaining_person_hours: 0.0
- released_reservation_person_hours: 177.6667
- available_remaining_person_hours: 209.6667

| Event | Hours | Demand | Effective at | Human role |
|---|---:|---:|---|---|
| INITIAL_PLAN | 80 | 0 | 2026-10-01T00:00:00+09:00 | HR_OPERATIONS_01 |
| GAP_IDENTIFIED | 688 | 768 | 2026-12-06T14:04:00+09:00 |  |
| CAPACITY_ADDED | 720 | 768 | 2026-12-08T14:04:00+09:00 | HR_OPERATIONS_01 |
- first_interview_plan_capacity_person_hours: 80
- incomplete_participation_intervals: 0

## Offer Lifecycle

- OFFERED: 86
- ACCEPTED: 62
- DECLINED: 11
- EXPIRED: 13
- PRE_JOIN_WITHDRAWAL: 6

## Offer Current State

- ACCEPTED: 56
- DECLINED: 11
- EXPIRED: 13
- PRE_JOIN_WITHDRAWAL: 6

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 56
- ready_observed: 30
- ready_by_target_date: 2
- target_date: 2027-09-01
- available_supply_at_target_fte: 14
- demand_fte: 16
- fulfillment_ratio: 0.875
- ramp_up_extended: 47
- join_to_ready_days: {'n': 30, 'min': 180.0, 'median': 217.0, 'p90': 231.0, 'max': 238.0}

## Evidence

- assessment_evidence: 3456
- assessment_observations: 6912
- evidence_decisions: 4785
- skill_decision_observations: 19472
- final_decisions: 251

## Calibration

- AGREED: 3760
- DISAGREEMENT_REMAINS: 592
- INSUFFICIENT_EVIDENCE: 433

## Final Decision History

- PROCEED_TO_OFFER: 86
- DO_NOT_PROCEED: 61
- HOLD: 104

## Latest Final Decisions

- DO_NOT_PROCEED: 61
- PROCEED_TO_OFFER: 86

## HOLD Follow-up

- initial: 104
- follow_up_activities: 104
- re_reviews: 104
- pending: 0
- re_review_outcomes: {'PROCEED_TO_OFFER': 48, 'DO_NOT_PROCEED': 56}

## Ready Coverage

- not_yet_ready: 26
- gap_skill_counts: {'M1_SKILL_06': 22, 'M1_SKILL_03': 37, 'M1_SKILL_05': 30, 'M1_SKILL_02': 1}

## Validation

- WARNING REVIEW_PENDING: Synthetic rules/realism review remains pending; no freeze.
- WARNING SYNTHETIC_POLICY_ASSUMPTIONS: Source matrix, resource blocks, re-review uncertainty handling and mentor scenarios require human rule audit; not employer policies.

## Interpretation Boundary

- Target differences are not validation errors.
- Calibration counts include successive review snapshots, not unique candidates.
- All people, judgments and work artifacts are synthetic. Human rule review remains pending.
