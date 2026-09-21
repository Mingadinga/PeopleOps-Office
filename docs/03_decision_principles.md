# PeopleOps Office — Decision Principles

## 1. Purpose

PeopleOps Office에서는 결과보다
결과가 만들어진 판단 과정을 중요하게 다룬다.

주요 Decision은 다음 질문에 답할 수 있어야 한다.

1. 어떤 질문에 대한 결정인가?
2. 어떤 선택을 했는가?
3. 어떤 근거를 사용했는가?
4. 어떤 대안이 있었는가?
5. 대안을 선택하지 않은 이유는 무엇인가?
6. 어떤 조건이 바뀌면 결정을 다시 검토해야 하는가?

---

# 2. Decision Structure

권장 구조:

Decision ID

Question

Decision

Reason

Evidence

Alternatives Considered

Not Selected Reason

Revisit Condition

---

# 3. Example

Question:

4 FTE Workforce Gap을 어떤 방식으로 확보할 것인가?

Decision:

신입 외부채용

Reason:

- 즉시전력 요구가 낮다.
- 6개월 Ramp-up이 가능하다.
- 기존 숙련인력의 육성 Capacity가 있다.

Alternatives:

경력채용

Not Selected Reason:

현재 Scenario에서는 즉시 독립 수행이 핵심 Constraint가 아니다.

내부이동

Not Selected Reason:

확정된 내부 이동을 Forecast Supply에 반영한 뒤에도
4 FTE Gap이 남는다.

Revisit:

- Target Ready Date가 앞당겨짐
- Ramp-up Capacity 감소
- 즉시 독립 수행 역할 필요
- 내부 Supply 변경

---

# 4. Decision and Evidence

Evidence Type:

PUBLIC
INFERENCE
SYNTHETIC
ANALYSIS

하나의 Decision은 여러 Evidence를 가질 수 있다.

가능하면 UI에서 Decision → Evidence를 탐색할 수 있도록 한다.

---

# 5. Explainability Questions

제품 구현 시 주요 Decision에 대해 다음 질문에 답할 수 있는지 확인한다.

### Workforce

왜 이 Demand가 필요한가?

왜 Gap이 이 숫자인가?

Current Headcount가 아니라 Target-date Supply를 보는 이유는 무엇인가?

### Sourcing

왜 External Hire인가?

왜 신입인가?

어떤 조건이면 경력채용으로 바뀌는가?

### Talent

어떤 Talent가 필요한가?

각 Skill은 왜 필요한가?

어떤 Skill은 입사 전에 필요하고
어떤 Skill은 입사 후 학습 가능한가?

### Attraction

왜 이 Message인가?

왜 이 Channel인가?

단순 지원자 수가 아니라 무엇을 개선하려는가?

### Selection

각 Skill을 어떤 Evidence로 확인하는가?

왜 해당 Assessment를 사용하는가?

Technical Assessment와 Technical Interview는 무엇이 다른가?

AI Problem Solving Case가 필요한 이유는 무엇인가?

### KPI

왜 이 KPI를 측정하는가?

어떤 Decision에 사용되는가?

### Onboarding

왜 Join으로 끝나지 않는가?

어떤 기준으로 Ready를 판단하는가?

### Analysis

Mission 1에서 실제로 무엇이 발견되었는가?

관찰된 관계와 원인 가설을 구분했는가?

Mission 2에서 무엇을 바꾸었으며 왜 바꾸었는가?

---

# 6. AI Removal Test

AI 기능을 제거해도 다음 제품 핵심은 남아 있어야 한다.

- Workforce Planning
- Talent Profile
- Attraction Strategy
- Selection Design
- KPI
- Data Model
- EDA
- Decision

AI는 이 과정의 근거 생성과 설명을 지원한다.

AI 자체가 제품의 판단 구조를 대체하지 않는다.
