# Mission 1 Dataset v0.5 — Sanity Report

Synthetic Dataset v0.5 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 412 |
| assessment_activities.csv | 672 |
| activity_participants.csv | 561 |
| assessment_evidence.csv | 1147 |
| evidence_skill_links.csv | 1147 |
| assessment_observations.csv | 2203 |
| evidence_decisions.csv | 764 |
| skill_decision_observations.csv | 3249 |
| final_decisions.csv | 20 |
| offers.csv | 9 |
| offer_events.csv | 20 |
| onboarding_profiles.csv | 4 |
| onboarding_skill_gaps.csv | 5 |
| onboarding_tasks.csv | 23 |
| interview_capacity_events.csv | 3 |
| capacity_assignments.csv | 224 |
| workforce_events.csv | 15 |
| calibration_reviews.csv | 73 |
| activity_sessions.csv | 159 |
| evaluator_reservations.csv | 530 |
| targeted_followups.csv | 6 |
| application_eligibility.csv | 246 |
| application_experiences.csv | 381 |
| workforce_plan.json | 1 |
| funnel_plan.json | 8 |
| talent_profile.json | 9 |

## Target vs Actual

| Bucket | Target | Actual | Difference |
|---|---:|---:|---:|
| 지원 시작 | 320 | 342 | +22 |
| 지원 완료 | 240 | 246 | +6 |
| 서류 통과 | 120 | 76 | -44 |
| 사전검증 통과 | 60 | 59 | -1 |
| 1차면접 계획 인원 | 20 | 59 | +39 |
| 2차면접 대상 | 8 | 17 | +9 |
| Offer | 5 | 9 | +4 |
| Join 목표 | 4 | 4 | +0 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Failed | Withdrawn | In Progress | Final lifecycle completed |
|---|---:|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 76 | 80 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 76 | 68 | 59 | 9 | 3 | 5 | 0 |
| FIRST_INTERVIEW | 59 | 53 | 17 | 11 | 1 | 30 | 0 |
| SECOND_INTERVIEW | 17 | 14 | 14 | 0 | 2 | 1 | 0 |
| FINAL_REVIEW | 14 | 14 | 0 | 0 | 0 | 0 | 14 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0413 | 12.0174 | 3.0174–14.0458 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 68 | 12.5712 | 16.0601 | 6.0694–18.0799 | 8 |
| stage_lead_time / FIRST_INTERVIEW | 53 | 21.7458 | 28.7458 | 9.7458–30.7458 | 6 |
| stage_lead_time / SECOND_INTERVIEW | 14 | 14.0208 | 19.4208 | 9.0312–20.0521 | 3 |
| stage_lead_time / FINAL_REVIEW | 14 | 14.5365 | 18.7701 | 5.0139–20.0556 | 0 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 76 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 59 | 12.6937 | 23.6938 | 5.6937–23.6938 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 17 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 14 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 68 | 3.0 | 5.0 | 1.0–5.0 | 8 |
| decision_time / FIRST_INTERVIEW | 53 | 3.0104 | 5.0104 | 1.0–5.0104 | 6 |
| decision_time / SECOND_INTERVIEW | 14 | 1.5052 | 3.0 | 1.0–5.0 | 3 |
| decision_time / FINAL_REVIEW | 14 | 11.5365 | 18.0628 | 5.0139–18.1042 | 0 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 68 | 1.5 | 4.0 | 0.0–4.0 | 8 |
| notification_delay / FIRST_INTERVIEW | 53 | 1.0 | 4.0 | 0.0–4.0 | 6 |
| notification_delay / SECOND_INTERVIEW | 14 | 1.0 | 4.0 | 0.0–4.0 | 3 |
| notification_delay / FINAL_REVIEW | 14 | 1.5 | 4.0 | 0.0–4.0 | 0 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 0.0, 'CALIBRATION': 20.5, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 11.3333, 'FIRST_INTERVIEW_SESSION': 159.0, 'FOCUSED_FOLLOW_UP': 8.0, 'FOLLOW_UP_CALIBRATION': 1.5, 'PRACTITIONER_QA': 0.0, 'TECHNICAL_ASSESSMENT': 0.0, 'VALUES_BEHAVIOR_INTERVIEW': 14.0}
- total_person_hours: 295.1667
- first_interview_and_calibration_person_hours: 178.5
- interview_consumed_person_hours: 159.0
- first_calibration_person_hours: 19.5
- additional_person_hours: 120.0
- initial_person_hours: 60.0
- demand_person_hours: 177.0
- gap_person_hours: 117.0
- revised_person_hours: 180.0
- reserved_remaining_person_hours: 0.0
- released_reservation_person_hours: 18.0
- available_remaining_person_hours: 21.0

| Event | Hours | Demand | Effective at | Human role |
|---|---:|---:|---|---|
| INITIAL_PLAN | 60 | 0 | 2026-10-01T00:00:00+09:00 | HR_OPERATIONS_01 |
| GAP_IDENTIFIED | 117 | 177 | 2026-12-02T16:21:00+09:00 |  |
| CAPACITY_ADDED | 120 | 177 | 2026-12-04T16:21:00+09:00 | HR_OPERATIONS_01 |
- first_interview_plan_capacity_person_hours: 60
- incomplete_participation_intervals: 0

## Offer Lifecycle

- OFFERED: 9
- ACCEPTED: 6
- DECLINED: 0
- EXPIRED: 3
- PRE_JOIN_WITHDRAWAL: 2

## Offer Current State

- ACCEPTED: 4
- EXPIRED: 3
- PRE_JOIN_WITHDRAWAL: 2

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 4
- ready_observed: 4
- ready_by_target_date: 0
- target_date: 2027-09-01
- available_supply_at_target_fte: 12
- demand_fte: 16
- fulfillment_ratio: 0.75
- ramp_up_extended: 3
- join_to_ready_days: {'n': 4, 'min': 187.0, 'median': 215.0, 'p90': 227.7, 'max': 231.0}

## Evidence

- assessment_evidence: 1147
- assessment_observations: 2203
- evidence_decisions: 764
- skill_decision_observations: 3249
- final_decisions: 20

## Calibration

- AGREED: 596
- DISAGREEMENT_REMAINS: 93
- INSUFFICIENT_EVIDENCE: 75

## Calibration Activities

- eligible: 73
- triggered: 44
- actual: 44
- person_hours: 22.0

## Final Decision History

- PROCEED_TO_OFFER: 9
- DO_NOT_PROCEED: 5
- HOLD: 6

## Latest Final Decisions

- PROCEED_TO_OFFER: 9
- DO_NOT_PROCEED: 5

## HOLD Follow-up

- initial_proceed: 8
- initial_do_not_proceed: 0
- targeted_completed: 6
- initial: 6
- follow_up_activities: 6
- re_reviews: 6
- pending: 0
- re_review_outcomes: {'DO_NOT_PROCEED': 5, 'PROCEED_TO_OFFER': 1}

## Ready Coverage

- not_yet_ready: 0
- gap_skill_counts: {'M1_SKILL_03': 2, 'M1_SKILL_06': 2, 'M1_SKILL_05': 1}

## Validation

- WARNING REVIEW_PENDING: Synthetic rules/realism review remains pending; no freeze.
- WARNING SYNTHETIC_POLICY_ASSUMPTIONS: Source matrix, resource blocks, re-review uncertainty handling and mentor scenarios require human rule audit; not employer policies.

## Interpretation Boundary

- Target differences are not validation errors.
- Calibration counts include successive review snapshots, not unique candidates.
- All people, judgments and work artifacts are synthetic. Human rule review remains pending.

## Application / Document (v0.5)

CLOSED means insufficient submitted application evidence; it is not Skill limitation.

```json
{
  "eligibility": {
    "PASS": 63,
    "UNKNOWN": 103,
    "FAIL": 80
  },
  "requirements": {
    "degree": {
      "PASS": 205,
      "UNKNOWN": 23,
      "FAIL": 18
    },
    "language": {
      "PASS": 197,
      "UNKNOWN": 21,
      "FAIL": 28
    },
    "travel_visa": {
      "PASS": 195,
      "UNKNOWN": 35,
      "FAIL": 16
    },
    "military": {
      "NOT_APPLICABLE": 114,
      "PASS": 90,
      "FAIL": 18,
      "UNKNOWN": 24
    }
  },
  "experience_count": 381,
  "experience_combinations": {
    "VALIDATE": 49,
    "BUILD+PROBLEM+VALIDATE": 49,
    "PROBLEM": 55,
    "BUILD+VALIDATE": 46,
    "PROBLEM+VALIDATE": 44,
    "BUILD": 43,
    "NONE": 48,
    "BUILD+PROBLEM": 47
  },
  "application_combinations": {
    "VALIDATE": 46,
    "BUILD+PROBLEM+VALIDATE": 48,
    "PROBLEM": 51,
    "BUILD+VALIDATE": 44,
    "PROBLEM+VALIDATE": 41,
    "BUILD": 43,
    "NONE": 45,
    "BUILD+PROBLEM": 44
  },
  "category_applications": {
    "PROBLEM": 161,
    "BUILD": 154,
    "VALIDATE": 152
  },
  "ownership_experiences": {
    "TEAM_CLEAR": 137,
    "TEAM_UNCLEAR": 120,
    "SELF": 124
  },
  "document_reasons": {
    "BASIC_REQUIREMENT_VIOLATION": 80,
    "INSUFFICIENT_APPLICATION_EVIDENCE": 90,
    "APPLICATION_EVIDENCE_CANDIDATE": 76
  },
  "note": "Application combination columns overlap for multiple experiences; category union is reporting only, never the decision rule. UNKNOWN eligibility is not verified PASS. CLOSED is insufficient submitted evidence, not Skill limitation."
}
```
