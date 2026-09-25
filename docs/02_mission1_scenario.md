# Mission 1 — Machine Learning Engineer Workforce Planning

## 1. Scenario Status

이 문서의 인력 숫자와 조직 상황은 SYNTHETIC이다.

실제 특정 기업의 내부 인력현황을 의미하지 않는다.

직무와 관련된 PUBLIC Evidence는 별도로 관리한다.

---

# 2. Mission

Mission ID:

M01

Job:

신입 Machine Learning Engineer

Baseline Date:

2026-10-01

Target Ready Date:

2027-09-01

---

# 3. Workforce Demand

Target Date의 ML Engineer Demand:

16 FTE

Evidence Type:

SYNTHETIC

---

# 4. Current Workforce

Baseline Current Supply:

12 FTE

Confirmed Flow:

2027-01
Internal Transfer In
+1 FTE

2027-03
Internal Transfer Out
-1 FTE

Confirmed Joiners:

0 FTE

따라서:

Forecast Supply
= 12 + 1 - 1 + 0
= 12 FTE

Workforce Gap
= max(Demand - Forecast Supply, 0)
= 16 - 12
= 4 FTE

---

# 5. Scenario Constraints

Immediate Productivity Required:

False

Ramp-up Tolerance:

6 months

Development Capacity:

Available

Independent Lead Role Required:

False

기존 숙련 인력이 존재하며
신규 인력을 일정 기간 육성할 수 있다고 가정한다.

Evidence Type:

SYNTHETIC

---

# 6. Recruiting Channel Decision

현재 Scenario에서는 신입 외부채용을 기본 방향으로 사용한다.

Reason:

- 즉시 독립 수행이 핵심 Constraint가 아니다.
- Target Ready Date까지 Ramp-up 기간을 확보할 수 있다.
- 기존 숙련 인력을 통한 육성 Capacity가 존재한다.
- Lead 역할이 필요한 상황이 아니다.

단, 이 결정은 모든 ML Engineer 채용에 일반화하지 않는다.

Workforce Need와 Constraint가 달라지면
경력채용 등 다른 방식이 적절할 수 있다.

---

# 7. Timeline

Target Ready:

2027-09

Ramp-up:

6 months

따라서 Target Join 시점:

approximately 2027-03

Recruiting Process는 이 Join 목표에서 역산하여 설계한다.

---

# 8. Workforce KPI

Primary Workforce KPI:

Target-date Workforce Fulfillment

Formula:

Target-date Available Supply / Demand × 100

Initial Forecast:

12 / 16 × 100
= 75%

Mission Goal:

100%

---

# 9. Recruiting Goal

Recruiting Output Goal:

Target Join 시점까지
ML Engineer 신규 입사 4명 확보

단:

4 JOINED ≠ Workforce Goal Achieved

최종 Workforce Goal은
Target Ready Date의 Available Supply로 확인한다.

---

# 10. Talent Profile Direction

현재 Target Candidate 방향:

현실의 문제를 구조화하고,
수리최적화와 머신러닝의 기초를 바탕으로
해결 방법을 설계하고 구현할 수 있으며,
새로운 기술을 능동적으로 학습하고
협업을 통해 해결책을 발전시킬 수 있는 신입 엔지니어.

Skill Group의 V2 기준:

| 구분 | 내용 |
|---|---|
| MUST | 문제 구조화; ML/수리적 사고 기초; 알고리즘 구현 및 검증; 새로운 기술 학습; 협업 및 기술 커뮤니케이션 |
| LEARNABLE | 운영 가능한 구현 이해 및 Production 경험 |
| PLUS | 논문/알고리즘 구현 경험; 관련 연구/프로젝트; 필요한 경우 Business English |

전문가 수준의 최적화/RL 경험을 신입 필수조건으로 요구하지 않는다.
핵심 질문은 필요한 기초를 갖추고 실제 문제를 해결하며 성장할 수 있는가이다.
공개자료의 직접 요건과 이 시나리오의 분류·판단을 구분한다.
세부 Skill ID와 Evidence 연결 계약은 [09](09_mission1_data_specification.md)를 따른다.
기존 `data/case/talent_profile.json`의 13개 Skill/6·4·3 분류는 현재 구현이며 V2 정본으로 간주하지 않는다.
데이터 파일의 실제 변경은 후속 이관 작업이다.

# 11. Target / Derived / Actual 경계

16 FTE Demand, 12 FTE Current, 전입 +1, 전출 -1, 확정 입사 0은 SYNTHETIC Plan이다.
Forecast 12와 Gap 4는 원천 입력에서 재계산하는 Derived Value다.
초기 Forecast 75%와 목표 100%는 최종 Workforce Actual이 아니다.
Join 목표 4명과 Ready 목표를 실제 결과로 표시하지 않는다.

채용 Funnel은 [07](07_recruitment_design_specification.md#3-funnel과-capacity-plan)에 정의된
320 → 240 → 120 → 60 → 20 → 8 → 5 → 4 계획을 사용한다.
Target은 quota나 통과 기준이 아니며 실제 결과는 canonical Dataset에서 계산한다.

# 12. 시나리오 출처와 결과

기아 신입 ML Engineer 공개자료를 직무 참고로 사용하는 설계다.
현재 제공된 자료에는 지원 문항 캡처가 있으나 공고 전문과 메타데이터는 미확보다.
실제 기아의 내부 조직·인원·평가표·상세 전형·온보딩을 설명하는 것으로 표현하지 않는다.
[11 출처 등록부](11_v2_migration_specification.md#8-출처-등록부)를 따른다.

대표 지원자 3명은 Dataset v1 Freeze 후 선정한다. [07](07_recruitment_design_specification.md)의
Evidence Pattern은 Desired Contrast이며 생성 입력이 아니다. 실제 사례와 UI 표시명은 09의 Presentation Mapping으로 연결한다.
최종 합불, Offer/Join 인원, Ready/연장, 분석 결과는 아직 정하지 않는다.
Mission 1 종료는 실제 산출된 Workforce / Recruiting Process / Onboarding 결과 확인이다.
