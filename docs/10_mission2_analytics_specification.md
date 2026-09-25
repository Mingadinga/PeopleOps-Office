# PeopleOps Office — V2 Mission 2 Analytics & Experienced Recruiting

## 1. Mission 정의와 종료

새로운 경력직 인력요청 `제조AI - 제조AI Agent 데이터 엔지니어링`의 조건을 검토하고,
Mission 1 데이터를 실제 Python/Pandas로 분석한 뒤 재사용할 운영 Evidence와 재설계할 가정을
구분하여 다음 경력 채용계획을 수립한다. Dashboard/EDA 결과 표시만으로 종료하지 않는다.

직무 선택은 확정 제품 결정이다. 공개 업무·자격은 원문을 확인한 범위에서만 PUBLIC으로 쓴다.
인원·목표일·현재 Supply·Capability·Ramp-up은 SYNTHETIC이다.
과거 예시의 2명, 2028년 3월, 2개월은 확정값이 아니며 OPEN-07로 남긴다.
Mission 2의 종료는 계획 확정이다. 실제 경력 후보자 선발·Offer·Join·Ready 완료를 구현 범위에 추가하지 않는다.

## 2. 분석 입력과 재현성

[09](09_mission1_data_specification.md)의 freeze된 canonical v1과 해당 Case/Plan을 읽는다.
현재 승인 Baseline은 `data/generation/baseline_registry.json`의 v1(source v0.4)이다. 분석 결과와 Presentation Mapping은 `dataset_version`을 반드시 기록한다.
새 Baseline 승인 시 과거 결과를 자동 치환하지 않는다. 새 버전 분석/Mapping은 별도로 생성하고 v1의 결과는 보존한다.
Runtime과 분석의 버전이 같아야 한다. 필드·enum은 09를 참조하고 별도로 정의하지 않는다.
실제 Python/Pandas 코드가 Raw Event로부터 결과를 계산해야 한다.
분석 JSON·표·차트·문구의 수치가 코드와 일치하고 입력 버전·조건·기간·표본·단위를 추적할 수 있어야 한다.

Fake Code와 수작업으로 맞춘 결과는 금지다. 실제 코드로 사전 계산한 artifact는 임의 작성 결과와 구분한다.
브라우저에서 실시간 실행할지 사전 실행 결과를 탐색할지는 OPEN-01이다.
후자의 경우 실행 중이라는 가짜 로그 대신 실제 실행 기록과 결과 탐색임을 표시한다.
이 선택을 이유로 별도 서버/DB/외부 AI 의존성을 임의 도입하지 않는다.
이번 문서 동기화에서 코드·데이터를 생성하거나 분석하지 않았다.

## 3. Mission 2 Scene 흐름

아래 M2-01~12는 회수한 상세 설계의 Scene이다. 공통 Trigger는 이전 Scene 확인 후 다음 행동이며
첫 Scene은 Mission 1의 데이터 분석 시작 문맥에서 새로운 경력 요청 확인이다.
각 Scene은 클릭으로 진행하고 기록된 결과를 변경하지 않는다. UI는 [05](05_ui_specification.md)를 따른다.

| Scene | Core Question | Space / Participants | Human Layer / Interaction |
|---|---|---|---|
| M2-01 새 요청 | 이번에는 어떤 Capability가 언제 필요한가? | Mission Board / 현업 채용책임자·ICT 인사담당자 | 요청 확인, 공개 직무와 합성 조건 구분 |
| M2-02 Capability Gap | 몇 명과 어떤 수행 수준이 부족한가? | 인력계획실 / 현업·HR | 필요/현재 Capability·Timing·육성 여력 비교 |
| M2-03 이전 데이터 | 이전 채용에서 무엇을 배울 수 있는가? | 데이터랩 / HR·인사 데이터 분석가 | Dataset 버전·파일·실제 행 수·검증 기록 확인 |
| M2-04 Workforce | 목표시점 공급과 Target은 어떻게 다른가? | 데이터랩 / HR·분석가 | 코드·결과·Target/Actual/Difference 탐색 |
| M2-05 Funnel | 어느 구간에서 계획과 결과가 다른가? | 데이터랩 / HR·분석가 | 버킷 대응과 FAILED/WITHDRAWN 분리 확인 |
| M2-06 Drill-down | 무엇을 더 확인할 필요가 있는가? | 데이터랩 / HR·분석가 | 실제 패턴에 따른 Lead Time·채널·Initial/Revised/Actual Capacity·Offer lifecycle·Planned vs Actual Ready 후보 분석 |
| M2-07 가설 | 관찰한 관계를 어떤 질문으로 검증할 것인가? | 데이터랩 / HR·분석가 | 관찰→가설→조건/표본 확인→추가 분석 |
| M2-08 한계·개선 | 어디까지 말할 수 있고 무엇을 더 측정할 것인가? | 데이터랩 / HR·분석가 | 사실·가능 해석·미확인·추가 데이터와 개선 연결 |
| M2-09 Context 전환 | 신입 결과를 이번 경력 요청에 적용할 수 있는가? | 전략 논의 / HR·현업 | 대상·수준·Ramp-up·Pool 비교, Think Before Reveal 가능 |
| M2-10 Transfer | 어떤 운영 근거를 재사용하고 어떤 가정을 바꾸는가? | 채용전략실 / HR·채용담당자·현업 | Evidence와 새 가정을 분리 |
| M2-11 경력 설계 | 필요한 수행 Evidence와 확보·검증 방식은 무엇인가? | 채용전략실·평가회의실 / HR·채용담당자·현업 | Profile·Sourcing·Funnel·Capacity·Assessment 설계 근거 탐색 |
| M2-12 계획 확정 | 다음 채용에서는 무엇을 실행하고 측정할 것인가? | Mission Board / HR·현업 | 계획과 적용 근거·제약·측정 계획 확인 |

| Scene | Decision Layer / Evidence | Decision / State Transition / Next Question |
|---|---|---|
| M2-01 | 직무 자료 상태와 SYNTHETIC 요청 변수 | 요청을 검증 대상으로 둠 → M2-02 현재 Capability는? |
| M2-02 | Required Skill Depth·Experience·Independence·Internal Supply·Mentoring·Timing·Scarcity | Headcount와 Capability Gap 구분 → M2-03 이전 운영에서 배울 것은? |
| M2-03 | manifest·Case·CSV, 실제 검증 기록 | 분석 입력과 한계 확인 → M2-04 목표 공급 결과는? |
| M2-04 | Plan과 READY_CONFIRMED Event의 실제 계산 | WHAT 확인, 원인 단정 없음 → M2-05 어느 구간에서 달랐나? |
| M2-05 | 계획/Actual·분자/분모·FAILED/WITHDRAWN | 추가 확인 Stage 선택, 병목 원인 단정 금지 → M2-06 무엇을 더 볼까? |
| M2-06 | 실제 표/분포/코드와 표본 | 의미 있는 패턴 또는 관계 없음 확인 → M2-07 어떤 가설인가? |
| M2-07 | 관찰·검증 조건·대안 해석·결측 | 가설 지지/미확인과 한계 보존 → M2-08 무엇을 개선/측정할까? |
| M2-08 | 불확실성과 추가 데이터, 다음 검증 가능한 개선 | Analysis→Hypothesis→Action→Measurement → M2-09 새 모집단에도 적용되나? |
| M2-09 | 신입/경력의 조건 비교 | 그대로 일반화하지 않음 → M2-10 재사용/재설정은? |
| M2-10 | Process Evidence와 Population Assumption | 적용 이유와 재설계 대상 기록 → M2-11 새 인재 요건/계획은? |
| M2-11 | 공개자료/해석/합성 계획, Experience Evidence | 새로운 조건에 맞춘 계획 근거 → M2-12 무엇을 측정할까? |
| M2-12 | Need·Gap·Profile·재사용 근거·새 가정·전략·Capacity·Join/Ready 목표·측정 계획 | 경력 채용계획 확정 → Mission 종료. 실행 완료 아님 |

Mission 2의 상위 6단계 표시 방식은 OPEN-02다. 분석 Scene 번호와 채용 Stage를 같은 것으로 표시하지 않는다.

## 4. 분석 질문과 Metric 계약

모든 지표에 분석 질문, 대상 모집단/기간, 분자·분모, 단위, 입력 필드, 결측·중복 처리,
계산 코드·결과 참조가 필요하다. 분모가 없거나 정의가 미완성이면 수치를 만들지 않는다.
아래는 기존 설계의 분석 후보와 계약이다. 새 KPI Target이나 결과를 확정한 표가 아니다.

| 질문 / 지표 | 입력·계산 | 해석과 경계 |
|---|---|---|
| 목표일 Workforce Fulfillment | Plan의 baseline/confirmed Flow Forecast + 목표일까지 READY_CONFIRMED인 신규 인력, 이를 Demand로 나눔 | 같은 인력 중복 금지. JOINED만으로 가용 Supply에 더하지 않음 |
| 지원완료율 | applications의 제출 완료 고유 candidate / 시작 고유 candidate, 동일 cohort | started_at/submitted_at 사용. 240/320은 계획 |
| Target vs Actual Funnel | 09의 Target 라벨에 맞춰 applications/Stage/Offer/Workforce의 고유 candidate 집계 | 서류·사전검증 통과와 면접 대상 구분. Activity/Event 개수로 인원 집계 금지 |
| Stage Entered/Completed/Advanced/Failed/Withdrawn/In Progress | stage_history의 entered_at/completed_at와 result | lifecycle과 결과가 중첩될 수 있으므로 모두 더하지 않음 |
| Stage Advancement / Failure / Withdrawal Rate | 각각 Advanced / Entered, Failed / Entered, Withdrawn / Entered | 동일 Stage 진입 cohort. WITHDRAWN을 분모에서 빼지 않음 |
| Stage Lead Time | notified_at - entered_at | 확정 결과 통보까지의 시간 |
| Scheduling Wait | scheduled_at - invited_at | 참여 안내와 예정 활동 시각 사용 |
| Decision Time | decision_at - completed_at | 요구 활동 완료부터 결과 확정까지 |
| Notification Delay | notified_at - decision_at | 결과 확정부터 결과 통보까지 |
| Actual person-hours | activity_participants의 대상 역할 참여 구간 합 / 3600초 | v0.3 Plan의 면접 60시간·후보당 3시간과 구분. 중복 구간/지원자 시간을 평가자 effort에 더하지 않음 |
| Offer | offers와 offer_events의 Offered/Accepted/Declined/Expired/Pre-join Withdrawal | 객체와 응답 이력 구분. JOINED는 Offer Event 아님 |
| Joined / Ready / Join→Ready Lead Time | workforce_events의 JOINED/READY_CONFIRMED, 두 effective_at의 차 | 목표일·관측창·연장·미완료 구분. 미확인 Ready를 만들지 않음 |

| 추가 분석 후보 | 입력·계산 | 해석과 경계 |
|---|---|---|
| Initial Interview Capacity | interview_capacity_events의 INITIAL_PLAN | 버전별 최초 계획 보존(v0.3 60h, v0.2 80h) |
| Capacity Demand / Gap | 필요 모집단 × unit effort, 같은 시점·범위의 가용량과 비교 | 09 §4.17의 전체/미배정 범위를 구분. Skill 부족 아님 |
| Revised Capacity | Initial + Added − Released | Human Capacity Decision 이력과 연결 |
| Actual / Capacity Variance | 실제 평가자 참여시간 및 Actual − Revised | Plan 단위로 결측 보간 금지. 효율 원인 단정 금지 |
| Offer lifecycle | offered_at·response_deadline·Response Event·observation_end | deadline 전 Open과 파생 EXPIRED, DECLINED와 NO_RESPONSE 구분 |
| Planned vs Actual Ready | planned_ready_at와 READY_CONFIRMED.effective_at | 미확인 Actual은 NULL/Not Yet Ready. post-join Evidence·Human Confirmation 확인 |

Calibration은 Eligible/Triggered/Actual과 실제 참여 person-hours를 분리한다. 발생 여부를 후보자 품질로 해석하지 않는다.
Capacity·Offer·Ready는 Drill-down 후보이며 Main Analysis Story로 선정한 것이 아니다.
v0.3은 부모 면접 Session의 참여시간만 면접 effort로 합산하고 필요시 Calibration 비용을 별도 표시한다.
v0.4에서는 FIRST decisionable Coverage(LIMITED 포함)와 Skill Sufficiency/ADVANCED/FAILED/IN_PROGRESS를 분리하고 targeted HOLD 질문·응답·잔여 불확실성을 추적한다.
버전 비교는 규칙/시간/모집단 변화가 함께 있으므로 단일 원인 효과로 단정하지 않는다.

v0.2 검토 후보의 Capacity/Funnel Decision Note는 09 §3.2/4.17/5.2/6.3을 따른다.
동일 FIRST_INTERVIEW 범위에서 Initial 80h, Demand 768h, Gap 688h, Human Decision에 따른
추가 720h와 Revised 800h, 실제 소비 590.3333h를 비교한다. 미사용 reservation 해제 177.6667h는
cycle 예산 회수나 음의 소비가 아니므로 중복 차감하지 않는다. 수요·결정 시점·모집단·참여구간을 함께 제시한다.

Target Funnel은 계획값이며 Actual은 사건과 합성 사람 판단 결과다. **Target Join 4 / Actual Join 56**의
큰 편차도 그대로 보존한다. 이를 맞추기 위한 데이터·판단 규칙·seed/확률·Revised Capacity 사후 조정을 금지한다.
현재 코드의 Capacity 산식은 Join 목표를 사용하지 않지만, 추가 pool은 일정과 관측창 내 완료 가능성에 영향을 줄 수 있다.
운영 선택의 현실성과 편차는 Dataset Human Review 및 승인·Freeze 이후 Mission 2의 분석 대상이다.
이 기록은 v0.2의 기술적 근거 확인이며 Freeze된 분석 입력의 승인이나 Main Analysis Story 선정이 아니다.
FINAL_REVIEW는 lifecycle과 final_decisions를 별도로 분석하며 Stage ADVANCED/FAILED로 최종 합불을 복제하지 않는다.

시간 의미·관측창·분모의 주 SSOT는 [09](09_mission1_data_specification.md)다.
Asia/Seoul offset-aware timestamp와 manifest의 observation_start/observation_end를 사용한다.
필요한 시각이 NULL이면 지표도 NULL이며 보간하지 않는다. 관측 종료까지 미확정 결과는 IN_PROGRESS다.
평가 완료자 중 통과율 등 다른 질문은 Metric 이름과 분모를 따로 명시한다.

OPEN-12는 Dataset v0.1 KPI/원자료 계약 범위에서 해결됐다. 아직 실제 결과를 계산한 것은 아니다.
source_channel·Observation·Calibration 및 근거 원자료를 보존하되 채널 성과·Attraction 효율·Calibration 합의율·
특정 Assessment 효과를 Main KPI로 미리 확정하지 않는다. 채널은 Quality 대리변수가 아니다.
Observation은 evidence_id로 Raw Evidence를, Skill Decision은 skill_decision_observations로 하나 이상의 저장된 Human Observation을 추적한다.
Raw Evidence → Observation → Skill Decision의 계보를 보존한다. 기존 Human Decision의 규칙·Process는 분석할 수 있으나
원자료를 Python으로 재평가·점수화하여 새로운 후보자 평가나 Ranking을 만들지 않는다.
입력 없는 Visit Rate/Qualified Application 등 지표를 추가하지 않는다.

## 5. 분석·가설·한계

관찰된 사실 → 가능한 해석 → 미확인 사항 → 추가 데이터 → 개선·측정 순서로 설명한다.
상관관계를 원인으로 단정하지 않는다. 작은 표본에는 표본 수와 한계를 표시한다.
UNKNOWN/Missing을 임의 사유나 정상 상태로 채우지 않는다.
개인의 합격·성과·퇴사를 예측하지 않는다.

Lead Time과 Withdrawal 관계는 후보 질문이지 예정된 결론이 아니다.
시간 구간 비교는 실제 timestamp 의미·누락·이탈 전 노출 기간을 먼저 확인해야 한다.
과거 대화의 예제 코드는 is_withdrawn 미정의, Stage/Plan enum 불일치 등 검토가 남아 있어
실행 가능한 분석 정본으로 복사하지 않는다(OPEN-11). 실제 코드는 후속 작업에서 09 계약에 맞춰 검증한다.

Rule-based 합성 데이터의 생성 가정을 현실 조직에 대한 인과 발견처럼 표현하지 않는다.
예상과 다른 결과나 관계 없음도 정상 결과다. Main Story를 위해 Dataset을 수정하지 않는다.

## 6. Main Analysis Story

Dataset 후보 생성·검토·승인·v1 Freeze → 실제 분석 → 의미 있는 패턴 확인 → Main Story 2~3개 선택.
다른 분석은 추가 분석 보기로 둘 수 있다. 지금은 분석 질문과 방법만 정의한다.
어느 단계의 이탈이 높다거나 Ready가 몇 명인지 미리 서술하지 않는다.
Mission 1 개선은 근거·대안·재검토 조건과 다음 측정 계획을 포함한다.

## 7. 신입과 경력의 Context 차이

Headcount Gap + Capability Gap을 함께 본다.
Required Capability, Skill Depth, Experience Context, Independence, Ramp-up Tolerance,
Internal Capability Supply, Mentoring Capacity, Target Ready Date, Talent Scarcity를 검토한다.
경력이라는 이름만으로 즉시전력이라고 가정하지 않는다.

Experience Evidence: Technology → Context → Scale → Ownership → Decision → Problem → Action → Result.
어떤 환경·규모에서 본인이 무엇을 판단·수행했고 무엇으로 결과를 확인했는지 탐색한다.
경력연수는 맥락일 수 있으나 Capability Score가 아니다.
원문이 확인되기 전 Kafka/Spark 등 개별 기술을 기아의 공식 Must로 확정하지 않는다.

## 8. Transferable Evidence와 새 계획

| 재사용을 검토할 Process Evidence | 다시 설정할 Population Assumption |
|---|---|
| 평가자 person-hours, Scheduling Delay, 통보 Lead Time | Funnel 전환, 지원완료율, 채널 전환 |
| Calibration 방식, Candidate Communication, 평가 운영비용 | Pool 규모, 인재 요건, 평가 기준, Offer Acceptance, Ramp-up |

재사용 가능한 종류라는 뜻이지 실제 관측값이 확보되었다는 뜻이 아니다.
**과거 데이터는 다음 채용의 정답이 아니라 다음 계획의 Evidence다.**

필요시 Target Pool → SOURCED → CONTACTED → RESPONDED → INTERESTED → APPLIED
→ Assessment → Offer → Join → Ready를 계획한다.
이는 PeopleOps Office의 경력 시나리오이며 실제 기아 내부 Sourcing 과정이 아니다.
경력 Event Dataset 확장은 후속 범위다. 이번 Mission은 실행 대신 계획을 확정한다.

Assessment는 Architecture Discussion / Technical Deep Dive / Incident Discussion /
Experience Interview 등 실제 수행 Evidence를 확인하는 시나리오 방식을 검토한다.
신입 Funnel과 평가표를 복사하지 않는다.
최종 계획에는 Need·Capability Gap·Profile·재사용 근거·새 가정·Sourcing·Funnel·Capacity·Assessment·
Target Join/Ready·측정 계획을 연결한다. Response/Qualified Interest/Stage Conversion/대기/이탈/Offer/Ready 등
기존 후보 중 어떤 질문을 위해 무엇을 측정할지 정하며 수치 Target은 미리 만들어 넣지 않는다.

## 9. 구현 전 남은 결정

OPEN-03/04/05/06/08/12의 데이터 의미 계약은 09에 확정됐다. 세부 구현 표현은 해당 Implementation Notes를 따른다.
OPEN-01 실행 방식, OPEN-02 진행도, OPEN-07 경력 시나리오 수치, OPEN-10 원문, OPEN-11 코드 검증은
[11 통합 등록부](11_v2_migration_specification.md#7-open-issues)를 따른다.
이 문서는 분석 설계이며 실제 데이터 분석을 완료했다는 보고가 아니다.
