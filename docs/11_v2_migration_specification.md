# PeopleOps Office — V2 Migration Specification

## 1. 책임과 기준

최신 후속 구현 기록은 §13이다. 이전 문서 동기화 시점의 STOP/미구현 표기는 당시 이력으로 보존한다.

이 문서는 확정 V2를 현재 구현으로 이전할 때의 재사용·확장·교체·신규 책임과 의존성을 정의한다.
구현 지시의 실행 결과가 아니다. 이번 작업은 AGENTS.md와 docs/00~11 동기화에서 종료한다.

기준은 2026-09-24 제공된 V2 Documentation Synchronization 요청, 회수한 확정 설계,
현재 작업 트리의 문서·코드다. 기존 미커밋 변경을 현재 구현 기준으로 읽었으며 되돌리지 않았다.
제품 결정은 최신 명시적 확정이 우선한다. 기아의 실제 공개 사실은 원문을 우선하며
설계 대화가 원문을 대체하지 않는다. 출처 부족은 8절, 미정은 7절에 남긴다.

후속 Dataset v0.1 Rules Audit와 사용자 확정 Decision/Data Contract를 최신 기준으로 추가한다.
초기 동기화·v0.1 자동 PASS·후속 Audit를 구분하며 충돌 시 최신 명시적 확정을 우선한다.

## 2. 현재 구현 조사

2026-09-24 코드 읽기 기준이다. 빌드·UI·분석 검증을 이번 작업에서 수행했다는 뜻이 아니다.

| 현재 파일 | 확인한 역할 / 상태 |
|---|---|
| `app/page.tsx` | useReducer 기반 탐색, Intro/Briefing/Case/Board 조합. Company를 호출하지 않음. Data Lab은 준비 안내 |
| `app/exploration/model.ts` | workforce/talent/attraction/operations/onboarding/kpi Step, Room 데이터, CURRENT/REVIEWED/UPCOMING, 자유 select, Plan 산술 |
| `app/game/OfficeWorld.tsx` | 현재 탐색 model을 읽는 방 렌더링·카메라·zoom/drag·선택. V2 Scene Engine 아님 |
| `app/exploration/CasePanel.tsx` | EvidenceBadge, Disclosure, Workforce 클릭 focus와 내부 Content Camera, TalentDeskContent. 후속 단계는 준비 콘텐츠 |
| `app/exploration/MissionIntro.tsx`, `MissionBriefing.tsx` | 시작·합성 요청·Goal 단계 |
| `app/exploration/MissionBoard.tsx`, `PeopleOpsHeader.tsx` | Mission 안내, Step 목록/위치 표시. V2 진행 제한과 다름 |
| `app/exploration.css`, `app/office.css`, `app/globals.css` | 현재 패널·픽셀 공간·스크롤·모션 표현 |
| `data/case/mission1.json` | 16/12/확정 이동/목표일, 기존 Step 설명. 일부 문서 절 번호 참조는 V2 이관 필요 |
| `data/case/talent_profile.json` | 기존 13 Skill의 인재 요건/출처. 최신 V2 분류로 실제 데이터 이관은 미실행 |
| `app/game/sim.ts`, `world.ts`, `staff.ts`, `report.ts`, `worker/` | 남아 있는 템플릿 영역. 홈 실행 책임과 혼동하지 않음. 삭제·개편은 별도 검토 |
| `package.json` | vinext build/lint 및 기존 테스트 명령. 의존성·배포 설정 변경 없음 |
| `tests/rendered-html.test.mjs`, `tests/exploration-browser.mjs` | 기존 UI 검증 자료. V2 수용 기준으로 검토할 후속 대상 |

기존 05의 'Home이 Company를 생성한다', '방은 클릭 대상이 아니다' 같은 초기 템플릿 설명은
현재 조사와 다르므로 V2 목표 명세에서 제거했다. 현재 파일 경로가 존재한다는 것과
모든 V2 기능이 구현되었다는 것은 다르다.
후속 작업에서 `scripts/mission1_dataset/` 생성기·Validator·Report와 `data/generated/v0.1/` 검토 후보를 추가했다.
V2 Scene/Dialogue, freeze된 v1, 실제 Mission 2 분석 연결은 여전히 미완료다.
실행/구현 상세와 검토 경계는 [생성기 개발 문서](../scripts/mission1_dataset/README.md)를 따른다.

v0.1은 deterministic generation 및 당시 Validator PASS 이후 Rules Audit에서 D-01과 modeling issues가 확인됐다.
APPLICATION_RESPONSE-only STRONG Skill Decision은 07 의미 계약과 충돌했다.
v0.1은 Audit history로 보존하고 Freeze 후보로 승격하지 않는다. 후속 규칙/Validator/새 Dataset은 미구현·미생성이다.

## 3. 유지·확장·교체·신규 매핑

| 분류 | 현재 기반 | V2 책임 |
|---|---|---|
| KEEP | OfficeWorld, 공간·가구·픽셀 표현 | Office 정체성, 방 렌더링, 카메라·zoom/drag |
| KEEP | CasePanel shell, Disclosure, 내부 Scroll | 읽기 가능한 패널, 클릭 기반 공개, 수동 입력 우선 |
| KEEP | Mission Board, Intro/Briefing, EvidenceBadge | 요청과 Mission 문맥, 네 Provenance |
| EXTEND | CasePanel | Scene과 연결된 Decision Layer, 원자료·판단·대안·불확실성 |
| EXTEND | Mission Board/Header | Mission lifecycle, 6단계 진행, 완료 Summary |
| EXTEND | Data Lab 준비 안내 | 실제 코드/결과/표·차트/가설·한계를 보는 Python Workspace |
| EXTEND | Plan 산술·Talent Profile | canonical Dataset/Plan 연결, Skill/Evidence 추적 |
| REPLACE | 공간별 정적 안내 역할 | 실제 업무 정보 제공·판단·논의에 필요한 Role Character |
| REPLACE | 설명 카드 중심 진행 | Human Scene과 Decision Layer의 연결 |
| REPLACE | Step=Room, 자유 select, Next Room | Stage/Scene 상태 전이, 예정 Jump 차단 |
| NEW | 아직 없음 | Scene Engine, Dialogue, Candidate View, Job Posting Editor/점검, Funnel Planning |
| NEW | 아직 없음 | Assessment Matrix, Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision |
| NEW | 아직 없음 | Capacity Gap / Human Capacity Decision / Revised Capacity, HOLD Focused Follow-up / Re-review |
| NEW | 아직 없음 | Offer response_deadline / derived EXPIRED, Planned vs Actual Ready / Work Evidence confirmation |
| NEW | 아직 없음 | Experience Evidence, System/Python Reveal, 실제 실행 기록/결과 표시 |

위 이름은 구현 책임이며 이번에 생성한 component 목록이 아니다.
Office를 20개 방으로 늘리지 않고 7개 공간에서 Scene을 교체한다.
Talent Desk→채용전략실 Workshop, Onboarding→업무공간으로 이관한다.
원본 License/Credit은 유지한다. 게임 시간·dayScript·배속·자동 보고가 Scene 진행을 결정하게 하지 않는다.
Company 분리는 이미 홈에 반영된 상태이므로 같은 작업을 다시 수행할 계획으로 쓰지 않는다.

## 4. 도메인·상태·데이터 이관

Mission → Stage → Scene을 중심으로 Space/Participants/Dialogue/System Action/Interaction/
Evidence/Decision/Transition을 연결한다. Scene 필드 개념은 scene_id, mission_id, stage, space,
participants, core_question, trigger, human_events, system_events, interactions, evidence_refs,
decision, state_transition, next_scene다. 실제 타입/저장 방식 확정과 구현은 후속이다.

탐색 상태와 결과 데이터는 분리한다. Scene 선택, 공개한 내용, 완료 Summary, 카메라 상태가
합불·인원·Ready·분석 결과를 바꾸지 않는다. 완료 Summary에서 현재 진행 문맥으로 돌아올 수 있어야 한다.
미래 Stage를 지도·목록·Board로 우회하지 않는다. 진입/복원 정책의 세부는 OPEN-13이다.

지원 건 application_id와 지원자 candidate_id를 구분하는 V2 계약으로, 단일 onboarding 예시는
profiles/skill_gaps/tasks/workforce_events로 이관한다. 원본 Evidence에 있던 level은
observation/decision으로 분리한다. Stage/Activity, Skill Decision의 복수 근거, Offer 객체/이력,
Workforce 입사/Ready의 canonical owner를 구분한다. 상세 계약은 09가 소유한다.
기존 데이터의 옛 Step·문서 절 참조도 후속 구현에서 수정해야 하며 이번에는 데이터 파일을 수정하지 않는다.

최신 canonical lineage는 `Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision`이다.
Stage Transition과 Final Hiring Decision은 분리하고 Skill Decision은 skill_decision_observations로 persisted Observation을 참조한다.
APPLICATION_RESPONSE는 SELF_REPORTED이며 자기기술의 STRONG Observation과 SELF_REPORTED-only STRONG Skill Decision 금지를 구분한다.
Calibration은 Evidence Evolution / Context Difference / Evaluator Disagreement를 구분한다.
80h는 cycle INITIAL_PLAN, 후보당 4h·20명은 계획이다. Capacity 부족은 합불 기준이 아니며 Initial→Demand→Gap→Human Decision→Revised→Actual을 보존한다.
Reusable evaluator pool의 reserved/released/consumed를 구분한다.
HOLD는 Reason+Resolution Plan→최대 1회 Follow-up→새 Observation→Calibration→Re-review이며 HOLD 재발행은 금지한다.
EXPIRED는 deadline과 응답 Event 부재에서 파생한다. READY_CONFIRMED는 개인별 Gap·post-join Work Evidence·Human Confirmation을 요구한다.
06의 최신 Scene은 M1-01~25이며 Capacity 재검토 M1-12, HOLD subflow M1-18~19다. 기존 UI 번호/상태 매핑은 후속 구현에서 이관한다.

## 5. 후속 구현 순서와 의존성

이번 작업 종료 후 별도 작업에서 아래 순서를 진행한다. 이 문서가 다음 작업 실행 승인은 아니다.

| Phase | 구현 책임 | 의존 / 완료 확인 |
|---|---|---|
| 1 Foundation | Scene Engine, Role Character, 6단계 Progress, Decision Layer | 05/06 계약, 상태 정합성, 결과 불변 |
| 2 Mission 1 Human Layer | 인력계획·인재 정의·채용 설계·검증·Offer·온보딩 Scene | 06/07, 원문/시나리오 구분, 미생성 결과를 채우지 않음 |
| 3 Canonical Dataset Integration | Workforce/Funnel/Evidence/Offer/Ready/KPI 연결 | Audit 반영 Generation Rules/독립 Validator 수정 → 새 version 생성 → 자동 Validation → Human Rules/Reality Review → 승인 → Freeze → canonical 연결 |
| 4 Mission 2 | Data Lab Python UX와 경력 채용계획 | 실제 분석, 10의 지표 정의, 새 모집단 조건 |
| 5 Polish | 카메라·대사·캐릭터·Reveal·Think Before Reveal·전환 | 결과/판단 구조를 바꾸지 않는 표현 조정 |

위는 확정 Migration의 구현 Phase 순서다. Dataset 후보 생성→검토→freeze는 별도 데이터 작업이며
Phase 3의 선행 의존성이다. 후속 대화의 Dataset 우선 지시는 화면에 맞춘 결과 조작을 피하고
본격 데이터 연결 전에 정본을 확보한다는 원칙으로 유지한다.
v0.1 생성 당시 Open Issue의 의미 계약은 문서화했으나 후속 Rules Audit에서 구현 불일치를 확인했다.
v0.1은 보존하고 후속 버전에서 새 계약을 구현·검증한다. 동일 seed를 우선 사용하되 UI/Target에 맞춘 seed search·target forcing은 금지한다.
Foundation 검토와 Dataset 준비의 세부 실행 일정은 이번 작업에서 정하지 않는다.

후속 코드 변경에는 Production build와 적절한 lint/동작 검증이 필요하다.
현재 vinext/Vite/Cloudflare 설정을 UI 이관과 함께 임의 교체하지 않는다.
Production 목표 Vercel, GitHub main 자동 배포, 공개 URL·무로그인·외부 AI 비의존을 유지한다.

## 6. V2 구현 완료 조건

- Mission 1 요청부터 Ready·세 Outcome까지 끊김 없이 탐색한다.
- 모든 주요 숫자는 Plan 정본 또는 canonical Dataset 실제 계산과 일치한다.
- 사람 판단과 System/AI 보조 출력, 네 Provenance, 출처 상태를 구분한다.
- 원답변·과제·관찰·판단과 관련 근거를 추적한다. Ranking/자동 합불이 없다.
- Mission 1과 Mission 2는 같은 Dataset 버전을 참조하고 분석 결과가 재현된다.
- 경력의 Capability·Experience Evidence·새 가정을 다루고 계획 확정에서 종료한다.
- 예정 Stage Jump를 막고 완료 Summary와 결과 데이터는 분리한다.
- 05의 접근성·Skip/reduced motion·스크롤·오류 기준을 만족한다.
- 실제 공개자료 검증과 미결정 해소를 완료로 속이지 않는다.

- Observation lineage와 SELF_REPORTED-only STRONG 금지, Stage/Final 분리를 검증한다.
- Capacity 이력·pool·실제 소비와 HOLD Reason/Plan/최대 1회 Follow-up/Re-review를 추적한다.
- EXPIRED의 deadline/응답 부재와 READY_CONFIRMED의 post-join 근거/사람 확인을 검증한다.
- Validator는 Generator 판단 함수를 oracle로 재사용하지 않고 09의 독립 invariant를 검사한다.

현재는 위 조건을 통과했다고 선언하지 않는다.

## 7. Open Issues

OPEN은 미결정, SOURCE NOT AVAILABLE은 원문 미확보, TO VERIFY는 추가 확인 필요다.
이 표는 이번 작업이 새 제품 정책을 승인한 목록이 아니다.

| ID | 남은 문제 | 책임 문서 / 필요한 결정 | 구현 영향 |
|---|---|---|---|
| OPEN-01 | Python 실제 실행의 제품 제공 방식 | 05/10. 브라우저 실행 또는 실제 사전 실행 산출물 탐색, 로그 표현 | 분석 UI 구현 전. 별도 인프라 임의 추가 금지 |
| OPEN-02 | Mission 2의 상위 6단계 적용 | 05/10. 분석·계획만 수행하는 Mission의 진행도 매핑 | 실제 채용·Ready 완료로 표시 금지 |
| OPEN-07 | 경력 시나리오 수치 | 10. 인원·목표일·현재 Capability·Ramp-up. 과거 2명/2028-03/2개월은 예시 | Mission 2 Case 확정 전 |
| OPEN-09 | 데이터 준비와 Migration 세부 일정 | 11. Phase 순서는 유지, Dataset freeze는 Phase 3 전제 | 이번 작업에서 실행 일정·병렬 진행을 승인하지 않음 |
| OPEN-10 | 공개 근거 검증 | 07/08/10, 아래 출처 등록부 | 출처 의존 주장·공식 문구 매핑은 검증 대기 |
| OPEN-11 | 과거 분석 예제의 실행 적합성 | 10. 미정의 열·enum 대응 등을 실제 코드 작성 때 검증 | 이번에는 예제 코드를 실행 정본으로 복사하지 않음 |
| OPEN-13 | UI 표현·복원 상세 | 05/06. 좌표·크기·breakpoint·대사·모션·URL/뒤로가기/재방문 | 핵심 판단 구조와 분리하여 후속 구체화 |

### 7.1 Resolved Issues — Dataset Open Issues Documentation Update

사용자 확정 결정으로 아래 상태를 RESOLVED로 갱신했다. 주 SSOT는 09다.
이력은 보존하며 코드·Dataset·검증 실행 완료를 뜻하지 않는다.

| ID | 상태 / 해결 범위 | 반영한 결정 |
|---|---|---|
| OPEN-03 | RESOLVED — Timestamp Contract | ISO 8601 offset-aware Asia/Seoul, invited/decision/notified/withdrawn 시각 분리, 관측창·NULL Metric·IN_PROGRESS 유지 |
| OPEN-04 | RESOLVED — Funnel Aggregation | 고유 candidate 단위, Target 라벨과 Actual 대응, Stage/Activity 분리, 이탈을 포함하는 Stage 진입 분모 |
| OPEN-05 | RESOLVED — Canonical Structure | 5계층 owner, application/candidate 분리, Activity·복수 Evidence 관계·Offer 이력·Workforce·stable ID·manifest |
| OPEN-06 | RESOLVED — Synthetic Human Scenario | 합성 Evidence/Observation/Decision, provenance, Rubric 기반 생성, 개별 합불이 아닌 Dataset 생성 규칙 검토 |
| OPEN-08 | RESOLVED — Representative Cases | Desired Contrast는 생성 입력 아님. Freeze 후 선정하고 별도 Presentation Mapping 사용 |
| OPEN-12 | RESOLVED — Dataset v0.1 KPI/원자료 계약 범위 | Workforce/Funnel/시간/참여 person-hours/Offer/입사·Ready 원자료. Main KPI/Story 또는 범위 밖 지표 확정 아님 |

### 7.2 Generator v0.1 Readiness 기록

아래는 v0.1 생성 직후의 역사적 기록이다. 최신 Readiness는 §7.3이 우선한다.

이번에 요청된 Dataset 의미 계약에 추가 제품 정책 결정을 요구하는 blocking issue는 남아 있지 않다.
후속 사용자 요청으로 생성기 v0.1 구현·검토 데이터 생성·자동 검증을 수행했다. Dataset 사람 검토와 Freeze는 미수행이다.
09의 Implementation Notes는 생성 규칙·실행 스키마·개발 문서에서 구체화하고 Validator로 검증했다.
새로운 의미 정책이 필요해지면 해당 부분만 별도 결정으로 남긴다. 자동 PASS는 생성 규칙의 현실성 승인과 다르다.
공개 원문 검증은 OPEN-10으로 유지하며 미검증 기업 사실을 생성 규칙의 공식 근거로 쓰지 않는다.
남은 UI·Mission 2·일정·분석 예제 이슈를 이번 결정으로 해결한 것으로 간주하지 않는다.

### 7.3 Dataset Rules Audit — Resolved Decisions

자동 Validation PASS 후 Rules Audit에서 D-01(지원 답변만으로 STRONG Skill Decision) 및 modeling issues를 확인했다.
Generator 판단 함수를 Validator가 동일하게 재사용하면 SSOT 준수를 독립적으로 보장하지 못한다.

| 영역 | 확정 계약 / 후속 구현 책임 |
|---|---|
| Evidence / Stage | SELF_REPORTED와 direct verification 구분; DOCUMENT_SCREEN은 검증 후보 발견; Stage/Final 분리 |
| Calibration | persisted Observation lineage; Evolution/Context Difference/Disagreement 구분 |
| Capacity / Evaluator | cycle 80h·계획 4h·20명은 quota 아님; Gap→사람 운영 결정; reusable pool·예약 해제·소비 구분 |
| HOLD | terminal 아님; Reason+Plan·최대 1회 Focused Follow-up·HOLD 없는 Re-review |
| Offer | response_deadline과 확인된 응답 Event 부재 기반 EXPIRED; motive 추론 금지 |
| Ready | 개인별 Gap·Planned/Actual 분리·post-join Work Evidence·Human Confirmation |
| Validator | 저장된 Dataset의 독립 invariants, generator 판단 oracle 재사용 금지 |

06~11 문서 반영 완료. Generation Rules/Validator의 최신 계약 구현과 새 Dataset 검증은 미완료다.
기존 OPEN-03/04/05/06/08/12 resolved history 및 OPEN-01/02/07/09/10/11/13 상태를 유지한다.
v0.1 row는 수정하지 않으며 후속 version에서 구현한다.

## 8. 출처 등록부

원본 파일은 로컬 handoff에 있고 public repo에 복사하지 않았다.
자료 ID는 원자료 추적을 위한 문서 식별자이며 Dataset Evidence ID가 아니다.
공식/아카이브/캡처/요약이라는 출처 성격과 네 Provenance는 별개의 축이다.

| ID | 자료 | 확인 범위 / 상태 | 사용할 수 있는 범위 |
|---|---|---|---|
| HR-01 | `hr테크 1장까지.pdf` | 82페이지 스캔. 앞부분 목차 확인, 본문 전체 검증 아님. TO VERIFY | HR 개념 참고. 개별 주장에 쓰려면 해당 페이지 확인 |
| HR-02 | `HR테크_요약_프롤로그-1부.pdf` | 22페이지, 첫 부분이 상세 요약임을 확인 | 2차 학습 요약. 도서 원문/직접 인용 근거로 대체하지 않음 |
| HR-03 | 대화에서 언급된 HR Magazine 6월호 PDF | SOURCE NOT AVAILABLE. 연도·정확한 발행처 확인 필요 | 참고 배경. 새 기능 요구사항을 만들지 않음 |
| KIA-01 | `mission1_application_questions.png` | 사용자 제공 ML Engineer 지원 문항 3개 확인. URL·게시일·공고 전체는 TO VERIFY | 750/750/500자 문항의 내용 참고. 공식 공고 전문으로 표현 금지 |
| KIA-02 | 신입 ML Engineer 공고 전문 | SOURCE NOT AVAILABLE | 담당업무/자격/우대/공개 전형의 원문 대응 검증 대기 |
| KIA-03 | 제조AI - 제조AI Agent 데이터 엔지니어링 경력 공고 | SOURCE NOT AVAILABLE. 과거 대화가 2차 아카이브를 언급했으나 원문 미회수 | 직무 선택은 확정, 상세 공개 사실은 검증 대기 |
| KIA-04 | Kia Values & Behaviors 공식 자료 | SOURCE NOT AVAILABLE | 캡처의 가치 명칭만으로 상세 행동 정의·평가 기준 복원 금지 |
| LEGACY-01 | 기존 talent_profile.json의 공개 출처 | V1에서 사용한 다른 공개 직무 자료 | 기아 해당 공고를 검증한 자료로 대체하지 않음 |

기아가 실제 공개한 사실과 PeopleOps의 해석을 분리한다.
가상의 조직·인원·Funnel·일정·평가·입사·온보딩은 SYNTHETIC이다.
실제 코드 계산 결과만 ANALYSIS로 표시한다. 아직 없는 결과를 예시 수치로 채우지 않는다.
원자료 자체의 외부 맥락을 제품 문구로 옮기지 않는다.
다른 프로젝트의 IA/Decision 파일, V1 영상·화면, 별도 2차 정리본을 기아/HR 원문으로 사용하지 않는다.

## 9. 결정 추적과 충돌 해결

설계 대화 출처는 기존 작업 `인사관리 입문 정리`의 handoff 발췌다.
사용자 최신 동기화 요청이 아래 회수본보다 우선하며 검색 인용 토큰은 원문 URL로 사용하지 않는다.

| 결정 근거 | 반영 | 충돌 해결 |
|---|---|---|
| Dataset v0.1 Rules Audit 및 후속 사용자 확정 | 06/07/08/09/10/11 | D-01, Stage 분리, Observation lineage, Capacity 이력, HOLD 후속검증, deadline Expiry, Work Evidence Ready, 독립 Validator |
| Dataset Open Issues Documentation Update | 09 주 SSOT, AGENTS·01~08·10·11 관련 부분 | OPEN-03/04/05/06/08 및 v0.1 범위 OPEN-12 해결. 기존 문서의 시간식·ID/Stage/Offer 계약·대표 생성 입력 해석 대체 |
| 최초 V2 동기화 요청 4~12, 40~43절 / 통합 af9a47b6-f146-486a-811a-0389bd35d3dc | AGENTS,00,01,05,06,11 | 설명 Office→Scene/Human Layer, 6단계/7공간, 예정 Jump 제한 |
| UI 최종 1ab926a2-fc44-4a3b-a1be-642157667133 | 05 | UI 규칙을 05로 통합. 초기 템플릿 조사와 구현 책임은 11로 이동 |
| 경험 확정·후속 선택, 07 매핑 c230760b-3cbb-4a23-a8a7-1a35d96ad215 | 06,07 | 대표 3명, 지원자 Mode, 2차 상세, 기술평가/AI 과제는 1차 활동 |
| AI 연결 확정 9e892e2d-d720-405f-8592-6a4b7a9d0707 | 03,08,09 | AI 후보와 사람의 연결·수준·최종 판단 분리 |
| 데이터 상세 e421340c-1dbe-4ba9-9f91-39329a3ada8c | 04,09 | 원문과 평가 분리, Event 파일 분할, 필드 정본을 09로 이동 |
| 경력 Mission 5fe4a9cf-f0e2-4d9c-97f0-865f4ae166f9 | 00,01,05,10 | 일반 EDA 종료→새 경력 조건과 계획 확정. 예시 수치 승격 금지 |
| Migration 62913ee6-4354-430e-b597-2bc81f025689 | 11 | 유지/확장/교체/신규를 현재 코드와 대조. 과거 제안 component를 현재 구현으로 오인하지 않음 |
| Source 보완 979042a8-9d11-4ce4-81d0-56fd2a849dea 및 실제 자료 확인 | 07,08,10,11 | 요약/원문/캡처 구분, 미확보 공개 사실을 OPEN으로 보존 |

## 10. 보존·이동·종료 기록

본 절은 최초 V2 Documentation Synchronization의 종료 기록이다.

보존: 독립 제품 정의, Evidence-first, 무로그인 공개 웹, Vercel/GitHub main 배포 목표,
외부 AI API 비의존, DB 비도입, Case JSON/Event CSV/Analysis JSON, seed 재현성,
Target 선행, 인과 단정 금지, JOINED≠READY, 16/12/4 FTE와 6개월 조건,
템플릿 License/Credit, 클릭·스크롤·접근성 원칙.

이동/대체: 04의 세부 필드·enum은 09, 05의 현재 구현/이관 표는 11,
옛 공간별 자유 진행과 Skill 분류·평가 구조는 최신 V2로 동기화했다.
각 문서는 소유 정의를 다른 문서에서 다시 확정하지 않고 참조한다.
기존 00~03과 AGENTS의 유효 구조는 유지하면서 수정·보완했고,
04/05는 책임 이동과 V2 충돌이 큰 부분을 재구성했다.

이번 작업의 완료 조건은 문서 00~11과 AGENTS 동기화, 전체 재검토,
Source Boundary·Open Issues 기록, 변경 보고다.
Application/source code, Dataset, package·deployment는 변경하지 않는다.
합성데이터 생성·Pandas 분석·v1 Freeze·UI 구현·배포로 진행하지 않고 STOP한다.

## 11. 후속 Dataset Generator v0.1 작업 기록

사용자 요청에 따라 오프라인 생성기·Validator·Sanity Report와 검토 후보를 생성했다.
결과를 Target에 맞춰 수정하지 않았다. 생성 규칙·schema·validator 오류만 수정 후 재실행하며,
정상적인 빈 입사/온보딩 결과는 그대로 보존한다.

이 작업은 최초 문서 동기화의 STOP 이후 별도로 승인된 범위다.
`data/synthetic/v1/`, 대표 Mapping, Mission 2 본 분석, UI는 구현하지 않았다.
기존 OPEN 7개와 출처 검증 상태는 변경하지 않는다.

## 12. Dataset v0.1 Rules Audit 후속 Documentation Sync

시간축: 최초 V2 문서 동기화 → v0.1 deterministic generation → 당시 자동 Validator PASS →
Rules Audit의 D-01 및 modeling issues 발견 → 사용자 계약 확정 → 06~11 실제 문서 반영.

현재 상태는 문서 동기화 완료, 새 Generation Rules/독립 Validator 구현 전, 새 Dataset 생성·검증·Freeze 전이다.
v0.1은 수정하지 않은 Audit history다. 대표 3명과 Mission 2 Main Analysis Story는 미선정이다.
Capacity/Offer lifecycle/Planned vs Actual Ready는 분석 후보일 뿐 선정된 Main Story가 아니다.
CLAUDE.template.md, 코드, 데이터, 생성 규칙, seed는 이번 Documentation Sync에서 변경하지 않는다.
AGENTS는 핵심 계약 참조만 최소 동기화한다. 00~05의 일반 원칙은 유지하고 세부 필드·Scene의 최신 정본은 06~11을 따른다.

## 13. Generator + Independent Validator vNext 후속 구현

사용자의 명시적 후속 요청에 따라 Generator와 독립 Validator를 구현하고 v0.2 검토 경로를 추가했다.
Raw Evidence→persisted Observation→Skill Decision→Final Review, Stage별 기준, Source Matrix,
Capacity 자원 결정/예약/해제/소비, HOLD 1회 후속검증/재검토, deadline Offer, 개인 Gap/업무 확인 Ready를 이관했다.
Validator는 생성기의 판단 함수를 oracle로 재사용하지 않는다.
세부 구현과 모델링 가정은 09 §9 및 scripts/mission1_dataset/README.md, 실제 자동 검증/수치는
`data/generation/v0.2/`의 manifest·validation_report·sanity_report에 기록한다.

v0.1과 기존 산출물은 Audit history로 보존한다. 새 후보는 UNREVIEWED, frozen=false이며
Rules/Reality Review·Freeze 승인·UI 연결·대표 선정·Mission 2 Main Analysis Story는 완료한 것으로 표시하지 않는다.
CLAUDE.template.md와 UI는 변경하지 않는다. 통합 OPEN/RESOLVED/출처 등록부의 상태는 유지한다.

## 14. Interview + Decision Model v0.3 승인 이관

2026-09-25 사용자 승인: 1차 3명·60분 단일 Session, 20×3=60h 면접 Initial, 필요시 별도 Calibration, 2차 2명·30분, 기술 핵심 Coverage 기반 진행, HOLD 질문 기반 targeted 수집. 07/09를 코드보다 먼저 갱신했다.
기존 80h/4h/80h panel 및 독립 재추출 Follow-up 설명은 v0.2 보존 이력이다. 상세 계약/구현 가정은 09를 따른다.
v0.1/v0.2는 불변, v0.3은 UNREVIEWED 검토 후보. Freeze·대표 선정·Mission 2 Main Story·UI 변경은 범위 밖이다.
공개 후기는 2차 Reference이며 원문/대표성 미검증이다. 1:3·60분/2차 30분을 기아 공식 운영 사실로 등록하지 않는다.

생성 실행 결과: seed 20260924의 v0.3 후보를 생성했고 독립 Validator/manifest 검사 PASS다.
1차 Session 173건(3명·60분), 2차 완료 37건(2명·30분); 면접 Initial 60h / Demand 576h / Additional 540h / Revised 600h / Consumption 519h / Released Reservation 57h.
FIRST 진입 192명 중 ADVANCED 45, FAILED 37, WITHDRAWN 5, IN_PROGRESS 105다. Offer 22, Join 11로 Target과 다르며 보존한다.
HOLD 15명은 targeted follow-up 후 진행 2/비진행 13으로 재검토됐고 HOLD 재발행은 없다.
실제 상세 검증/수치는 data/generation/v0.3의 산출물을 따른다. 자동 PASS는 Dataset Human Review·Freeze 승인이 아니다.

## 15. Final Dataset Candidate v0.4

최종 Human Review 결정을 07/09에 먼저 반영한다. Coverage는 직접 LIMITED를 포함한 판단 가능성이고 충분성과 별개다.
Calibration은 명시적 해석 차이/직접 충돌에 조건부 발생하며 MUST 판단불가능 상태의 Re-review Offer 진행을 금지한다.
30명 pool은 유지한 합성 parameter일 뿐 제품 정책이나 기아 운영 인원이 아니다.
v0.1/v0.2/v0.3, UI, AGENTS, CLAUDE.template은 보존한다. v0.4 생성·검증 후 STOP하며 자동 Freeze/대표 선정/Mission 2 분석을 하지 않는다.

실행 완료: v0.4 후보 생성·독립 Validator/manifest PASS, Python 회귀 114건 PASS, 별도 경로 재생성 25개 파일 바이트 동일, lint/build/HTML rendering PASS.
FIRST 진입192 / Coverage87 / Advanced59 / Failed37 / Waiting91 / Withdrawn5. Coverage에는 직접 limitation 비진행28명이 포함된다.
Calibration Eligible242 / Triggered144 / Actual144 / 72h이며 면접 예산과 분리했다.
면접 Initial60h / Demand576h / Additional540h / Revised600h / Consumed519h / Released57h.
Initial Final Proceed31 / DNP2 / HOLD18 → Targeted Follow-up18 → Re-review Proceed1 / DNP17 / Remaining HOLD0.
Offer32 / Join17 / Ready8(목표일까지1). Target에 맞추지 않고 결과를 보존한다.
확인된 제품 의미·데이터 정합성 Freeze blocker 없음. 합성 parameter/현실성 한계는 규칙·manifest에 남긴다.
상태는 UNREVIEWED, frozen=false이며 Dataset 승인/Freeze·대표 선정·Mission 2 분석을 수행하지 않았다.


## 16. Mission 1 Dataset v1 Baseline 승인

사용자의 명시적 Human Review 승인으로 v0.4 snapshot을 v1으로 승격한다. canonical 파일은 재생성 없이 동일 bytes로 보존하며
v0.1~v0.4·Generator·UI는 변경하지 않는다. Active Baseline과 승인시각은 `data/generation/baseline_registry.json`,
source provenance와 실제 검증 결과는 `data/generation/v1/`에서 확인한다. 기존 §15의 UNREVIEWED 상태는 source v0.4 이력이다.
v1은 현재 승인 Baseline이며 기아 실데이터/공식 정책이 아니다. snapshot을 직접 수정하지 않고 정당한 변경 사유가 있으면
새 Candidate→Validation→Human Review→새 Baseline으로 교체하며 과거 버전과 그 분석/Presentation을 보존한다(09 §6.3).
이번 범위는 승인 snapshot·합성 가정·Registry·Freeze 검증까지다. 대표 사례 선정, Presentation Mapping 생성,
Mission 2 분석 및 UI 연결은 별도 후속 작업이다.

## v0.5 Application / Document contract

KIA-02 supplement: PUBLIC REPOSTED SOURCE https://app.superpasshr.com/positions/0da4b528-75fb-4d56-989c-9190cd34dbd7 reproduces eligibility/preferred/job structure. Official https://career.kia.com/apply/applyView.kc?recuCls=39&recuType=N1&recuYy=2026 detailed body not retrieved; official-source verification remains pending. Dates are synthetic adaptations, not original employer dates. v0.5 requires Human Review; ACTIVE remains v1.
