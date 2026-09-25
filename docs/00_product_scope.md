# PeopleOps Office — Product Scope

## 1. Product Definition

PeopleOps Office는 인력계획부터 채용, 온보딩, 데이터 분석까지
HR 의사결정 과정을 탐색하는 인터랙티브 웹서비스다.

**People make decisions. Technology organizes evidence.**

사람의 업무·대화·근거·판단으로 이어지는 ICT 채용 프로젝트를 탐색한다.
Human Layer와 Decision Layer의 경험 규칙은 [UI 명세](05_ui_specification.md)를 따른다.

핵심 질문은 다음과 같다.

1. 어떤 인력이 필요한가?
2. 현재 인력과 필요한 인력 사이에 어떤 Gap이 있는가?
3. 어떤 인재를 확보해야 하는가?
4. 그 인재에게 어떻게 직무를 알릴 것인가?
5. 필요한 역량을 어떤 방식으로 확인할 것인가?
6. 채용 결과가 실제 인력 확보로 이어졌는가?
7. 채용 과정에서 어떤 문제가 발생했는가?
8. 다음 채용에서는 무엇을 개선할 것인가?

---

## 2. Primary User

ICT HR 담당자

사용자는 IT/SW 조직의 인력 수요를 이해하고,
이를 Talent Profile과 채용 프로세스로 변환하며,
채용 결과를 데이터로 확인하고 다음 프로세스를 개선한다.

---

## 3. Product Goal

PeopleOps Office가 보여주는 핵심 Flow:

필요한 인재 정의
→ 인재에게 직무 알림
→ 필요한 역량 검증
→ 인재 확보
→ 업무 가능한 인력으로 연결
→ 데이터 분석
→ 다음 채용 개선

---

## 4. MVP

### Mission 1

신입 Machine Learning Engineer 인력 확보

Workforce Planning
→ Talent Profile
→ Attraction
→ Selection
→ Recruiting Operation
→ Onboarding
→ KPI

### Mission 2

새로운 경력직 인력요청인 `제조AI - 제조AI Agent 데이터 엔지니어링`을 검토한다.
Mission 1 데이터를 실제 Python/Pandas로 분석하고 새로운 조건과 비교하여,
재사용할 운영 근거와 다시 설정할 모집단 가정을 구분한 뒤 경력 채용계획을 수립한다.

새 요청 → Capability Gap → Mission 1 분석 → 관찰·가설·한계 → 개선
→ 신입/경력 조건 비교 → 인재 요건·Sourcing·Funnel·Capacity·Assessment → 계획 확정

직무명 선택은 V2 제품 결정이며, 공개 업무·자격의 원문 확인 상태는
[출처 등록부](11_v2_migration_specification.md#8-출처-등록부)를 따른다.
경력채용의 실제 Offer·Join·Ready 실행은 이번 Mission의 종료 조건이 아니다.

---

## 5. HR Copilot

HR Copilot은 의사결정을 대신하지 않는다.

핵심 역할은 다음과 같다.

- 근거 탐색
- 데이터 설명
- 계산 설명
- 분석 결과 설명
- Decision 근거 정리

Human Decision은 항상 별도로 존재한다. AI 출력은 원본 Evidence가 아니다.
AI의 역량 연결 후보는 사람이 수정·거부·확정하며 수준 평가와 최종 판단도 사람이 한다.

---

## 6. Non-Goals

PeopleOps Office는 다음 제품을 목표로 하지 않는다.

- ATS
- HRIS
- 성과관리 시스템
- L&D Platform
- 실제 지원자 평가 시스템
- AI 채용 심사 시스템
- 실제 기업 인력 DB
- AI Recruiter / 후보자 Ranking / 분기형 채용 게임
- 보상·성과관리·장기 CDP·전사 L&D 플랫폼

---

## 7. Evidence

제품의 모든 핵심 정보는 다음 중 하나로 구분한다.

PUBLIC
공개된 외부 근거

INFERENCE
공개 근거를 기반으로 한 HR/직무 해석

SYNTHETIC
제품 시나리오를 위해 생성한 가상 데이터

ANALYSIS
Synthetic Data를 실제 분석하여 얻은 결과

특히 SYNTHETIC 데이터를 실제 기업 내부 데이터처럼 표현하지 않는다.

---

## 8. Deployment

PeopleOps Office는 Public Web Application으로 제공한다.

### Access

- 별도 설치 없음
- 로그인 없음
- Public URL을 통한 즉시 접근
- Desktop First

### Production

Deployment Platform:
Vercel

Source Repository:
GitHub

Deployment:

GitHub `main`
→ Vercel Build
→ Production

개발 Branch 및 Pull Request는
가능한 경우 Preview Deployment를 통해 검증한다.

### Runtime Principle

핵심 Mission은 외부 AI API에 의존하지 않는다.

Case JSON, Synthetic CSV 및 사전에 계산된 Analysis JSON은
Application과 함께 배포한다.

HR Copilot 등 LLM 기능이 추가되는 경우
API Key는 Client에 노출하지 않고
Server-side API를 통해 호출한다.

## 9. V2 범위와 문서 책임

기본 Interaction은 Guided Exploration이며 사용자의 선택으로 결과가 바뀌지 않는다.
신입 채용의 6단계 진행과 7개 업무 공간은 서로 다른 개념이다. 상세 흐름은 [01](01_product_flow.md),
Scene은 [06](06_mission1_experience_specification.md), 채용 설계는 [07](07_recruitment_design_specification.md),
AI 경계는 [08](08_hr_tech_specification.md), 데이터 계약은 [09](09_mission1_data_specification.md),
분석과 다음 계획은 [10](10_mission2_analytics_specification.md)을 따른다.

합성 인원·일정·조직·전형을 실제 기업 내부 운영처럼 표현하지 않는다.
모든 제품 산출물은 독립적인 HR 업무 지원 제품의 목적과 사용자 문제를 설명한다.
2026-09-24 V2 문서 동기화는 목표 설계의 반영이며 구현·Dataset 생성 완료를 의미하지 않는다.
