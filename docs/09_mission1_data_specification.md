# PeopleOps Office — V2 Mission 1 Data Specification

## 1. 책임과 상태

최신 v0.4 계약은 §3.2의 승인 계약을 우선한다. §9는 v0.2 구현 이력이다. 기존 v0.1/v0.2와 Documentation Sync 이력을 보존한다.

Mission 1 Dataset의 파일·필드·enum·관계·생성·검증·freeze를 정의하는 SSOT다.
Audit 이전 계약의 오프라인 생성기와 Dataset v0.1이 존재한다. 자동 Validator PASS 후 Rules Audit에서 D-01 및 modeling issues를 확인했다.
현재 계약은 후속 버전의 구현 기준이며 v0.1 준수·승인 선언이 아니다. v1 Freeze와 Mission 2 분석은 수행하지 않았다.
도메인 구조는 [04](04_data_model.md), 판단 의미는 [07](07_recruitment_design_specification.md),
분석 Metric은 [10](10_mission2_analytics_specification.md)를 따른다.

Dataset Open Issues Documentation Update에서 확정한 OPEN-03/04/05/06/08/12의 의미 계약을 반영한다.
이 여섯 항목의 해결 범위와 이력은 7절과 11 문서에 남긴다. 구현·검증 완료를 뜻하지 않는다.
PK는 파일 내 고유, FK는 참조 대상에 존재해야 한다. 날짜와 timestamp를 구분한다.
모든 timestamp는 ISO 8601 offset-aware 형식이며 Dataset timezone은 Asia/Seoul이다.
정해지지 않은 세부 NULL/FK action/serialization을 새 제품 정책으로 만들지 않고 7절 Implementation Notes로 관리한다.

판단 계보는 `Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision`이다. Stage 진행, Skill 수준, 최종 채용 판단을 분리한다.
v0.1은 Audit history로 보존하며 row hand-edit하지 않는다. 문서 변경만으로 새 Dataset 생성·검증·Freeze가 완료되지 않는다.

## 2. 파일과 버전

| 구분 | 파일 |
|---|---|
| Case / Plan | workforce_plan.json, funnel_plan.json, talent_profile.json |
| Candidate / Process | applications.csv, stage_history.csv, assessment_activities.csv, activity_participants.csv, interview_capacity_events.csv, offers.csv, offer_events.csv |
| Evidence | assessment_evidence.csv, evidence_skill_links.csv |
| Human Interpretation / Decision | assessment_observations.csv, evidence_decisions.csv, skill_decision_observations.csv, final_decisions.csv |
| Workforce Outcome | onboarding_profiles.csv, onboarding_skill_gaps.csv, onboarding_tasks.csv, workforce_events.csv |
| Generation | generation_rules.json, dataset_manifest.json |

검토 후보는 `data/generated/v0.1/`, `data/generated/v0.2/` 등으로 구분한다.
승인 후 Event 정본은 `data/synthetic/v1/`에 freeze한다.
v1은 source candidate의 Case/Plan JSON과 Event CSV를 함께 `data/synthetic/v1/`에 보존한다. 별도 `data/case/v1/` 복제는 만들지 않는다.
승인 manifest·검증·Human Review snapshot·합성 가정은 `data/generation/v1/`, Active/Historical Registry는 `data/generation/baseline_registry.json`에 둔다.
생성규칙과 Generator provenance는 보존된 source candidate v0.4의 파일과 hash를 참조한다.
Plan·규칙·manifest가 어느 Event 버전을 설명하는지 명시하며 다른 버전을 혼용하지 않는다.
Manifest의 필수 버전·관측창·검증 정보는 6.3절을 따른다.
Runtime과 Mission 2는 동일 canonical v1을 사용한다. Runtime에서 generator를 실행하지 않는다.

의미 계층은 PLAN / CANDIDATE·PROCESS / EVIDENCE / HUMAN INTERPRETATION·DECISION /
WORKFORCE OUTCOME의 다섯 가지다. 각 사실은 하나의 canonical owner를 갖는다.
동일 사실의 조회용 복제·파생값이 필요하면 owner에서 재계산하며 독립적으로 수정하지 않는다.
파일 형식인 Case JSON / Event CSV / Analysis JSON 구분과 의미 계층을 혼동하지 않는다.
대표 사례는 정본 채용 데이터 밖의 Presentation Mapping에서만 관리한다(6.4절).

## 3. Case / Plan 계약

### 3.1 workforce_plan.json

| 필드 | 타입 / 제약 |
|---|---|
| plan_id | string, PK |
| baseline_date, target_date | date |
| demand_fte, current_fte | number, 인력계획 원천 입력 |
| confirmed_transfer_in, confirmed_transfer_out, confirmed_joiners | number, 유입·유출 규모. out은 식에서 차감 |
| forecast_supply_fte, workforce_gap | number, DERIVED. 저장 시에도 재계산 가능 |
| target_join, target_ready | 목표 인원. 날짜는 baseline_date/target_date와 혼동하지 않음 |

Forecast = current + transfer_in - transfer_out + confirmed_joiners.
Gap = max(demand - forecast, 0).
현재 Plan은 16, 12, +1, -1, 0 → Forecast 12 → Gap 4 FTE다.
기준일 2026-10-01, 목표일 2027-09-01은 기존 시나리오의 정밀 날짜를 유지한다.
UI 월 표기는 2027-09다. Join 목표 4와 6개월 Ramp-up은 Actual이 아니다.
초기 Forecast와 신규 Ready의 최종 공급 계산을 구분하고 같은 인력을 중복 계상하지 않는다.

### 3.2 funnel_plan.json

| 필드 | 의미 / 제약 |
|---|---|
| plan_id | 인력계획 연결 |
| stage | 아래 계획 버킷 |
| target_count | 사전에 정의한 계획 인원 |
| expected_conversion_rate | 계획 전환 가정. Actual 아님 |
| unit_effort_person_hours | 후보당 노력 시간 |
| available_capacity_person_hours | 가용 평가자 시간 |
| assumption_note | 계획 근거·제약·Trade-off |
| evidence_type | 시나리오 계획은 SYNTHETIC |

| 계획 stage | UI Target 라벨 | target_count | Actual의 canonical 근거 |
|---|---|---:|---|
| APPLICATION_STARTED | 지원 시작 | 320 | applications.started_at의 고유 candidate |
| APPLICATION_SUBMITTED | 지원 완료 | 240 | applications의 SUBMITTED / submitted_at |
| DOCUMENT_SCREEN | 서류 통과 | 120 | DOCUMENT_SCREEN의 ADVANCED |
| PRE_ASSESSMENT | 사전검증 통과 | 60 | PRE_ASSESSMENT의 ADVANCED |
| FIRST_INTERVIEW | 1차면접 계획 인원 | 20 | FIRST_INTERVIEW에 Entered인 고유 candidate |
| SECOND_INTERVIEW | 2차면접 대상 | 8 | SECOND_INTERVIEW에 Entered인 고유 candidate |
| OFFER | Offer | 5 | offers와 OFFERED 이력으로 확인한 고유 candidate |
| JOIN | Join 목표 | 4 | workforce_events의 JOINED에 연결된 고유 candidate |

Target / Capacity Plan이며 quota·pass threshold가 아니다. Actual을 이 숫자에 강제로 맞추지 않는다.
v0.3 FIRST_INTERVIEW의 계획 unit effort는 60분 ÷ 60 × 평가자 3명 = 3 person-hours다.
v0.3 Initial Capacity Plan은 3h × 계획 인원 20명 = 60h다.
이는 계획이며 Actual effort는 activity_participants의 시각으로 계산한다.
계획 버킷의 라벨과 Stage lifecycle 상태는 다르다. 이름만으로 merge하지 않는다.
계획 JSON의 배열 구조·키 직렬화는 Implementation Note로 남기며 Actual을 Plan에 저장하지 않는다.



### v0.4 Final Dataset Candidate — 최종 Human Review 계약

v0.4부터 이 계약이 아래 v0.3/v0.2 보존 이력보다 우선한다. 기존 Dataset과 생성 규칙/보고서는 변경하지 않는다.
Coverage ≠ Skill Sufficiency ≠ Pass Score다. FIRST 책임 핵심 MUST01/02/03 각각에 해당 FIRST 평가영역의
Skill 연결된 직접 Observation과 AGREED Skill Decision이 있어야 한다. 일치된 LIMITED/MODERATE/STRONG은
판단 가능한 근거로 Coverage에 포함한다. NOT_OBSERVED, unresolved, SELF_REPORTED-only, 미연결 근거는 제외한다.
Coverage는 Skill별 decisionable Boolean과 Observation/Skill Decision 참조로 남기며 점수·Ranking·quota를 만들지 않는다.

기존 A/B/C/D 설명은 유지하되 B의 직접 LIMITED는 decisionable=true일 수 있다. Coverage 충족이 자동 진행을 뜻하지 않는다.
v0.3의 명시적 핵심 limitation 비진행 기준(긍정 반증 없이 AGREED LIMITED이고 직접 검증 미실행 확인)은 별도 판단으로 유지한다.
그 근거가 있으면 FAILED, 없고 핵심 Coverage가 모두 충족되면 ADVANCED다. 나머지는 IN_PROGRESS/EVIDENCE_PENDING이다.
평가 미완료·무응답과 완료 후 근거 부족/미해결을 rationale로 구분하며 근거 부족을 Skill 부족으로 변환하지 않는다.

Calibration은 동일 직접 Evidence에 대한 평가자/Rubric 해석 차이 또는 직접 Evidence 간 의미 있는 충돌이 있을 때만 수행한다.
현재 합성 모델의 명시적 trigger는 (1) 이번 검토의 동일 Evidence에서 proposed_level이 다름,
(2) 이번 Observation을 포함한 동일 Skill/직접 context에서 서로 다른 Evidence의 명시적 제한과 긍정 관찰이 충돌함이다.
이는 판단에 영향을 주는 unresolved uncertainty의 구현 표현이다. 이전 다른 맥락의 LIMITED와 후속 긍정 근거 차이만으로 trigger를 만들지 않는다.
모두 같은 LIMITED 또는 모두 NOT_OBSERVED인 경우 그 사실만으로 회의를 만들지 않는다. 추가 원자료가 필요한 것과 평가 해석 조정을 구분한다.
먼저 Observation을 저장하고 trigger를 확인한 뒤 필요한 회의만 수행한다. 회의가 없어도 Skill Decision lineage는 필수다.
발생 여부는 후보자 품질이나 선발 가점/감점으로 사용하지 않는다.

면접 60분/3명, 계획 20명×3h=Initial 60h와 별도 Calibration Actual 비용 계약은 유지한다.
Evaluator pool 규모는 제품 정책/기아 운영 인원이 아닌 generation parameter다. 이번 후보에서는 v0.3과 동일한 30명을 유지한다.
동일 pool 각 평가자의 추가 시간 배분과 예약/소비/해제 기록을 유지하며 Funnel을 맞추기 위해 pool 규모를 바꾸지 않는다.

Targeted Follow-up 입력(Reason/Skill/기존 Evidence·Observation/질문), 최대 1회와 새로운 직접 근거 생성 방식은 유지한다.
Re-review PROCEED에는 모든 MUST가 직접 근거에 기반한 AGREED LIMITED/MODERATE/STRONG으로 판단 가능해야 한다.
이는 필요조건이지 LIMITED의 충분성을 자동 승인하는 규칙이 아니다. 기존 명시적 제한/상충에 대한 비진행 기준은 별도 적용한다.
최대 1회 후에도 MUST 자체가 미관찰/미해결이면 DO_NOT_PROCEED로 종료하며, 이유는 '판단 근거 미확보로 이번 채용 진행 불가'다.
역량 부족을 확인했다고 기록하거나 Stage FAILED로 소급하지 않는다. RE_REVIEW에서 HOLD를 다시 만들지 않는다.
감수 가능한 불확실성은 판단 가능한 MUST의 비핵심 Context 또는 Learnable 영역에 한정하고 rationale과 지원 범위를 명시한다.
MUST의 판단불가능 상태를 accepted uncertainty로 숨기는 것을 금지한다.

Implementation Note:
`calibration_reviews.csv`는 검토 기회마다 review_id, stage_event_id, review_round(INTERVIEW/FOLLOW_UP),
evaluated_at, observation_ids(JSON), trigger_codes(JSON), activity_id(nullable), rationale를 기록한다.
대상은 완료된 FIRST/SECOND 면접 또는 완료된 Targeted Follow-up의 신규 직접 Observation이다.
Eligible은 검토 기회 수, Triggered는 trigger가 확인된 수, Actual은 관측창 내 완료된 Calibration Activity 수다.
관측창 밖/미완료 Activity는 Actual 비용에 보간하지 않는다. 회의 참여자는 2명·15분의 기존 합성 parameter를 유지한다.
Re-review rationale에 must_not_decisionable과 decision_basis를 남기고 독립 Validator가 실제 snapshot/lineage와 대조한다.
초기 Final Review의 HOLD 계약, Source Matrix, Offer/READY 분포, seed 20260924 및 Target/Actual 독립은 유지한다.

### v0.3 Interview / Decision Model — 승인 계약 (2026-09-25)

이 절은 v0.3 검토 후보부터 적용한다. 아래 v0.2 Decision Note와 수치는 변경 전 이력이며 새 계약을 대체하지 않는다.
공개 후기의 1:3·60분/2차 약 30분은 사용자가 제공한 2차 참고자료다. 원문·대표성은 미검증이며
기아 공식 정책이 아니다. 채택한 운영은 PeopleOps Office의 SYNTHETIC 시나리오다.

- FIRST_INTERVIEW: 지원자 1명, 재사용 패널 평가자 3명, 단일 60분 Session, 면접 노력 3 person-hours.
  TECHNICAL_ASSESSMENT / AI_CASE / PRACTITIONER_QA는 이 Session의 Evidence 평가영역이다.
  영역은 별도 참여시간을 갖지 않으며 Session만 시간을 소유한다. Calibration은 면접시간 밖의 별도 Activity다.
- Plan: 20명 × 3h = Initial 60h. 20명은 quota가 아니다. Target/Actual은 독립이다.
  Initial → 실제 면접 Demand → Gap → Human Decision → 추가 evaluator hours → Revised → Reservation → Consumption/Release를 보존한다.
  Capacity 부족은 FAILED를 만들지 않는다. 최초 계획을 덮어쓰거나 Offer/Join에서 자원을 역산하지 않는다.
- SECOND_INTERVIEW: 지원자 1명, 합성 평가자 2명, 30분. Skill04/05의 학습·협업·Values & Behaviors 및 과거 행동을 확인하며 기술평가를 반복하지 않는다.
- Observation을 먼저 저장한다. 직접 근거의 LIMITED/NOT_OBSERVED 또는 평가자 이견이 있으면 해당 stage/round의 별도 Calibration을 수행한다.
  없으면 회의 없이 Observation 기반 Skill Decision을 기록한다. Calibration은 Stage 합불을 생성하지 않는다.
- FIRST → SECOND Coverage: Assessment Matrix의 기술 핵심 Must01(구조화), 02(ML/수리), 03(구현/검증)을 각각 확인한다.
  FIRST 영역의 직접 근거에서 평가자들이 MODERATE/STRONG으로 일치한 지지가 있고, 누적 Skill Decision도 AGREED MODERATE/STRONG이어야 A(충족)다.
  A 세 항목을 모두 확보해야 ADVANCED다. MUST04/05는 2차 행동 검증으로 이어지므로 여기서 모두 STRONG을 요구하지 않는다.
  B는 직접 관찰로 명시적 검증 미실행이 확인되고 긍정 반증 없이 AGREED LIMITED인 핵심 Skill이며 FAILED 근거가 된다.
  C(직접 근거 미관찰/부족), D(평가자 이견 또는 미해결)는 IN_PROGRESS / EVIDENCE_PENDING으로 남긴다.
  B가 없고 A가 부족한 경우 추가 Stage나 자동 탈락을 발명하지 않는다. 관측창 내 추가 검증이 없는 pending은 그대로 보존한다.
  Coverage는 Skill별 범주와 원 Observation 참조이며 총점·순위·인원 cut이 아니다.
- HOLD 후속검증은 INITIAL HOLD의 이유, unresolved Skill, 기존 Evidence/Observation ID와 질문을 입력으로 받는다.
  질문별 응답은 누락 산출물 제출/미제출/검증 생략, 한계 재검증/한계 확인/질문 미해소, 개인 기여 확인/공동 범위 확인/범위 불명확으로 구분한다.
  일반 Assessment의 독립 패턴 lottery를 호출하지 않는다. 질문별 명시적 응답 옵션을 동일 가중치로 추출하며 결과 통과 방향을 강제하지 않는다.
  새 Evidence에 입력 snapshot·기존 원근거의 맥락/미해결 Observation을 반영한 질문과 응답 종류를 보존하고 새 Observation→필요시 Calibration→Re-review를 수행한다.
  최대 1회, Re-review HOLD 금지, 미관찰만으로 자동 실패 금지 및 기존 Offer/READY 계약은 유지한다.

Implementation Notes (결과 생성 전 고정):

- 고정 10개 패널 × (ML_ENGINEER, HIRING_MANAGER, TECHNICAL_REVIEWER) = stable evaluator 30명.
  최초 면접 예산은 evaluator당 2h로 총 60h. 추가 자원은 같은 pool 각 evaluator의 1h 할당 단위다.
  추가시간 = ceil(Gap / 30h) × 30h; 80h panel 증설을 사용하지 않는다. Human Decision에 evaluator별 추가시간과 대안을 남긴다.
  pool 규모는 수요나 Funnel에 따라 증감하지 않는다. 주 2회 패널 slot은 단순 일정 가정이며 상세 개인 업무 Calendar가 아니다.
- Calibration 참여자는 해당 합성 pool의 ML_ENGINEER/HIRING_MANAGER 2명, 15분이다.
  면접 예산과 별도 운영 노력으로 예약/소비를 기록하며 Interview Initial/Revised에 섞지 않는다. 총 운영비는 둘을 명시적으로 합산한다.
- activity_sessions.csv: activity_id(PK/FK, 평가영역), session_activity_id(FK, FIRST_INTERVIEW_SESSION).
  영역 timestamp는 Session 완료시각의 Evidence 기록 시점(0분)이다. 평가자 참여구간은 부모 Session에만 기록한다.
- evaluator_reservations.csv: allocation_id(PK), stage_event_id(FK), activity_id(nullable FK), participant_id,
  purpose(INTERVIEW/CALIBRATION), event_type(RESERVED/CONSUMED/RELEASED), person_hours, effective_at, reason_code.
  면접 예약은 stage별 evaluator 1h씩이며 aggregate capacity_assignments와 대조한다. 취소/철회/무응답의 미사용분은 가용량으로 반환한다.
- targeted_followups.csv: evidence_id(PK/FK), hold_decision_id(FK), skill_id, hold_reason, question,
  existing_evidence_ids/existing_observation_ids(JSON), response_kind. 입력은 HOLD 시점 snapshot이며 미래/타인 근거를 금지한다.
- 3명 참여와 개별 Observation을 연결한다. Calibration 판단은 persisted Observation만 소비한다.
  기존 v0.1/v0.2 및 규칙/보고서는 보존하고 seed 20260924, 기존 일반 Evidence·Offer·Ready 응답 가중치를 유지한다.
- 독립 Validator는 Session 60분/3명/단일 시간 소유, 60h/3h/자원 산식·원장 replay, Coverage, targeted input/output provenance를 검사한다.
  Generator의 해석/Calibration/전환/최종 판단 함수를 oracle로 재사용하지 않는다. 자동 PASS는 현실성 승인/Freeze가 아니다.

### FIRST_INTERVIEW Capacity 운영 계약 — v0.2 보존 이력

80 evaluator person-hours는 전체 채용 cycle의 INITIAL_PLAN이다.
`(면접 90분 + 평가/Calibration 30분) × 평가자 2명 = 후보당 계획 4 person-hours`이므로
20명은 planned operational capacity이며 합격 정원·quota·평가 cut-off가 아니다.
`Initial Plan → Demand → Gap → Human Decision → Revised Capacity → Actual Consumption` 이력을 보존한다.
Capacity 부족을 candidate FAILED 근거로 쓰지 않는다. Mission 1에서는 추가 평가자 Resource 확보를 사람의 운영 결정으로 탐색한다.
기간 조정·평가방식 변경 등의 대안과 이유를 남기며 최초 계획을 덮어쓰지 않는다.

**Decision Note — v0.2 Capacity Revision 근거 확인 (2026-09-25)**

아래는 저장된 v0.2의 계산·사건을 읽어 확인한 기록이다. Dataset 재생성·Freeze·새 운영 정책 승인이 아니다.
규칙은 `data/generation/v0.2/generation_rules.json`, 사건은 `data/generated/v0.2/interview_capacity_events.csv`다.
`capacity.py::Capacity.plan`과 `generate.py::Generator.process`를 따라 다음 계보를 확인했다.

| 구분 | 실제 입력·계산 및 기록 |
|---|---|
| Initial Plan | `CAP_0000`, 2026-10-01T00:00:00+09:00, 80h. 계획 4h × 20명과 일치 |
| Demand | PRE_ASSESSMENT ADVANCED 후 통보된 전체 cohort 192명 × 4h = 768h. application ID 목록을 보존 |
| Capacity Gap | `CAP_0001`, 2026-12-06T14:04:00+09:00, max(768−80, 0) = 688h. 예산 증감 아님 |
| Human Decision | `CAP_0002`, Gap 확인 2일 뒤 2026-12-08T14:04:00+09:00. `HR_OPERATIONS_01`이 `ADD_EVALUATOR_RESOURCES` 선택. 대안 `EXTEND_WINDOW` / `REDESIGN_ASSESSMENT` 기록 |
| Added Capacity | 규칙 `additional_panel_person_hours=80`; 추가 panel = ceil(688/80) = 9개, 추가 시간 = 9×80 = 720h |
| Revised Capacity | 80 + 720 − cycle 예산 회수 0 = **800h**. Initial panel 1개 + 추가 9개 = 10개 pool panel |

Human Decision의 provenance는 `SYNTHETIC_HUMAN_SCENARIO`다. 실제 담당자의 승인 증빙이 아니라,
추가 평가자 확보를 선택한 가상 운영 판단을 Generator가 기록한 것이다. 80h 단위 확보와 2일 지연은
합성 구현 가정이며, 왜 실제 조직에서 이 단위·규모의 자원을 확보할 수 있는지는 이 Dataset으로 증명하지 않는다.
800h는 768h 수요에 대한 80h block 올림 결과여서 32h 여유가 생긴다. Join 4/56이나 Offer 86을 역산한 값이 아니다.
추가 panel은 `Capacity.next_slot`의 일정 배정에도 사용되므로 관측창 내 진행량에 영향을 줄 수 있지만,
Capacity 수치 자체는 `stage_transition_decision` / `final_review`의 선발·탈락 조건이 아니다.
자원 결정이 관측창을 넘으면 `CAPACITY_WAIT` / IN_PROGRESS를 유지하며 Capacity 부족만으로 FAILED를 만들지 않는다.

구현 표현의 한계도 구분한다. Initial 80h는 실행 중 `target_count × unit_effort`로 산출하지 않고
`capacity.initial_person_hours=80`을 읽는다. Plan 직렬화에도 4/80 상수가 있고 target_count=20은 별도로 읽는다.
현재 값들은 4×20=80 계약과 일치하지만, 자동으로 연결된 단일 계산식이라고 설명하지 않는다.
Revised Capacity를 Funnel/목표 채용인원에 맞춰 역산하는 규칙은 허용하지 않는다.

participant_id는 Activity마다 새로 만들지 않고 reusable synthetic evaluator pool에서 재사용하며 동일 ID의 역할은 일관된다.
AVAILABLE은 사용 가능한 잔여시간, RESERVED는 배정했으나 미사용인 예약, CONSUMED는 실제 참여시간이다.
시작 전 취소/확인된 철회의 미사용 예약은 released되어 AVAILABLE로 돌아가며 이미 consumed된 시간을 되돌리지 않는다.
예약 해제는 cycle 예산 회수(CAPACITY_RELEASED)와 다르다. NO_RESPONSE로 미사용 예약을 해제할 수 있어도
별도 확인 없이 후보자를 WITHDRAWN으로 바꾸지 않는다. 상세 근무 Calendar는 합성하지 않는다.
Actual은 activity_participants의 실제 평가자 참여구간 합으로 계산하고 결측을 계획 4h로 채우지 않는다.

### 3.3 talent_profile.json

| 필드 | 의미 |
|---|---|
| skill_id | 안정적인 Skill 식별자, PK |
| skill_name | 역량명 |
| requirement_type | MUST / LEARNABLE / PLUS |
| description | 정의 |
| expected_evidence | 확인할 근거 |

Job과 Skill의 표시 문자열을 ID로 사용하지 않는다. job_id는 `M1_ML_ENGINEER`,
Skill은 `M1_SKILL_01`부터의 안정적인 ID로 관리하고 라벨 변경으로 ID를 변경하지 않는다.
02/07의 MUST 다섯 항목 순서에 M1_SKILL_01~05, Production Learnable에 M1_SKILL_06을 대응한다.
PLUS 세 항목은 02의 순서에 M1_SKILL_07~09를 대응한다. 기존 13개 Skill 데이터의 실제 이관은 별도 작업이다.
기존 talent_profile의 출처·해석·분류 이유와 source_reference/evidence_refs 추적은 보존해야 한다.
전문가 수준 최적화/RL 요구를 임의 추가하지 않는다.

## 4. Synthetic Event 계약

### 4.1 applications.csv

지원 건의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| application_id | PK. 지원 건 식별자 |
| candidate_id | 지원자 식별자. application_id와 구분 |
| job_id | Case의 stable Job ID |
| source_channel | CAREER_SITE / TECH_COMMUNITY / CAMPUS / RECRUITING_EVENT |
| started_at | 지원 시작 시각 |
| submitted_at | 제출 시각, 미제출이면 NULL |
| application_status | STARTED / SUBMITTED / ABANDONED |

Mission 1에서 1 candidate = 1 application이어도 두 ID를 합치지 않는다.
이하 application_id는 이 파일을 참조하며 동반 candidate_id는 해당 지원 건의 지원자와 일치해야 한다.
SUBMITTED에는 submitted_at이 필요하고 ABANDONED에는 NULL이다. submitted_at >= started_at이다.
평가 점수·최종 결과를 넣지 않으며 포기 사유를 추정하지 않는다.
기존 application_started_at/application_submitted_at 명칭은 started_at/submitted_at으로 대체한다.

### 4.2 stage_history.csv

채용 Process lifecycle의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| stage_event_id | PK |
| application_id, candidate_id | 지원 건과 지원자 연결 |
| stage | DOCUMENT_SCREEN / PRE_ASSESSMENT / FIRST_INTERVIEW / SECOND_INTERVIEW / FINAL_REVIEW |
| entered_at | 내부 처리 또는 lifecycle 시작 |
| invited_at | 참여 요청/안내. 해당 개념이 없으면 NULL 가능 |
| scheduled_at | 예약된 활동의 예정 시각. 해당 개념이 없으면 NULL 가능 |
| completed_at | 지원자가 해당 Stage의 요구 활동을 완료한 시각. 미완료면 NULL |
| decision_at | 결과를 확정한 시각. 결정 전이면 NULL |
| notified_at | 확정 결과 통보 시각. 통보 전이면 NULL |
| withdrawn_at | 이탈 확인 시각. 이탈하지 않았으면 NULL |
| result | ADVANCED / FAILED / WITHDRAWN / IN_PROGRESS. FINAL_REVIEW 완료 시 NULL 허용; 상세 의미는 아래 계약 |
| decision_reason_code | 판단 사유. FAILED의 설명 가능한 근거 필요 |
| withdrawal_reason_code | 확인한 이탈 사유. 미확인 UNKNOWN |
| decision_provenance | 합성 평가 판단이 있는 레코드에 SYNTHETIC_HUMAN_SCENARIO |

Offer와 Join은 Stage Result가 아니다. 해당 사실은 offers/offer_events와 workforce_events가 소유한다.
FAILED와 WITHDRAWN의 사유를 혼용하지 않는다. 연락 두절에서 다른 회사 합격·처우 불만을 추정하지 않는다.
Entered/Completed는 각각 entered_at/completed_at에서, Advanced/Failed/Withdrawn/In Progress는 result에서 구분한다.
Completed는 별도 최종 result가 아니며 평가 완료 뒤 IN_PROGRESS일 수 있다.
이전 DOCUMENT_SCREENING, PASS/FAIL/WITHDRAW enum은 위 계약으로 대체한다.

### Stage Decision Contract

| Stage | Decision Question / ADVANCED 의미 | FAILED 허용 범위 |
|---|---|---|
| DOCUMENT_SCREEN | 기본요건과 Evidence Candidate를 발견하여 후속 검증으로 진행할 수 있는가? / 진행을 막는 근거가 확인되지 않음 | 해당 단계에서 확인 가능한 명시적 기본요건 미충족 |
| PRE_ASSESSMENT | 직접 직무평가에 필요한 기초 Evidence가 확보됐는가? / 사전검증 완료 후 직접평가로 진행 가능 | 사전 정의된 직접 Task 기준에서 확인된 비진행 근거 |
| FIRST_INTERVIEW | 핵심 MUST 판단에 필요한 직접 Evidence가 확보됐는가? / 다음 판단에 사용할 근거 확보 | 직접 Evidence에서 확인된 중요 MUST의 제한과 해당 단계 비진행 근거 |
| SECOND_INTERVIEW | 협업·학습·Values & Behaviors의 행동 Evidence가 확보됐는가? / 필요한 행동 근거 확보 | 사전 정의된 행동 기준에서 확인된 비진행 근거 |
| FINAL_REVIEW | 전체 근거로 Offer 여부를 판단할 수 있는가? | 결과는 final_decisions가 소유하며 Stage result로 합불을 표현하지 않음 |

Stage Transition Decision과 Final Hiring Decision은 별개다. ADVANCED는 Skill 확정이나 최종 합격이 아니다.
DOCUMENT_SCREEN은 Skill 확정이 아닌 Evidence Candidate와 후속검증 대상 발견이다.
NOT_OBSERVED / INSUFFICIENT_EVIDENCE / 미확인 자체를 Skill 부족으로 바꾸어 자동 FAILED 처리하지 않는다.
WITHDRAWN은 확인된 지원자 이탈이며 NO_RESPONSE만으로 추론하지 않는다.
PROCEED_TO_OFFER / DO_NOT_PROCEED / HOLD는 FINAL_REVIEW의 final_decisions만 소유한다.

FINAL_REVIEW 행은 lifecycle만 보존한다. 평가 결과에 해당하지 않는 result는 NULL로 두고,
진행 중에는 IN_PROGRESS, 확인된 철회에는 WITHDRAWN을 쓴다. 완료된 Final Review를 ADVANCED/FAILED로 복제하지 않는다.

### 4.3 assessment_evidence.csv

Raw Evidence의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| evidence_id | PK |
| activity_id | 원자료가 연결된 assessment_activities 참조 |
| application_id, candidate_id | Activity와 동일한 지원 건/지원자 |
| source_type | APPLICATION_RESPONSE / CODING_TEST_RESPONSE / TECHNICAL_ASSESSMENT_RESPONSE / AI_CASE_RESPONSE / INTERVIEW_RESPONSE |
| verification_mode | SELF_REPORTED / DIRECT_TASK / DIRECT_INTERACTION / BEHAVIORAL_INTERACTION |
| source_ref | 원자료 위치 참조 |
| raw_evidence | 관찰 가능한 합성 원답변·과제 등 |
| created_at | 생성/기록 시각 |

해석·Skill Level을 넣지 않는다. Synthetic Evidence이며 실제 지원자의 원자료가 아니다.
역량검사의 실제 문항·심리 프로파일은 생성하지 않는다.
지원 답변처럼 Activity 이전에 생성되는 원자료의 activity_id 연결/NULL 표현은 7절 Implementation Note로 남긴다.

### Source-specific Evidence / Verification Mode

| Source / Activity | verification_mode | 확인 범위 |
|---|---|---|
| APPLICATION_RESPONSE | SELF_REPORTED | 경험·역할·행동·결과의 자기기술, 후속 검증 후보 |
| CODING_TEST_RESPONSE | DIRECT_TASK | 구현·검증 기본기 |
| TECHNICAL_ASSESSMENT_RESPONSE | DIRECT_TASK | 결과 해석·목표·변수·제약 |
| AI_CASE_RESPONSE | DIRECT_TASK | 문제 정의·접근·결과 검증·한계 |
| PRACTITIONER_QA의 INTERVIEW_RESPONSE | DIRECT_INTERACTION | 설명·질의에서 직접 확인한 근거 |
| VALUES_BEHAVIOR_INTERVIEW의 INTERVIEW_RESPONSE | BEHAVIORAL_INTERACTION | 구체적 행동과 후속 확인 |
| FOCUSED_FOLLOW_UP | DIRECT_TASK / DIRECT_INTERACTION / BEHAVIORAL_INTERACTION | 실제 추가 확인 방식에 대응 |

source_type은 원자료 종류, activity_type은 평가 활동, verification_mode는 확인 방식이다.
지원 답변은 구체적인 STRONG Observation을 가질 수 있으나 SELF_REPORTED-only STRONG Skill Decision은 금지한다.
STRONG Skill Decision에는 해당 Skill 판단을 지지하는 non-SELF_REPORTED Evidence의 Observation이 최소 하나 필요하다.
이는 필요조건이며 직접검증 근거가 있다는 사실만으로 STRONG을 자동 확정하지 않는다.
지원 답변의 Observation을 일괄 MODERATE 이하로 제한하지 않는다.

### 4.4 evidence_skill_links.csv

Evidence와 Skill 관계의 제안 및 사람 확인 기록이다.

| 필드 | 제약 / 의미 |
|---|---|
| link_id | PK |
| evidence_id | FK → assessment_evidence |
| suggested_skill_id | nullable, 값이 있으면 talent_profile의 Skill |
| suggestion_source | AI/System 제안 또는 사람의 직접 연결을 구분 |
| confirmed_skill_id | nullable, 값이 있으면 talent_profile의 Skill |
| confirmation_status | PENDING / CONFIRMED / MODIFIED / REJECTED |
| confirmed_by, confirmed_at | 합성 확인 역할/시각 |
| decision_provenance | 확인 판단이 있는 레코드에 SYNTHETIC_HUMAN_SCENARIO |

AI/System 제안은 확정 관계가 아니다. AI 제안 없이 사람 연결도 가능하며 원 제안을 덮어쓰지 않는다.
수준 판단을 이 관계 제안으로 대체하지 않는다.

### 4.5 assessment_observations.csv

가상 평가자의 Observation이며 최종 Skill Decision이 아니다.

| 필드 | 제약 / 의미 |
|---|---|
| observation_id | PK |
| evidence_id | FK → assessment_evidence |
| application_id, candidate_id | Evidence의 지원 건/지원자와 일치 |
| skill_id, rubric_id | 확인된 Skill 연결 및 적용 Rubric 식별자. Skill은 talent_profile 참조 |
| evaluator_id, evaluator_role | 합성 평가자 stable ID/역할. 실제 인명 아님 |
| observation_text | Evidence를 참조하는 관찰 |
| proposed_level | NOT_OBSERVED / LIMITED / MODERATE / STRONG |
| created_at | 기록 시각 |
| decision_provenance | SYNTHETIC_HUMAN_SCENARIO |

UI 수준은 확인되지 않음 / 제한적 / 충분 / 강함이다. 숫자·평균·숨은 능력치로 변환하지 않는다.
NOT_OBSERVED는 0점이나 역량 없음이 아니다. 평가자별 관찰을 개별 보존한다.

Observation은 하나의 저장된 Evidence와 확인된 Skill 연결을 추적한다. 평가자는 관찰 가능한 범위만 기술한다.
후속 판단 변경에도 기존 Observation을 덮어쓰지 않는다.

### 4.6 evidence_decisions.csv

Calibration 이후 지원 건의 Skill별 판단 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| decision_id | PK |
| application_id, candidate_id | 판단 대상 지원 건/지원자 |
| skill_id | FK → talent_profile |
| final_level | Evidence Level. 미합의/근거부족에서 확정 수준을 임의 채우지 않음 |
| decision_status | AGREED / DISAGREEMENT_REMAINS / INSUFFICIENT_EVIDENCE |
| rationale | 근거·Rubric에 따른 판단 이유 |
| decided_by, decided_at | 합성 판단 역할/시각 |
| decision_provenance | SYNTHETIC_HUMAN_SCENARIO |

Skill Decision은 최소 하나의 저장된 Observation을 4.14 relation으로 연결한다. Raw Evidence 직접 relation은 사용하지 않는다.
Rubric을 다시 검토하며 평균으로 합의를 만들지 않는다. 세부 NULL/버전 저장 방식은 Implementation Note다.

Calibration은 persisted `assessment_observations`를 입력으로 사용하고 원 Evidence·Verification Mode·Context·Rubric을 함께 검토한다.
Raw Evidence를 별도 경로로 재해석해 Observation을 우회한 Skill Decision을 만들지 않는다.

- Evidence Evolution: 후속 직접검증으로 초기 불확실성이 해소되거나 근거가 추가됨.
- Context Difference: 서로 다른 Task/상황에서 관찰된 내용의 차이.
- Evaluator Disagreement: 동일/관련 근거에 대한 평가자 해석 차이 또는 직접검증 근거 간 의미 있는 충돌.

이전 LIMITED/NOT_OBSERVED와 이후 MODERATE/STRONG의 차이만으로 DISAGREEMENT_REMAINS를 만들지 않는다.
최신 근거를 자동 우선하지 않으며 이전 Observation을 수정·삭제하지 않고 새 Observation과 Decision 이력을 추가한다.
AGREED는 연결된 Observation과 Rubric 검토 후 합의, DISAGREEMENT_REMAINS는 검토 후에도 남은 충돌,
INSUFFICIENT_EVIDENCE는 판단 근거 부족이며 Skill 부족이 아니다.

### 4.7 final_decisions.csv

최종 채용 판단의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| final_decision_id | PK |
| review_round | INITIAL / RE_REVIEW |
| application_id, candidate_id | 판단 대상 지원 건/지원자 |
| must_evidence_status | 필수 근거 확인 상태 |
| remaining_uncertainty | 남은 불확실성 |
| learnable_gap_summary | 학습 가능한 Gap |
| decision | PROCEED_TO_OFFER / DO_NOT_PROCEED / HOLD |
| hold_reason_code | MISSING_EVIDENCE / UNRESOLVED_EVIDENCE / EVALUATOR_DISAGREEMENT. HOLD 외 NULL |
| resolution_plan | HOLD의 질문·Skill·Context·추가 확인 방법. HOLD 외 NULL |
| follow_up_activity_id | nullable FK → assessment_activities, INITIAL HOLD 이후 수행된 FOCUSED_FOLLOW_UP |
| rationale | 설명 가능한 판단 이유 |
| decided_by, decided_at | 합성 판단 역할/시각 |
| decision_provenance | SYNTHETIC_HUMAN_SCENARIO |

총점·Ranking·Fit Score·개인 성공확률을 저장하지 않는다. 상세 생성 원칙은 6.1절을 따른다.

### HOLD / Focused Follow-up / Re-review

HOLD는 terminal outcome이나 후보자 결함이 아니라 해소 가능한 판단 정보가 남은 상태다.
INITIAL HOLD에는 Reason(`MISSING_EVIDENCE / UNRESOLVED_EVIDENCE / EVALUATOR_DISAGREEMENT`)과 Resolution Plan이 필수다.
Plan은 확인할 질문·Skill·Context·방법을 명시한다. 한 application당 최대 1회 FOCUSED_FOLLOW_UP으로 해당 범위만 확인한다.
`Reason + Resolution Plan → Focused Follow-up → new Evidence → new Observation → Calibration → RE_REVIEW` 이력을 보존한다.
전체 면접을 반복하거나 후보자를 통과시키기 위한 rescue mechanism으로 사용하지 않는다.
RE_REVIEW는 INITIAL HOLD 뒤에만 존재하며 HOLD 재발행을 금지한다. 남은 uncertainty를 포함해 사람이
PROCEED_TO_OFFER 또는 DO_NOT_PROCEED를 결정한다. 관측창 내 후속검증 미완료는 미완료로 보존하며 결과를 강제하지 않는다.

Final Review는 검토한 Skill Decision ID와 적용 Rubric/근거를 역추적할 수 있어야 한다.
참조 직렬화는 Implementation Note이며 최신 snapshot으로 과거 검토 근거를 덮어쓰지 않는다.

### 4.8 offers.csv

Offer 객체의 정본이다. 현재 상태를 덮어쓰는 결과 필드를 두지 않는다.

| 필드 | 제약 / 의미 |
|---|---|
| offer_id | PK |
| application_id, candidate_id | 제안 대상 지원 건/지원자 |
| offered_at | 제안 시각. OFFERED Event와 일치하는 객체 속성 |
| expected_join_at | 예정 입사 시각 |
| response_deadline | 합성 응답 유효기한. offered_at 이후 |

최종검토의 PROCEED_TO_OFFER 이후 제안하며, 수락·거절·만료·입사 전 철회는 4.15의 이력으로 보존한다.
실제 입사 시각/사실은 workforce_events가 소유한다. 이전 offer_result/response_at/actual_join_at은 이력/Workforce 조회로 대체한다.
중복 표현인 offered_at은 OFFERED 사실과 독립적으로 관리하지 않는다.

EXPIRED는 임의로 선택하는 Candidate Outcome이 아니다. response_deadline까지 ACCEPTED/DECLINED가 없고
observation_end가 deadline에 도달한 경우에만 파생한다. 관측 종료가 deadline 전이면 Open 상태다.
ACCEPTED/DECLINED는 확인된 Response Event가 필요하다. NO_RESPONSE는 응답 부재의 관측이며 motive가 아니다.
응답하지 않은 이유는 UNKNOWN으로 유지한다. response window는 실제 기아 정책이 아닌 generation_rules의 합성 가정이다.
ACCEPTED ≠ JOINED이며 실제 입사는 workforce_events가 소유한다.

### 4.9 onboarding_profiles.csv

| 필드 | 제약 / 의미 |
|---|---|
| employee_id | PK. 입사 후 합성 식별자 |
| source_candidate_id | applications의 지원자 연결 |
| joined_at | workforce_events.JOINED에서 가져오는 조회용 시각 |
| onboarding_started_at | workforce_events.ONBOARDING_STARTED에서 가져오는 조회용 시각 |
| planned_ready_at | 개인 계획 Ready 시각. 이전 target_ready_at을 대체하며 실제 확인 시각과 구분 |

입사·온보딩 시작 사실의 owner는 workforce_events이며 profile의 중복 시각을 독립 수정하지 않는다.
Offer 수락 이후 Join을 기록한다. 실제 개인 이름·학교를 사용하지 않는다.

### 4.10 onboarding_skill_gaps.csv

| 필드 | 제약 / 의미 |
|---|---|
| gap_id | PK |
| employee_id | FK → onboarding_profiles |
| skill_id | FK → talent_profile |
| gap_level | 업무 관련 Gap 표현. 점수로 임의 대체 금지 |
| gap_source | SELECTION_EVIDENCE / POST_JOIN_ASSESSMENT / MENTOR_OBSERVATION |
| source_evidence_id | 원본 Evidence 연결. 입사 후 업무 근거 참조의 직렬화는 Implementation Note |
| confirmed_by, confirmed_at | 합성 확인 역할/시각 |
| decision_provenance | SYNTHETIC_HUMAN_SCENARIO |

Selection Evidence는 초기 참고다. 주관적 인상을 Gap으로 재사용하지 않고 입사 후 업무 근거로 재확인한다.

개인별 Onboarding Gap은 Final Review의 learnable_gap_summary와 입사 후 업무 준비 요구에서 파생한다.
모든 Joiner에게 동일 Skill Gap을 강제하거나 이미 확인한 Skill을 불필요하게 재평가하지 않는다.
planned_ready_at은 Ramp-up 계획 시각이며 Actual Ready 시각이 아니다.
READY_CONFIRMED는 JOINED 이후 필요한 Task/Gap 확인, post-join Work Evidence와 멘토/현업의 Human Confirmation을 요구한다.
시스템은 요건과 근거를 정리하며 시간 경과·Task 완료 Boolean만으로 Ready 또는 실패를 자동 생성하지 않는다.
계획 시각까지 확인이 없으면 Not Yet Ready로 조회하며 목표일 Available Supply에 포함하지 않는다.
별도 NOT_YET_READY Event는 필수가 아니며 RAMP_UP_EXTENDED도 실패 판정이 아니다.

### 4.11 onboarding_tasks.csv

| 필드 | 제약 / 의미 |
|---|---|
| task_id | PK |
| candidate_id | 정본 지원자 연결. employee_id의 source_candidate_id와 일치 |
| employee_id | FK → onboarding_profiles |
| milestone | MONTH_1 / MONTH_3 / MONTH_6 / EXTENDED |
| task_type | 업무 종류 |
| related_skill_id | nullable, 값이 있으면 talent_profile 참조 |
| planned_at | Task 계획 시각 |
| assigned_at | 기존 부여 시각. planned_at과 다른 사건이면 구분 |
| completed_at | 미완료면 NULL |
| evidence_ref | 실제 업무 관련 산출물/근거 참조 |
| status | PLANNED / IN_PROGRESS / COMPLETED / DELAYED / CANCELLED |
| mentor_confirmed | 합성 멘토 확인 여부 |
| decision_provenance | 멘토 확인 판단이 있는 레코드에 SYNTHETIC_HUMAN_SCENARIO |

완료 Boolean이나 시간 경과만으로 Ready를 결정하지 않는다. 업무 Evidence를 추적할 수 있어야 한다.

### 4.12 workforce_events.csv

Workforce Supply 변화의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| workforce_event_id | PK |
| employee_id | FK → onboarding_profiles → source_candidate_id |
| event_type | JOINED / ONBOARDING_STARTED / READY_CONFIRMED / RAMP_UP_EXTENDED |
| effective_at | 효력 시각 |
| source_ref | 근거 참조. READY_CONFIRMED에는 post-join Work Evidence 필수 |
| confirmed_by, confirmed_at | READY_CONFIRMED의 멘토/현업 확인 역할과 시각 필수. 단순 입사 사실에는 NULL 가능 |
| decision_provenance | Ready/연장 등 판단 레코드에 SYNTHETIC_HUMAN_SCENARIO |

JOINED 이후 ONBOARDING_STARTED, 업무 근거에 따라 READY_CONFIRMED 또는 RAMP_UP_EXTENDED를 기록한다.
이전 READY Event 명칭은 READY_CONFIRMED로 대체하며 UI의 Ready 표현과 구분한다.
목표일까지 READY_CONFIRMED인 신규 입사자만 Available Supply에 포함한다.
현재 Case의 신규 입사 1명과 FTE 대응을 다른 근로형태에 일반화하지 않는다.
Baseline과 확정 전입·전출은 Plan 입력이며 신규 입사 Event와 중복 계상하지 않는다.

### 4.13 assessment_activities.csv

Stage 내부 평가 활동의 정본이다.

| 필드 | 제약 / 의미 |
|---|---|
| activity_id | PK |
| stage_event_id | FK → stage_history |
| application_id, candidate_id | 참조 Stage와 동일한 지원 건/지원자 |
| activity_type | 아래 Activity 유형 예시 |
| started_at, completed_at | 활동 시작/완료. 미완료 시각은 NULL |
| activity_status | 활동 수행 상태. Stage result와 별개 |

PRE_ASSESSMENT 내부: APTITUDE / CODING_TEST.
FIRST_INTERVIEW 내부: TECHNICAL_ASSESSMENT / AI_CASE / PRACTITIONER_QA.
SECOND_INTERVIEW의 활동 예: VALUES_BEHAVIOR_INTERVIEW.
FINAL_REVIEW 내부 추가 검증: FOCUSED_FOLLOW_UP. INITIAL HOLD의 특정 질문·Skill·Context만 확인한다.
Activity를 별도 Funnel Stage로 집계하지 않는다. 예시 외 활동과 activity_status의 세부 enum은 Implementation Note다.

### 4.14 skill_decision_observations.csv

| 필드 | 제약 / 의미 |
|---|---|
| decision_id | FK → evidence_decisions |
| observation_id | FK → assessment_observations |

두 ID 조합은 중복하지 않는다. Decision과 Observation의 application_id/candidate_id/skill_id가 일치해야 한다.
Observation → Evidence와 확인된 Skill Link까지 추적한다. 각 Observation은 결정 시각 이전에 저장되어야 한다.
`assessment_evidence → assessment_observations → skill_decision_observations → evidence_decisions`가 정본 계보다.
이 관계는 기존 v0.1의 evidence_decision_sources.csv를 대체한다. 구 파일은 Audit history에만 보존한다.

### 4.15 offer_events.csv

| 필드 | 제약 / 의미 |
|---|---|
| offer_event_id | PK |
| offer_id | FK → offers |
| event_type | OFFERED / ACCEPTED / DECLINED / EXPIRED / PRE_JOIN_WITHDRAWAL |
| occurred_at | 사건 시각 |
| reason_code | 확인한 사유만 기록. 미확인 UNKNOWN |

JOINED는 Offer Event가 아니다. 실제 입사는 workforce_events에서만 관리한다.
사유의 기존 어휘 OTHER_OFFER / COMPENSATION / ROLE_EXPECTATION / WORK_CONDITION / PERSONAL /
NO_RESPONSE / OTHER / UNKNOWN은 확인된 사실 범위에서 사용한다. 무응답 사실에서 다른 사유를 추정하지 않는다.
실제 연봉·불필요한 개인 특성을 생성하지 않는다. 응답 이력은 현재 상태로 덮어쓰지 않는다.

### 4.16 activity_participants.csv

| 필드 | 제약 / 의미 |
|---|---|
| activity_id | FK → assessment_activities |
| participant_id | 합성 역할의 stable ID. 개인 이름 아님 |
| participant_role | 활동 참여 역할 |
| participation_started_at | 참여 시작 시각 |
| participation_ended_at | 참여 종료 시각 |

Actual person-hours는 해당 분석 대상 역할의 실제 참여 구간 합 / 3600초로 계산한다.
평가자 노력 시간에는 평가자 역할을 사용하며 지원자의 응시 시간을 평가자 effort에 더하지 않는다.
누락 구간을 계획 90분/30분으로 채우지 않는다. 여러 참여자의 시간을 합산하되 동일 참여 구간을 중복 계상하지 않는다.
관계키·동일 참여자의 여러 구간 표현·Calibration 활동 연결의 세부는 Implementation Note다.

### 4.17 interview_capacity_events.csv

| 필드 | 제약 / 의미 |
|---|---|
| capacity_event_id | PK |
| stage | FIRST_INTERVIEW |
| event_type | INITIAL_PLAN / GAP_IDENTIFIED / CAPACITY_ADDED / CAPACITY_RELEASED |
| person_hours | 비음수 평가자 시간. INITIAL_PLAN은 v0.3에서 60(v0.2는 80); GAP은 부족량이며 예산 증감이 아님 |
| effective_at | 효력 시각 |
| reason_code | 계획·Gap·추가 확보·회수 이유 |
| decided_by | Human Capacity Decision의 합성 역할 |
| decision_provenance | Human Decision이면 SYNTHETIC_HUMAN_SCENARIO |

최초 계획은 cycle/stage당 하나이며 수정·삭제하지 않는다. Revised Capacity = Initial + Added − Released.
Demand는 해당 시점 FIRST_INTERVIEW 필요 모집단 × 계획 unit effort이며 cohort/시점을 명시한다.
Gap은 같은 범위의 Demand와 Available Capacity 차이의 양수 부분이다. 전체 cycle Demand에는 Revised 총예산을,
미배정 Demand에는 Revised − Reserved − Consumed의 잔여 가용량을 대응하며 서로 다른 범위를 섞지 않는다.
GAP_IDENTIFIED는 계산 결과, ADDED/RELEASED는 사람의 운영 판단이다. Snapshot으로 이력을 대체하지 않는다.
Reservation/해제의 assignment·시각·미사용 시간은 재계산 가능한 운영 이력으로 보존한다.
그 직렬화/관계키는 Implementation Note이며 CAPACITY_RELEASED로 예약 해제를 중복 차감하지 않는다.

위 v0.2 Decision Note의 Actual은 `activity_participants → assessment_activities → stage_history`를 연결해
FIRST_INTERVIEW의 완료된 실제 평가자 참여구간만 합산한 값이다. 다른 Stage와 FINAL_REVIEW의 후속검증 시간은 제외한다.

| 활동 | 참여구간 초 합계 | person-hours |
|---|---:|---:|
| TECHNICAL_ASSESSMENT | 623,400 | 173.1667 |
| AI_CASE | 618,600 | 171.8333 |
| PRACTITIONER_QA | 463,800 | 128.8333 |
| CALIBRATION | 419,400 | 116.5000 |
| 합계 | 2,125,200 | **590.3333** |

173명 완료 × 4개 활동 × 평가자 2명 = 1,384개 참여구간이다. 계획 4h를 실제 소비로 대입하지 않는다.
`Capacity.close`는 각 reservation의 Reserved−Consumed−기해제 잔여분을 RELEASED로 기록한다.
이번 예약은 192×4=768h이며, 완료 후 미사용 101.6667h + 미응답 14명×4=56h + 확인된 철회 5명×4=20h
= **Released Reservation 177.6667h**다. 완료 후 해제 행은 170개이며 나머지 완료 3명은 4h를 전부 소비해 해제량이 0이다.
따라서 768 = 590.3333 + 177.6667, 미사용 예약 잔여 0h, Revised 800 − Consumed 590.3333 = 가용 잔여 209.6667h다.
이는 이미 소비한 시간을 되돌리거나 cycle 예산 800h를 줄이는 사건이 아니다. 무응답은 철회/거절로 바꾸지 않는다.

위 표는 소수 넷째 자리 반올림이다. 참여구간의 정확한 시간은 2,125,200/3,600h이고,
assignment CSV의 행별 8자리 직렬화 합은 CONSUMED 590.33333328h / RELEASED 177.66666672h다.
이 미세한 직렬화 반올림 차이를 새로운 운영 사건으로 해석하지 않는다.

`invariants.py::capacity_history`는 최초 80h·4h unit, eligible cohort/Demand/Gap, Human Decision 참조,
실제 참여와 소비 일치, 예약 해제와 시간순 잔액을 독립 검사한다. 현재 저장본은 read-only 검증 PASS다.
다만 `ceil(Gap/80)`의 최소 panel 수·추가 720h 공식 자체를 별도 강제하는 Validator 검사는 없다.
따라서 **정확히 800h인 근거는 위 코드·규칙·사건의 직접 대조로 확인**했으며 Validator PASS만으로 주장하지 않는다.

## 5. 시각과 파생 지표

### 5.1 Timestamp와 관측창

모든 timestamp는 ISO 8601 offset-aware 형식, timezone은 `Asia/Seoul`이다.
예: `2027-01-12T14:00:00+09:00`. Manifest에 observation_start / observation_end / timezone을 기록한다.
Stage 필드의 의미는 4.2절을 따른다. invited_at은 참여 안내, notified_at은 확정 결과 통보다.
이전의 두 의미를 혼용한 notified_at과 파생식은 폐기한다.

| Metric | Raw timestamp 계산 |
|---|---|
| Scheduling Wait | scheduled_at - invited_at |
| Decision Time | decision_at - completed_at |
| Notification Delay | notified_at - decision_at |
| Stage Lead Time | notified_at - entered_at |

필요한 timestamp가 하나라도 NULL이면 Metric도 NULL이며 보간하지 않는다.
음수 시간을 0으로 고쳐 숨기지 않는다. 참여 안내/예약이 없는 Stage에 시각을 만들어 넣지 않는다.
observation_end까지 결과가 확정되지 않은 지원자는 IN_PROGRESS로 유지하며 FAILED/WITHDRAWN으로 변환하지 않는다.
이탈은 withdrawn_at과 확인된 사유/UNKNOWN으로 보존한다. 관측창 밖의 미래 완료를 현재 결과처럼 사용하지 않는다.

### 5.2 Funnel 집계

기본 단위는 고유 candidate_id다. 같은 지원자의 Event·Activity·평가자 기록 수를 인원으로 세지 않는다.
Stage별 Entered, Completed, Advanced, Failed, Withdrawn, In Progress를 구분할 수 있어야 한다.
Entered/Completed는 lifecycle 관측이며 Advanced 등 최종 결과와 중첩 가능하므로 모두 더하지 않는다.

동일 Stage 진입 cohort의 고유 인원을 분모로:

- Stage Advancement Rate = Advanced / Entered.
- Failure Rate = Failed / Entered.
- Withdrawal Rate = Withdrawn / Entered.

예: Entered 60, Advanced 40, Failed 15, Withdrawn 5라면 각각 40/60, 15/60, 5/60이다.
이는 산식 설명 예시이며 Mission 1 Actual이 아니다. WITHDRAWN을 진입 분모에서 빼지 않는다.
평가 완료자 중 통과율을 별도로 계산한다면 Metric 이름·분모를 명시한다.
관측 종료 시 IN_PROGRESS를 실패/이탈로 처리하지 않는다.
Target은 3.2절 Plan, Actual은 정본 Event의 같은 정의/관측창에서 계산한다.

**v0.2 Funnel 근거 — 위 Capacity Decision Note와 동일 관측창**

Target Funnel은 사전 계획이며 Actual Funnel은 생성된 사건과 합성 사람 판단의 결과다.
`generate.py::applications/process/offer`, `evidence.py::stage_transition_decision/final_review`와
applications/stage_history/final_decisions/offers/offer_events/workforce_events의 저장 행에서 다음을 확인했다.

| 연결 | 저장된 사건·판단 결과 |
|---|---|
| 지원 시작 342 → 제출 246 | 21일간 일별 12~20명 유입 규칙의 실현값 342. SUBMITTED 246 / ABANDONED 50 / STARTED 46. Target 320/240으로 개수를 잘라내지 않음 |
| 서류 | 제출 246명 모두 ADVANCED. 경험·후속검증 후보를 기록하며 검증된 공개 기본요건 위반을 임의 생성하지 않음 |
| 사전검증 246 → 통과 192 | 직접 코딩 검증 미실행 기준으로 FAILED 25; 확인된 WITHDRAWN 9; IN_PROGRESS 20. 미관찰 자체를 실패로 사용하지 않음 |
| 1차 진입 192 → 2차 대상 170 | 반복된 직접 기술 MUST 제한으로 FAILED 3; WITHDRAWN 5; 미응답 IN_PROGRESS 14; ADVANCED 170 |
| 2차 진입 170 → 최종검토 147 | 행동 영역 검토 후 ADVANCED 147; WITHDRAWN 13; IN_PROGRESS 10; FAILED 0 |
| Final Review 147 → Offer 86 | INITIAL Proceed 38 / Do not proceed 5 / HOLD 104. 104회 후속검증·재검토에서 Proceed 48 / Do not proceed 56. 최종 Proceed 38+48=86, 비진행 61 |
| Offer 86 → Join 56 | ACCEPTED 62 / DECLINED 11 / EXPIRED 13. 수락 뒤 PRE_JOIN_WITHDRAWAL 6; 나머지 56명의 JOINED를 workforce_events에서 확인 |

EXPIRED 13은 응답기한까지 ACCEPTED/DECLINED가 없고 observation_end가 기한에 도달한 경우다.
무응답 동기는 UNKNOWN이며 수락 자체를 Join으로 집계하지 않는다.
전체 FAILED 28건의 사유는 DIRECT_TASK_LIMITATION 25 / REPEATED_MUST_LIMITATION 3이다.
Capacity 부족은 이 사유에 없고 Final Hiring 판단에도 Capacity/Target Join을 입력하지 않는다.

현재 코드에서 funnel_targets는 Plan 작성에, target_join은 Workforce Plan에 쓰이며 인원 gate가 아니다.
Capacity 추가는 Offer 생성 전에 사전검증 cohort로 결정되고, 목표 오차를 줄이는 seed search/결과 재시도 루프는 없다.
v0.1과 seed 20260924, applications/evidence 패턴 분포, withdrawal contacts가 같고,
Offer 응답 가중치도 기존 EXPIRED 선택지를 NO_RESPONSE 관측으로 바꾼 의미 변경 외 유지한다.
applications.csv는 v0.1과 byte-identical이다. 현재 저장 규칙·manifest·코드에서 목표 맞춤 tuning의 근거는 발견되지 않았다.
다만 이 자료만으로 저장되지 않은 과거 시행 전체의 부재까지 증명할 수는 없으며,
새 80h resource block 가정의 사전 적절성/현실성은 사람의 검토 대상으로 남긴다.

### 5.3 KPI 원자료 범위 — Audit 반영

| 영역 | 재계산할 항목 / Owner |
|---|---|
| Workforce | Target-date Available Supply / Demand. Plan의 기존 Supply·확정 이동 + 목표일까지 READY_CONFIRMED인 신규 인력 |
| Funnel | Target vs Actual, Stage Entered/Completed/Advanced/Failed/Withdrawn/In Progress와 5.2절 비율 |
| Process Time | 5.1절의 네 시간 Metric |
| Capacity | Initial / Demand / Gap / Human Decision / Revised 이력과 실제 Participant 구간의 Actual 분리 |
| Offer | offers/offer_events의 Offered, Accepted, Declined, Expired, Pre-join Withdrawal |
| Onboarding | workforce_events의 Joined Count, Ready Count, JOINED→READY_CONFIRMED Lead Time |

KPI 결과를 목표로 데이터를 생성하지 않는다. 업무 Event를 생성하고 수치를 재계산한다.
source_channel과 관련 원자료를 보존하되 Channel performance, Attraction efficiency,
Calibration agreement rate, 특정 Assessment 효과/Channel Quality를 Mission 2 Main KPI로 미리 정하지 않는다.
채널은 지원 경로이며 Quality 대리변수가 아니다. 높은 Offer/Join 비율을 좋은 채널로 자동 해석하지 않는다.
Assessment Evidence를 Candidate Ranking용 숫자 KPI로 바꾸지 않는다.
노출/방문 원자료 없는 Attraction 비율 등 범위 밖 지표를 새로 추가하지 않는다.

## 6. 생성·검증·Freeze 원칙

### 6.1 생성 규칙

Channel → Application → Observable Evidence → Screening / Pre-assessment → Interview Evidence
→ Human Decision 기록 → Stage Timing / Withdrawal → Offer → Join → Skill Gap → Onboarding → Ready → KPI.
이는 개념적 의존성 순서다. Capacity·시간·이탈은 인과 의존성을 보존하며 구체적 생성 방식은 후속 계약으로 닫는다.

- 고정 seed, 버전 있는 규칙, 현실적 분포와 Noise로 재현한다.
- 숨은 종합 능력치·단일 pass probability를 만들지 않는다. Stage마다 서로 다른 관찰 Evidence를 사용한다.
- 관찰되지 않은 역량을 잠재 점수로 저장하지 않는다.
- 평가자 관찰/해석 차이를 보존하되 과도한 무작위 오류나 강제 합불을 만들지 않는다.
- Withdrawal은 회사 Selection Decision과 분리한다. 강한 Evidence가 있어도 이탈할 수 있다.
- Lead Time 영향은 모든 이탈을 설명하는 결정식이 되어서는 안 된다. 생성 가정을 실제 원인 발견으로 주장하지 않는다.
- Channel별 유입 구조 차이와 개인 Quality를 구분한다. 특정 채널 합격 가산 규칙은 금지다.
- Capacity가 실제 일정 timestamp에 영향을 준다. 분석용 설명만 붙이지 않는다.
- Ready는 Skill Gap·Task·멘토 확인·업무 근거를 연결하며 몇 명을 연장할지 미리 정하지 않는다.
- Synthetic Human Scenario와 실제 Dataset Reviewer의 규칙 검토를 구분한다. 아래 생성 계약을 따른다.
- 성별·나이·인종·종교·장애·혼인 여부·사진·실제 학교명·실제 이름·불필요한 연봉을 포함하지 않는다.

Source별 Evidence 종류·맥락은 Assessment Matrix와 verification_mode를 따른다. 동일 Skill/문장 Pattern을 모든 Source에서 반복하지 않는다.
Source별 목표 합격률·Evidence Level 분포로 Funnel 결과를 맞추지 않는다. probability·시간 간격·evaluator pool 규모·response window는 버전별 generation_rules와 manifest에 기록한다.
후속 버전은 v0.1과 동일 seed를 우선 사용하여 규칙 변경 영향을 비교한다. 결과를 유지하거나 Target에 맞추기 위한 seed search는 금지한다.

### 6.1.1 Synthetic Evaluation / Human Decision

Synthetic Evidence / Synthetic Human Observation / Synthetic Human Decision은 모두 SYNTHETIC이다.
실제 사람이 평가한 데이터라고 표현하지 않는다. Evidence는 가상 지원자가 남겼다고 가정하는 관찰 원자료,
Observation은 가상 평가자가 Evidence를 보고 남겼다는 기록,
Decision은 Evidence·Observation·Rubric을 검토한 가상 사람의 판단 시나리오다.

모든 판단 레코드에는 `decision_provenance = SYNTHETIC_HUMAN_SCENARIO`를 기록한다.
필드 위치는 4절의 Stage 판단, Skill Link 확인, Observation, Skill/최종 Decision,
Skill Gap 확인, Task의 멘토 확인, Ready/연장 판단 행이다. 순수 시간·입사·지원 사실을 판단으로 바꾸지 않는다.
Raw Evidence는 합성 원자료, 계산 Metric은 ANALYSIS이며 provenance 축을 혼합하지 않는다.

Generator는 관찰 가능한 Evidence Pattern부터 만들고 명시된 Rubric에 따라 합성 Observation/Decision을 생성한다.
Rubric은 NOT_OBSERVED / LIMITED / MODERATE / STRONG의 해석 기준이며 숫자 점수표가 아니다.
Hidden candidate ability, fit/culture fit/aggregate score, pass/performance/turnover probability,
score threshold 합불, Ranking을 내부에도 만들지 않는다. 능력 점수를 먼저 만들고 Evidence를 역산하지 않는다.
평가자 차이는 Evidence 모호성·관찰 범위·Rubric 해석 차이로 설명하며 단순 random noise로 흔들지 않는다.
Calibration은 저장된 Observation을 입력으로 원근거와 Rubric을 확인하여 합의/미합의/근거부족을 보존한다.

Final Decision은 Must Evidence Coverage, Remaining Uncertainty, Learnable Gap, Calibration Result,
Talent Profile을 함께 검토한 시나리오다. MUST 근거 부족에서 HOLD/추가 Evidence 필요를 허용하며 자동 탈락시키지 않는다.
LEARNABLE Gap만으로 자동 탈락시키지 않는다. 여러 직접 Assessment에서 반복 확인된 명확한 MUST의 제한은
DO_NOT_PROCEED의 설명 가능한 근거가 될 수 있다. Target 인원에 맞추거나 총점 threshold로 결정하지 않는다.

### 6.2 Validation

| 영역 | 반드시 확인할 불변 조건 |
|---|---|
| 식별·참조 | PK 중복 없음, FK 존재, Evidence와 지원자/Skill 관계 일치 |
| 지원 | SUBMITTED의 제출 시각 필수, ABANDONED의 제출 시각 NULL |
| 결과·사유 | FAILED/회사 판단과 WITHDRAWN/지원자 이탈 및 IN_PROGRESS 분리, 미확인 사유 UNKNOWN |
| 시간 | Stage별 lifecycle, 역전 없음, 결측과 미완료를 0시간으로 대체하지 않음 |
| 전형 | 최종검토 후 Offer, 수락 후 Join, Join 후 Onboarding, 그 후 Ready |
| AI/사람 | AI 후보와 사람의 연결 분리, 수준과 최종 판단 주체 구분, 평균 점수 없음 |
| 온보딩 | employee→candidate 참조, 입사·업무·Ready 시각과 근거 일치 |
| 집계 | Plan/Actual 분리, 동일 사건·지원자 중복 집계 방지, 목표일 이후 Ready 제외 |
| 재현 | 같은 버전·입력·seed에서 동일 데이터/지표, Raw Event→Metric 추적 |

의미에서 도출되는 추가 불변 조건:

- submitted_at >= started_at, decision_at >= completed_at, notified_at >= decision_at (각 시각이 모두 있을 때).
- withdrawn_at과 WITHDRAWN 상태가 모순되지 않아야 한다.
- Evidence→Activity→Stage의 application/candidate 관계가 일치해야 한다.
- Skill Decision의 복수 근거는 같은 지원 건/지원자를 참조한다.
- READY_CONFIRMED에는 업무 관련 Evidence 참조가 필요하다.
- offer_event는 존재하는 offer를 참조하고 JOINED를 Offer Event로 저장하지 않는다.
- 참여 종료는 시작보다 빠르지 않으며 같은 참여 구간을 중복 합산하지 않는다.
- 대표 Mapping은 freeze된 버전의 candidate를 참조한다.

세부 validator 표현/NULL 직렬화가 아직 작성되지 않았다면 검증을 완료했다고 보고하지 않는다.

### 6.2.1 Audit-derived Independent Invariants

- STRONG Skill Decision의 지지 Observation이 모두 SELF_REPORTED이면 ERROR. Observation 자체의 STRONG은 허용한다.
- 모든 Skill Decision에 최소 하나의 skill_decision_observations가 필요하며 Decision/Observation/Evidence의 application·candidate·Skill 관계와 시각을 검사한다.
- Observation 우회 relation, source/activity와 verification_mode 불일치, 미확인/INSUFFICIENT_EVIDENCE만으로 자동 FAILED 처리하면 ERROR.
- INITIAL HOLD에는 reason과 resolution_plan이 필수다. RE_REVIEW에는 동일 application의 INITIAL HOLD, 후속 Evidence/Observation/Calibration 이력이 선행해야 한다.
- application당 FOCUSED_FOLLOW_UP 최대 1회, RE_REVIEW의 HOLD는 ERROR. 후속 근거는 원 기록을 덮어쓰지 않는다.
- INITIAL_PLAN 보존, Capacity 부족만을 FAILED 사유로 사용 금지, 동일 participant_id의 역할 일치, 예약 해제와 예산 회수 구분을 검사한다.
- Actual effort는 실제 평가자 구간으로 계산하고 Plan 시간의 결측 대입·중복 소비를 금지한다.
- EXPIRED이면 offered_at < response_deadline <= observation_end, occurred_at은 deadline 이전이 아니며 deadline까지 ACCEPTED/DECLINED가 없어야 한다.
- ACCEPTED/DECLINED Event 없이 응답을 추론하지 않는다. 관측창 밖 deadline의 EXPIRED는 ERROR. 미확인 motive는 UNKNOWN이다.
- READY_CONFIRMED는 JOINED 이후이며 post-join Work Evidence, 필요한 Task/Gap 확인과 confirmed_by/confirmed_at을 추적해야 한다.
- planned_ready_at 경과만으로 READY를 만들거나 모든 Joiner의 Gap을 generator constant로 강제하지 않는다.

Validator는 generator의 interpret / calibrate / stage_transition_decision / final_hiring_decision 함수를 oracle로 재사용하지 않는다.
저장된 canonical Dataset과 독립 invariant를 검사한다. 동일 판단 구현의 동일 오류 반복을 Validation 성공으로 보지 않는다.
이 목록은 후속 Validator의 구현·검증 기준이며 현재 v0.1의 PASS를 최신 계약 준수로 승격하지 않는다.

### 6.3 검토와 Freeze

규칙 기반 후보 생성 → 무결성/현실성 검토 → 필요시 규칙 수정과 새 후보 전체 재생성 → 승인 → v1 Freeze.
개별 CSV를 결과에 맞춰 수정하지 않는다. 분석 Story를 만들기 위한 seed/분포 탐색도 하지 않는다.
Human Review 대상은 generation rule, provenance, Evidence traceability, schema validity,
decision logic consistency, 전체 현실성, 금지 hidden score 존재 여부다.
Reviewer가 320명 등의 개별 합불을 수동 승인하는 구조가 아니라 Synthetic HR Decision Process의 생성 규칙을 검토한다.

v0.2의 **Target Join 4 → Actual Join 56(+52명, 계획의 14배)** 편차도 원자료 그대로 보존한다.
이를 줄이기 위해 데이터·판단 규칙·seed·확률·Revised Capacity를 사후 조정하지 않는다.
이 편차와 초기 80h→Revised 800h 운영 선택의 규모는 Dataset Human Review 대상이며,
검토·승인·Freeze 이후 Mission 2에서 Plan/Revised/Actual과 판단·운영 이력을 함께 분석할 질문이다.
추가 Capacity가 일정에 미친 영향과 Join 편차의 원인을 단일 관측 Dataset만으로 인과 단정하지 않는다.
이번 Decision Note 추가는 Human Review 완료·Main Story 선정·Dataset 재생성·Freeze를 뜻하지 않는다.

Manifest 필수 항목: dataset_version, generation_version, seed, generated_at,
observation_start, observation_end, timezone, case_id, job_id, schema_version,
record_counts, generation_rules_version, validation_status, validation_errors.
이전 generator_version 표기는 generation_version으로 정리한다. Freeze 후 필요시 frozen_at을 추가한다.
record_counts는 파일별 실제 행 수다. 검증 상태/오류는 실제 검증에 근거하며 성공을 미리 기록하지 않는다.
최초 문서 동기화에서는 Dataset을 생성하지 않았다. 후속 생성기 작업에서 v0.1 생성·자동 검증을 수행했으며
이후 Rules Audit에서 D-01 및 modeling issues를 발견했다. 그 뒤 vNext 구현과 v0.2 생성·자동 검증을 수행했다(§9).
v0.2는 UNREVIEWED / frozen=false이며 사람 검토·승인·Freeze는 미수행이다.
Freeze 후 UI와 분석은 같은 버전을 사용한다. 변경이 필요하면 버전과 변경 이유를 구분한다.
Main Story는 실제 데이터 분석 후 의미 있는 패턴 2~3개로 정하며 무관계도 정상 결과다.

#### 승인 Baseline v1과 후속 버전 정책

v1은 사용자 Human Review 승인에 따라 v0.4(seed 20260924)를 승격한 **현재 승인된 Mission 1 Synthetic Dataset Baseline**이다.
Human Review, Independent Validation, 현재 SSOT 정합성, 재현성 확인을 완료한 기준선이며 Mission 1 Presentation과 Mission 2 분석의 기본 입력이다.
`data/synthetic/v1/`의 canonical 25개 파일은 source `data/generated/v0.4/`와 byte/hash가 동일하다. 재생성·row 수정·Target 사후 조정을 하지 않는다.
승인 metadata는 `data/generation/v1/dataset_manifest.json`에서 dataset_version=v1, source_candidate_version=v0.4, frozen=true,
baseline_status=FROZEN, review_status=APPROVED, frozen_at, source manifest/rules/code hashes와 관측창을 기록한다.
이는 PeopleOps Office 합성 시나리오이며 기아 내부 채용 데이터나 공식 운영정책이 아니다.
합성 가정은 `data/generation/v1/synthetic_assumptions.json`, 승인 당시 결과는 `human_review_snapshot.json`에 보존한다.

Freeze는 현재 snapshot을 직접 덮어쓰지 않는다는 뜻이며 향후 오류 수정이나 제품 변경을 금지하지 않는다.
변경 절차는 Current Baseline → Change Reason → 필요한 SSOT/Generation Rule 변경 → 새 Candidate → Validation → Human Review → 새 Baseline(v2 등)이다.
Generator bug, 미검출 데이터 오류, 공개 근거 추가, 채용/Assessment 설계 변경, 합성 가정 개선,
Mission 2 모델링 문제 또는 UI canonical contract 문제는 변경 사유가 될 수 있다.
원하는 분석 결과가 나오지 않거나 Target Funnel과 다르다는 이유만으로 버전을 변경하지 않는다.

Registry는 active_baseline과 각 version의 status(ACTIVE/SUPERSEDED), source_candidate_version, approved_at,
superseded_by, change_reason 및 manifest 참조를 관리한다. 새 Baseline 승인 시 Registry만 기존 항목을 SUPERSEDED로 전환하며
과거 Baseline의 canonical 파일·승인 manifest·결과 snapshot은 보존한다. 이번 승격은 v1만 생성한다.
Mission 2 분석과 Presentation Mapping은 dataset_version을 필수 기록한다. Baseline 교체 후에도
과거 분석/Presentation을 새 Dataset의 결과로 자동 재해석하지 않으며 새 버전 대상 재실행/재선정은 별도 작업이다.

Freeze 검증은 `python3 -B data/generation/v1/verify_baseline.py`로 수행한다.
기존 candidate CLI는 UNREVIEWED 계약 전용이므로 승인 manifest를 candidate manifest로 위장하거나 Generator를 변경하지 않는다.
검증 스크립트는 v1 canonical에 기존 Independent Validator를 실행하고 source candidate manifest, 내용 동일성,
승인 metadata, Registry, 합성 가정·승인 snapshot hash를 별도로 대조한다. source의 REVIEW_PENDING 경고는
v0.4 검토 이력으로 유지하며 v1의 사용자 승인과 합성 가정 수용 기록을 분리한다.

### 6.4 대표 사례 선정과 Presentation Mapping

대표 3명은 generation input이 아니다. 기존 01/02/03 특성은 강제 archetype이 아닌 Desired Contrast다.

| Contrast | 탐색 의도 |
|---|---|
| A | 기술 구현/문제 구조화 Evidence vs 모델/AI 가정 검증 Evidence |
| B | 구현의 화려함 vs 문제 정의/제약/결과 검증의 견고함 |
| C | 빠른 학습/AI 활용 vs 기초 원리/검증의 불확실성 |

Generation Rules → Synthetic Candidates → Evidence → Observation → Decision → Dataset Validation
→ Dataset v1 Freeze → Representative Case Selection → Presentation Mapping.
가능하면 서로 다른 Evidence Pattern·판단 쟁점, 2개 이상 Assessment Source,
Observation→Evidence Decision→Final Review 추적, 보호특성/개인정보 미사용을 만족하는 사례를 고른다.
정확한 세 패턴이 없어도 Dataset을 수정하지 않고 더 의미 있는 쟁점을 선택할 수 있다.
합격/불합격/HOLD 비율을 연출하기 위해 강제 선정하지 않는다.

대표 여부는 canonical recruiting data에 저장하지 않는다.
별도 `presentation/mission1_representative_cases.json` 책임으로
dataset_version / display_id / candidate_id / selection_reason을 관리한다.
UI 지원자 01 등의 display_id와 정본 candidate_id를 분리한다.
**대표 사례는 Dataset의 입력이 아니라 Dataset의 결과다.**

사용자 Human Selection 확정: CASE A=C0003/APP0003, CASE B=C0005/APP0005, CASE C=C0228/APP0228.
`presentation/mission1_representative_cases.json`은 mapping_version과 dataset_version=v1, 승인 manifest hash에 귀속된다.
canonical Dataset의 일부가 아니며 v2로 자동 승계하지 않는다. v2에서는 별도 대표 선정과 새 Mapping을 검토한다.
카드 제목은 후보 ID·합불이 아닌 판단 질문이다. ID는 상세에서 확인한다. 각 case는 primary_skill_id,
2~4개 evidence_cards, scene별 ordered steps, table별 canonical refs, presentation copy, caveats를 가진다.
refs는 Evidence/Observation/Skill Decision/Stage/Final/Calibration/Session/Follow-up ID만 연결하고 canonical 원문을 복제하지 않는다.
Resolution Plan은 final_decision_id + skill_id로 원본 항목을 찾는다. 결과는 canonical record에서 읽으며 새 평가나 점수를 만들지 않는다.
C0003의 APPLICATION_RESPONSE는 Skill01 배경이며 Skill02 자기기술로 오인하지 않는다. Skill02 미관찰과 보조 Skill03 직접 근거를 분리한다.
C0005는 근거 미확보 종료이며 역량 부족 판정으로 표시하지 않는다. C0228은 targeted 확인 후 진행한 사례이나
HOLD 18명 중 해당 경로는 1명이라는 version-bound 참고 문맥을 보존한다. Offer EXPIRED는 별도 lifecycle이다.
Human Layer는 기존 직책·공간을 사용한다. 사람 대화에 typing을 쓰지 않고 Decision Panel의 순차 reveal은
저장된 v1 trace 조회임을 명시하며 전체 표시/reduced motion을 지원하도록 계약만 둔다. 실시간 AI 판단이 아니다.
`python3 -B scripts/validate_mission1_presentation.py`로 참조·동일 후보 소유·계보·HOLD chain·v1 hash를 검사한다.
이번 구현은 Mapping과 검증까지이며 React/UI 연결 및 Mission 2 분석은 포함하지 않는다.

## 7. Open Issues

### 7.1 Resolved Decisions

- OPEN-03 RESOLVED: offset-aware Asia/Seoul, lifecycle 시각 분리, NULL Metric, 관측창의 IN_PROGRESS 유지.
- OPEN-04 RESOLVED: 고유 candidate 집계, Target 라벨/Actual 대응, Stage와 Activity, 진입 분모의 이탈 포함.
- OPEN-05 RESOLVED: 5계층 canonical owner, 별도 application/candidate, Activity/복수 근거/Offer 이력/Workforce 구조와 manifest.
- OPEN-06 RESOLVED: 합성 Evidence/Observation/Decision, 명시적 provenance, Rubric 기반 생성과 Dataset 규칙 검토.
- OPEN-08 RESOLVED: freeze 후 사례 선정과 별도 Presentation Mapping.
- OPEN-12 RESOLVED: Dataset v0.1의 KPI/운영 원자료 계약 범위. Main KPI/Story 및 범위 밖 Attraction 지표를 확정한 것이 아님.

#### Dataset Rules Audit — Resolved Decisions

SELF_REPORTED-only STRONG 금지, Stage/Final 분리, persisted Observation 기반 Calibration,
Capacity 운영 이력과 reusable pool, HOLD 1회 후속검증/Re-review, deadline 기반 EXPIRED,
개인별 Gap과 업무 근거/Human Confirmation 기반 READY, 독립 Validator를 확정했다.
기존 resolved history는 유지한다. 문서 계약 확정은 후속 구현 완료를 뜻하지 않는다.

### 7.2 Implementation Notes

의미 계약은 확정됐다. 다음은 구현에서 명시하고 검증할 상세이며 새 정책을 추정해 채우지 않는다.

- CSV NULL 직렬화·타입·FK action·관계키·JSON 형태, activity_status/suggestion_source/must_evidence_status/gap_level/task_type의 세부 어휘.
- 지원 답변의 Activity 연결, 다중 Skill에 걸친 Observation의 표현, Rubric 식별·버전/참조, 미합의 final_level의 NULL 처리.
- 업무 Evidence의 source_ref/evidence_ref 해석, participant의 여러 참여 구간과 Calibration 활동 표현.
- 관측창 실제 날짜·seed·구체적 생성 분포와 Rubric 내용은 generation_rules에 명시할 구현 입력이다. 이번에 임의 확정하지 않는다.

이 상세가 표현만으로 해결되지 않고 새로운 판단 정책을 요구하면 해당 부분을 후속 결정으로 분리한다.
제품 의미 계약을 다시 OPEN으로 돌리거나 상세가 모두 구현됐다고 보고하지 않는다.

통합 상태와 필요한 결정은 [11](11_v2_migration_specification.md#7-open-issues)에 둔다.
남은 OPEN-01/02/07/09/10/11/13은 유지한다. 생성기 구현 시작과 Dataset 검증·Freeze 완료는 별개다.

## 8. Generator v0.1 구현 기록 — Audit 이전 이력

아래는 당시 구현 기록이다. 현재 준수 여부는 1절 및 Audit 계약을 따른다. v0.1은 Freeze 후보로 승격하지 않는다.

실행 도구는 [scripts/mission1_dataset](../scripts/mission1_dataset/README.md)이며 Python 표준 라이브러리만 사용한다.
[생성 규칙](../data/generation/generation_rules.json)에 seed 20260924, generation_version m1-generator-0.1.0,
관측창 2026-10-01~2027-10-31(Asia/Seoul), Rubric·시간·직접 관찰 원자료 생성 가정을 기록했다.
3개 Plan과 16개 CSV는 `data/generated/v0.1/`의 검토 후보이고, 단일 manifest owner는
[data/generation/dataset_manifest.json](../data/generation/dataset_manifest.json)이다.
고정 generated_at은 재현용 논리 시각이며 실제 실행 시각이 아니다.

구체화한 구현 상세:

- 빈 CSV 셀은 NULL, enum/required/키는 schema.py, offline FK는 전체 snapshot 검증으로 관리한다.
- DOCUMENT_REVIEW와 FINAL_REVIEW_DISCUSSION을 내부 Activity로 표현한다. 요구 자료가 준비된 시각과 내부 검토 완료를 구분한다.
- Observation에 skill_id/rubric_id, Stage 판단에 rationale을 추가해 근거와 해석 기준을 추적한다.
- 미합의 final_level은 NULL, Skill Decision은 검토 시점별 snapshot과 복수 source relation으로 보존한다.
- 업무 산출물은 onboarding_tasks.work_evidence와 행 내부 evidence_ref로 표현한다. Ready는 해당 업무 검증과 멘토 확인을 참조한다.
- Actual effort는 명시된 참여 구간만 합산한다. 미기록 운영 업무의 시간을 추정하지 않는다.
- 대표 사례나 새로운 HR 판단 정책, 기아 공식 사실을 추가하지 않는다.

자동 검증/기술 통계는 [Sanity Report](../data/generation/sanity_report.md)에 기록한다.
빈 온보딩 집단도 결과를 맞추지 않고 보존하며 별도 테스트 fixture로 Ready/연장 구현을 검증한다.
이는 Dataset v1 승인이나 Main Analysis Story 선정이 아니다. OPEN-01/02/07/09/10/11/13은 유지한다.

## 9. Generator + Independent Validator vNext 구현

사용자의 후속 구현 요청으로 `scripts/mission1_dataset/`를 최신 계약으로 이관했다.
새 검토 후보/규칙/manifest는 각각 `data/generated/v0.2/`, `data/generation/v0.2/`에 둔다.
v0.1 데이터와 기존 generation 산출물은 변경하지 않는다. v1 Freeze·대표 선정·Mission 2 Story·UI 연결은 별도다.
실제 실행 결과는 v0.2 validation_report / sanity_report / dataset_manifest가 소유하며 자동 PASS는 사람 검토 승인이 아니다.

구체화한 Implementation Notes:

- Source별 허용 Skill·Verification Matrix와 source context는 versioned generation_rules에 기록한다.
- Observation에 `explicit_limitation`, Evidence에 `verification_mode/context_id`를 추가한다.
- Skill Decision은 `skill_decision_observations`로만 persisted Observation을 참조하고 rationale에 지지·차이·한계 근거를 기록한다.
- Stage별 직접 기준/후속 질문과 Final review snapshot을 분리한다. Final 완료 Stage의 result는 NULL이다.
- HOLD의 resolution_plan은 question/skill_id/context/method 배열; Final rationale는 Skill Decision ID snapshot과 불확실성·사람 rationale를 저장한다.
- `capacity_assignments`는 reservation_id·stage_event_id·event_type·person_hours·effective_at·activity_id·participant_id·reason_code 이력이다. 예약 해제를 cycle 예산 회수로 집계하지 않는다.
- Capacity event에는 cohort_application_ids/demand_person_hours/scope/source_event_id/rationale를 추가해 whole-cycle 수요·Gap·운영 대안을 추적한다. 최초 80h, 계획 4h는 보존한다.
- 추가 resource는 80h panel block, 결정 지연 2일, pool당 주 2회 block이라는 합성 구현 가정이다. pool의 겹치는 활동만 배제하며 상세 개인 Calendar를 생성하지 않는다.
- Offer response window는 14일 합성 가정이며 EXPIRED는 이벤트 부재/기한에서 파생한다.
- Gap의 final_decision_id/requirement_ref/rationale로 개인별 Final Review와 업무 요구를 연결한다.
- Ready source_ref JSON은 work_evidence_refs/gap_ids/human_rationale를 가지며 모든 필요 Task/Gap의 업무 확인을 검증한다. 업무 근거 observed_at은 완료시각과 일치한다.
- Final 재검토에서 미관찰만 남은 경우의 수용/업무 지원, 다른 맥락의 직접 근거로 모호성을 설명하는 Calibration은 명시된 합성 패널 정책이며 Rules/Reality Review 대상이다.
- 동일 seed와 v0.1 keyed random namespace를 유지한다. Source/Skill/새 Activity 변경에 따른 원자료 차이는 규칙 변경 효과이며 Target에 맞춘 추출 조정이 아니다.

전체 필드·실행·정책·검증·한계는 [생성기 개발 문서](../scripts/mission1_dataset/README.md)에 기록한다.
기존 OPEN-01/02/07/09/10/11/13 및 resolved history를 유지한다.
