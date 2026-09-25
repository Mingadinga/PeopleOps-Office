# PeopleOps Office — Product Flow

## 1. Core Loop

PeopleOps Office의 핵심은 다음 Loop이다.

Workforce Need
→ Recruiting
→ Join
→ Ready
→ Data
→ Analysis
→ Improvement
→ Next Workforce Need

채용 자체가 최종 목적이 아니다.

최종적으로 필요한 것은
목표 시점에 업무 가능한 Workforce Supply를 확보하는 것이다.

---

# 2. Mission 1

## Step 1. Workforce Planning

Business Question:

목표 시점에 필요한 인력이 충분한가?

확인 데이터:

- Demand
- Current Supply
- Confirmed Workforce Flow
- Forecast Supply
- Gap

Output:

Workforce Gap

---

## Step 2. Sourcing Strategy

Business Question:

Gap을 어떤 방식으로 해결할 것인가?

검토 가능한 방법:

- External Hire
- Internal Move
- Develop
- External Capacity

현재 Mission에서는 Scenario의 조건을 기반으로
적절한 확보 방식을 결정한다.

채용 방식은 미리 정해진 결론이 아니라
Workforce Need와 Constraint에서 도출한다.

---

## Step 3. Talent Profile

Business Question:

어떤 사람을 확보해야 하는가?

Flow:

Business / Work
→ Required Skill
→ Required Evidence
→ Talent Profile

Skill은 다음과 같이 구분한다.

- MUST
- LEARNABLE
- PLUS

---

## Step 4. Attraction

Business Question:

Target Talent에게 해당 직무를 어떻게 알릴 것인가?

핵심:

단순 지원자 수 증가보다
직무에 적합한 관심과 지원을 만드는 것을 목표로 한다.

Attraction Strategy는 다음을 포함할 수 있다.

- Target
- Message
- Content
- Channel
- Candidate Information Need
- KPI

---

## Step 5. Selection

Business Question:

Talent Profile에서 정의한 역량을
어떤 Evidence로 확인할 것인가?

Flow:

Skill
→ Evidence
→ Assessment

V2 Selection Flow(상세 전형은 PeopleOps Office 시나리오):

지원 → 서류 → 사전검증(역량검사·코딩테스트)
→ 1차 실무진면접(기술평가·AI 문제해결 과제·실무진 질의)
→ 1차 평가 조정 → 2차면접 → 최종검토 → Offer → Join

기술평가와 AI 문제해결 과제는 독립 채용 Stage가 아니라 1차면접의 평가 활동이다.
사전검증 Stage의 역량검사·코딩테스트는 내부 Activity다. 역량검사는 활동 이벤트만 다루며 실제 기업의 문항을 재현하지 않는다.
세부 판단은 [07 채용 설계](07_recruitment_design_specification.md)를 따른다.

각 역량은 Primary Assessment를 가진다.

다른 전형은 해당 Evidence를 보완하거나 검증할 수 있다.

불필요하게 같은 역량을 여러 전형에서 반복 평가하지 않는다.

---

## Step 6. Recruiting Operation

채용 과정에서 다음 Event를 기록한다.

- Application Start
- Application Complete
- Stage Enter
- Stage Complete
- Result
- Withdrawal
- Offer
- Join

이를 이용해 다음을 계산한다.

- Conversion
- Lead Time
- Withdrawal
- Offer Acceptance
- Join

---

## Step 7. Onboarding

Join은 Workforce Planning의 끝이 아니다.

Flow:

Join
→ Selection Evidence
→ Skill Gap
→ Ramp-up Task
→ Ready

Onboarding은 전체 교육 플랫폼을 구현하지 않는다.

목표는 입사자가 Target Date까지
Available Supply가 되었는지 확인하는 것이다.

---

## Step 8. KPI

각 단계에서 사용하는 KPI는 Target과 Actual을 구분한다. 아직 계산하지 않은 Actual을 0으로 표시하지 않는다.

Target은 실제 결과를 보기 전에 설정한다.

Actual은 Event Data에서 계산한다.

---

# 3. Mission 2

새로운 경력직 인력요청(제조AI - 제조AI Agent 데이터 엔지니어링)
→ Headcount / Capability Gap
→ Mission 1 canonical Dataset
→ Workforce Outcome / Target vs Actual Funnel
→ FAIL / WITHDRAW / Lead Time / 추가 분석
→ 관찰 / 가설 / 한계 / Mission 1 개선
→ 신입과 경력 조건 비교
→ 재사용 Evidence / 재설계 Assumption
→ 경력 인재 요건 / Sourcing / Funnel / Capacity / Assessment
→ 경력 채용계획 확정

Mission 1 결과를 미리 정하지 않는다. 실제 분석 후 의미 있는 패턴을 선택한다.
과거 데이터는 다음 채용의 정답이 아니라 다음 계획의 Evidence다.
상세 분석과 종료 조건은 [10](10_mission2_analytics_specification.md)을 따른다.

---

# 4. Analysis Principle

분석 UI에서는 결과만 보여주지 않는다.

가능한 경우 다음 과정을 확인할 수 있어야 한다.

분석 질문
→ 분석 목표
→ 사용 데이터
→ Prompt
→ Python/Pandas Code
→ Result
→ Interpretation
→ Hypothesis
→ Decision

이를 통해 분석 결과가 어떻게 만들어졌는지 추적 가능하게 한다.

# 5. 사용자 진행도와 업무 흐름의 대응

위 업무 Step은 HR 개념 구분이며 화면 진행도와 1:1 관계가 아니다.

| 상위 Stage | 포함 업무 |
|---|---|
| 인력계획 | 요청, Demand, Current/Confirmed Flow, Forecast/Gap, 확보 방식 |
| 인재 정의 | 업무 이해, 인재 요건 Workshop, Skill/Evidence |
| 채용 설계 | 공고, 점검, 지원자 화면, 인재 유치, 지원 질문, Funnel/Capacity |
| 지원자 검증 | 서류, 사전검증, 1차 설계·수행·조정, 2차 |
| 인재 확보 | 최종검토, Offer, 응답, Join |
| 업무 준비 | Skill Gap, Ramp-up, 실제 업무 Evidence, Ready, 결과 |

완료 Summary는 다시 볼 수 있고 예정 단계로 Jump하지 않는다. Room 선택으로 이 규칙을 우회하지 않는다.
Scene이 질문·근거·판단을 연결하며 동일 공간을 여러 Scene이 사용한다.
Mission 1 결과는 Workforce / Recruiting Process / Onboarding의 WHAT을 보여주고
`데이터 분석 시작`으로 연결한다. 원인 가설은 Mission 2에서 다룬다.
Mission 2의 6단계 진행도 적용은 [OPEN-02](11_v2_migration_specification.md#7-open-issues)이며
계획 수립을 실제 채용 완료로 표시하지 않는다.
