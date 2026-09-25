# PeopleOps Office — V2 Recruitment Design

v0.5 Application/Document 승인 계약은 하단에 있으며 서류에 한해 이전 계약보다 우선한다. v1 Baseline은 변경하지 않는다.

## 1. 책임과 출처 경계

인재 요건 → 인재 유치·공고 → 지원·검증 → 평가 조정 → 최종검토 → Offer·Join → Ready의
설계 이유와 판단 원칙을 정의한다. Scene 순서는 [06](06_mission1_experience_specification.md),
UI는 [05](05_ui_specification.md), 데이터는 [09](09_mission1_data_specification.md)가 소유한다.

Source → Job Interpretation → Competency → Assessment → Evidence → Human Decision의 추적을 유지한다.
공개자료의 확인된 문구만 PUBLIC이며, 이를 역량/평가로 연결하는 해석은 INFERENCE,
가상 조직·인원·전형·문항·지원자·시간·Capacity는 SYNTHETIC이다.
현재 기아 공고 전문은 SOURCE NOT AVAILABLE이다. 과거 대화의 공고 설명을 공식 원문으로 인용하지 않는다.
지원 문항 캡처는 문항 내용만 확인하며 공식 발행일·공고 전체를 증명하지 않는다.

판단 계보는 `Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision`이다. 원자료, 평가자의 관찰, Calibration 후 Skill 판단, 최종 채용 판단을 구분한다.
시스템/AI는 이 계보를 우회해 판단을 확정하지 않는다. 상세 저장 계약은 09가 소유한다.

## 2. 인재 요건·인재 유치·지원 질문

인력 확보 방식과 신입의 제약 조건은 [02](02_mission1_scenario.md)를 따른다.
Must는 문제 구조화, ML/수리적 사고 기초, 알고리즘 구현 및 검증, 새로운 기술 학습,
협업 및 기술 커뮤니케이션이다. Production 경험·운영 가능한 구현 이해는 Learnable이며
논문/알고리즘 구현·관련 연구/프로젝트·필요시 Business English는 Plus다.
신입에게 전문가 수준 최적화/RL 경험을 필수로 요구하지 않는다.

채용담당자·ICT 인사담당자·ML 엔지니어가 업무와 인재 요건을 공고 문장으로 연결한다.
Must와 Plus를 혼합하지 않고 역할·업무·필요한 기초·학습 가능 영역을 구분한다.
공고 점검은 모호한 표현·내부용어·긴 문장·요건 연결을 표시하며 사람이 문구를 확정한다.

인재 유치는 Target / Message / Content / Channel / Candidate Information Need / 측정 목적을 연결한다.
단순 지원자 수가 아니라 직무를 이해한 관심과 지원을 목표로 한다.
데이터 채널은 CAREER_SITE / TECH_COMMUNITY / CAMPUS / RECRUITING_EVENT이며
채널을 인재 Quality 대리변수나 합격 가산점으로 쓰지 않는다.
채널별 예상/실제 수치가 확정되지 않았다면 만들지 않는다.

| 제공 캡처의 문항 주제 | 분량 | 확인하려는 근거와 후속 활용 |
|---|---:|---|
| 해당 분야 동기와 입사 후 성장 | 750자 | 직무 이해·학습 방향 탐색. 표현력만으로 기술역량 확정 금지 |
| 중요한 역량, 이유, 이를 기른 노력 | 750자 | 직무 해석과 구체적 경험 발견. 1차 후속 질문 연결 |
| 기아 가치·행동 중 하나와 관련 경험 | 500자 | 구체적 과거 행동 탐색. 2차에서 보완 확인 |

위는 사용자 제공 문항의 주제 요약이다. 사용한 공식 문구·공고 메타데이터의 검증 상태는
[11 출처 등록부](11_v2_migration_specification.md#8-출처-등록부)를 따른다.
지원 답변만으로 Skill을 STRONG으로 확정하거나 Culture Fit을 계산하지 않는다.

## 3. Funnel과 Capacity Plan

확정 Target은 다음과 같다. 고유 candidate_id로 집계하며 계획 버킷과 Stage lifecycle을 구분한다.
세부 Actual 대응과 진입 분모·Stage/Activity 계약의 정본은 [09](09_mission1_data_specification.md)다.

| 계획 버킷 | Target |
|---|---:|
| 지원 시작 | 320 |
| 지원 완료 | 240 |
| 서류 통과 | 120 |
| 사전검증 통과 | 60 |
| 1차면접 계획 인원 | 20 |
| 2차면접 대상 | 8 |
| Offer | 5 |
| Join 목표 | 4 |

모두 SYNTHETIC Target/Capacity Plan이며 Actual, quota, pass threshold가 아니다.
기준 미달을 목표 인원에 맞춰 통과시키지 않는다.
Workforce Goal → 예상 전환 → 평가비용 → 현업 Capacity → 선발 위험 → HR 판단을 남긴다.
Funnel Plan의 입력값·가정·계산·대안은 고정 Case 자료로 보존한다.

v0.3 1차면접: 단일 60분 Session × 평가자 3명 = 후보당 면접 3 person-hours.
계획 20명 × 3h = Initial 60h. Calibration은 필요할 때 별도 Activity/노력으로 기록한다.
시스템은 산술을 수행하고 ICT 인사담당자·채용담당자·ML 엔지니어가 Trade-off를 검토한다.
'20명이 최적'이라는 알고리즘 판단을 만들지 않는다. 다른 전형의 비용·Capacity는 미확정 값을 채우지 않는다.



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
  새 Evidence에 입력 snapshot과 응답 종류를 보존하고 새 Observation→필요시 Calibration→Re-review를 수행한다.
  최대 1회, Re-review HOLD 금지, 미관찰만으로 자동 실패 금지 및 기존 Offer/READY 계약은 유지한다.


세부 resource/schema 구현 선택은 09의 동일 승인 계약 Implementation Notes를 따른다.

### FIRST_INTERVIEW Capacity 운영 계약 — v0.2 보존 이력

80 evaluator person-hours는 전체 채용 cycle의 INITIAL_PLAN이다.
`(면접 90분 + 평가/Calibration 30분) × 평가자 2명 = 후보당 계획 4 person-hours`이므로
20명은 planned operational capacity이며 합격 정원·quota·평가 cut-off가 아니다.
`Initial Plan → Demand → Gap → Human Decision → Revised Capacity → Actual Consumption` 이력을 보존한다.
Capacity 부족을 candidate FAILED 근거로 쓰지 않는다. Mission 1에서는 추가 평가자 Resource 확보를 사람의 운영 결정으로 탐색한다.
기간 조정·평가방식 변경 등의 대안과 이유를 남기며 최초 계획을 덮어쓰지 않는다.

participant_id는 Activity마다 새로 만들지 않고 reusable synthetic evaluator pool에서 재사용하며 동일 ID의 역할은 일관된다.
AVAILABLE은 사용 가능한 잔여시간, RESERVED는 배정했으나 미사용인 예약, CONSUMED는 실제 참여시간이다.
시작 전 취소/확인된 철회의 미사용 예약은 released되어 AVAILABLE로 돌아가며 이미 consumed된 시간을 되돌리지 않는다.
예약 해제는 cycle 예산 회수(CAPACITY_RELEASED)와 다르다. NO_RESPONSE로 미사용 예약을 해제할 수 있어도
별도 확인 없이 후보자를 WITHDRAWN으로 바꾸지 않는다. 상세 근무 Calendar는 합성하지 않는다.
Actual은 activity_participants의 실제 평가자 참여구간 합으로 계산하고 결측을 계획 4h로 채우지 않는다.

## 4. 채용 전형과 Assessment Matrix

지원 → 서류 → 사전검증(역량검사·코딩테스트)
→ 1차 실무진면접(기술평가·AI 문제해결 과제·실무진 질의)
→ 1차 평가 조정 → 2차면접 → 최종검토(필요시 HOLD → Focused Follow-up → Calibration → Re-review) → Offer → Join → Onboarding → Ready.

이는 PeopleOps Office의 상세 시나리오 설계다. 실제 기아 2026 H1 상세 전형이라고 표현하지 않는다.
역량검사는 PRE_ASSESSMENT 내부 APTITUDE Activity의 응시·완료 이벤트만 정의하고 실제 문항이나 성향 점수는 만들지 않는다.
CODING_TEST도 사전검증 내부 Activity다. FIRST_INTERVIEW 내부에는 TECHNICAL_ASSESSMENT / AI_CASE / PRACTITIONER_QA가 있다.
Activity·평가자 기록 증가가 Funnel 인원 증가를 뜻하지 않는다.
코딩테스트는 구현 기초·데이터 처리·논리·검증을 확인하며 고난도 알고리즘 대회가 아니다.
기술평가/AI 과제는 1차면접 활동이며 독립 채용 Stage로 중복 집계하지 않는다.

| 인재 요건 / 관찰 영역 | 주 평가 | 보완 / Evidence |
|---|---|---|
| 문제 구조화 | 1차 AI 문제해결 과제 | 지원 경험 탐색, 기술평가·후속 질문 |
| ML/수리적 사고 기초 | 1차 기술평가 | 결과 해석·목표/변수/제약 설명, 실무진 근거 확인 |
| 알고리즘 구현 및 검증 | 1차 AI 문제해결 과제 | 코딩 기본기, 결과 검증 설명·후속 질문 |
| 새로운 기술 학습 | 1차 실무진 질의 | 지원 경험·새 방법 적용·2차 보완 |
| 협업 및 기술 커뮤니케이션 | 1차 실무진 질의 | 과제 설명, 2차 실제 행동 검증 |
| 가치와 행동 | 2차면접 | 캡처 문항의 경험과 후속 질문. 별도 Fit Score 없음 |
| 운영환경/Production | 입사 후 학습 | 기존 경험은 참고하며 신입 탈락용 필수조건으로 바꾸지 않음 |

주 평가와 보완 검증을 구분한다. 같은 역량을 여러 단계에서 점수화해 누적하지 않는다.
서류는 기본요건과 후속 검증할 경험 Evidence를 확인한다. 공개 자격의 원문 미확보를 임의 기준으로 채우지 않는다.

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

## 5. 기술평가와 AI 문제해결 과제

기술평가는 1~2개 문제를 통해 사고과정과 평가 근거를 상세 탐색하는 범위다.
모델을 직접 학습하거나 완전한 최적화 프로그램을 개발하는 과제를 요구하지 않는다.
확정한 문제 방향은 결과 해석·검증과 현실 자원배분의 구조화다.

| 문제 방향 | 제시 맥락 | 관찰 근거 |
|---|---|---|
| 모델 결과 검증 | 평균 성능은 높으나 편차가 큰 방법과 상대적으로 안정적인 방법 | 추가로 확인할 정보, 비교 조건, 실제 적용의 한계 |
| 자원배분 구조화 | 제한된 설비시간, 작업별 필요시간·납기·우선순위 | 결정변수, 목적, 제약조건과 선택 이유 |

문항의 최종 표현·정확한 입력값·공식 공고 문구와 1:1 연결은 원문과 후속 Case 검토가 필요하다.
이번 문서 동기화에서 평가 답안이나 합성 CSV를 생성하지 않는다.

AI 과제는 생산/설비 자원배분의 작은 CSV를 사용한다.
기존 설계의 입력 개념은 task_id / required_hours / deadline / priority / expected_value / preceding_task다.
관찰 대상은 문제 정의, 목적·제약조건, 접근 선택, AI 사용 판단, 결과 검증, 한계 설명이다.
특정 Solver·ML 모델이나 AI 사용량 자체를 평가하지 않는다.
과제 산출물 + 설명 + 후속 질문을 함께 확인하며 단일 정답값으로 종합 능력을 판단하지 않는다.

## 6. 대표 지원자와 면접

기존 지원자 01/02/03의 설계 의도는 아래 Desired Contrast로 유지한다. 강제 생성 archetype이 아니다.

| Desired Contrast | 탐색할 Evidence의 차이 |
|---|---|
| A | 기술 구현/문제 구조화 vs 모델/AI 가정 검증 |
| B | 구현의 화려함 vs 문제 정의/제약/결과 검증의 견고함 |
| C | 빠른 학습/AI 활용 vs 기초 원리/검증의 불확실성 |

좋음/보통/나쁨이나 합격 순서를 뜻하지 않는다. 최종 합불은 선결정하지 않는다.
같은 기본 질문과 각 답변에서 이어지는 고정 후속 질문으로 판단 깊이를 탐색한다.
사용자 선택에 따라 답변·평가·합불이 바뀌지 않는다. 대표 사례는 Dataset v1 Freeze 후 선정한다.
정확한 패턴이 없어도 Dataset을 수정하지 않는다. 더 의미 있는 판단 쟁점을 선택할 수 있다.
가능하면 2개 이상 Assessment Source와 Observation→Skill Decision→Final Review를 추적할 수 있는 서로 다른 사례를 고른다.
합불/HOLD 비율을 연출하지 않으며 대표 여부는 정본에 넣지 않는다. 별도 Presentation Mapping은 09를 따른다.

2차면접은 요약만 하지 않고 질문·답변·관찰을 상세 탐색한다.
협업·학습·피드백·가치와 행동을 실제 경험에서 확인하며 1차 기술평가를 반복하지 않는다.
Kia Values & Behaviors의 공식 상세 정의는 미확보이므로 확인된 캡처의 명칭만으로 내부 평가표를 복원하지 않는다.

## 7. Evidence Level과 Calibration

| 내부값 | UI | 의미 |
|---|---|---|
| NOT_OBSERVED | 확인되지 않음 | 판단할 근거가 관찰되지 않음. 역량 없음/0점 아님 |
| LIMITED | 제한적 | 관련 행동은 있으나 과정·기여·검증이 충분히 확인되지 않음 |
| MODERATE | 충분 | 스스로 접근·검증한 구체적 근거 확인 |
| STRONG | 강함 | 접근 설계·검증·결과에 따른 개선의 구체적 근거 확인 |

이는 관찰 Evidence에 대한 사람의 판단이며 숨은 능력치가 아니다.
AI는 관련 Skill 후보만 제안한다. 사람은 연결을 수정·거부·확정하고 수준을 판단한다.
평가자 관찰은 개별 보존한다. 차이가 나면 Observation → Original Evidence → Rubric → Review로 돌아간다.
결과는 AGREED / DISAGREEMENT_REMAINS / INSUFFICIENT_EVIDENCE다.
평균·숫자 환산·다수결 자동 평가로 차이를 지우지 않는다. 미합의 final_level의 세부 NULL 표현은 09 Implementation Note를 따른다.
Observation과 Decision은 SYNTHETIC_HUMAN_SCENARIO이며 실제 평가 결과가 아니다. Rubric·근거 기반 생성 계약은 09에 둔다.

최종 검토는 Talent Profile → Coverage → Must Evidence → Remaining Uncertainty → Learnable Gap
→ Calibration → Human Decision이다. PROCEED_TO_OFFER / DO_NOT_PROCEED / HOLD를 구분한다.
총점·순위·Fit/Culture Fit·미래 성과 예측으로 결정하지 않는다.

Calibration은 persisted `assessment_observations`를 입력으로 사용하고 원 Evidence·Verification Mode·Context·Rubric을 함께 검토한다.
Raw Evidence를 별도 경로로 재해석해 Observation을 우회한 Skill Decision을 만들지 않는다.

- Evidence Evolution: 후속 직접검증으로 초기 불확실성이 해소되거나 근거가 추가됨.
- Context Difference: 서로 다른 Task/상황에서 관찰된 내용의 차이.
- Evaluator Disagreement: 동일/관련 근거에 대한 평가자 해석 차이 또는 직접검증 근거 간 의미 있는 충돌.

이전 LIMITED/NOT_OBSERVED와 이후 MODERATE/STRONG의 차이만으로 DISAGREEMENT_REMAINS를 만들지 않는다.
최신 근거를 자동 우선하지 않으며 이전 Observation을 수정·삭제하지 않고 새 Observation과 Decision 이력을 추가한다.
AGREED는 연결된 Observation과 Rubric 검토 후 합의, DISAGREEMENT_REMAINS는 검토 후에도 남은 충돌,
INSUFFICIENT_EVIDENCE는 판단 근거 부족이며 Skill 부족이 아니다.

### HOLD / Focused Follow-up / Re-review

HOLD는 terminal outcome이나 후보자 결함이 아니라 해소 가능한 판단 정보가 남은 상태다.
INITIAL HOLD에는 Reason(`MISSING_EVIDENCE / UNRESOLVED_EVIDENCE / EVALUATOR_DISAGREEMENT`)과 Resolution Plan이 필수다.
Plan은 확인할 질문·Skill·Context·방법을 명시한다. 한 application당 최대 1회 FOCUSED_FOLLOW_UP으로 해당 범위만 확인한다.
`Reason + Resolution Plan → Focused Follow-up → new Evidence → new Observation → Calibration → RE_REVIEW` 이력을 보존한다.
전체 면접을 반복하거나 후보자를 통과시키기 위한 rescue mechanism으로 사용하지 않는다.
RE_REVIEW는 INITIAL HOLD 뒤에만 존재하며 HOLD 재발행을 금지한다. 남은 uncertainty를 포함해 사람이
PROCEED_TO_OFFER 또는 DO_NOT_PROCEED를 결정한다. 관측창 내 후속검증 미완료는 미완료로 보존하며 결과를 강제하지 않는다.

## 8. Offer와 Join

최종검토 이후 OFFERED → ACCEPTED → JOINED를 추적한다.
DECLINED / EXPIRED / PRE_JOIN_WITHDRAWAL은 별도 경로다.
offers.csv는 Offer 객체, offer_events.csv는 OFFERED/ACCEPTED/DECLINED/EXPIRED/PRE_JOIN_WITHDRAWAL 이력을 소유한다.
JOINED는 Offer Event가 아니며 workforce_events가 실제 입사를 관리한다.
Offer 시각·응답·예정/실제 입사와 확인된 사유를 보존한다. 미확인 사유는 UNKNOWN이며 추정하지 않는다.
단계별 저장 계약과 동일 사건 간 정합성은 09를 따른다.

EXPIRED는 임의로 선택하는 Candidate Outcome이 아니다. response_deadline까지 ACCEPTED/DECLINED가 없고
observation_end가 deadline에 도달한 경우에만 파생한다. 관측 종료가 deadline 전이면 Open 상태다.
ACCEPTED/DECLINED는 확인된 Response Event가 필요하다. NO_RESPONSE는 응답 부재의 관측이며 motive가 아니다.
응답하지 않은 이유는 UNKNOWN으로 유지한다. response window는 실제 기아 정책이 아닌 generation_rules의 합성 가정이다.
ACCEPTED ≠ JOINED이며 실제 입사는 workforce_events가 소유한다.

## 9. 온보딩과 Ready

JOINED ≠ READY.
Selection Evidence → Skill Profile → Skill Gap → Ramp-up Plan → Actual Work Evidence → Ready.
채용 Evidence는 초기 업무 관련 Gap의 참고이며 입사 후 재확인한다. 사람의 성과평가로 대체하지 않는다.

| 시점 | 업무 방향 |
|---|---|
| 1개월 | 개발환경·시스템·도메인 이해 |
| 3개월 | 기존 Pipeline 분석, Code Review, 작은 개선 |
| 6개월 | 실제 업무 Task 수행 및 Review |
| 연장 | 남은 Gap과 업무 근거를 확인하고 지원 |

사람이 업무 Evidence로 Ready를 확인하며 Task 완료만으로 자동 Ready 판정하지 않는다.
JOINED → ONBOARDING → READY 또는 RAMP_UP_EXTENDED → READY를 표현한다.
목표일까지 Ready가 확인된 신규 인력만 목표시점 Available Supply에 연결한다.
멘토에게는 목적에 필요한 업무 관련 근거만 전달하며 Values 원문·면접 인상·합불 논의를 포괄 이전하지 않는다.

개인별 Onboarding Gap은 Final Review의 learnable_gap_summary와 입사 후 업무 준비 요구에서 파생한다.
모든 Joiner에게 동일 Skill Gap을 강제하거나 이미 확인한 Skill을 불필요하게 재평가하지 않는다.
planned_ready_at은 Ramp-up 계획 시각이며 Actual Ready 시각이 아니다.
READY_CONFIRMED는 JOINED 이후 필요한 Task/Gap 확인, post-join Work Evidence와 멘토/현업의 Human Confirmation을 요구한다.
시스템은 요건과 근거를 정리하며 시간 경과·Task 완료 Boolean만으로 Ready 또는 실패를 자동 생성하지 않는다.
계획 시각까지 확인이 없으면 Not Yet Ready로 조회하며 목표일 Available Supply에 포함하지 않는다.
별도 NOT_YET_READY Event는 필수가 아니며 RAMP_UP_EXTENDED도 실패 판정이 아니다.

## 10. 업무 장소와 판단 책임

인재 요건·공고·유치·질문·Funnel은 채용전략실에서 HR과 현업이 협의한다.
서류/Offer는 채용운영실, 평가 설계·Calibration·최종검토는 평가회의실,
면접은 면접실, 온라인 응시는 특수 Mode, Join·온보딩·Ready는 업무공간에서 진행한다.
공간과 참여자는 정보 제공·판단·논의·영향 관계가 있을 때만 배치한다.
계산·검색은 모니터 등 도구이며 AI 캐릭터가 최종 판단을 대신하지 않는다.

## 11. 결과와 남은 확인

Mission 1은 Workforce / Recruiting Process / Onboarding 결과의 WHAT을 보여주고 Mission 2로 이어진다.
모든 Actual은 freeze된 Dataset과 연결하며 합불·이탈·Ready를 Story에 맞춰 만들지 않는다.
Funnel/데이터 구조·합성 판단·대표 사례 결정은 09에 반영했고 해결 이력을 11에 남겼다.
OPEN-10 공고·Culture 원문은 [11](11_v2_migration_specification.md#7-open-issues)에 유지한다.

## Application / Document Screen v0.5 — approved Human Review

v1 remains the ACTIVE approved baseline; v0.5 is a new UNREVIEWED candidate, not v2.
The public reposted 2026 H1 Kia ML Engineer eligibility structure is referenced; dates
are adapted to the PeopleOps Office synthetic recruiting cycle, not Kia internal policy.
Eligibility reference date is the synthetic application submission date; expected join date
is the cycle plan 2027-03-01. Degree is bachelor/master, graduated or expected graduation
by that planned join date; language is TOEIC Speaking/OPIc valid through reference date;
travel/visa must be eligible; military completion/exemption applies only when applicable.
Only minimal statuses are stored; no sex, age, military/visa reason or sensitive background.
Each requirement records PASS/FAIL/UNKNOWN/NOT_APPLICABLE; explicit FAIL takes precedence,
then UNKNOWN; military NOT_APPLICABLE satisfies that requirement without fabricating a pass.
UNKNOWN is not failure. Preferred qualifications are never hard filters.

Application experiences are SELF_REPORTED, with stable experience_id, context/type,
category-specific observable actions, ownership SELF/TEAM_CLEAR/TEAM_UNCLEAR and Evidence IDs.
PROBLEM maps to Skill01; BUILD and VALIDATE to Skill03. This replaces the fixed application
Skill01/04/05/06/08 template only in v0.5. Direct Assessment matrices and rules stay unchanged.
Within at least one SAME experience, at least two of PROBLEM/BUILD/VALIDATE must have
explicit actions and SELF/TEAM_CLEAR personal contribution. Unrelated experiences cannot
be combined. Categories are evidence candidates, not Skill levels, points or ranking.
Document explicit eligibility failure uses FAILED/BASIC_REQUIREMENT_VIOLATION with requirement
references. Otherwise qualifying experience uses ADVANCED/APPLICATION_EVIDENCE_CANDIDATE.
Otherwise CLOSED/INSUFFICIENT_APPLICATION_EVIDENCE terminates this application: insufficient
submitted evidence to proceed, NOT a Skill/ability limitation. CLOSED is Document-only.
No document-only canonical Skill Decision; existing self-reported-only STRONG prohibition remains.

Implementation parameters fixed before results: one or two experiences (equal categorical
weights); all eight subsets of the three categories equally represented in the sampling catalog;
three context templates and three ownership states sampled equally. These are illustrative
coverage scenarios, not empirical applicant frequencies. Eligibility uses a complete-profile
scenario plus one explicit failure and one unknown scenario per requirement (nine equally
weighted scenarios); military applicability is independently applicable/not applicable.
The distributions are not derived from Target 120. No latent quality or ability score.
Each experience's actions are generated once and reused by its application Evidence; subsequent
direct tests retain their previous keyed scenario generation, not conditioned on self-report.
This limited cross-stage consistency is a documented synthetic assumption, not verified ability.

Funnel Targets remain 320/240/120/60/20/8/5/4. FIRST 20 is expected planned FIRST population;
20 × 3h = initial 60h, never quota. Actual demand comes from prior Stage outcomes.
No target-based resampling, probability tuning or automatic baseline promotion.

## v0.6 Eligibility Resolution — approved Human Review

v0.6 supersedes only the v0.5 Eligibility lifecycle. Active baseline remains v1;
v0.5 remains an unchanged historical candidate. Experience/category/ownership distribution,
same-experience two-category Document evidence rule and every downstream decision/distribution remain unchanged.
Document PASS + qualifying experience → ADVANCED; UNKNOWN + qualifying experience →
CONDITIONAL_ADVANCE / ELIGIBILITY_CONFIRMATION_REQUIRED. Explicit FAIL and insufficient
application evidence retain their v0.5 closure semantics. Conditional is not verified PASS.

A minimal requirement-level eligibility_verifications.csv preserves initial application_eligibility
without overwriting it. Each event contains stable verification_id, application/candidate/eligibility
reference, requirement, previous_status=UNKNOWN, requested_at, verification_deadline, result,
verified_at (only for confirmed response), resolved_at, resulting_status, verification_evidence
(JSON minimal confirmed fact), human role, rationale and SYNTHETIC_HUMAN_SCENARIO provenance.
This is an operational gate between Document and PRE, not a scored assessment/new hiring Stage.

Implementation Note fixed before results: request one day after Document notification; allow
7 calendar days; confirmed synthetic response at day 3. Each unknown requirement independently
uses one of three equally weighted scenarios VERIFIED_PASS, VERIFIED_FAIL, ELIGIBILITY_NOT_VERIFIED.
These are illustrative synthetic administrative responses, not Kia frequencies or target-derived rates.
Missing response resolves at deadline to UNKNOWN/ELIGIBILITY_NOT_VERIFIED and closes this procedure,
never Skill limitation or eligibility FAIL. If the observation window ends first, retain PENDING with
no resolved_at/verified_at and do not advance. PASS/FAIL require explicit minimal requirement facts
and HR_OPERATIONS_01 confirmation. No degree/military/visa/language inference or sensitive details.

PRE entry and every PRE Activity require all requirements PASS/NOT_APPLICABLE at that time;
conditional applicants need linked verified records. Any verified FAIL or not-verified requirement
prevents entry, Offer and Join. Existing explicit PASS/FAIL/N/A statuses cannot be changed by this gate.
The original Document conditional decision remains history even after resolution. Reports separate
Document evidence-qualified progression (ADVANCED + CONDITIONAL_ADVANCE) from resolved PRE entry.
Target counts never influence verification response or deadline. No automatic baseline promotion.
