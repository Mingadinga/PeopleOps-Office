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

AI는 원자료의 검색·정리·연결 후보·계산·설명을 지원한다. AI 출력은 원본 Evidence가 아니다.

AI 자체가 제품의 판단 구조를 대체하지 않는다.

# 7. V2 Human Decision Boundary

**People make decisions. Technology organizes evidence.**

원본 Evidence → AI Skill 후보 → 사람이 연결 확정 → 사람이 수준 판단 → 평가 조정 → Human Decision.
AI 후보는 수정·거부할 수 있고 자동 확정하지 않는다. Evidence Level은
확인되지 않음 / 제한적 / 충분 / 강함이며 숫자·평균·총점으로 변환하지 않는다.
확인되지 않음은 역량이 없다는 뜻이 아니다.

평가 차이는 Observation → Original Evidence → Rubric → Review로 확인한다.
AGREED / DISAGREEMENT_REMAINS / INSUFFICIENT_EVIDENCE를 구분하고 미합의를 보존한다.
최종 검토는 인재 요건, Must Evidence, 남은 불확실성, Learnable Gap, Calibration을 보고 사람이 결정한다.
자동 합불, Candidate Total Score/Ranking, Fit/Culture Fit Score, 개인 성공·성과·퇴사 예측은 금지한다.

Dataset의 Evidence·Human Observation·Human Decision은 모두 SYNTHETIC 시나리오다.
실제 사람의 평가 결과가 아니며 판단에는 SYNTHETIC_HUMAN_SCENARIO provenance를 남긴다.
Generator는 관찰 가능한 Evidence와 Rubric을 바탕으로 기록을 구성한다. 숨은 능력 점수·합격확률에서 역산하지 않는다.
평가 차이는 원근거의 모호성·관찰 범위·Rubric 해석으로 설명하며 무작위 점수 차이로 만들지 않는다.
MUST 근거 부족은 HOLD/추가 근거 필요일 수 있고 LEARNABLE Gap만으로 탈락시키지 않는다.
여러 Assessment의 명확한 필수 근거 부족은 DO_NOT_PROCEED의 설명 가능한 이유가 될 수 있다.
실제 Dataset Reviewer는 개별 합불이 아닌 생성 규칙·출처·근거 추적·정합성·현실성·금지 점수 유무를 검토한다.
구조와 생성 계약의 정본은 [09](09_mission1_data_specification.md)다.

# 8. 계획과 분석을 위한 결정

Funnel Target은 예상 전환·평가비용·Capacity·선발 위험을 사람이 검토한 계획이다.
시스템의 Capacity 계산이 최적 인원이나 통과 기준을 결정하지 않는다.
FAIL과 WITHDRAW, UNKNOWN과 관찰된 사유, JOINED와 READY를 구분한다.
Ready는 실제 업무 Evidence와 사람의 확인을 필요로 한다.

Mission 2는 관찰·해석·가설·한계를 분리한다. 상관관계나 작은 표본으로 원인을 확정하지 않는다.
신입 모집단의 전환율·채널·Ramp-up을 경력 계획에 그대로 복사하지 않는다.
운영 근거의 적용 가능성과 새 가정을 함께 기록하고 다음 측정 계획까지 연결한다.

# 9. Source와 미결정 처리

제품 결정은 최신 확정사항, 외부 사실은 검증 가능한 원문을 기준으로 한다.
원문·2차 아카이브·캡처·요약을 구분하며 PUBLIC 사실과 INFERENCE/SYNTHETIC을 혼합하지 않는다.
원문이 없으면 SOURCE NOT AVAILABLE, 검증이 남으면 TO VERIFY, 결정이 남으면 OPEN ISSUE로 기록한다.
네 Evidence 유형을 변경하거나 미정 항목을 사실처럼 채우지 않는다.
출처와 미결정 등록부는 [11](11_v2_migration_specification.md)에, AI 기능별 권한은 [08](08_hr_tech_specification.md)에 둔다.
