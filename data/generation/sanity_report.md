# Mission 1 Dataset v0.1 — Sanity Report

Synthetic Dataset v0.1 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 842 |
| assessment_activities.csv | 1562 |
| activity_participants.csv | 1190 |
| assessment_evidence.csv | 3773 |
| evidence_skill_links.csv | 3771 |
| assessment_observations.csv | 7542 |
| evidence_decisions.csv | 6084 |
| evidence_decision_sources.csv | 9545 |
| final_decisions.csv | 61 |
| offers.csv | 2 |
| offer_events.csv | 4 |
| onboarding_profiles.csv | 0 |
| onboarding_skill_gaps.csv | 0 |
| onboarding_tasks.csv | 0 |
| workforce_events.csv | 0 |
| workforce_plan.json | 1 |
| funnel_plan.json | 8 |
| talent_profile.json | 9 |

## Target vs Actual

| Bucket | Target | Actual | Difference |
|---|---:|---:|---:|
| 지원 시작 | 320 | 342 | +22 |
| 지원 완료 | 240 | 246 | +6 |
| 서류 통과 | 120 | 246 | +126 |
| 사전검증 통과 | 60 | 205 | +145 |
| 1차면접 대상 | 20 | 205 | +185 |
| 2차면접 대상 | 8 | 81 | +73 |
| Offer | 5 | 2 | -3 |
| Join 목표 | 4 | 0 | -4 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Failed | Withdrawn | In Progress |
|---|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 246 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 246 | 217 | 205 | 12 | 9 | 20 |
| FIRST_INTERVIEW | 205 | 86 | 83 | 3 | 5 | 114 |
| SECOND_INTERVIEW | 81 | 67 | 64 | 2 | 7 | 8 |
| FINAL_REVIEW | 64 | 64 | 2 | 0 | 0 | 62 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0174 | 12.0174 | 3.0104–14.0174 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 217 | 12.0799 | 17.0618 | 6.0694–20.0764 | 29 |
| stage_lead_time / FIRST_INTERVIEW | 84 | 198.7517 | 318.0511 | 39.7764–344.7368 | 121 |
| stage_lead_time / SECOND_INTERVIEW | 66 | 16.0347 | 20.5312 | 9.0347–22.0417 | 15 |
| stage_lead_time / FINAL_REVIEW | 2 | 10.0208 | 12.4208 | 7.0208–13.0208 | 62 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 246 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 205 | 376.7243 | 651.2335 | 37.7174–713.7889 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 81 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 64 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 217 | 2.0 | 5.0 | 1.0–5.0 | 29 |
| decision_time / FIRST_INTERVIEW | 86 | 2.0174 | 5.0139 | 1.0104–5.0174 | 119 |
| decision_time / SECOND_INTERVIEW | 66 | 2.0 | 5.0 | 1.0–5.0 | 15 |
| decision_time / FINAL_REVIEW | 61 | 7.0208 | 10.0174 | 3.0174–12.0208 | 3 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 217 | 2.0 | 4.0 | 0.0–4.0 | 29 |
| notification_delay / FIRST_INTERVIEW | 84 | 1.0 | 4.0 | 0.0–4.0 | 121 |
| notification_delay / SECOND_INTERVIEW | 66 | 1.0 | 4.0 | 0.0–4.0 | 15 |
| notification_delay / FINAL_REVIEW | 2 | 1.5 | 1.9 | 1.0–2.0 | 62 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 84.6667, 'CALIBRATION': 59.1667, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 50.3333, 'PRACTITIONER_QA': 64.5, 'TECHNICAL_ASSESSMENT': 87.3333, 'VALUES_BEHAVIOR_INTERVIEW': 110.3333}
- total_person_hours: 537.1667
- first_interview_and_calibration_person_hours: 295.6667
- first_interview_plan_capacity_person_hours: 80
- incomplete_participation_intervals: 0

## Offer Lifecycle

- OFFERED: 2
- ACCEPTED: 0
- DECLINED: 0
- EXPIRED: 2
- PRE_JOIN_WITHDRAWAL: 0

## Offer Current State

- EXPIRED: 2

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 0
- ready_observed: 0
- ready_by_target_date: 0
- target_date: 2027-09-01
- available_supply_at_target_fte: 12
- demand_fte: 16
- fulfillment_ratio: 0.75
- ramp_up_extended: 0
- join_to_ready_days: {'n': 0, 'min': None, 'median': None, 'p90': None, 'max': None}

## Evidence

- assessment_evidence: 3773
- assessment_observations: 7542
- evidence_decisions: 6084
- evidence_decision_sources: 9545
- final_decisions: 61

## Calibration

- AGREED: 4206
- DISAGREEMENT_REMAINS: 1208
- INSUFFICIENT_EVIDENCE: 670

## Final Decisions

- PROCEED_TO_OFFER: 2
- DO_NOT_PROCEED: 0
- HOLD: 59

## Validation

- WARNING REVIEW_PENDING: Synthetic generation rules and overall realism require human Dataset review; no v1 freeze.
- WARNING EMPTY_ONBOARDING_COHORT: No joined cohort; preserve the outcome, review rules without tuning to Target.

## Interpretation Boundary

- Target differences are not validation errors.
- Calibration counts include successive review snapshots, not unique candidates.
- All people, judgments and work artifacts are synthetic. Human rule review remains pending.
