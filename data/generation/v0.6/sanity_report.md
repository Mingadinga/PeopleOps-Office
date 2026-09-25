# Mission 1 Dataset v0.6 — Sanity Report

Synthetic Dataset v0.6 sanity only; no WHY, hypothesis, intervention or Mission 2 Main Story.

Validation: **PASS** · Errors: 0 · Warnings: 2

## Record Counts

| File | Records |
|---|---:|
| applications.csv | 342 |
| stage_history.csv | 337 |
| assessment_activities.csv | 477 |
| activity_participants.csv | 419 |
| assessment_evidence.csv | 885 |
| evidence_skill_links.csv | 885 |
| assessment_observations.csv | 1463 |
| evidence_decisions.csv | 428 |
| skill_decision_observations.csv | 1834 |
| final_decisions.csv | 12 |
| offers.csv | 7 |
| offer_events.csv | 15 |
| onboarding_profiles.csv | 4 |
| onboarding_skill_gaps.csv | 6 |
| onboarding_tasks.csv | 28 |
| interview_capacity_events.csv | 3 |
| capacity_assignments.csv | 118 |
| workforce_events.csv | 15 |
| calibration_reviews.csv | 41 |
| activity_sessions.csv | 87 |
| evaluator_reservations.csv | 272 |
| targeted_followups.csv | 4 |
| eligibility_verifications.csv | 50 |
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
| 서류 근거 충족(조건부 포함) | 120 | 76 | -44 |
| 사전검증 통과 | 60 | 30 | -30 |
| 1차면접 계획 인원 | 20 | 30 | +10 |
| 2차면접 대상 | 8 | 10 | +2 |
| Offer | 5 | 7 | +2 |
| Join 목표 | 4 | 4 | +0 |

## Stage Outcomes

| Stage | Entered | Completed | Advanced | Conditional | Failed | Closed | Withdrawn | In Progress | Final lifecycle completed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DOCUMENT_SCREEN | 246 | 246 | 26 | 50 | 80 | 90 | 0 | 0 | 0 |
| PRE_ASSESSMENT | 43 | 36 | 30 | 0 | 6 | 0 | 2 | 5 | 0 |
| FIRST_INTERVIEW | 30 | 29 | 10 | 0 | 7 | 0 | 0 | 13 | 0 |
| SECOND_INTERVIEW | 10 | 8 | 8 | 0 | 0 | 0 | 1 | 1 | 0 |
| FINAL_REVIEW | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |

## Time Distributions

Days; NULL endpoints are excluded, never filled. Scheduling Wait includes known future appointments and does not imply elapsed waiting.

| Metric / Stage | n | Median | p90 | Range | NULL endpoints |
|---|---:|---:|---:|---|---:|
| stage_lead_time / DOCUMENT_SCREEN | 246 | 8.0413 | 12.0174 | 3.0174–14.0458 | 0 |
| stage_lead_time / PRE_ASSESSMENT | 36 | 12.0729 | 17.0625 | 6.0694–18.0799 | 7 |
| stage_lead_time / FIRST_INTERVIEW | 29 | 17.7611 | 20.9715 | 10.7611–22.7715 | 1 |
| stage_lead_time / SECOND_INTERVIEW | 8 | 15.0312 | 18.6208 | 9.0312–20.0208 | 2 |
| stage_lead_time / FINAL_REVIEW | 8 | 15.5278 | 18.0507 | 5.059–18.0556 | 0 |
| scheduling_wait / DOCUMENT_SCREEN | 0 | None | None | None–None | 246 |
| scheduling_wait / PRE_ASSESSMENT | 43 | 7.0 | 10.0 | 4.0–10.0 | 0 |
| scheduling_wait / FIRST_INTERVIEW | 30 | 10.7194 | 13.7194 | 6.7194–13.7194 | 0 |
| scheduling_wait / SECOND_INTERVIEW | 10 | 10.0 | 14.0 | 7.0–14.0 | 0 |
| scheduling_wait / FINAL_REVIEW | 0 | None | None | None–None | 8 |
| decision_time / DOCUMENT_SCREEN | 246 | 7.0104 | 10.0122 | 3.0104–12.0174 | 0 |
| decision_time / PRE_ASSESSMENT | 36 | 3.0 | 5.0 | 1.0–5.0 | 7 |
| decision_time / FIRST_INTERVIEW | 29 | 3.0104 | 5.0104 | 1.0–5.0104 | 1 |
| decision_time / SECOND_INTERVIEW | 8 | 2.0 | 3.6 | 1.0–5.0 | 2 |
| decision_time / FINAL_REVIEW | 8 | 11.5278 | 18.0507 | 5.059–18.0556 | 0 |
| notification_delay / DOCUMENT_SCREEN | 246 | 1.5 | 4.0 | 0.0–4.0 | 0 |
| notification_delay / PRE_ASSESSMENT | 36 | 1.0 | 4.0 | 0.0–4.0 | 7 |
| notification_delay / FIRST_INTERVIEW | 29 | 2.0 | 4.0 | 0.0–4.0 | 1 |
| notification_delay / SECOND_INTERVIEW | 8 | 1.0 | 2.6 | 0.0–4.0 | 2 |
| notification_delay / FINAL_REVIEW | 8 | 0.5 | 4.0 | 0.0–4.0 | 0 |

## Capacity

- by_activity_person_hours: {'AI_CASE': 0.0, 'CALIBRATION': 11.0, 'DOCUMENT_REVIEW': 80.8333, 'FINAL_REVIEW_DISCUSSION': 6.3333, 'FIRST_INTERVIEW_SESSION': 87.0, 'FOCUSED_FOLLOW_UP': 5.3333, 'FOLLOW_UP_CALIBRATION': 0.5, 'PRACTITIONER_QA': 0.0, 'TECHNICAL_ASSESSMENT': 0.0, 'VALUES_BEHAVIOR_INTERVIEW': 8.0}
- total_person_hours: 199.0
- first_interview_and_calibration_person_hours: 97.5
- interview_consumed_person_hours: 87.0
- first_calibration_person_hours: 10.5
- additional_person_hours: 30.0
- initial_person_hours: 60.0
- demand_person_hours: 90.0
- gap_person_hours: 30.0
- revised_person_hours: 90.0
- reserved_remaining_person_hours: 0.0
- released_reservation_person_hours: 3.0
- available_remaining_person_hours: 3.0

| Event | Hours | Demand | Effective at | Human role |
|---|---:|---:|---|---|
| INITIAL_PLAN | 60 | 0 | 2026-10-01T00:00:00+09:00 | HR_OPERATIONS_01 |
| GAP_IDENTIFIED | 30 | 90 | 2026-12-01T15:44:00+09:00 |  |
| CAPACITY_ADDED | 30 | 90 | 2026-12-03T15:44:00+09:00 | HR_OPERATIONS_01 |
- first_interview_plan_capacity_person_hours: 60
- incomplete_participation_intervals: 0

## Offer Lifecycle

- OFFERED: 7
- ACCEPTED: 5
- DECLINED: 1
- EXPIRED: 1
- PRE_JOIN_WITHDRAWAL: 1

## Offer Current State

- ACCEPTED: 4
- DECLINED: 1
- EXPIRED: 1
- PRE_JOIN_WITHDRAWAL: 1

## Workforce / Onboarding

- forecast_supply_fte: 12
- joined: 4
- ready_observed: 3
- ready_by_target_date: 0
- target_date: 2027-09-01
- available_supply_at_target_fte: 12
- demand_fte: 16
- fulfillment_ratio: 0.75
- ramp_up_extended: 4
- join_to_ready_days: {'n': 3, 'min': 210.0, 'median': 220.0, 'p90': 228.8, 'max': 231.0}

## Evidence

- assessment_evidence: 885
- assessment_observations: 1463
- evidence_decisions: 428
- skill_decision_observations: 1834
- final_decisions: 12

## Calibration

- AGREED: 325
- DISAGREEMENT_REMAINS: 58
- INSUFFICIENT_EVIDENCE: 45

## Calibration Activities

- eligible: 41
- triggered: 23
- actual: 23
- person_hours: 11.5

## Final Decision History

- PROCEED_TO_OFFER: 7
- DO_NOT_PROCEED: 1
- HOLD: 4

## Latest Final Decisions

- PROCEED_TO_OFFER: 7
- DO_NOT_PROCEED: 1

## HOLD Follow-up

- initial_proceed: 4
- initial_do_not_proceed: 0
- targeted_completed: 4
- initial: 4
- follow_up_activities: 4
- re_reviews: 4
- pending: 0
- re_review_outcomes: {'PROCEED_TO_OFFER': 3, 'DO_NOT_PROCEED': 1}

## Ready Coverage

- not_yet_ready: 1
- gap_skill_counts: {'M1_SKILL_03': 3, 'M1_SKILL_05': 2, 'M1_SKILL_06': 1}

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
    "ELIGIBILITY_CONFIRMATION_REQUIRED": 50,
    "APPLICATION_EVIDENCE_CANDIDATE": 26
  },
  "note": "Application combination columns overlap for multiple experiences; category union is reporting only, never the decision rule. UNKNOWN eligibility is not verified PASS. CLOSED is insufficient submitted evidence, not Skill limitation."
}
```

## Eligibility Resolution (v0.6)

```json
{
  "initial": {
    "PASS": 63,
    "UNKNOWN": 103,
    "FAIL": 80
  },
  "document_states": {
    "FAILED": 80,
    "CLOSED": 90,
    "CONDITIONAL_ADVANCE": 50,
    "ADVANCED": 26
  },
  "document_evidence_qualified": 76,
  "verification_candidates": {
    "ELIGIBILITY_NOT_VERIFIED": 15,
    "VERIFIED_PASS": 17,
    "VERIFIED_FAIL": 18
  },
  "verification_requirements": {
    "ELIGIBILITY_NOT_VERIFIED": 15,
    "VERIFIED_PASS": 17,
    "VERIFIED_FAIL": 18
  },
  "pre_entry": 43,
  "offer_unresolved": 0,
  "join_unresolved": 0,
  "note": "Document conditional decision remains history; original UNKNOWN is never rewritten. NOT_VERIFIED is procedure closure, not eligibility FAIL or Skill limitation."
}
```
