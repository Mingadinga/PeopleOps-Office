# PeopleOps Office — V2 HR Tech / Human Decision Boundary

## 1. 원칙과 범위

**People make decisions. Technology organizes evidence.**
HR Tech는 별도 방·AI 캐릭터가 아니라 필요한 Scene의 PC·모니터·지원자 화면에 나타나는 보조 도구다.
계산·검색·정리·연결 후보·초안·설명을 지원한다. AI 출력 자체는 Evidence가 아니며
지원 답변·과제 결과·면접관 관찰·실제 업무 결과를 대체하지 않는다.
원문으로 돌아가는 경로를 유지한다. 제품은 사전에 구성한 Case 탐색 서비스이며 실운영 ATS가 아니다.

HR Tech는 `Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision`를 지원하며 우회하지 않는다.
Capacity Gap·deadline 경과의 계산과 Skill/Final Hiring/READY_CONFIRMED의 Human Decision을 구분한다.

## 2. 기능별 입력과 권한

| 기능 / Scene | 입력 | 시스템·AI 보조 출력 | 사람이 담당하는 결정 |
|---|---|---|---|
| 공고 점검 / 채용공고 | 초안·인재 요건·업무정보 | 모호한 표현·내부용어·긴 문장·요건 혼재 표시, 수정안 | 최종 공고 문구 |
| 지원 안내 / 지원자 화면 | 제공된 공개 채용정보와 명시적 시나리오 안내 | 관련 정보 검색·설명. 공개정보와 시나리오 표시 분리 | 합격 가능성 판단을 제공하지 않음 |
| Funnel / Capacity | Initial Plan·Demand·Capacity 이력·참여시간 | Gap·Revised·Actual 산술, 대안 정리 | Resource 추가·기간 조정·평가방식 변경 |
| 서류 | SELF_REPORTED 답변·명시적 요건 | 관련 경험·Evidence Candidate·후속검증 지점 표시 | DOCUMENT_SCREEN 진행과 검증 질문 |
| 평가 근거 정리 / 면접 | 원본 Evidence·Skill 정의 | 관련 Skill 후보·원문 연결 | 연결 확정·Evidence 수준 |
| Calibration / 평가회의 | persisted Observation·Verification Mode·Context·원문·Rubric | Evolution/Context Difference/Disagreement 표시 | AGREED / DISAGREEMENT_REMAINS / INSUFFICIENT_EVIDENCE |
| 최종검토 | Must·근거·불확실성·Learnable Gap | Coverage·누락 근거 정리 | Offer 진행/보류/미진행 |
| HOLD / Follow-up | Reason·기존 Observation·미확인 질문 | 관련 Evidence와 새 근거 연결 | Resolution Plan·최대 1회 검증·새 Observation·Calibration·Re-review |
| Offer / 운영 | response_deadline·확인된 Response Event·관측창 | Open/EXPIRED 상태 계산 | Offer 결정·확인된 사유 기록 |
| 온보딩 / 업무공간 | 업무 관련 Evidence·Gap·Task | 체크리스트·문서·일정·계획 초안 | Ramp-up 확정 |
| Ready / 업무공간 | 개인별 Gap·planned_ready_at·post-join Work Evidence | Planned vs Actual·요건 정리 | 멘토/현업의 READY_CONFIRMED |
| Data Lab | canonical Dataset·실제 코드·결과 | Python 계산·질문·설명 보조 | 해석·가설·개선·다음 계획 |

v0.3의 FIRST 핵심 Coverage A/B/C/D, 필요한 Calibration, HOLD 질문별 후속검증은 07/09를 따른다. 근거 부족을 자동 탈락 또는 자동 진행으로 바꾸지 않는다.
v0.4 Coverage는 직접 LIMITED도 포함할 수 있는 판단 가능 여부이며 합격 점수가 아니다. Calibration 발생 여부는 품질 신호가 아니며 MUST 판단불가능 상태를 uncertainty accepted로 숨겨 Offer 진행하지 않는다.
계산된 Coverage는 사람의 종합 능력 점수가 아니다. HR이 원문과 불확실성을 검토하도록 돕는다.

## 3. 평가 근거 연결 계약

원본 Evidence → AI의 관련 Skill 후보 → 사람의 연결 확정 → 사람의 Evidence 수준 판단.
사람은 후보를 수락·수정·거부하거나 AI 제안 없이 직접 연결할 수 있다.
AI는 `알고리즘 구현·검증과 관련될 가능성`을 제안할 수 있지만 `제한적` 등 수준을 판정하지 않는다.
확인되지 않음 / 제한적 / 충분 / 강함은 사람의 판단이며 숫자화하지 않는다.

원본, suggested_skill_id, confirmed_skill_id, 확인 상태·주체·시각, 평가자 관찰을 분리한다.
실제 필드와 enum은 [09](09_mission1_data_specification.md)가 소유한다.
Calibration에서도 AI는 원근거를 찾아줄 뿐 재평가하거나 평균으로 합의를 만들지 않는다.
사람의 수정/거부 기록은 원문과 AI 제안을 덮어쓰지 않는다.
이 업무 흐름은 Case 안의 가상 사람 판단 시나리오를 뜻하며 제품 사용자의 클릭으로 실제 결과를 바꾸지 않는다.
Synthetic Evidence·Human Observation·Human Decision은 모두 SYNTHETIC이다.
Generator가 Evidence/Rubric 기반 판단 시나리오를 생성하는 것과 제품 AI가 실제 지원자를 평가하는 것을 구분한다.
판단에는 SYNTHETIC_HUMAN_SCENARIO provenance를 남기고 실제 사람의 평가라고 표현하지 않는다.
Dataset Reviewer는 개별 합불이 아닌 생성 규칙·근거 추적·정합성·현실성과 hidden score 부재를 검토한다.

## 4. 공고 점검과 지원 안내

공고 점검은 문제 문장과 관련 인재 요건을 연결해 보여준다. 표시 건수는 실제 Case/검사 결과와 일치해야 한다.
수정안은 제안이며 자동 확정하지 않는다. Textio는 HR Tech 참고 사례일 뿐 직접 연동·점수 제공을 뜻하지 않는다.

지원 안내는 제공 정보 범위 안에서 직무·준비 자료·전형을 설명한다.
공개 사실과 합성 안내를 혼합하지 않는다. 근거가 없으면 확인 불가로 답한다.
지원자에게 합격 가능성·점수·유리한 답안을 예측하지 않는다.

## 5. 온보딩 정보 경계

Selection Evidence에서 업무 관련 Skill과 확인할 Gap만 초기 계획에 연결한다.
Values 답변 원문·주관적 인상·합불 논의를 멘토에게 일괄 전달하지 않는다.
입사 후 실제 업무에서 재확인할 수 있어야 한다.
체크리스트 완료·자동 일정 계산이 Ready 확인을 대신하지 않는다.
알림·상태 관리 표현은 시나리오 범위이며 외부 실발송 기능을 추가하지 않는다.

## 6. HR Copilot

기본은 접힌 보조 진입점이다. Scene 질문, 기록된 Decision, Plan, 데이터와 Evidence를 바탕으로 답한다.
응답 구조는 결론 → 근거 → 출처 → 불확실성이다.
관련 자료·계산 과정·원문을 열 수 있어야 한다.
근거가 없으면 `현재 제공된 데이터에서는 확인할 수 없습니다.`라고 답한다.
미확인 사유나 기업 내부 제도를 추정하지 않는다.

핵심 설명은 정적/규칙 기반으로 제공할 수 있으며 외부 AI API를 필수로 만들지 않는다.
외부 LLM 도입은 후속 범위다. 도입하더라도 서버 측 호출과 Secret 비노출 원칙을 지킨다.
응답/원문 오류가 Mission 탐색을 막지 않는다.

## 7. 금지와 검증

AI 자동 합불·Ranking·Fit/Culture Fit Score·개인 성공/성과/퇴사 예측·보호특성 활용·얼굴/음성/표정 성향 분석을 금지한다.
숨은 종합 능력치, Evidence 없는 추론, 미확인 이탈 사유 추정을 만들지 않는다.

SELF_REPORTED만으로 STRONG Skill Decision을 확정하거나 Raw Evidence를 재해석해 Observation을 우회하지 않는다.
Capacity 부족으로 자동 탈락시키거나 HOLD를 terminal outcome으로 처리하지 않는다. RE_REVIEW의 HOLD 재발행을 금지한다.
NO_RESPONSE에서 철회·거절·motive를 추론하지 않는다. Planned Ready 경과나 Task 완료만으로 READY_CONFIRMED를 자동 생성하지 않는다.
합성 Generator의 시나리오 생성도 09의 계약과 독립 Validator를 따라야 하며 제품 AI의 평가 권한을 뜻하지 않는다.

후속 구현에서 확인할 조건:

- 모든 보조 결과에서 원자료·관련 Decision을 추적할 수 있다.
- AI 후보와 사람의 확인·수준·판단이 UI와 데이터에서 구분된다.
- 사람이 AI 제안을 수정·거부해도 원문과 제안 기록이 유지된다.
- AI 기능을 제거해도 핵심 Mission과 실제 계산 결과 탐색이 가능하다.
- System Reveal은 사람 대화에 적용되지 않으며 Skip/reduced motion을 지원한다.

## 8. 참고자료와 미결정

HR Tech 스캔본은 개념 참고자료, 별도 요약 PDF는 2차 자료다.
이번 설계 동기화는 특정 HR Tech 제품의 기능·연동을 새로 검증하거나 구현한 작업이 아니다.
자료 위치와 확인 범위는 [11 출처 등록부](11_v2_migration_specification.md#8-출처-등록부)를 따른다.
OPEN-06은 합성 판단 시나리오와 실제 Dataset 규칙 검토의 구분으로 해결됐다.
필드·Rubric 기반 생성·검토 계약은 09를 따르며 제품 AI의 평가 권한을 늘리지 않는다.
