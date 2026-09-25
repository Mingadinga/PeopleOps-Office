# v0.6 Eligibility Resolution candidate

Active baseline remains v1. v0.5 is preserved. v0.6 adds only the conditional Document
→ human eligibility verification → PRE gate. Evidence-qualified count includes both
ADVANCED and CONDITIONAL_ADVANCE; neither is a verified Skill judgment.

```sh
python3 -B -m scripts.mission1_dataset generate --rules data/generation/v0.6/generation_rules.json --output data/generated/v0.6 --manifest data/generation/v0.6/dataset_manifest.json
python3 -B -m scripts.mission1_dataset validate --rules data/generation/v0.6/generation_rules.json --output data/generated/v0.6 --manifest data/generation/v0.6/dataset_manifest.json
```

7-day deadline / day-3 response and equal administrative scenario weights are synthetic,
recorded in rules and manifest. No inferred qualification or target-based resampling.
Historical command examples below must not be used to overwrite preserved versions.

# v0.5 Application / Document candidate

Active baseline remains v1 (source v0.4). v0.5 is UNREVIEWED, NOT FROZEN.
Use explicit paths; legacy Python defaults remain v0.4 for historical regression compatibility.
Do not run legacy generation commands against preserved candidate directories.

```sh
python3 -B -m scripts.mission1_dataset generate --rules data/generation/v0.5/generation_rules.json --output data/generated/v0.5 --manifest data/generation/v0.5/dataset_manifest.json
python3 -B -m scripts.mission1_dataset validate --rules data/generation/v0.5/generation_rules.json --output data/generated/v0.5 --manifest data/generation/v0.5/dataset_manifest.json
python3 -B -m unittest discover -s tests -p 'test_mission1*.py'
```

New eligibility and experience tables are version-optional; legacy canonical bytes remain unchanged.
Document CLOSED is insufficient application evidence, not candidate ability failure.
Same-experience 2-of-3 categories and personal ownership are required. Reposted public eligibility
structure and synthetic dates/distributions are separate. See docs/07 and docs/09 v0.5 contracts.
Manifest implementation_parameters.application_model records the predeclared scenario catalog.
The following v0.4/v0.3/v0.2 sections preserve historical documentation.

# v0.4 Final Dataset Candidate

Current CLI defaults target v0.4, the UNREVIEWED / NOT FROZEN Final Freeze Candidate, not Dataset v1. v0.1/v0.2/v0.3 are write-protected history.
See docs/07 and docs/09 v0.4 final Human Review contract (takes precedence below).

Coverage records decisionability separately from level/sufficiency: linked FIRST
agreed direct LIMITED/MODERATE/STRONG can satisfy coverage. Existing explicit
limitation rejection is separate. Missing/unresolved remains EVIDENCE_PENDING.
Calibration reviews record eligible opportunity, actual persisted Observation IDs,
explicit same-evidence disagreement / same-context direct conflict triggers, and
optional meeting ID. Consensus LIMITED/NOT_OBSERVED alone does not create a meeting.
Re-review cannot proceed with any nondecisionable MUST. After one follow-up it
terminates DNP for insufficient decision basis without inventing skill deficiency.
Accepted uncertainty is scoped to decisionable noncore context or Learnable gaps.
Fixed pool 30 is a retained generation parameter, not product/employer policy.
Offer/Ready/evidence response distributions, resource parameters and seed unchanged.

```sh
python3 -B -m scripts.mission1_dataset generate
python3 -B -m scripts.mission1_dataset validate
python3 -B -m scripts.mission1_dataset report
python3 -B -m unittest discover -s tests -p 'test_mission1*.py'
```

No automatic Freeze, representative selection or Mission 2 analysis.

---

# v0.3 Interview + Decision Model — historical implementation

Historical v0.3 CLI defaults used v0.3; the current CLI defaults to v0.4. v0.1/v0.2/v0.3 paths are now write-protected.

```sh
python3 -B -m scripts.mission1_dataset generate
python3 -B -m scripts.mission1_dataset validate
python3 -B -m scripts.mission1_dataset report
python3 -B -m unittest discover -s tests -p 'test_mission1*.py'
```

SSOT: docs/07 and docs/09 §3.2 v0.3 approval. Three evaluators share one 60-minute
FIRST_INTERVIEW_SESSION; activity_sessions links three zero-duration evidence domains.
Only the parent session owns interview participation effort (3h). Calibration is
conditional on persisted direct observations and is separate two-person/15-minute labor.
Fixed 30-person synthetic pool has 2 initial interview hours per evaluator (60h).
Additional hours are ceil(Gap/30) per evaluator, never extra 80h panels. Aggregate
capacity_assignments and per-evaluator reservations independently replay consumed,
reserved and released hours; calibration has its own purpose and is not charged to
interview capacity. This is a simplified synthetic resource allocation, not an employer calendar.

FIRST coverage explicitly classifies core Skills 01/02/03 as A supported direct
coverage, B agreed explicit limitation, C missing evidence, D unresolved evidence.
All A advance; B supports non-progression; other cases remain EVIDENCE_PENDING.
No missing-to-failed conversion, ranking, quota or Target-based cut.

Targeted follow-up records the actual HOLD snapshot, question, prior Evidence and
Observation references, and a question-specific response category. It does not invoke
ordinary observable-pattern generation. Response options and all implementation
parameters are in generation_rules and the manifest. Offer/Ready distributions and
seed 20260924 remain unchanged. No freeze or representative/Main Story selection.

The following sections describe the retained **v0.2 historical implementation**;
The v0.4 contract above and current SSOT take precedence. Historical regression suites exercise v0.2
and v0.3 explicitly; test_mission1_final_candidate.py exercises the v0.4 contract.

---

# Mission 1 Dataset Generator + Independent Validator vNext

Python 표준 라이브러리만 사용하는 오프라인 합성 시나리오 도구다. UI/서버에서 실행하지 않는다.
주 계약은 [docs/09](../../docs/09_mission1_data_specification.md), 판단 의미는 [docs/07](../../docs/07_recruitment_design_specification.md)다.
Synthetic Human Scenario는 가상 역할의 판단 기록이며 실제 사람의 평가나 운영용 자동 채용 판단이 아니다.

## 실행과 보존

저장소 루트에서:

```sh
python3 -m scripts.mission1_dataset generate
python3 -m scripts.mission1_dataset validate
python3 -m scripts.mission1_dataset report
python3 -m unittest discover -s tests -p 'test_mission1*.py' -v
npm test
npm run lint
```

v0.2 당시 기본 후보는 `data/generated/v0.2/`, 생성규칙·단일 manifest·검증 및 sanity report는 `data/generation/v0.2/`였다. 현재 기본 경로는 상단 v0.4 절을 따른다.
`data/generated/v0.1/`와 `data/generation/` 바로 아래 기존 산출물은 Audit history로 보존한다.
현재 CLI는 v0.1 및 synthetic/presentation 경로를 쓰지 않는다. v0.1의 과거 PASS를 최신 계약 준수로 해석하지 않는다.
다른 검토 경로에는 `--rules`, `--output`, `--manifest`를 함께 지정한다.
`generate`는 원자료 전체 생성 → 직렬화 → 파일 재독해 → 독립 검증 → manifest/report를 실행한다.
실패하면 종료 코드 1과 오류를 기록하고 이전 통계를 성공 결과로 남기지 않는다.

Seed 20260924, 관측창 2026-10-01~2027-10-31, 기존 유입·원자료 패턴·응답/철회 가중치는 유지한다.
난수 stream namespace도 v0.1 값을 유지해 버전 문자열 변경이 모든 추출을 흔들지 않도록 했다.
새 활동·Skill·mentor 등은 별도 keyed stream을 사용한다. seed/분포 탐색이나 Target forcing은 없다.
`generated_at`은 고정 논리 시각이다. manifest에는 규칙·데이터·실행 소스 hash와 실제 검증 결과를 기록한다.
개별 row를 수정하지 않는다. 오류 수정 시 규칙/코드를 고친 뒤 전체 후보를 재생성한다.

## 파일 책임

| 모듈 | 책임 |
|---|---|
| common.py | keyed randomness, offset-aware 시각, CSV/JSON, 보호 경로 |
| schema.py | 필드·NULL·enum·키 |
| evidence.py | source별 원자료, Observation 저장, Observation 기반 Calibration, 단계/최종 판단 시나리오 |
| generate.py | Stage·Activity, HOLD 후속 흐름, 응답/입사/업무/Ready |
| capacity.py | Initial→Demand→Gap→자원 결정, 예약·해제·실제 소비 |
| validate.py | schema·FK·시간·관측창·manifest 무결성 |
| invariants.py | SSOT에서 별도 구현한 독립 의미 제약 |
| report.py | Raw Event의 기술 통계. Mission 2 WHY/Story 선정 아님 |

CSV는 UTF-8/LF, 빈 셀은 NULL이다. JSON payload는 canonical key 순서를 사용한다.
Skill Decision relation은 `skill_decision_observations(decision_id, observation_id)`다.
v0.1의 raw-decision relation은 v0.2에 생성하지 않으며 존재하면 오류다.

## Source / Skill Matrix와 판단 계보

숫자는 `M1_SKILL_` 뒤 두 자리다. PLUS 근거를 억지로 모두 만들지 않는다.

| 활동 | Source | Verification | 허용 Skill |
|---|---|---|---|
| DOCUMENT_REVIEW | APPLICATION_RESPONSE | SELF_REPORTED | 01,04,05,06,08 |
| CODING_TEST | CODING_TEST_RESPONSE | DIRECT_TASK | 03 |
| TECHNICAL_ASSESSMENT | TECHNICAL_ASSESSMENT_RESPONSE | DIRECT_TASK | 01,02,07 |
| AI_CASE | AI_CASE_RESPONSE | DIRECT_TASK | 01,03 |
| PRACTITIONER_QA | INTERVIEW_RESPONSE | DIRECT_INTERACTION | 04,05,06,08 |
| VALUES_BEHAVIOR_INTERVIEW | INTERVIEW_RESPONSE | BEHAVIORAL_INTERACTION | 04,05 |
| FOCUSED_FOLLOW_UP | 기술 Task 또는 행동 질의 | 해당 직접 확인 방식 | INITIAL HOLD plan의 미해결 MUST만 |

각 Source의 맥락과 표현을 구분하고 action/verification/revision/ownership을 원자료로 기록한다.
`verification_mode`, `context_id`는 원자료 메타데이터이며 Skill 수준은 Observation에만 있다.
Observation의 `explicit_limitation`은 직접 확인된 검증 미실행을 모호한 팀 기여/미관찰과 구분한다.
지원 답변의 STRONG Observation은 허용한다. application-only canonical Skill Decision은 만들지 않는다.
STRONG Skill Decision은 non-SELF_REPORTED STRONG 지지 Observation을 요구한다.

Calibration은 저장된 Observation의 level/explicit limitation과 Evidence 메타데이터를 소비한다.
raw JSON 재해석, 평균, 수치 Level, 최신 근거 자동 우선은 없다.
결정 rationale에는 지지 Observation, 제한·미관찰·평가자 차이와 다음 구분을 보존한다.

- Evidence Evolution: 후속 직접 관찰이 앞선 미확인을 보완한다.
- Context Difference: 다른 과제에서 확인된 제한과 수행 근거를 각 맥락에 남긴다.
- Evaluator Disagreement: 같은 근거에 대한 역할별 해석 차이; 같은 직접 맥락의 명시적 상충도 미합의로 남긴다.

독립 직접 관찰에서 해당 Skill의 행동/검증이 확인되면 다른 맥락의 모호성을 그 근거의 한계로 보존하며 합의할 수 있다.
이 합성 Calibration 정책의 현실성은 사람의 Rules/Reality Review 대상이다.

## Stage와 Final Review

DOCUMENT_SCREEN은 원답변·Evidence Candidate·후속 질문을 기록한다. 검증된 공개 기본요건이 없으므로
임의 자격을 만들어 실패시키지 않는다. 이번 후보의 서류 ADVANCED가 높아도 목표에 맞추지 않는다.

PRE_ASSESSMENT는 코딩 검증 미실행이라는 명시적 직접 기준을 사용한다.
FIRST_INTERVIEW는 기술 MUST의 반복된 직접 제한과 보완 근거를 검토한다.
SECOND_INTERVIEW는 학습/협업 행동 영역을 검토하며 두 영역 모두 명시적 제한이고 보완 근거가 없는 경우를 비진행 사유로 삼는다.
NOT_OBSERVED/INSUFFICIENT_EVIDENCE 자체는 어느 단계에서도 실패 사유가 아니다.
Stage rationale에는 해당 단계 Observation 참조와 기준이 있고 Offer-level 결론은 없다.

INITIAL FINAL_REVIEW는 Skill snapshot과 MUST/learnable/uncertainty를 추적한다.
HOLD에는 reason과 질문·Skill·Context·method를 가진 resolution plan을 기록한다.
최대 한 번의 FOCUSED_FOLLOW_UP → 새 Observation → FOLLOW_UP_CALIBRATION → RE_REVIEW를 추가한다.
후속 확인은 계획된 질문만 대상으로 하며 같은 원자료 패턴 분포를 사용한다. rescue용 성공 패턴을 주입하지 않는다.
RE_REVIEW의 남은 명시적 제한/해석 충돌은 합성 패널이 비진행 이유로 기록한다.
미관찰만 남으면 자동 탈락시키지 않고 불확실성 수용 및 업무 준비 지원을 명시한 진행 판단을 기록한다.
이 처리 정책은 실제 기업 정책이 아니라 검토 가능한 생성 가정이다.

FINAL_REVIEW Stage는 완료 시 result=NULL, 진행 중 IN_PROGRESS다. ADVANCED/FAILED로 최종 판단을 복제하지 않는다.
내부 검토의 completed_at은 최초 요구자료 준비 시각, 후속검증 완료는 별도 Activity가 소유한다.
최종 Stage decision_at은 관측된 마지막 review 시각이며 각 INITIAL/RE_REVIEW 시점은 final_decisions에 보존한다.
관측창 밖 후속검증/결정은 생성하지 않고 미완료로 남긴다.

## Capacity와 시간

Initial 80h, 계획 4h/후보, 계획 20명은 quota가 아니다.
사전검증 후 통보된 전체 cohort를 application ID 목록과 시점으로 고정한다.
Demand=cohort×4, Gap=max(Demand−Initial,0). 부족하면 2일 뒤 HR의 추가 evaluator resource 결정으로
80h 단위 합성 panel을 확보한다. 추가 panel은 FIRST_INTERVIEW의 주 2회 block 공급도 늘린다.
Resource block/대안/판단/효력시각을 기록하며 최초 80h를 덮어쓰지 않는다.

`interview_capacity_events`: INITIAL_PLAN / GAP_IDENTIFIED / CAPACITY_ADDED / CAPACITY_RELEASED.
전체 cycle demand는 전체 예산과 비교한다. Gap 이벤트 자체는 예산 증감이 아니다.
`capacity_assignments`: reservation_id별 RESERVED / RELEASED / CONSUMED.
CONSUMED는 activity_id+participant_id의 실제 참여구간과 일치한다. 계획 4h를 대입하지 않는다.
완료/확인된 철회/취소/미응답의 미사용 예약은 RELEASED이며 cycle CAPACITY_RELEASED가 아니다.
미응답/취소에서 WITHDRAWN을 추정하지 않는다. `CANCEL_CONFIRMED` 처리는 테스트하며 기본 분포에 새 취소 가중치를 추가하지 않았다.
예약 잔여·소비·가용량은 시간순 이력을 재생해 검사한다.

평가자는 재사용되는 pool ID다. 동일 ID의 역할과 실제 참여 구간을 검사한다.
겹치는 Activity block만 피해 예약하며 미래 후속검증 예약 전의 빈 구간을 사용할 수 있다.
개인의 출퇴근·휴가·휴일 Calendar를 합성하지 않는다. 상세 workforce scheduling의 현실성은 모델링 한계다.

실제 timestamp는 관측창 안이다. 예약/예정 입사/응답기한/계획 Ready는 미래 날짜가 가능하다.
원자료가 저장됐지만 연결·Observation·Calibration 전에 관측이 끝난 경우 미검토 원자료로 보존할 수 있다.
판단이 존재한다면 전체 canonical lineage와 판단 이전 시각이 필수다.

## Offer, Onboarding, Ready

Offer response_deadline은 14일의 합성 가정이다. 응답 추출은 ACCEPTED/DECLINED/NO_RESPONSE이며
EXPIRED는 deadline까지 응답이 없고 관측창이 deadline에 도달한 경우에만 파생한다.
deadline 전 무응답은 Open이다. 응답 부재의 motive는 UNKNOWN이다.
수락 뒤 확인된 PRE_JOIN_WITHDRAWAL 또는 workforce_events의 JOINED로 이어진다.

개인 Gap은 Final Review learnable gap·수용한 불확실성·로컬 업무 준비 요구에서 재계산한다.
이번 work-prep는 파이프라인 검증/팀 인수인계이며 관련 selection Skill이 STRONG이면 불필요한 반복 Gap을 생략한다.
Gap에는 final_decision_id, requirement_ref, rationale, 관련 원근거를 기록한다. 고정 Skill06을 모든 입사자에게 넣지 않는다.
Gap이 없는 사람도 Skill 재평가가 아닌 로컬 통합 업무 Task를 수행한다.

planned_ready_at은 180일 계획이다. 실제 작업은 onboarding_tasks.work_evidence가 소유한다.
수행·확인·기록 시각과 mentor review를 구분한다. 검증 완료만으로 멘토 확인을 강제하지 않는다.
필요한 Task별 검증/멘토 확인 또는 해당 Skill의 후속 업무 확인을 모두 검토해야 Ready를 기록한다.
READY_CONFIRMED의 source_ref JSON은 업무 근거 목록, 개인 Gap 목록, 사람 rationale을 담는다.
confirmed_by/confirmed_at과 post-join 근거가 필수다. 계획일 경과만으로 Ready/실패를 만들지 않는다.
미확인 업무는 연장 또는 미완료로 남으며 목표일 Available Supply에 포함하지 않는다.

## 검증과 한계

Validator는 Generator의 interpret/calibrate/stage/final 함수를 import하거나 호출하지 않는다.
구조, lineage, source matrix, Stage/Final 경계, HOLD, Capacity replay, Offer deadline,
개인 Gap, post-join Work Evidence/Human Confirmation, 관측창을 별도로 검사한다.
테스트는 위반 row 주입, 원판단 함수 호출 차단, 결정적 재생성, Target/Channel 비의존,
미관찰-only·미응답·취소·불완전 관측창·멘토 확인 분기를 검사한다.
테스트 fixture의 분포/seed 변경은 branch 검증이며 실제 후보의 seed search가 아니다.

자동 PASS는 Rules/Reality Review 승인이나 Freeze가 아니다.
대량의 합성 템플릿, 일정 pool 가정, 역할별 해석, 남은 불확실성의 수용, 교육·멘토 분포는 현실성 검토 대상이다.
PLUS 09는 검증 Source가 없어 근거를 만들지 않는다. 공개 자격·공식 회사 정책은 검증 대기 상태다.
UI 변경, v1 Freeze, 대표 3명/Presentation Mapping, Mission 2 Main Analysis Story는 수행하지 않는다.
