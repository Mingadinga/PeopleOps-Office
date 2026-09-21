# PeopleOps Office — Data Model

## 1. Purpose

데이터 모델은 Database 구현을 위한 Schema가 아니다.

목적은 다음 질문에 답하는 것이다.

어떤 Business Question에 답하기 위해
어떤 Data가 필요한가?

기본 구조:

Business Question
→ Required Data
→ File / Field
→ Analysis
→ Decision

---

# 2. Data Layers

MVP는 영속 Database를 사용하지 않는다. 실행 중인 Office UI에서 사용하지 않는
템플릿의 Drizzle 접근 코드, 마이그레이션 메타데이터 및 D1 예제는 제거했다.
Case JSON, Synthetic CSV, Analysis JSON을 배포 Artifact에 포함하는 구조를 유지한다.

기존 실행 환경을 보존하기 위해 Cloudflare 설정과 Worker는 유지한다.
`.openai/hosting.json`의 D1 설정은 `null`이며, Worker의 `DB` 타입 선언은
실제 Database 사용을 의미하지 않는다.

## Case Data

Format:

JSON

Purpose:

Scenario와 사전에 정의된 HR Decision을 표현한다.

Examples:

mission1.json
talent_profile.json
recruiting_strategy.json
kpi_definitions.json
decisions.json

---

## Event Data

Format:

CSV

Purpose:

Recruiting 및 Onboarding 과정에서 발생하는 Event를 표현한다.

Examples:

attraction_daily.csv
applications.csv
stage_history.csv
assessment_evidence.csv
onboarding.csv

모든 Event Data는 SYNTHETIC이다.

---

## Analysis Data

Format:

JSON

Purpose:

Python/Pandas 분석 결과를 Web UI에서 사용한다.

Example:

mission1_results.json

Analysis JSON은 사람이 결과를 직접 작성하지 않는다.

Synthetic CSV
→ Python/Pandas
→ Analysis JSON

방식으로 생성한다.

---

# 3. Mission Data

File:

data/case/mission1.json

Business Questions:

- 목표시점 Demand는 얼마인가?
- 현재 Supply는 얼마인가?
- 목표시점 Forecast Supply는 얼마인가?
- Gap은 얼마인가?
- 어떤 Constraint가 존재하는가?

Required Data:

mission_id
baseline_date
target_ready_date
demand_fte
current_fte
confirmed_flow
ramp_up_months
development_capacity
immediate_productivity_required

Derived:

forecast_supply_fte

gap_fte

Formula:

Forecast Supply
= Current Supply + Confirmed Future Flow

Gap
= Demand - Forecast Supply

---

# 4. Talent Profile

File:

data/case/talent_profile.json

Business Questions:

- 어떤 Skill이 필요한가?
- 입사 전 반드시 필요한 Skill인가?
- 입사 후 학습 가능한가?
- 어떤 Evidence로 확인할 수 있는가?

Fields:

skill_id
name
requirement
reason
expected_evidence
evidence_type
source_reference

Requirement:

MUST
LEARNABLE
PLUS

---

# 5. Recruiting Strategy

File:

data/case/recruiting_strategy.json

Includes:

Attraction Strategy
Selection Strategy

Attraction:

target
problem
message
content
channel
channel_reason

Selection:

stage
skill
required_evidence
primary_assessment
validation_assessment
reason

---

# 6. Attraction Event

File:

data/synthetic/attraction_daily.csv

Business Question:

어떤 Channel이 실제 관심과 지원으로 이어졌는가?

Fields:

date
campaign_id
channel_id
impressions
job_page_visits
application_starts

Analysis:

Visit Rate

Application Start Rate

Channel Comparison

개별 사용자의 마케팅 Tracking Data는 MVP에서 수집하지 않는다.

---

# 7. Applications

File:

data/synthetic/applications.csv

Business Questions:

- 어느 Channel에서 지원했는가?
- 지원을 완료했는가?
- 기본 Qualification을 충족했는가?
- 지원 중 이탈했는가?

Fields:

application_id
candidate_id
campaign_id
channel_id
started_at
submitted_at
qualification_status

Candidate는 Synthetic ID만 사용한다.

실제 이름, 학교, 성별, 나이 등의 개인정보는 사용하지 않는다.

Qualification은 불투명한 AI Fit Score가 아니다.

명시된 기본 기준을 기반으로 한다.

---

# 8. Recruiting Stage History

File:

data/synthetic/stage_history.csv

Business Questions:

- 어느 단계에서 이탈하는가?
- 어느 단계가 오래 걸리는가?
- 각 단계의 Conversion은 얼마인가?

Fields:

application_id
stage
entered_at
result_decided_at
notified_at
completed_at
result
reason_code

Stages:

APPLICATION
TECH_ASSESSMENT
AI_CASE
TECH_INTERVIEW
FINAL_INTERVIEW
OFFER
JOIN

Results:

PASS
FAIL
WITHDRAW
PENDING

Analysis:

Stage Conversion

Stage Lead Time

Notification Delay

Withdrawal Rate

현재 상태만 저장하지 않고
Stage History를 보존해야 위 지표를 계산할 수 있다.

---

# 9. Assessment Evidence

File:

data/synthetic/assessment_evidence.csv

Business Question:

Selection 과정에서 어떤 Skill Evidence가 관찰되었는가?

Fields:

application_id
stage
skill_id
evidence_level
observation_code

Evidence Level:

NOT_OBSERVED
LIMITED
MODERATE
STRONG

종합적인 AI Candidate Score를 만들지 않는다.

Evidence는 관찰 기록이다.

---

# 10. Onboarding

File:

data/synthetic/onboarding.csv

Business Questions:

- 입사자가 언제 Ready가 되었는가?
- 어떤 Skill Gap이 있었는가?
- Ramp-up이 목표 기간 내 완료되었는가?

Fields:

hire_id
application_id
join_date
target_ready_date
actual_ready_date
readiness_status
primary_skill_gap
onboarding_task_type
task_completed

Readiness:

ONBOARDING
READY
RAMP_UP_EXTENDED

Core Concept:

JOINED ≠ READY

---

# 11. KPI

File:

data/case/kpi_definitions.json

Each KPI should contain:

code
name
category
formula
purpose
decision_use

현재 KPI 후보:

Workforce

- Workforce Fulfillment

Attraction

- Visit Rate
- Application Start Rate
- Qualified Application Rate

Selection

- Stage Conversion

Operation

- Stage Lead Time
- Notification Delay
- Withdrawal Rate

Offer

- Offer Acceptance

Hiring

- Join Rate

Onboarding

- Ready Rate

KPI는 측정 가능하다는 이유만으로 추가하지 않는다.

각 KPI는 반드시 다음 질문에 답해야 한다.

이 KPI를 어떤 Decision에 사용할 것인가?

---

# 12. Decision Data

File:

data/case/decisions.json

Fields:

decision_id
mission_id
step
question
decision
reason
alternatives
evidence_refs
revisit_condition

Purpose:

UI의 `판단 근거 보기`와
HR Copilot의 설명에 공통으로 사용한다.

---

# 13. Evidence Reference

Recommended ID:

PUBLIC-XXX
INFERENCE-XXX
SYN-XXX
ANALYSIS-XXX

각 Decision은 Evidence Reference를 통해
근거를 추적할 수 있어야 한다.

---

# 14. Synthetic Data Generation

Generation Order:

1. Attraction Channel Events
2. Application Inflow
3. Observable Skill Evidence
4. Application Completion / Withdrawal
5. Stage Events
6. Stage Assessment Evidence
7. Stage Results
8. Lead Time
9. Offer / Join
10. Onboarding Skill Gap
11. Ramp-up Tasks
12. Ready State
13. KPI Calculation

Fixed Random Seed를 사용한다.

초기 후보:

20260921

Synthetic Data는 특정 분석 결론을 강제로 만들기 위해 생성하지 않는다.

현실적인 Noise를 포함한다.

Examples:

- Evidence가 강해도 지원자가 Withdraw할 수 있다.
- 전형을 통과해도 Offer를 거절할 수 있다.
- Channel별 Volume과 Qualification 비율이 다를 수 있다.
- 작은 Skill Gap이 항상 빠른 Ready를 보장하지 않는다.
- Stage Lead Time은 일정하지 않다.

---

# 15. Mission 2 Analysis Questions

현재 Data Model은 최소한 다음 질문에 답할 수 있어야 한다.

- 어느 Channel이 Qualified Application 확보에 효과적이었는가?
- 어느 Stage에서 지원자가 가장 많이 이탈했는가?
- 어느 Stage의 Lead Time이 가장 길었는가?
- Lead Time과 Withdrawal 사이에 어떤 관계가 관찰되는가?
- 어떤 Skill Evidence가 상대적으로 부족했는가?
- Selection Evidence와 Onboarding Skill Gap 사이에 어떤 관계가 관찰되는가?
- 신규 입사자 4명이 실제 Target Date의 Available Supply가 되었는가?

관계가 관찰되더라도 인과관계로 단정하지 않는다.
