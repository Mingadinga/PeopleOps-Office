# PeopleOps Office — Agent Instructions

## 1. Working Rule

구현을 시작하기 전에 작업과 관련된 `/docs` 문서를 먼저 읽는다.

문서와 현재 구현이 충돌하는 경우 임의로 제품 요구사항을 변경하지 않는다.
명확하지 않은 요구사항은 기존 문서의 Product Principles와 Decision Principles를 우선 적용한다.

새로운 중요한 제품, 데이터, 분석 관련 결정을 내린 경우 코드에만 남기지 말고 관련 문서에도 반영한다.

---

## 2. Product

제품명: PeopleOps Office

PeopleOps Office는 인력계획부터 채용, 온보딩, 데이터 분석까지 연결해
HR 담당자의 근거 기반 의사결정을 지원하는 업무 공간이다.

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

다음과 같은 표현을 제품 내부에 사용하지 않는다.

- 면접
- 면접관에게 보여주기 위해
- 취업
- 지원용
- 포트폴리오 평가
- 평가자에게 보여주기 위해

단, 채용 프로세스의 실제 단계로서 사용하는
'직무면접', '최종면접' 등의 용어는 사용할 수 있다.

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
INFERENCE → 직무/HR 해석
SYNTHETIC → 시나리오 데이터
ANALYSIS → 분석 결과

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

AI가 생성한 근거는 사람이 확인할 수 있어야 한다.

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

### Mission 2 — 데이터 기반 개선

새로운 인력소요
→ Mission 1 KPI Review
→ 분석 목표 설정
→ Prompt 작성
→ Python/Pandas 분석
→ EDA
→ 문제 발견
→ 원인 가설
→ 추가 분석
→ 채용 프로세스 개선
→ 다음 채용전략 설계

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

사용자의 Interaction은 주로
정보와 사고과정의 깊이를 선택하는 데 사용한다.

---

## 11. UI Language

사용자에게 노출되는 일반 UI 문구는 가능한 한 한국어를 사용한다.

고유명사 또는 업계에서 일반적으로 사용하는 기술 용어는 영문 사용이 가능하다.

예:

- Workforce Planning
- Talent Profile
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
- docs/05_ui_specification.md

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
