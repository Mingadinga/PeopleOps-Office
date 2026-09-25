# PeopleOps Office — Domain / Data Model

## 1. 목적과 책임

Business Question → Required Data → File / Field → Analysis → Decision을 연결한다.
이 문서는 도메인과 데이터 계층의 정본이며 영속 DB 설계서가 아니다.
V2 세부 필드·enum·PK/FK·생성·검증·freeze는 [09](09_mission1_data_specification.md),
Metric과 분석 방법은 [10](10_mission2_analytics_specification.md)이 소유한다.
V1의 개별 CSV 필드 목록은 09로 이동·대체했으며 서로 다른 계약을 병행하지 않는다.

## 2. 데이터 계층과 실행 경계

| 계층 | 형식 | 책임 |
|---|---|---|
| Case / Plan | JSON | Mission, 인력계획, 인재 요건, Funnel 계획, 판단·대안·근거, KPI 정의 |
| Event | CSV | 합성 지원·전형·평가·Offer·입사·온보딩·Ready 원자료 |
| Analysis | JSON | 동일 canonical Dataset을 실제 Python/Pandas로 계산한 결과 |

Case JSON + Synthetic CSV → 실제 Python/Pandas → Analysis JSON → UI.
Analysis JSON은 수작업으로 원하는 결과를 채우지 않는다.
핵심 Mission은 Case·Event·Analysis 산출물을 배포 artifact에 포함하고 외부 AI API 없이 동작한다.
영속 DB, 별도 분석 서버는 MVP 전제가 아니다.
기존 Cloudflare/Worker 흔적은 현재 실행 환경의 요소이며 실제 DB 운영이나 Vercel 배포 완료를 뜻하지 않는다.
이관 중 인프라 변경은 별도 범위다.

## 3. 경험 도메인

Mission → Stage → Scene.
Scene은 Space, Characters, Dialogue, System Action, Interaction, Evidence, Decision, Transition을 연결한다.
Room은 장소이며 채용 Stage와 동일한 식별자가 아니다.
Scene Contract는 [06](06_mission1_experience_specification.md#2-scene-contract)를 따른다.
탐색 상태(현재 Scene, 공개한 정보, 완료 Summary, 선택 Evidence)는 정본 채용 결과와 분리한다.
사용자의 선택·Reveal·카메라 이동은 결과 데이터를 변경하지 않는다.

## 4. 채용 데이터 관계

WorkforcePlan → FunnelPlan / TalentProfile → Application → StageHistory.
StageHistory → AssessmentActivity → AssessmentEvidence → EvidenceSkillLink / AssessmentObservation.
EvidenceDecision → EvidenceDecisionSource → 복수 AssessmentEvidence.
Application → FinalDecision → Offer → OfferEvent. 실제 Join/Ready는 WorkforceEvent가 소유한다.
OnboardingProfile → SkillGap / Task → WorkforceEvent; ActivityParticipant는 활동 참여 시간을 보존한다.

의미 계층은 PLAN / CANDIDATE·PROCESS / EVIDENCE / HUMAN INTERPRETATION·DECISION /
WORKFORCE OUTCOME이다. 파일 형식의 3계층과 다른 구분이며 각 사실에는 하나의 canonical owner를 둔다.

| 질문 | 데이터 책임 | 다음 판단 |
|---|---|---|
| 목표시점 인력이 충분한가? | workforce_plan의 입력과 확정 Flow, workforce_events의 Ready | Gap과 확보 방식 |
| 어떤 역량을 언제 확인하는가? | talent_profile, 원본 Evidence, 연결·관찰·조정 기록 | Must/Learnable/Plus, 후속 질문 |
| 어떤 정보와 채널을 사용할 것인가? | 채용전략 Case, applications.source_channel | 인재 유치 전략 |
| 어느 단계에서 무엇이 일어났는가? | stage_history의 시각·결과·사유 | 처리·대기·이탈 검토 |
| 실제로 입사·업무 준비가 되었는가? | offers, onboarding, workforce_events | JOINED/READY와 목표시점 Supply |
| 무엇을 다음 경력채용에 가져갈 수 있는가? | 실제 Analysis와 새로운 Capability 조건 | 운영 근거 재사용 / 가정 재설계 |

지원 건 application_id와 지원자 candidate_id를 분리하고 입사자는 employee_id로 연결한다.
Mission 1의 1인 1지원도 같은 ID로 합치지 않는다. 실명·학교·보호특성을 사용하지 않는다.

## 5. Plan / Derived / Actual

Plan은 분석 전에 정의한다. Forecast와 Gap은 Plan 원천값에서 재계산할 수 있다.
Actual은 Event에서 계산하고 Plan의 expected_conversion_rate와 혼합하지 않는다.
초기 Forecast와 최종 Available Supply도 구분한다. 신규 입사자는 목표일의 Ready 확인 없이
가용 인력으로 더하지 않는다. 같은 사람이나 확정 Flow를 중복 계상하지 않는다.

Funnel 계획은 [07](07_recruitment_design_specification.md#3-funnel과-capacity-plan),
집계 단위는 고유 candidate_id이며 Stage/Activity·시간·원자료 계약은 [09](09_mission1_data_specification.md)에 둔다.
UI 수치는 Plan 정본 또는 계산 산출물에서 가져온다. 미생성 Actual은 0이나 성공으로 표시하지 않는다.

## 6. Evidence와 Decision

PUBLIC / INFERENCE / SYNTHETIC / ANALYSIS는 정보의 출처 유형이다.
NOT_OBSERVED / LIMITED / MODERATE / STRONG은 사람의 평가 수준이며 출처 유형과 다른 축이다.
원본 assessment_evidence에는 수준을 넣지 않는다. 관찰·AI 제안·사람의 확정·최종 판단을 분리한다.
AI 요약은 원문을 대체하지 않는다.

Decision의 기존 공통 개념은 유지한다:
`decision_id`, `mission_id`, 질문, 결정, 이유, 대안, 미선택 이유, `evidence_refs`, 재검토 조건.
V1 `step` 참조는 V2 Stage/Scene으로 이관할 대상이며 실제 필드 변경은 후속 작업이다.

Evidence 참조는 기존 PUBLIC- / INFERENCE- / SYN- / ANALYSIS- 접두 구조를 사용할 수 있다.
PUBLIC에는 발행 주체·제목·원문 위치·날짜·확인 범위·공식/아카이브/캡처 구분이 필요하다.
INFERENCE는 해석의 기반을, SYNTHETIC은 Case/Event를, ANALYSIS는 데이터 버전·입력·코드·산출 항목을 추적한다.
없는 출처를 임의 ID/URL로 만들지 않는다. Source 상태는 [11](11_v2_migration_specification.md#8-출처-등록부)을 따른다.

## 7. KPI 정의와 분석

기존 KPI 정의의 `code`, 이름, 산식, 목적, 사용하는 Decision을 보존한다.
Target·Actual·단위·대상 기간·분자·분모·결측 처리·참조 데이터가 구별되어야 한다.
사용할 수 있는 분석 범주는 Workforce Fulfillment, 지원완료, Stage 전환·FAIL/WITHDRAW,
Lead Time, Offer Acceptance, Join, Ready다. 숫자를 얻을 수 있다는 이유만으로 KPI를 추가하지 않는다.

V1의 attraction_daily.csv와 Visit/Application Start Rate는 기존 개념 후보이며 V2 09의 확정 파일 목록에는 없다.
노출·방문 원자료 없이 비율을 계산하지 않는다. OPEN-12는 v0.1 KPI/원자료 계약 범위에서 해결됐으며
Attraction 효율·채널 성과·Calibration 합의율·Assessment 효과를 Mission 2 Main KPI로 미리 정하지 않는다.
Actual person-hours는 activity_participants의 참여 구간에서, 입사/Ready는 JOINED/READY_CONFIRMED에서 계산한다.
기존 Qualified Application Rate도 자격 판정 정의와 원천 데이터가 먼저 필요하며 자동 Fit Score로 대체하지 않는다.
개별 실제 사용자의 마케팅 Tracking을 도입하지 않는다.

## 8. 버전과 재현성

검토 후보 `data/generated/v0.x/` → 규칙·현실성·무결성 검토 → 승인 → `data/synthetic/v1/` freeze.
Case/Plan과 생성규칙·manifest도 해당 Dataset 버전에 연결한다.
Runtime과 Mission 2 분석은 동일한 canonical v1을 사용한다. 매 방문 랜덤 재생성은 하지 않는다.
고정 seed를 사용하되 V1의 20260921은 초기 후보였으므로 최종 seed로 자동 확정하지 않는다.
규칙 변경 시 CSV를 직접 고치지 않고 새 후보 전체를 재생성한다. 결과를 원하는 방향으로 맞추는 변경은 금지다.

## 9. 현재 구현과 목표 설계

현재 존재하는 Case는 `data/case/mission1.json`, `data/case/talent_profile.json`이다.
09의 생성기와 검토 후보 `data/generated/v0.1/`을 추가했다. freeze된 v1과 Mission 2 Analysis 결과는 아직 없다.
기존 Case/UI 데이터와 검토 후보를 연결하거나 교체하지 않았다.
application_id와 candidate_id의 분리, Stage/Activity 및 Offer 객체/이력 분리, 단일 onboarding 파일의 분할,
Evidence 수준 분리는 후속 이관 대상이다. 실제 구현 매핑은 [11](11_v2_migration_specification.md)을 따른다.

## v0.5 Application / Document contract

v0.5 adds application_eligibility.csv (raw minimal fields plus requirement states) and application_experiences.csv (same-experience actions/categories/ownership and Evidence references). Document-only CLOSED distinguishes insufficient submitted evidence from Skill limitation. Existing v1 schema/snapshot remains unchanged.

## v0.6 operational eligibility history

The requirement-level eligibility_verifications.csv links Document CONDITIONAL_ADVANCE to confirmed minimal facts, resolution and PRE entry. Initial eligibility and historical Document decisions remain unchanged. No new assessment Stage or candidate score. See 09 v0.6.

### 현재 Baseline 및 Presentation 버전

Active Baseline은 v2(source v0.6), v1은 historical / SUPERSEDED다. v1 대표 Mapping(C0003/C0005/C0228)과 현재 UI는 dataset_version=v1에 귀속되며 v2로 자동 승계하지 않는다. v2 신규 대표 선정·Mapping·UI 연결은 후속 작업이다. 승인 snapshot과 Document evidence-qualified / Eligibility-resolved PRE Entry 지표 분리는 [09](09_mission1_data_specification.md)의 v2 Baseline 계약을 따른다.
