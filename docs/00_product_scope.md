# PeopleOps Office — Product Scope

## 1. Product Definition

PeopleOps Office는 인력계획부터 채용, 온보딩, 데이터 분석까지 연결해
ICT HR 담당자의 근거 기반 의사결정을 지원하는 업무 공간이다.

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

Machine Learning Engineer 인력 확보

Workforce Planning
→ Talent Profile
→ Attraction
→ Selection
→ Recruiting Operation
→ Onboarding
→ KPI

### Mission 2

Mission 1에서 발생한 데이터를 분석하여
다음 인력 확보 전략과 채용 프로세스를 개선한다.

KPI Review
→ Analysis Goal
→ Prompt
→ Python/Pandas
→ EDA
→ Finding
→ Hypothesis
→ Additional Analysis
→ Improvement
→ Next Recruiting Strategy

---

## 5. HR Copilot

HR Copilot은 의사결정을 대신하지 않는다.

다음 역할만 수행한다.

- 근거 탐색
- 데이터 설명
- 계산 설명
- 분석 결과 설명
- Decision 근거 정리

Human Decision은 항상 별도로 존재한다.

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
