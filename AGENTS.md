# PeopleOps Office — Agent Instructions

## 1. Working Rule

구현을 시작하기 전에 작업과 관련된 `/docs` 문서를 먼저 읽는다.

문서와 현재 구현이 충돌하는 경우 임의로 제품 요구사항을 변경하지 않는다.
명확하지 않은 요구사항은 기존 문서의 Product Principles와 Decision Principles를 우선 적용한다.

새로운 중요한 제품, 데이터, 분석 관련 결정을 내린 경우 코드에만 남기지 말고 관련 문서에도 반영한다.

---

## 2. Product

제품명: PeopleOps Office

PeopleOps Office는 인력계획부터 채용, 온보딩, 데이터 분석까지
HR 의사결정 과정을 탐색하는 인터랙티브 웹서비스다.

**People make decisions. Technology organizes evidence.**

사용자는 ICT HR 담당자의 관점에서 사람들의 업무·대화·근거·판단을 탐색한다.
운영용 HRIS, AI Recruiter, 채용 자동판단 시스템이나 분기형 게임을 만들지 않는다.

Primary User:

- ICT HR 담당자

이 제품의 핵심은 HR 업무를 자동화하는 것이 아니라 다음 흐름을 보여주고 지원하는 것이다.

Problem
→ Data
→ Evidence
→ Decision
→ Execution
→ Result
→ Analysis
→ Next Decision

---

## 3. Product Context Rule

모든 문서, 코드, 데이터 및 사용자 인터페이스는
PeopleOps Office를 독립적인 HR 업무 지원 제품으로 기술한다.

서비스 외부의 활용 목적이나 특정 평가 상황을 전제로 한 표현을
제품 산출물에 포함하지 않는다.

채용공고, 지원 문항, 직무면접, 1차면접, 2차면접 등 실제 채용 업무 용어는 사용한다.
가상 인명 대신 역할명과 필요한 업무 맥락을 표시한다.

---

## 4. Core Product Principles

### 4.1 Evidence First

주요 HR 의사결정에는 근거가 있어야 한다.

사용자는 주요 의사결정에서 다음을 확인할 수 있어야 한다.

- 무엇을 결정했는가
- 왜 결정했는가
- 어떤 데이터를 사용했는가
- 어떤 공개 근거를 사용했는가
- 어떤 대안을 검토했는가

주요 Decision UI에는 가능한 경우
`판단 근거 보기` 기능을 제공한다.

### 4.2 Evidence Type

모든 중요한 정보는 다음 네 유형 중 하나로 구분한다.

PUBLIC

- 공식 채용공고, 공식 기업자료 등 공개자료

INFERENCE

- 공개자료와 HR 원칙을 바탕으로 한 해석

SYNTHETIC

- 프로젝트에서 구성한 가상 시나리오 및 합성 데이터

ANALYSIS

- 합성 데이터를 실제 코드로 분석하여 계산한 결과

PUBLIC과 SYNTHETIC을 혼합하여 실제 기업 내부 데이터처럼 표현하지 않는다.

사용자 UI에서는 필요에 따라 다음과 같이 표시할 수 있다.

PUBLIC → 공개자료
INFERENCE → 직무 해석
SYNTHETIC → 시나리오 가정
ANALYSIS → 데이터 분석

### 4.3 Explainability by Design

주요 HR 의사결정은 서비스 내부에서 근거를 추적할 수 있어야 한다.

결과만 보여주지 않는다.

가능하면 다음 구조를 유지한다.

Question
→ Evidence
→ Reasoning
→ Decision

### 4.4 Target Before Actual

KPI Target은 분석 결과를 본 뒤 결정하지 않는다.

Target을 먼저 정의하고,
Actual은 실제 Synthetic Data에서 계산한다.

### 4.5 Do Not Predetermine Analysis Results

Synthetic Data를 특정 결론이 나오도록 직접 조작하지 않는다.

현실적인 분포와 Noise를 가진 데이터를 생성한 뒤
Python/Pandas로 실제 EDA를 수행한다.

분석 결과에서 발견된 현상을 바탕으로 다음 의사결정을 수행한다.

### 4.6 Correlation Is Not Causation

EDA에서 발견된 관계를 원인으로 단정하지 않는다.

다음 표현을 구분한다.

- 관찰된 현상
- 분석 결과
- 원인 가설
- 추가 검증이 필요한 사항

---

## 5. AI Principle

AI의 역할은 HR Copilot이다.

AI는 의사결정자가 아니다.

허용 역할:

- Evidence Retrieval
- 데이터 계산 설명
- 분석 결과 설명
- 의사결정 근거 정리
- 문서 초안 생성
- 분석을 위한 코드 또는 Prompt 작성 지원

금지 역할:

- 지원자 자동 합격/불합격
- 지원자 자동 순위화
- 불투명한 Fit Score 생성
- Culture Fit Score 생성
- 개인의 미래 성과 예측
- 개인의 퇴사 확률 예측
- 사람에 대한 최종 판단 자동화

AI 출력 자체는 Evidence가 아니며 원자료를 대체하지 않는다.
원본 Evidence → AI의 Skill 연결 후보 → 사람의 연결 확정 → 사람의 Evidence 수준 판단을 구분한다.
AI 제안은 수정·거부할 수 있다. Evidence 수준과 최종 채용·Ready 판단은 사람이 담당한다.
근거 없는 추론, 확인되지 않은 이탈 사유 추정, 보호특성 기반 판단을 하지 않는다.
Copilot은 결론 → 근거 → 출처 → 불확실성 순서로 설명한다.

---

## 6. MVP Scope

### Mission 1 — 채용 실행

Workforce Planning
→ Talent Profile
→ Attraction
→ Selection
→ Recruiting Operation
→ Onboarding
→ KPI Measurement

### Mission 2 — 분석과 경력 채용계획

새로운 경력직 인력요청(제조AI - 제조AI Agent 데이터 엔지니어링)
→ Headcount / Capability Gap
→ Mission 1 canonical Dataset을 실제 Python/Pandas로 분석
→ 관찰·가설·한계·개선
→ 신입/경력 조건 비교
→ 재사용 가능한 운영 Evidence / 재설계할 가정 분리
→ 경력 인재 요건·Sourcing·Funnel·Capacity·Assessment
→ 경력 채용계획 확정

Mission 2는 실제 경력채용 실행 완료를 뜻하지 않는다. 공개 직무의 원문 검증과
합성 인원·일정·내부 Supply 가정을 구분한다.

Core Loop:

Recruiting
→ Data
→ Analysis
→ Improvement
→ Next Recruiting

---

## 7. Out of Scope

현재 MVP에서 다음 기능을 구현하지 않는다.

- 성과관리 시스템
- 보상 시스템
- 장기 CDP
- 전사 L&D 플랫폼
- 퇴사 예측
- AI 지원자 자동 평가
- AI 지원자 Ranking
- 실사용 채용 ATS
- 다중 사용자 HR 운영 시스템

Onboarding은 전체 HRM 시스템이 아니라 다음 범위만 다룬다.

Join
→ Skill Gap
→ Ramp-up Task
→ Ready

---

## 8. Data Architecture

MVP에서는 별도의 영속 Database를 사용하지 않는다.

현재 제품은 실시간 HR 운영 시스템이 아니라
사전에 구성된 HR Case의 의사결정과 분석 과정을 탐색하는 서비스이기 때문이다.

데이터는 세 계층으로 관리한다.

### Case Data

JSON

예:

- mission
- talent profile
- recruiting strategy
- decisions
- KPI definitions

### Event Data

CSV

예:

- attraction
- applications
- recruiting stage history
- assessment evidence
- onboarding

### Analysis Data

JSON

Python/Pandas 분석을 통해 생성한다.

Flow:

Case JSON

- Synthetic CSV
  → Python / Pandas
  → Analysis JSON
  → UI

DB가 필요한 실제 요구사항이 발생하기 전까지
PostgreSQL, Supabase, Drizzle 등의 영속 DB를 도입하지 않는다.

---

## 9. Synthetic Data

Synthetic Data는 반드시 실제 기업 내부 데이터와 구분한다.

합성 데이터에는 다음과 같은 민감하거나 불필요한 개인 특성을 포함하지 않는다.

- 성별
- 나이
- 인종
- 종교
- 장애
- 혼인 여부
- 사진
- 실제 학교명
- 실제 개인 이름

다음과 같은 파생 AI 점수를 만들지 않는다.

- AI_FIT_SCORE
- CULTURE_FIT_SCORE
- SUCCESS_PROBABILITY
- PERFORMANCE_PREDICTION
- TURNOVER_PROBABILITY

Random generation은 재현 가능해야 한다.
Generator에는 fixed random seed를 사용한다.
Rule-based 생성에서 숨은 종합 능력치, 단일 pass probability, Channel을 Quality 대리변수로 쓰는 규칙을 금지한다.
Stage와 내부 Activity, FAILED/WITHDRAWN/IN_PROGRESS, Capacity와 timestamp, JOINED/READY_CONFIRMED를 구분한다.
Synthetic Evidence·Human Observation·Human Decision은 모두 SYNTHETIC이며 실제 사람의 평가 결과가 아니다.
판단 provenance와 Rubric/원근거를 추적한다. Dataset Reviewer는 개별 합불이 아닌 생성 규칙·정합성을 검토한다.
대표 사례는 v1 Freeze 후 별도 Presentation Mapping으로 선정하며 생성 입력으로 사용하지 않는다.
검토 중 후보는 `data/generated/v0.x/`, 승인 후 정본은 `data/synthetic/v1/`로 구분한다.
Runtime과 Mission 2는 동일한 freeze된 canonical Dataset을 사용하며 런타임에서 다시 생성하지 않는다.
Plan 수치는 Plan 정본, Actual은 Raw Event 계산 결과에서 가져온다. UI에 별도 결과를 하드코딩하지 않는다.
Dataset v1을 생성·검토·freeze하고 실제 분석한 후에만 Main Analysis Story 2~3개를 선택한다.
분석 결론을 만들기 위한 데이터 수정은 금지한다. 세부 계약은 docs/09와 docs/10을 따른다.

---

### Dataset Rules Audit 이후 핵심 계약

현재 데이터 SSOT는 docs/09, HR 의미는 docs/07, Migration 상태는 docs/11이다.
Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision을 보존하며 Stage Transition은 별개다.
APPLICATION_RESPONSE=SELF_REPORTED; self-reported-only STRONG Skill Decision은 금지한다.
Calibration은 persisted Observation 기반이며 Evidence Evolution/Context Difference/Evaluator Disagreement를 구분한다.
현재 v0.3/v0.4의 cycle Initial Plan은 20명 × 3h/후보 = 60h이며 quota가 아니다. 80h·4h/후보는 v0.2 보존 이력이다. Capacity 부족은 탈락 근거가 아니고 변경/예약/해제/소비 이력을 보존한다.
HOLD는 Reason+Resolution Plan·최대 1회 Focused Follow-up·새 Observation/Calibration·Re-review를 가지며 HOLD 재발행을 금지한다.
EXPIRED는 deadline과 응답 Event 부재에서 파생한다. READY_CONFIRMED는 개인별 Gap·post-join 업무 근거·사람 확인이 필요하다.
Validator는 Generator 판단 함수를 oracle로 재사용하지 않는 독립 invariants를 검사한다.
v0.1은 자동 PASS 뒤 Audit에서 D-01/modeling issues가 확인된 보존 이력이다. 문서 수정은 새 Dataset 생성/검증/Freeze 완료가 아니다.

---

## 10. UI Principle

원본 AI Office 프로젝트의 공간형 Office UI를 활용한다.

그러나 원본의 게임 구조에 PeopleOps Office의 제품 구조를 억지로 맞추지 않는다.

제품의 핵심은 게임이 아니라
Interactive HR Case Study / HR Workspace이다.

사용자가 결과를 바꾸는 Branching Simulation을 만들지 않는다.

주요 Interaction 예:

- 인력소요 확인
- 데이터 확인
- 분석 과정 보기
- 판단 근거 보기
- Copilot에게 물어보기
- 다음 단계

기본 Interaction은 Guided Exploration이며 결과는 바뀌지 않는다.
Mission 1에서 약 5~7회의 Think Before Reveal을 사용할 수 있으나 정답/오답·점수·순위를 만들지 않는다.
상위 진행도는 인력계획 / 인재 정의 / 채용 설계 / 지원자 검증 / 인재 확보 / 업무 준비다.
완료·현재·예정을 구분하고 완료 요약은 다시 볼 수 있으나 예정 단계로 Jump하지 않는다.
Room은 업무 장소, Stage는 진행 단계, Scene은 하나의 핵심 질문을 다루는 경험 단위다.
왼쪽 Human Layer와 오른쪽 Decision Layer를 연결한다. 캐릭터는 업무상 역할이 필요할 때 등장한다.
사람의 대화에는 Typing을 적용하지 않는다. 도구 처리와 코드 Reveal은 즉시 전체 표시와 reduced motion을 지원한다.
UI/UX/Interaction의 최종 정본은 docs/05_ui_specification.md다.

---

## 11. UI Language

사용자에게 노출되는 일반 UI 문구는 가능한 한 한국어를 사용한다.

고유명사 또는 업계에서 일반적으로 사용하는 기술 용어는 영문 사용이 가능하다.

예:

- 인력계획
- 인재 요건
- KPI
- Python
- Pandas
- HR Copilot

불필요한 영문 UI Label 사용은 피한다.

---

## 12. Existing Template

프로젝트는 기존 AI Office UI Template을 기반으로 한다.

원본 구조는 참고 대상이며 변경 금지 영역이 아니다.

PeopleOps Office 요구사항을 구현하기 위해 필요한 경우
기존 game 관련 코드와 component를 수정할 수 있다.

단, 큰 구조 변경 전에 현재 구현이 담당하는 역할을 먼저 파악한다.

원본 Template의 License 및 Credit 요구사항은 유지한다.

---

## 13. Development Rule

현재 우선순위:

1. 제품 흐름
2. 의사결정 설명 가능성
3. 데이터 일관성
4. 분석 재현성
5. UI 완성도
6. 추가 기술적 복잡성

필요하지 않은 Infrastructure를 추가하지 않는다.

현재 MVP에서 필요하지 않은 예:

- 별도 Backend Server
- Database
- Message Queue
- Docker
- Microservice

새 Dependency를 추가하기 전에 기존 Dependency로 해결 가능한지 확인한다.

---

## 14. Documentation

현재 핵심 문서:

- docs/00_product_scope.md
- docs/01_product_flow.md
- docs/02_mission1_scenario.md
- docs/03_decision_principles.md
- docs/04_data_model.md
- docs/05_ui_specification.md — UI/UX/Interaction
- docs/06_mission1_experience_specification.md — Mission 1 Scene
- docs/07_recruitment_design_specification.md — 채용 설계
- docs/08_hr_tech_specification.md — HR Tech / Human Decision Boundary
- docs/09_mission1_data_specification.md — 필드·enum·생성·검증·freeze
- docs/10_mission2_analytics_specification.md — 분석과 경력 채용계획
- docs/11_v2_migration_specification.md — 현재 구현에서 V2로의 이전

제품 설계는 최신 명시적 확정사항을 우선하되, 외부 기업 사실은 검증 가능한 공개 원문을 우선한다.
공식자료·2차 아카이브·사용자 캡처·요약본을 구분한다. 원문 미확보는 SOURCE NOT AVAILABLE,
검증 대기는 TO VERIFY, 미결정은 OPEN ISSUE로 기록하며 추정으로 채우지 않는다.
출처 상태는 네 Evidence 유형과 별개다. 참고자료를 이유로 Scope를 확장하지 않는다.
문서 동기화 완료는 구현 완료가 아니다. 미결정과 출처 목록은 docs/11의 통합 등록부를 확인한다.

구현이 문서의 결정사항을 변경하는 경우
관련 문서도 함께 수정한다.

---

## 15. Deployment Principle

PeopleOps Office는 별도 설치나 로그인이 필요 없는
Public Web Application으로 배포한다.

Production deployment target은 Vercel이다.

GitHub Repository와 Vercel을 연결하여
Git 기반 자동 배포를 사용한다.

Deployment Flow:

Local Development
→ Git Commit
→ GitHub Push
→ Vercel Build
→ Production Deployment

### Requirements

- Public URL을 통해 즉시 접근 가능해야 한다.
- 로그인 없이 모든 핵심 Mission을 탐색할 수 있어야 한다.
- Desktop First로 구현한다.
- 핵심 Mission Flow는 외부 AI API 없이도 정상적으로 동작해야 한다.
- Case Data와 Analysis Result는 배포 Artifact에 포함한다.
- Secret 또는 API Key를 Client에 노출하지 않는다.
- LLM 기능을 추가할 경우 Server-side API를 통해서만 호출한다.
- Production Build가 실패하는 변경사항은 완료된 작업으로 간주하지 않는다.

### Deployment Automation

- GitHub Repository를 Source of Truth로 사용한다.
- Production Branch는 `main`을 사용한다.
- `main`에 반영된 변경사항은 Vercel Production으로 자동 배포한다.
- Pull Request 또는 별도 Branch는 가능한 경우 Vercel Preview Deployment로 확인한다.
- 배포를 위해 수동으로 파일을 복사하거나 별도의 Build Artifact를 관리하지 않는다.
